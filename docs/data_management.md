# TCRFlowX Data Management Policy

## Directory Responsibilities

### `data/raw/sra/`

Original SRA archives retrieved from NCBI during dataset acquisition.

These archives are treated as immutable source data after validation.

### `data/raw/fastq/`

Validated paired-end FASTQ files used by the production workflow.

Raw FASTQ files are never manually edited.

### `data/processed/`

Reserved for derived sequencing files if a preprocessing stage is scientifically justified.

The current validated production workflow sends raw FASTQ input directly to MiXCR after sequencing QC.

### `metadata/`

Contains:

- sample identity and accession mapping
- data inventory
- FASTQ SHA256 checksums
- software-version lock
- input-integrity manifest

### `results/`

Contains regenerable workflow outputs including:

- sequencing QC
- MiXCR outputs
- repertoire analysis
- biological interpretation
- formal QC
- run provenance
- Nextflow execution reports

## Raw Data Policy

Production FASTQ and SRA files must not be committed to GitHub.

The repository contains only the small deterministic CI FASTQ fixtures under:

`tests/data/ci/`

## Input Integrity

Production FASTQ SHA256 checksums are recorded in:

`metadata/fastq_checksums.sha256`

Release-critical metadata and configuration integrity is recorded in:

`metadata/input_integrity.sha256`

The integrity manifest covers the samplesheet, data inventory, FASTQ checksum
manifest, software lock, and workflow configuration files.

Input integrity is verified before release-grade canonical execution.

## Provenance

Biological samples remain traceable through:

GEO sample → SRA run → paired FASTQ → MiXCR reconstruction → repertoire analysis → biological interpretation

Run-level provenance is generated automatically by the workflow.

It records:

- UTC run timestamp
- Git commit
- Git branch
- Git working-tree state
- execution profile
- runtime samplesheet
- samplesheet SHA256
- reads directory
- output directory
- input-integrity manifest and SHA256
- software lock and SHA256
- Nextflow version
- Java version
- Python version
- MiXCR preset

Provenance outputs:

`results/provenance/run_provenance.tsv`

`results/provenance/run_provenance.md`

## Naming Convention

Stable biological sample identifiers are used throughout the analysis:

- `PBMC_PRE`
- `TUMOR_PRE`
- `PBMC_RELAPSE`
- `PBMC_PROGRESSION`
- `TUMOR_PROGRESSION`

Filenames must not replace biological sample identifiers inside analytical logic.
