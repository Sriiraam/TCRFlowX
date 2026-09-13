process PROVENANCE {

    tag "run_provenance"

    cpus 1
    memory '512 MB'

    publishDir "${params.outdir}/provenance",
        mode: 'copy',
        overwrite: true

    input:
    val execution_profile
    val git_commit_fingerprint
    val git_state_fingerprint
    val runtime_samplesheet
    val runtime_reads_dir
    val runtime_outdir
    val runtime_input_manifest

    output:
    path "run_provenance.tsv"
    path "run_provenance.md"

    script:
    """
    export TCRFLOWX_PROJECT_DIR="${projectDir}"
    export TCRFLOWX_PROFILE="${execution_profile}"
    export TCRFLOWX_SAMPLESHEET="${runtime_samplesheet}"
    export TCRFLOWX_READS_DIR="${runtime_reads_dir}"
    export TCRFLOWX_OUTDIR="${runtime_outdir}"
    export TCRFLOWX_INPUT_MANIFEST="${runtime_input_manifest}"

    python ${projectDir}/scripts/generate_provenance.py
    """
}
