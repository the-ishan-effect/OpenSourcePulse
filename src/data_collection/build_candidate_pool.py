import csv
import random
import sys
import time
from pathlib import Path

import requests

sys.path.append(str(Path(__file__).resolve().parent))

from github_client import BASE_URL, HEADERS


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "candidate_repositories.csv"
)

RANDOM_SEED = 42

CANDIDATES_PER_STRATUM = 100


POPULARITY_STRATA = {
    "S1_100_999": "stars:100..999",
    "S2_1000_9999": "stars:1000..9999",
    "S3_10000_99999": "stars:10000..99999",
    "S4_100000_plus": "stars:>=100000",
}


def search_repositories(
    query: str,
    page: int,
    per_page: int = 100,
) -> list[dict]:

    url = f"{BASE_URL}/search/repositories"

    params = {
        "q": query,
        "per_page": per_page,
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


def collect_candidates() -> list[dict]:

    random.seed(RANDOM_SEED)

    all_candidates = {}

    for stratum, query in POPULARITY_STRATA.items():

        print()
        print(f"Collecting candidate pool: {stratum}")
        print(f"Query: {query}")

        candidates = []

        # Two independent pages give us a broader candidate frame.
        for page in [1, 2]:

            items = search_repositories(
                query,
                page=page,
                per_page=100,
            )

            candidates.extend(items)

            time.sleep(0.5)

        # Deduplicate.
        unique = {}

        for repository in candidates:

            full_name = repository.get("full_name")

            if full_name:
                unique[full_name] = repository

        candidates = list(unique.values())

        print(
            f"Candidates retrieved: "
            f"{len(candidates)}"
        )

        random.shuffle(candidates)

        selected = candidates[
            :CANDIDATES_PER_STRATUM
        ]

        for repository in selected:

            full_name = repository["full_name"]

            repository["_sampling_stratum"] = stratum

            all_candidates[full_name] = repository

        print(
            f"Candidates retained: "
            f"{len(selected)}"
        )

    return list(all_candidates.values())


def save_candidates(candidates: list[dict]) -> None:

    OUTPUT_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    fields = [
        "id",
        "name",
        "full_name",
        "owner",
        "html_url",
        "description",
        "language",
        "created_at",
        "updated_at",
        "pushed_at",
        "stargazers_count",
        "forks_count",
        "open_issues_count",
        "fork",
        "archived",
        "_sampling_stratum",
    ]

    with OUTPUT_FILE.open(
        "w",
        newline="",
        encoding="utf-8",
    ) as file:

        writer = csv.DictWriter(
            file,
            fieldnames=fields,
            extrasaction="ignore",
        )

        writer.writeheader()

        for repository in candidates:
            writer.writerow(repository)


def main() -> None:

    print()
    print("OpenSourcePulse — Candidate Pool Builder")
    print("=" * 60)

    candidates = collect_candidates()

    save_candidates(candidates)

    print()
    print("=" * 60)
    print(
        f"Total candidate repositories: "
        f"{len(candidates)}"
    )
    print(f"Saved to: {OUTPUT_FILE}")
    print("=" * 60)


if __name__ == "__main__":
    main()