# ADR-001: TCRFlowX Scientific and Technical Design

## Status

Accepted

## Context

TCRFlowX requires a small but biologically meaningful public NGS dataset suitable for local execution while demonstrating production-style bioinformatics engineering.

GSE337136 provides longitudinal bulk TCRβ sequencing from a classical Hodgkin lymphoma patient undergoing PD-1 blockade.

## Decision

TCRFlowX will analyze all five bulk TCR-seq samples from GSE337136.

The pipeline will use:

- Nextflow DSL2
- Docker
- FastQC
- MultiQC
- conditional fastp preprocessing
- MiXCR for TCRβ reconstruction
- immunarch/R and Python for repertoire analysis
- Streamlit for interactive reporting

## Scientific Scope

The project focuses on T-cell receptor repertoire dynamics rather than conventional human genome variant discovery.

## Consequences

Advantages:

- real cancer patient data
- longitudinal treatment design
- tumor and peripheral blood samples
- cancer immunotherapy relevance
- small local-compute footprint
- authors' processed clonotypes available for validation

Limitations:

- single-patient longitudinal study
- targeted TCRβ assay rather than unbiased whole-genome sequencing
- findings are exploratory and cannot establish population-level clinical conclusions

## Final Decision

Dataset and scientific direction are frozen for TCRFlowX.
