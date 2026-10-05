# ============================================================
# OpenSourcePulse
# Live GitHub Repository Analyzer
# ============================================================
#
# BACSE301 - Exploratory Data Analysis
#
# This module powers the LIVE APPLICATION layer.
#
# Research / EDA dataset:
#   300 repositories
#
# Live application:
#   User GitHub URL
#        ↓
#   Repository metadata
#        ↓
#   Aggregate GitHub activity
#        ↓
#   Contributor statistics
#        ↓
#   Feature engineering
#        ↓
#   Reference-data percentile normalization
#        ↓
#   Repository Health Index
#
# IMPORTANT:
# The research notebooks and research dataset are NOT changed
# by this optimized live analyzer.
# ============================================================

import os
import re
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import requests
from dotenv import load_dotenv


# ============================================================
# PROJECT CONFIGURATION
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

REFERENCE_DATASET = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "repository_features_clean.csv"
)


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv(
    PROJECT_ROOT / ".env"
)

GITHUB_TOKEN = os.getenv(
    "GITHUB_TOKEN"
)

if not GITHUB_TOKEN:
    raise ValueError(
        "GITHUB_TOKEN was not found. "
        "Check your .env file."
    )


# ============================================================
# GITHUB API CONFIGURATION
# ============================================================

BASE_URL = "https://api.github.com"

HEADERS = {
    "Accept": "application/vnd.github+json",
    "Authorization": f"Bearer {GITHUB_TOKEN}",
    "X-GitHub-Api-Version": "2022-11-28",
}


# ============================================================
# GENERIC GITHUB GET
# ============================================================

def github_get(
    url,
    params=None,
    timeout=30,
):
    """
    Perform a GitHub GET request.

    Handles basic rate-limit detection.
    """

    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=timeout,
    )

    # --------------------------------------------------------
    # Rate limit
    # --------------------------------------------------------

    if response.status_code == 403:

        remaining = response.headers.get(
            "X-RateLimit-Remaining"
        )

        if remaining == "0":

            reset_timestamp = int(
                response.headers.get(
                    "X-RateLimit-Reset",
                    time.time() + 60,
                )
            )

            wait_seconds = max(
                reset_timestamp
                - int(time.time())
                + 2,
                1,
            )

            raise RuntimeError(
                "GitHub API rate limit reached. "
                f"Retry after approximately "
                f"{wait_seconds} seconds."
            )

    response.raise_for_status()

    return response.json()


# ============================================================
# URL PARSER
# ============================================================

def parse_repository_url(
    repository_url,
):
    """
    Parse a GitHub repository URL.

    Supported examples:

    https://github.com/microsoft/vscode
    http://github.com/microsoft/vscode
    github.com/microsoft/vscode
    https://github.com/microsoft/vscode.git
    """

    if not isinstance(
        repository_url,
        str,
    ):
        raise ValueError(
            "Repository URL must be a string."
        )

    url = repository_url.strip()

    pattern = (
        r"^(?:https?://)?"
        r"(?:www\.)?"
        r"github\.com/"
        r"([^/\s]+)/"
        r"([^/\s#?]+)"
        r"/?$"
    )

    match = re.match(
        pattern,
        url,
    )

    if not match:
        raise ValueError(
            "Please enter a valid GitHub repository URL. "
            "Example: "
            "https://github.com/microsoft/vscode"
        )

    owner = match.group(1)

    repo = match.group(2)

    if repo.endswith(".git"):
        repo = repo[:-4]

    return owner, repo


# ============================================================
# REPOSITORY METADATA
# ============================================================

def fetch_repository(
    owner,
    repo,
):
    """
    Fetch repository metadata.
    """

    url = (
        f"{BASE_URL}/repos/"
        f"{owner}/{repo}"
    )

    return github_get(url)


# ============================================================
# FAST 365-DAY COMMIT COUNT
# ============================================================

