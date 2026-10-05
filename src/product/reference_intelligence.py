# ============================================================
# OpenSourcePulse
# Reference Intelligence Engine
#
# PCA
# t-SNE
# Contributor Network Analysis
# Network Centrality
# ============================================================

from pathlib import Path

import numpy as np
import pandas as pd
import networkx as nx

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE


# ============================================================
# PROJECT PATHS
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parents[2]

FEATURE_FILE = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "repository_features_clean.csv"
)

CONTRIBUTOR_FILE = (
    PROJECT_ROOT
    / "data"
    / "raw"
    / "repository_contributors.csv"
)


# ============================================================
# PCA / t-SNE FEATURE SET
# ============================================================

PCA_FEATURES = [
    "log1p_stars",
    "log1p_forks",
    "log1p_open_issues",
    "log1p_size_kb",
    "age_years",
    "days_since_update",
    "days_since_push",
    "log1p_contributors",
    "log1p_total_contributions",
    "top_contributor_share",
    "log1p_commits_365d",
    "active_months",
    "log1p_peak_monthly_commits",
    "mean_monthly_commits",
    "monthly_commit_std",
]


# ============================================================
# LOAD REFERENCE DATA
# ============================================================

def load_reference_features():
    """
    Load the cleaned 300-repository analytical dataset.
    """

    if not FEATURE_FILE.exists():
        raise FileNotFoundError(
            f"Reference feature file not found:\n{FEATURE_FILE}"
        )

    return pd.read_csv(FEATURE_FILE)


# ============================================================
# PCA
# ============================================================

def build_pca_projection():
    """
    Build a 2D PCA projection of the reference repository sample.

    PCA is used here for dimensionality reduction and visualization.
    """

    df = load_reference_features()

    available = [
        column
        for column in PCA_FEATURES
        if column in df.columns
    ]

    if len(available) < 3:
        raise ValueError(
            "Insufficient PCA features available."
        )

    columns = ["full_name"] + available

    work = (
        df[columns]
        .copy()
        .dropna(subset=available)
        .reset_index(drop=True)
    )

    scaler = StandardScaler()

    X = scaler.fit_transform(
        work[available]
    )

    pca = PCA(
        n_components=2,
        random_state=42,
    )

    coordinates = pca.fit_transform(X)

    work["PC1"] = coordinates[:, 0]
    work["PC2"] = coordinates[:, 1]

    return (
        work,
        pca.explained_variance_ratio_,
    )


# ============================================================
# PCA WITH MORE INFORMATION
# ============================================================

def build_pca_full():
    """
    PCA projection with additional repository metadata
    useful for dashboard coloring and hover information.
    """

    df = load_reference_features()

    available = [
        column
        for column in PCA_FEATURES
        if column in df.columns
    ]

    metadata = [
        column
        for column in [
            "full_name",
            "language",
            "stars",
            "forks",
            "commits_365d",
            "contributors_count",
            "health_index",
            "health_profile",
        ]
        if column in df.columns
    ]

    work = (
        df[metadata + available]
        .copy()
        .dropna(subset=available)
        .reset_index(drop=True)
    )

    scaler = StandardScaler()

    X = scaler.fit_transform(
        work[available]
    )

    pca = PCA(
        n_components=min(
            7,
            len(available),
        ),
        random_state=42,
    )

    coordinates = pca.fit_transform(X)

    for i in range(
        coordinates.shape[1]
    ):
        work[f"PC{i + 1}"] = coordinates[:, i]

    return (
        work,
        pca.explained_variance_ratio_,
        pca.components_,
        available,
    )


# ============================================================
# t-SNE
# ============================================================

