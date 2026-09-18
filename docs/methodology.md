\---



\# API Enrichment Strategy



\## Purpose



The initial repository dataset contains repository-level metadata collected

from the GitHub REST API. Additional enrichment is required to analyze

development activity, maintenance, community participation, collaboration,

and longitudinal behavior.



The enrichment strategy collects only variables that directly support the

project's research questions and Exploratory Data Analysis objectives.



\## Enrichment Layers



\### Repository Metadata



Already collected in:



`data/raw/repositories.csv`



Includes repository identity, programming language, topics, license,

timestamps, stars, forks, watchers, open issues, repository size, and

eligibility indicators.



\### Contributors



Raw contributor-level observations will be stored in:



`data/raw/repository\_contributors.csv`



Planned fields:



\- repository ID

\- repository name

\- contributor login

\- contributor ID

\- contribution count



Potential derived variables:



\- contributor count

\- total contributor contributions

\- top contributor share

\- contributor concentration



\### Commits



Raw commit observations will be stored in:



`data/raw/repository\_commits.csv`



The collection will use a defined observation window rather than attempting

to retrieve the complete lifetime history of every repository.



Planned fields:



\- repository ID

\- repository name

\- commit SHA

\- author

\- committer

\- commit timestamp



Potential derived variables:



\- commit count during observation window

\- active committers

\- commit rate

\- monthly commit activity



\### Issues



Raw issue observations will be stored in:



`data/raw/repository\_issues.csv`



Planned fields:



\- repository ID

\- issue number

\- creation timestamp

\- closing timestamp

\- state

\- author



Potential derived variables:



\- issues created during observation window

\- issues closed during observation window

\- issue resolution rate

\- issue resolution time

\- monthly issue activity



\### Pull Requests



Raw pull-request observations will be stored in:



`data/raw/repository\_pull\_requests.csv`



Planned fields:



\- repository ID

\- pull-request number

\- creation timestamp

\- closing timestamp

\- merge timestamp

\- state

\- author



Potential derived variables:



\- pull requests created during observation window

\- closed pull requests

\- merged pull requests

\- pull-request merge rate

\- pull-request lifecycle time

\- monthly pull-request activity



\### Releases



Raw release observations will be stored in:



`data/raw/repository\_releases.csv`



Planned fields:



\- repository ID

\- release ID

\- tag name

\- creation timestamp

\- publication timestamp

\- prerelease indicator

\- draft indicator



Potential derived variables:



\- release count

\- release frequency

\- monthly release activity



\## Longitudinal Activity



Historical activity will be represented using dated commit, issue,

pull-request, and release observations.



These observations can be aggregated into a monthly repository activity

dataset:



`data/processed/repository\_monthly\_activity.csv`



This enables analysis of:



\- activity trends

\- rolling activity

\- growth and decline

\- activity volatility

\- monthly comparisons

\- temporal differences across repositories and languages



Current metadata timestamps such as `updated\_at` and `pushed\_at` will not

be treated as substitutes for a historical time series.



\## Collaboration Network



Contributor observations will be used to construct a

repository-contributor bipartite representation.



A contributor projection can subsequently be constructed in which two

contributors are connected when they contribute to the same repository.



Potential network measures include:



\- degree

\- weighted degree

\- centrality

\- network density

\- community structure



Network measures will only be included when they provide meaningful

analytical information.



\## Feature Dataset



After preprocessing and feature engineering, repository-level analytical

variables will be consolidated into:



`data/processed/repository\_features.csv`



Potential feature groups include:



\### Popularity



\- stars

\- forks



\### Activity



\- commit count

\- commit rate

\- active contributors/committers

\- pull-request activity



\### Maintenance



\- days since last push

\- issue resolution rate

\- issue resolution time

\- release frequency



\### Community



\- contributor count

\- contributor concentration

\- fork-to-star relationship



\### Repository Scale



\- repository age

\- repository size



The final feature set will be determined after data-quality assessment,

descriptive analysis, correlation analysis, and feature-selection review.



\## Health Score



The repository health score will not be defined using arbitrary weights

before examining the collected data.



The health framework will be established after preprocessing and exploratory

analysis.



Potential dimensions include:



\- activity

\- maintenance

\- community

\- popularity

\- collaboration



Popularity will be treated as one dimension rather than as the definition

of repository health.



Normalization, weighting, and feature inclusion will be documented and

justified in the final methodology.



\## API Efficiency and Reproducibility



API collection will use authenticated requests, pagination, explicit

observation windows, request logging, and rate-limit monitoring.



The collection process will avoid unnecessary requests and will stop safely

when rate-limit constraints require waiting.



Raw API datasets will remain separate from processed analytical datasets.

This preserves data lineage from:



Raw API Data

→ Data Quality

→ Preprocessing

→ Feature Engineering

→ Analysis

→ Repository Intelligence.



Generated raw datasets are excluded from Git version control; the

collection scripts and methodology are version-controlled for

reproducibility.

