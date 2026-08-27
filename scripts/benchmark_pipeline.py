from pathlib import Path
import pandas as pd

trace = Path("results/nextflow/trace.txt")
outdir = Path("results/benchmark")
outdir.mkdir(parents=True, exist_ok=True)

if not trace.exists():
    raise SystemExit("ERROR: results/nextflow/trace.txt not found")

df = pd.read_csv(trace, sep="\t")

# Normalize Nextflow trace headers
df.columns = [c.strip().lstrip("#").strip() for c in df.columns]

print("Trace columns:")
print(list(df.columns))

# Nextflow normally calls this column 'name'
if "process" not in df.columns:
    if "name" in df.columns:
        df["process"] = (
            df["name"]
            .astype(str)
            .str.replace(r"\s*\(.*\)$", "", regex=True)
        )
    else:
        raise SystemExit(
            f"ERROR: Neither 'process' nor 'name' found. Columns: {list(df.columns)}"
        )

# CPU conversion
if "%cpu" in df.columns:
    df["cpu_numeric"] = pd.to_numeric(
        df["%cpu"].astype(str).str.replace("%", "", regex=False),
        errors="coerce"
    )

# Task-level table
keep = [
    "task_id",
    "process",
    "name",
    "status",
    "realtime",
    "%cpu",
    "peak_rss",
    "peak_vmem",
    "read_bytes",
    "write_bytes"
]

available = [c for c in keep if c in df.columns]

df[available].to_csv(
    outdir / "process_benchmark.tsv",
    sep="\t",
    index=False
)

# Process-level summary
aggregations = {}

if "task_id" in df.columns:
    aggregations["tasks"] = ("task_id", "count")

if "cpu_numeric" in df.columns:
    aggregations["mean_cpu_pct"] = ("cpu_numeric", "mean")
    aggregations["max_cpu_pct"] = ("cpu_numeric", "max")

if aggregations:
    process_summary = (
        df.groupby("process")
        .agg(**aggregations)
        .reset_index()
    )
else:
    process_summary = df[["process"]].drop_duplicates()

process_summary.to_csv(
    outdir / "process_summary.tsv",
    sep="\t",
    index=False
)

print("\n=== TCRFlowX PROCESS BENCHMARK ===")
print(df[available].to_string(index=False))

print("\n=== PROCESS SUMMARY ===")
print(process_summary.to_string(index=False))

print("\nPhase 11 benchmark tables generated.")
