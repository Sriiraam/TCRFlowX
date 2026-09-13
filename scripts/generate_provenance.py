from pathlib import Path
from datetime import datetime, timezone
import hashlib
import os
import platform
import subprocess


def command(cmd):
    try:
        return subprocess.check_output(
            cmd,
            text=True,
            stderr=subprocess.STDOUT
        ).strip()
    except Exception:
        return "unavailable"


def sha256(path):
    path = Path(path)

    if not path.exists():
        return "unavailable"

    h = hashlib.sha256()

    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)

    return h.hexdigest()


project_dir = Path(
    os.environ.get("TCRFLOWX_PROJECT_DIR", ".")
).resolve()

profile = os.environ.get(
    "TCRFLOWX_PROFILE",
    "unknown"
)

samplesheet = project_dir / "metadata/samplesheet.csv"
input_manifest = project_dir / "metadata/input_integrity.sha256"
software_lock = project_dir / "metadata/software_versions.lock.tsv"

git_commit = command(
    ["git", "-C", str(project_dir), "rev-parse", "HEAD"]
)

git_branch = command(
    ["git", "-C", str(project_dir), "branch", "--show-current"]
)

git_status = command(
    ["git", "-C", str(project_dir), "status", "--porcelain"]
)

git_state = "clean" if git_status == "" else "dirty"

nextflow_version = command(
    ["nextflow", "-version"]
)

java_version = command(
    ["java", "-version"]
)

timestamp = datetime.now(
    timezone.utc
).isoformat()

rows = [
    ("run_timestamp_utc", timestamp),
    ("git_commit", git_commit),
    ("git_branch", git_branch),
    ("git_state", git_state),
    ("execution_profile", profile),
    (
        "nextflow_version",
        nextflow_version.replace("\n", " | ")
    ),
    (
        "java_version",
        java_version.replace("\n", " | ")
    ),
    ("python_version", platform.python_version()),
    (
        "mixcr_preset",
        "invivoscribe-human-dna-trb-lymphotrack"
    ),
    (
        "samplesheet",
        str(samplesheet.relative_to(project_dir))
    ),
    (
        "samplesheet_sha256",
        sha256(samplesheet)
    ),
    (
        "input_integrity_manifest",
        str(input_manifest.relative_to(project_dir))
    ),
    (
        "input_integrity_manifest_sha256",
        sha256(input_manifest)
    ),
    (
        "software_lock",
        str(software_lock.relative_to(project_dir))
    ),
    (
        "software_lock_sha256",
        sha256(software_lock)
    ),
]


with open("run_provenance.tsv", "w") as fh:
    fh.write("field\tvalue\n")

    for key, value in rows:
        clean_value = str(value).replace("\t", " ").replace("\n", " ")
        fh.write(f"{key}\t{clean_value}\n")


with open("run_provenance.md", "w") as fh:
    fh.write("# TCRFlowX Run Provenance\n\n")

    fh.write(
        "Automatically generated execution-level provenance "
        "for this TCRFlowX workflow run.\n\n"
    )

    fh.write("| Field | Value |\n")
    fh.write("|---|---|\n")

    for key, value in rows:
        safe = (
            str(value)
            .replace("|", "\\|")
            .replace("\n", " ")
        )

        fh.write(f"| {key} | `{safe}` |\n")


print("Generated run_provenance.tsv")
print("Generated run_provenance.md")
print(f"Git commit: {git_commit}")
print(f"Git state: {git_state}")
print(f"Profile: {profile}")
