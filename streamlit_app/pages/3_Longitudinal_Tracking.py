import sys
from pathlib import Path
from textwrap import dedent

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
import streamlit as st


APP_DIR = Path(__file__).resolve().parents[1]

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from theme import apply_theme
from data_paths import RESULTS_ROOT


st.set_page_config(
    page_title="TCRFlowX | Longitudinal Dynamics",
    page_icon="🧬",
    layout="wide",
)

apply_theme()

ROOT = Path(__file__).resolve().parents[2]


def html(content):
    st.html(dedent(content).strip())


tracking = pd.read_csv(
    RESULTS_ROOT
    / "repertoire/tables/"
    "pbmc_longitudinal_clonotypes.tsv",
    sep="\t",
)


# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Longitudinal TCRβ Clone Dynamics</h3>
</div>
""")

st.caption(
    "Track productive clonotypes across pre-treatment, "
    "relapse and progressive disease."
)


# ---------------------------------------------------------
# KPI
# ---------------------------------------------------------

persistent = tracking[
    tracking["detected_timepoints"] == 3
]

pre_only = tracking[
    (tracking["PBMC_PRE"] > 0)
    & (tracking["PBMC_RELAPSE"] == 0)
    & (tracking["PBMC_PROGRESSION"] == 0)
]

relapse_emergent = tracking[
    (tracking["PBMC_PRE"] == 0)
    & (tracking["PBMC_RELAPSE"] > 0)
]

progression_emergent = tracking[
    (tracking["PBMC_PRE"] == 0)
    & (tracking["PBMC_PROGRESSION"] > 0)
]


c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Persistent clones",
    f"{len(persistent):,}"
)

c2.metric(
    "Pre-treatment only",
    f"{len(pre_only):,}"
)

c3.metric(
    "Relapse-emergent",
    f"{len(relapse_emergent):,}"
)

c4.metric(
    "Progression-emergent",
    f"{len(progression_emergent):,}"
)


# ---------------------------------------------------------
# SANKEY
# Intent:
# Illustrate longitudinal clone-state continuity
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Longitudinal clone flow</h3>
</div>
""")

st.caption(
    "Top persistent clones are represented individually; "
    "the visualization emphasizes continuity through the clinical course."
)


top_n = st.slider(
    "Persistent clonotypes shown in flow",
    min_value=5,
    max_value=20,
    value=10,
)

top_persistent = (
    persistent
    .sort_values(
        "max_fraction",
        ascending=False
    )
    .head(top_n)
    .copy()
)


labels = []

for stage in [
    "PRE",
    "RELAPSE",
    "PROGRESSION"
]:

    for clone in top_persistent["cdr3aa"]:

        labels.append(
            f"{stage}<br>{clone}"
        )


n = len(
    top_persistent
)

sources = []
targets = []
values = []


for i, (_, row) in enumerate(
    top_persistent.iterrows()
):

    sources.append(i)

    targets.append(n + i)

    values.append(
        max(
            row["PBMC_PRE"],
            0.00001
        )
    )


    sources.append(n + i)

    targets.append(
        (2 * n) + i
    )

    values.append(
        max(
            row["PBMC_RELAPSE"],
            0.00001
        )
    )


node_colors = (
    ["#B8343E"] * n
    + ["#F28A3C"] * n
    + ["#C93E55"] * n
)


fig = go.Figure(
    go.Sankey(
        arrangement="snap",

        node=dict(
            pad=14,
            thickness=17,
            label=labels,
            color=node_colors,
            line=dict(
                color="#FFFFFF",
                width=0.7
            ),
        ),

        link=dict(
            source=sources,
            target=targets,
            value=values,
            color="rgba(214,90,69,0.28)",
        ),
    )
)


fig.update_layout(
    height=max(
        550,
        top_n * 42
    ),
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(
        size=10,
        color="#60383A"
    ),
    margin=dict(
        l=20,
        r=20,
        t=30,
        b=20
    ),
)

st.plotly_chart(
    fig,
    width='stretch'
)


