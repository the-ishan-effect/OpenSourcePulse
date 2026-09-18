import random
import time
import pandas as pd
import requests

from github_client import BASE_URL, HEADERS


RANDOM_SEED = 42
random.seed(RANDOM_SEED)

INPUT_FILE = "data/raw/repositories.csv"
OUTPUT_FILE = "data/raw/repositories.csv"


# Current target sample size for each stratum
TARGETS = {
    "P1_100_499": 35,
    "P2_500_999": 35,
    "P3_1000_2499": 35,
    "P4_2500_4999": 35,
    "P5_5000_9999": 35,
    "P6_10000_24999": 35,
    "P7_25000_49999": 30,
    "P8_50000_99999": 25,
    "P9_100000_199999": 15,
    "P10_200000_plus": 20,
}


# We deliberately split each affected range into smaller
# star intervals so replacements are not concentrated
# at the upper boundary.
RANGES = {
    "P1_100_499": [
        "stars:100..199",
        "stars:200..299",
        "stars:300..399",
        "stars:400..499",
    ],
    "P2_500_999": [
        "stars:500..599",
        "stars:600..699",
        "stars:700..799",
        "stars:800..899",
        "stars:900..999",
    ],
    "P3_1000_2499": [
        "stars:1000..1299",
        "stars:1300..1599",
        "stars:1600..1899",
        "stars:1900..2199",
        "stars:2200..2499",
    ],
    "P4_2500_4999": [
        "stars:2500..2999",
        "stars:3000..3499",
        "stars:3500..3999",
        "stars:4000..4499",
        "stars:4500..4999",
    ],
    "P5_5000_9999": [
        "stars:5000..5999",
        "stars:6000..6999",
        "stars:7000..7999",
        "stars:8000..8999",
        "stars:9000..9999",
    ],
    "P6_10000_24999": [
        "stars:10000..12999",
        "stars:13000..15999",
        "stars:16000..18999",
        "stars:19000..21999",
        "stars:22000..24999",
    ],
}


