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

    output:
    path "run_provenance.tsv"
    path "run_provenance.md"

    script:
    """
    export TCRFLOWX_PROJECT_DIR="${projectDir}"
    export TCRFLOWX_PROFILE="${execution_profile}"

    python ${projectDir}/scripts/generate_provenance.py
    """
}
