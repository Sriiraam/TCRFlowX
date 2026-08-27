import sys
from pathlib import Path
from textwrap import dedent

import streamlit as st


# ---------------------------------------------------------
# APP / THEME SETUP
# ---------------------------------------------------------

APP_DIR = Path(__file__).resolve().parents[1]

if str(APP_DIR) not in sys.path:
    sys.path.insert(0, str(APP_DIR))

from theme import apply_theme


st.set_page_config(
    page_title="TCRFlowX | Reports",
    page_icon="📥",
    layout="wide",
)

apply_theme()

ROOT = Path(__file__).resolve().parents[2]


def html(content):
    st.html(dedent(content).strip())


# ---------------------------------------------------------
# DOWNLOAD HELPER
# ---------------------------------------------------------

def download_file(label, path, mime):

    path = Path(path)

    if not path.exists():
        st.warning(f"Missing: {path.name}")
        return

    unique_key = (
        "download_"
        + str(path)
        .replace("/", "_")
        .replace("\\", "_")
        .replace(".", "_")
        .replace(" ", "_")
    )

    st.download_button(
        label=label,
        data=path.read_bytes(),
        file_name=path.name,
        mime=mime,
        width='stretch',
        key=unique_key,
    )


# ---------------------------------------------------------
# PAGE HEADER
# ---------------------------------------------------------

html("""
<div class="section-banner">
    <h3>Reports, Results & Downloads</h3>
</div>
""")

st.caption(
    "Review and download TCRFlowX quality-control, repertoire, "
    "biological interpretation, benchmarking and workflow reports."
)


# =========================================================
# 1. SEQUENCING QC
# =========================================================

html("""
<div class="section-banner">
    <h3>Sequencing QC Reports</h3>
</div>
""")

multiqc = (
    ROOT
    / "results"
    / "qc"
    / "multiqc_raw"
    / "multiqc_report.html"
)

mixcr_qc = (
    ROOT
    / "results"
    / "mixcr"
    / "mixcr_qc_summary.tsv"
)

c1, c2 = st.columns(2)

with c1:
    download_file(
        "⬇ Download MultiQC HTML Report",
        multiqc,
        "text/html",
    )

with c2:
    download_file(
        "⬇ Download MiXCR QC Summary",
        mixcr_qc,
        "text/tab-separated-values",
    )


# =========================================================
# 2. BIOLOGICAL INTERPRETATION
# =========================================================

html("""
<div class="section-banner">
    <h3>Biological Interpretation</h3>
</div>
""")

bio_md = (
    ROOT
    / "results"
    / "repertoire"
    / "biological_interpretation.md"
)

bio_summary = (
    ROOT
    / "results"
    / "repertoire"
    / "biological_summary.tsv"
)

persistent = (
    ROOT
    / "results"
    / "repertoire"
    / "top_persistent_clonotypes.tsv"
)

c1, c2, c3 = st.columns(3)

with c1:
    download_file(
        "⬇ Biological Interpretation",
        bio_md,
        "text/markdown",
    )

with c2:
    download_file(
        "⬇ Biological Summary TSV",
        bio_summary,
        "text/tab-separated-values",
    )

with c3:
    download_file(
        "⬇ Persistent Clonotypes",
        persistent,
        "text/tab-separated-values",
    )


# ---------------------------------------------------------
# INTERPRETATION PREVIEW
# ---------------------------------------------------------

if bio_md.exists():

    with st.expander(
        "📖 Read Biological Interpretation",
        expanded=False,
    ):

        st.markdown(
            bio_md.read_text(
                encoding="utf-8",
                errors="ignore",
            )
        )


# =========================================================
# 3. REPERTOIRE TABLES
# =========================================================

html("""
<div class="section-banner">
    <h3>Repertoire Analysis Tables</h3>
</div>
""")

tables_dir = (
    ROOT
    / "results"
    / "repertoire"
    / "tables"
)

table_files = [
    (
        "Diversity & Clonality",
        "diversity_clonality.tsv",
    ),
    (
        "Top 20 Clonotypes",
        "top20_clonotypes.tsv",
    ),
    (
        "TRBV Usage",
        "trbv_usage.tsv",
    ),
    (
        "TRBJ Usage",
        "trbj_usage.tsv",
    ),
    (
        "Pairwise Jaccard",
        "pairwise_jaccard.tsv",
    ),
    (
        "PBMC Longitudinal Clonotypes",
        "pbmc_longitudinal_clonotypes.tsv",
    ),
    (
        "Tumor Longitudinal Clonotypes",
        "tumor_longitudinal_clonotypes.tsv",
    ),
    (
        "Tumor–PBMC Overlap",
        "tumor_pbmc_overlap.tsv",
    ),
]

for i in range(0, len(table_files), 2):

    cols = st.columns(2)

    for col, item in zip(
        cols,
        table_files[i:i + 2],
    ):

        label, filename = item

        with col:

            download_file(
                f"⬇ {label}",
                tables_dir / filename,
                "text/tab-separated-values",
            )


# =========================================================
# 4. BENCHMARK OUTPUTS
# =========================================================

html("""
<div class="section-banner">
    <h3>Benchmarking Outputs</h3>
</div>
""")

