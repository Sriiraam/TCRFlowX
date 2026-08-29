import sys
from pathlib import Path
from textwrap import dedent

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import streamlit as st


APP_DIR = Path(__file__).resolve().parents[1]

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from theme import apply_theme
from data_paths import RESULTS_ROOT


st.set_page_config(
    page_title="TCRFlowX | Repertoire Landscape",
    page_icon="🧬",
    layout="wide",
)

apply_theme()

ROOT = Path(__file__).resolve().parents[2]


def html(content):
    st.html(dedent(content).strip())


# ---------------------------------------------------------
# LOAD METRICS
# ---------------------------------------------------------

div = pd.read_csv(
    ROOT
    / "results/repertoire/tables/"
    "diversity_clonality.tsv",
    sep="\t",
)


# ---------------------------------------------------------
# LOAD PRODUCTIVE CLONES
# ---------------------------------------------------------

clone_tables = []

for sample in div["sample"]:

    path = (
        ROOT
        / "results"
        / "mixcr"
        / sample
        / f"{sample}.clones_TRB.tsv"
    )

    x = pd.read_csv(
        path,
        sep="\t"
    )

    x = x[
        x["aaSeqCDR3"].notna()
    ].copy()

    x = x[
        ~x["aaSeqCDR3"].astype(str)
        .str.contains(
            r"[\*_]",
            regex=True
        )
    ].copy()

    x["sample"] = sample

    clone_tables.append(x)


clones = pd.concat(
    clone_tables,
    ignore_index=True
)

clones["log_fraction"] = np.log10(
    clones["readFraction"]
    .clip(lower=1e-8)
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>TCRβ Repertoire Landscape</h3>
</div>
""")

st.caption(
    "Explore repertoire breadth, diversity, oligoclonality "
    "and dominant-clone architecture."
)


# ---------------------------------------------------------
# KPI ROW
# ---------------------------------------------------------

most_diverse = div.loc[
    div["shannon"].idxmax()
]

most_clonal = div.loc[
    div["clonality"].idxmax()
]

widest = div.loc[
    div["productive_richness"].idxmax()
]

c1, c2, c3 = st.columns(3)

c1.metric(
    "Largest productive repertoire",
    widest["sample"],
    f"{int(widest['productive_richness']):,} clones"
)

c2.metric(
    "Highest Shannon diversity",
    most_diverse["sample"],
    f"{most_diverse['shannon']:.3f}"
)

c3.metric(
    "Highest clonality",
    most_clonal["sample"],
    f"{most_clonal['clonality']:.3f}"
)


# ---------------------------------------------------------
# LOLLIPOP — RICHNESS
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Repertoire breadth</h3>
</div>
""")

fig, ax = plt.subplots(
    figsize=(10, 5)
)

fig.patch.set_facecolor(
    "#FFF9F4"
)

ax.set_facecolor(
    "#FFF9F4"
)

plot_df = div.sort_values(
    "productive_richness"
)

y = np.arange(
    len(plot_df)
)

ax.hlines(
    y,
    0,
    plot_df["productive_richness"],
    color="#F2A071",
    linewidth=4,
)

ax.scatter(
    plot_df["productive_richness"],
    y,
    s=180,
    color="#A92E3B",
    edgecolor="white",
    linewidth=1.5,
)

for i, value in enumerate(
    plot_df["productive_richness"]
):
    ax.text(
        value + 80,
        i,
        f"{int(value):,}",
        va="center",
        fontsize=10,
        fontweight="bold",
        color="#6A3134",
    )

ax.set_yticks(y)

ax.set_yticklabels(
    plot_df["sample"]
)

ax.set_xlabel(
    "Productive unique CDR3 clonotypes"
)

ax.set_title(
    "How broad is each TCRβ repertoire?",
    fontweight="bold"
)

sns.despine(
    left=True
)

plt.tight_layout()

st.pyplot(
    fig,
    width='stretch'
)

plt.close(fig)


