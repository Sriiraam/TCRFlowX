from pathlib import Path
import re
import pandas as pd


def grab(text, label):
    m = re.search(
        rf"{re.escape(label)}:\s+([\d.]+)%",
        text
    )
    return float(m.group(1)) if m else None


def high_good(value, pass_min, warn_min):
    if value >= pass_min:
        return "PASS"
    if value >= warn_min:
        return "WARN"
    return "FAIL"


def low_good(value, pass_max, warn_max):
    if value <= pass_max:
        return "PASS"
    if value <= warn_max:
        return "WARN"
    return "FAIL"


def clonotype_status(value):
    if value >= 1000:
        return "PASS"
    if value >= 100:
        return "WARN"
    return "FAIL"


severity = {
    "PASS": 0,
    "WARN": 1,
    "FAIL": 2,
}


qc_files = sorted(Path(".").glob("*.qc.txt"))

if not qc_files:
    raise SystemExit("No MiXCR *.qc.txt files found")


rows = []

for qc_file in qc_files:

    sample = qc_file.name.removesuffix(".qc.txt")
    clone_file = Path(f"{sample}.clones_TRB.tsv")

    if not clone_file.exists():
        raise SystemExit(
            f"Missing clone table for {sample}: {clone_file}"
        )

    text = qc_file.read_text()

    clonotypes = sum(1 for _ in clone_file.open()) - 1

    rows.append({
        "sample_id": sample,
        "aligned_reads_pct": grab(
            text,
            "Successfully aligned reads"
        ),
        "off_target_pct": grab(
            text,
            "Off target (non TCR/IG) reads"
        ),
        "reads_used_in_clonotypes_pct": grab(
            text,
            "Reads used in clonotypes"
        ),
        "no_v_or_j_hits_pct": grab(
            text,
            "Reads with no V or J hits"
        ),
        "no_cdr3_pct": grab(
            text,
            "Alignments that do not cover CDR3"
        ),
        "low_quality_drop_pct": grab(
            text,
            "Alignments dropped due to low sequence quality"
        ),
        "trb_clonotypes": clonotypes,
    })


df = pd.DataFrame(rows).sort_values("sample_id")

df.to_csv(
    "mixcr_qc_summary.tsv",
    sep="\t",
    index=False
)


formal_rows = []

for _, row in df.iterrows():

    metrics = {
        "aligned_reads_status": high_good(
            row["aligned_reads_pct"],
            80.0,
            60.0
        ),
        "off_target_status": low_good(
            row["off_target_pct"],
            20.0,
            40.0
        ),
        "reads_used_status": high_good(
            row["reads_used_in_clonotypes_pct"],
            70.0,
            50.0
        ),
        "no_v_or_j_status": low_good(
            row["no_v_or_j_hits_pct"],
            5.0,
            10.0
        ),
        "no_cdr3_status": low_good(
            row["no_cdr3_pct"],
            10.0,
            20.0
        ),
        "low_quality_status": low_good(
            row["low_quality_drop_pct"],
            5.0,
            10.0
        ),
        "clonotype_status": clonotype_status(
            row["trb_clonotypes"]
        ),
    }

    overall = max(
        metrics.values(),
        key=lambda x: severity[x]
    )

    formal_rows.append({
        **row.to_dict(),
        **metrics,
        "overall_qc": overall,
    })


out = pd.DataFrame(formal_rows)

out.to_csv(
    "formal_qc_summary.tsv",
    sep="\t",
    index=False
)


with open("formal_qc_report.md", "w") as fh:

    fh.write("# TCRFlowX Formal QC Report\n\n")

    fh.write(
        "This report applies reproducible PASS/WARN/FAIL "
        "classification to MiXCR repertoire-reconstruction metrics.\n\n"
    )

    fh.write(
        "A FAIL indicates a sample requiring explicit QC review; "
        "it does not automatically invalidate downstream biological "
        "interpretation.\n\n"
    )

    fh.write("## Thresholds\n\n")

    fh.write(
        "| Metric | PASS | WARN | FAIL |\n"
        "|---|---|---|---|\n"
        "| Successfully aligned reads | >=80% | 60-<80% | <60% |\n"
        "| Reads used in clonotypes | >=70% | 50-<70% | <50% |\n"
        "| Off-target reads | <=20% | >20-40% | >40% |\n"
        "| Reads with no V/J hits | <=5% | >5-10% | >10% |\n"
        "| Alignments without CDR3 | <=10% | >10-20% | >20% |\n"
        "| Low-quality alignment drop | <=5% | >5-10% | >10% |\n"
        "| TRB clonotypes | >=1000 | 100-999 | <100 |\n\n"
    )

    fh.write("## Sample Results\n\n")

    fh.write(
        "| Sample | Aligned | Used in clonotypes | "
        "Off-target | TRB clonotypes | Overall |\n"
    )

    fh.write("|---|---:|---:|---:|---:|---|\n")

    for _, row in out.iterrows():
        fh.write(
            f"| {row['sample_id']} "
            f"| {row['aligned_reads_pct']:.2f}% "
            f"| {row['reads_used_in_clonotypes_pct']:.2f}% "
            f"| {row['off_target_pct']:.2f}% "
            f"| {int(row['trb_clonotypes'])} "
            f"| **{row['overall_qc']}** |\n"
        )

    fh.write("\n## FastQC Interpretation Policy\n\n")

    fh.write(
        "TCRFlowX treats FastQC duplication, overrepresented-sequence, "
        "sequence-composition and GC-distribution warnings/failures as "
        "contextual for targeted TCR repertoire sequencing rather than "
        "automatic sample failure. Genuine clonal expansion and assay "
        "design can produce these patterns.\n\n"
    )

    fh.write(
        "Per-base sequence quality, adapter contamination, N content and "
        "other conventional sequencing-quality metrics remain reviewable "
        "technical QC signals.\n"
    )


print(
    out[
        [
            "sample_id",
            "aligned_reads_pct",
            "reads_used_in_clonotypes_pct",
            "off_target_pct",
            "trb_clonotypes",
            "overall_qc",
        ]
    ].to_string(index=False)
)
