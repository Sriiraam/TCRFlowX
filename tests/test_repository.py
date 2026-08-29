from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_core_repository_files_exist():
    required = [
        "main.nf",
        "nextflow.config",
        "requirements.txt",
        "LICENSE",
        "CITATION.cff",
        "CHANGELOG.md",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
        "SECURITY.md",
    ]

    for item in required:
        assert (ROOT / item).exists(), f"Missing repository file: {item}"


def test_nextflow_modules_exist():
    expected = [
        "fastqc.nf",
        "multiqc.nf",
        "mixcr.nf",
        "repertoire_analysis.nf",
        "biological_summary.nf",
    ]

    for item in expected:
        assert (ROOT / "modules" / item).exists(), f"Missing module: {item}"


def test_subworkflows_exist():
    expected = [
        "qc.nf",
        "repertoire.nf",
    ]

    for item in expected:
        assert (
            ROOT / "workflow" / "subworkflows" / item
        ).exists(), f"Missing subworkflow: {item}"


def test_config_profiles_exist():
    expected = [
        "local.config",
        "docker.config",
        "slurm.config",
        "k8s.config",
        "azure.config",
    ]

    for item in expected:
        assert (ROOT / "conf" / item).exists(), f"Missing config profile: {item}"