def fetch_commit_count(
    owner,
    repo,
    days=365,
):
    """
    Determine the number of commits in the rolling
    time window without downloading every commit.

    GitHub pagination metadata gives us the final page.
    Since per_page=1, the final page number corresponds
    to the total number of matching commits.
    """

    since = (
        datetime.now(timezone.utc)
        - timedelta(days=days)
    ).isoformat()

    url = (
        f"{BASE_URL}/repos/"
        f"{owner}/{repo}/commits"
    )

    params = {
        "since": since,
        "per_page": 1,
        "page": 1,
    }

    response = requests.get(
        url,
        headers=HEADERS,
        params=params,
        timeout=30,
    )

    # --------------------------------------------------------
    # Rate limit
    # --------------------------------------------------------

    if response.status_code == 403:

        remaining = response.headers.get(
            "X-RateLimit-Remaining"
        )

        if remaining == "0":

            reset_timestamp = int(
                response.headers.get(
                    "X-RateLimit-Reset",
                    time.time() + 60,
                )
            )

            wait_seconds = max(
                reset_timestamp
                - int(time.time())
                + 2,
                1,
            )

            raise RuntimeError(
                "GitHub API rate limit reached. "
                f"Retry after approximately "
                f"{wait_seconds} seconds."
            )

    response.raise_for_status()

    first_page = response.json()

    if not first_page:
        return 0

    link_header = response.headers.get(
        "Link",
        "",
    )

    # --------------------------------------------------------
    # Only one page
    # --------------------------------------------------------

    if 'rel="last"' not in link_header:
        return len(first_page)

    # --------------------------------------------------------
    # Find last URL
    # --------------------------------------------------------

    match = re.search(
        r'<([^>]+)>;\s*rel="last"',
        link_header,
    )

    if not match:
        return len(first_page)

    last_url = match.group(1)

    page_match = re.search(
        r"[?&]page=(\d+)",
        last_url,
    )

    if not page_match:
        return len(first_page)

    last_page = int(
        page_match.group(1)
    )

    return last_page


# ============================================================
# GITHUB AGGREGATE COMMIT ACTIVITY
# ============================================================

def fetch_commit_activity(
    owner,
    repo,
):
    """
    Fetch GitHub's aggregate weekly commit activity.

    Instead of downloading thousands of individual commits,
    GitHub provides approximately 52 weekly observations.

    This gives us:
        - weekly commit activity
        - active weeks
        - active months
        - mean weekly commits
        - peak weekly commits
    """

    url = (
        f"{BASE_URL}/repos/"
        f"{owner}/{repo}/stats/commit_activity"
    )

    max_attempts = 4

    for attempt in range(
        max_attempts
    ):

        response = requests.get(
            url,
            headers=HEADERS,
            timeout=30,
        )

        # ----------------------------------------------------
        # GitHub may return 202 while calculating statistics
        # ----------------------------------------------------

        if response.status_code == 202:

            if attempt < max_attempts - 1:

                time.sleep(
                    2 * (attempt + 1)
                )

                continue

            return {
                "status": "unavailable",
                "weeks": [],
            }

        # ----------------------------------------------------
        # No activity
        # ----------------------------------------------------

        if response.status_code == 204:

            return {
                "status": "zero",
                "weeks": [],
            }

        # ----------------------------------------------------
        # Rate limit
        # ----------------------------------------------------

        if response.status_code == 403:

            remaining = response.headers.get(
                "X-RateLimit-Remaining"
            )

            if remaining == "0":

                reset_timestamp = int(
                    response.headers.get(
                        "X-RateLimit-Reset",
                        time.time() + 60,
                    )
                )

                wait_seconds = max(
                    reset_timestamp
                    - int(time.time())
                    + 2,
                    1,
                )

                raise RuntimeError(
                    "GitHub API rate limit reached. "
                    f"Retry after approximately "
                    f"{wait_seconds} seconds."
                )

        response.raise_for_status()

        data = response.json()

        if not data:

            return {
                "status": "zero",
                "weeks": [],
            }

        return {
            "status": "success",
            "weeks": data,
        }

    return {
        "status": "unavailable",
        "weeks": [],
    }


