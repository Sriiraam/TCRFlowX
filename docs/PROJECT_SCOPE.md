# TCRFlowX — Project Scope

## Project Title

TCRFlowX: A Reproducible Cancer Immunogenomics Pipeline for Longitudinal TCRβ Repertoire Analysis

## Domain

Cancer Immunogenomics / Bulk TCR-seq / Immune Repertoire Sequencing

## Biological Context

Classical Hodgkin lymphoma (cHL) patient treated with PD-1 blockade.

The study contains longitudinal PBMC and lymphoid tumor tissue samples collected before treatment, at relapse, and during progressive disease.

## Primary Biological Question

How does the T-cell receptor beta-chain repertoire change during PD-1 blockade, relapse, and progressive classical Hodgkin lymphoma?

## Secondary Questions

1. Does TCRβ repertoire diversity change during disease evolution?
2. Are specific clonotypes expanded or contracted during relapse/progression?
3. How does TCRβ clonality change over time?
4. Which TRBV/TRBJ genes dominate at different clinical stages?
5. Which clonotypes persist across multiple timepoints?
6. Which clonotypes are shared between peripheral blood and tumor tissue?
7. Does the tumor-associated TCR repertoire change between pre-treatment and progression?

## Engineering Objective

Develop a reproducible Nextflow DSL2 workflow capable of processing paired-end bulk TCRβ FASTQ files from raw sequencing data through quality control, TCR reconstruction, clonotype quantification, repertoire analysis, validation, reporting, and interactive visualization.

## Input

Paired-end Illumina MiSeq FASTQ files.

## Core Outputs

- Raw sequencing QC reports
- MultiQC report
- MiXCR alignment statistics
- TCRβ clonotype tables
- CDR3 nucleotide sequences
- CDR3 amino-acid sequences
- TRBV/TRBD/TRBJ assignments
- Clonotype counts and frequencies
- Diversity metrics
- Clonality metrics
- V/J gene-usage profiles
- Longitudinal clonotype tracking
- Tumor–PBMC repertoire overlap
- Benchmark/validation results
- Interactive Streamlit dashboard
- Reproducible Nextflow execution reports

## Validation Strategy

TCRFlowX results will be compared against processed clonotype files deposited by the original study authors.

Validation will include:

- clonotype count comparison
- dominant clonotype comparison
- CDR3 sequence overlap
- clonotype-frequency agreement
- repertoire-level summary comparison

## Success Criteria

TCRFlowX is considered complete when:

- all five samples run successfully
- raw FASTQ QC is documented
- TCRβ clonotypes are reconstructed reproducibly
- longitudinal repertoire metrics are generated
- PBMC and tumor repertoires are compared
- authors' processed results are used for validation
- Nextflow resume functionality is demonstrated
- software versions are pinned
- pipeline execution metrics are benchmarked
- Streamlit dashboard uses actual pipeline outputs
- GitHub documentation allows another user to reproduce the workflow

## Explicit Non-Goals

TCRFlowX will NOT perform:

- germline variant calling
- somatic SNV/indel calling
- BWA/GATK variant pipelines
- whole-genome analysis
- whole-exome analysis
- RNA differential-expression analysis
- single-cell RNA-seq analysis

TCRFlowX is specifically a bulk TCRβ immune-repertoire sequencing project.
