# OpenSourcePulse

## GitHub Repository Intelligence System

> **Beyond Stars: Exploring the Health, Activity & Collaboration of Open-Source Projects**

OpenSourcePulse is an Exploratory Data Analysis (EDA) and repository intelligence system that studies GitHub repositories beyond conventional popularity metrics such as stars.

The system combines **data collection, data quality analysis, preprocessing, descriptive statistics, visualization, correlation analysis, outlier analysis, dimensionality reduction, clustering, time-series analysis, contributor network analysis, and an interpretable Repository Health Index**.

It also includes a **live GitHub repository analyzer** that allows a user to enter a repository URL and obtain an analytical profile using the same reference distribution developed during the EDA study.

---

## 1. Project Overview

GitHub repository popularity is commonly judged using metrics such as:

- Stars
- Forks
- Watchers

However, popularity alone does not fully describe the characteristics of a repository.

A repository may have many stars but limited recent activity, while another repository may have fewer stars but demonstrate strong maintenance, contributor participation, and sustained development.

OpenSourcePulse therefore investigates multiple dimensions of repository behavior:

- Popularity
- Development activity
- Maintenance recency
- Community participation
- Contributor distribution
- Repository age
- Repository size
- Issues and forks
- Temporal activity
- Contributor collaboration

The project is designed as an **EDA-first analytical system**, where advanced techniques such as PCA and K-Means are used to extend the exploratory analysis rather than replace it.

---

## 2. Problem Statement

GitHub repository stars provide a useful popularity signal, but they do not capture the complete behavioral characteristics of an open-source project.

The problem addressed by OpenSourcePulse is:

> **How can exploratory data analysis be used to understand repository health, activity, maintenance, community participation, temporal behavior, and contributor collaboration beyond simple popularity metrics?**

The project investigates whether multidimensional repository characteristics reveal patterns that cannot be observed from stars alone.

---

## 3. Objectives

The major objectives are:

1. Collect repository metadata from GitHub using the GitHub REST API.
2. Construct a structured analytical dataset containing numerical and categorical variables.
3. Perform systematic data-quality inspection.
4. Identify missing values, duplicates, inconsistent values, and potential outliers.
5. Apply appropriate preprocessing and transformation techniques.
6. Perform descriptive and exploratory statistical analysis.
7. Study relationships between repository popularity, activity, maintenance, and community participation.
8. Analyze repository distributions across programming languages.
9. Investigate potential outliers using statistical methods.
10. Apply PCA for dimensionality reduction and multivariate interpretation.
11. Apply K-Means clustering to identify repository profiles.
12. Analyze repository activity using genuine commit timestamps.
13. Study contributor-repository relationships using network analysis.
14. Develop an interpretable multidimensional Repository Health Index.
15. Build an interactive Streamlit dashboard.
16. Provide live analysis of user-specified GitHub repositories.
17. Convert EDA findings into an accessible repository intelligence system.

---

## 4. Research Questions

OpenSourcePulse is structured around the following research questions:

### RQ1 â€” Popularity vs Health

**Does repository popularity correspond to broader repository health characteristics?**

### RQ2 â€” Activity and Maintenance

**Which repository characteristics are associated with higher activity and maintenance?**

### RQ3 â€” Repository Profiles

**Can repositories be grouped into meaningful activity, popularity, and community profiles?**

### RQ4 â€” Programming Languages

**How do repository characteristics differ across programming languages?**

### RQ5 â€” Temporal Behavior

**How does repository activity evolve over time?**

### RQ6 â€” Contributor Collaboration

**What structural patterns emerge from contributor-repository relationships?**

### RQ7 â€” Multidimensional Health

**Can a multidimensional health index provide information beyond stars alone?**

---

## 5. Dataset

### Reference Dataset

The primary analytical dataset contains:

- **300 GitHub repositories**
- **20 original repository variables**
- Additional engineered analytical features

The repositories were selected using **star-stratified sampling** across multiple popularity ranges.

This was done to prevent the analysis from being dominated exclusively by extremely popular repositories.

### Sampling Strata

