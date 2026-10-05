# ================================================================

# OpenSourcePulse

# BACSE301 - Exploratory Data Analysis

# GitHub Repository Intelligence System

# ================================================================



from pathlib import Path

import sys

import time

import math

import networkx as nx

import numpy as np

import pandas as pd

import plotly.express as px

import plotly.graph_objects as go

import streamlit as st





# ================================================================

# PROJECT PATH

# ================================================================



ROOT = Path(__file__).resolve().parents[1]



if str(ROOT) not in sys.path:

    sys.path.insert(0, str(ROOT))





# ================================================================

# LIVE ANALYZER

# ================================================================



from src.product.repository_analyzer import analyze_repository





# ================================================================

# STREAMLIT CONFIG

# ================================================================



st.set_page_config(

    page_title="OpenSourcePulse",

    page_icon="◉",

    layout="wide",

    initial_sidebar_state="collapsed",

)





# ================================================================

# PATHS

# ================================================================



RAW_DIR = ROOT / "data" / "raw"

PROCESSED_DIR = ROOT / "data" / "processed"

REPORT_DIR = ROOT / "reports"



REPOSITORIES_FILE = RAW_DIR / "repositories.csv"

FEATURES_FILE = PROCESSED_DIR / "repository_features_clean.csv"

MONTHLY_FILE = PROCESSED_DIR / "repository_monthly_activity.csv"

CONTRIBUTORS_FILE = RAW_DIR / "repository_contributors.csv"



PCA_EV_FILE = REPORT_DIR / "pca_explained_variance.csv"

PCA_LOADINGS_FILE = REPORT_DIR / "pca_loadings.csv"
PCA_SCORES_FILE = REPORT_DIR / "pca_repository_scores.csv"
CORRELATIONS_FILE = REPORT_DIR / "research_question_correlations.csv"
KMEANS_EVAL_FILE = REPORT_DIR / "kmeans_evaluation.csv"
KMEANS_PROFILES_FILE = REPORT_DIR / "kmeans_cluster_profiles.csv"
KMEANS_REPOS_FILE = REPORT_DIR / "kmeans_repository_clusters.csv"





# ================================================================

# GLOBAL CSS

# ================================================================



st.markdown(

    """

    <style>



    /* ------------------------------------------------------------

       GLOBAL

    ------------------------------------------------------------ */



    html, body, [class*="css"] {

        font-family: Inter, Arial, sans-serif;

    }



    .stApp {

        background:

            radial-gradient(

                circle at 10% 0%,

                rgba(76, 110, 245, 0.12),

                transparent 28%

            ),

            radial-gradient(

                circle at 95% 5%,

                rgba(140, 70, 255, 0.10),

                transparent 28%

            ),

            #050711;

        color: #f4f7ff;

    }



    [data-testid="stHeader"] {

        background: rgba(5, 7, 17, 0.90);

    }



    .block-container {

        max-width: 1400px;

        padding-top: 2rem;

        padding-bottom: 4rem;

    }





    /* ------------------------------------------------------------

       HERO

    ------------------------------------------------------------ */



    .hero {

        padding: 52px 56px;

        border-radius: 28px;

        margin-bottom: 34px;



        border: 1px solid rgba(110, 135, 255, 0.35);



        background:

            radial-gradient(

                circle at 80% 20%,

                rgba(130, 85, 255, 0.22),

                transparent 32%

            ),

            linear-gradient(

                135deg,

                #16245a 0%,

                #101735 55%,

                #10142d 100%

            );



        box-shadow:

            0 30px 90px rgba(35, 55, 150, 0.20);

    }



    .hero-kicker {

        color: #9db7ff;

        font-size: 13px;

        font-weight: 800;

        letter-spacing: 3px;

        margin-bottom: 14px;

    }



    .hero-title {

        font-size: 52px;

        font-weight: 800;

        line-height: 1.05;

        color: #ffffff;

        margin-bottom: 18px;

    }



    .hero-description {

        max-width: 850px;

        color: #b9c5e6;

        font-size: 17px;

        line-height: 1.75;

        margin-bottom: 28px;

    }



    .hero-pills {

        display: flex;

        flex-wrap: wrap;

        gap: 10px;

    }



    .hero-pill {

        display: inline-block;

        padding: 9px 14px;

        border-radius: 999px;



        color: #d9e2ff;

        background: rgba(255,255,255,0.06);

        border: 1px solid rgba(255,255,255,0.10);



        font-size: 12px;

        font-weight: 600;

    }





    /* ------------------------------------------------------------

       NAVIGATION

    ------------------------------------------------------------ */



    .nav-line {

        display: flex;

        gap: 28px;

        padding: 10px 0 14px;

        margin-bottom: 32px;



        border-bottom: 1px solid rgba(255,255,255,0.10);



        color: #9aa8cc;

        font-size: 13px;

        font-weight: 700;

    }



    .nav-active {

        color: #ff5570;

    }





    /* ------------------------------------------------------------

       SECTION TITLES

    ------------------------------------------------------------ */



    .eyebrow {

        color: #83a4ff;

        font-size: 11px;

        font-weight: 800;

        letter-spacing: 3px;

        margin-bottom: 8px;

    }



    .section-title {

        font-size: 29px;

        font-weight: 800;

        color: #ffffff;

        margin-bottom: 6px;

    }



    .section-subtitle {

        color: #8494bd;

        font-size: 14px;

        line-height: 1.6;

        margin-bottom: 24px;

    }





    /* ------------------------------------------------------------

       METRIC CARDS

    ------------------------------------------------------------ */



    .metric-card {

        min-height: 145px;

        padding: 22px;



        border-radius: 20px;



        background:

            linear-gradient(

                145deg,

                rgba(20,28,50,0.95),

                rgba(10,14,27,0.95)

            );



        border: 1px solid rgba(115,135,190,0.18);



        box-shadow:

            0 15px 40px rgba(0,0,0,0.18);

    }



    .metric-label {

        color: #87a2e8;

        font-size: 11px;

        font-weight: 800;

        letter-spacing: 1.5px;

        margin-bottom: 13px;

    }



    .metric-value {

        color: #ffffff;

        font-size: 30px;

        font-weight: 800;

        line-height: 1.1;

    }



    .metric-note {

        color: #7182aa;

        font-size: 12px;

        margin-top: 10px;

        line-height: 1.4;

    }





    /* ------------------------------------------------------------

       HEALTH CARD

    ------------------------------------------------------------ */



    .health-card {

        padding: 32px;



        border-radius: 24px;



        background:

            radial-gradient(

                circle at 85% 10%,

                rgba(120, 80, 255, 0.16),

                transparent 30%

            ),

            linear-gradient(

                135deg,

                #121b3a,

                #0c1021

            );



        border: 1px solid rgba(111,137,255,0.25);

    }



    .health-score {

        font-size: 70px;

        font-weight: 800;

        line-height: 1;

        color: #ffffff;

    }



    .health-profile {

        display: inline-block;



        margin-top: 10px;

        padding: 7px 14px;



        border-radius: 999px;



        background: rgba(108, 91, 255, 0.18);

        border: 1px solid rgba(108, 91, 255, 0.35);



        color: #c9c1ff;

        font-weight: 700;

        font-size: 13px;

    }





    /* ------------------------------------------------------------

       INFO BOX

    ------------------------------------------------------------ */



    .info-box {

        padding: 24px;



        border-radius: 18px;



        background: rgba(15, 25, 48, 0.72);



        border: 1px solid rgba(100,125,190,0.18);



        color: #aab8d8;



        line-height: 1.7;

        font-size: 14px;

    }



    .info-title {

        color: #ffffff;

        font-size: 18px;

        font-weight: 800;

        margin-bottom: 10px;

    }





    /* ------------------------------------------------------------

       LIVE STATUS

    ------------------------------------------------------------ */



    .live-status {

        padding: 12px 16px;

        margin: 15px 0;



        border-radius: 12px;



        background: rgba(50, 200, 130, 0.08);

        border: 1px solid rgba(50, 200, 130, 0.20);



        color: #7de4b2;

        font-size: 13px;

        font-weight: 600;

    }





    /* ------------------------------------------------------------

       FOOTER

    ------------------------------------------------------------ */



    .footer {

        margin-top: 70px;

        padding-top: 25px;



        border-top: 1px solid rgba(255,255,255,0.08);



        color: #596789;

        text-align: center;



        font-size: 12px;

    }





    /* ------------------------------------------------------------

       STREAMLIT BUTTONS

    ------------------------------------------------------------ */



    .stButton > button {

        border: none;

        border-radius: 13px;



        padding: 0.72rem 1.5rem;



        font-weight: 800;



        background:

            linear-gradient(

                135deg,

                #566cff,

                #984bff

            );



        color: white;



        box-shadow:

            0 12px 30px rgba(92, 75, 255, 0.25);

    }



    .stButton > button:hover {

        border: none;

        color: white;



        background:

            linear-gradient(

                135deg,

                #667bff,

                #a75cff

            );

    }





    /* ------------------------------------------------------------

       INPUT

    ------------------------------------------------------------ */



    div[data-baseweb="input"] {

        background: #0c1020;

        border-radius: 13px;

    }



    div[data-baseweb="input"] input {

        color: #ffffff;

    }





    /* ------------------------------------------------------------

       DATAFRAME

    ------------------------------------------------------------ */



    [data-testid="stDataFrame"] {

        border-radius: 14px;

        overflow: hidden;

    }



    </style>

    """,

    unsafe_allow_html=True,

)