# ============================================================
# CONTRIBUTORS
# ============================================================

def fetch_contributors(
    owner,
    repo,
    max_pages=10,
):
    """
    Fetch contributor information.

    Maximum:
        10 pages × 100 contributors
        = 1,000 contributors

    This is separate from the research contributor
    collection and is used only for the live product.
    """

    url = (
        f"{BASE_URL}/repos/"
        f"{owner}/{repo}/contributors"
    )

    contributors = []

    for page in range(
        1,
        max_pages + 1,
    ):

        params = {
            "per_page": 100,
            "page": page,
        }

        try:

            batch = github_get(
                url,
                params=params,
            )

        except requests.HTTPError as exc:

            response = exc.response

            if (
                response is not None
                and response.status_code == 403
            ):

                return {
                    "status": "unavailable",
                    "data": [],
                }

            raise

        if not batch:
            break

        contributors.extend(
            batch
        )

        if len(batch) < 100:
            break

    return {
        "status": "success",
        "data": contributors,
    }


# ============================================================
# REFERENCE DATASET
# ============================================================

def build_reference_scores():
    """
    Load the 300-repository research reference dataset.
    """

    if not REFERENCE_DATASET.exists():

        raise FileNotFoundError(
            "Reference dataset not found: "
            f"{REFERENCE_DATASET}"
        )

    return pd.read_csv(
        REFERENCE_DATASET
    )


# ============================================================
# PERCENTILE NORMALIZATION
# ============================================================

def percentile_against_reference(
    value,
    reference_series,
    higher_is_better=True,
):
    """
    Percentile-normalize a live value against
    the 300-repository reference sample.
    """

    reference = pd.to_numeric(
        reference_series,
        errors="coerce",
    ).dropna()

    if (
        value is None
        or pd.isna(value)
        or len(reference) == 0
    ):
        return np.nan

    percentile = (
        (reference <= value).sum()
        / len(reference)
        * 100
    )

    if not higher_is_better:

        percentile = (
            100 - percentile
        )

    return float(
        np.clip(
            percentile,
            0,
            100,
        )
    )


# ============================================================
# LIVE FEATURE ENGINEERING
# ============================================================

