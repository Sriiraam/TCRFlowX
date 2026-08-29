from pathlib import Path
from data_paths import RESULTS_ROOT
from textwrap import dedent

import pandas as pd
import streamlit as st

from theme import apply_theme


# Project root: ~/TCRFlowX
ROOT = Path(__file__).resolve().parents[1]


st.set_page_config(
    page_title="TCRFlowX",
    page_icon="🧬",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_theme()


def html(content):
    st.html(
        dedent(content).strip()
    )
# -------------------------------------------------------
# LOAD DATA
# -------------------------------------------------------

div = pd.read_csv(
    RESULTS_ROOT / "repertoire/tables/diversity_clonality.tsv",
    sep="\t",
)

summary = pd.read_csv(
    RESULTS_ROOT / "repertoire/biological_summary.tsv",
    sep="\t",
)

tracking = pd.read_csv(
    RESULTS_ROOT / "repertoire/tables/pbmc_longitudinal_clonotypes.tsv",
    sep="\t",
)

benchmark = pd.read_csv(
    ROOT
    / "results/benchmark/PBMC_PRE/PBMC_PRE_benchmark_summary.tsv",
    sep="\t",
)

persistent = int(
    (tracking["detected_timepoints"] == 3).sum()
)

rho = benchmark.loc[
    benchmark["metric"] == "spearman_rho",
    "value",
].iloc[0]

jaccard = benchmark.loc[
    benchmark["metric"] == "cdr3_jaccard",
    "value",
].iloc[0]


# -------------------------------------------------------
# HERO
# -------------------------------------------------------

html("""
<div class="tcr-hero">

    <div class="hero-eyebrow">
        CANCER IMMUNOGENOMICS • TCRβ REPERTOIRE INTELLIGENCE
    </div>

    <h1>🧬 TCRFlowX</h1>

    <p>
        Longitudinal T-cell receptor repertoire profiling across
        PD-1 blockade, relapse and disease progression.
    </p>

</div>
""")


# -------------------------------------------------------
# KPI CARDS
# -------------------------------------------------------

cols = st.columns(4)

cards = [
    (
        "Samples analyzed",
        "5",
        "PBMC + lymphoid tumor tissue",
    ),
    (
        "Persistent clones",
        f"{persistent:,}",
        "Detected across all 3 PBMC timepoints",
    ),
    (
        "Author concordance",
        f"{jaccard * 100:.1f}%",
        "Productive CDR3 Jaccard",
    ),
    (
        "Frequency correlation",
        f"{rho:.3f}",
        "Spearman vs author processed data",
    ),
]

for col, (label, value, note) in zip(cols, cards):
    with col:

        html(f"""
        <div class="kpi-card">

            <div class="kpi-label">
                {label}
            </div>

            <div class="kpi-value">
                {value}
            </div>

            <div class="kpi-note">
                {note}
            </div>

        </div>
        """)


# -------------------------------------------------------
# CLINICAL TRAJECTORY
# -------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Clinical trajectory</h3>
</div>
""")


html("""
<div class="content-card">

    <div style="
        display:grid;
        grid-template-columns:1fr 1fr 1fr;
        gap:28px;
        text-align:center;
    ">

        <div>

            <div style="
                font-size:0.76rem;
                font-weight:850;
                letter-spacing:0.10em;
                color:#B8343E;
            ">
                TIMEPOINT 1
            </div>

            <div style="
                font-size:1.35rem;
                font-weight:850;
                margin-top:8px;
                color:#68222C;
            ">
                PRE-TREATMENT
            </div>

            <div style="
                font-size:1rem;
                font-weight:750;
                margin-top:12px;
                color:#D65A45;
            ">
                PBMC + Tumor
            </div>

            <div class="muted" style="margin-top:6px;">
                Before PD-1 inhibitor therapy
            </div>

        </div>


        <div>

            <div style="
                font-size:0.76rem;
                font-weight:850;
                letter-spacing:0.10em;
                color:#E17E35;
            ">
                TIMEPOINT 4
            </div>

            <div style="
                font-size:1.35rem;
                font-weight:850;
                margin-top:8px;
                color:#68222C;
            ">
                RELAPSE
            </div>

            <div style="
                font-size:1rem;
                font-weight:750;
                margin-top:12px;
                color:#E17E35;
            ">
                PBMC
            </div>

            <div class="muted" style="margin-top:6px;">
                Off PD-1 inhibitor
            </div>

        </div>


        <div>

            <div style="
                font-size:0.76rem;
                font-weight:850;
                letter-spacing:0.10em;
                color:#C93E55;
            ">
                TIMEPOINT 6
            </div>

            <div style="
                font-size:1.35rem;
                font-weight:850;
                margin-top:8px;
                color:#68222C;
            ">
                PROGRESSION
            </div>

            <div style="
                font-size:1rem;
                font-weight:750;
                margin-top:12px;
                color:#C93E55;
            ">
                PBMC + Tumor
            </div>

            <div class="muted" style="margin-top:6px;">
                Progressive disease on PD-1i
            </div>

        </div>

    </div>


    <div style="
        margin-top:30px;
        display:flex;
        align-items:center;
        gap:10px;
    ">

        <div style="
            width:15px;
            height:15px;
            border-radius:50%;
            background:#B8343E;
        ">
        </div>

        <div style="
            height:4px;
            flex:1;
            border-radius:5px;
            background:linear-gradient(
                90deg,
                #B8343E,
                #E17E35
            );
        ">
        </div>

        <div style="
            width:15px;
            height:15px;
            border-radius:50%;
            background:#E17E35;
        ">
        </div>

        <div style="
            height:4px;
            flex:1;
            border-radius:5px;
            background:linear-gradient(
                90deg,
                #E17E35,
                #C93E55
            );
        ">
        </div>

        <div style="
            width:15px;
            height:15px;
            border-radius:50%;
            background:#C93E55;
        ">
        </div>

    </div>

</div>
""")


# -------------------------------------------------------
# BIOLOGICAL FINDINGS
# -------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Executive biological findings</h3>
</div>
""")