# ================================================================

# HELPERS

# ================================================================



def safe_float(value, default=0.0):

    try:

        value = float(value)



        if math.isnan(value) or math.isinf(value):

            return default



        return value



    except (TypeError, ValueError):

        return default





def safe_int(value, default=0):

    try:

        return int(round(safe_float(value, default)))

    except Exception:

        return default





def fmt_int(value):

    return f"{safe_int(value):,}"





def fmt_float(value, digits=1):

    return f"{safe_float(value):,.{digits}f}"





def render_html(html: str):

    """Render raw HTML directly in Streamlit."""

    import textwrap

    cleaned_html = textwrap.dedent(html).strip()

    st.html(cleaned_html)





@st.cache_data

def load_csv(path_string):

    path = Path(path_string)



    if not path.exists():

        return pd.DataFrame()



    try:

        return pd.read_csv(path)

    except Exception:

        return pd.DataFrame()





def section(title, subtitle="", eyebrow="OPENSOURCEPULSE INTELLIGENCE"):

    render_html(

        f"""

        <div class="eyebrow">{eyebrow}</div>

        <div class="section-title">{title}</div>

        <div class="section-subtitle">{subtitle}</div>

        """

    )





def metric_card(label, value, note=""):

    render_html(

        f"""

        <div class="metric-card">

            <div class="metric-label">{label}</div>

            <div class="metric-value">{value}</div>

            <div class="metric-note">{note}</div>

        </div>

        """

    )





def clean_language(series):

    if series is None:

        return pd.Series(dtype="object")



    s = series.fillna("Unknown").astype(str).str.strip()



    s = s.replace(

        {

            "nan": "Unknown",

            "None": "Unknown",

            "": "Unknown",

            "Vim script": "Vim Script",

        }

    )



    return s





def find_column(df, candidates):

    for candidate in candidates:

        if candidate in df.columns:

            return candidate



    return None





# ================================================================

# HERO

# ================================================================



render_html(

    """

    <div class="hero">



        <div class="hero-kicker">

            BACSE301 · EXPLORATORY DATA ANALYSIS

        </div>



        <div class="hero-title">

            OpenSourcePulse

        </div>



        <div class="hero-description">

            GitHub Repository Intelligence System.

            Go beyond stars with evidence-based analysis of

            activity, maintenance, community participation,

            contribution structure and repository profiles.

        </div>



        <div class="hero-pills">



            <div class="hero-pill">

                300-Repository EDA Reference

            </div>



            <div class="hero-pill">

                Live GitHub Analysis

            </div>



            <div class="hero-pill">

                PCA + K-Means

            </div>



            <div class="hero-pill">

                Time-Series Intelligence

            </div>



            <div class="hero-pill">

                Contributor Network

            </div>



        </div>



    </div>

    """

)





# ================================================================

# NAVIGATION

# ================================================================



tabs = st.tabs(

    [

        "◉  Live Overview",

        "◇  EDA Explorer",

        "◌  Activity Intelligence",

        "◎  Multivariate Intelligence",

        "⌘  Network Analysis",

        "⌘  Methodology",

    ]

)





# ================================================================

# DATA LOADING

# ================================================================



repos = load_csv(str(REPOSITORIES_FILE))

features = load_csv(str(FEATURES_FILE))

monthly = load_csv(str(MONTHLY_FILE))

contributors = load_csv(str(CONTRIBUTORS_FILE))

pca_ev = load_csv(str(PCA_EV_FILE))

pca_loadings = load_csv(str(PCA_LOADINGS_FILE))
pca_scores = load_csv(str(PCA_SCORES_FILE))
research_correlations = load_csv(str(CORRELATIONS_FILE))
kmeans_eval = load_csv(str(KMEANS_EVAL_FILE))
kmeans_profiles = load_csv(str(KMEANS_PROFILES_FILE))
kmeans_repos = load_csv(str(KMEANS_REPOS_FILE))





# ================================================================

# TAB 1 — LIVE OVERVIEW

# ================================================================