def build_live_features(
    metadata,
    commit_activity,
    commit_count,
    contributor_result,
):
    """
    Build live repository-level features.
    """

    now = datetime.now(
        timezone.utc
    )

    # ========================================================
    # DATES
    # ========================================================

    created_at = pd.to_datetime(
        metadata.get(
            "created_at"
        ),
        utc=True,
    )

    updated_at = pd.to_datetime(
        metadata.get(
            "updated_at"
        ),
        utc=True,
    )

    pushed_at = pd.to_datetime(
        metadata.get(
            "pushed_at"
        ),
        utc=True,
    )

    repository_age_days = (
        now - created_at
    ).days

    days_since_update = (
        now - updated_at
    ).total_seconds() / 86400

    days_since_push = (
        now - pushed_at
    ).total_seconds() / 86400

    # ========================================================
    # WEEKLY ACTIVITY
    # ========================================================

    weeks = commit_activity.get(
        "weeks",
        [],
    )

    weekly_counts = []

    week_dates = []

    for week in weeks:

        total = week.get(
            "total",
            0,
        )

        try:
            total = int(total)
        except Exception:
            total = 0

        weekly_counts.append(
            total
        )

        timestamp = week.get(
            "week"
        )

        if timestamp is not None:

            try:

                week_date = pd.to_datetime(
                    timestamp,
                    unit="s",
                    utc=True,
                )

                week_dates.append(
                    week_date
                )

            except Exception:
                pass

    # ========================================================
    # ACTIVITY FEATURES
    # ========================================================

    if weekly_counts:

        active_weeks = sum(
            count > 0
            for count in weekly_counts
        )

        peak_weekly_commits = max(
            weekly_counts
        )

        mean_weekly_commits = float(
            np.mean(
                weekly_counts
            )
        )

        monthly_labels = set()

        for date in week_dates:

            if date is not None:

                monthly_labels.add(
                    date.strftime(
                        "%Y-%m"
                    )
                )

        active_months = len(
            monthly_labels
        )

    else:

        active_weeks = 0

        peak_weekly_commits = 0

        mean_weekly_commits = 0.0

        active_months = 0

    # ========================================================
    # MONTHLY AVERAGE
    # ========================================================

    if active_months > 0:

        mean_monthly_commits = (
            commit_count
            / active_months
        )

    else:

        mean_monthly_commits = 0.0

    # ========================================================
    # CONTRIBUTORS
    # ========================================================

    contributor_status = (
        contributor_result.get(
            "status"
        )
    )

    contributor_data = (
        contributor_result.get(
            "data",
            [],
        )
    )

    if contributor_status == "success":

        contributors_count = len(
            contributor_data
        )

        contribution_values = []

        for item in contributor_data:

            value = item.get(
                "contributions",
                0,
            )

            try:
                value = int(value)
            except Exception:
                value = 0

            contribution_values.append(
                value
            )

        total_contributions = sum(
            contribution_values
        )

        if (
            contribution_values
            and total_contributions > 0
        ):

            top_contributor_share = (
                max(
                    contribution_values
                )
                / total_contributions
            )

        else:

            top_contributor_share = np.nan

    else:

        contributors_count = np.nan

        total_contributions = np.nan

        top_contributor_share = np.nan

    # ========================================================
    # RETURN
    # ========================================================

    return {

        "full_name":
            metadata.get(
                "full_name"
            ),

        "language":
            metadata.get(
                "language"
            ),

        "stars":
            metadata.get(
                "stargazers_count",
                0,
            ),

        "forks":
            metadata.get(
                "forks_count",
                0,
            ),

        "open_issues":
            metadata.get(
                "open_issues_count",
                0,
            ),

        "size_kb":
            metadata.get(
                "size",
                0,
            ),

        "repository_age_days":
            repository_age_days,

        "repository_age_years":
            repository_age_days
            / 365.25,

        "days_since_update":
            days_since_update,

        "days_since_push":
            days_since_push,

        "commits_365d":
            int(commit_count),

        "active_months":
            active_months,

        "active_weeks":
            active_weeks,

        "peak_weekly_commits":
            peak_weekly_commits,

        "mean_weekly_commits":
            mean_weekly_commits,

        "mean_monthly_commits":
            mean_monthly_commits,

        "contributors_count":
            contributors_count,

        "total_contributions":
            total_contributions,

        "top_contributor_share":
            top_contributor_share,

        "contributor_status":
            contributor_status,
    }


# ============================================================
# HEALTH INDEX
# ============================================================

