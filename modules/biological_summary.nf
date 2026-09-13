process BIOLOGICAL_SUMMARY {

    tag "biological_summary"

    cpus 1
    memory '1 GB'

    publishDir "${params.outdir}/repertoire",
        mode: 'copy',
        overwrite: true

    input:
    path tables

    output:
    path "biological_summary.tsv"
    path "biological_interpretation.md"
    path "top_persistent_clonotypes.tsv"

    script:
    """
    python ${projectDir}/scripts/biological_summary.py
    """
}
