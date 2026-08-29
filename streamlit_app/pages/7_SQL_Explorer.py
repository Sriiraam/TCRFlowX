import sqlite3
import sys
from pathlib import Path
from textwrap import dedent

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================================================
# CONFIGURATION
# ============================================================

APP_DIR = Path(__file__).resolve().parents[1]
ROOT = APP_DIR.parent

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from theme import apply_theme

apply_theme()

DB_PATH = ROOT / "database" / "tcrflowx.db"


def html(content):
    st.html(dedent(content).strip())


@st.cache_resource
def get_connection():
    return sqlite3.connect(
        DB_PATH,
        check_same_thread=False
    )


def query_db(query, params=()):
    return pd.read_sql_query(
        query,
        get_connection(),
        params=params
    )


if not DB_PATH.exists():
    st.error(
        "TCRFlowX SQL database was not found. "
        "Run `python3 scripts/build_database.py`."
    )
    st.stop()


# ============================================================
# PAGE-SPECIFIC POLISH
# ============================================================

st.markdown(
    """
    <style>

    div[data-testid="stMetric"] {
        background: rgba(255,253,250,0.86);
        border: 1px solid #EED9CC;
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 5px 18px rgba(91,59,43,0.05);
    }

    div[data-testid="stMetricLabel"] {
        color: #806A63;
        font-weight: 650;
    }

    div[data-testid="stMetricValue"] {
        color: #352B2A;
        font-weight: 850;
    }

    div[data-testid="stDataFrame"] {
        border: 1px solid #EED9CC;
        border-radius: 16px;
        overflow: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HERO
# ============================================================

html("""
<div style="
    padding:46px 48px;
    border-radius:30px;
    background:
        radial-gradient(circle at 88% 16%,
        rgba(244,162,97,.28), transparent 28%),
        radial-gradient(circle at 72% 100%,
        rgba(42,157,143,.11), transparent 30%),
        linear-gradient(135deg,#FFF0E5 0%,#FFF9F4 56%,#FCE8DF 100%);
    border:1px solid #EFD7CA;
    box-shadow:0 18px 42px rgba(95,58,40,.08);
    margin-bottom:30px;
">

    <div style="
        color:#E76F51;
        font-weight:850;
        font-size:14px;
        letter-spacing:2.2px;
    ">
        TCRFLOWX • RELATIONAL IMMUNOGENOMICS
    </div>

    <div style="
        color:#302523;
        font-weight:900;
        font-size:60px;
        line-height:1.02;
        letter-spacing:-2.4px;
        margin-top:9px;
    ">
        SQL Repertoire Explorer
    </div>

    <div style="
        color:#705B55;
        font-size:19px;
        line-height:1.65;
        max-width:920px;
        margin-top:17px;
    ">
        A relational analytics layer connecting reconstructed TCRβ
        clonotypes, longitudinal immune dynamics, repertoire diversity
        and tumor–blood sharing.
    </div>

    <div style="
        display:flex;
        flex-wrap:wrap;
        gap:10px;
        margin-top:24px;
    ">

        <span style="
            background:#FFE0D1;
            color:#AE4B35;
            padding:7px 14px;
            border-radius:30px;
            font-weight:750;">
            SQLite
        </span>

        <span style="
            background:#DDF1EB;
            color:#23766B;
            padding:7px 14px;
            border-radius:30px;
            font-weight:750;">
            24K+ TRB clonotypes
        </span>

        <span style="
            background:#FAE7B8;
            color:#82601E;
            padding:7px 14px;
            border-radius:30px;
            font-weight:750;">
            Longitudinal disease
        </span>

        <span style="
            background:#F3DDE4;
            color:#923E57;
            padding:7px 14px;
            border-radius:30px;
            font-weight:750;">
            Tumor–immune analytics
        </span>

    </div>
</div>
""")


# ============================================================
# DATABASE KPIs
# ============================================================

sample_count = int(
    query_db("SELECT COUNT(*) n FROM samples").iloc[0]["n"]
)

clone_count = int(
    query_db("SELECT COUNT(*) n FROM clonotypes").iloc[0]["n"]
)

long_count = int(
    query_db(
        "SELECT COUNT(*) n FROM pbmc_longitudinal"
    ).iloc[0]["n"]
)

persistent_count = int(
    query_db("""
        SELECT COUNT(*) n
        FROM pbmc_longitudinal
        WHERE detected_timepoints = 3
    """).iloc[0]["n"]
)


c1, c2, c3, c4 = st.columns(4)

c1.metric("Clinical Samples", f"{sample_count:,}")
c2.metric("TRB Clonotypes", f"{clone_count:,}")
c3.metric("Longitudinal Records", f"{long_count:,}")
c4.metric("Persistent PBMC Clones", f"{persistent_count:,}")

st.caption(
    "All statistics are queried live from the SQLite analytical database."
)


# ============================================================
# SECTION 01 — CLONOTYPE EXPLORER
# ============================================================

html("""
<div style="margin-top:48px;margin-bottom:15px;">

    <div style="
        color:#E76F51;
        font-size:13px;
        font-weight:850;
        letter-spacing:1.8px;">
        01 • CLONOTYPE ARCHITECTURE
    </div>

    <div style="
        color:#352B2A;
        font-size:35px;
        font-weight:880;
        margin-top:4px;">
        Who dominates the repertoire?
    </div>

    <div style="
        color:#78645F;
        font-size:16px;
        margin-top:6px;">
        Explore highly abundant TCRβ clones reconstructed within each
        longitudinal blood or tumor sample.
    </div>

</div>
""")


samples = query_db("""
SELECT sample_id
FROM samples
ORDER BY
CASE sample_id
    WHEN 'PBMC_PRE' THEN 1
    WHEN 'TUMOR_PRE' THEN 2
    WHEN 'PBMC_RELAPSE' THEN 3
    WHEN 'PBMC_PROGRESSION' THEN 4
    WHEN 'TUMOR_PROGRESSION' THEN 5
END
""")["sample_id"].tolist()


a, b = st.columns([1, 1])

with a:
    selected_sample = st.selectbox(
        "Sample",
        samples
    )

with b:
    minimum_frequency = st.slider(
        "Minimum clone frequency (%)",
        min_value=0.0,
        max_value=10.0,
        value=0.1,
        step=0.1
    )


TOP_QUERY = """
SELECT
    cdr3_aa,
    clone_count,
    clone_fraction * 100 AS frequency_pct,
    v_gene,
    j_gene
FROM clonotypes
WHERE sample_id = ?
  AND clone_fraction * 100 >= ?
ORDER BY clone_fraction DESC
LIMIT 15
"""

top = query_db(
    TOP_QUERY,
    (selected_sample, minimum_frequency)
)


# ---------------- LOLLIPOP ----------------

if not top.empty:

    plot_df = top.sort_values("frequency_pct")

    fig = go.Figure()

    for _, r in plot_df.iterrows():

        fig.add_trace(
            go.Scatter(
                x=[0, r["frequency_pct"]],
                y=[r["cdr3_aa"], r["cdr3_aa"]],
                mode="lines",
                line=dict(
                    width=3,
                    color="#E7C0AE"
                ),
                hoverinfo="skip",
                showlegend=False
            )
        )

    fig.add_trace(
        go.Scatter(
            x=plot_df["frequency_pct"],
            y=plot_df["cdr3_aa"],
            mode="markers",
            marker=dict(
                size=16,
                color=plot_df["frequency_pct"],
                colorscale=[
                    [0, "#F4A261"],
                    [0.5, "#E76F51"],
                    [1, "#9D3B53"]
                ],
                colorbar=dict(
                    title="Frequency"
                )
            ),
            customdata=plot_df[
                ["clone_count", "v_gene", "j_gene"]
            ],
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Frequency: %{x:.3f}%<br>"
                "Reads: %{customdata[0]:,.0f}<br>"
                "V gene: %{customdata[1]}<br>"
                "J gene: %{customdata[2]}"
                "<extra></extra>"
            ),
            showlegend=False
        )
    )

    fig.update_layout(
        title=f"Dominant clonotypes • {selected_sample}",
        height=560,
        xaxis_title="Repertoire frequency (%)",
        yaxis_title="",
        plot_bgcolor="#FFFDFC",
        paper_bgcolor="#FFFDFC",
        margin=dict(l=30, r=30, t=75, b=50)
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


st.caption(
    "Lollipop encoding highlights individual clonotypes rather than "
    "treating CDR3 sequences as ordinary categorical bars."
)


show_table = st.toggle(
    "Show underlying clonotype records",
    value=False
)

if show_table:
    table = top.copy()
    table["frequency_pct"] = (
        table["frequency_pct"].round(3)
    )

    st.dataframe(
        table,
        width="stretch",
        hide_index=True
    )


# ============================================================
# SECTION 02 — REPERTOIRE STATE
# ============================================================

html("""
<div style="margin-top:52px;margin-bottom:16px;">

    <div style="
        color:#2A9D8F;
        font-size:13px;
        font-weight:850;
        letter-spacing:1.8px;">
        02 • IMMUNE REPERTOIRE STATE
    </div>

    <div style="
        color:#352B2A;
        font-size:35px;
        font-weight:880;
        margin-top:4px;">
        Diversity, clonality & dominance
    </div>

    <div style="
        color:#78645F;
        font-size:16px;
        margin-top:6px;">
        Compare the global immune-repertoire state across blood,
        tumor and clinical timepoints.
    </div>

</div>
""")


DIVERSITY_QUERY = """
SELECT
    s.sample_id,
    s.tissue,
    s.timepoint,
    s.clinical_stage,
    d.productive_richness,
    d.shannon,
    d.clonality,
    d.top10_fraction * 100 AS top10_pct
FROM samples s
JOIN diversity_metrics d
    ON s.sample_id = d.sample_id
"""

diversity = query_db(DIVERSITY_QUERY)


# ---------------- BUBBLE STATE SPACE ----------------

fig = px.scatter(
    diversity,
    x="productive_richness",
    y="clonality",
    size="top10_pct",
    color="tissue",
    text="sample_id",
    hover_data={
        "shannon": ":.3f",
        "top10_pct": ":.2f",
        "clinical_stage": True
    },
    color_discrete_map={
        "PBMC": "#E76F51",
        "Tumor": "#2A9D8F"
    },
    labels={
        "productive_richness": "Productive richness",
        "clonality": "Clonality",
        "top10_pct": "Top-10 dominance (%)"
    }
)

fig.update_traces(
    textposition="top center",
    marker=dict(
        line=dict(
            width=1.2,
            color="#FFFDFC"
        )
    )
)

fig.update_layout(
    title="Repertoire State Space",
    height=540,
    plot_bgcolor="#FFFDFC",
    paper_bgcolor="#FFFDFC",
    legend_title="Compartment"
)

st.plotly_chart(
    fig,
    width="stretch"
)


st.caption(
    "Position represents richness and clonality; bubble size captures "
    "dominance of the top ten clones. PBMC relapse shows marked repertoire "
    "contraction with increased clonal concentration."
)


# ============================================================
# SECTION 03 — SIMILARITY HEATMAP
# ============================================================

html("""
<div style="margin-top:52px;margin-bottom:16px;">

    <div style="
        color:#B15F81;
        font-size:13px;
        font-weight:850;
        letter-spacing:1.8px;">
        03 • REPERTOIRE RELATEDNESS
    </div>

    <div style="
        color:#352B2A;
        font-size:35px;
        font-weight:880;
        margin-top:4px;">
        Cross-sample similarity map
    </div>

    <div style="
        color:#78645F;
        font-size:16px;
        margin-top:6px;">
        Pairwise Jaccard similarity reveals how strongly clonotype
        repertoires are shared across tissues and disease stages.
    </div>

</div>
""")


jaccard = query_db("""
SELECT
    sample_a,
    sample_b,
    jaccard
FROM pairwise_jaccard
""")


matrix = jaccard.pivot(
    index="sample_a",
    columns="sample_b",
    values="jaccard"
)


desired_order = [
    "PBMC_PRE",
    "TUMOR_PRE",
    "PBMC_RELAPSE",
    "PBMC_PROGRESSION",
    "TUMOR_PROGRESSION"
]

matrix = matrix.reindex(
    index=desired_order,
    columns=desired_order
)


fig = go.Figure(
    data=go.Heatmap(
        z=matrix.values,
        x=matrix.columns,
        y=matrix.index,
        text=np.round(matrix.values, 3),
        texttemplate="%{text}",
        colorscale=[
            [0.00, "#FFF5EE"],
            [0.15, "#F4A261"],
            [0.45, "#E76F51"],
            [1.00, "#8D3851"]
        ],
        zmin=0,
        zmax=1,
        colorbar=dict(
            title="Jaccard"
        ),
        hovertemplate=(
            "%{y}<br>%{x}<br>"
            "Jaccard: %{z:.3f}"
            "<extra></extra>"
        )
    )
)

fig.update_layout(
    title="Pairwise TCRβ Repertoire Similarity",
    height=530,
    plot_bgcolor="#FFFDFC",
    paper_bgcolor="#FFFDFC"
)

st.plotly_chart(
    fig,
    width="stretch"
)


st.caption(
    "The diagonal represents each repertoire compared with itself. "
    "Off-diagonal values quantify biological sharing across timepoints "
    "and tissue compartments."
)


# ============================================================
# SECTION 04 — LONGITUDINAL DYNAMICS
# ============================================================

html("""
<div style="margin-top:52px;margin-bottom:16px;">

    <div style="
        color:#9D3B53;
        font-size:13px;
        font-weight:850;
        letter-spacing:1.8px;">
        04 • LONGITUDINAL CLONE DYNAMICS
    </div>

    <div style="
        color:#352B2A;
        font-size:35px;
        font-weight:880;
        margin-top:4px;">
        Follow clones through disease
    </div>

    <div style="
        color:#78645F;
        font-size:16px;
        margin-top:6px;">
        Trace individual circulating TCRβ clonotypes from pre-treatment
        through relapse and progressive disease.
    </div>

</div>
""")


population = st.selectbox(
    "Clone behavior",
    [
        "Persistent",
        "Progression-expanded",
        "Relapse-emergent"
    ]
)


if population == "Persistent":

    LONG_QUERY = """
    SELECT
        cdr3_aa,
        pbmc_pre * 100 AS pre,
        pbmc_relapse * 100 AS relapse,
        pbmc_progression * 100 AS progression
    FROM pbmc_longitudinal
    WHERE detected_timepoints = 3
    ORDER BY max_fraction DESC
    LIMIT 10
    """

elif population == "Progression-expanded":

    LONG_QUERY = """
    SELECT
        cdr3_aa,
        pbmc_pre * 100 AS pre,
        pbmc_relapse * 100 AS relapse,
        pbmc_progression * 100 AS progression
    FROM pbmc_longitudinal
    WHERE pbmc_pre > 0
      AND pbmc_progression > pbmc_pre
    ORDER BY
        (pbmc_progression - pbmc_pre) DESC
    LIMIT 10
    """

else:

    LONG_QUERY = """
    SELECT
        cdr3_aa,
        pbmc_pre * 100 AS pre,
        pbmc_relapse * 100 AS relapse,
        pbmc_progression * 100 AS progression
    FROM pbmc_longitudinal
    WHERE pbmc_pre = 0
      AND pbmc_relapse > 0
    ORDER BY pbmc_relapse DESC
    LIMIT 10
    """


longitudinal = query_db(LONG_QUERY)


if not longitudinal.empty:

    long_plot = longitudinal.melt(
        id_vars="cdr3_aa",
        var_name="stage",
        value_name="frequency"
    )

    stage_map = {
        "pre": 0,
        "relapse": 1,
        "progression": 2
    }

    long_plot["stage_order"] = (
        long_plot["stage"].map(stage_map)
    )


    fig = px.line(
        long_plot,
        x="stage_order",
        y="frequency",
        color="cdr3_aa",
        markers=True,
        labels={
            "stage_order": "",
            "frequency": "Clone frequency (%)"
        }
    )

    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=9)
    )

    fig.update_xaxes(
        tickmode="array",
        tickvals=[0, 1, 2],
        ticktext=[
            "Pre-treatment",
            "Relapse",
            "Progression"
        ]
    )

    fig.update_layout(
        title=f"{population} TCRβ Clone Trajectories",
        height=590,
        plot_bgcolor="#FFFDFC",
        paper_bgcolor="#FFFDFC",
        legend_title="CDR3 clonotype"
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


st.caption(
    "Trajectory geometry makes expansion, contraction and persistence "
    "visible across the clinical timeline."
)


# ============================================================
# SECTION 05 — TUMOR / PBMC
# ============================================================

html("""
<div style="margin-top:52px;margin-bottom:16px;">

    <div style="
        color:#F08C46;
        font-size:13px;
        font-weight:850;
        letter-spacing:1.8px;">
        05 • BLOOD–TUMOR INTERFACE
    </div>

    <div style="
        color:#352B2A;
        font-size:35px;
        font-weight:880;
        margin-top:4px;">
        Compartment divergence
    </div>

    <div style="
        color:#78645F;
        font-size:16px;
        margin-top:6px;">
        Quantify how strongly circulating and tumor-associated
        repertoires remain connected as disease progresses.
    </div>

</div>
""")


overlap = query_db("""
SELECT
    stage,
    pbmc_clonotypes,
    tumor_clonotypes,
    shared_clonotypes,
    jaccard
FROM tumor_pbmc_overlap
ORDER BY
CASE stage
    WHEN 'PRE' THEN 1
    WHEN 'PROGRESSION' THEN 2
END
""")


pre = overlap.iloc[0]
prog = overlap.iloc[1]


c1, c2, c3 = st.columns(3)

c1.metric(
    "PRE shared clones",
    f"{int(pre['shared_clonotypes']):,}"
)

c2.metric(
    "Progression shared clones",
    f"{int(prog['shared_clonotypes']):,}",
    f"{int(prog['shared_clonotypes'] - pre['shared_clonotypes']):,}"
)

jaccard_change = (
    (prog["jaccard"] - pre["jaccard"])
    / pre["jaccard"]
) * 100

c3.metric(
    "Jaccard change",
    f"{jaccard_change:.1f}%"
)


# ---------------- DUMBBELL ----------------

fig = go.Figure()


fig.add_trace(
    go.Scatter(
        x=[
            pre["jaccard"],
            prog["jaccard"]
        ],
        y=[
            "Tumor ↔ PBMC",
            "Tumor ↔ PBMC"
        ],
        mode="lines",
        line=dict(
            width=8,
            color="#EED0BE"
        ),
        hoverinfo="skip",
        showlegend=False
    )
)


fig.add_trace(
    go.Scatter(
        x=[pre["jaccard"]],
        y=["Tumor ↔ PBMC"],
        mode="markers+text",
        marker=dict(
            size=30,
            color="#F4A261"
        ),
        text=["PRE"],
        textposition="top center",
        name="Pre-treatment",
        hovertemplate=(
            f"PRE<br>"
            f"Jaccard: {pre['jaccard']:.3f}<br>"
            f"Shared clones: {int(pre['shared_clonotypes']):,}"
            "<extra></extra>"
        )
    )
)


fig.add_trace(
    go.Scatter(
        x=[prog["jaccard"]],
        y=["Tumor ↔ PBMC"],
        mode="markers+text",
        marker=dict(
            size=30,
            color="#9D3B53"
        ),
        text=["PROGRESSION"],
        textposition="bottom center",
        name="Progression",
        hovertemplate=(
            f"PROGRESSION<br>"
            f"Jaccard: {prog['jaccard']:.3f}<br>"
            f"Shared clones: {int(prog['shared_clonotypes']):,}"
            "<extra></extra>"
        )
    )
)


fig.update_layout(
    title="Tumor–PBMC Repertoire Similarity",
    xaxis_title="Jaccard similarity",
    height=380,
    plot_bgcolor="#FFFDFC",
    paper_bgcolor="#FFFDFC",
    xaxis=dict(
        range=[0, 0.16]
    ),
    showlegend=False
)

st.plotly_chart(
    fig,
    width="stretch"
)


html(f"""
<div style="
    padding:20px 22px;
    background:#FFF1E8;
    border-left:5px solid #E76F51;
    border-radius:14px;
    color:#594743;
    font-size:16px;
    line-height:1.65;
">

    Blood–tumor Jaccard similarity decreased from
    <b>{pre['jaccard']:.3f}</b> to
    <b>{prog['jaccard']:.3f}</b>, while shared clonotypes declined
    from <b>{int(pre['shared_clonotypes']):,}</b> to
    <b>{int(prog['shared_clonotypes']):,}</b>.

    This indicates stronger compartmental repertoire divergence
    by progression.

</div>
""")


# ============================================================
# SECTION 06 — CLONE FATE
# ============================================================

html("""
<div style="margin-top:52px;margin-bottom:16px;">

    <div style="
        color:#7655A6;
        font-size:13px;
        font-weight:850;
        letter-spacing:1.8px;">
        06 • CLONE FATE
    </div>

    <div style="
        color:#352B2A;
        font-size:35px;
        font-weight:880;
        margin-top:4px;">
        Longitudinal fate composition
    </div>

    <div style="
        color:#78645F;
        font-size:16px;
        margin-top:6px;">
        SQL classifies thousands of clonotypes according to
        persistence, emergence, loss or variable temporal behavior.
    </div>

</div>
""")


classification = query_db("""
WITH clone_dynamics AS (

    SELECT
        cdr3_aa,

        CASE
            WHEN detected_timepoints = 3
                THEN 'Persistent'

            WHEN pbmc_pre = 0
                 AND pbmc_relapse > 0
                THEN 'Relapse-emergent'

            WHEN pbmc_pre > 0
                 AND pbmc_progression = 0
                THEN 'Lost'

            ELSE 'Variable'

        END AS clone_status

    FROM pbmc_longitudinal
)

SELECT
    clone_status,
    COUNT(*) AS clonotypes

FROM clone_dynamics

GROUP BY clone_status
ORDER BY clonotypes DESC
""")


color_map = {
    "Variable": "#F4A261",
    "Lost": "#9D3B53",
    "Relapse-emergent": "#E76F51",
    "Persistent": "#2A9D8F"
}


fig = go.Figure(
    go.Pie(
        labels=classification["clone_status"],
        values=classification["clonotypes"],
        hole=0.68,
        marker=dict(
            colors=[
                color_map.get(x, "#BBBBBB")
                for x in classification["clone_status"]
            ]
        ),
        textinfo="label+percent",
        hovertemplate=(
            "<b>%{label}</b><br>"
            "%{value:,} clonotypes<br>"
            "%{percent}"
            "<extra></extra>"
        )
    )
)


fig.update_layout(
    title="PBMC Longitudinal Clone Fate",
    height=500,
    paper_bgcolor="#FFFDFC",
    annotations=[
        dict(
            text=(
                f"<b>{classification['clonotypes'].sum():,}</b>"
                "<br>clonotypes"
            ),
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=18)
        )
    ]
)

st.plotly_chart(
    fig,
    width="stretch"
)


# ============================================================
# SQL IMPLEMENTATION — COMPACT ONLY
# ============================================================

html("""
<div style="
    margin-top:55px;
    padding:28px 30px;
    border-radius:22px;
    background:linear-gradient(135deg,#FFF0E7,#FFF9F4);
    border:1px solid #EDD4C5;
">

    <div style="
        color:#E76F51;
        font-size:13px;
        font-weight:850;
        letter-spacing:1.7px;">
        SQL IMPLEMENTATION
    </div>

    <div style="
        color:#352B2A;
        font-size:27px;
        font-weight:850;
        margin-top:4px;">
        Relational analytics underneath the dashboard
    </div>

    <div style="
        color:#705C57;
        font-size:16px;
        line-height:1.75;
        margin-top:12px;">

        The visual layer is powered by parameterized SQLite queries,
        relational joins, aggregations, CTEs and CASE-based
        longitudinal classification.

        <br><br>

        <b>Implementation files</b><br>
        database/schema.sql<br>
        database/analysis_queries.sql<br>
        scripts/build_database.py<br>
        database/tcrflowx.db

    </div>

</div>
""")


concepts = pd.DataFrame({
    "SQL capability": [
        "Relational schema",
        "JOIN",
        "WHERE filtering",
        "GROUP BY / aggregation",
        "Parameterized queries",
        "CTE",
        "CASE classification"
    ],

    "TCRFlowX application": [
        "Samples, clonotypes, diversity, QC and overlap",
        "Sample metadata × repertoire metrics",
        "Sample-specific clonotype exploration",
        "Clone-fate and tissue summaries",
        "Interactive dashboard filtering",
        "Longitudinal clone-state derivation",
        "Persistent / emergent / lost classification"
    ]
})


with st.expander(
    "View SQL capabilities demonstrated",
    expanded=False
):
    st.dataframe(
        concepts,
        width="stretch",
        hide_index=True
    )