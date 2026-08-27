process MULTIQC {

    tag "raw_qc"

    cpus 2
    memory '2 GB'

    publishDir "${params.outdir}/qc/multiqc_raw",
        mode: 'copy',
        overwrite: true

    input:
    path fastqc_files

    output:
    path "multiqc_report.html", emit: report
    path "multiqc_data", emit: data

    script:
    """
    multiqc \
        ${fastqc_files} \
        --outdir . \
        --force
    """
}