with tabs[0]:



    section(

        "Analyze a GitHub Repository",

        "Enter any public GitHub repository to generate a live analytical profile against the OpenSourcePulse reference layer.",

    )



    col_input, col_button = st.columns([5, 1])



    with col_input:

        repo_url = st.text_input(

            "GitHub Repository URL",

            value="https://github.com/microsoft/vscode",

            placeholder="https://github.com/owner/repository",

            label_visibility="collapsed",

        )



    with col_button:

        analyze_clicked = st.button(

            "Analyze Repository",

            use_container_width=True,

        )





    # ------------------------------------------------------------

    # SESSION STATE

    # ------------------------------------------------------------



    if "analysis_result" not in st.session_state:

        st.session_state.analysis_result = None



    if "analysis_error" not in st.session_state:

        st.session_state.analysis_error = None





    # ------------------------------------------------------------

    # ANALYZE

    # ------------------------------------------------------------



    if analyze_clicked:



        if not repo_url.strip():



            st.session_state.analysis_result = None

            st.session_state.analysis_error = "Please enter a GitHub repository URL."



        else:



            st.session_state.analysis_error = None



            progress = st.empty()



            progress.markdown(

                """

                <div class="live-status">

                    ◉ Collecting live GitHub metadata, recent commits and contributor information...

                </div>

                """,

                unsafe_allow_html=True,

            )



            try:



                start_time = time.time()



                
                result = analyze_repository(repo_url.strip())



                elapsed = time.time() - start_time



                st.session_state.analysis_result = result



                progress.markdown(

                    f"""

                    <div class="live-status">

                        ✓ Live analysis completed in {elapsed:.1f} seconds.

                    </div>

                    """,

                    unsafe_allow_html=True,

                )



            except Exception as exc:



                st.session_state.analysis_result = None



                st.session_state.analysis_error = str(exc)



                progress.empty()





    # ------------------------------------------------------------

    # ERROR

    # ------------------------------------------------------------



    if st.session_state.analysis_error:



        st.error(

            st.session_state.analysis_error

        )





    # ------------------------------------------------------------

    # LIVE RESULT

    # ------------------------------------------------------------



    live = st.session_state.analysis_result



    if live:



        # The analyzer may return nested structures.

        # We keep this robust.



        repo = live.get("repository", live.get("repo", {}))

        features_live = live.get(

            "features",

            live.get("repository_features", {}),

        )



        health = live.get(

            "health",

            live.get("health_index", {}),

        )



        dimensions = live.get(

            "dimensions",

            health.get("dimensions", {}),

        )



        coverage = live.get(

            "coverage",

            health.get("coverage", None),

        )





        # --------------------------------------------------------

        # REPOSITORY HEADER

        # --------------------------------------------------------



        full_name = (

            repo.get("full_name")

            or repo.get("name")

            or live.get("full_name")

            or "GitHub Repository"

        )



        description = (

            repo.get("description")

            or live.get("description")

            or "No repository description available."

        )



        html_url = (

            repo.get("html_url")

            or live.get("html_url")

            or repo_url

        )



        render_html(

            f"""

            <div style="

                padding: 25px;

                border-radius: 20px;

                background: rgba(12,18,36,0.72);

                border: 1px solid rgba(110,135,210,0.18);

                margin-top: 18px;

                margin-bottom: 30px;

            ">



                <div style="

                    color:#ffffff;

                    font-size:30px;

                    font-weight:800;

                    margin-bottom:8px;

                ">

                    {full_name}

                </div>



                <div style="

                    color:#8fa1c9;

                    font-size:14px;

                    margin-bottom:18px;

                ">

                    {description}

                </div>



                <a

                    href="{html_url}"

                    target="_blank"

                    style="

                        display:inline-block;

                        padding:10px 15px;

                        border-radius:10px;

                        background:#111a35;

                        border:1px solid #34426e;

                        color:#d9e2ff;

                        text-decoration:none;

                        font-size:13px;

                        font-weight:700;

                    "

                >

                    View repository on GitHub ↗

                </a>



            </div>

            """

        )





        # --------------------------------------------------------

        # REPOSITORY SNAPSHOT

        # --------------------------------------------------------



        section(

            "Repository Snapshot",

            "Current GitHub metadata and rolling 365-day activity measurements.",

        )



        stars = (

            repo.get("stargazers_count")

            or repo.get("stars")

            or live.get("stars")

            or features_live.get("stars")

        )



        forks = (

            repo.get("forks_count")

            or repo.get("forks")

            or live.get("forks")

            or features_live.get("forks")

        )



        commits = (

            features_live.get("commits_365d")

            or live.get("commits_365d")

            or 0

        )



        active_months = (

            features_live.get("active_months")

            or live.get("active_months")

            or 0

        )



        contributor_count = (

            features_live.get("contributors_count")

            or live.get("contributors_count")

            or repo.get("contributors_count")

            or 0

        )



        language = (

            repo.get("language")

            or live.get("language")

            or features_live.get("language")

            or "Unknown"

        )



        c1, c2, c3 = st.columns(3)

        c4, c5, c6 = st.columns(3)



        with c1:

            metric_card(

                "STARS",

                fmt_int(stars),

                "GitHub visibility",

            )



        with c2:

            metric_card(

                "FORKS",

                fmt_int(forks),

                "Adoption / reuse",

            )



        with c3:

            metric_card(

                "COMMITS · 365D",

                fmt_int(commits),

                "Recent development",

            )



        with c4:

            metric_card(

                "ACTIVE MONTHS",

                fmt_int(active_months),

                "Calendar months with observed commits",

            )



        with c5:

            metric_card(

                "CONTRIBUTORS",

                fmt_int(contributor_count),

                "Participation breadth",

            )



        with c6:

            metric_card(

                "LANGUAGE",

                str(language),

                "Primary GitHub language",

            )





        # --------------------------------------------------------

        # HEALTH INDEX

        # --------------------------------------------------------



        st.markdown("<br>", unsafe_allow_html=True)



        section(

            "Repository Health Intelligence",

            "An interpretable multidimensional index comparing the live repository with the 300-repository reference sample.",

        )



        health_score = (

            health.get("score")

            or health.get("health_score")

            or live.get("health_score")

            or live.get("score")

            or 0

        )



        health_profile = (

            health.get("profile")

            or health.get("health_profile")

            or live.get("health_profile")

            or "Not available"

        )



        coverage_value = safe_float(

            coverage,

            default=100.0,

        )



        left, right = st.columns([1.15, 1.85])



        with left:



            render_html(

                f"""

                <div class="health-card">



                    <div class="metric-label">

                        REPOSITORY HEALTH INDEX

                    </div>



                    <div class="health-score">

                        {safe_float(health_score):.2f}

                    </div>



                    <div class="health-profile">

                        {health_profile}

                    </div>



                    <div style="

                        margin-top:18px;

                        color:#8393b8;

                        font-size:13px;

                        line-height:1.6;

                    ">

                        Reference-normalized analytical score.

                        It is not an objective software-quality

                        measurement.

                    </div>



                    <div style="

                        margin-top:15px;

                        color:#6f82ae;

                        font-size:12px;

                    ">

                        Measurement coverage:

                        {coverage_value:.0f}%

                    </div>



                </div>

                """

            )



        with right:



            dimension_values = {}



            if isinstance(dimensions, dict):



                for key, value in dimensions.items():



                    if isinstance(value, dict):



                        dimension_values[key] = safe_float(

                            value.get("score", value.get("value", 0))

                        )



                    else:



                        dimension_values[key] = safe_float(value)





            if not dimension_values:



                dimension_values = {

                    "Popularity": safe_float(

                        health.get("popularity", 0)

                    ),

                    "Activity": safe_float(

                        health.get("activity", 0)

                    ),

                    "Maintenance": safe_float(

                        health.get("maintenance", 0)

                    ),

                    "Community": safe_float(

                        health.get("community", 0)

                    ),

                    "Distribution": safe_float(

                        health.get("distribution", 0)

                    ),

                }



            dimension_df = pd.DataFrame(

                {

                    "Dimension": list(dimension_values.keys()),

                    "Score": list(dimension_values.values()),

                }

            )



            if not dimension_df.empty:



                fig = px.bar(

                    dimension_df,

                    x="Score",

                    y="Dimension",

                    orientation="h",

                    range_x=[0, 100],

                    text="Score",

                )



                fig.update_traces(

                    texttemplate="%{text:.1f}",

                    textposition="outside",

                )



                fig.update_layout(

                    height=330,

                    margin=dict(

                        l=10,

                        r=40,

                        t=30,

                        b=10,

                    ),

                    paper_bgcolor="rgba(0,0,0,0)",

                    plot_bgcolor="rgba(0,0,0,0)",

                    font=dict(

                        color="#cbd5f0"

                    ),

                    xaxis=dict(

                        gridcolor="rgba(255,255,255,0.08)",

                        zeroline=False,

                    ),

                    yaxis=dict(

                        gridcolor="rgba(0,0,0,0)"

                    ),

                )



                st.plotly_chart(

                    fig,

                    use_container_width=True,

                    config={"displayModeBar": False},

                )





        # --------------------------------------------------------

        # LIVE INSIGHTS

        # --------------------------------------------------------



        st.markdown("<br>", unsafe_allow_html=True)



        section(

            "Live Analytical Signals",

            "The live application translates raw GitHub measurements into interpretable repository characteristics.",

        )



        a1, a2, a3 = st.columns(3)



        with a1:



            render_html(

                f"""

                <div class="info-box">



                    <div class="info-title">

                        Activity

                    </div>



                    <div>

                        <b>{fmt_int(commits)}</b>

                        commits were observed in the rolling

                        365-day collection window across

                        <b>{fmt_int(active_months)}</b>

                        calendar months.

                    </div>



                </div>

                """

            )



        with a2:



            render_html(

                f"""

                <div class="info-box">



                    <div class="info-title">

                        Community

                    </div>



                    <div>

                        The live repository has approximately

                        <b>{fmt_int(contributor_count)}</b>

                        observed contributors in the collected

                        contributor data.

                    </div>



                </div>

                """

            )



        with a3:



            top_share = features_live.get(

                "top_contributor_share",

                live.get("top_contributor_share", None),

            )



            render_html(

                f"""

                <div class="info-box">



                    <div class="info-title">

                        Contribution Structure

                    </div>



                    <div>

                        Top-contributor share:

                        <b>

                            {

                                "N/A"

                                if top_share is None

                                else f"{safe_float(top_share) * 100:.1f}%"

                            }

                        </b>

                    </div>



                </div>

                """

            )





    else:



        render_html(

            """

            <div class="info-box" style="margin-top:25px;">



                <div class="info-title">

                    Start with a repository.

                </div>



                <div>

                    Enter a public GitHub URL above and click

                    <b>Analyze Repository</b>.

                    <br><br>

                    OpenSourcePulse will collect live metadata,

                    recent commit activity and contributor

                    information, then compare the repository

                    against the 300-repository EDA reference

                    sample.

                </div>



            </div>

            """

        )





# ================================================================

# TAB 2 — EDA EXPLORER

# ================================================================