# ---------------------------------------------------------
# VIOLIN + SWARM — CLONE ABUNDANCE
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Clone-frequency architecture</h3>
</div>
""")

st.caption(
    "Violin shape uses every productive clonotype. "
    "Swarm points are a representative sample for readability."
)

swarm_parts = []

for sample_name in div["sample"]:

    group = clones[
        clones["sample"] == sample_name
    ]

    sampled = group.sample(
        n=min(
            180,
            len(group)
        ),
        random_state=42,
    ).copy()

    sampled["sample"] = sample_name

    swarm_parts.append(
        sampled
    )

swarm_df = pd.concat(
    swarm_parts,
    ignore_index=True
)


fig, ax = plt.subplots(
    figsize=(12, 6)
)

fig.patch.set_facecolor(
    "#FFF9F4"
)

ax.set_facecolor(
    "#FFF9F4"
)


sns.violinplot(
    data=clones,
    x="sample",
    y="log_fraction",
    inner="quart",
    cut=0,
    linewidth=1.1,
    palette="rocket",
    hue="sample",
    legend=False,
    ax=ax,
)


sns.swarmplot(
    data=swarm_df,
    x="sample",
    y="log_fraction",
    size=2.2,
    alpha=0.38,
    color="#501D27",
    ax=ax,
)


ax.set_xlabel("")

ax.set_ylabel(
    "log10 clone fraction"
)

ax.set_title(
    "Distribution of productive clonotype abundance",
    fontweight="bold"
)

ax.tick_params(
    axis="x",
    rotation=18
)

sns.despine()

plt.tight_layout()

st.pyplot(
    fig,
    width='stretch'
)

plt.close(fig)


html("""
<div class="insight-card">

    <div class="insight-title">
        Why this visualization?
    </div>

    <div class="muted" style="margin-top:7px;">
        TCR clone frequencies are extremely skewed. The violin reveals
        the complete abundance distribution while the swarm exposes
        individual clonotype observations. A wider upper tail indicates
        stronger expansion of dominant T-cell clones.
    </div>

</div>
""")


# ---------------------------------------------------------
# POLAR CLONALITY
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Oligoclonality profile</h3>
</div>
""")

polar = div.copy()

fig = go.Figure()

fig.add_trace(
    go.Scatterpolar(
        r=polar["clonality"],
        theta=polar["sample"],
        fill="toself",
        line=dict(
            color="#B8343E",
            width=3
        ),
        fillcolor="rgba(232,93,78,0.28)",
        marker=dict(
            size=10,
            color="#F28A3C"
        ),
        hovertemplate=(
            "<b>%{theta}</b><br>"
            "Clonality: %{r:.3f}"
            "<extra></extra>"
        ),
    )
)

fig.update_layout(
    polar=dict(
        bgcolor="#FFF9F4",
        radialaxis=dict(
            visible=True,
            range=[
                0,
                max(
                    div["clonality"]
                ) * 1.25
            ],
            gridcolor="#EED6C9",
        ),
        angularaxis=dict(
            gridcolor="#EED6C9"
        ),
    ),
    height=520,
    showlegend=False,
    paper_bgcolor="rgba(0,0,0,0)",
    margin=dict(
        l=80,
        r=80,
        t=40,
        b=40
    ),
)

st.plotly_chart(
    fig,
    width='stretch'
)


# ---------------------------------------------------------
# CLONE DOMINANCE COMPOSITION
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Dominant clone contribution</h3>
</div>
""")

dominance = div.copy()

dominance["Top 1 clone"] = (
    dominance["top1_fraction"]
    * 100
)

dominance["Clones 2–10"] = (
    dominance["top10_fraction"]
    - dominance["top1_fraction"]
) * 100

dominance["Clones 11–100"] = (
    dominance["top100_fraction"]
    - dominance["top10_fraction"]
) * 100

dominance["Remaining repertoire"] = (
    1
    - dominance["top100_fraction"]
) * 100


fig = go.Figure()

segments = [
    (
        "Top 1 clone",
        "#9D2835"
    ),
    (
        "Clones 2–10",
        "#D94C45"
    ),
    (
        "Clones 11–100",
        "#F28A3C"
    ),
    (
        "Remaining repertoire",
        "#F7D9C5"
    ),
]

for column, color in segments:

    fig.add_bar(
        y=dominance["sample"],
        x=dominance[column],
        name=column,
        orientation="h",
        marker_color=color,
        hovertemplate=(
            "%{y}<br>"
            f"{column}: "
            "%{x:.1f}%"
            "<extra></extra>"
        ),
    )


fig.update_layout(
    barmode="stack",
    height=470,
    xaxis=dict(
        title="Repertoire composition (%)",
        range=[0, 100]
    ),
    yaxis_title="",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#FFF9F4",
    legend=dict(
        orientation="h",
        y=1.12
    ),
)

st.plotly_chart(
    fig,
    width='stretch'
)


# ---------------------------------------------------------
# METRIC TABLE
# ---------------------------------------------------------

with st.expander(
    "View repertoire metrics"
):

    st.dataframe(
        div.round(4),
        width='stretch',
        hide_index=True,
    )