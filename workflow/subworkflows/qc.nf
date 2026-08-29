include { FASTQC }  from '../../modules/fastqc'
include { MULTIQC } from '../../modules/multiqc'

workflow QC_WORKFLOW {

    take:
    samples_ch

    main:

    FASTQC(samples_ch)

    multiqc_input_ch = FASTQC.out.reports
        .map { meta, html, zip -> [html, zip] }
        .flatten()
        .collect()

    MULTIQC(multiqc_input_ch)
}
