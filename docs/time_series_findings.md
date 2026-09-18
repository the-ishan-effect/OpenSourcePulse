# OpenSourcePulse — Time-Series Findings

## Objective

Time-series analysis was performed using actual commit timestamps collected
over the recent 365-day observation window.

The analysis examines monthly repository activity, active repository coverage,
activity intensity, repository activity trajectories, and concentration of
commit activity.

## Data Preparation

The commit dataset initially contained 381,308 records.

Nine duplicate repository-commit records were identified and removed using
the combination of repository ID and commit SHA.

The final time-series analysis therefore used 381,299 unique repository-commit
records.

The observed timestamp range was:

2025-09-18 to 2026-09-18

The data therefore produces 13 calendar-month labels. September 2025 and
September 2026 are partial observation periods and are not directly comparable
with complete calendar months.

## Monthly Activity

The highest observed monthly commit count was:

- May 2026: 43,781 commits
- Active repositories: 134

The lowest observed monthly commit count was:

- September 2025: 8,031 commits
- Active repositories: 105

The low September 2025 value is partly attributable to the partial-month
observation window.

Monthly activity fluctuated substantially throughout the observation period.
Examples include a 53.88% month-over-month increase in January 2026, a 25.54%
decline in June 2026, and a 23.80% increase in July 2026.

## Activity per Active Repository

Commits per active repository were calculated to distinguish aggregate activity
from changes in the number of participating repositories.

The observed values ranged from:

- September 2025: 76.49
- May 2026: 326.72

This normalization provides additional context because the number of active
repositories varies across months.

## Repository Activity Coverage

Among repositories represented in the collected commit dataset, the number of
active months varied substantially.

The distribution included repositories active for only one or a few months as
well as repositories active across all 13 calendar-month labels.

This demonstrates heterogeneous temporal participation across repositories.

## Activity Concentration

Recent commit activity was highly concentrated among a relatively small
number of repositories.

The cumulative shares of collected commits were:

- Top 5 repositories: 61.76%
- Top 10 repositories: 72.49%
- Top 20 repositories: 81.42%
- Top 50 repositories: 94.09%

Therefore, aggregate commit totals are strongly influenced by a relatively
small number of highly active repositories.

## Repository Trajectories

Individual repository trajectories showed substantially different activity
patterns.

Some repositories displayed sustained activity across many months, while
others showed intermittent or low activity.

Highly active repositories also displayed substantial month-to-month
variation rather than perfectly constant activity.

## Relationship to Clustering

The concentration analysis provides context for the K-Means results.

The k = 3 clustering solution isolated two extremely high-activity
repositories into a small cluster. The time-series analysis independently
shows that repository-level commit activity is highly concentrated, with the
top five repositories accounting for 61.76% of collected commits.

This indicates that extreme activity observations are an important structural
characteristic of the dataset rather than observations that should
automatically be removed.

## Interpretation

The time-series analysis demonstrates that repository activity is dynamic,
heterogeneous, and highly concentrated.

Aggregate monthly activity should therefore be interpreted together with:

- the number of active repositories,
- activity per active repository,
- repository-level trajectories,
- and concentration among highly active repositories.

## Limitations

The dataset represents an analytical stratified sample rather than a
population-representative sample of GitHub repositories.

The first and final calendar months are partial observation periods.

The commit collection covered repositories for which commit history could be
successfully retrieved. Two repositories had API collection errors and were
therefore not included in complete activity-based analyses.

The time-series analysis describes observed activity patterns and does not
establish causal explanations for changes in commit volume.