| Stratum | Stars | Target |
|---|---:|---:|
| P1 | 100â€“499 | 35 |
| P2 | 500â€“999 | 35 |
| P3 | 1,000â€“2,499 | 35 |
| P4 | 2,500â€“4,999 | 35 |
| P5 | 5,000â€“9,999 | 35 |
| P6 | 10,000â€“24,999 | 35 |
| P7 | 25,000â€“49,999 | 30 |
| P8 | 50,000â€“99,999 | 25 |
| P9 | 100,000â€“199,999 | 15 |
| P10 | â‰¥200,000 | 20 |
| **Total** | | **300** |

This is an **analytical stratified sample**, not a claim that the sample is statistically representative of the entire GitHub population.

---

## 6. Raw Repository Variables

The original repository dataset contains variables including:

- `repo_id`
- `repo_name`
- `owner`
- `full_name`
- `description`
- `html_url`
- `language`
- `topics`
- `license`
- `created_at`
- `updated_at`
- `pushed_at`
- `stars`
- `forks`
- `watchers`
- `open_issues`
- `size_kb`
- `default_branch`
- `is_fork`
- `archived`

Additional features are derived during preprocessing and feature engineering.

---

## 7. Data Collection

Repository metadata is collected through the **GitHub REST API**.

The collection pipeline uses:

- Python
- Requests
- GitHub REST API
- Environment-based API authentication
- Pandas

The GitHub API token is stored locally through an environment variable and is intentionally excluded from version control.

The collection process also records collection status and API availability information.

---

## 8. Data Quality Analysis

The 300-repository reference dataset was inspected for:

- Dataset dimensions
- Duplicate repository IDs
- Missing values
- Data types
- Invalid values
- Inconsistent categorical values
- Potential outliers

### Dataset Size

Rows: 300  
Columns: 20  
Duplicate repository IDs: 0

### Missing Values

| Variable | Missing | Percentage |
|---|---:|---:|
| Topics | 83 | 27.7% |
| License | 41 | 13.7% |
| Language | 25 | 8.3% |
| Description | 3 | 1.0% |

All other original repository variables had no missing values in the reference metadata dataset.

The missingness was inspected rather than silently treating missing values as meaningful numerical zeros.

---

## 9. Data Preprocessing

The preprocessing workflow includes:

1. Duplicate detection
2. Datetime conversion
3. Language normalization
4. Explicit handling of missing categorical values
5. Negative-value validation
6. Distribution analysis
7. Log transformation of strongly right-skewed numerical variables
8. IQR-based outlier identification
9. Preservation of genuine extreme observations

Several GitHub metrics exhibit heavy right-skew because a small number of repositories are extremely popular or active.

### Examples of Highly Skewed Variables

| Variable | Skewness Before |
|---|---:|
| Stars | 3.070 |
| Forks | 3.325 |
| Open issues | 10.023 |
| Repository size | 16.637 |
| Commits in 365 days | 10.942 |
| Total contributions | 7.041 |
| Peak monthly commits | 11.792 |

Log transformation substantially reduced these skewness values.

For example:

```text
log1p(x) = log(1 + x)
```

was used for appropriate highly skewed count variables.

Importantly, the project **does not automatically remove statistical outliers**. Extreme repositories can represent genuine GitHub behavior and therefore remain part of the analysis unless a specific analytical method requires otherwise.

---

## 10. Descriptive Exploratory Data Analysis

The project performs:

- Univariate analysis
- Bivariate analysis
- Multivariate analysis
- Distribution analysis
- Correlation analysis
- Group comparisons
- Outlier analysis
- Language-wise comparisons

### Popularity Statistics

For repository stars:

```text
Mean: 43,782.693
Median: 9,772.5
Minimum: 200
Maximum: 547,866
```

The substantial difference between the mean and median demonstrates the strong right-skew of repository popularity.

---

## 11. Programming Language Analysis

The dataset contains repositories across multiple programming languages.

The most frequent observed languages include:

- Python
- JavaScript
- TypeScript
- C++
- Go
- Java
- Rust
- C#
- C
- PHP
- Shell
- Kotlin
- Jupyter
- HTML
- Objective-C

Missing language values are retained as an explicit missing category during appropriate categorical analyses.

Language normalization is also applied to resolve inconsistent categorical representations such as variations in Vim Script naming.

