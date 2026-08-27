#!/usr/bin/env nextflow

nextflow.enable.dsl = 2

include { FASTQC }              from './modules/fastqc'
include { MULTIQC }             from './modules/multiqc'
include { MIXCR }               from './modules/mixcr'
include { REPERTOIRE_ANALYSIS } from './modules/repertoire_analysis'
include { BIOLOGICAL_SUMMARY }  from './modules/biological_summary'

workflow {

    ch_samples = Channel
        .fromPath(params.samplesheet, checkIfExists: true)
        .splitCsv(header: true)
        .map { row ->

            def meta = [
                id            : row.sample_id,
                run_accession : row.run_accession,
                biosample     : row.biosample,
                geo_sample    : row.geo_sample,
                tissue        : row.tissue,
                timepoint     : row.timepoint as Integer,
                clinical_state: row.clinical_state,
                pd1_status    : row.pd1_status,
                assay         : row.assay,
                receptor_chain: row.receptor_chain,
                layout        : row.layout
            ]

            def r1 = file(
                "${params.reads_dir}/${row.run_accession}_1.fastq.gz",
                checkIfExists: true
            )

            def r2 = file(
                "${params.reads_dir}/${row.run_accession}_2.fastq.gz",
                checkIfExists: true
            )

            tuple(meta, r1, r2)
        }

    /*
     * Raw QC
     */
    FASTQC(ch_samples)

    ch_multiqc_input = FASTQC.out.reports
        .map { meta, html, zip -> [html, zip] }
        .flatten()
        .collect()

    MULTIQC(ch_multiqc_input)

    /*
     * MiXCR
     */
    MIXCR(ch_samples)

    /*
     * Collect TRB clonotype files only AFTER MIXCR runs
     */
    ch_trb_clones = MIXCR.out.clones
        .map { meta, clones -> clones }
        .collect()

    /*
     * Repertoire analysis
     */
    REPERTOIRE_ANALYSIS(ch_trb_clones)

    /*
     * Biological interpretation
     */
    BIOLOGICAL_SUMMARY(
        REPERTOIRE_ANALYSIS.out.tables
    )
}