# TCRFlowX Tool Decisions

## Workflow Manager

### Nextflow DSL2

Decision: ACCEPTED

Purpose:
- workflow orchestration
- reproducibility
- modular processes
- resume support
- resource management
- container integration
- execution reporting

## Sequencing QC

### FastQC

Decision: ACCEPTED

Purpose:
- per-base quality
- sequence length
- GC distribution
- adapter signals
- duplication
- overrepresented sequences

Important:

High duplication or unusual sequence composition in targeted TCR libraries must not automatically be interpreted as sequencing failure.

## QC Aggregation

### MultiQC

Decision: ACCEPTED

Purpose:
Aggregate sequencing and pipeline QC into a project-level report.

## Read Preprocessing

### fastp

Decision: CONDITIONAL

fastp will only be used if raw-read QC demonstrates a justified preprocessing requirement.

Automatic trimming without evidence is not part of TCRFlowX.

## TCR Reconstruction

### MiXCR

Decision: ACCEPTED — CORE TOOL

Purpose:
- TCRβ V(D)J alignment
- CDR3 identification
- clonotype assembly
- clonotype abundance calculation
- receptor gene assignment

Scientific justification:

The original GSE337136 study also used MiXCR for TCR-seq processing.

## Downstream Repertoire Analysis

### immunarch

Decision: ACCEPTED — INSTALLATION DEFERRED

Purpose:
- repertoire diversity
- clonality
- repertoire overlap
- gene usage
- clonotype exploration

Installation will be finalized when the repertoire-analysis module is implemented.

## Custom Data Processing

### Python

Libraries planned:

- pandas
- numpy
- scipy
- plotly

Purpose:
- data transformation
- custom clonotype tracking
- benchmarking
- dashboard preparation

## Statistical / Repertoire Analysis

### R

Purpose:
- immunarch
- statistical analysis
- publication-quality analysis where appropriate

## Dashboard

### Streamlit

Decision: ACCEPTED

Purpose:
Interactive visualization of actual TCRFlowX outputs.

## Containers

### Docker

Decision: ACCEPTED

Purpose:
- pinned environments
- portable execution
- reproducibility

## Data Acquisition

### NCBI SRA Toolkit

Tools:

- prefetch
- fasterq-dump

Purpose:
Controlled retrieval of public sequencing data.

## Tools Explicitly Excluded

The following are not part of the core TCRFlowX workflow:

- BWA
- STAR
- GATK
- Mutect2
- HaplotypeCaller
- featureCounts
- DESeq2

These tools answer different biological questions and are not required for targeted bulk TCRβ repertoire reconstruction.