---

## 12. Correlation Analysis

Correlation analysis is used to investigate relationships between repository characteristics.

Selected Pearson correlations observed in the analytical dataset include:

| Relationship | Correlation |
|---|---:|
| Popularity â†” Activity | 0.521 |
| Popularity â†” Contributors | 0.614 |
| Popularity â†” Forks | 0.939 |
| Age â†” Activity | -0.280 |
| Push Recency â†” Activity | -0.591 |
| Contributors â†” Activity | 0.596 |

These correlations describe associations within the sampled dataset.

They **do not establish causality**.

For example, a positive popularity-activity correlation does not prove that stars cause activity or that activity causes stars.

---

## 13. Popularity and Activity Analysis

Repositories were divided into popularity groups and activity groups to examine how repository behavior changes across popularity levels.

A clear pattern emerged:

- Lower-popularity repositories contain a larger proportion of repositories with limited recent activity.
- Higher-popularity repositories contain a larger proportion of repositories with higher recent activity.

For example, among the highest popularity group, approximately 48% belonged to the highest observed activity group.

The result suggests an association between popularity and recent activity, while still requiring caution because the analysis is observational.

---

## 14. Outlier Analysis

Potential outliers were identified using the **Interquartile Range (IQR)** method.

Examples of identified high-end observations include:

| Variable | IQR Outliers |
|---|---:|
| Stars | 34 |
| Forks | 36 |
| Open issues | 42 |
| Repository size | 51 |
| 365-day commits | 52 |
| Contributors | 4 |
| Total contributions | 36 |

These observations were not automatically deleted.

Instead, they were investigated as potentially meaningful extreme repository behaviors.

---

## 15. Commit Activity Dataset

The project collected repository commit information over a rolling approximately 365-day analytical window.

The collected commit dataset contains:

Raw commit observations: 381,308  
After repository + commit SHA deduplication: 381,299  
Repositories represented: 209

The analysis uses genuine GitHub commit timestamps rather than simulated activity.

This allows the project to investigate temporal development behavior.

---

## 16. Time-Series Analysis

Commit activity was aggregated by repository and month.

The resulting monthly activity dataset contains:

Rows: 1,740  
Repositories represented: 209  
Period: September 2025 â€“ September 2026

The analysis uses:

- Commit counts
- Active contributor counts
- Repository-level activity
- Monthly trends
- Relative concentration of development activity

The highest aggregate monthly commit count in the observed period occurred in:

**May 2026**

with approximately:

**43,781 commits**

The final September observations are partial-period observations and are therefore interpreted carefully.

---

## 17. Activity Concentration

Repository activity is highly concentrated.

Based on the observed commit dataset:

- Top 5 repositories â†’ **61.76%** of commits
- Top 10 repositories â†’ **72.49%**
- Top 20 repositories â†’ **81.42%**
- Top 50 repositories â†’ **94.09%**

This demonstrates why aggregate GitHub activity statistics can be heavily influenced by a relatively small number of highly active repositories.

---

## 18. Principal Component Analysis (PCA)

PCA is used to reduce the dimensionality of the multivariate repository feature space while retaining the major sources of variation.

The PCA input contains 15 standardized analytical features covering:

- Popularity
- Forks
- Issues
- Repository size
- Age
- Update recency
- Push recency
- Contributor metrics
- Contribution distribution
- Commit activity
- Active months
- Monthly activity statistics

Approximately **298 complete observations** are available for the PCA feature matrix after handling the required analytical missingness.

The PCA analysis identifies a substantially smaller set of components capable of representing most of the variation in the original feature space.

The final analysis retains enough principal components to cross the **90% cumulative explained-variance threshold**.

This reduces dimensionality while preserving the major multivariate structure.

---

## 19. K-Means Clustering

K-Means clustering is used to investigate whether repositories naturally form groups based on their multidimensional characteristics.

Candidate values:

**k = 2 ... 8**

were evaluated using:

- Inertia
- Silhouette score

Observed evaluation:

| k | Inertia | Silhouette |
|---:|---:|---:|
| 2 | 3041.10 | 0.2924 |
| 3 | 2482.24 | 0.2984 |
| 4 | 2108.77 | 0.2111 |
| 5 | 1890.59 | 0.1968 |
| 6 | 1706.91 | 0.1934 |
| 7 | 1570.60 | 0.1889 |
| 8 | 1482.12 | 0.1824 |

Although k=3 has a marginally higher silhouette score, it isolates only two extreme repositories into a very small subgroup.

The project therefore uses **k=2 as the primary interpretable clustering solution**, while retaining the k=3 result as a sensitivity observation.

---

## 20. K-Means Repository Profiles

The two primary clusters can be interpreted as:

### Cluster 0 â€” Lower Recent-Activity Profile

Typical characteristics include:

- Lower median popularity
- Lower contributor participation
- Very low recent commit activity
- Fewer active months
- Older repositories on average
- Greater contribution concentration

### Cluster 1 â€” Higher Popularity / Activity / Community Profile

Typical characteristics include:

- Higher median popularity
- Higher fork counts
- Higher recent commit activity
- More active months
- Larger contributor communities
- Lower top-contributor concentration

These cluster labels are descriptive.

They are **not equivalent to â€œbadâ€ and â€œgoodâ€ repositories**.

---

## 21. Contributor Analysis

Contributor information was collected to study community participation.

The contributor dataset contains approximately:

- **37,656 contributor-repository observations**
- **297 repositories represented**

Two extremely large repositories could not be fully enumerated through the GitHub contributors endpoint because GitHub restricts contributor-list retrieval for repositories with extremely large histories.

These cases are therefore represented as API-unavailable rather than incorrectly treated as zero contributors.

---

## 22. Contributor Network Analysis

OpenSourcePulse models relationships between contributors and repositories.

The network analysis investigates:

- Contributor degree
- Repository participation
- Contribution breadth
- Contributor centrality
- Contributor-repository relationships
- Collaboration structure

A focused network subgraph is used for interpretable visualization rather than attempting to render every relationship simultaneously.

The analytical network can therefore be explored through:

- Highly connected contributors
- Repositories with broad contributor participation
- Contributor collaboration structure
- Repository-community relationships

---

## 23. Repository Health Index

OpenSourcePulse introduces an interpretable **Repository Health Index** to summarize multiple dimensions of repository behavior.

The index uses five equally weighted dimensions:

| Dimension | Weight |
|---|---:|
| Popularity | 20% |
| Activity | 20% |
| Maintenance | 20% |
| Community | 20% |
| Contribution Distribution | 20% |

Each dimension is percentile-normalized against the 300-repository reference sample.

The resulting score is:

> **Comparative within the reference sample rather than an absolute measure of software quality.**

The index should not be interpreted as a predictive model or causal quality score.

---

## 24. Health Profiles

The primary Health Index produces four analytical profiles:

| Profile | Repositories |
|---|---:|
| Developing | 52 |
| Moderate | 97 |
| High | 99 |
| Very High | 52 |

The profiles are intended to summarize multidimensional repository characteristics.

They should not be interpreted as definitive judgments of software engineering quality.

---

## 25. Health Index vs Stars

The relationship between the Health Index and stars was explicitly evaluated.

Observed correlations include:

```text
Health Index vs raw stars:
Pearson r = 0.5256

Health Index vs log(stars):
Pearson r = 0.7868

Health Index vs stars:
Spearman Ï = 0.7896
```

A sensitivity analysis was also performed by excluding popularity from the Health Index.

The popularity-excluded index produced:

```text
Pearson correlation with raw stars = 0.4328
Pearson correlation with log(stars) = 0.6618
Spearman correlation = 0.6629
```

This supports an important interpretation:

> Popularity is strongly associated with broader repository characteristics, but stars alone do not completely characterize activity, maintenance, community participation, and contribution structure.

---

## 26. Health Rank Shifts

Some repositories change substantially in ranking when evaluated using the multidimensional Health Index rather than stars alone.

Examples include:

| Repository | Stars Rank | Health Rank | Shift |
|---|---:|---:|---:|
| `coopcycle/coopcycle-web` | 265 | 101 | +164 |
| `awslabs/mcp` | 158 | 42 | +116 |
| `ethereum-lists/chains` | 142 | 41 | +101 |
| `pymc-devs/pymc` | 154 | 52 | +102 |

