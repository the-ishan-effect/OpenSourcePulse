import time

import requests

from github_client import BASE_URL, HEADERS


def github_get(url: str, params: dict | None = None) -> dict | list:
    """
    Make a GET request to the GitHub REST API.

    Handles:
    - authentication headers
    - HTTP errors
    - GitHub rate limits
    """

    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=30,
    )

    # If rate limit is exhausted, wait until GitHub's reset time.
    if response.status_code == 403:

        remaining = response.headers.get("X-RateLimit-Remaining")
        reset = response.headers.get("X-RateLimit-Reset")

        if remaining == "0" and reset:
            wait_seconds = max(
                int(reset) - int(time.time()),
                0,
            )

            print(
                f"GitHub API rate limit exhausted. "
                f"Waiting {wait_seconds} seconds."
            )

            time.sleep(wait_seconds + 2)

            response = requests.get(
                url,
                headers=HEADERS,
                params=params,
                timeout=30,
            )

    response.raise_for_status()

    return response.json()


def get_rate_limit() -> dict:
    """Return the current GitHub core API rate-limit information."""

    url = f"{BASE_URL}/rate_limit"

    data = github_get(url)

    return data["resources"]["core"]


if __name__ == "__main__":

    rate_limit = get_rate_limit()

    print("GitHub API helper test")
    print("----------------------")
    print("Limit     :", rate_limit["limit"])
    print("Used      :", rate_limit["used"])
    print("Remaining :", rate_limit["remaining"])
    print("Reset     :", rate_limit["reset"])