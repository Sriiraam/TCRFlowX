process MIXCR {

    tag "${meta.id}"

    cpus 4
    memory '5 GB'
    maxForks 1

    publishDir "${params.outdir}/mixcr/${meta.id}",
        mode: 'copy',
        overwrite: true

    input:
    tuple val(meta), path(r1), path(r2)

    output:
    tuple val(meta),
          path("${meta.id}.clones_TRB.tsv"),
          emit: clones

    tuple val(meta),
          path("${meta.id}.align.report.txt"),
          path("${meta.id}.assemble.report.txt"),
          path("${meta.id}.qc.txt"),
          emit: reports

    path "${meta.id}.qc.json", emit: qc_json

    script:
    """
    mixcr analyze \
        invivoscribe-human-dna-trb-lymphotrack \
        ${r1} \
        ${r2} \
        ${meta.id}
    """
}
