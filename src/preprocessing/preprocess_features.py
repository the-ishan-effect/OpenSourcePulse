import pandas as pd
import numpy as np


INPUT_FILE = "data/processed/repository_features.csv"
OUTPUT_FILE = "data/processed/repository_features_clean.csv"
OUTLIER_FILE = "data/processed/repository_outlier_summary.csv"


def main():

    print("OpenSourcePulse - Data Preprocessing")
    print("=====================================")

    df = pd.read_csv(INPUT_FILE)

    print("Original shape:", df.shape)

    # ---------------------------------------------------------
    # 1. Duplicate check
    # ---------------------------------------------------------

    duplicate_rows = df.duplicated().sum()
    duplicate_repositories = df["repo_id"].duplicated().sum()

    print()
    print("Duplicate rows:", duplicate_rows)
    print("Duplicate repository IDs:", duplicate_repositories)

    # ---------------------------------------------------------
    # 2. Date-time conversion
    # ---------------------------------------------------------

    date_columns = [
        "created_at",
        "updated_at",
        "pushed_at"
    ]

    for column in date_columns:
        df[column] = pd.to_datetime(
            df[column],
            utc=True,
            errors="coerce"
        )

    # ---------------------------------------------------------
    # 3. Categorical normalization
    # ---------------------------------------------------------

    df["language_normalized"] = (
        df["language"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .str.lower()
    )

    # ---------------------------------------------------------
    # 4. Missing-value treatment
    # ---------------------------------------------------------

    # Description: explicit Unknown rather than fabricated text
    df["description"] = df["description"].fillna(
        "No description provided"
    )

    # Language already represented as Unknown
    df["language_normalized"] = (
        df["language_normalized"]
        .replace("", "unknown")
    )

    # License: preserve missingness explicitly
    df["license"] = df["license"].fillna(
        "No license specified"
    )

    # Topics: preserve missingness explicitly
    df["topics"] = df["topics"].fillna(
        "No topics specified"
    )

    # ---------------------------------------------------------
    # 5. Numerical consistency checks
    # ---------------------------------------------------------

    non_negative_columns = [
        "stars",
        "forks",
        "watchers",
        "open_issues",
        "size_kb",
        "repository_age_days",
        "repository_age_years",
        "days_since_update",
        "days_since_push",
        "contributors_count",
        "total_contributions",
        "top_contributor_contributions",
        "commits_365d",
        "active_months",
        "peak_monthly_commits",
        "mean_monthly_commits"
    ]

    print()
    print("Negative-value checks:")

    for column in non_negative_columns:
        negative_count = (df[column] < 0).sum()
        print(
            f"{column}: {negative_count}"
        )

    # ---------------------------------------------------------
    # 6. Skewness analysis
    # ---------------------------------------------------------

    skewed_columns = [
        "stars",
        "forks",
        "open_issues",
        "size_kb",
        "commits_365d",
        "contributors_count",
        "total_contributions",
        "peak_monthly_commits"
    ]

    print()
    print("Skewness before transformation:")
    
    for column in skewed_columns:
        print(
            f"{column}: "
            f"{df[column].skew():.3f}"
        )

    # ---------------------------------------------------------
    # 7. Log transformation
    # ---------------------------------------------------------

    for column in skewed_columns:

        transformed_column = (
            f"log1p_{column}"
        )

        df[transformed_column] = np.log1p(
            df[column]
        )

    # ---------------------------------------------------------
    # 8. Skewness after transformation
    # ---------------------------------------------------------

    print()
    print("Skewness after log1p transformation:")

    for column in skewed_columns:

        transformed_column = (
            f"log1p_{column}"
        )

        print(
            f"{transformed_column}: "
            f"{df[transformed_column].skew():.3f}"
        )

    # ---------------------------------------------------------
    # 9. IQR outlier detection
    # ---------------------------------------------------------

    outlier_rows = []

    outlier_columns = [
        "stars",
        "forks",
        "open_issues",
        "size_kb",
        "commits_365d",
        "contributors_count",
        "total_contributions"
    ]

    for column in outlier_columns:

        q1 = df[column].quantile(0.25)
        q3 = df[column].quantile(0.75)

        iqr = q3 - q1

        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr

        mask = (
            (df[column] < lower_bound)
            | (df[column] > upper_bound)
        )

        outlier_rows.append(
            {
                "feature": column,
                "Q1": q1,
                "Q3": q3,
                "IQR": iqr,
                "lower_bound": lower_bound,
                "upper_bound": upper_bound,
                "outlier_count": int(mask.sum()),
                "outlier_percentage": (
                    mask.mean() * 100
                )
            }
        )

    outlier_summary = pd.DataFrame(
        outlier_rows
    )

    # ---------------------------------------------------------
    # 10. Preserve outliers
    # ---------------------------------------------------------

    # IMPORTANT:
    # We do not delete genuine high-activity repositories.
    # Outliers are retained because they represent real
    # repository behavior.

    # ---------------------------------------------------------
    # 11. Save outlier summary
    # ---------------------------------------------------------

    outlier_summary.to_csv(
        OUTLIER_FILE,
        index=False
    )

    # ---------------------------------------------------------
    # 12. Save cleaned dataset
    # ---------------------------------------------------------

    df.to_csv(
        OUTPUT_FILE,
        index=False
    )

    # ---------------------------------------------------------
    # 13. Final diagnostics
    # ---------------------------------------------------------

    print()
    print("Preprocessing complete")
    print("----------------------")
    print("Final shape:", df.shape)

    print()
    print("Final missing values:")
    print(
        df.isna()
        .sum()
        .sort_values(ascending=False)
        .head(15)
    )

    print()
    print("Outlier summary:")
    print(
        outlier_summary[
            [
                "feature",
                "outlier_count",
                "outlier_percentage"
            ]
        ].to_string(index=False)
    )

    print()
    print("Saved:")
    print(OUTPUT_FILE)
    print(OUTLIER_FILE)


if __name__ == "__main__":
    main()