benchmark_dir = (
    ROOT
    / "results"
    / "benchmark"
)

process_benchmark = (
    benchmark_dir
    / "process_benchmark.tsv"
)

process_summary = (
    benchmark_dir
    / "process_summary.tsv"
)

pbmc_benchmark = (
    benchmark_dir
    / "PBMC_PRE"
    / "PBMC_PRE_benchmark_summary.tsv"
)

shared_benchmark = (
    benchmark_dir
    / "PBMC_PRE"
    / "PBMC_PRE_shared_clonotypes.tsv"
)

c1, c2 = st.columns(2)

with c1:
    download_file(
        "⬇ Pipeline Process Benchmark",
        process_benchmark,
        "text/tab-separated-values",
    )

with c2:
    download_file(
        "⬇ Pipeline Process Summary",
        process_summary,
        "text/tab-separated-values",
    )

c3, c4 = st.columns(2)

with c3:
    download_file(
        "⬇ PBMC_PRE Author Benchmark",
        pbmc_benchmark,
        "text/tab-separated-values",
    )

with c4:
    download_file(
        "⬇ Shared Benchmark Clonotypes",
        shared_benchmark,
        "text/tab-separated-values",
    )


# =========================================================
# 5. REPERTOIRE FIGURES
# =========================================================

html("""
<div class="section-banner">
    <h3>Repertoire Figures</h3>
</div>
""")

fig_dir = (
    ROOT
    / "results"
    / "repertoire"
    / "figures"
)

if fig_dir.exists():

    figures = sorted(
        fig_dir.glob("*.png")
    )

    if figures:

        for i in range(
            0,
            len(figures),
            2,
        ):

            cols = st.columns(2)

            for col, fig_path in zip(
                cols,
                figures[i:i + 2],
            ):

                with col:

                    st.image(
                        str(fig_path),
                        caption=fig_path.stem
                        .replace("_", " ")
                        .title(),
                        width='stretch',
                    )

                    download_file(
                        f"⬇ Download {fig_path.name}",
                        fig_path,
                        "image/png",
                    )

    else:
        st.info(
            "No repertoire PNG figures found."
        )

else:
    st.warning(
        "Repertoire figure directory not found."
    )


# =========================================================
# 6. NEXTFLOW EXECUTION REPORTS
# =========================================================

html("""
<div class="section-banner">
    <h3>Nextflow Execution Reports</h3>
</div>
""")

nextflow_dir = (
    ROOT
    / "results"
    / "nextflow"
)

nextflow_files = [
    (
        "Execution Report",
        "report.html",
        "text/html",
    ),
    (
        "Execution Timeline",
        "timeline.html",
        "text/html",
    ),
    (
        "Workflow DAG",
        "dag.html",
        "text/html",
    ),
    (
        "Trace File",
        "trace.txt",
        "text/plain",
    ),
]

for i in range(
    0,
    len(nextflow_files),
    2,
):

    cols = st.columns(2)

    for col, item in zip(
        cols,
        nextflow_files[i:i + 2],
    ):

        label, filename, mime = item

        with col:

            download_file(
                f"⬇ {label}",
                nextflow_dir / filename,
                mime,
            )


# =========================================================
# 7. QUICK OUTPUT INVENTORY
# =========================================================

html("""
<div class="section-banner">
    <h3>Available Project Deliverables</h3>
</div>
""")

html("""
<div class="content-card">

    <div style="
        display:grid;
        grid-template-columns:
            repeat(4, minmax(150px, 1fr));
        gap:18px;
        text-align:center;
    ">

        <div>
            <div style="font-size:2rem;">✅</div>
            <div style="
                font-weight:850;
                color:#8E2430;
                margin-top:6px;
            ">
                QC
            </div>
            <div class="muted">
                FastQC • MultiQC • MiXCR
            </div>
        </div>

        <div>
            <div style="font-size:2rem;">🧬</div>
            <div style="
                font-weight:850;
                color:#B8343E;
                margin-top:6px;
            ">
                Repertoire
            </div>
            <div class="muted">
                Diversity • V/J • clonotypes
            </div>
        </div>

        <div>
            <div style="font-size:2rem;">📊</div>
            <div style="
                font-weight:850;
                color:#D65A45;
                margin-top:6px;
            ">
                Benchmark
            </div>
            <div class="muted">
                Validation • CPU • memory
            </div>
        </div>

        <div>
            <div style="font-size:2rem;">📄</div>
            <div style="
                font-weight:850;
                color:#F28A3C;
                margin-top:6px;
            ">
                Reports
            </div>
            <div class="muted">
                Biological • Nextflow • figures
            </div>
        </div>

    </div>

</div>
""")


# =========================================================
# FOOTER
# =========================================================

html("""
<div style="
    margin-top:30px;
    padding:16px 18px;
    border-radius:14px;
    background:linear-gradient(
        90deg,
        #FFE8DD,
        #FFF2DF
    );
    border:1px solid #EFD5C8;
    color:#805E58;
    font-size:.84rem;
">

    <b style="color:#8E2430;">
        TCRFlowX Deliverables Hub
    </b>

    &nbsp;•&nbsp;

    All downloads are generated directly from the
    reproducible workflow outputs.

</div>
""")