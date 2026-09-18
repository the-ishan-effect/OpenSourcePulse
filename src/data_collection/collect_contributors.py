import time

import pandas as pd

from api_helper import BASE_URL, github_get


INPUT_FILE = "data/raw/repositories.csv"
OUTPUT_FILE = "data/raw/repository_contributors.csv"


def get_all_contributors(owner: str, repo: str) -> list:
    """Fetch all contributors using pagination."""

    all_contributors = []
    page = 1

    while True:

        url = f"{BASE_URL}/repos/{owner}/{repo}/contributors"

        params = {
            "per_page": 100,
            "page": page,
        }

        contributors = github_get(url, params=params)

        if not contributors:
            break

        all_contributors.extend(contributors)

        if len(contributors) < 100:
            break

        page += 1

    return all_contributors


def main():

    df = pd.read_csv(INPUT_FILE)

    all_rows = []

    print("=" * 70)
    print("OpenSourcePulse — Contributor Collection")
    print("=" * 70)
    print(f"Repositories to process: {len(df)}")
    print()

    for index, repository in df.iterrows():

        owner = repository["owner"]
        repo = repository["repo_name"]

        print(
            f"[{index + 1:03}/{len(df)}] "
            f"{owner}/{repo}",
            end=" ... ",
            flush=True,
        )

        try:

            contributors = get_all_contributors(
                owner,
                repo,
            )

            print(f"{len(contributors)} contributors")

            for contributor in contributors:

                all_rows.append({
                    "repo_id": repository["repo_id"],
                    "full_name": repository["full_name"],
                    "contributor_login": contributor.get("login"),
                    "contributor_id": contributor.get("id"),
                    "contributions": contributor.get(
                        "contributions"
                    ),
                })

        except Exception as error:

            print(f"ERROR: {error}")

        # Small delay to avoid unnecessarily aggressive requests.
        time.sleep(0.1)

    result = pd.DataFrame(all_rows)

    result.to_csv(
        OUTPUT_FILE,
        index=False,
    )

    print()
    print("=" * 70)
    print("Collection complete")
    print("=" * 70)
    print("Rows collected :", len(result))
    print("Repositories   :", result["repo_id"].nunique())
    print("Missing values :")
    print(result.isna().sum().to_string())
    print()
    print("Duplicate records :",
          result.duplicated(
              subset=["repo_id", "contributor_id"]
          ).sum())
    print()
    print("Saved to:")
    print(OUTPUT_FILE)


if __name__ == "__main__":
    main()