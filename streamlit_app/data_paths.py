from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

LOCAL_RESULTS = PROJECT_ROOT / "results"
DEMO_RESULTS = PROJECT_ROOT / "demo_data" / "public_results"

LOCAL_DATABASE = PROJECT_ROOT / "database" / "tcrflowx.db"
DEMO_DATABASE = PROJECT_ROOT / "demo_data" / "database" / "tcrflowx.db"

# The dashboard requires both current pipeline outputs and historical
# benchmarking outputs. A local results directory may exist after a
# canonical workflow run without containing the benchmark bundle.
_REQUIRED_DASHBOARD_FILES = (
    "repertoire/tables/diversity_clonality.tsv",
    "repertoire/biological_summary.tsv",
    "benchmark/PBMC_PRE/PBMC_PRE_benchmark_summary.tsv",
    "mixcr/formal_qc_summary.tsv",
    "provenance/run_provenance.tsv",
)


def _dashboard_bundle_complete(root: Path) -> bool:
    return root.exists() and all(
        (root / relative_path).is_file()
        for relative_path in _REQUIRED_DASHBOARD_FILES
    )


# Prefer a complete local dashboard bundle. Otherwise use the committed
# public demo bundle, which supports Streamlit Community Cloud deployment.
RESULTS_ROOT = (
    LOCAL_RESULTS
    if _dashboard_bundle_complete(LOCAL_RESULTS)
    else DEMO_RESULTS
)

DATABASE_PATH = (
    LOCAL_DATABASE
    if LOCAL_DATABASE.exists()
    else DEMO_DATABASE
)
