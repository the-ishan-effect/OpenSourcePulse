import os

import requests
from dotenv import load_dotenv


# Load environment variables from .env
load_dotenv()

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")

if not GITHUB_TOKEN:
    raise ValueError(
        "GITHUB_TOKEN was not found. "
        "Check that your .env file contains GITHUB_TOKEN."
    )


BASE_URL = "https://api.github.com"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}


def get_repository(owner: str, repo: str) -> dict:
    """
    Fetch metadata for a public GitHub repository.

    Parameters
    ----------
    owner : str
        GitHub repository owner.

    repo : str
        Repository name.

    Returns
    -------
    dict
        Repository metadata returned by GitHub.
    """

    url = f"{BASE_URL}/repos/{owner}/{repo}"

    response = requests.get(
        url,
        headers=HEADERS,
        timeout=30,
    )

    response.raise_for_status()

    return response.json()


if __name__ == "__main__":
    repository = get_repository("python", "cpython")

    print("GitHub API connection successful!")
    print()
    print("Repository :", repository["full_name"])
    print("Stars      :", repository["stargazers_count"])
    print("Forks      :", repository["forks_count"])
    print("Language   :", repository["language"])
    print("Created    :", repository["created_at"])
    print("Updated    :", repository["updated_at"])