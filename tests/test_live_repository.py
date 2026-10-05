from src.product.repository_analyzer import (
    analyze_repository
)


result = analyze_repository(
    "https://github.com/microsoft/vscode"
)

print("\n==============================")
print("OpenSourcePulse Live Test")
print("==============================")

print(
    "\nRepository:",
    result["features"]["full_name"]
)

print(
    "Stars:",
    result["features"]["stars"]
)

print(
    "Forks:",
    result["features"]["forks"]
)

print(
    "Commits in last 365 days:",
    result["features"]["commits_365d"]
)

print(
    "Active months:",
    result["features"]["active_months"]
)

print(
    "Contributors:",
    result["features"]["contributors_count"]
)

print(
    "\nHealth Index:",
    round(
        result["health"]["health_score"],
        2
    )
)

print(
    "Health Profile:",
    result["health"]["health_profile"]
)

print(
    "Score Coverage:",
    round(
        result["health"]["health_score_coverage"],
        2
    ),
    "%"
)

print("\nDimension Scores:")

for key, value in result["health"].items():

    if key.endswith("_score"):

        if value == value:

            print(
                f"{key}: {value:.2f}"
            )

print("\nBackend test completed.")