with tabs[1]:



    section(

        "Reference EDA Layer",

        "The 300-repository star-stratified sample is the analytical reference layer used throughout OpenSourcePulse.",

    )



    if repos.empty:



        st.warning(

            "repositories.csv was not found."

        )



    else:



        # --------------------------------------------------------

        # DATA QUALITY

        # --------------------------------------------------------



        row_count = len(repos)

        column_count = len(

            features.columns

            if not features.empty

            else repos.columns

        )



        duplicate_count = 0



        if "repo_id" in repos.columns:

            duplicate_count = int(

                repos["repo_id"].duplicated().sum()

            )



        missing_cells = int(

            repos.isna().sum().sum()

        )



        q1, q2, q3, q4 = st.columns(4)



        with q1:

            metric_card(

                "REFERENCE REPOSITORIES",

                fmt_int(row_count),

                "Star-stratified sample",

            )



        with q2:

            metric_card(

                "VARIABLES",

                fmt_int(column_count),

                "Available analytical features",

            )



        with q3:

            metric_card(

                "DUPLICATE ROWS",

                fmt_int(duplicate_count),

                "Data-quality check",

            )



        with q4:

            metric_card(

                "MISSING CELLS",

                fmt_int(missing_cells),

                "Reference dataset",

            )





        # --------------------------------------------------------

        # LANGUAGE DISTRIBUTION

        # --------------------------------------------------------



        st.markdown("<br>", unsafe_allow_html=True)



        section(

            "Programming Language Distribution",

            "Language composition of the reference repository sample.",

        )



        language_column = find_column(

            repos,

            [

                "language",

                "Language",

            ],

        )



        if language_column:



            lang = clean_language(

                repos[language_column]

            )



            lang_counts = (

                lang.value_counts()

                .head(12)

                .reset_index()

            )



            lang_counts.columns = [

                "Language",

                "Repositories",

            ]



            fig = px.bar(

                lang_counts,

                x="Repositories",

                y="Language",

                orientation="h",

                text="Repositories",

            )



            fig.update_layout(

                height=470,

                margin=dict(

                    l=10,

                    r=20,

                    t=20,

                    b=20,

                ),

                paper_bgcolor="rgba(0,0,0,0)",

                plot_bgcolor="rgba(0,0,0,0)",

                font=dict(color="#cbd5f0"),

                xaxis=dict(

                    gridcolor="rgba(255,255,255,0.08)"

                ),

                yaxis=dict(

                    categoryorder="total ascending"

                ),

            )



            fig.update_traces(

                textposition="outside"

            )



            st.plotly_chart(

                fig,

                use_container_width=True,

                config={"displayModeBar": False},

            )





        # --------------------------------------------------------

        # POPULARITY DISTRIBUTION

        # --------------------------------------------------------



        st.markdown("<br>", unsafe_allow_html=True)



        section(

            "Repository Popularity",

            "Raw star counts are highly right-skewed, motivating logarithmic transformation during analysis.",

        )



        stars_column = find_column(

            repos,

            [

                "stars",

                "stargazers_count",

            ],

        )



        if stars_column:



            star_values = pd.to_numeric(

                repos[stars_column],

                errors="coerce",

            ).dropna()



            fig = px.histogram(

                x=star_values,

                nbins=35,

                labels={

                    "x": "Stars",

                    "y": "Repositories",

                },

            )



            fig.update_layout(

                height=400,

                paper_bgcolor="rgba(0,0,0,0)",

                plot_bgcolor="rgba(0,0,0,0)",

                font=dict(color="#cbd5f0"),

                xaxis=dict(

                    gridcolor="rgba(255,255,255,0.08)"

                ),

                yaxis=dict(

                    gridcolor="rgba(255,255,255,0.08)"

                ),

            )



            st.plotly_chart(

                fig,

                use_container_width=True,

                config={"displayModeBar": False},

            )





        # --------------------------------------------------------

        # BASIC STATISTICS

        # --------------------------------------------------------



        st.markdown("<br>", unsafe_allow_html=True)



        section(

            "Descriptive Statistics",

            "Summary statistics for major numerical repository variables.",

        )



        numeric_candidates = [

            "stars",

            "forks",

            "open_issues",

            "size_kb",

        ]



        available_numeric = [

            c for c in numeric_candidates

            if c in repos.columns

        ]



        if available_numeric:



            desc = (

                repos[available_numeric]

                .apply(pd.to_numeric, errors="coerce")

                .describe()

                .T

                .round(2)

            )



            st.dataframe(

                desc,

                use_container_width=True,

            )





