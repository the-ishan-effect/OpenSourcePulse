import pandas as pd

from api_helper import BASE_URL, github_get


INPUT_FILE = "data/raw/repositories.csv"


def get_contributors(owner: str, repo: str) -> list:
    """
    Fetch all contributors for a repository using pagination.
    """

    all_contributors = []

    page = 1

    while True:

        url = f"{BASE_URL}/repos/{owner}/{repo}/contributors"

        params = {
            "per_page": 100,
            "page": page,
        }

        contributors = github_get(
            url,
            params=params,
        )

        if not contributors:
            break

        all_contributors.extend(contributors)

        # If fewer than 100 records are returned,
        # there are no more pages.
        if len(contributors) < 100:
            break

        page += 1

    return all_contributors


def main():

    df = pd.read_csv(INPUT_FILE)

    # Test exactly five repositories.
    pilot = df.head(5)

    print("Contributor API Pagination Pilot")
    print("=" * 60)
    print()

    all_rows = []

    for _, repository in pilot.iterrows():

        owner = repository["owner"]
        repo = repository["repo_name"]

        print(f"Repository: {owner}/{repo}")

        contributors = get_contributors(
            owner,
            repo,
        )

        print(
            f"Contributors returned: {len(contributors)}"
        )

        for contributor in contributors:

            all_rows.append({
                "repo_id": repository["repo_id"],
                "full_name": repository["full_name"],
                "contributor_login": contributor.get("login"),
                "contributor_id": contributor.get("id"),
                "contributions": contributor.get("contributions"),
            })

        print()

    result = pd.DataFrame(all_rows)

    print("=" * 60)
    print("Pilot result")
    print("=" * 60)

    print("Rows collected:", len(result))
    print()

    if not result.empty:

        print("Sample:")
        print(
            result.head(10).to_string(
                index=False
            )
        )

        print()

        print("Missing values:")
        print(
            result.isna().sum().to_string()
        )

        print()

        print("Duplicate contributor records:")

        duplicates = result.duplicated(
            subset=[
                "repo_id",
                "contributor_id",
            ]
        ).sum()

        print(duplicates)


if __name__ == "__main__":
    main()