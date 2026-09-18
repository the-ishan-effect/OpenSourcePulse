\# OpenSourcePulse Data Dictionary



\## 1. Dataset Overview



OpenSourcePulse uses a stratified analytical sample of 300 public GitHub

repositories for exploratory data analysis.



Repositories were selected across predefined repository star-count strata.

Forked and archived repositories were excluded during collection.



The dataset is intended for comparative exploratory analysis across

repository popularity levels. It is not treated as a population-representative

sample of the entire GitHub ecosystem.



\---



\## 2. Raw Dataset



File:



`data/raw/repositories.csv`



Shape:



\- Rows: 300

\- Columns: 20

\- Duplicate `repo\_id`: 0



\---



\## 3. Raw Variables



| # | Variable | Data Type | Description | Source | Analytical Role |

|---|---|---|---|---|---|

| 1 | `repo\_id` | Integer | Unique GitHub repository identifier | GitHub API | Identifier |

| 2 | `repo\_name` | String | Repository name | GitHub API | Identifier / descriptive |

| 3 | `owner` | String | GitHub account or organization owning the repository | GitHub API | Descriptive |

| 4 | `full\_name` | String | Repository name in `owner/repository` format | GitHub API | Identifier / lookup |

| 5 | `description` | String | Repository description provided by its owner | GitHub API | Text / descriptive |

| 6 | `html\_url` | String | Web URL of the repository | GitHub API | Reference |

| 7 | `language` | Categorical | Primary programming language reported by GitHub | GitHub API | Categorical analysis |

| 8 | `topics` | String | Repository topics associated with the repository | GitHub API | Categorical / text analysis |

| 9 | `license` | String | Repository license identifier when available | GitHub API | Categorical analysis |

| 10 | `created\_at` | Date-time string | Repository creation timestamp | GitHub API | Temporal analysis |

| 11 | `updated\_at` | Date-time string | Timestamp of the most recent repository metadata update | GitHub API | Maintenance analysis |

| 12 | `pushed\_at` | Date-time string | Timestamp associated with the most recent push | GitHub API | Activity / recency analysis |

| 13 | `stars` | Integer | Number of GitHub stars | GitHub API | Popularity measure / stratification |

| 14 | `forks` | Integer | Number of repository forks | GitHub API | Community / popularity measure |

| 15 | `watchers` | Integer | Number of repository watchers reported by GitHub | GitHub API | Raw field; reviewed for redundancy |

| 16 | `open\_issues` | Integer | Number of currently open issues reported by GitHub | GitHub API | Issue-pressure indicator |

| 17 | `size\_kb` | Integer | Repository size in kilobytes reported by GitHub | GitHub API | Repository-scale variable |

| 18 | `default\_branch` | String | Name of the repository's default branch | GitHub API | Descriptive |

| 19 | `is\_fork` | Boolean | Indicates whether the repository is a fork | GitHub API | Eligibility filter |

| 20 | `archived` | Boolean | Indicates whether the repository is archived | GitHub API | Eligibility filter |



\---



\## 4. Missing-Value Profile



The raw dataset contains missing values in four variables:



| Variable | Missing Count | Missing Percentage |

|---|---:|---:|

| `description` | 3 | 1.0% |

| `language` | 25 | 8.3% |

| `topics` | 83 | 27.7% |

| `license` | 41 | 13.7% |



All remaining variables contain zero missing values in the collected dataset.



Missing values will be investigated during preprocessing rather than

automatically replaced without considering the semantic meaning of each

variable.



\---



\## 5. Data-Quality Observations



\### Duplicate repositories



No duplicate `repo\_id` values were detected.



Therefore:



`Duplicate repo\_id = 0`



\---



\### Fork and archive eligibility



All 300 repositories in the finalized dataset satisfy the collection

eligibility criteria:



\- `is\_fork = False`

\- `archived = False`



These variables are retained as audit/eligibility fields.



\---



\### Watcher redundancy



In the collected dataset, `watchers` has the same descriptive statistics

as `stars`, including identical minimum, maximum and mean values.



This indicates that the two variables provide redundant information in the

current dataset.



The relationship will be verified during preprocessing/correlation

analysis before feature selection. `watchers` will not automatically be

treated as an independent health dimension.



\---



\### Categorical inconsistency



The language field contains both:



\- `Vim script`

\- `Vim Script`



This represents a categorical-label normalization issue.



The raw `language` column will be preserved, while normalization will be

performed in the processed dataset.



\---



\## 6. Numerical Variables



The primary numerical variables currently available are:



\- `stars`

\- `forks`

\- `watchers`

\- `open\_issues`

\- `size\_kb`



Their distributions will be examined using:



\- descriptive statistics

\- histograms

\- boxplots

\- skewness

\- correlation analysis

\- outlier detection



Because several variables exhibit large differences between their mean and

median values, transformation and scaling will be evaluated during

preprocessing.



\---



\## 7. Temporal Variables



The dataset contains three raw temporal fields:



\- `created\_at`

\- `updated\_at`

\- `pushed\_at`



These will be converted from strings to appropriate datetime types.



Potential engineered temporal variables include:



\- repository age

\- days since last push

\- days since last metadata update

\- repository age in years



Historical activity trends require additional longitudinal data and will

not be inferred solely from these timestamps.



\---



\## 8. Raw vs Engineered Data



Raw variables represent values directly collected from GitHub.



Engineered variables will be created separately during preprocessing and

feature engineering.



Examples of potential engineered variables include:



\- `repository\_age\_days`

\- `repository\_age\_years`

\- `days\_since\_last\_push`

\- `days\_since\_update`

\- `fork\_star\_ratio`

\- `issue\_pressure`

\- `recent\_activity\_indicator`



Final engineered variables will only be introduced after examining the

available enriched GitHub data and establishing their analytical

justification.



\---



\## 9. Sampling Structure



The repository sample was stratified by star count.



| Stratum | Star Range | Target |

|---|---:|---:|

| P1 | 100–499 | 35 |

| P2 | 500–999 | 35 |

| P3 | 1,000–2,499 | 35 |

| P4 | 2,500–4,999 | 35 |

| P5 | 5,000–9,999 | 35 |

| P6 | 10,000–24,999 | 35 |

| P7 | 25,000–49,999 | 30 |

| P8 | 50,000–99,999 | 25 |

| P9 | 100,000–199,999 | 15 |

| P10 | ≥200,000 | 20 |

| \*\*Total\*\* | | \*\*300\*\* |



The sampling design provides observations across multiple popularity levels

for comparative EDA. It should not be interpreted as proportional

sampling of the complete GitHub repository population.



\---



\## 10. Planned Analytical Use



The raw variables provide the initial basis for analysis of:



1\. Repository popularity

2\. Repository scale

3\. Community engagement

4\. Maintenance recency

5\. Repository age

6\. Programming-language differences

7\. Missing-data patterns

8\. Outliers and skewness



Additional GitHub API data will be collected before finalizing measures of:



\- development activity

\- contributor participation

\- issue resolution

\- pull-request activity

\- releases

\- collaboration networks

\- longitudinal repository activity



This separation prevents the project from treating incomplete raw metadata

as if it already represented complete repository health.

