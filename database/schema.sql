PRAGMA foreign_keys = ON;

CREATE TABLE samples (
    sample_id TEXT PRIMARY KEY,
    tissue TEXT NOT NULL,
    timepoint TEXT NOT NULL,
    clinical_stage TEXT NOT NULL
);

CREATE TABLE clonotypes (
    clonotype_id INTEGER PRIMARY KEY AUTOINCREMENT,
    sample_id TEXT NOT NULL,
    cdr3_aa TEXT NOT NULL,
    clone_count INTEGER,
    clone_fraction REAL,
    v_gene TEXT,
    j_gene TEXT,
    FOREIGN KEY (sample_id) REFERENCES samples(sample_id)
);

CREATE TABLE diversity_metrics (
    sample_id TEXT PRIMARY KEY,
    productive_richness INTEGER,
    shannon REAL,
    simpson REAL,
    clonality REAL,
    top1_fraction REAL,
    top10_fraction REAL,
    top100_fraction REAL,
    FOREIGN KEY (sample_id) REFERENCES samples(sample_id)
);

CREATE TABLE mixcr_qc (
    sample_id TEXT PRIMARY KEY,
    aligned_reads_pct REAL,
    off_target_pct REAL,
    reads_used_pct REAL,
    no_vj_hits_pct REAL,
    no_cdr3_pct REAL,
    low_quality_drop_pct REAL,
    trb_clonotypes INTEGER,
    FOREIGN KEY (sample_id) REFERENCES samples(sample_id)
);

CREATE TABLE tumor_pbmc_overlap (
    stage TEXT PRIMARY KEY,
    pbmc_sample TEXT,
    tumor_sample TEXT,
    pbmc_clonotypes INTEGER,
    tumor_clonotypes INTEGER,
    shared_clonotypes INTEGER,
    jaccard REAL
);

CREATE TABLE pairwise_jaccard (
    sample_a TEXT,
    sample_b TEXT,
    jaccard REAL,
    PRIMARY KEY (sample_a, sample_b)
);

CREATE TABLE pbmc_longitudinal (
    cdr3_aa TEXT PRIMARY KEY,
    pbmc_pre REAL,
    pbmc_relapse REAL,
    pbmc_progression REAL,
    max_fraction REAL,
    detected_timepoints INTEGER
);

CREATE INDEX idx_clonotypes_sample
ON clonotypes(sample_id);

CREATE INDEX idx_clonotypes_cdr3
ON clonotypes(cdr3_aa);

CREATE INDEX idx_clonotypes_fraction
ON clonotypes(clone_fraction);