def build_tsne_projection():
    """
    Build a 2D t-SNE visualization.

    PCA is applied first to reduce noise and dimensionality.
    t-SNE is used only for nonlinear visualization,
    not clustering.
    """

    df = load_reference_features()

    available = [
        column
        for column in PCA_FEATURES
        if column in df.columns
    ]

    columns = ["full_name"] + available

    work = (
        df[columns]
        .copy()
        .dropna(subset=available)
        .reset_index(drop=True)
    )

    scaler = StandardScaler()

    X = scaler.fit_transform(
        work[available]
    )

    # --------------------------------------------------------
    # PCA preprocessing before t-SNE
    # --------------------------------------------------------

    n_components = min(
        10,
        X.shape[1],
    )

    pca = PCA(
        n_components=n_components,
        random_state=42,
    )

    X_reduced = pca.fit_transform(X)

    # --------------------------------------------------------
    # Perplexity must be smaller than number of observations
    # --------------------------------------------------------

    perplexity = min(
        30,
        max(
            5,
            len(work) // 8,
        ),
    )

    tsne = TSNE(
        n_components=2,
        perplexity=perplexity,
        learning_rate="auto",
        init="pca",
        random_state=42,
        max_iter=1000,
    )

    coordinates = tsne.fit_transform(
        X_reduced
    )

    work["tSNE1"] = coordinates[:, 0]
    work["tSNE2"] = coordinates[:, 1]

    return work


# ============================================================
# t-SNE WITH METADATA
# ============================================================

def build_tsne_full():
    """
    t-SNE projection with repository metadata.
    """

    df = load_reference_features()

    available = [
        column
        for column in PCA_FEATURES
        if column in df.columns
    ]

    metadata = [
        column
        for column in [
            "full_name",
            "language",
            "stars",
            "forks",
            "commits_365d",
            "contributors_count",
            "health_index",
            "health_profile",
        ]
        if column in df.columns
    ]

    work = (
        df[metadata + available]
        .copy()
        .dropna(subset=available)
        .reset_index(drop=True)
    )

    scaler = StandardScaler()

    X = scaler.fit_transform(
        work[available]
    )

    pca = PCA(
        n_components=min(
            10,
            X.shape[1],
        ),
        random_state=42,
    )

    X_reduced = pca.fit_transform(X)

    perplexity = min(
        30,
        max(
            5,
            len(work) // 8,
        ),
    )

    tsne = TSNE(
        n_components=2,
        perplexity=perplexity,
        learning_rate="auto",
        init="pca",
        random_state=42,
        max_iter=1000,
    )

    coordinates = tsne.fit_transform(
        X_reduced
    )

    work["tSNE1"] = coordinates[:, 0]
    work["tSNE2"] = coordinates[:, 1]

    return work


# ============================================================
# CONTRIBUTOR DATA
# ============================================================

def load_contributor_data():
    """
    Load the actual contributor dataset.

    Expected schema:

    repo_id
    full_name
    contributor_login
    contributor_id
    contributions
    """

    if not CONTRIBUTOR_FILE.exists():
        raise FileNotFoundError(
            f"Contributor file not found:\n{CONTRIBUTOR_FILE}"
        )

    df = pd.read_csv(
        CONTRIBUTOR_FILE
    )

    required = {
        "repo_id",
        "full_name",
        "contributor_login",
        "contributor_id",
        "contributions",
    }

    missing = required.difference(
        df.columns
    )

    if missing:
        raise ValueError(
            "Contributor dataset is missing columns: "
            + ", ".join(sorted(missing))
        )

    return df


# ============================================================
# CONTRIBUTOR NETWORK
# ============================================================

