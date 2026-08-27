from pathlib import Path
import pandas as pd

base = Path("results/repertoire/tables")
outdir = Path("results/repertoire")
outdir.mkdir(parents=True, exist_ok=True)

div = pd.read_csv(base / "diversity_clonality.tsv", sep="\t")
overlap = pd.read_csv(base / "tumor_pbmc_overlap.tsv", sep="\t")
tracking = pd.read_csv(base / "pbmc_longitudinal_clonotypes.tsv", sep="\t")

# ---------------------------------------------------------
# Extract key samples
# ---------------------------------------------------------

pre = div.loc[div["sample"] == "PBMC_PRE"].iloc[0]
relapse = div.loc[div["sample"] == "PBMC_RELAPSE"].iloc[0]
prog = div.loc[div["sample"] == "PBMC_PROGRESSION"].iloc[0]

tumor_pre = div.loc[div["sample"] == "TUMOR_PRE"].iloc[0]
tumor_prog = div.loc[div["sample"] == "TUMOR_PROGRESSION"].iloc[0]

pre_overlap = overlap.loc[overlap["stage"] == "PRE"].iloc[0]
prog_overlap = overlap.loc[overlap["stage"] == "PROGRESSION"].iloc[0]

# ---------------------------------------------------------
# Persistent and stage-specific clones
# ---------------------------------------------------------

persistent = tracking[
    tracking["detected_timepoints"] == 3
].copy()

persistent = persistent.sort_values(
    "max_fraction",
    ascending=False
)

relapse_only_or_emergent = tracking[
    (tracking["PBMC_PRE"] == 0) &
    (tracking["PBMC_RELAPSE"] > 0)
].copy()

progression_only_or_emergent = tracking[
    (tracking["PBMC_PRE"] == 0) &
    (tracking["PBMC_PROGRESSION"] > 0)
].copy()

top_persistent = persistent.head(10)

# ---------------------------------------------------------
# Machine-readable summary
# ---------------------------------------------------------

summary_rows = [
    {
        "finding": "PBMC richness decreases at relapse",
        "value_pre": pre["productive_richness"],
        "value_relapse": relapse["productive_richness"],
        "interpretation": "Marked contraction of productive TCRbeta repertoire richness at relapse."
    },
    {
        "finding": "PBMC clonality increases at relapse",
        "value_pre": pre["clonality"],
        "value_relapse": relapse["clonality"],
        "interpretation": "Relapse repertoire becomes more oligoclonal, consistent with expansion of selected T-cell clones."
    },
    {
        "finding": "PBMC richness rebounds at progression",
        "value_pre": relapse["productive_richness"],
        "value_relapse": prog["productive_richness"],
        "interpretation": "Repertoire richness expands again at progression, although clonality remains above the pre-treatment state."
    },
    {
        "finding": "Tumor clonality decreases at progression",
        "value_pre": tumor_pre["clonality"],
        "value_relapse": tumor_prog["clonality"],
        "interpretation": "Progression tumor repertoire is less dominated by a small number of clones than the pre-treatment tumor repertoire."
    },
    {
        "finding": "Tumor-PBMC overlap decreases",
        "value_pre": pre_overlap["jaccard"],
        "value_relapse": prog_overlap["jaccard"],
        "interpretation": "Shared productive TCRbeta repertoire between blood and tumor decreases at progression."
    }
]

summary_df = pd.DataFrame(summary_rows)

summary_df.to_csv(
    outdir / "biological_summary.tsv",
    sep="\t",
    index=False
)

# ---------------------------------------------------------
# Markdown interpretation report
# ---------------------------------------------------------

top_clone = tracking.sort_values(
    "max_fraction",
    ascending=False
).iloc[0]

