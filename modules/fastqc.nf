process FASTQC {

    tag "${meta.id}"

    cpus 2
    memory '2 GB'

    publishDir "${params.outdir}/qc/fastqc_raw",
        mode: 'copy',
        overwrite: true

    input:
    tuple val(meta), path(r1), path(r2)

    output:
    tuple val(meta),
          path("*_fastqc.html"),
          path("*_fastqc.zip"),
          emit: reports

    script:
    """
    fastqc \
        --threads ${task.cpus} \
        ${r1} \
        ${r2}
    """
}