def calculate_health_index(
    live_features,
    reference,
):
    """
    Calculate the OpenSourcePulse Health Index.

    Five equally weighted dimensions:

        Popularity                 20%
        Activity                   20%
        Maintenance                20%
        Community                  20%
        Contribution Distribution  20%

    The score is comparative within the reference sample.
    """

    # ========================================================
    # POPULARITY
    # ========================================================

    stars_score = percentile_against_reference(
        live_features["stars"],
        reference["stars"],
        higher_is_better=True,
    )

    forks_score = percentile_against_reference(
        live_features["forks"],
        reference["forks"],
        higher_is_better=True,
    )

    popularity_score = np.nanmean(
        [
            stars_score,
            forks_score,
        ]
    )

    # ========================================================
    # ACTIVITY
    # ========================================================

    commits_score = percentile_against_reference(
        live_features["commits_365d"],
        reference["commits_365d"],
        higher_is_better=True,
    )

    active_months_score = percentile_against_reference(
        live_features["active_months"],
        reference["active_months"],
        higher_is_better=True,
    )

    activity_score = np.nanmean(
        [
            commits_score,
            active_months_score,
        ]
    )

    # ========================================================
    # MAINTENANCE
    # ========================================================

    push_score = percentile_against_reference(
        live_features["days_since_push"],
        reference["days_since_push"],
        higher_is_better=False,
    )

    update_score = percentile_against_reference(
        live_features["days_since_update"],
        reference["days_since_update"],
        higher_is_better=False,
    )

    maintenance_score = np.nanmean(
        [
            push_score,
            update_score,
        ]
    )

    # ========================================================
    # COMMUNITY
    # ========================================================

    contributor_score = percentile_against_reference(
        live_features["contributors_count"],
        reference["contributors_count"],
        higher_is_better=True,
    )

    contribution_score = percentile_against_reference(
        live_features["total_contributions"],
        reference["total_contributions"],
        higher_is_better=True,
    )

    community_score = np.nanmean(
        [
            contributor_score,
            contribution_score,
        ]
    )

    # ========================================================
    # CONTRIBUTION DISTRIBUTION
    # ========================================================

    distribution_score = percentile_against_reference(
        live_features[
            "top_contributor_share"
        ],
        reference[
            "top_contributor_share"
        ],
        higher_is_better=False,
    )

    # ========================================================
    # DIMENSIONS
    # ========================================================

    dimensions = {

        "popularity_score":
            popularity_score,

        "activity_score":
            activity_score,

        "maintenance_score":
            maintenance_score,

        "community_score":
            community_score,

        "distribution_score":
            distribution_score,
    }

    # ========================================================
    # FINAL HEALTH SCORE
    # ========================================================

    valid_scores = [
        score
        for score in dimensions.values()
        if not pd.isna(score)
    ]

    if valid_scores:

        health_score = float(
            np.mean(
                valid_scores
            )
        )

    else:

        health_score = np.nan

    coverage = (
        len(valid_scores)
        / len(dimensions)
        * 100
    )

    # ========================================================
    # PROFILE
    # ========================================================

    if pd.isna(
        health_score
    ):

        profile = "Unavailable"

    elif health_score < 25:

        profile = "Developing"

    elif health_score < 50:

        profile = "Moderate"

    elif health_score < 75:

        profile = "High"

    else:

        profile = "Very High"

    return {

        **dimensions,

        "health_score":
            health_score,

        "health_score_coverage":
            coverage,

        "health_profile":
            profile,
    }


# ============================================================
# MAIN ANALYZER
# ============================================================

