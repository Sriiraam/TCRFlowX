from pathlib import Path
import sqlite3
import pandas as pd
import pytest

ROOT = Path(__file__).resolve().parents[1]


def require_file(path: Path):
    if not path.exists():
        pytest.skip(f"Generated pipeline output not available: {path}")


def test_diversity_table():
    path = ROOT / "results/repertoire/tables/diversity_clonality.tsv"
    require_file(path)

    df = pd.read_csv(path, sep="\t")
    assert len(df) == 5
    assert not df.empty


def test_mixcr_qc():
    path = ROOT / "results/mixcr/mixcr_qc_summary.tsv"
    require_file(path)

    df = pd.read_csv(path, sep="\t")
    assert len(df) == 5


def test_database():
    db = ROOT / "database/tcrflowx.db"
    require_file(db)

    con = sqlite3.connect(db)

    samples = con.execute(
        "SELECT COUNT(*) FROM samples"
    ).fetchone()[0]

    clonotypes = con.execute(
        "SELECT COUNT(*) FROM clonotypes"
    ).fetchone()[0]

    con.close()

    assert samples == 5
    assert clonotypes > 0


def test_expected_samples():
    path = ROOT / "results/repertoire/tables/diversity_clonality.tsv"
    require_file(path)

    df = pd.read_csv(path, sep="\t")

    expected = {
        "PBMC_PRE",
        "TUMOR_PRE",
        "PBMC_RELAPSE",
        "PBMC_PROGRESSION",
        "TUMOR_PROGRESSION",
    }

    assert set(df["sample"]) == expected


def test_benchmark_result():
    path = ROOT / "results/benchmark/process_summary.tsv"
    require_file(path)

    df = pd.read_csv(path, sep="\t")
    assert not df.empty
