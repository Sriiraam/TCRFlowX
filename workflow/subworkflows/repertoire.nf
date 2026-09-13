include { MIXCR }               from '../../modules/mixcr'
include { REPERTOIRE_ANALYSIS } from '../../modules/repertoire_analysis'
include { BIOLOGICAL_SUMMARY }  from '../../modules/biological_summary'
include { FORMAL_QC }            from '../../modules/formal_qc'

workflow REPERTOIRE_WORKFLOW {

    take:
    samples_ch

    main:

    MIXCR(samples_ch)

    /*
     * Repertoire-analysis handoff
     */
    trb_clones_ch = MIXCR.out.clones
        .map { meta, clones -> clones }
        .collect()

    REPERTOIRE_ANALYSIS(
        trb_clones_ch
    )

    BIOLOGICAL_SUMMARY(
        REPERTOIRE_ANALYSIS.out.tables
    )

    /*
     * Formal QC handoff
     *
     * QC operates directly on staged MiXCR outputs rather than
     * reading previously published files from results/.
     */
    mixcr_qc_files_ch = MIXCR.out.reports
        .map { meta, align, assemble, qc -> qc }
        .collect()

    qc_clone_files_ch = MIXCR.out.clones
        .map { meta, clones -> clones }
        .collect()

    FORMAL_QC(
        mixcr_qc_files_ch,
        qc_clone_files_ch
    )
}
