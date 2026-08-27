import sys
from pathlib import Path
from textwrap import dedent

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import streamlit as st


APP_DIR = Path(__file__).resolve().parents[1]

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from theme import apply_theme


st.set_page_config(
    page_title="TCRFlowX | Benchmark",
    page_icon="⚙️",
    layout="wide",
)

apply_theme()

ROOT = Path(__file__).resolve().parents[2]


def html(content):
    st.html(dedent(content).strip())


process = pd.read_csv(
    ROOT
    / "results/benchmark/process_summary.tsv",
    sep="\t",
)

task = pd.read_csv(
    ROOT
    / "results/benchmark/process_benchmark.tsv",
    sep="\t",
)


html("""
<div class="section-banner">
    <h3>Workflow Performance & Benchmarking</h3>
</div>
""")

st.caption(
    "Runtime, CPU utilization and memory footprint across "
    "the TCRFlowX Nextflow DSL2 workflow."
)


# ---------------------------------------------------------
# KPI
# ---------------------------------------------------------

mixcr = process.loc[
    process["process"] == "MIXCR"
].iloc[0]

c1, c2, c3, c4 = st.columns(4)

c1.metric(
    "Processes",
    f"{len(process)}"
)

c2.metric(
    "MiXCR tasks",
    f"{int(mixcr['tasks'])}"
)

c3.metric(
    "MiXCR mean CPU",
    f"{mixcr['mean_cpu_pct']:.0f}%"
)

c4.metric(
    "MiXCR max CPU",
    f"{mixcr['max_cpu_pct']:.0f}%"
)


# ---------------------------------------------------------
# CPU LOLLIPOP
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Process CPU profile</h3>
</div>
""")

plot_df = process.sort_values(
    "mean_cpu_pct"
)

fig, ax = plt.subplots(
    figsize=(9, 5)
)

fig.patch.set_facecolor(
    "#FFF9F4"
)

y = range(len(plot_df))

ax.hlines(
    y,
    0,
    plot_df["mean_cpu_pct"],
    linewidth=4,
    color="#F1B18C",
)

ax.scatter(
    plot_df["mean_cpu_pct"],
    y,
    s=180,
    color="#B8343E",
)

ax.set_yticks(list(y))

ax.set_yticklabels(
    plot_df["process"]
)

ax.set_xlabel(
    "Mean CPU utilization (%)"
)

ax.set_title(
    "Compute intensity by process",
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
# CPU × MEMORY SCATTER
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Runtime resource landscape</h3>
</div>
""")

task_plot = task.copy()

def parse_mb(value):

    if pd.isna(value):
        return None

    text = str(value).strip()

    if "GB" in text:
        return float(
            text.replace(
                "GB",
                ""
            )
        ) * 1024

    if "MB" in text:
        return float(
            text.replace(
                "MB",
                ""
            )
        )

    return None


task_plot["peak_rss_mb"] = (
    task_plot["peak_rss"]
    .apply(parse_mb)
)

task_plot["cpu"] = (
    task_plot["%cpu"]
    .astype(str)
    .str.replace(
        "%",
        "",
        regex=False
    )
    .astype(float)
)


fig = px.scatter(
    task_plot,
    x="cpu",
    y="peak_rss_mb",
    size="peak_rss_mb",
    color="process",
    hover_name="name",
    labels={
        "cpu":
            "CPU utilization (%)",

        "peak_rss_mb":
            "Peak RSS (MB)",
    },
    title=
        "CPU intensity versus memory footprint",
)


fig.update_layout(
    height=560,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="#FFF9F4",
)

st.plotly_chart(
    fig,
    width='stretch'
)


# ---------------------------------------------------------
# TASK TABLE
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Detailed task benchmark</h3>
</div>
""")

st.dataframe(
    task,
    width='stretch',
    hide_index=True,
)


html("""
<div class="insight-card">

    <div class="insight-title">
        Engineering conclusion
    </div>

    <div class="muted" style="margin-top:7px;">

        MiXCR is the principal computational bottleneck in TCRFlowX,
        while MultiQC, repertoire analysis and biological reporting
        have comparatively small resource footprints.

        This makes the current workflow practical on modest local
        hardware while preserving an obvious scaling path for HPC.

    </div>

</div>
""")