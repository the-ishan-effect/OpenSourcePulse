import time
from datetime import datetime, timedelta, timezone

import pandas as pd

from api_helper import BASE_URL, github_get


INPUT_FILE = "data/raw/repositories.csv"
OUTPUT_FILE = "data/raw/repository_commits.csv"
STATUS_FILE = "data/raw/commit_collection_status.csv"

# Collect only the most recent 12 months.
LOOKBACK_DAYS = 365


def get_recent_commits(owner, repo, since):
    all_commits = []
    page = 1

    while True:
        url = f"{BASE_URL}/repos/{owner}/{repo}/commits"

        params = {
            "per_page": 100,
            "page": page,
            "since": since,
        }

        commits = github_get(url, params=params)

        if not commits:
            break

        all_commits.extend(commits)

        if len(commits) < 100:
            break

        page += 1

    return all_commits


def main():
    df = pd.read_csv(INPUT_FILE)

    since_date = (
        datetime.now(timezone.utc) - timedelta(days=LOOKBACK_DAYS)
    ).isoformat()

    all_rows = []
    status_rows = []

    print("GitHub Recent Commit Collection")
    print("--------------------------------")
    print("Repositories to process:", len(df))
    print("Lookback period: 365 days")
    print("Since:", since_date)
    print()

    for index, repository in df.iterrows():

        repo_id = repository["repo_id"]
        owner = repository["owner"]
        repo = repository["repo_name"]
        full_name = repository["full_name"]

        print(f"[{index + 1}/{len(df)}] {full_name}")

        try:
            commits = get_recent_commits(
                owner,
                repo,
                since_date
            )

            print("   Recent commits:", len(commits))

            for commit in commits:

                commit_data = commit.get("commit", {})
                author_data = commit_data.get("author") or {}
                committer_data = commit_data.get("committer") or {}

                all_rows.append(
                    {
                        "repo_id": repo_id,
                        "full_name": full_name,
                        "commit_sha": commit.get("sha"),
                        "author_login": (
                            commit.get("author") or {}
                        ).get("login"),
                        "author_id": (
                            commit.get("author") or {}
                        ).get("id"),
                        "author_name": author_data.get("name"),
                        "author_date": author_data.get("date"),
                        "committer_login": (
                            commit.get("committer") or {}
                        ).get("login"),
                        "committer_id": (
                            commit.get("committer") or {}
                        ).get("id"),
                        "committer_name": committer_data.get("name"),
                        "committer_date": committer_data.get("date"),
                        "message": commit_data.get("message"),
                        "html_url": commit.get("html_url"),
                    }
                )

            status_rows.append(
                {
                    "repo_id": repo_id,
                    "full_name": full_name,
                    "status": (
                        "zero_commits"
                        if len(commits) == 0
                        else "success"
                    ),
                    "commits_count": len(commits),
                    "error_message": None,
                }
            )

        except Exception as error:

            print("   ERROR:", error)

            status_rows.append(
                {
                    "repo_id": repo_id,
                    "full_name": full_name,
                    "status": "error",
                    "commits_count": 0,
                    "error_message": str(error),
                }
            )

        time.sleep(0.1)

    commits_df = pd.DataFrame(all_rows)
    status_df = pd.DataFrame(status_rows)

    commits_df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    status_df.to_csv(
        STATUS_FILE,
        index=False
    )

    print()
    print("Collection complete")
    print("-------------------")
    print("Commit rows:", len(commits_df))
    print(
        "Repositories represented:",
        commits_df["repo_id"].nunique()
        if not commits_df.empty
        else 0
    )
    print()
    print("Collection status:")
    print(status_df["status"].value_counts())
    print()
    print("Saved:", OUTPUT_FILE)
    print("Saved:", STATUS_FILE)


if __name__ == "__main__":
    main()