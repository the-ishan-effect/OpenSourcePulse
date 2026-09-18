import csv
import random
import sys
import time
from pathlib import Path

import requests

sys.path.append(str(Path(__file__).resolve().parent))

from github_client import BASE_URL, HEADERS


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_FILE = PROJECT_ROOT / "data" / "raw" / "repositories.csv"
SAMPLING_LOG = PROJECT_ROOT / "data" / "raw" / "sampling_log.csv"

RANDOM_SEED = 42

# Number of repositories finally selected from each popularity stratum.
STRATA = [
    ("P1_100_499", "stars:100..499", 35),
    ("P2_500_999", "stars:500..999", 35),
    ("P3_1000_2499", "stars:1000..2499", 35),
    ("P4_2500_4999", "stars:2500..4999", 35),
    ("P5_5000_9999", "stars:5000..9999", 35),
    ("P6_10000_24999", "stars:10000..24999", 35),
    ("P7_25000_49999", "stars:25000..49999", 30),
    ("P8_50000_99999", "stars:50000..99999", 25),
    ("P9_100000_199999", "stars:100000..199999", 15),
    ("P10_200000_plus", "stars:>=200000", 20),
]

# We retrieve several pages to create a broader candidate frame.
PAGES_PER_STRATUM = 2
RESULTS_PER_PAGE = 100


def search_repositories(
    query: str,
    page: int,
) -> list[dict]:
    """Retrieve one page of GitHub repository search results."""

    url = f"{BASE_URL}/search/repositories"

    params = {
        "q": query,
        "per_page": RESULTS_PER_PAGE,
        "page": page,
    }

    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()["items"]


def get_repository(owner: str, repo: str) -> dict:
    """Retrieve detailed metadata for one repository."""

    url = f"{BASE_URL}/repos/{owner}/{repo}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


def is_eligible(repository: dict) -> bool:
    """Return True when a repository satisfies our inclusion criteria."""

    if repository.get("fork", False):
        return False

    if repository.get("archived", False):
        return False

    if repository.get("id") is None:
        return False

    if repository.get("created_at") is None:
        return False

    return True


def extract_repository(repository: dict) -> dict:
    """Convert GitHub metadata into the OpenSourcePulse raw schema."""

    license_info = repository.get("license")

    return {
        "repo_id": repository.get("id"),
        "repo_name": repository.get("name"),
        "owner": repository.get("owner", {}).get("login"),
        "full_name": repository.get("full_name"),
        "description": repository.get("description"),
        "html_url": repository.get("html_url"),
        "language": repository.get("language"),
        "topics": "|".join(repository.get("topics", [])),
        "license": (
            license_info.get("spdx_id")
            if license_info
            else None
        ),
        "created_at": repository.get("created_at"),
        "updated_at": repository.get("updated_at"),
        "pushed_at": repository.get("pushed_at"),
        "stars": repository.get("stargazers_count"),
        "forks": repository.get("forks_count"),
        "watchers": repository.get("watchers_count"),
        "open_issues": repository.get("open_issues_count"),
        "size_kb": repository.get("size"),
        "default_branch": repository.get("default_branch"),
        "is_fork": repository.get("fork"),
        "archived": repository.get("archived"),
    }


def build_candidate_pool() -> tuple[list[dict], list[dict]]:
    """Build and randomize candidate repositories for every stratum."""

    random.seed(RANDOM_SEED)

    all_candidates = []
    sampling_records = []

    for stratum, query, target in STRATA:

        print()
        print(f"Stratum: {stratum}")
        print(f"Query  : {query}")
        print(f"Target : {target}")

        candidates = []

        for page in range(1, PAGES_PER_STRATUM + 1):

            items = search_repositories(
                query,
                page,
            )

            candidates.extend(items)

            print(
                f"  Page {page}: "
                f"{len(items)} repositories"
            )

            time.sleep(0.3)

        # Deduplicate by GitHub repository ID.
        unique = {}

        for repository in candidates:

            repo_id = repository.get("id")

            if repo_id is not None:
                unique[repo_id] = repository

        candidates = list(unique.values())

        print(
            f"  Unique candidates: "
            f"{len(candidates)}"
        )

        # Randomize candidate order.
        random.shuffle(candidates)

        # Store enough candidates for the target.
        retained = candidates[:target]

        print(
            f"  Candidate selection: "
            f"{len(retained)}"
        )

        for repository in retained:

            repository["_sampling_stratum"] = stratum

            all_candidates.append(repository)

            sampling_records.append(
                {
                    "repo_id": repository.get("id"),
                    "full_name": repository.get("full_name"),
                    "popularity_stratum": stratum,
                    "search_query": query,
                    "selection_method": (
                        "randomized_multi_page_candidate_selection"
                    ),
                    "random_seed": RANDOM_SEED,
                }
            )

    return all_candidates, sampling_records


def collect_final_sample() -> None:

    print()
    print("OpenSourcePulse — Final Repository Sampler")
    print("=" * 65)

    candidates, sampling_records = build_candidate_pool()

    print()
    print("=" * 65)
    print(
        f"Repositories entering eligibility check: "
        f"{len(candidates)}"
    )
    print("=" * 65)

    collected = []
    seen_ids = set()

    for index, candidate in enumerate(
        candidates,
        start=1,
    ):

        full_name = candidate.get("full_name")

        if not full_name:
            continue

        owner, repo = full_name.split("/", 1)

        print(
            f"[{index:03d}/{len(candidates):03d}] "
            f"Checking {full_name}"
        )

        try:

            repository = get_repository(
                owner,
                repo,
            )

            if not is_eligible(repository):

                print(
                    "    Excluded: "
                    "fork/archived/invalid"
                )

                continue

            repo_id = repository.get("id")

            if repo_id in seen_ids:

                print(
                    "    Excluded: "
                    "duplicate ID"
                )

                continue

            collected.append(
                extract_repository(repository)
            )

            seen_ids.add(repo_id)

            print("    Included")

        except requests.RequestException as error:

            print(
                f"    ERROR: {error}"
            )

        time.sleep(0.2)

    fields = [
        "repo_id",
        "repo_name",
        "owner",
        "full_name",
        "description",
        "html_url",
        "language",
        "topics",
        "license",
        "created_at",
        "updated_at",
        "pushed_at",
        "stars",
        "forks",
        "watchers",
        "open_issues",
        "size_kb",
        "default_branch",
        "is_fork",
        "archived",
    ]

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fields,
        )

        writer.writeheader()
        writer.writerows(collected)

    with SAMPLING_LOG.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        log_fields = [
            "repo_id",
            "full_name",
            "popularity_stratum",
            "search_query",
            "selection_method",
            "random_seed",
        ]

        writer = csv.DictWriter(
            file,
            fieldnames=log_fields,
        )

        writer.writeheader()
        writer.writerows(sampling_records)

    print()
    print("=" * 65)
    print("FINAL COLLECTION COMPLETE")
    print("=" * 65)
    print(f"Rows collected : {len(collected)}")
    print(f"Repository CSV : {OUTPUT_FILE}")
    print(f"Sampling log   : {SAMPLING_LOG}")
    print("=" * 65)


if __name__ == "__main__":
    collect_final_sample()