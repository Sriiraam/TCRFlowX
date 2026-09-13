# TCRFlowX Formal QC Report

This report applies reproducible PASS/WARN/FAIL classification to MiXCR repertoire-reconstruction metrics.

A FAIL indicates a sample requiring explicit QC review; it does not automatically invalidate downstream biological interpretation.

## Thresholds

| Metric | PASS | WARN | FAIL |
|---|---|---|---|
| Successfully aligned reads | >=80% | 60-<80% | <60% |
| Reads used in clonotypes | >=70% | 50-<70% | <50% |
| Off-target reads | <=20% | >20-40% | >40% |
| Reads with no V/J hits | <=5% | >5-10% | >10% |
| Alignments without CDR3 | <=10% | >10-20% | >20% |
| Low-quality alignment drop | <=5% | >5-10% | >10% |
| TRB clonotypes | >=1000 | 100-999 | <100 |

## Sample Results

| Sample | Aligned | Used in clonotypes | Off-target | TRB clonotypes | Overall |
|---|---:|---:|---:|---:|---|
| PBMC_PRE | 50.79% | 40.92% | 48.20% | 6236 | **FAIL** |
| PBMC_PROGRESSION | 67.73% | 64.05% | 31.11% | 6423 | **WARN** |
| PBMC_RELAPSE | 73.09% | 67.63% | 24.70% | 2319 | **WARN** |
| TUMOR_PRE | 79.82% | 74.34% | 19.49% | 5932 | **WARN** |
| TUMOR_PROGRESSION | 60.55% | 56.83% | 38.21% | 3188 | **WARN** |

## FastQC Interpretation Policy

TCRFlowX treats FastQC duplication, overrepresented-sequence, sequence-composition and GC-distribution warnings/failures as contextual for targeted TCR repertoire sequencing rather than automatic sample failure. Genuine clonal expansion and assay design can produce these patterns.

Per-base sequence quality, adapter contamination, N content and other conventional sequencing-quality metrics remain reviewable technical QC signals.
