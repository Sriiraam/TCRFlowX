# TCRFlowX Software Versions

## Validated Analysis Environment

The versions below correspond to the environment used to validate the
TCRFlowX workflow and biological analysis.

| Software | Version | Notes |
|---|---:|---|
| Ubuntu | 24.04.4 LTS | WSL2 development environment |
| Java | OpenJDK 21.0.12 | Local validated runtime |
| Nextflow | 25.10.4 build 11173 | Pinned in CI |
| Python | 3.12.3 | Validated local environment |
| FastQC | 0.12.1 | Sequencing QC |
| MultiQC | 1.35 | Pinned Python dependency |
| MiXCR | 4.7.0-370-develop | Revision `00eb424cfc`; exact validated build |
| MiXCR reference library | repseqio.v6.3 | Built-in V/D/J/C library |
| R | 4.3.3 | Repertoire analysis |
| dplyr | 1.2.1 | R package |
| tidyr | 1.3.2 | R package |
| ggplot2 | 4.0.3 | R package |
| Streamlit | 1.62.0 | Dashboard |
| pandas | 3.0.5 | Python package |
| NumPy | 2.5.2 | Python package |
| SciPy | 1.18.1 | Python package |
| Matplotlib | 3.11.1 | Python package |
| seaborn | 0.13.2 | Python package |
| Plotly | 7.0.0 | Dashboard visualization |
| pytest | 9.1.1 | Development/test dependency |

The machine-readable version record is:

`metadata/software_versions.lock.tsv`

## MiXCR Version Policy

The validated TCRFlowX analysis uses:

`MiXCR v4.7.0-370-develop`

with revision:

`00eb424cfc`

and built-in reference library:

`repseqio.v6.3`

The SHA256 checksum of the validated MiXCR executable is recorded in
`metadata/software_versions.lock.tsv`.

This build is retained to preserve reproducibility of the current validated
analysis. TCRFlowX does not represent it as a stable MiXCR release.

Changing the MiXCR release or build must be treated as a workflow version
change and requires re-running and re-validating clonotype and repertoire
results.

## Container Scope

The Dockerfile packages the Streamlit dashboard environment.

It does not represent the complete TCRFlowX biological pipeline runtime.
FastQC, MiXCR, Nextflow and R are not claimed to execute inside the dashboard
container.

## Execution Profiles

- `local`: validated local execution
- `docker`: Docker-enabled configuration profile
- `slurm`: configuration profile only; real SLURM execution has not been claimed
- `azure`: placeholder configuration only; real Azure execution has not been claimed

## Reproducibility Policy

Changes to Nextflow, MiXCR, FastQC, MultiQC, Python dependencies, R
dependencies or biological analysis scripts require reproducibility
validation before a new release is created.
