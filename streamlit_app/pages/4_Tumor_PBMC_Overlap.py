import sys
from pathlib import Path
from textwrap import dedent

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import streamlit as st


APP_DIR = Path(__file__).resolve().parents[1]

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from theme import apply_theme


st.set_page_config(
    page_title="TCRFlowX | Tumor PBMC Overlap",
    page_icon="🧬",
    layout="wide",
)

apply_theme()

ROOT = Path(__file__).resolve().parents[2]


def html(content):
    st.html(dedent(content).strip())


overlap = pd.read_csv(
    ROOT
    / "results/repertoire/tables/"
    "tumor_pbmc_overlap.tsv",
    sep="\t",
)

jaccard = pd.read_csv(
    ROOT
    / "results/repertoire/tables/"
    "pairwise_jaccard.tsv",
    sep="\t",
    index_col=0,
)

tumor = pd.read_csv(
    ROOT
    / "results/repertoire/tables/"
    "tumor_longitudinal_clonotypes.tsv",
    sep="\t",
)


# ---------------------------------------------------------
# MASTER TITLE
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Tumor–PBMC Immune Repertoire Overlap</h3>
</div>
""")

st.caption(
    "Compare circulating and tumor-associated TCRβ repertoires "
    "before treatment and during progressive disease."
)


# ---------------------------------------------------------
# KPIs
# ---------------------------------------------------------

pre = overlap.loc[
    overlap["stage"] == "PRE"
].iloc[0]

prog = overlap.loc[
    overlap["stage"] == "PROGRESSION"
].iloc[0]

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "PRE shared clones",
    f"{int(pre['shared_clonotypes']):,}"
)

c2.metric(
    "PRE Jaccard",
    f"{pre['jaccard']:.3f}"
)

c3.metric(
    "Progression shared",
    f"{int(prog['shared_clonotypes']):,}"
)

c4.metric(
    "Progression Jaccard",
    f"{prog['jaccard']:.3f}"
)


# ---------------------------------------------------------
# DUMBBELL
# Intent: matched blood-vs-tumor repertoire breadth
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Matched repertoire breadth</h3>
</div>
""")

dumbbell = pd.DataFrame({
    "stage": ["Pre-treatment", "Progression"],
    "PBMC": [
        pre["pbmc_clonotypes"],
        prog["pbmc_clonotypes"],
    ],
    "Tumor": [
        pre["tumor_clonotypes"],
        prog["tumor_clonotypes"],
    ],
})

fig, ax = plt.subplots(figsize=(10, 4.8))

fig.patch.set_facecolor("#FFF9F4")
ax.set_facecolor("#FFF9F4")

y = np.arange(len(dumbbell))

for i, row in dumbbell.iterrows():

    ax.plot(
        [row["PBMC"], row["Tumor"]],
        [i, i],
        linewidth=4,
        color="#F1B18C",
        zorder=1,
    )

    ax.scatter(
        row["PBMC"],
        i,
        s=180,
        color="#B8343E",
        label="PBMC" if i == 0 else "",
        zorder=3,
    )

    ax.scatter(
        row["Tumor"],
        i,
        s=180,
        color="#F28A3C",
        label="Tumor" if i == 0 else "",
        zorder=3,
    )

ax.set_yticks(y)
ax.set_yticklabels(dumbbell["stage"])

ax.set_xlabel(
    "Productive clonotypes"
)

ax.set_title(
    "PBMC vs tumor repertoire breadth",
    fontweight="bold"
)

ax.legend(
    frameon=False,
    loc="lower right"
)

sns.despine()

plt.tight_layout()

st.pyplot(
    fig,
    width='stretch'
)

plt.close(fig)


# ---------------------------------------------------------
# JACCARD HEATMAP
# Intent: pairwise repertoire similarity
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Pairwise repertoire similarity</h3>
</div>
""")

fig, ax = plt.subplots(
    figsize=(9, 7)
)

fig.patch.set_facecolor(
    "#FFF9F4"
)

sns.heatmap(
    jaccard,
    annot=True,
    fmt=".2f",
    cmap="YlOrRd",
    linewidths=1,
    linecolor="#FFF4EC",
    square=True,
    ax=ax,
)

ax.set_title(
    "Productive CDR3 Jaccard similarity",
    fontweight="bold"
)

ax.set_xlabel("")
ax.set_ylabel("")

plt.tight_layout()

st.pyplot(
    fig,
    width='stretch'
)

plt.close(fig)


# ---------------------------------------------------------
# OVERLAP CHANGE
# Intent: direct PRE -> progression decline
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Blood–tumor overlap across disease progression</h3>
</div>
""")

fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=[
            "Pre-treatment",
            "Progression",
        ],
        y=[
            pre["jaccard"],
            prog["jaccard"],
        ],
        mode="lines+markers+text",
        line=dict(
            color="#B8343E",
            width=5
        ),
        marker=dict(
            size=15,
            color=[
                "#F28A3C",
                "#B8343E",
            ]
        ),
        text=[
            f"{pre['jaccard']:.3f}",
            f"{prog['jaccard']:.3f}",
        ],
        textposition="top center",
    )
)

fig.update_layout(
    height=430,
    yaxis_title="Jaccard similarity",
    xaxis_title="",
    showlegend=False,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#FFF9F4",
)

st.plotly_chart(
    fig,
    width='stretch'
)


# ---------------------------------------------------------
# TUMOR CLONE CHANGE
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Tumor clonotype remodeling</h3>
</div>
""")

top_tumor = (
    tumor
    .sort_values(
        "max_fraction",
        ascending=False
    )
    .head(20)
    .copy()
)

top_tumor["log2_fold_change"] = np.log2(
    top_tumor["fold_change"].clip(
        lower=1e-8
    )
)

fig, ax = plt.subplots(
    figsize=(10, 7)
)

fig.patch.set_facecolor(
    "#FFF9F4"
)

bars = ax.barh(
    top_tumor["cdr3aa"],
    top_tumor["log2_fold_change"],
    color=[
        "#B8343E"
        if x > 0
        else "#F28A3C"
        for x in top_tumor[
            "log2_fold_change"
        ]
    ],
)

ax.axvline(
    0,
    color="#6A4A47",
    linewidth=1
)

ax.set_xlabel(
    "log2 progression / pre-treatment"
)

ax.set_title(
    "Top tumor clonotype expansion and contraction",
    fontweight="bold"
)

sns.despine()

plt.tight_layout()

st.pyplot(
    fig,
    width='stretch'
)

plt.close(fig)


html(f"""
<div class="insight-card">

    <div class="insight-title">
        Tumor–blood repertoire divergence
    </div>

    <div class="muted" style="margin-top:7px;">

        Shared productive clonotypes decreased from
        <b>{int(pre["shared_clonotypes"]):,}</b>
        before treatment to
        <b>{int(prog["shared_clonotypes"]):,}</b>
        during progression.

        Jaccard similarity declined from
        <b>{pre["jaccard"]:.3f}</b>
        to
        <b>{prog["jaccard"]:.3f}</b>.

    </div>

</div>
""")