def build_contributor_network(
    top_repositories=20,
    top_contributors=40,
):
    """
    Build a weighted contributor-repository bipartite network.

    Repository nodes:
        repo::<full_name>

    Contributor nodes:
        user::<contributor_login>

    Edge weight:
        contribution count
    """

    contributors = load_contributor_data()

    # --------------------------------------------------------
    # Clean contributor data
    # --------------------------------------------------------

    contributors = contributors.dropna(
        subset=[
            "full_name",
            "contributor_login",
            "contributions",
        ]
    ).copy()

    contributors["contributions"] = pd.to_numeric(
        contributors["contributions"],
        errors="coerce",
    )

    contributors = contributors.dropna(
        subset=["contributions"]
    )

    contributors = contributors[
        contributors["contributions"] >= 0
    ]

    # --------------------------------------------------------
    # Aggregate duplicate repository-contributor pairs
    # --------------------------------------------------------

    contributors = (
        contributors
        .groupby(
            [
                "repo_id",
                "full_name",
                "contributor_login",
            ],
            as_index=False,
        )[
            "contributions"
        ]
        .sum()
    )

    # --------------------------------------------------------
    # Select top repositories based on contribution activity
    # --------------------------------------------------------

    repo_activity = (
        contributors
        .groupby(
            "full_name"
        )[
            "contributions"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(
            top_repositories
        )
    )

    selected_repositories = (
        repo_activity.index
        .tolist()
    )

    contributors = contributors[
        contributors["full_name"].isin(
            selected_repositories
        )
    ].copy()

    # --------------------------------------------------------
    # Select top contributors within selected repositories
    # --------------------------------------------------------

    contributor_activity = (
        contributors
        .groupby(
            "contributor_login"
        )[
            "contributions"
        ]
        .sum()
        .sort_values(
            ascending=False
        )
        .head(
            top_contributors
        )
    )

    selected_contributors = (
        contributor_activity.index
        .tolist()
    )

    contributors = contributors[
        contributors[
            "contributor_login"
        ].isin(
            selected_contributors
        )
    ].copy()

    # --------------------------------------------------------
    # Build weighted bipartite graph
    # --------------------------------------------------------

    G = nx.Graph()

    # Repository nodes
    for repo in selected_repositories:

        G.add_node(
            f"repo::{repo}",
            node_type="repository",
            label=repo,
        )

    # Contributor nodes
    for contributor in selected_contributors:

        G.add_node(
            f"user::{contributor}",
            node_type="contributor",
            label=contributor,
        )

    # --------------------------------------------------------
    # Add weighted edges
    # --------------------------------------------------------

    for row in contributors.itertuples(
        index=False
    ):

        repo_node = (
            f"repo::{row.full_name}"
        )

        user_node = (
            f"user::{row.contributor_login}"
        )

        G.add_edge(
            repo_node,
            user_node,
            weight=float(
                row.contributions
            ),
        )

    # --------------------------------------------------------
    # Remove isolated nodes
    # --------------------------------------------------------

    isolated = list(
        nx.isolates(G)
    )

    G.remove_nodes_from(
        isolated
    )

    # --------------------------------------------------------
    # Network statistics
    # --------------------------------------------------------

    repository_nodes = [
        node
        for node, attrs
        in G.nodes(data=True)
        if attrs.get("node_type")
        == "repository"
    ]

    contributor_nodes = [
        node
        for node, attrs
        in G.nodes(data=True)
        if attrs.get("node_type")
        == "contributor"
    ]

    density = nx.density(G)

    components = (
        nx.number_connected_components(G)
        if len(G) > 0
        else 0
    )

    return {
        "graph": G,
        "nodes": G.number_of_nodes(),
        "edges": G.number_of_edges(),
        "contributors": len(
            contributor_nodes
        ),
        "repositories": len(
            repository_nodes
        ),
        "density": density,
        "components": components,
        "selected_repositories": selected_repositories,
        "selected_contributors": selected_contributors,
    }


# ============================================================
# NETWORK PLOT DATA
# ============================================================

def network_plot_data(
    network_result,
):
    """
    Convert NetworkX graph into Plotly-ready node data.
    """

    G = network_result.get(
        "graph"
    )

    if G is None or len(G) == 0:
        return pd.DataFrame()

    # --------------------------------------------------------
    # Spring layout
    # --------------------------------------------------------

    pos = nx.spring_layout(
        G,
        seed=42,
        k=0.8,
        iterations=100,
        weight="weight",
    )

    degree = dict(
        G.degree()
    )

    weighted_degree = dict(
        G.degree(
            weight="weight"
        )
    )

    rows = []

    for node in G.nodes():

        attrs = G.nodes[
            node
        ]

        rows.append(
            {
                "node": node,
                "x": pos[node][0],
                "y": pos[node][1],
                "label": attrs.get(
                    "label",
                    node,
                ),
                "type": attrs.get(
                    "node_type",
                    "unknown",
                ),
                "degree": degree.get(
                    node,
                    0,
                ),
                "weighted_degree": weighted_degree.get(
                    node,
                    0,
                ),
            }
        )

    return pd.DataFrame(
        rows
    )


# ============================================================
# NETWORK EDGE DATA
# ============================================================

def network_edge_data(
    network_result,
):
    """
    Convert NetworkX edges into Plotly-ready data.
    """

    G = network_result.get(
        "graph"
    )

    if G is None or len(G) == 0:
        return pd.DataFrame()

    pos = nx.spring_layout(
        G,
        seed=42,
        k=0.8,
        iterations=100,
        weight="weight",
    )

    rows = []

    for source, target, attrs in G.edges(
        data=True
    ):

        rows.append(
            {
                "source": source,
                "target": target,
                "x0": pos[source][0],
                "y0": pos[source][1],
                "x1": pos[target][0],
                "y1": pos[target][1],
                "weight": attrs.get(
                    "weight",
                    1,
                ),
            }
        )

    return pd.DataFrame(
        rows
    )


# ============================================================
# NETWORK CENTRALITY
# ============================================================

def network_centrality(
    network_result,
):
    """
    Calculate degree centrality for contributors
    and repositories.
    """

    G = network_result.get(
        "graph"
    )

    if G is None or len(G) == 0:
        return pd.DataFrame()

    centrality = nx.degree_centrality(
        G
    )

    weighted_degree = dict(
        G.degree(
            weight="weight"
        )
    )

    rows = []

    for node, score in centrality.items():

        attrs = G.nodes[
            node
        ]

        rows.append(
            {
                "label": attrs.get(
                    "label",
                    node,
                ),
                "type": attrs.get(
                    "node_type",
                    "unknown",
                ),
                "degree": G.degree(
                    node
                ),
                "weighted_degree": weighted_degree.get(
                    node,
                    0,
                ),
                "degree_centrality": score,
            }
        )

    result = pd.DataFrame(
        rows
    )

    if result.empty:
        return result

    return result.sort_values(
        [
            "type",
            "degree_centrality",
        ],
        ascending=[
            True,
            False,
        ],
    ).reset_index(
        drop=True
    )


# ============================================================
# NETWORK SUMMARY
# ============================================================

def network_summary(
    network_result,
):
    """
    Human-readable network summary.
    """

    return {
        "repositories": network_result.get(
            "repositories",
            0,
        ),
        "contributors": network_result.get(
            "contributors",
            0,
        ),
        "connections": network_result.get(
            "edges",
            0,
        ),
        "nodes": network_result.get(
            "nodes",
            0,
        ),
        "density": network_result.get(
            "density",
            0,
        ),
        "components": network_result.get(
            "components",
            0,
        ),
    }


# ============================================================
# MODULE TEST
# ============================================================

if __name__ == "__main__":

    print("=" * 60)
    print("OpenSourcePulse Reference Intelligence Test")
    print("=" * 60)

    # PCA
    pca_df, variance = build_pca_projection()

    print()
    print("PCA")
    print("-" * 60)
    print("Rows:", len(pca_df))
    print(
        "PC1 variance:",
        round(
            variance[0] * 100,
            2,
        ),
        "%",
    )
    print(
        "PC2 variance:",
        round(
            variance[1] * 100,
            2,
        ),
        "%",
    )

    # t-SNE
    tsne_df = build_tsne_projection()

    print()
    print("t-SNE")
    print("-" * 60)
    print("Rows:", len(tsne_df))

    # Network
    network = build_contributor_network()

    print()
    print("Contributor Network")
    print("-" * 60)
    print(
        "Nodes:",
        network["nodes"],
    )
    print(
        "Edges:",
        network["edges"],
    )
    print(
        "Repositories:",
        network["repositories"],
    )
    print(
        "Contributors:",
        network["contributors"],
    )
    print(
        "Density:",
        round(
            network["density"],
            6,
        ),
    )
    print(
        "Components:",
        network["components"],
    )

    print()
    print("=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)