def github_search(query: str, page: int = 1, per_page: int = 100) -> list:
    """Search GitHub repositories."""
    url = f"{BASE_URL}/search/repositories"

    params = {
        "q": query,
        "sort": "stars",
        "order": "asc",
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

    return response.json().get("items", [])


def get_repository(owner: str, repo: str) -> dict | None:
    """Fetch repository details and verify eligibility."""
    url = f"{BASE_URL}/repos/{owner}/{repo}"

    try:
        response = requests.get(
            url,
            headers=HEADERS,
            timeout=30,
        )

        if response.status_code != 200:
            return None

        repository = response.json()

        # Exclude forks and archived repositories.
        if repository.get("fork", False):
            return None

        if repository.get("archived", False):
            return None

        return repository

    except requests.RequestException:
        return None


def build_candidate_pool(query: str) -> list:
    """
    Collect candidates from several pages.

    Multiple pages are used because GitHub search results are
    ordered by stars, and we do not want to depend on only
    the first page.
    """
    candidates = []

    for page in range(1, 4):
        try:
            items = github_search(query, page=page, per_page=100)

            for item in items:
                candidates.append(item)

            time.sleep(0.2)

        except requests.RequestException as error:
            print(f"Search failed for {query}, page {page}: {error}")

    # Deduplicate by GitHub repository ID
    unique = {}

    for item in candidates:
        repo_id = item.get("id")

        if repo_id is not None:
            unique[repo_id] = item

    return list(unique.values())


def main():
    df = pd.read_csv(INPUT_FILE)

    existing_ids = set(df["repo_id"].astype(int))

    # Determine current stratum counts
    bins = [
        99,
        499,
        999,
        2499,
        4999,
        9999,
        24999,
        49999,
        99999,
        199999,
        float("inf"),
    ]

    labels = list(TARGETS.keys())

    df["stratum"] = pd.cut(
        df["stars"],
        bins=bins,
        labels=labels,
    )

    print("=" * 70)
    print("OpenSourcePulse — Controlled Replacement")
    print("=" * 70)
    print()

    current_counts = df["stratum"].value_counts().sort_index()

    print("Current counts:")
    print(current_counts.to_string())
    print()

    all_replacements = []

    # Only affected strata need replacements.
    for stratum, target in TARGETS.items():

        current = int(current_counts.get(stratum, 0))
        needed = target - current

        if needed <= 0:
            continue

        print("-" * 70)
        print(f"{stratum}")
        print(f"Current : {current}")
        print(f"Target  : {target}")
        print(f"Needed  : {needed}")
        print()

        candidates = []

        # Gather candidates from several smaller star ranges.
        for query in RANGES[stratum]:

            print(f"Searching {query} ...")

            items = build_candidate_pool(query)

            for item in items:
                repo_id = item.get("id")

                if repo_id is None:
                    continue

                if repo_id in existing_ids:
                    continue

                candidates.append(item)

        # Deduplicate candidates.
        unique_candidates = {}

        for item in candidates:
            unique_candidates[item["id"]] = item

        candidates = list(unique_candidates.values())

        print(f"Unique new candidates: {len(candidates)}")

        # Shuffle candidates before eligibility checking.
        random.shuffle(candidates)

        selected = []

        for candidate in candidates:

            if len(selected) >= needed:
                break

            full_name = candidate.get("full_name")

            if not full_name or "/" not in full_name:
                continue

            owner, repo = full_name.split("/", 1)

            repository = get_repository(owner, repo)

            if repository is None:
                continue

            repo_id = repository.get("id")

            if repo_id in existing_ids:
                continue

            # Make sure the repository is still inside
            # the intended star stratum.
            stars = repository.get("stargazers_count", 0)

            if stratum == "P1_100_499" and not 100 <= stars <= 499:
                continue

            if stratum == "P2_500_999" and not 500 <= stars <= 999:
                continue

            if stratum == "P3_1000_2499" and not 1000 <= stars <= 2499:
                continue

            if stratum == "P4_2500_4999" and not 2500 <= stars <= 4999:
                continue

            if stratum == "P5_5000_9999" and not 5000 <= stars <= 9999:
                continue

            if stratum == "P6_10000_24999" and not 10000 <= stars <= 24999:
                continue

            selected.append(repository)
            existing_ids.add(repo_id)

            print(
                f"  + {repository['full_name']} "
                f"({repository['stargazers_count']} stars)"
            )

        print()
        print(f"Selected replacements: {len(selected)}")

        all_replacements.extend(selected)

    if not all_replacements:
        print("No replacements found.")
        return

    print()
    print("=" * 70)
    print("Adding replacements")
    print("=" * 70)

    replacement_rows = []

    for repository in all_replacements:

        replacement_rows.append({
            "repo_id": repository.get("id"),
            "repo_name": repository.get("name"),
            "owner": repository.get("owner", {}).get("login"),
            "full_name": repository.get("full_name"),
            "description": repository.get("description"),
            "html_url": repository.get("html_url"),
            "language": repository.get("language"),
            "topics": ", ".join(repository.get("topics", [])),
            "license": (
                repository.get("license", {}).get("spdx_id")
                if repository.get("license")
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
        })

    replacements_df = pd.DataFrame(replacement_rows)

    # Remove helper column before saving.
    original_columns = [
        column for column in df.columns
        if column != "stratum"
    ]

    df = df[original_columns]

    replacements_df = replacements_df[original_columns]

    combined = pd.concat(
        [df, replacements_df],
        ignore_index=True,
    )

    # Final duplicate protection.
    combined = combined.drop_duplicates(
        subset=["repo_id"],
        keep="first",
    )

    combined.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print()
    print(f"Repositories added : {len(replacements_df)}")
    print(f"Final dataset size : {len(combined)}")
    print()
    print("Saved:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()