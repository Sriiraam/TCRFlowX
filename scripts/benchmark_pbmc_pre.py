import pandas as pd
from scipy.stats import spearmanr
from pathlib import Path

author_file = Path(
    "data/reference/author_processed/"
    "GSM9848698_TP1_PBMC_TCR_processed.txt.gz"
)

our_file = Path(
    "results/mixcr/pilot/PBMC_PRE/"
    "PBMC_PRE.clones_TRB.tsv"
)

outdir = Path("results/benchmark/PBMC_PRE")
outdir.mkdir(parents=True, exist_ok=True)

# Load tables
author = pd.read_csv(author_file, sep="\t")
ours = pd.read_csv(our_file, sep="\t")

# Standardize key columns
author = author.rename(columns={
    "aaSeqCDR3": "cdr3",
    "cloneCount": "author_count",
    "cloneFraction": "author_fraction"
})

ours = ours.rename(columns={
    "aaSeqCDR3": "cdr3",
    "readCount": "our_count",
    "readFraction": "our_fraction"
})

# Keep productive CDR3 sequences only
author = author[author["cdr3"].notna()].copy()
ours = ours[ours["cdr3"].notna()].copy()

author = author[~author["cdr3"].str.contains(r"[\*_]", regex=True)]
ours = ours[~ours["cdr3"].str.contains(r"[\*_]", regex=True)]

# Collapse duplicate CDR3 amino-acid sequences
author_cdr3 = (
    author.groupby("cdr3", as_index=False)
    .agg(
        author_count=("author_count", "sum"),
        author_fraction=("author_fraction", "sum")
    )
)

our_cdr3 = (
    ours.groupby("cdr3", as_index=False)
    .agg(
        our_count=("our_count", "sum"),
        our_fraction=("our_fraction", "sum")
    )
)

# Shared clonotypes
shared = author_cdr3.merge(our_cdr3, on="cdr3", how="inner")

author_set = set(author_cdr3["cdr3"])
our_set = set(our_cdr3["cdr3"])

intersection = len(author_set & our_set)
union = len(author_set | our_set)

jaccard = intersection / union if union else 0

# Rank agreement
author_top20 = set(
    author_cdr3.nlargest(20, "author_fraction")["cdr3"]
)

our_top20 = set(
    our_cdr3.nlargest(20, "our_fraction")["cdr3"]
)

author_top100 = set(
    author_cdr3.nlargest(100, "author_fraction")["cdr3"]
)

our_top100 = set(
    our_cdr3.nlargest(100, "our_fraction")["cdr3"]
)

top20_overlap = len(author_top20 & our_top20)
top100_overlap = len(author_top100 & our_top100)

# Frequency correlation
rho, pvalue = spearmanr(
    shared["author_fraction"],
    shared["our_fraction"]
)

summary = pd.DataFrame({
    "metric": [
        "author_productive_unique_cdr3",
        "tcrflowx_productive_unique_cdr3",
        "shared_productive_cdr3",
        "cdr3_jaccard",
        "top20_overlap",
        "top100_overlap",
        "spearman_rho",
        "spearman_pvalue"
    ],
    "value": [
        len(author_cdr3),
        len(our_cdr3),
        intersection,
        jaccard,
        top20_overlap,
        top100_overlap,
        rho,
        pvalue
    ]
})

summary.to_csv(
    outdir / "PBMC_PRE_benchmark_summary.tsv",
    sep="\t",
    index=False
)

shared.to_csv(
    outdir / "PBMC_PRE_shared_clonotypes.tsv",
    sep="\t",
    index=False
)

print(summary.to_string(index=False))