# ================================================================


    # --------------------------------------------------------
    # MISSING-VALUE INTELLIGENCE
    # --------------------------------------------------------

    st.markdown("<br>", unsafe_allow_html=True)

    section(
        "Missing-Value Intelligence",
        "Missingness is quantified before preprocessing so that data-quality decisions remain transparent.",
    )

    missing_summary = (
        repos.isna()
        .sum()
        .reset_index()
    )
    missing_summary.columns = ["Variable", "Missing"]

    missing_summary["Missing"] = pd.to_numeric(
        missing_summary["Missing"],
        errors="coerce",
    ).fillna(0)

    missing_summary["Percentage"] = (
        missing_summary["Missing"] / max(len(repos), 1) * 100
    )

    missing_summary = (
        missing_summary[missing_summary["Missing"] > 0]
        .sort_values("Missing", ascending=False)
        .reset_index(drop=True)
    )

    if missing_summary.empty:

        render_html(
            """
            <div class="info-box">
                <div class="info-title">Complete observed fields</div>
                No missing cells were detected in the repository metadata.
            </div>
            """
        )

    else:

        m1, m2 = st.columns([1.15, 1.85])

        with m1:

            metric_card(
                "FIELDS WITH MISSINGNESS",
                fmt_int(len(missing_summary)),
                "Repository metadata",
            )

        with m2:

            metric_card(
                "TOTAL MISSING CELLS",
                fmt_int(int(missing_summary["Missing"].sum())),
                "Before preprocessing",
            )

        fig = px.bar(
            missing_summary,
            x="Missing",
            y="Variable",
            orientation="h",
            text="Missing",
        )

        fig.update_traces(
            textposition="outside",
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Missing: %{x}<br>"
                "Share: %{customdata:.1f}%<extra></extra>"
            ),
            customdata=missing_summary["Percentage"],
        )

        fig.update_layout(
            height=390,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cbd5f0"),
            xaxis=dict(
                title="Missing cells",
                gridcolor="rgba(255,255,255,0.08)",
            ),
            yaxis=dict(
                categoryorder="total ascending",
            ),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

        display_missing = missing_summary.copy()
        display_missing["Missing %"] = display_missing["Percentage"].round(1)
        display_missing = display_missing[["Variable", "Missing", "Missing %"]]

        st.dataframe(
            display_missing,
            use_container_width=True,
            hide_index=True,
        )


# TAB 3 — ACTIVITY INTELLIGENCE

# ================================================================



with tabs[2]:



    section(

        "Time-Series Intelligence",

        "Monthly commit activity built from genuine commit timestamps in the rolling observation window.",

    )



    if monthly.empty:



        st.warning(

            "repository_monthly_activity.csv was not found."

        )



    else:



        month_col = find_column(

            monthly,

            [

                "month",

                "Month",

            ],

        )



        commit_col = find_column(

            monthly,

            [

                "commits_count",

                "commit_count",

                "commits",

            ],

        )



        repo_col = find_column(

            monthly,

            [

                "repo_name",

                "full_name",

                "repository",

            ],

        )





        if month_col and commit_col:



            ts = monthly.copy()



            ts[month_col] = pd.to_datetime(

                ts[month_col],

                errors="coerce",

            )



            ts[commit_col] = pd.to_numeric(

                ts[commit_col],

                errors="coerce",

            )



            overall = (

                ts.dropna(subset=[month_col])

                .groupby(month_col)[commit_col]

                .sum()

                .reset_index()

                .sort_values(month_col)

            )



            fig = px.line(

                overall,

                x=month_col,

                y=commit_col,

                markers=True,

            )



            fig.update_layout(

                height=500,

                paper_bgcolor="rgba(0,0,0,0)",

                plot_bgcolor="rgba(0,0,0,0)",

                font=dict(color="#cbd5f0"),

                xaxis=dict(

                    title="Month",

                    gridcolor="rgba(255,255,255,0.08)",

                ),

                yaxis=dict(

                    title="Commits",

                    gridcolor="rgba(255,255,255,0.08)",

                ),

                hovermode="x unified",

            )



            st.plotly_chart(

                fig,

                use_container_width=True,

                config={"displayModeBar": False},

            )





        # --------------------------------------------------------

        # MONTHLY SUMMARY

        # --------------------------------------------------------



        if month_col and commit_col:



            total_commits = int(

                overall[commit_col].sum()

            )



            peak_idx = overall[commit_col].idxmax()



            peak_month = overall.loc[

                peak_idx,

                month_col,

            ]



            peak_commits = int(

                overall.loc[

                    peak_idx,

                    commit_col,

                ]

            )



            s1, s2, s3 = st.columns(3)



            with s1:

                metric_card(

                    "TOTAL OBSERVED COMMITS",

                    fmt_int(total_commits),

                    "Reference sample",

                )



            with s2:

                metric_card(

                    "PEAK MONTH",

                    peak_month.strftime("%b %Y"),

                    "Highest aggregate activity",

                )



            with s3:

                metric_card(

                    "PEAK COMMITS",

                    fmt_int(peak_commits),

                    "Aggregate monthly peak",

                )





        # --------------------------------------------------------

        # TOP ACTIVE REPOSITORIES

        # --------------------------------------------------------



        if repo_col and commit_col:



            section(

                "Most Active Repositories",

                "Repositories with the highest observed commit volume in the collected activity dataset.",

            )



            top_repos = (

                monthly.groupby(repo_col)[commit_col]

                .sum()

                .sort_values(ascending=False)

                .head(15)

                .reset_index()

            )



            top_repos.columns = [

                "Repository",

                "Commits",

            ]



            fig = px.bar(

                top_repos,

                x="Commits",

                y="Repository",

                orientation="h",

            )



            fig.update_layout(

                height=520,

                margin=dict(

                    l=10,

                    r=20,

                    t=20,

                    b=20,

                ),

                paper_bgcolor="rgba(0,0,0,0)",

                plot_bgcolor="rgba(0,0,0,0)",

                font=dict(color="#cbd5f0"),

                xaxis=dict(

                    gridcolor="rgba(255,255,255,0.08)"

                ),

                yaxis=dict(

                    categoryorder="total ascending"

                ),

            )



            st.plotly_chart(

                fig,

                use_container_width=True,

                config={"displayModeBar": False},

            )





# ================================================================

# ================================================================
# TAB 4 — MULTIVARIATE INTELLIGENCE
# ================================================================

with tabs[3]:

    section(
        "Multivariate Intelligence",
        "Correlation, PCA and clustering reveal repository structure beyond individual variables.",
    )

    # ------------------------------------------------------------
    # OVERVIEW
    # ------------------------------------------------------------

    pc1_pct = 0.0
    pc2_pct = 0.0
    pcs_for_90 = "—"

    if not pca_ev.empty:

        ev0 = pca_ev.copy()

        vcol = find_column(
            ev0,
            [
                "explained_variance_ratio",
                "Explained Variance Ratio",
                "variance_ratio",
                "explained_variance",
                "Explained Variance",
            ],
        )

        ccol = find_column(
            ev0,
            [
                "cumulative_variance",
                "Cumulative Variance",
                "cumulative_explained_variance",
                "cumulative_explained_variance_ratio",
                "cumulative_ratio",
            ],
        )

        if vcol:

            ev0[vcol] = pd.to_numeric(
                ev0[vcol],
                errors="coerce",
            )

            vals = ev0[vcol].dropna().reset_index(drop=True)

            if len(vals) >= 1:
                pc1_pct = safe_float(vals.iloc[0]) * 100

            if len(vals) >= 2:
                pc2_pct = safe_float(vals.iloc[1]) * 100

            # ----------------------------------------------------
            # Calculate cumulative variance directly from the
            # explained-variance ratios when necessary.
            # This makes the dashboard independent of the exact
            # cumulative-column name in the CSV.
            # ----------------------------------------------------

            if ccol:

                ev0[ccol] = pd.to_numeric(
                    ev0[ccol],
                    errors="coerce",
                )

                cumulative_values = (
                    ev0[ccol]
                    .dropna()
                    .reset_index(drop=True)
                )

                hits = np.where(
                    cumulative_values.values >= 0.90
                )[0]

            else:

                cumulative_values = vals.cumsum()

                hits = np.where(
                    cumulative_values.values >= 0.90
                )[0]

            if len(hits):

                pcs_for_90 = str(
                    int(hits[0] + 1)
                )

    a1, a2, a3, a4 = st.columns(4)

    with a1:
        metric_card(
            "PCA OBSERVATIONS",
            fmt_int(len(pca_scores) if not pca_scores.empty else 298),
            "Complete analytical rows",
        )

    with a2:
        metric_card(
            "PC1 VARIANCE",
            f"{pc1_pct:.1f}%",
            "Largest information component",
        )

    with a3:
        metric_card(
            "PC2 VARIANCE",
            f"{pc2_pct:.1f}%",
            "Second information component",
        )

    with a4:
        metric_card(
            "90% RETENTION",
            f"{pcs_for_90} PCs",
            "Components needed for ≥90%",
        )

    render_html(
        """
        <div class="info-box">
            <div class="info-title">Why multivariate analysis?</div>
            Repository characteristics interact across popularity, activity,
            maintenance and community participation. OpenSourcePulse therefore
            combines correlation analysis, PCA and K-Means profiling to study
            the repository as a multidimensional system.
        </div>
        """
    )

    # ------------------------------------------------------------
    # CORRELATION HEATMAP
    # ------------------------------------------------------------

    section(
        "Correlation Intelligence",
        "Relationships among major analytical variables in the reference sample.",
    )

    corr_candidates = [
        "log1p_stars",
        "log1p_forks",
        "log1p_open_issues",
        "age_years",
        "days_since_push",
        "log1p_contributors",
        "log1p_commits_365d",
        "log1p_total_contributions",
    ]

    corr_cols = [c for c in corr_candidates if c in features.columns]

    if len(corr_cols) >= 3:

        corr = (
            features[corr_cols]
            .apply(pd.to_numeric, errors="coerce")
            .corr()
        )

        labels = {
            "log1p_stars": "Stars",
            "log1p_forks": "Forks",
            "log1p_open_issues": "Open Issues",
            "age_years": "Age",
            "days_since_push": "Days Since Push",
            "log1p_contributors": "Contributors",
            "log1p_commits_365d": "Commits · 365d",
            "log1p_total_contributions": "Contributions",
        }

        corr = corr.rename(index=labels, columns=labels)

        fig = go.Figure(
            data=go.Heatmap(
                z=corr.values,
                x=corr.columns,
                y=corr.index,
                zmin=-1,
                zmax=1,
                colorscale="RdBu",
                text=np.round(corr.values, 2),
                texttemplate="%{text}",
                colorbar=dict(title="r"),
                hovertemplate=(
                    "%{y} × %{x}<br>"
                    "Pearson r = %{z:.3f}<extra></extra>"
                ),
            )
        )

        fig.update_layout(
            height=600,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(color="#cbd5f0"),
            margin=dict(l=80, r=20, t=20, b=100),
        )

        st.plotly_chart(
            fig,
            use_container_width=True,
            config={"displayModeBar": False},
        )

    if not research_correlations.empty:

        rc = research_correlations.copy()

        rcol = find_column(
            rc,
            ["pearson_r", "correlation", "r", "spearman_r"],
        )

        pair_col = find_column(
            rc,
            ["relationship", "pair", "comparison", "question"],
        )

        if rcol and pair_col:

            rc[rcol] = pd.to_numeric(rc[rcol], errors="coerce")
            rc = rc.dropna(subset=[rcol]).head(6)

            if not rc.empty:

                display_rc = rc[[pair_col, rcol]].copy()
                display_rc.columns = ["Research Relationship", "Correlation"]
                display_rc["Correlation"] = display_rc["Correlation"].round(3)

                st.dataframe(
                    display_rc,
                    use_container_width=True,
                    hide_index=True,
                )

    render_html(
        """
        <div class="info-box">
            <div class="info-title">Statistical interpretation</div>
            Correlation measures association, not causation. Strong
            relationships reveal redundancy or shared structure, while
            weaker relationships can indicate dimensions carrying additional
            information.
        </div>
        """
    )

    # ------------------------------------------------------------
    # PCA EXPLAINED VARIANCE
    # ------------------------------------------------------------

    section(
        "PCA Explained Variance",
        "Principal components compress correlated repository measurements while retaining information.",
    )

    if pca_ev.empty:

        st.info("PCA explained-variance report is not available yet.")

    else:

        ev = pca_ev.copy()

        component_col = find_column(
            ev,
            ["component", "Component", "PC"],
        )
        variance_col = find_column(
            ev,
            ["explained_variance_ratio", "Explained Variance Ratio", "variance_ratio"],
        )
        cumulative_col = find_column(
            ev,
            ["cumulative_variance", "Cumulative Variance", "cumulative_explained_variance"],
        )

        if variance_col:

            ev[variance_col] = pd.to_numeric(
                ev[variance_col],
                errors="coerce",
            )

            if cumulative_col:
                ev[cumulative_col] = pd.to_numeric(
                    ev[cumulative_col],
                    errors="coerce",
                )

            x = (
                ev[component_col]
                if component_col
                else np.arange(1, len(ev) + 1)
            )

            fig = go.Figure()

            fig.add_trace(
                go.Bar(
                    x=x,
                    y=ev[variance_col] * 100,
                    name="Individual variance",
                )
            )

            if cumulative_col:

                fig.add_trace(
                    go.Scatter(
                        x=x,
                        y=ev[cumulative_col] * 100,
                        mode="lines+markers",
                        name="Cumulative variance",
                        yaxis="y2",
                    )
                )

                fig.update_layout(
                    yaxis2=dict(
                        title="Cumulative variance (%)",
                        overlaying="y",
                        side="right",
                        range=[0, 105],
                        gridcolor="rgba(0,0,0,0)",
                    )
                )

            fig.add_hline(
                y=90,
                line_dash="dash",
                annotation_text="90% retention target",
                annotation_position="top left",
            )

            fig.update_layout(
                height=500,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#cbd5f0"),
                xaxis=dict(
                    title="Principal Component",
                    gridcolor="rgba(255,255,255,0.08)",
                ),
                yaxis=dict(
                    title="Individual variance (%)",
                    gridcolor="rgba(255,255,255,0.08)",
                ),
                legend=dict(
                    orientation="h",
                    y=1.08,
                    x=0,
                ),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False},
            )

    # ------------------------------------------------------------
    # PCA LOADINGS
    # ------------------------------------------------------------

    section(
        "PCA Loading Structure",
        "Large absolute loadings indicate variables that contribute strongly to each component.",
    )

    if pca_loadings.empty:

        st.info("PCA loading report is not available yet.")

    else:

        loading_display = pca_loadings.copy()

        first_col = loading_display.columns[0]

        if str(first_col).lower().startswith("unnamed"):
            loading_display = loading_display.rename(
                columns={first_col: "Feature"}
            )

        st.dataframe(
            loading_display.head(20),
            use_container_width=True,
            hide_index=True,
        )

        feature_col = (
            "Feature"
            if "Feature" in loading_display.columns
            else loading_display.columns[0]
        )

        pcs = [
            c for c in loading_display.columns
            if str(c).upper() in {"PC1", "PC2"}
        ]

        if pcs:

            plot_parts = []

            for pc in pcs:

                temp = loading_display[
                    [feature_col, pc]
                ].copy()

                temp[pc] = pd.to_numeric(
                    temp[pc],
                    errors="coerce",
                )

                temp["Absolute Loading"] = temp[pc].abs()
                temp["Component"] = pc

                plot_parts.append(
                    temp.nlargest(8, "Absolute Loading")
                )

            load_plot = pd.concat(
                plot_parts,
                ignore_index=True,
            )

            fig = px.bar(
                load_plot.sort_values("Absolute Loading"),
                x="Absolute Loading",
                y=feature_col,
                color="Component",
                orientation="h",
                facet_row="Component" if len(pcs) > 1 else None,
            )

            fig.update_layout(
                height=520,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#cbd5f0"),
                showlegend=False,
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False},
            )

    # ------------------------------------------------------------
    # PCA REPOSITORY MAP
    # ------------------------------------------------------------

    section(
        "Repository Position in PCA Space",
        "Each point represents a repository positioned by its first two principal-component scores.",
    )

    if not pca_scores.empty:

        scores = pca_scores.copy()

        pc1_col = find_column(
            scores,
            ["PC1", "pc1", "principal_component_1"],
        )
        pc2_col = find_column(
            scores,
            ["PC2", "pc2", "principal_component_2"],
        )
        repo_col = find_column(
            scores,
            ["full_name", "repo_name", "repository", "name"],
        )

        if pc1_col and pc2_col:

            scores[pc1_col] = pd.to_numeric(
                scores[pc1_col],
                errors="coerce",
            )
            scores[pc2_col] = pd.to_numeric(
                scores[pc2_col],
                errors="coerce",
            )

            scores = scores.dropna(
                subset=[pc1_col, pc2_col]
            )

            # Join K-Means labels where a common repository identifier exists.
            cluster_col = find_column(
                scores,
                ["cluster", "Cluster", "kmeans_cluster"],
            )

            if cluster_col is None and not kmeans_repos.empty:

                merge_key = None

                for candidate in [
                    "repo_id",
                    "full_name",
                    "repo_name",
                    "repository",
                ]:

                    if (
                        candidate in scores.columns
                        and candidate in kmeans_repos.columns
                    ):
                        merge_key = candidate
                        break

                cluster_source = find_column(
                    kmeans_repos,
                    ["cluster", "Cluster", "kmeans_cluster"],
                )

                if merge_key and cluster_source:

                    cluster_map = kmeans_repos[
                        [merge_key, cluster_source]
                    ].drop_duplicates()

                    scores = scores.merge(
                        cluster_map,
                        on=merge_key,
                        how="left",
                    )

                    cluster_col = cluster_source

            if cluster_col:

                scores["Cluster"] = (
                    scores[cluster_col]
                    .astype(str)
                    .replace("nan", "Unassigned")
                )

            fig = px.scatter(
                scores,
                x=pc1_col,
                y=pc2_col,
                color="Cluster" if cluster_col else None,
                hover_name=repo_col if repo_col else None,
                opacity=0.78,
            )

            fig.update_layout(
                height=560,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#cbd5f0"),
                xaxis=dict(
                    title="PC1",
                    gridcolor="rgba(255,255,255,0.08)",
                ),
                yaxis=dict(
                    title="PC2",
                    gridcolor="rgba(255,255,255,0.08)",
                ),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False},
            )

    # ------------------------------------------------------------
    # K-MEANS
    # ------------------------------------------------------------

    section(
        "Repository Profile Clustering",
        "K-Means groups repositories with similar multidimensional activity and community characteristics.",
    )

    if not kmeans_eval.empty:

        evaluation = kmeans_eval.copy()

        k_col = find_column(
            evaluation,
            ["k", "K", "clusters", "n_clusters"],
        )
        silhouette_col = find_column(
            evaluation,
            ["silhouette_score", "silhouette", "Silhouette"],
        )

        if k_col and silhouette_col:

            evaluation[k_col] = pd.to_numeric(
                evaluation[k_col],
                errors="coerce",
            )
            evaluation[silhouette_col] = pd.to_numeric(
                evaluation[silhouette_col],
                errors="coerce",
            )

            evaluation = evaluation.dropna(
                subset=[k_col, silhouette_col]
            )

            fig = px.line(
                evaluation,
                x=k_col,
                y=silhouette_col,
                markers=True,
                text=evaluation[silhouette_col].round(3),
            )

            fig.update_traces(
                textposition="top center"
            )

            fig.update_layout(
                height=400,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#cbd5f0"),
                xaxis=dict(
                    title="Number of clusters (K)",
                    dtick=1,
                    gridcolor="rgba(255,255,255,0.08)",
                ),
                yaxis=dict(
                    title="Silhouette score",
                    gridcolor="rgba(255,255,255,0.08)",
                ),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False},
            )

    if not kmeans_profiles.empty:

        profiles = kmeans_profiles.copy()

        # Remove export artifacts if present.
        profiles = profiles.loc[
            :,
            [
                c for c in profiles.columns
                if not str(c).lower().startswith("unnamed")
            ],
        ]

        st.dataframe(
            profiles,
            use_container_width=True,
            hide_index=True,
        )

    render_html(
        """
        <div class="info-box">
            <div class="info-title">Why K = 2?</div>
            K = 2 is retained as the primary segmentation because it provides
            a more balanced and interpretable partition. K = 3 has only a
            slightly higher silhouette score and isolates a very small
            extreme high-activity subgroup, so it is treated as a sensitivity
            view rather than the main repository profile segmentation.
        </div>
        """
    )

    # ------------------------------------------------------------
    # POPULARITY VS ACTIVITY
    # ------------------------------------------------------------

    section(
        "Popularity vs Recent Activity",
        "A direct research-question view of whether repository popularity is associated with recent development activity.",
    )

    if not features.empty:

        star_col = find_column(
            features,
            ["stars", "log1p_stars"],
        )
        commit_col = find_column(
            features,
            ["commits_365d", "log1p_commits_365d"],
        )
        language_col = find_column(
            features,
            ["language", "language_normalized"],
        )

        if star_col and commit_col:

            scatter_df = features.copy()

            scatter_df[star_col] = pd.to_numeric(
                scatter_df[star_col],
                errors="coerce",
            )
            scatter_df[commit_col] = pd.to_numeric(
                scatter_df[commit_col],
                errors="coerce",
            )

            scatter_df = scatter_df.dropna(
                subset=[star_col, commit_col]
            )

            if language_col:

                scatter_df["Language"] = clean_language(
                    scatter_df[language_col]
                )

            fig = px.scatter(
                scatter_df,
                x=star_col,
                y=commit_col,
                color="Language" if language_col else None,
                hover_name=(
                    "full_name"
                    if "full_name" in scatter_df.columns
                    else None
                ),
                opacity=0.72,
            )

            fig.update_layout(
                height=520,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#cbd5f0"),
                xaxis=dict(
                    title=star_col,
                    gridcolor="rgba(255,255,255,0.08)",
                ),
                yaxis=dict(
                    title=commit_col,
                    gridcolor="rgba(255,255,255,0.08)",
                ),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False},
            )

    render_html(
        """
        <div class="info-box">
            <div class="info-title">Research finding</div>
            Popularity and recent activity show a moderate positive association
            in the reference sample (Pearson r ≈ 0.521). More popular
            repositories therefore tend to exhibit greater recent activity,
            but popularity alone does not determine activity and correlation
            does not establish causality.
        </div>
        """
    )

    # ------------------------------------------------------------
    # MULTIVARIATE FINDINGS
    # ------------------------------------------------------------

    section(
        "Multivariate Findings",
        "The statistical outputs are translated into concise analytical conclusions.",
    )

    findings = [
        (
            "01",
            "Repository structure is multidimensional.",
            "Popularity, activity, maintenance and community participation cannot be represented by one variable.",
        ),
        (
            "02",
            "PCA compresses correlated dimensions.",
            "Multiple components are required to preserve most of the information in the original feature space.",
        ),
        (
            "03",
            "Popularity and activity are associated.",
            "The observed Pearson correlation is approximately 0.521.",
        ),
        (
            "04",
            "Repository profiles are distinguishable.",
            "K-Means identifies a lower recent-activity profile and a higher popularity/activity/community profile.",
        ),
        (
            "05",
            "Extreme repositories influence clustering.",
            "The K = 3 sensitivity view isolates a very small extreme high-activity subgroup.",
        ),
    ]

    finding_cols = st.columns(5)

    for idx, (number, title, body) in enumerate(findings):

        with finding_cols[idx]:

            render_html(
                f"""
                <div class="metric-card" style="min-height:220px;">
                    <div class="metric-label">{number}</div>
                    <div class="info-title">{title}</div>
                    <div class="metric-note" style="font-size:13px;line-height:1.55;">
                        {body}
                    </div>
                </div>
                """
            )


