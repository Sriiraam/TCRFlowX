# TCRFlowX Biological Interpretation

## Study Context

TCRFlowX analyzes longitudinal bulk TCRbeta repertoire sequencing from a classical Hodgkin lymphoma patient undergoing PD-1 inhibitor therapy.

The analysis compares:

- PBMC pre-treatment
- PBMC relapse
- PBMC progression
- Tumor tissue pre-treatment
- Tumor tissue progression

## 1. Peripheral Blood Repertoire Dynamics

PBMC productive richness decreased from **4994** clonotypes pre-treatment to **1862** at relapse.

Shannon diversity decreased from **7.330** to **5.648**.

Clonality increased from **0.139** to **0.250**.

This indicates a substantial contraction of repertoire diversity at relapse together with stronger dominance by selected T-cell clones.

At progression, productive richness increased again to **5193**, while clonality remained elevated at **0.219** compared with the pre-treatment state.

## 2. Dominant Persistent Clonotype

The most prominent longitudinal clonotype was:

**CASSQGTGYTNTEAFF**

Frequency:

- Pre-treatment: **6.26%**
- Relapse: **8.04%**
- Progression: **8.25%**

This clone persisted across all three PBMC timepoints and increased in abundance during disease evolution.

## 3. Tumor Repertoire Dynamics

Tumor productive richness changed from **4710** pre-treatment to **2534** at progression.

Tumor clonality decreased from **0.221** to **0.112**.

The top-10 clonotype contribution also decreased from **27.37%** to **10.44%**.

This suggests that the progression tumor repertoire became less dominated by a small number of highly expanded T-cell clones.

## 4. Tumor-Blood Repertoire Overlap

At pre-treatment:

- PBMC productive clonotypes: **4835**
- Tumor productive clonotypes: **4546**
- Shared clonotypes: **1096**
- Jaccard overlap: **0.132**

At progression:

- PBMC productive clonotypes: **5018**
- Tumor productive clonotypes: **2467**
- Shared clonotypes: **445**
- Jaccard overlap: **0.063**

The reduction in blood-tumor repertoire overlap suggests greater divergence between circulating and tumor-associated T-cell populations during progression.

## 5. Persistent Clonotypes

Number of productive CDR3 clonotypes detected across all three PBMC timepoints:

**206**

The top persistent clonotypes are written to:

`results/repertoire/top_persistent_clonotypes.tsv`

## Biological Interpretation

The TCRFlowX analysis shows a pronounced repertoire contraction and increased clonality at relapse, followed by expansion of repertoire richness at progression.

Several clonotypes remain persistent across the clinical timeline, while tumor and circulating repertoires become less similar at progression.

These findings are consistent with dynamic restructuring of the T-cell repertoire during PD-1 inhibitor treatment and disease evolution.

## Important Limitation

This dataset represents a longitudinal analysis of a single classical Hodgkin lymphoma patient.

The findings are therefore descriptive and hypothesis-generating. They should not be interpreted as population-level clinical conclusions.
