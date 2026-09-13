process REPERTOIRE_ANALYSIS {

    tag "repertoire_analysis"

    cpus 2
    memory '2 GB'

    publishDir "${params.outdir}/repertoire",
        mode: 'copy',
        overwrite: true

    input:
    path clones

    output:
    path "tables", emit: tables
    path "figures", emit: figures

    script:
    """
    Rscript ${projectDir}/scripts/repertoire_analysis.R
    """
}
