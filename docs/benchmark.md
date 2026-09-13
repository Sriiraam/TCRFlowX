# TCRFlowX Benchmark Summary

## Test Environment

The measurements below are historical process-level benchmark observations
from the development/benchmarking run and are retained as engineering evidence.

- Execution: Local WSL2
- Available CPU threads: 12
- RAM: 7.6 GiB
- Workflow manager: Nextflow DSL2

These measurements should not be interpreted as the resource allocation of
the current release configuration. The hardened release configuration caps
the MiXCR process at 4 CPUs.

## Main Performance Finding

MiXCR was the dominant computational stage.

Across five samples:

- CPU utilization: approximately 1034–1080%
- Peak RSS: approximately 2.6–2.8 GB
- Runtime per sample: approximately 1.75–7 minutes

During that historical benchmark run, MiXCR utilized roughly 10–11 CPU
cores while remaining within the available physical memory.

Current release resource settings are intentionally more conservative and are
documented in the workflow configuration.

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
