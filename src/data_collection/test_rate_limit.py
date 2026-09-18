from github_client import HEADERS, BASE_URL

import requests


def check_rate_limit() -> None:
    """Display the authenticated GitHub API rate limit."""

    url = f"{BASE_URL}/rate_limit"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    data = response.json()
    core = data["resources"]["core"]

    print("GitHub API rate-limit information")
    print("----------------------------------")
    print("Limit     :", core["limit"])
    print("Used      :", core["used"])
    print("Remaining :", core["remaining"])
    print("Reset     :", core["reset"])


if __name__ == "__main__":
    check_rate_limit()