def analyze_repository(
    repository_url,
):
    """
    Complete live repository analysis.
    """

    # --------------------------------------------------------
    # URL
    # --------------------------------------------------------

    owner, repo = parse_repository_url(
        repository_url
    )

    # --------------------------------------------------------
    # METADATA
    # --------------------------------------------------------

    metadata = fetch_repository(
        owner,
        repo,
    )

    # --------------------------------------------------------
    # AGGREGATE ACTIVITY
    # --------------------------------------------------------

    commit_activity = (
        fetch_commit_activity(
            owner,
            repo,
        )
    )

    # --------------------------------------------------------
    # EXACT 365-DAY COUNT
    # --------------------------------------------------------

    commit_count = fetch_commit_count(
        owner,
        repo,
        days=365,
    )

    # --------------------------------------------------------
    # CONTRIBUTORS
    # --------------------------------------------------------

    contributor_result = (
        fetch_contributors(
            owner,
            repo,
        )
    )

    # --------------------------------------------------------
    # FEATURES
    # --------------------------------------------------------

    live_features = build_live_features(
        metadata,
        commit_activity,
        commit_count,
        contributor_result,
    )

    # --------------------------------------------------------
    # REFERENCE DATA
    # --------------------------------------------------------

    reference = (
        build_reference_scores()
    )

    # --------------------------------------------------------
    # HEALTH
    # --------------------------------------------------------

    health = calculate_health_index(
        live_features,
        reference,
    )

    # ========================================================
    # DASHBOARD DIMENSIONS
    # ========================================================

    dimensions = {

        "popularity":
            health["popularity_score"],

        "activity":
            health["activity_score"],

        "maintenance":
            health["maintenance_score"],

        "community":
            health["community_score"],

        "distribution":
            health["distribution_score"],
    }

    # ========================================================
    # COVERAGE
    # ========================================================

    coverage = {

        "overall":
            health[
                "health_score_coverage"
            ],
    }

    # ========================================================
    # DASHBOARD HEALTH OBJECT
    # ========================================================

    dashboard_health = {

        "score":
            health["health_score"],

        "profile":
            health["health_profile"],

        "coverage":
            health[
                "health_score_coverage"
            ],

        "health_score":
            health["health_score"],

        "health_profile":
            health["health_profile"],

        "health_score_coverage":
            health[
                "health_score_coverage"
            ],

        "popularity_score":
            health["popularity_score"],

        "activity_score":
            health["activity_score"],

        "maintenance_score":
            health["maintenance_score"],

        "community_score":
            health["community_score"],

        "distribution_score":
            health["distribution_score"],
    }

    # ========================================================
    # FINAL RESULT
    # ========================================================

    return {

        "repository": {

            "full_name":
                metadata.get(
                    "full_name"
                ),

            "html_url":
                metadata.get(
                    "html_url"
                ),

            "description":
                metadata.get(
                    "description"
                ),

            "stars":
                metadata.get(
                    "stargazers_count",
                    0,
                ),

            "forks":
                metadata.get(
                    "forks_count",
                    0,
                ),
        },

        "features":
            live_features,

        "health":
            dashboard_health,

        "dimensions":
            dimensions,

        "coverage":
            coverage,

        # Original backend fields
        "owner":
            owner,

        "repo":
            repo,

        "url":
            metadata.get(
                "html_url"
            ),

        "metadata":
            metadata,

        "commit_count":
            commit_count,

        "commit_activity":
            commit_activity,

        "contributor_result":
            contributor_result,
    }


# ============================================================
# DIRECT TERMINAL TEST
# ============================================================

if __name__ == "__main__":

    test_url = (
        "https://github.com/microsoft/vscode"
    )

    print()
    print("=" * 65)
    print(
        "OpenSourcePulse Live Analyzer Test"
    )
    print("=" * 65)
    print()

    start_time = time.time()

    result = analyze_repository(
        test_url
    )

    elapsed = (
        time.time()
        - start_time
    )

    print()
    print("=" * 65)
    print("RESULT")
    print("=" * 65)

    print(
        "Repository:",
        result[
            "repository"
        ][
            "full_name"
        ],
    )

    print(
        "Stars:",
        result[
            "repository"
        ][
            "stars"
        ],
    )

    print(
        "Forks:",
        result[
            "repository"
        ][
            "forks"
        ],
    )

    print(
        "Commits · 365d:",
        result[
            "features"
        ][
            "commits_365d"
        ],
    )

    print(
        "Active Months:",
        result[
            "features"
        ][
            "active_months"
        ],
    )

    print(
        "Mean Monthly Commits:",
        round(
            result[
                "features"
            ][
                "mean_monthly_commits"
            ],
            1,
        ),
    )

    print(
        "Contributors:",
        result[
            "features"
        ][
            "contributors_count"
        ],
    )

    print(
        "Health Index:",
        round(
            result[
                "health"
            ][
                "score"
            ],
            2,
        ),
    )

    print(
        "Health Profile:",
        result[
            "health"
        ][
            "profile"
        ],
    )

    print(
        "Coverage:",
        round(
            result[
                "health"
            ][
                "coverage"
            ],
            2,
        ),
        "%",
    )

    print(
        "Elapsed Time:",
        round(
            elapsed,
            2,
        ),
        "seconds",
    )

    print("=" * 65)