Conversely, some highly starred repositories receive lower health ranks under the multidimensional analysis.

These differences illustrate the central project argument:

> **Popularity and multidimensional repository behavior are related, but they are not identical.**

---

## 27. Live GitHub Repository Analyzer

A major application layer of OpenSourcePulse allows users to enter a GitHub repository URL.

Example:

https://github.com/microsoft/vscode

The analyzer:

1. Parses the GitHub URL.
2. Retrieves repository metadata.
3. Retrieves recent commit activity.
4. Retrieves contributor information.
5. Constructs the required analytical features.
6. Applies the same dimensional framework used by the reference analysis.
7. Percentile-normalizes the live repository against the 300-repository reference sample.
8. Produces:
   - Health score
   - Health profile
   - Analytical dimensions
   - Coverage information

The reference dataset therefore serves as the analytical baseline, while the user-entered repository forms the live application layer.

---

## 28. Example Live Analysis

The live analyzer was tested using real GitHub repositories.

### Microsoft VS Code

- Health Score: approximately **92.53**
- Profile: **Very High**
- Coverage: **100%**

### Facebook React

- Health Score: approximately **91.58**
- Profile: **Very High**

### OpenAI Python

- Health Score: approximately **76.68**
- Profile: **Very High**

These examples are demonstrations of the implemented live analyzer and should not be interpreted as permanent scores because GitHub repository statistics change over time.

---

## 29. Dashboard

OpenSourcePulse includes an interactive Streamlit dashboard.

### Main Sections

#### Live Overview

Provides:

- GitHub repository input
- Live analysis
- Repository snapshot
- Health Index
- Analytical signals

#### EDA Explorer

Provides:

- Dataset overview
- Data-quality metrics
- Missing-value analysis
- Language distribution
- Popularity distributions
- Descriptive statistics

#### Activity Intelligence

Provides:

- Commit time series
- Monthly activity
- Active repositories
- Activity concentration
- Top active repositories

#### Multivariate Intelligence

Provides:

- Correlation analysis
- Research-question correlations
- PCA explained variance
- PCA loadings
- Repository PCA map
- K-Means evaluation
- Cluster profiles
- Popularity vs activity analysis

#### Network Analysis

Provides:

- Contributor statistics
- Repository participation
- Contributor centrality
- Collaboration information
- Contributor-repository relationships

#### Methodology

Documents:

- Data pipeline
- Analytical methods
- Health Index methodology
- Interpretation guidelines
- Limitations

---

## 30. System Architecture

```text
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚      GitHub REST API     â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                 â”‚
                                 â–¼
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚   Data Collection Layer  â”‚
                    â”‚ Repository + Contributorsâ”‚
                    â”‚        + Commits         â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                 â”‚
                                 â–¼
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚   Data Quality & Cleaningâ”‚
                    â”‚ Missing Values            â”‚
                    â”‚ Duplicates                â”‚
                    â”‚ Validation                â”‚
                    â”‚ Transformation            â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                 â”‚
                                 â–¼
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚   Feature Engineering    â”‚
                    â”‚ Age / Recency             â”‚
                    â”‚ Activity                  â”‚
                    â”‚ Contributors              â”‚
                    â”‚ Contribution Structure    â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                 â”‚
                                 â–¼
             â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
             â”‚                   â”‚                    â”‚
             â–¼                   â–¼                    â–¼
       Descriptive EDA       Multivariate        Temporal / Network
       Statistics            Analysis            Analysis
             â”‚                   â”‚                    â”‚
             â”‚              PCA + K-Means             â”‚
             â”‚                   â”‚                    â”‚
             â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¼â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                 â”‚
                                 â–¼
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚   Repository Health      â”‚
                    â”‚         Index            â”‚
                    â””â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”¬â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”˜
                                 â”‚
                    â”Œâ”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”´â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”
                    â”‚                         â”‚
                    â–¼                         â–¼
             Streamlit Dashboard       Live Repository
                                       Analyzer
```

---

## 31. Technology Stack

### Programming

- Python

### Data Analysis

- Pandas
- NumPy
- SciPy

### Visualization

- Plotly
- Matplotlib

