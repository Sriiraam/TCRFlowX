# TCRFlowX Pipeline Architecture

## High-Level Architecture

SRA Accessions
      |
      v
DATA ACQUISITION
      |
      v
Paired FASTQ
      |
      v
RAW FASTQ QC
FastQC
      |
      v
MultiQC
      |
      v
PREPROCESSING DECISION
      |
      +---- Good quality ----------> continue
      |
      +---- Adapter/quality issue -> fastp
                                      |
                                      v
                                  FastQC
                                      |
                                      v
TCR RECONSTRUCTION
MiXCR
      |
      v
V(D)J Assignment
      |
      v
CDR3 Identification
      |
      v
Clonotype Assembly
      |
      v
Clonotype Tables
      |
      +----------------------+
      |                      |
      v                      v
REPERTOIRE QC          REPERTOIRE ANALYSIS
                             |
                +------------+------------+
                |            |            |
                v            v            v
             Diversity    Clonality    V/J Usage
                |
                v
        CLONOTYPE TRACKING
                |
                v
       LONGITUDINAL ANALYSIS
                |
        +-------+-------+
        |               |
        v               v
 PBMC trajectory    Tumor trajectory
        |               |
        +-------+-------+
                |
                v
       TUMOR-PBMC OVERLAP
                |
                v
          VALIDATION
 Authors' processed data
                |
                v
           REPORTING
                |
                v
       STREAMLIT DASHBOARD

Workflow Engineering

Nextflow DSL2 will orchestrate independent modules.

Planned modules:

SRA download
FASTQ conversion
FastQC raw
fastp
FastQC processed
MultiQC
MiXCR analysis
clonotype export
repertoire QC
repertoire statistics
clonotype tracking
repertoire overlap
benchmark comparison
report generation
Subworkflows

Planned logical subworkflows:

ACQUIRE_DATA

SRA accession → validated paired FASTQ

READ_QC

FASTQ → FastQC → optional fastp → post-QC

TCR_RECONSTRUCTION

FASTQ → MiXCR → TCRβ clonotypes

REPERTOIRE_ANALYSIS

Clonotypes → diversity/clonality/gene usage/overlap

VALIDATION

TCRFlowX clonotypes → comparison with deposited study results

REPORTING

Pipeline outputs → figures/tables/dashboard-ready files

Execution Model

Primary execution:

local WSL2 workstation

Future compatibility:

Docker
SLURM/HPC
other container-compatible environments

Paid cloud compute is not required.
