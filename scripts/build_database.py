#!/usr/bin/env python3

import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB = ROOT / "database" / "tcrflowx.db"
SCHEMA = ROOT / "database" / "schema.sql"

SAMPLES = {
    "PBMC_PRE": ("PBMC", "T1", "PRE"),
    "TUMOR_PRE": ("Tumor", "T1", "PRE"),
    "PBMC_RELAPSE": ("PBMC", "T4", "RELAPSE"),
    "PBMC_PROGRESSION": ("PBMC", "T6", "PROGRESSION"),
    "TUMOR_PROGRESSION": ("Tumor", "T6", "PROGRESSION"),
}


def first_present(row, candidates, default=""):
    for name in candidates:
        if name in row and row[name] not in ("", None):
            return row[name]
    return default


def clean_gene(value):
    if not value:
        return None
    # MiXCR hit fields may look like TRBV7-9*00(123.4)
    return value.split("(")[0].split(",")[0]


def build_database():
    if DB.exists():
        DB.unlink()

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.executescript(SCHEMA.read_text())

    # ---------------------------------------------------------
    # Samples
    # ---------------------------------------------------------
    for sample_id, (tissue, timepoint, stage) in SAMPLES.items():
        cur.execute(
            """
            INSERT INTO samples
            (sample_id, tissue, timepoint, clinical_stage)
            VALUES (?, ?, ?, ?)
            """,
            (sample_id, tissue, timepoint, stage),
        )

    # ---------------------------------------------------------
    # MiXCR clonotypes
    # ---------------------------------------------------------
    for sample_id in SAMPLES:
        path = (
            ROOT
            / "results"
            / "mixcr"
            / sample_id
            / f"{sample_id}.clones_TRB.tsv"
        )

        if not path.exists():
            print(f"WARNING: missing {path}")
            continue

        with path.open() as fh:
            reader = csv.DictReader(fh, delimiter="\t")

            inserted = 0

            for row in reader:
                cdr3 = first_present(
                    row,
                    [
                        "aaSeqCDR3",
                        "cdr3aa",
                        "aaSeqImputedCDR3",
                        "aminoAcidSeqCDR3",
                    ],
                )

                if not cdr3:
                    continue

                count = first_present(
                    row,
                    ["readCount", "cloneCount", "count", "Clone count"],
                    "0",
                )

                fraction = first_present(
                    row,
                    ["readFraction", "cloneFraction", "fraction", "Clone fraction"],
                    "0",
                )

                v_gene = first_present(
                    row,
                    [
                        "bestVHit",
                        "allVHitsWithScore",
                        "vGene",
                        "V",
                    ],
                )

                j_gene = first_present(
                    row,
                    [
                        "bestJHit",
                        "allJHitsWithScore",
                        "jGene",
                        "J",
                    ],
                )

                try:
                    count = int(float(count))
                except (ValueError, TypeError):
                    count = 0

                try:
                    fraction = float(fraction)
                except (ValueError, TypeError):
                    fraction = 0.0

                cur.execute(
                    """
                    INSERT INTO clonotypes
                    (
                        sample_id,
                        cdr3_aa,
                        clone_count,
                        clone_fraction,
                        v_gene,
                        j_gene
                    )
                    VALUES (?, ?, ?, ?, ?, ?)
                    """,
                    (
                        sample_id,
                        cdr3,
                        count,
                        fraction,
                        clean_gene(v_gene),
                        clean_gene(j_gene),
                    ),
                )

                inserted += 1

        print(f"{sample_id}: {inserted} clonotypes")

    # ---------------------------------------------------------
    # Diversity metrics
    # ---------------------------------------------------------
    path = ROOT / "results/repertoire/tables/diversity_clonality.tsv"

    with path.open() as fh:
        reader = csv.DictReader(fh, delimiter="\t")

        for r in reader:
            cur.execute(
                """
                INSERT INTO diversity_metrics VALUES
                (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    r["sample"],
                    int(r["productive_richness"]),
                    float(r["shannon"]),
                    float(r["simpson"]),
                    float(r["clonality"]),
                    float(r["top1_fraction"]),
                    float(r["top10_fraction"]),
                    float(r["top100_fraction"]),
                ),
            )

    # ---------------------------------------------------------
    # MiXCR QC
    # ---------------------------------------------------------
    path = ROOT / "results/mixcr/mixcr_qc_summary.tsv"

    with path.open() as fh:
        reader = csv.DictReader(fh, delimiter="\t")

        for r in reader:
            cur.execute(
                """
                INSERT INTO mixcr_qc VALUES
                (?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    r["sample_id"],
                    float(r["aligned_reads_pct"]),
                    float(r["off_target_pct"]),
                    float(r["reads_used_in_clonotypes_pct"]),
                    float(r["no_v_or_j_hits_pct"]),
                    float(r["no_cdr3_pct"]),
                    float(r["low_quality_drop_pct"]),
                    int(r["trb_clonotypes"]),
                ),
            )

    # ---------------------------------------------------------
    # PBMC longitudinal clones
    # ---------------------------------------------------------
    path = (
        ROOT
        / "results/repertoire/tables/pbmc_longitudinal_clonotypes.tsv"
    )

    with path.open() as fh:
        reader = csv.DictReader(fh, delimiter="\t")

        for r in reader:
            cur.execute(
                """
                INSERT INTO pbmc_longitudinal VALUES
                (?, ?, ?, ?, ?, ?)
                """,
                (
                    r["cdr3aa"],
                    float(r["PBMC_PRE"]),
                    float(r["PBMC_RELAPSE"]),
                    float(r["PBMC_PROGRESSION"]),
                    float(r["max_fraction"]),
                    int(r["detected_timepoints"]),
                ),
            )

    # ---------------------------------------------------------
    # Tumor-PBMC overlap
    # ---------------------------------------------------------
    path = ROOT / "results/repertoire/tables/tumor_pbmc_overlap.tsv"

    with path.open() as fh:
        reader = csv.reader(fh, delimiter="\t")
        rows = list(reader)

    header = rows[0]

    for row in rows[1:]:
        if not row:
            continue

        # Read by position because the displayed header can occasionally
        # render shared_clonotypes / jaccard without visible spacing.
        cur.execute(
            """
            INSERT INTO tumor_pbmc_overlap VALUES
            (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                row[0],
                row[1],
                row[2],
                int(row[3]),
                int(row[4]),
                int(row[5]),
                float(row[6]),
            ),
        )

    # ---------------------------------------------------------
    # Pairwise Jaccard matrix -> relational table
    # ---------------------------------------------------------
    path = ROOT / "results/repertoire/tables/pairwise_jaccard.tsv"

    with path.open() as fh:
        reader = csv.reader(fh, delimiter="\t")
        rows = list(reader)

    sample_names = rows[0][1:]

    for row in rows[1:]:
        sample_a = row[0]

        for sample_b, value in zip(sample_names, row[1:]):
            cur.execute(
                """
                INSERT INTO pairwise_jaccard
                (sample_a, sample_b, jaccard)
                VALUES (?, ?, ?)
                """,
                (sample_a, sample_b, float(value)),
            )

    con.commit()

    print("\nDatabase created successfully:")
    print(DB)

    tables = [
        "samples",
        "clonotypes",
        "diversity_metrics",
        "mixcr_qc",
        "tumor_pbmc_overlap",
        "pairwise_jaccard",
        "pbmc_longitudinal",
    ]

    print("\nRow counts:")

    for table in tables:
        n = cur.execute(
            f"SELECT COUNT(*) FROM {table}"
        ).fetchone()[0]

        print(f"{table:25s} {n}")

    con.close()


if __name__ == "__main__":
    build_database()