### Machine Learning / Multivariate Analysis

- Scikit-learn
- PCA
- K-Means
- t-SNE where applicable

### Network Analysis

- NetworkX

### Dashboard

- Streamlit

### Data Collection

- GitHub REST API
- Requests
- python-dotenv

### Development

- Jupyter Notebook
- Git
- GitHub
- VS Code

---

## 32. Project Structure

```text
OpenSourcePulse/
â”‚
â”œâ”€â”€ README.md
â”œâ”€â”€ requirements.txt
â”œâ”€â”€ .gitignore
â”œâ”€â”€ .env.example
â”‚
â”œâ”€â”€ data/
â”‚   â”œâ”€â”€ raw/
â”‚   â”œâ”€â”€ processed/
â”‚   â””â”€â”€ external/
â”‚
â”œâ”€â”€ notebooks/
â”‚   â”œâ”€â”€ 05_descriptive_eda.ipynb
â”‚   â”œâ”€â”€ 07_dimensionality_reduction.ipynb
â”‚   â”œâ”€â”€ 09_time_series.ipynb
â”‚   â”œâ”€â”€ 10_network_analysis.ipynb
â”‚   â””â”€â”€ 11_health_score.ipynb
â”‚
â”œâ”€â”€ src/
â”‚   â”œâ”€â”€ data_collection/
â”‚   â”œâ”€â”€ preprocessing/
â”‚   â”œâ”€â”€ features/
â”‚   â”œâ”€â”€ analysis/
â”‚   â”œâ”€â”€ visualization/
â”‚   â”œâ”€â”€ health_score/
â”‚   â”œâ”€â”€ network/
â”‚   â””â”€â”€ product/
â”‚
â”œâ”€â”€ dashboard/
â”‚   â””â”€â”€ app.py
â”‚
â”œâ”€â”€ reports/
â”‚   â”œâ”€â”€ automated/
â”‚   â””â”€â”€ figures/
â”‚
â”œâ”€â”€ tests/
â”‚
â””â”€â”€ docs/
    â”œâ”€â”€ clustering_findings.md
    â”œâ”€â”€ data_dictionary.md
    â”œâ”€â”€ eda_findings.md
    â”œâ”€â”€ health_score.md
    â”œâ”€â”€ methodology.md
    â””â”€â”€ time_series_findings.md
```

---

## 33. Key Findings

### Finding 1 â€” Stars are highly skewed

A small number of repositories account for extremely high popularity values, making median and log-transformed analysis important.

### Finding 2 â€” Popularity and activity are associated

The observed correlation between popularity and activity is approximately:

**r = 0.521**

This indicates a moderate positive association within the reference sample.

### Finding 3 â€” Contributors are strongly associated with popularity and activity

Observed relationships include:

- Popularity â†” Contributors = **0.614**
- Contributors â†” Activity = **0.596**

### Finding 4 â€” Repository activity is highly concentrated

The top 10 repositories account for approximately **72.49%** of observed commits.

### Finding 5 â€” Repository activity varies substantially over time

Monthly commit activity changes considerably across the observed period.

### Finding 6 â€” Repository populations contain distinct profiles

K-Means identifies interpretable differences between lower-recent-activity repositories and higher-popularity/activity/community repositories.

### Finding 7 â€” Stars do not fully describe multidimensional repository behavior

The Health Index is positively associated with stars, but individual repositories can experience substantial rank shifts when multiple dimensions are considered.

### Finding 8 â€” Contribution structure provides an additional perspective

Contributor concentration and distribution capture a dimension that simple popularity metrics do not directly represent.

---

## 34. Limitations

The project has several important limitations.

### 1. Sample Limitation

The 300 repositories form a stratified analytical sample and are not intended to represent the entire GitHub ecosystem.

### 2. API Limitations

Some extremely large repositories cannot be completely enumerated through certain GitHub API endpoints.

### 3. Temporal Limitation

The commit analysis is based on an approximately 365-day observation window.

### 4. Partial Periods

The first and final months of the commit window can represent partial periods.

### 5. Health Index Interpretation

The Health Index is an analytical comparative index, not an objective or universally accepted definition of repository quality.

### 6. Correlation Is Not Causation

