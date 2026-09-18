from pathlib import Path

import pandas as pd


PROJECT_ROOT = Path(__file__).resolve().parents[2]
INPUT_FILE = PROJECT_ROOT / "data" / "raw" / "repositories.csv"


def main() -> None:
    print("OpenSourcePulse — Repository Data Quality Inspection")
    print("=" * 60)

    df = pd.read_csv(INPUT_FILE)

    print("\n1. DATASET SHAPE")
    print("-" * 30)
    print("Rows    :", df.shape[0])
    print("Columns :", df.shape[1])

    print("\n2. COLUMN NAMES")
    print("-" * 30)
    for column in df.columns:
        print(column)

    print("\n3. DATA TYPES")
    print("-" * 30)
    print(df.dtypes)

    print("\n4. MISSING VALUES")
    print("-" * 30)

    missing = df.isnull().sum()
    missing_percent = (missing / len(df)) * 100

    missing_table = pd.DataFrame({
        "missing_count": missing,
        "missing_percent": missing_percent.round(2),
    })

    print(missing_table)

    print("\n5. DUPLICATE ROWS")
    print("-" * 30)
    print("Duplicate rows :", df.duplicated().sum())

    print("\n6. DUPLICATE REPOSITORY IDs")
    print("-" * 30)
    print("Duplicate repo IDs :", df["repo_id"].duplicated().sum())

    print("\n7. DUPLICATE REPOSITORY NAMES")
    print("-" * 30)
    print("Duplicate full names :", df["full_name"].duplicated().sum())

    print("\n8. LANGUAGE DISTRIBUTION")
    print("-" * 30)
    print(df["language"].value_counts(dropna=False))

    print("\n9. POPULARITY STATISTICS")
    print("-" * 30)
    print(df["stars"].describe())

    print("\n10. FORK STATISTICS")
    print("-" * 30)
    print(df["forks"].describe())

    print("\n11. OPEN ISSUE STATISTICS")
    print("-" * 30)
    print(df["open_issues"].describe())

    print("\n12. ARCHIVED REPOSITORIES")
    print("-" * 30)
    print(df["archived"].value_counts(dropna=False))

    print("\n13. FORK REPOSITORIES")
    print("-" * 30)
    print(df["is_fork"].value_counts(dropna=False))

    print("\n14. ZERO-VALUE COUNTS")
    print("-" * 30)

    numeric_columns = [
        "stars",
        "forks",
        "watchers",
        "open_issues",
        "size_kb",
    ]

    for column in numeric_columns:
        print(f"{column:15s}: {(df[column] == 0).sum()}")

    print("\n15. SAMPLE RECORDS")
    print("-" * 30)
    print(
        df[
            [
                "full_name",
                "language",
                "stars",
                "forks",
                "open_issues",
                "created_at",
                "pushed_at",
                "archived",
                "is_fork",
            ]
        ].to_string(index=False)
    )

    print("\n" + "=" * 60)
    print("Inspection complete.")


if __name__ == "__main__":
    main()