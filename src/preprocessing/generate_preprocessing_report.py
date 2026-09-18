import pandas as pd


INPUT_FILE = "data/processed/repository_features.csv"
OUTPUT_FILE = "data/processed/preprocessing_report.csv"


def main():

    df = pd.read_csv(INPUT_FILE)

    rows = []

    # ---------------------------------------------------------
    # Missing-value mechanism assessment
    # ---------------------------------------------------------

    missing_info = {
        "description": (
            "MAR/structural: repositories may not provide "
            "a description"
        ),
        "language": (
            "MAR/structural: GitHub may not assign a "
            "primary language"
        ),
        "topics": (
            "MAR/structural: repository topics are optional"
        ),
        "license": (
            "MAR/structural: repositories may not specify "
            "a license"
        )
    }

    treatments = {
        "description": "Explicit category: No description provided",
        "language": "Explicit category: Unknown",
        "topics": "Explicit category: No topics specified",
        "license": "Explicit category: No license specified"
    }

    for column, mechanism in missing_info.items():

        missing_count = df[column].isna().sum()

        rows.append(
            {
                "feature": column,
                "missing_count": missing_count,
                "missing_percentage": (
                    missing_count / len(df) * 100
                ),
                "mechanism_assessment": mechanism,
                "treatment": treatments[column]
            }
        )

    report = pd.DataFrame(rows)

    report.to_csv(
        OUTPUT_FILE,
        index=False
    )

    print("Preprocessing Report")
    print("====================")
    print(report.to_string(index=False))
    print()
    print("Saved:", OUTPUT_FILE)


if __name__ == "__main__":
    main()