Observed statistical relationships should not be interpreted as causal relationships.

### 7. GitHub-Specific Data

The analysis reflects information available through GitHub and therefore does not capture every aspect of software-project health.

---

## 35. Reproducibility

The project separates the data pipeline into multiple layers.

### Raw Collection Layer

Raw API-generated data is kept locally, including the large commit-history dataset.

The full commit dataset is approximately **279 MB** and is intentionally excluded from normal Git tracking.

### Processed Analytical Layer

Compact processed datasets required for analysis are version-controlled under:

`data/processed/`

### Analytical Results

Derived analytical results are stored under:

`reports/`

These include:

- PCA results
- K-Means results
- Health Index results
- Correlation results
- Network statistics
- Activity summaries

---

## 36. Running the Project

### 1. Clone the Repository

```bash
git clone https://github.com/the-ishan-effect/OpenSourcePulse.git
cd OpenSourcePulse
```

### 2. Create a Virtual Environment

#### Windows

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

#### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure GitHub API Access

Create a local `.env` file:

```text
GITHUB_TOKEN=your_github_token_here
```

Never commit the `.env` file.

### 5. Launch the Dashboard

```bash
streamlit run dashboard/app.py
```

The Streamlit interface can then be opened in the browser.

---

## 37. Academic Alignment â€” BACSE301 EDA

OpenSourcePulse directly follows the recommended EDA workflow:

```text
Dataset Selection
       â†“
Problem Definition
       â†“
Data Understanding
       â†“
Data Quality Analysis
       â†“
Data Cleaning & Preprocessing
       â†“
Descriptive Statistics
       â†“
Univariate Analysis
       â†“
Bivariate Analysis
       â†“
Multivariate Analysis
       â†“
Outlier Detection
       â†“
Correlation Analysis
       â†“
Dimensionality Reduction
       â†“
Clustering
       â†“
Time-Series Analysis
       â†“
Network Analysis
       â†“
Interpretation
       â†“
Conclusions & Insights
```

The project emphasizes **why each analytical method is used and what insight it provides**, rather than simply generating visualizations.

---

## 38. Future Scope

Potential future extensions include:

- Larger and more diverse repository sampling
- More extensive historical GitHub data
- Pull-request lifecycle analysis
- Issue-resolution analysis
- Release-frequency analysis
- Repository topic modeling
- More advanced contributor community detection
- Historical Health Index tracking
- Repository health trajectories
- Automated anomaly detection
- More sophisticated live repository comparisons
- GitHub organization-level intelligence
- Cross-platform open-source analysis

---

## 39. Conclusion

OpenSourcePulse demonstrates how exploratory data analysis can transform raw GitHub repository metadata into a structured repository intelligence system.

The project moves beyond a single popularity metric by combining:

- Data quality analysis
- Statistical exploration
- Visualization
- Correlation analysis
- Outlier analysis
- PCA
- K-Means clustering
- Time-series analysis
- Contributor network analysis
- Multidimensional health scoring
- Live repository analysis

The central conclusion is:

> **GitHub stars provide an important popularity signal, but repository behavior is multidimensional. Activity, maintenance, community participation, contribution structure, and temporal behavior provide additional perspectives that are not captured by stars alone.**

OpenSourcePulse therefore combines the academic principles of EDA with a practical interactive application for repository intelligence.

---

## 40. References

1. GitHub REST API Documentation  
   https://docs.github.com/en/rest

2. Pandas Documentation  
   https://pandas.pydata.org/docs/

3. NumPy Documentation  
   https://numpy.org/doc/

4. Scikit-learn Documentation  
   https://scikit-learn.org/stable/

5. Plotly Python Documentation  
   https://plotly.com/python/

6. Streamlit Documentation  
   https://docs.streamlit.io/

7. NetworkX Documentation  
   https://networkx.org/documentation/stable/

---

## Project Information

**OpenSourcePulse â€” GitHub Repository Intelligence System**

**Course:** BACSE301 â€” Exploratory Data Analysis  
**Program:** B.Tech Computer Science and Engineering  
**Institution:** VIT Vellore  
**Academic Year:** 2026â€“27

> **Beyond Stars. Explore the Pulse of Open Source.**