markdown = f"""# TCRFlowX Biological Interpretation

## Study Context

TCRFlowX analyzes longitudinal bulk TCRbeta repertoire sequencing from a classical Hodgkin lymphoma patient undergoing PD-1 inhibitor therapy.

The analysis compares:

- PBMC pre-treatment
- PBMC relapse
- PBMC progression
- Tumor tissue pre-treatment
- Tumor tissue progression

## 1. Peripheral Blood Repertoire Dynamics

PBMC productive richness decreased from **{int(pre['productive_richness'])}** clonotypes pre-treatment to **{int(relapse['productive_richness'])}** at relapse.

Shannon diversity decreased from **{pre['shannon']:.3f}** to **{relapse['shannon']:.3f}**.

Clonality increased from **{pre['clonality']:.3f}** to **{relapse['clonality']:.3f}**.

This indicates a substantial contraction of repertoire diversity at relapse together with stronger dominance by selected T-cell clones.

At progression, productive richness increased again to **{int(prog['productive_richness'])}**, while clonality remained elevated at **{prog['clonality']:.3f}** compared with the pre-treatment state.

## 2. Dominant Persistent Clonotype

The most prominent longitudinal clonotype was:

**{top_clone['cdr3aa']}**

Frequency:

- Pre-treatment: **{top_clone['PBMC_PRE']*100:.2f}%**
- Relapse: **{top_clone['PBMC_RELAPSE']*100:.2f}%**
- Progression: **{top_clone['PBMC_PROGRESSION']*100:.2f}%**

This clone persisted across all three PBMC timepoints and increased in abundance during disease evolution.

## 3. Tumor Repertoire Dynamics

Tumor productive richness changed from **{int(tumor_pre['productive_richness'])}** pre-treatment to **{int(tumor_prog['productive_richness'])}** at progression.

Tumor clonality decreased from **{tumor_pre['clonality']:.3f}** to **{tumor_prog['clonality']:.3f}**.

The top-10 clonotype contribution also decreased from **{tumor_pre['top10_fraction']*100:.2f}%** to **{tumor_prog['top10_fraction']*100:.2f}%**.

This suggests that the progression tumor repertoire became less dominated by a small number of highly expanded T-cell clones.

## 4. Tumor-Blood Repertoire Overlap

At pre-treatment:

- PBMC productive clonotypes: **{int(pre_overlap['pbmc_clonotypes'])}**
- Tumor productive clonotypes: **{int(pre_overlap['tumor_clonotypes'])}**
- Shared clonotypes: **{int(pre_overlap['shared_clonotypes'])}**
- Jaccard overlap: **{pre_overlap['jaccard']:.3f}**

At progression:

- PBMC productive clonotypes: **{int(prog_overlap['pbmc_clonotypes'])}**
- Tumor productive clonotypes: **{int(prog_overlap['tumor_clonotypes'])}**
- Shared clonotypes: **{int(prog_overlap['shared_clonotypes'])}**
- Jaccard overlap: **{prog_overlap['jaccard']:.3f}**

The reduction in blood-tumor repertoire overlap suggests greater divergence between circulating and tumor-associated T-cell populations during progression.

## 5. Persistent Clonotypes

Number of productive CDR3 clonotypes detected across all three PBMC timepoints:

**{len(persistent)}**

The top persistent clonotypes are written to:

`results/repertoire/top_persistent_clonotypes.tsv`

## Biological Interpretation

The TCRFlowX analysis shows a pronounced repertoire contraction and increased clonality at relapse, followed by expansion of repertoire richness at progression.

Several clonotypes remain persistent across the clinical timeline, while tumor and circulating repertoires become less similar at progression.

These findings are consistent with dynamic restructuring of the T-cell repertoire during PD-1 inhibitor treatment and disease evolution.

## Important Limitation

This dataset represents a longitudinal analysis of a single classical Hodgkin lymphoma patient.

The findings are therefore descriptive and hypothesis-generating. They should not be interpreted as population-level clinical conclusions.
"""

(outdir / "biological_interpretation.md").write_text(markdown)

top_persistent.to_csv(
    outdir / "top_persistent_clonotypes.tsv",
    sep="\t",
    index=False
)

print(summary_df.to_string(index=False))
print()
print(f"Persistent PBMC clonotypes across all 3 timepoints: {len(persistent)}")
print(f"Relapse-emergent clonotypes: {len(relapse_only_or_emergent)}")
print(f"Progression-emergent clonotypes: {len(progression_only_or_emergent)}")
print()
print("Phase 9 biological interpretation complete.")
