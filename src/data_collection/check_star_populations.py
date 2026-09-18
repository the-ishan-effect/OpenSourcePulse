import sys
from pathlib import Path

import requests

sys.path.append(str(Path(__file__).resolve().parent))

from github_client import BASE_URL, HEADERS


STAR_RANGES = [
    ("P1_100_499", "stars:100..499"),
    ("P2_500_999", "stars:500..999"),
    ("P3_1000_2499", "stars:1000..2499"),
    ("P4_2500_4999", "stars:2500..4999"),
    ("P5_5000_9999", "stars:5000..9999"),
    ("P6_10000_24999", "stars:10000..24999"),
    ("P7_25000_49999", "stars:25000..49999"),
    ("P8_50000_99999", "stars:50000..99999"),
    ("P9_100000_199999", "stars:100000..199999"),
    ("P10_200000_plus", "stars:>=200000"),
]


def check_populations() -> None:
    print()
    print("OpenSourcePulse — GitHub Star Population Check")
    print("=" * 65)
    print()

    for name, query in STAR_RANGES:

        url = f"{BASE_URL}/search/repositories"

        params = {
            "q": query,
            "per_page": 1,
        }

        response = requests.get(
            url,
            headers=HEADERS,
            params=params,
            timeout=30,
        )

        response.raise_for_status()

        data = response.json()

        total = data["total_count"]

        print(f"{name:20s} -> {total:,} repositories")


if __name__ == "__main__":
    check_populations()