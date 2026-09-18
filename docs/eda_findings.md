# OpenSourcePulse — Exploratory Data Analysis Findings

## 1. Dataset Overview

The final analytical dataset contains 300 GitHub repositories selected using
stratified sampling based on repository star-count ranges.

The dataset contains repository metadata, popularity indicators, activity
features, contributor information, temporal features, and engineered
repository-level measures.

Duplicate repository IDs: 0

All repositories in the original sample are non-fork and non-archived
repositories.

---

## 2. Missing-Value Findings

The main missing values in the raw repository data were:

| Feature | Missing Count | Missing Percentage |
|---|---:|---:|
| Description | 3 | 1.00% |
| Language | 25 | 8.33% |
| Topics | 83 | 27.67% |
| License | 41 | 13.67% |

These missing values were treated as structural/optional metadata rather than
automatically deleting the corresponding repositories.

Categorical values were handled using explicit labels such as:

- No description provided
- Unknown
- No topics specified
- No license specified

---

## 3. Popularity Distribution

Repository popularity is highly right-skewed.

| Statistic | Stars |
|---|---:|
| Mean | 43,782.69 |
| Median | 9,772.50 |
| Minimum | 200 |
| Maximum | 547,866 |

The large difference between the mean and median demonstrates the influence
of highly popular repositories.

Therefore, log1p transformation was examined for popularity-related
analysis.

---

## 4. Activity Distribution

Recent repository activity was measured using commits collected during the
365-day analysis window.

| Statistic | Commits in 365 Days |
|---|---:|
| Mean | 1,270.997 |
| Median | 28.5 |
| Maximum | 96,177 |

The activity distribution is strongly right-skewed because a relatively small
number of repositories have extremely high recent commit activity.

Log transformation substantially reduced this skewness and made the feature
more suitable for correlation and multivariate analysis.

---

## 5. Contributor Distribution

The contributor count is also highly heterogeneous.

| Statistic | Contributors |
|---|---:|
| Mean | 125.52 |
| Median | 46.5 |
| Maximum | 474 |

The difference between mean and median indicates that some repositories have
substantially larger contributor communities than the typical repository in
the sample.

---

## 6. Fork and Popularity Relationship

The correlation between log-transformed stars and log-transformed forks was:

**r = 0.939**

This represents a very strong positive association in the analytical sample.

This indicates that repositories with greater popularity generally also have
larger numbers of forks.

However, correlation does not establish causation.

---

## 7. Popularity and Activity

The correlation between popularity and recent activity was:

**r = 0.521**

This indicates a moderate positive association.

The popularity/activity quartile analysis also showed a difference between
lower- and higher-popularity repositories.

Among the lower-popularity group:

- 57.89% had no recent activity
- 2.63% belonged to the highest activity group

Among the higher-popularity group:

- 10.67% had no recent activity
- 48.00% belonged to the highest activity group

These observations indicate an association between popularity and activity
within the analytical sample, but they do not establish a causal relationship.

---

## 8. Popularity and Contributors

The correlation between popularity and contributor count was:

**r = 0.614**

This indicates a moderate-to-strong positive association.

Repositories with higher popularity tend to have larger contributor
communities within this analytical sample.

---

## 9. Contributors and Activity

The correlation between contributor count and recent activity was:

**r = 0.596**

This indicates a moderate positive association between the size of the
contributor community and recent commit activity.

This relationship supports examining community participation as a separate
dimension of repository health.

---

## 10. Repository Age and Activity

The correlation between repository age and recent activity was:

**r = -0.280**

This represents a weak-to-moderate negative association.

Repository age alone therefore does not appear to explain recent activity
strongly in this analytical sample.

---

## 11. Push Recency and Activity

The correlation between days since the last push and recent activity was:

**r = -0.591**

The negative relationship indicates that repositories with fewer days since
their latest push tend to have greater recent activity.

This relationship is consistent with the interpretation of push recency as a
maintenance/activity indicator.

---

## 12. Outlier Findings

IQR-based analysis identified substantial numbers of high-end observations:

| Feature | IQR Outliers |
|---|---:|
| Stars | 34 |
| Forks | 36 |
| Open issues | 42 |
| Repository size | 51 |
| Recent commits | 52 |
| Contributors | 4 |
| Total contributions | 36 |

These observations were retained because they represent genuine differences
between GitHub repositories rather than automatically treating extreme values
as errors.

---

## 13. Transformation Findings

Log1p transformation substantially reduced skewness in highly skewed
variables.

Examples:

| Feature | Before | After |
|---|---:|---:|
| Stars | 3.070 | 0.086 |
| Forks | 3.325 | 0.120 |
| Open issues | 10.023 | 0.253 |
| Repository size | 16.637 | -0.085 |
| Recent commits | 10.979 | 0.324 |
| Contributors | 1.104 | -0.263 |
| Total contributions | 7.052 | -0.382 |
| Peak monthly commits | 11.831 | 0.406 |

The transformation therefore provides a more balanced representation for
subsequent multivariate analysis.

---

## 14. Language-Level Analysis

Programming language was examined as a categorical dimension.

The dataset contains repositories across multiple programming languages,
with Python, JavaScript, TypeScript, C++, and Go among the more frequently
represented languages.

Language-wise distributions of recent commits and contributors were examined
using boxplots and grouped descriptive statistics.

These comparisons help identify whether repository activity and community
size vary across language categories.

---

## 15. Overall EDA Insights

The EDA indicates that repository quality cannot reasonably be represented by
stars alone.

Several dimensions show meaningful relationships:

- Popularity is associated with activity.
- Popularity is strongly associated with forks.
- Popularity is associated with contributor count.
- Contributor count is associated with recent activity.
- Push recency is associated with recent activity.
- Repository age has a weaker relationship with recent activity.
- Repository-level variables contain substantial outliers and skewness.

These observations motivate the subsequent construction of a multidimensional
repository analysis framework.

The EDA therefore provides the basis for examining repository health using
multiple dimensions rather than relying exclusively on popularity.

---

## 16. Methodological Cautions

The findings should be interpreted within the scope of the project dataset.

The repositories were selected using star-count strata, so the sample is an
analytical stratified sample rather than a population-representative random
sample of all GitHub repositories.

Correlation results describe associations and should not be interpreted as
causal effects.

Activity-based analysis must also distinguish successfully collected
repositories from repositories for which GitHub API activity data was
unavailable.

Therefore, API collection status is retained as part of the analysis
pipeline.