# ================================================================
# TAB 5 — NETWORK ANALYSIS
# ================================================================

with tabs[4]:

    section(
        "Contributor Network Intelligence",
        "The contributor–repository bipartite structure reveals collaboration breadth and cross-repository participation.",
    )

    if contributors.empty:

        st.info(
            "repository_contributors.csv was not found."
        )

    else:

        contributor_col = find_column(
            contributors,
            ["contributor_login", "login", "contributor"],
        )

        repository_col = find_column(
            contributors,
            ["repo_name", "full_name", "repository"],
        )

        contributions_col = find_column(
            contributors,
            ["contributions", "commit_count"],
        )

        if contributor_col and repository_col:

            network_df = contributors[
                [contributor_col, repository_col]
                + (
                    [contributions_col]
                    if contributions_col
                    else []
                )
            ].copy()

            network_df = network_df.dropna(
                subset=[
                    contributor_col,
                    repository_col,
                ]
            )

            if contributions_col:

                network_df[contributions_col] = pd.to_numeric(
                    network_df[contributions_col],
                    errors="coerce",
                ).fillna(0)

            unique_contributors = network_df[
                contributor_col
            ].nunique()

            unique_repositories = network_df[
                repository_col
            ].nunique()

            relationship_count = len(network_df)

            # NetworkX metrics on the complete contributor-repository graph.
            try:

                G = nx.Graph()

                for row in network_df.itertuples(
                    index=False,
                    name=None,
                ):

                    contributor = str(row[0])
                    repository = str(row[1])

                    G.add_node(
                        f"C::{contributor}",
                        bipartite="contributor",
                    )
                    G.add_node(
                        f"R::{repository}",
                        bipartite="repository",
                    )

                    weight = (
                        float(row[2])
                        if contributions_col and len(row) > 2
                        else 1.0
                    )

                    G.add_edge(
                        f"C::{contributor}",
                        f"R::{repository}",
                        weight=weight,
                    )

                network_density = nx.density(G)
                component_count = nx.number_connected_components(G)

            except Exception:

                network_density = 0.0
                component_count = 0

            n1, n2, n3, n4, n5 = st.columns(5)

            with n1:
                metric_card(
                    "CONTRIBUTORS",
                    fmt_int(unique_contributors),
                    "Observed contributor nodes",
                )

            with n2:
                metric_card(
                    "REPOSITORIES",
                    fmt_int(unique_repositories),
                    "Observed repository nodes",
                )

            with n3:
                metric_card(
                    "RELATIONSHIPS",
                    fmt_int(relationship_count),
                    "Contributor–repository links",
                )

            with n4:
                metric_card(
                    "COMPONENTS",
                    fmt_int(component_count),
                    "Connected components",
                )

            with n5:
                metric_card(
                    "DENSITY",
                    f"{network_density:.4f}",
                    "Bipartite graph density",
                )

            render_html(
                """
                <div class="info-box" style="margin-top:20px;">
                    <div class="info-title">How to read the network</div>
                    Contributors and repositories form two node types. An edge
                    means that a contributor is observed in a repository's
                    contributor dataset. Edge weight represents recorded
                    contribution count when available.
                </div>
                """
            )

            # --------------------------------------------------------
            # ACTUAL NETWORK VISUALIZATION
            # --------------------------------------------------------

            section(
                "Contributor ↔ Repository Network",
                "A focused subgraph is rendered for interpretability rather than displaying all relationships simultaneously.",
            )

            top_repo_names = (
                network_df.groupby(repository_col)[
                    contributor_col
                ]
                .nunique()
                .sort_values(ascending=False)
                .head(12)
                .index
            )

            sub = network_df[
                network_df[repository_col].isin(top_repo_names)
            ].copy()

            if contributions_col:

                top_contributor_names = (
                    sub.groupby(contributor_col)[
                        contributions_col
                    ]
                    .sum()
                    .sort_values(ascending=False)
                    .head(30)
                    .index
                )

            else:

                top_contributor_names = (
                    sub[contributor_col]
                    .value_counts()
                    .head(30)
                    .index
                )

            sub = sub[
                sub[contributor_col].isin(
                    top_contributor_names
                )
            ].copy()

            contributor_names = list(
                pd.unique(sub[contributor_col])
            )[:30]

            repository_names = list(
                pd.unique(sub[repository_col])
            )[:12]

            sub = sub[
                sub[contributor_col].isin(contributor_names)
                & sub[repository_col].isin(repository_names)
            ]

            nc = max(len(contributor_names), 1)
            nr = max(len(repository_names), 1)

            cy = {
                name: 1 - (i + 1) / (nc + 1)
                for i, name in enumerate(contributor_names)
            }

            ry = {
                name: 1 - (i + 1) / (nr + 1)
                for i, name in enumerate(repository_names)
            }

            fig = go.Figure()

            # Edges.
            for row in sub.itertuples(
                index=False,
                name=None,
            ):

                contributor = row[0]
                repository = row[1]

                fig.add_trace(
                    go.Scatter(
                        x=[0, 1],
                        y=[
                            cy[contributor],
                            ry[repository],
                        ],
                        mode="lines",
                        line=dict(
                            color="rgba(130,155,220,0.22)",
                            width=1,
                        ),
                        hoverinfo="skip",
                        showlegend=False,
                    )
                )

            contributor_degree = (
                sub.groupby(contributor_col)
                .size()
                .reindex(contributor_names)
                .fillna(0)
            )

            fig.add_trace(
                go.Scatter(
                    x=[0] * len(contributor_names),
                    y=[cy[x] for x in contributor_names],
                    mode="markers+text",
                    text=contributor_names,
                    textposition="middle right",
                    marker=dict(
                        size=np.clip(
                            10 + contributor_degree.values * 1.5,
                            10,
                            30,
                        ),
                        color="#83a4ff",
                        line=dict(
                            color="#dbe4ff",
                            width=1,
                        ),
                    ),
                    name="Contributors",
                    hovertemplate=(
                        "<b>%{text}</b><br>"
                        "Type: Contributor<extra></extra>"
                    ),
                )
            )

            repository_degree = (
                sub.groupby(repository_col)
                .size()
                .reindex(repository_names)
                .fillna(0)
            )

            fig.add_trace(
                go.Scatter(
                    x=[1] * len(repository_names),
                    y=[ry[x] for x in repository_names],
                    mode="markers+text",
                    text=repository_names,
                    textposition="middle left",
                    marker=dict(
                        size=np.clip(
                            12 + repository_degree.values * 0.8,
                            12,
                            32,
                        ),
                        color="#b987ff",
                        symbol="square",
                        line=dict(
                            color="#eee4ff",
                            width=1,
                        ),
                    ),
                    name="Repositories",
                    hovertemplate=(
                        "<b>%{text}</b><br>"
                        "Type: Repository<extra></extra>"
                    ),
                )
            )

            fig.update_layout(
                height=760,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#cbd5f0"),
                margin=dict(l=20, r=20, t=30, b=20),
                xaxis=dict(
                    range=[-0.18, 1.18],
                    showgrid=False,
                    showticklabels=False,
                    zeroline=False,
                ),
                yaxis=dict(
                    range=[-0.05, 1.05],
                    showgrid=False,
                    showticklabels=False,
                    zeroline=False,
                ),
                legend=dict(
                    orientation="h",
                    y=1.02,
                    x=0,
                ),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False},
            )

            # --------------------------------------------------------
            # TOP CONTRIBUTORS
            # --------------------------------------------------------

            if contributions_col:

                section(
                    "Top Contributors",
                    "Highest observed contribution totals in the contributor dataset.",
                )

                top_contributors = (
                    network_df
                    .groupby(contributor_col)[
                        contributions_col
                    ]
                    .sum()
                    .sort_values(ascending=False)
                    .head(20)
                    .reset_index()
                )

                top_contributors.columns = [
                    "Contributor",
                    "Contributions",
                ]

                fig = px.bar(
                    top_contributors,
                    x="Contributions",
                    y="Contributor",
                    orientation="h",
                )

                fig.update_layout(
                    height=560,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#cbd5f0"),
                    xaxis=dict(
                        gridcolor="rgba(255,255,255,0.08)"
                    ),
                    yaxis=dict(
                        categoryorder="total ascending"
                    ),
                )

                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    config={"displayModeBar": False},
                )

            # --------------------------------------------------------
            # CONTRIBUTOR REACH
            # --------------------------------------------------------

            section(
                "Contributor Repository Reach",
                "Contributors ranked by the number of repositories in which they appear.",
            )

            contributor_reach = (
                network_df.groupby(contributor_col)[
                    repository_col
                ]
                .nunique()
                .sort_values(ascending=False)
                .head(20)
                .reset_index()
            )

            contributor_reach.columns = [
                "Contributor",
                "Repositories",
            ]

            fig = px.bar(
                contributor_reach,
                x="Repositories",
                y="Contributor",
                orientation="h",
            )

            fig.update_layout(
                height=540,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#cbd5f0"),
                xaxis=dict(
                    gridcolor="rgba(255,255,255,0.08)"
                ),
                yaxis=dict(
                    categoryorder="total ascending"
                ),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False},
            )

            # --------------------------------------------------------
            # REPOSITORY COLLABORATION BREADTH
            # --------------------------------------------------------

            section(
                "Repository Collaboration Breadth",
                "Repositories with the largest number of observed contributors.",
            )

            repo_breadth = (
                network_df
                .groupby(repository_col)[
                    contributor_col
                ]
                .nunique()
                .sort_values(ascending=False)
                .head(20)
                .reset_index()
            )

            repo_breadth.columns = [
                "Repository",
                "Contributors",
            ]

            fig = px.bar(
                repo_breadth,
                x="Contributors",
                y="Repository",
                orientation="h",
            )

            fig.update_layout(
                height=560,
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#cbd5f0"),
                xaxis=dict(
                    gridcolor="rgba(255,255,255,0.08)"
                ),
                yaxis=dict(
                    categoryorder="total ascending"
                ),
            )

            st.plotly_chart(
                fig,
                use_container_width=True,
                config={"displayModeBar": False},
            )

            render_html(
                """
                <div class="info-box">
                    <div class="info-title">Network interpretation</div>
                    The contributor dataset forms a bipartite
                    contributor–repository structure. A contributor may connect
                    to multiple repositories, while a repository may contain
                    contributions from many developers. This provides a
                    structural view of collaboration that repository stars
                    cannot represent.
                </div>
                """
            )