# ---------------------------------------------------------
# TRAJECTORY CHART
# Intent:
# Which dominant clones expand / contract?
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Expansion and contraction trajectories</h3>
</div>
""")


trajectory_n = st.slider(
    "Top clones for trajectory analysis",
    min_value=5,
    max_value=30,
    value=12,
)


top = tracking.sort_values(
    "max_fraction",
    ascending=False
).head(
    trajectory_n
).copy()


long = top.melt(
    id_vars=["cdr3aa"],
    value_vars=[
        "PBMC_PRE",
        "PBMC_RELAPSE",
        "PBMC_PROGRESSION",
    ],
    var_name="Clinical stage",
    value_name="Fraction",
)


order_map = {
    "PBMC_PRE":
        "Pre-treatment",

    "PBMC_RELAPSE":
        "Relapse",

    "PBMC_PROGRESSION":
        "Progression",
}

long[
    "Clinical stage"
] = long[
    "Clinical stage"
].map(
    order_map
)


fig = px.line(
    long,
    x="Clinical stage",
    y="Fraction",
    color="cdr3aa",
    markers=True,
    category_orders={
        "Clinical stage": [
            "Pre-treatment",
            "Relapse",
            "Progression",
        ]
    },
)


fig.update_traces(
    line=dict(
        width=2.8
    ),
    marker=dict(
        size=8
    ),
)


fig.update_layout(
    height=620,
    xaxis_title="Clinical stage",
    yaxis_title="Clone fraction",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#FFF9F4",
    legend_title="CDR3",
    hovermode="x unified",
)


st.plotly_chart(
    fig,
    width='stretch'
)


# ---------------------------------------------------------
# HEATMAP
# Intent:
# Detect persistent / stage-biased clones
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Longitudinal abundance fingerprint</h3>
</div>
""")


heat_n = st.slider(
    "Top clonotypes in heatmap",
    min_value=10,
    max_value=60,
    value=30,
)


heat = (
    tracking
    .sort_values(
        "max_fraction",
        ascending=False
    )
    .head(heat_n)
    .set_index("cdr3aa")
    [
        [
            "PBMC_PRE",
            "PBMC_RELAPSE",
            "PBMC_PROGRESSION",
        ]
    ]
)


heat.columns = [
    "Pre-treatment",
    "Relapse",
    "Progression"
]


heat_log = np.log10(
    heat + 1e-6
)


fig, ax = plt.subplots(
    figsize=(
        8.5,
        max(
            7,
            heat_n * 0.26
        )
    )
)

fig.patch.set_facecolor(
    "#FFF9F4"
)


sns.heatmap(
    heat_log,
    cmap="rocket",
    linewidths=0.35,
    linecolor="#FFF4EC",
    cbar_kws={
        "label":
        "log10 clone fraction"
    },
    ax=ax,
)


ax.set_xlabel("")
ax.set_ylabel(
    "CDR3 amino-acid sequence"
)

ax.set_title(
    "Persistent and stage-biased TCRβ clonotypes",
    fontweight="bold"
)


plt.tight_layout()


st.pyplot(
    fig,
    width='stretch'
)

plt.close(fig)


# ---------------------------------------------------------
# DOMINANT CLONE
# ---------------------------------------------------------

dominant = tracking.sort_values(
    "max_fraction",
    ascending=False
).iloc[0]


html(f"""
<div class="insight-card">

    <div class="insight-title">
        Dominant persistent clonotype — {dominant["cdr3aa"]}
    </div>

    <div class="muted" style="margin-top:8px; line-height:1.8;">

        Pre-treatment:
        <b>{dominant["PBMC_PRE"] * 100:.2f}%</b>

        &nbsp;&nbsp;→&nbsp;&nbsp;

        Relapse:
        <b>{dominant["PBMC_RELAPSE"] * 100:.2f}%</b>

        &nbsp;&nbsp;→&nbsp;&nbsp;

        Progression:
        <b>{dominant["PBMC_PROGRESSION"] * 100:.2f}%</b>

        <br>

        This clonotype remains detectable across the entire
        longitudinal disease trajectory.

    </div>

</div>
""")


with st.expander(
    "Explore longitudinal clonotype table"
):

    st.dataframe(
        tracking,
        width='stretch',
        hide_index=True,
    )