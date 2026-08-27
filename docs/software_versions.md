# TCRFlowX Software Versions

## Current Development Environment

| Software | Version | Status |
|---|---|---|
| Ubuntu / WSL2 | Ubuntu 24.04 environment | Ready |
| Java | OpenJDK 21.0.11 | Ready |
| Nextflow | 25.10.4 | Ready |
| Docker | 29.7.2 | Ready |
| FastQC | 0.12.1 | Ready |
| MultiQC | 1.18 | Ready |
| fastp | 0.23.4 | Ready |
| SRA Toolkit prefetch | 3.0.3 | Ready |
| SRA Toolkit fasterq-dump | 3.0.3 | Ready |
| R | 4.3.3 | Ready |
| Python | 3.12.3 | Ready |
| MiXCR | 4.7.0-370-develop | Development install |
| immunarch | Pending | Deferred |

## Hardware Environment

- CPU threads available: 12
- RAM: 7.6 GiB
- Swap: 2.0 GiB
- Development execution: local WSL2
- Paid cloud compute: not required

## Reproducibility Policy

Development versions may be used during exploration.

Before production release:

- MiXCR must be pinned to an approved stable version
- container versions must be pinned
- package versions must be recorded
- Nextflow version must be recorded
- final software versions must not use floating tags such as `latest`
