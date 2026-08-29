# Changelog

All notable changes to TCRFlowX are documented here.

The project follows Semantic Versioning where practical.

## [Unreleased]

### Planned
- Extended workflow containerization
- Additional automated integration tests
- Optional cloud/HPC validation

## [0.1.0] - 2026-08-29

### Added
- Nextflow DSL2 TCR-seq workflow
- FastQC sequencing quality control
- MultiQC aggregated QC reporting
- MiXCR TRB repertoire reconstruction
- Diversity and clonality analysis
- Longitudinal clonotype tracking
- Tumor–PBMC repertoire overlap analysis
- Biological summary generation
- Author-processed repertoire benchmarking
- Pipeline resource benchmarking
- SQLite analytical database
- SQL clonotype exploration
- Interactive Streamlit dashboard
- Dockerized dashboard deployment
- Local Kubernetes deployment using kind
- Local, Docker, SLURM, Kubernetes and Azure configuration profiles
- Automated pytest output validation
- Nextflow report, trace, timeline and DAG generation
- Project architecture and technical documentation

### Validation
- 5 automated tests passing
- Author repertoire Jaccard similarity: 0.983
- Top-20 clonotype agreement: 20/20
- Top-100 clonotype agreement: 98/100
- Spearman correlation: 0.997

