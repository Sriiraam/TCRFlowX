from pathlib import Path
import re
import pandas as pd

samples = [
    "PBMC_PRE",
    "TUMOR_PRE",
    "PBMC_RELAPSE",
    "PBMC_PROGRESSION",
    "TUMOR_PROGRESSION"
]

rows = []

for sample in samples:
    qc_file = Path(f"results/mixcr/{sample}/{sample}.qc.txt")
    text = qc_file.read_text()

    def grab(label):
        m = re.search(rf"{re.escape(label)}:\s+([\d.]+)%", text)
        return float(m.group(1)) if m else None

    clone_file = Path(
        f"results/mixcr/{sample}/{sample}.clones_TRB.tsv"
    )

    clonotypes = sum(1 for _ in clone_file.open()) - 1

    rows.append({
        "sample_id": sample,
        "aligned_reads_pct": grab("Successfully aligned reads"),
        "off_target_pct": grab("Off target (non TCR/IG) reads"),
        "reads_used_in_clonotypes_pct": grab("Reads used in clonotypes"),
        "no_v_or_j_hits_pct": grab("Reads with no V or J hits"),
        "no_cdr3_pct": grab("Alignments that do not cover CDR3"),
        "low_quality_drop_pct": grab(
            "Alignments dropped due to low sequence quality"
        ),
        "trb_clonotypes": clonotypes
    })

df = pd.DataFrame(rows)

out = Path("results/mixcr/mixcr_qc_summary.tsv")
df.to_csv(out, sep="\t", index=False)

print(df.to_string(index=False))
