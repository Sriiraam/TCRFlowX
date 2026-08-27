# TCRFlowX Data Management Policy

## Directory Responsibilities

### data/raw/sra/

Original SRA archives downloaded from NCBI.

These files are immutable after successful validation.

### data/raw/fastq/

FASTQ files generated from validated SRA archives.

Raw FASTQ files are never manually edited.

### data/processed/

Only derived sequencing files created by preprocessing stages.

### metadata/

Contains sample identity, accession mapping, clinical metadata, and data inventory.

### results/

Contains reproducible pipeline outputs only.

Results must be regenerable from:

- raw data
- metadata
- pipeline code
- configuration
- pinned environments

## Raw Data Policy

Raw FASTQ and SRA files must NOT be committed to GitHub.

## Integrity

After acquisition, checksums will be generated for input files.

Checksums will be recorded before downstream pipeline execution.

## Provenance

Every biological sample must remain traceable through:

GEO sample
→ BioSample
→ SRA run
→ FASTQ
→ MiXCR output
→ repertoire analysis

## Naming Convention

Use stable project identifiers:

PBMC_PRE
TUMOR_PRE
PBMC_RELAPSE
PBMC_PROGRESSION
TUMOR_PROGRESSION

Do not use filenames as biological identifiers inside analytical scripts.
