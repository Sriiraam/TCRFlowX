# TCRFlowX Benchmark Summary

## Test Environment

- Execution: Local WSL2
- CPU threads: 12
- RAM: 7.6 GiB
- Workflow manager: Nextflow DSL2

## Main Performance Finding

MiXCR was the dominant computational stage.

Across five samples:

- CPU utilization: approximately 1034–1080%
- Peak RSS: approximately 2.6–2.8 GB
- Runtime per sample: approximately 1.75–7 minutes

This indicates MiXCR efficiently used roughly 10–11 CPU cores while remaining within the available physical memory.

## Other Processes

FastQC:
- Peak RSS approximately 0.6–0.9 GB
- CPU approximately 140–175%

MultiQC:
- Peak RSS approximately 108 MB

Repertoire analysis:
- Peak RSS approximately 227 MB
- Runtime approximately 7 seconds

Biological summary:
- Minimal memory and runtime requirements

## Conclusion

TCRFlowX is practical for local execution on a modest workstation.

The main resource-intensive component is MiXCR, while downstream repertoire analysis and reporting require relatively little compute.

For larger cohorts, MiXCR is the primary process that would benefit from HPC or parallel execution.
