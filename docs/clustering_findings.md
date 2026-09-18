# OpenSourcePulse — Clustering Findings

## K-Means Repository Profiling

K-Means clustering was evaluated for k = 2 through k = 8 using both inertia
and silhouette score.

The highest tested silhouette score occurred at k = 3 (0.2984). However,
the k = 3 solution isolated only two repositories into a separate cluster,
representing 0.67% of the complete observations. These repositories,
openclaw/openclaw and torvalds/linux, had exceptionally high recent commit
activity.

The k = 2 solution produced two substantially more balanced groups:

- Cluster 0: 155 repositories (52.01%)
- Cluster 1: 143 repositories (47.99%)

The k = 2 silhouette score was 0.2924.

Therefore, k = 2 was used for the main repository-profile analysis, while
the k = 3 solution was retained as a sensitivity/outlier finding.

## Cluster 0 — Lower Recent-Activity Profile

The median repository in Cluster 0 had:

- 2,489 stars
- 330 forks
- 0 commits during the recent activity window
- 15 contributors
- 0 active months
- 420 days since the last push
- 2 days since the last metadata update
- 9.98 years of repository age
- 0.766 top-contributor share

## Cluster 1 — Higher Popularity/Activity/Community Profile

The median repository in Cluster 1 had:

- 43,920 stars
- 4,455 forks
- 326 recent commits
- 209 contributors
- 12 active months
- 3 days since the last push
- 0 days since the last metadata update
- 8.10 years of repository age
- 0.416 top-contributor share

## Interpretation

The two clusters differ simultaneously across popularity, recent activity,
community participation, maintenance recency, and contributor concentration.

Cluster 1 shows substantially higher median popularity, activity, contributor
count, and activity-month coverage, together with substantially more recent
push activity.

Cluster 0 shows lower recent activity and smaller contributor communities in
the analytical sample.

These are descriptive repository profiles rather than classifications of
repository quality. Cluster labels do not imply that one group is universally
better or worse.

## Important Limitation

The clustering is exploratory. The silhouette score of 0.2924 indicates
moderate rather than highly separated clusters.

The repositories were selected using star-count strata, so the results should
be interpreted within the analytical sample rather than generalized to all
GitHub repositories.

The two API-error repositories were excluded from PCA/K-Means because their
recent commit data was unavailable.