process FORMAL_QC {

    tag "formal_qc"

    cpus 1
    memory '1 GB'

    publishDir "${params.outdir}/mixcr",
        mode: 'copy',
        overwrite: true

    input:
    path qc_files
    path clone_files

    output:
    path "mixcr_qc_summary.tsv", emit: mixcr_summary
    path "formal_qc_summary.tsv", emit: formal_summary
    path "formal_qc_report.md", emit: formal_report

    script:
    """
    python ${projectDir}/scripts/evaluate_qc.py
    """
}