# TAB 6 — METHODOLOGY

# ================================================================



with tabs[5]:



    section(

        "Methodology",

        "How the research layer connects to the live application.",

    )



    m1, m2, m3 = st.columns(3)



    with m1:



        render_html(

            """

            <div class="info-box">



                <div class="info-title">

                    Research Layer

                </div>



                <b>300 repositories</b>



                <br><br>



                The star-stratified reference sample supports:



                <ul>

                    <li>Data-quality analysis</li>

                    <li>Descriptive statistics</li>

                    <li>Univariate EDA</li>

                    <li>Bivariate analysis</li>

                    <li>Multivariate analysis</li>

                    <li>Outlier analysis</li>

                    <li>PCA</li>

                    <li>K-Means profiling</li>

                    <li>Time-series analysis</li>

                    <li>Network analysis</li>

                </ul>



            </div>

            """

        )





    with m2:



        render_html(

            """

            <div class="info-box">



                <div class="info-title">

                    Live Application

                </div>



                Any public GitHub repository:



                <ol>

                    <li>Receives repository URL</li>

                    <li>Collects live metadata</li>

                    <li>Collects recent commits</li>

                    <li>Collects contributors</li>

                    <li>Constructs analytical features</li>

                    <li>Normalizes against reference layer</li>

                    <li>Produces repository intelligence</li>

                </ol>



            </div>

            """

        )





    with m3:



        render_html(

            """

            <div class="info-box">



                <div class="info-title">

                    Repository Health Index

                </div>



                Five equally weighted dimensions:



                <ul>

                    <li>Popularity — 20%</li>

                    <li>Activity — 20%</li>

                    <li>Maintenance — 20%</li>

                    <li>Community — 20%</li>

                    <li>Contribution Distribution — 20%</li>

                </ul>



                The score is a comparative analytical

                index rather than an objective software-quality

                label.



            </div>

            """

        )





    # ------------------------------------------------------------

    # PIPELINE

    # ------------------------------------------------------------



    st.markdown("<br>", unsafe_allow_html=True)



    section(

        "End-to-End Analytical Pipeline",

        "The project connects data collection, EDA and intelligence generation into one workflow.",

    )



    render_html(

        """

        <div style="

            display:grid;

            grid-template-columns:repeat(5,1fr);

            gap:12px;

            margin-top:20px;

        ">



            <div class="metric-card">

                <div class="metric-label">

                    01

                </div>

                <div class="metric-value" style="font-size:20px;">

                    Collect

                </div>

                <div class="metric-note">

                    GitHub repository data

                </div>

            </div>



            <div class="metric-card">

                <div class="metric-label">

                    02

                </div>

                <div class="metric-value" style="font-size:20px;">

                    Clean

                </div>

                <div class="metric-note">

                    Missing values, duplicates,

                    transformations

                </div>

            </div>



            <div class="metric-card">

                <div class="metric-label">

                    03

                </div>

                <div class="metric-value" style="font-size:20px;">

                    Explore

                </div>

                <div class="metric-note">

                    Statistics and visualization

                </div>

            </div>



            <div class="metric-card">

                <div class="metric-label">

                    04

                </div>

                <div class="metric-value" style="font-size:20px;">

                    Analyze

                </div>

                <div class="metric-note">

                    PCA, clustering, time series

                </div>

            </div>



            <div class="metric-card">

                <div class="metric-label">

                    05

                </div>

                <div class="metric-value" style="font-size:20px;">

                    Intelligence

                </div>

                <div class="metric-note">

                    Health and repository profiles

                </div>

            </div>



        </div>

        """

    )





    # ------------------------------------------------------------

    # IMPORTANT LIMITATIONS

    # ------------------------------------------------------------



    st.markdown("<br>", unsafe_allow_html=True)



    section(

        "Analytical Limitations",

        "Important interpretation constraints retained from the project methodology.",

    )



    render_html(

        """

        <div class="info-box">



            <ul>



                <li>

                    The 300-repository dataset is a

                    <b>star-stratified analytical sample</b>,

                    not a population-representative sample.

                </li>



                <li>

                    Repository Health Index is a

                    <b>comparative analytical index</b>,

                    not an objective measure of software quality.

                </li>



                <li>

                    Correlation does not imply causation.

                </li>



                <li>

                    GitHub API contributor data can omit

                    anonymous or otherwise unavailable identities.

                </li>



                <li>

                    Time-series observations are based on genuine

                    commit timestamps collected within the

                    observation window.

                </li>



                <li>

                    API-unavailable measurements are not silently

                    converted into zero activity.

                </li>



            </ul>



        </div>

        """

    )





# ================================================================

# FOOTER

# ================================================================



render_html(

    """

    <div class="footer">

        OpenSourcePulse · BACSE301 Exploratory Data Analysis

        · GitHub Repository Intelligence System

    </div>

    """

)
