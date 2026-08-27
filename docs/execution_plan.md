# TCRFlowX Execution Plan

## Phase 0 — Scientific Definition

Status: COMPLETE

Deliverables:

- biological objective
- project scope
- explicit non-goals
- success criteria

## Phase 1 — Dataset Verification

Status: COMPLETE

Verified:

- GSE337136
- PRJNA1484115
- SRP713941
- bulk TCR-seq
- TCR beta chain
- LymphoTrack TRB Assay Panel
- genomic DNA
- Illumina MiSeq
- paired-end sequencing
- longitudinal cHL study design

## Phase 2 — Manifest and Inventory Freeze

Status: COMPLETE

Deliverables:

- metadata/samplesheet.csv
- metadata/data_inventory.tsv
- docs/dataset.md

## Phase 3 — Architecture and Tool Freeze

Status: COMPLETE

Deliverables:

- docs/architecture.md
- docs/tool_decisions.md
- software environment inventory

## Phase 4 — Controlled Data Acquisition

Tasks:

1. retrieve SRA archives
2. verify archive integrity
3. convert to paired FASTQ
4. verify R1/R2 pairs
5. calculate checksums
6. record file sizes
7. update data inventory

Gate:

Do not proceed until all five inputs are validated.

## Phase 5 — Raw Sequencing QC

Tasks:

1. FastQC on every R1/R2
2. aggregate using MultiQC
3. inspect TCR-specific QC patterns
4. document PASS/WARN observations

Gate:

Preprocessing decision must be scientifically justified.

## Phase 6 — Read Preprocessing

Conditional phase.

If required:

FASTQ → fastp → FastQC → MultiQC

If unnecessary:

raw FASTQs proceed directly to MiXCR.

## Phase 7 — MiXCR Pilot

Use PBMC_PRE first.

Tasks:

1. identify correct MiXCR workflow/preset
2. process paired FASTQ
3. inspect alignment statistics
4. inspect assembled clonotypes
5. verify TRB assignments
6. verify CDR3 outputs

Gate:

Pilot must pass before scaling to five samples.

## Phase 8 — Full MiXCR Execution

Run all five frozen samples.

Outputs:

- MiXCR reports
- alignment files
- clonotype assemblies
- exported clonotype tables

## Phase 9 — Repertoire QC

Metrics:

- input reads
- aligned reads
- productive clonotypes
- unique clonotypes
- clone frequencies
- CDR3 length
- repertoire concentration

## Phase 10 — Repertoire Analysis

Analyses:

- diversity
- clonality
- TRBV usage
- TRBJ usage
- V-J combinations
- dominant clonotypes
- repertoire structure

## Phase 11 — Longitudinal Analysis

PBMC:

PRE → RELAPSE → PROGRESSION

Tumor:

PRE → PROGRESSION

Track:

- persistent clones
- expanded clones
- contracted clones
- newly detected clones
- disappearing clones

## Phase 12 — Tumor–Blood Comparison

Comparisons:

PBMC_PRE ↔ TUMOR_PRE

PBMC_PROGRESSION ↔ TUMOR_PROGRESSION

Metrics:

- shared clonotypes
- overlap indices
- dominant shared clones
- tissue-enriched clones
- blood-enriched clones

## Phase 13 — Validation

Compare TCRFlowX results with authors' processed clonotype files.

Evaluate:

- clonotype recovery
- CDR3 overlap
- top-clone agreement
- frequency agreement
- repertoire summary consistency

## Phase 14 — Nextflow Productionization

Requirements:

- DSL2 modules
- subworkflows
- parameter validation
- sample validation
- error handling
- resume support
- resource configuration
- trace
- timeline
- execution report

## Phase 15 — Containers and Testing

Requirements:

- Docker environments
- pinned software versions
- test profile
- minimal test input
- deterministic outputs where possible
- workflow tests

## Phase 16 — Benchmarking

Measure:

- execution time
- CPU usage
- peak memory
- disk usage
- process-level resource consumption

## Phase 17 — Streamlit Dashboard

Planned pages:

1. Project Overview
2. Sequencing QC
3. Repertoire Overview
4. Diversity & Clonality
5. V/J Gene Usage
6. Clonotype Tracking
7. Tumor–Blood Overlap
8. Clinical Timeline
9. Validation
10. Pipeline Performance

## Phase 18 — Documentation and Release

Deliverables:

- professional README
- methods
- architecture diagram
- dataset provenance
- results interpretation
- limitations
- reproducibility instructions
- benchmark report
- screenshots
- tagged GitHub release