for _, row in summary.iterrows():

    html(f"""
    <div class="insight-card">

        <div class="insight-title">
            {row["finding"]}
        </div>

        <div class="muted" style="margin-top:7px;">
            {row["interpretation"]}
        </div>

    </div>
    """)


# -------------------------------------------------------
# REPERTOIRE SNAPSHOT
# -------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Repertoire snapshot</h3>
</div>
""")


pre = div.loc[
    div["sample"] == "PBMC_PRE"
].iloc[0]

relapse = div.loc[
    div["sample"] == "PBMC_RELAPSE"
].iloc[0]

progression = div.loc[
    div["sample"] == "PBMC_PROGRESSION"
].iloc[0]


c1, c2, c3 = st.columns(3)


with c1:

    html(f"""
    <div class="content-card">

        <div class="kpi-label">
            PRE-TREATMENT PBMC
        </div>

        <div style="
            font-size:1.9rem;
            font-weight:850;
            color:#B8343E;
            margin-top:10px;
        ">
            {int(pre["productive_richness"]):,}
        </div>

        <div class="muted">
            productive clonotypes
        </div>

        <div style="
            margin-top:16px;
            font-size:.92rem;
            color:#654B49;
            line-height:1.7;
        ">
            Shannon diversity:
            <b>{pre["shannon"]:.3f}</b>
            <br>

            Clonality:
            <b>{pre["clonality"]:.3f}</b>
        </div>

    </div>
    """)


with c2:

    html(f"""
    <div class="content-card">

        <div class="kpi-label">
            RELAPSE PBMC
        </div>

        <div style="
            font-size:1.9rem;
            font-weight:850;
            color:#E17E35;
            margin-top:10px;
        ">
            {int(relapse["productive_richness"]):,}
        </div>

        <div class="muted">
            productive clonotypes
        </div>

        <div style="
            margin-top:16px;
            font-size:.92rem;
            color:#654B49;
            line-height:1.7;
        ">
            Shannon diversity:
            <b>{relapse["shannon"]:.3f}</b>
            <br>

            Clonality:
            <b>{relapse["clonality"]:.3f}</b>
        </div>

    </div>
    """)


with c3:

    html(f"""
    <div class="content-card">

        <div class="kpi-label">
            PROGRESSION PBMC
        </div>

        <div style="
            font-size:1.9rem;
            font-weight:850;
            color:#C93E55;
            margin-top:10px;
        ">
            {int(progression["productive_richness"]):,}
        </div>

        <div class="muted">
            productive clonotypes
        </div>

        <div style="
            margin-top:16px;
            font-size:.92rem;
            color:#654B49;
            line-height:1.7;
        ">
            Shannon diversity:
            <b>{progression["shannon"]:.3f}</b>
            <br>

            Clonality:
            <b>{progression["clonality"]:.3f}</b>
        </div>

    </div>
    """)


# -------------------------------------------------------
# PIPELINE ARCHITECTURE
# -------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Analytical architecture</h3>
</div>
""")


