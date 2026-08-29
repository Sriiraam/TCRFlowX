include { MIXCR }               from '../../modules/mixcr'
include { REPERTOIRE_ANALYSIS } from '../../modules/repertoire_analysis'
include { BIOLOGICAL_SUMMARY }  from '../../modules/biological_summary'

workflow REPERTOIRE_WORKFLOW {

    take:
    samples_ch

    main:

    MIXCR(samples_ch)

    trb_clones_ch = MIXCR.out.clones
        .map { meta, clones -> clones }
        .collect()

    REPERTOIRE_ANALYSIS(trb_clones_ch)

    BIOLOGICAL_SUMMARY(
        REPERTOIRE_ANALYSIS.out.tables
    )
}
