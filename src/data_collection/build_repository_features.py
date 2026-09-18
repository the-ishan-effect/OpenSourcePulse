import pandas as pd
import numpy as np


REPOSITORY_FILE = "data/raw/repositories.csv"
CONTRIBUTOR_FILE = "data/raw/repository_contributors.csv"
MONTHLY_FILE = "data/processed/repository_monthly_activity.csv"
COMMIT_STATUS_FILE = "data/raw/commit_collection_status.csv"

OUTPUT_FILE = "data/processed/repository_features.csv"


def main():

    print("Building Repository Feature Dataset")
    print("------------------------------------")

    # ---------------------------------------------------------
    # 1. Load datasets
    # ---------------------------------------------------------

    repos = pd.read_csv(REPOSITORY_FILE)

    contributors = pd.read_csv(
        CONTRIBUTOR_FILE
    )

    monthly = pd.read_csv(
        MONTHLY_FILE
    )

    commit_status = pd.read_csv(
        COMMIT_STATUS_FILE
    )

    print("Repositories:", len(repos))
    print("Contributor records:", len(contributors))
    print("Monthly activity rows:", len(monthly))

    # ---------------------------------------------------------
    # 2. Repository age
    # ---------------------------------------------------------

    repos["created_at"] = pd.to_datetime(
        repos["created_at"],
        utc=True,
        errors="coerce"
    )

    repos["updated_at"] = pd.to_datetime(
        repos["updated_at"],
        utc=True,
        errors="coerce"
    )

    repos["pushed_at"] = pd.to_datetime(
        repos["pushed_at"],
        utc=True,
        errors="coerce"
    )

    reference_date = pd.Timestamp.now(tz="UTC")

    repos["repository_age_days"] = (
        reference_date - repos["created_at"]
    ).dt.days

    repos["repository_age_years"] = (
        repos["repository_age_days"] / 365.25
    )

    # ---------------------------------------------------------
    # 3. Recency features
    # ---------------------------------------------------------

    repos["days_since_update"] = (
        reference_date - repos["updated_at"]
    ).dt.days

    repos["days_since_push"] = (
        reference_date - repos["pushed_at"]
    ).dt.days

    # ---------------------------------------------------------
    # 4. Contributor statistics
    # ---------------------------------------------------------

    contributor_stats = (
        contributors
        .groupby("repo_id")
        .agg(
            contributors_count=(
                "contributor_id",
                "nunique"
            ),
            total_contributions=(
                "contributions",
                "sum"
            ),
            top_contributor_contributions=(
                "contributions",
                "max"
            )
        )
        .reset_index()
    )

    # ---------------------------------------------------------
    # 5. Contributor concentration
    # ---------------------------------------------------------

    contributor_stats["top_contributor_share"] = (
        contributor_stats["top_contributor_contributions"]
        / contributor_stats["total_contributions"]
    )

    # ---------------------------------------------------------
    # 6. Commit activity
    # ---------------------------------------------------------

    commit_stats = (
        monthly
        .groupby("repo_id")
        .agg(
            commits_365d=(
                "commits_count",
                "sum"
            ),
            active_months=(
                "month",
                "nunique"
            ),
            peak_monthly_commits=(
                "commits_count",
                "max"
            ),
            mean_monthly_commits=(
                "commits_count",
                "mean"
            ),
            monthly_commit_std=(
                "commits_count",
                "std"
            )
        )
        .reset_index()
    )

    # ---------------------------------------------------------
    # 7. Activity consistency
    # ---------------------------------------------------------

    commit_stats["activity_consistency"] = (
        commit_stats["active_months"] / 13
    )

    # ---------------------------------------------------------
    # 8. Merge everything
    # ---------------------------------------------------------

    features = repos.merge(
        contributor_stats,
        on="repo_id",
        how="left"
    )

    features = features.merge(
        commit_stats,
        on="repo_id",
        how="left"
    )

    # ---------------------------------------------------------
    # 9. Collection status
    # ---------------------------------------------------------

    status_small = commit_status[
        [
            "repo_id",
            "status",
            "commits_count"
        ]
    ].rename(
        columns={
            "commits_count": "collected_commits"
        }
    )

    features = features.merge(
        status_small,
        on="repo_id",
        how="left"
    )

    # ---------------------------------------------------------
    # 10. Fill structural zeros
    # ---------------------------------------------------------
    # Only repositories with successful or genuine zero-result
    # collection should receive structural zeros.
    #
    # API-error repositories remain NaN for activity features
    # so that unavailable data is not interpreted as inactivity.

    structural_zero_statuses = [
        "success",
        "zero_commits"
    ]

    zero_features = [
        "contributors_count",
        "total_contributions",
        "top_contributor_contributions",
        "top_contributor_share",
        "commits_365d",
        "active_months",
        "peak_monthly_commits",
        "mean_monthly_commits",
        "monthly_commit_std",
        "activity_consistency"
    ]

    valid_zero_mask = features["status"].isin(
        structural_zero_statuses
    )

    for column in zero_features:
        features.loc[valid_zero_mask, column] = (
            features.loc[valid_zero_mask, column].fillna(0)
        )

    # ---------------------------------------------------------
    # 11. Derived ratios
    # ---------------------------------------------------------

    features["fork_star_ratio"] = np.where(
        features["stars"] > 0,
        features["forks"] / features["stars"],
        0
    )

    features["issues_per_star"] = np.where(
        features["stars"] > 0,
        features["open_issues"] / features["stars"],
        0
    )

    features["commits_per_active_month"] = np.where(
        features["active_months"] > 0,
        features["commits_365d"]
        / features["active_months"],
        np.nan
    )

    # ---------------------------------------------------------
    # 12. Normalize language labels
    # ---------------------------------------------------------

    features["language_normalized"] = (
        features["language"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # ---------------------------------------------------------
    # 13. Log transformations for skewed variables
    # ---------------------------------------------------------
    # np.log1p preserves NaN values for API-unavailable records.

    skewed_columns = [
        "stars",
        "forks",
        "open_issues",
        "size_kb",
        "commits_365d",
        "contributors_count",
        "total_contributions"
    ]

    for column in skewed_columns:
        features[f"log1p_{column}"] = np.log1p(
            features[column]
        )

    # ---------------------------------------------------------
    # 14. Sort rows
    # ---------------------------------------------------------

    features = features.sort_values(
        "repo_id"
    ).reset_index(drop=True)

    # ---------------------------------------------------------
    # 15. Save
    # ---------------------------------------------------------

    features.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # ---------------------------------------------------------
    # 16. Diagnostics
    # ---------------------------------------------------------

    print()
    print("Feature dataset created")
    print("-----------------------")
    print("Rows:", len(features))
    print("Columns:", len(features.columns))

    print()
    print("Selected feature summary:")

    print(
        features[
            [
                "stars",
                "forks",
                "open_issues",
                "repository_age_days",
                "contributors_count",
                "commits_365d",
                "active_months",
                "fork_star_ratio",
                "activity_consistency"
            ]
        ].describe()
    )

    print()
    print("Commit collection status:")
    print(
        features["status"]
        .value_counts()
    )

    print()
    print("Activity values unavailable due to API errors:")

    error_mask = features["status"] == "error"

    print(
        features.loc[
            error_mask,
            [
                "full_name",
                "commits_365d",
                "active_months",
                "contributors_count"
            ]
        ]
    )

    print()
    print("Saved:", OUTPUT_FILE)


if __name__ == "__main__":
    main()