html("""
<div class="content-card">

    <div style="
        display:grid;
        grid-template-columns:
            1fr auto 1fr auto 1fr auto 1fr;
        align-items:center;
        gap:14px;
        text-align:center;
    ">

        <div>

            <div style="
                font-size:2rem;
                margin-bottom:6px;
            ">
                🧬
            </div>

            <div style="
                font-weight:850;
                color:#8E2430;
            ">
                FASTQ
            </div>

            <div class="muted">
                Raw paired reads
            </div>

        </div>


        <div style="
            color:#E17E35;
            font-size:1.5rem;
            font-weight:850;
        ">
            →
        </div>


        <div>

            <div style="
                font-size:2rem;
                margin-bottom:6px;
            ">
                ✓
            </div>

            <div style="
                font-weight:850;
                color:#B8343E;
            ">
                QC
            </div>

            <div class="muted">
                FastQC + MultiQC
            </div>

        </div>


        <div style="
            color:#E17E35;
            font-size:1.5rem;
            font-weight:850;
        ">
            →
        </div>


        <div>

            <div style="
                font-size:2rem;
                margin-bottom:6px;
            ">
                🔬
            </div>

            <div style="
                font-weight:850;
                color:#D65A45;
            ">
                MiXCR
            </div>

            <div class="muted">
                TRB reconstruction
            </div>

        </div>


        <div style="
            color:#E17E35;
            font-size:1.5rem;
            font-weight:850;
        ">
            →
        </div>


        <div>

            <div style="
                font-size:2rem;
                margin-bottom:6px;
            ">
                📊
            </div>

            <div style="
                font-weight:850;
                color:#C93E55;
            ">
                Repertoire
            </div>

            <div class="muted">
                Diversity • V/J • overlap
            </div>

        </div>

    </div>


    <div style="
        text-align:center;
        margin-top:28px;
        font-size:1.4rem;
        color:#E17E35;
        font-weight:850;
    ">
        ↓
    </div>


    <div style="
        text-align:center;
        margin-top:10px;
    ">

        <span style="
            color:#8E2430;
            font-weight:850;
        ">
            Longitudinal immune dynamics
        </span>

        <span class="muted">
            &nbsp;→&nbsp;
            biological interpretation
            &nbsp;→&nbsp;
            interactive reporting
        </span>

    </div>

</div>
""")


# -------------------------------------------------------
# FOOTER
# -------------------------------------------------------

html("""
<div style="
    margin-top:34px;
    padding:15px 18px;
    border-radius:14px;
    background:linear-gradient(
        90deg,
        #FFEAE0,
        #FFF3DF
    );
    border:1px solid #EFD4C4;
    color:#805E58;
    font-size:.83rem;
">

    <b style="color:#8E2430;">
        TCRFlowX
    </b>

    &nbsp;•&nbsp;
    Human TCRβ repertoire sequencing
    &nbsp;•&nbsp;
    LymphoTrack TRB
    &nbsp;•&nbsp;
    Classical Hodgkin lymphoma
    &nbsp;•&nbsp;
    PD-1 blockade

</div>
""")