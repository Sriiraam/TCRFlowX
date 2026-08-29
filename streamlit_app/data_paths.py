from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

LOCAL_RESULTS = PROJECT_ROOT / "results"
DEMO_RESULTS = PROJECT_ROOT / "demo_data" / "public_results"

LOCAL_DATABASE = PROJECT_ROOT / "database" / "tcrflowx.db"
DEMO_DATABASE = PROJECT_ROOT / "demo_data" / "database" / "tcrflowx.db"

# Local development uses full pipeline outputs.
# Streamlit Community Cloud falls back to the committed demo bundle.
RESULTS_ROOT = LOCAL_RESULTS if LOCAL_RESULTS.exists() else DEMO_RESULTS
DATABASE_PATH = LOCAL_DATABASE if LOCAL_DATABASE.exists() else DEMO_DATABASE
