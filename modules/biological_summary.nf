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
    mkdir -p results/repertoire

    cp -r ${tables} results/repertoire/tables

    python ${projectDir}/scripts/biological_summary.py

    cp ${projectDir}/results/repertoire/biological_summary.tsv .
    cp ${projectDir}/results/repertoire/biological_interpretation.md .
    cp ${projectDir}/results/repertoire/top_persistent_clonotypes.tsv .
    """
}
