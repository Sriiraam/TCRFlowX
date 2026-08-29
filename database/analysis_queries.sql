-- =========================================================
-- TCRFlowX SQL Repertoire Analysis
-- =========================================================


-- 1. Sample metadata
SELECT *
FROM samples;


-- 2. Rank samples by clonality
SELECT
    sample_id,
    productive_richness,
    ROUND(shannon, 3) AS shannon,
    ROUND(clonality, 3) AS clonality
FROM diversity_metrics
ORDER BY clonality DESC;


-- 3. Top 10 clonotypes in each sample
SELECT *
FROM (
    SELECT
        sample_id,
        cdr3_aa,
        clone_count,
        ROUND(clone_fraction * 100, 2) AS frequency_pct,
        ROW_NUMBER() OVER (
            PARTITION BY sample_id
            ORDER BY clone_fraction DESC
        ) AS clone_rank
    FROM clonotypes
)
WHERE clone_rank <= 10;


-- 4. Persistent PBMC clonotypes
SELECT
    cdr3_aa,
    ROUND(pbmc_pre * 100, 2) AS pre_pct,
    ROUND(pbmc_relapse * 100, 2) AS relapse_pct,
    ROUND(pbmc_progression * 100, 2) AS progression_pct
FROM pbmc_longitudinal
WHERE detected_timepoints = 3
ORDER BY max_fraction DESC
LIMIT 20;


-- 5. Clones expanding from PRE to PROGRESSION
SELECT
    cdr3_aa,
    ROUND(pbmc_pre * 100, 3) AS pre_pct,
    ROUND(pbmc_progression * 100, 3) AS progression_pct,
    ROUND(
        (pbmc_progression - pbmc_pre) * 100,
        3
    ) AS change_pct
FROM pbmc_longitudinal
WHERE pbmc_pre > 0
  AND pbmc_progression > pbmc_pre
ORDER BY change_pct DESC
LIMIT 20;


-- 6. Tumor-PBMC repertoire overlap
SELECT
    stage,
    shared_clonotypes,
    ROUND(jaccard, 3) AS jaccard
FROM tumor_pbmc_overlap
ORDER BY jaccard DESC;


-- 7. JOIN metadata with diversity results
SELECT
    s.sample_id,
    s.tissue,
    s.timepoint,
    s.clinical_stage,
    d.productive_richness,
    ROUND(d.clonality, 3) AS clonality
FROM samples s
JOIN diversity_metrics d
    ON s.sample_id = d.sample_id
ORDER BY d.clonality DESC;


-- 8. Average clonality by tissue
SELECT
    s.tissue,
    COUNT(*) AS samples,
    ROUND(AVG(d.clonality), 3) AS mean_clonality
FROM samples s
JOIN diversity_metrics d
    ON s.sample_id = d.sample_id
GROUP BY s.tissue;


-- 9. Best cross-sample repertoire similarities
SELECT
    sample_a,
    sample_b,
    ROUND(jaccard, 3) AS jaccard
FROM pairwise_jaccard
WHERE sample_a <> sample_b
ORDER BY jaccard DESC
LIMIT 10;


-- 10. CTE: classify longitudinal PBMC clones
WITH clone_dynamics AS (
    SELECT
        cdr3_aa,
        pbmc_pre,
        pbmc_relapse,
        pbmc_progression,
        CASE
            WHEN detected_timepoints = 3 THEN 'Persistent'
            WHEN pbmc_pre = 0
                 AND pbmc_relapse > 0 THEN 'Emergent'
            WHEN pbmc_pre > 0
                 AND pbmc_progression = 0 THEN 'Lost'
            ELSE 'Variable'
        END AS clone_status
    FROM pbmc_longitudinal
)
SELECT
    clone_status,
    COUNT(*) AS clonotypes
FROM clone_dynamics
GROUP BY clone_status
ORDER BY clonotypes DESC;
