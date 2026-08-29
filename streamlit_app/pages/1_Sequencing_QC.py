import sys
from pathlib import Path
from textwrap import dedent

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
    page_title="TCRFlowX | Sequencing QC",
    page_icon="🧬",
    layout="wide",
)

apply_theme()

ROOT = Path(__file__).resolve().parents[2]


def html(content):
    st.html(dedent(content).strip())


# ---------------------------------------------------------
# DATA
# ---------------------------------------------------------

qc = pd.read_csv(
    RESULTS_ROOT / "mixcr/mixcr_qc_summary.tsv",
    sep="\t",
)


# ---------------------------------------------------------
# HERO
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Sequencing & MiXCR Quality Control</h3>
</div>
""")

st.caption(
    "Assess sequencing usability, TCR reconstruction efficiency, "
    "off-target burden and clonotype recovery."
)


# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Mean alignment",
    f"{qc['aligned_reads_pct'].mean():.1f}%"
)

c2.metric(
    "Best alignment",
    f"{qc['aligned_reads_pct'].max():.1f}%"
)

c3.metric(
    "TRB clonotypes",
    f"{qc['trb_clonotypes'].sum():,}"
)

c4.metric(
    "Quality-loss maximum",
    f"{qc['low_quality_drop_pct'].max():.1f}%"
)


# ---------------------------------------------------------
# SAMPLE GAUGE + CLONOTYPE RECOVERY
# Intent:
# Gauge = reconstruction efficiency
# Lollipop = absolute TRB recovery
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Reconstruction efficiency</h3>
</div>
""")

left, right = st.columns([0.9, 1.2])

with left:

    selected = st.selectbox(
        "Inspect sample",
        qc["sample_id"].tolist()
    )

    row = qc.loc[
        qc["sample_id"] == selected
    ].iloc[0]

    fig = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=row["aligned_reads_pct"],
            number={
                "suffix": "%",
                "font": {"size": 42}
            },
            title={
                "text":
                f"{selected}<br>"
                "<span style='font-size:14px'>"
                "MiXCR alignment"
                "</span>"
            },
            gauge={
                "axis": {
                    "range": [0, 100],
                    "tickwidth": 1
                },
                "bar": {
                    "color": "#B8343E",
                    "thickness": 0.30
                },
                "steps": [
                    {
                        "range": [0, 50],
                        "color": "#FCE4DE"
                    },
                    {
                        "range": [50, 75],
                        "color": "#F9C9B3"
                    },
                    {
                        "range": [75, 100],
                        "color": "#F6A15E"
                    },
                ],
            },
        )
    )

    fig.update_layout(
        height=350,
        margin=dict(
            l=30,
            r=30,
            t=70,
            b=20
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#5A3133"},
    )

    st.plotly_chart(
        fig,
        width='stretch'
    )


with right:

    plot_df = qc.sort_values(
        "trb_clonotypes"
    )

    fig, ax = plt.subplots(
        figsize=(8.5, 4.6)
    )

    fig.patch.set_facecolor("#FFF9F4")
    ax.set_facecolor("#FFF9F4")

    y = range(len(plot_df))

    ax.hlines(
        y=y,
        xmin=0,
        xmax=plot_df["trb_clonotypes"],
        linewidth=3,
        color="#F2A071",
    )

    ax.scatter(
        plot_df["trb_clonotypes"],
        y,
        s=150,
        color="#B8343E",
        edgecolor="white",
        linewidth=1.5,
        zorder=3,
    )

    ax.set_yticks(list(y))
    ax.set_yticklabels(
        plot_df["sample_id"]
    )

    ax.set_xlabel(
        "TRB clonotypes"
    )

    ax.set_title(
        "TRB repertoire recovery",
        fontweight="bold"
    )

    sns.despine(
        left=True,
        bottom=False
    )

    plt.tight_layout()

    st.pyplot(
        fig,
        width='stretch'
    )

    plt.close(fig)


# ---------------------------------------------------------
# STACKED READ COMPOSITION
# Intent:
# Where sequencing reads go after reconstruction
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Where did the sequencing reads go?</h3>
</div>
""")

composition = qc.copy()

composition["other_pct"] = (
    100
    - composition["aligned_reads_pct"]
    - composition["off_target_pct"]
).clip(lower=0)

fig = go.Figure()

fig.add_bar(
    y=composition["sample_id"],
    x=composition["aligned_reads_pct"],
    name="Successfully aligned",
    orientation="h",
    marker_color="#B8343E",
)

fig.add_bar(
    y=composition["sample_id"],
    x=composition["off_target_pct"],
    name="Off-target",
    orientation="h",
    marker_color="#F28A3C",
)

fig.add_bar(
    y=composition["sample_id"],
    x=composition["other_pct"],
    name="Other / unresolved",
    orientation="h",
    marker_color="#F4D6BF",
)

fig.update_layout(
    barmode="stack",
    height=440,
    xaxis_title="Sequencing reads (%)",
    yaxis_title="",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#FFF9F4",
    legend=dict(
        orientation="h",
        y=1.12
    ),
    margin=dict(
        l=20,
        r=20,
        t=50,
        b=40
    ),
)

st.plotly_chart(
    fig,
    width='stretch'
)


# ---------------------------------------------------------
# QC HEATMAP
# Intent:
# Detect samples with unusual QC patterns
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Cross-sample QC fingerprint</h3>
</div>
""")

heat_cols = [
    "aligned_reads_pct",
    "reads_used_in_clonotypes_pct",
    "off_target_pct",
    "no_v_or_j_hits_pct",
    "no_cdr3_pct",
]

heat = qc.set_index(
    "sample_id"
)[heat_cols]

heat_z = (
    heat - heat.mean()
) / heat.std(ddof=0)

fig, ax = plt.subplots(
    figsize=(11, 5)
)

fig.patch.set_facecolor("#FFF9F4")

sns.heatmap(
    heat_z,
    annot=heat.round(1),
    fmt=".1f",
    cmap="rocket_r",
    center=0,
    linewidths=1,
    linecolor="#FFF4EC",
    cbar_kws={
        "label": "Relative QC signal"
    },
    ax=ax,
)

ax.set_xlabel("")
ax.set_ylabel("")

ax.set_title(
    "MiXCR QC fingerprint\n"
    "Numbers = original percentages",
    fontweight="bold"
)

plt.tight_layout()

st.pyplot(
    fig,
    width='stretch'
)

plt.close(fig)


# ---------------------------------------------------------
# QC DECISION
# ---------------------------------------------------------

html("""
<div class="insight-card">

    <div class="insight-title">
        Preprocessing decision
    </div>

    <div class="muted" style="margin-top:7px;">
        MiXCR reported 0% alignment loss from low sequence quality
        across all five samples. The raw paired-end reads were
        therefore retained without aggressive fastp trimming.
    </div>

</div>
""")

with st.expander(
    "View complete MiXCR QC table"
):
    st.dataframe(
        qc.round(2),
        width='stretch',
        hide_index=True,
    )