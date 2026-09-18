import pandas as pd


INPUT_FILE = "data/raw/repository_commits.csv"
REPOSITORY_FILE = "data/raw/repositories.csv"
STATUS_FILE = "data/raw/commit_collection_status.csv"
OUTPUT_FILE = "data/processed/repository_monthly_activity.csv"


def main():

    print("Building Monthly Repository Activity")
    print("------------------------------------")

    commits = pd.read_csv(INPUT_FILE)
    repositories = pd.read_csv(REPOSITORY_FILE)
    status = pd.read_csv(STATUS_FILE)

    print("Commit records loaded:", len(commits))

    # ---------------------------------------------------------
    # 1. Parse dates
    # ---------------------------------------------------------

    commits["committer_date"] = pd.to_datetime(
        commits["committer_date"],
        utc=True,
        errors="coerce"
    )

    # ---------------------------------------------------------
    # 2. Remove exact duplicate repository + commit records
    # ---------------------------------------------------------

    before = len(commits)

    commits = commits.drop_duplicates(
        subset=["repo_id", "commit_sha"]
    )

    after = len(commits)

    print("Duplicate records removed:", before - after)

    # ---------------------------------------------------------
    # 3. Create monthly time index
    # ---------------------------------------------------------

    commits["month"] = (
        commits["committer_date"]
        .dt.to_period("M")
        .astype(str)
    )

    # ---------------------------------------------------------
    # 4. Aggregate commits by repository and month
    # ---------------------------------------------------------

    monthly = (
        commits
        .groupby(
            ["repo_id", "full_name", "month"],
            as_index=False
        )
        .agg(
            commits_count=("commit_sha", "nunique"),
            active_contributors=(
                "author_id",
                "nunique"
            )
        )
    )

    # ---------------------------------------------------------
    # 5. Add repository metadata
    # ---------------------------------------------------------

    metadata = repositories[
        [
            "repo_id",
            "language",
            "stars",
            "forks",
            "open_issues",
            "created_at",
            "pushed_at",
            "archived",
            "is_fork"
        ]
    ].copy()

    monthly = monthly.merge(
        metadata,
        on="repo_id",
        how="left"
    )

    # ---------------------------------------------------------
    # 6. Add collection status
    # ---------------------------------------------------------

    status_small = status[
        [
            "repo_id",
            "status",
            "commits_count"
        ]
    ].copy()

    status_small = status_small.rename(
        columns={
            "commits_count": "collected_commits"
        }
    )

    monthly = monthly.merge(
        status_small,
        on="repo_id",
        how="left"
    )

    # ---------------------------------------------------------
    # 7. Sort
    # ---------------------------------------------------------

    monthly = monthly.sort_values(
        ["repo_id", "month"]
    ).reset_index(drop=True)

    # ---------------------------------------------------------
    # 8. Save
    # ---------------------------------------------------------

    monthly.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # ---------------------------------------------------------
    # 9. Diagnostics
    # ---------------------------------------------------------

    print()
    print("Monthly activity created")
    print("------------------------")
    print("Rows:", len(monthly))
    print("Repositories:", monthly["repo_id"].nunique())
    print(
        "Months:",
        monthly["month"].min(),
        "to",
        monthly["month"].max()
    )

    print()
    print("Top repositories by monthly activity:")
    print(
        monthly
        .groupby("full_name")["commits_count"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    print()
    print("Saved:", OUTPUT_FILE)


if __name__ == "__main__":
    main()