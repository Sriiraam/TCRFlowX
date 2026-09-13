#!/usr/bin/env nextflow

nextflow.enable.dsl = 2

include { QC_WORKFLOW }         from './workflow/subworkflows/qc'
include { REPERTOIRE_WORKFLOW } from './workflow/subworkflows/repertoire'
include { PROVENANCE }          from './modules/provenance'

workflow {

    /*
     * Build sample channel from metadata.
     */
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
     * Stage 1: sequencing quality control
     */
    QC_WORKFLOW(ch_samples)

    /*
     * Stage 2: TRB reconstruction and repertoire analysis
     */
    REPERTOIRE_WORKFLOW(ch_samples)

    /*
     * Stage 3: run-level provenance
     *
     * Git commit and working-tree state are explicit inputs so
     * provenance is regenerated when repository state changes.
     */
    def git_commit_fingerprint = [
        'git',
        '-C',
        projectDir.toString(),
        'rev-parse',
        'HEAD'
    ].execute().text.trim()

    def git_status_text = [
        'git',
        '-C',
        projectDir.toString(),
        'status',
        '--porcelain'
    ].execute().text.trim()

    def git_state_fingerprint =
        git_status_text ? "dirty:${git_status_text}" : "clean"

    PROVENANCE(
        workflow.profile ?: 'unknown',
        git_commit_fingerprint,
        git_state_fingerprint
    )
}
