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
    mkdir -p results/mixcr

    for file in ${clones}; do
        sample=\$(basename \$file .clones_TRB.tsv)

        mkdir -p results/mixcr/\$sample

        cp \$file \
           results/mixcr/\$sample/\${sample}.clones_TRB.tsv
    done

    Rscript ${projectDir}/scripts/repertoire_analysis.R

    cp -r ${projectDir}/results/repertoire/tables .
    cp -r ${projectDir}/results/repertoire/figures .
    """
}
