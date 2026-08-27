suppressPackageStartupMessages({
  library(dplyr)
  library(tidyr)
  library(ggplot2)
})

# ---------------------------------------------------------
# TCRFlowX — Phase 8 Repertoire Analysis
# ---------------------------------------------------------

samples <- c(
  "PBMC_PRE",
  "TUMOR_PRE",
  "PBMC_RELAPSE",
  "PBMC_PROGRESSION",
  "TUMOR_PROGRESSION"
)

outdir <- "results/repertoire"
dir.create(outdir, recursive = TRUE, showWarnings = FALSE)
dir.create(file.path(outdir, "tables"), showWarnings = FALSE)
dir.create(file.path(outdir, "figures"), showWarnings = FALSE)

# ---------------------------------------------------------
# Load MiXCR TRB clonotypes
# ---------------------------------------------------------

load_sample <- function(sample) {

  path <- paste0(
    "results/mixcr/",
    sample,
    "/",
    sample,
    ".clones_TRB.tsv"
  )

  x <- read.delim(
    path,
    check.names = FALSE,
    stringsAsFactors = FALSE
  )

  x <- x %>%
    transmute(
      sample = sample,
      count = as.numeric(readCount),
      fraction = as.numeric(readFraction),
      cdr3aa = aaSeqCDR3,
      v_gene = bestVHit,
      j_gene = bestJHit
    ) %>%
    filter(
      !is.na(cdr3aa),
      cdr3aa != "",
      !grepl("[*_]", cdr3aa)
    )

  x
}

repertoires <- lapply(samples, load_sample)
names(repertoires) <- samples

all_clones <- bind_rows(repertoires)

# ---------------------------------------------------------
# 1. Diversity + clonality
# ---------------------------------------------------------

diversity_table <- bind_rows(
  lapply(samples, function(sample) {

    x <- repertoires[[sample]]

    p <- x$fraction
    p <- p[p > 0]
    p <- p / sum(p)

    richness <- length(p)

    shannon <- -sum(p * log(p))

    normalized_shannon <-
      ifelse(
        richness > 1,
        shannon / log(richness),
        0
      )

    clonality <- 1 - normalized_shannon

    simpson <- 1 - sum(p^2)

    top1 <- max(p)

    top10 <- sum(sort(p, decreasing = TRUE)[
      seq_len(min(10, length(p)))
    ])

    top100 <- sum(sort(p, decreasing = TRUE)[
      seq_len(min(100, length(p)))
    ])

    data.frame(
      sample = sample,
      productive_richness = richness,
      shannon = shannon,
      simpson = simpson,
      clonality = clonality,
      top1_fraction = top1,
      top10_fraction = top10,
      top100_fraction = top100
    )
  })
)

write.table(
  diversity_table,
  file.path(outdir, "tables", "diversity_clonality.tsv"),
  sep = "\t",
  row.names = FALSE,
  quote = FALSE
)

print(diversity_table)

# ---------------------------------------------------------
# 2. Top clonotypes
# ---------------------------------------------------------

top_clonotypes <- all_clones %>%
  group_by(sample) %>%
  arrange(desc(fraction), .by_group = TRUE) %>%
  slice_head(n = 20) %>%
  mutate(rank = row_number()) %>%
  ungroup()

write.table(
  top_clonotypes,
  file.path(outdir, "tables", "top20_clonotypes.tsv"),
  sep = "\t",
  row.names = FALSE,
  quote = FALSE
)

# ---------------------------------------------------------
# 3. TRBV usage
# ---------------------------------------------------------

v_usage <- all_clones %>%
  filter(!is.na(v_gene), v_gene != "") %>%
  group_by(sample, v_gene) %>%
  summarise(
    frequency = sum(fraction),
    .groups = "drop"
  )

write.table(
  v_usage,
  file.path(outdir, "tables", "trbv_usage.tsv"),
  sep = "\t",
  row.names = FALSE,
  quote = FALSE
)

# ---------------------------------------------------------
# 4. TRBJ usage
# ---------------------------------------------------------

j_usage <- all_clones %>%
  filter(!is.na(j_gene), j_gene != "") %>%
  group_by(sample, j_gene) %>%
  summarise(
    frequency = sum(fraction),
    .groups = "drop"
  )

write.table(
  j_usage,
  file.path(outdir, "tables", "trbj_usage.tsv"),
  sep = "\t",
  row.names = FALSE,
  quote = FALSE
)

# ---------------------------------------------------------
# 5. Pairwise repertoire overlap
# Productive CDR3 AA Jaccard
# ---------------------------------------------------------

jaccard <- matrix(
  NA,
  nrow = length(samples),
  ncol = length(samples),
  dimnames = list(samples, samples)
)

for (i in seq_along(samples)) {

  a <- unique(repertoires[[samples[i]]]$cdr3aa)

  for (j in seq_along(samples)) {

    b <- unique(repertoires[[samples[j]]]$cdr3aa)

    jaccard[i, j] <-
      length(intersect(a, b)) /
      length(union(a, b))
  }
}

write.table(
  jaccard,
  file.path(outdir, "tables", "pairwise_jaccard.tsv"),
  sep = "\t",
  quote = FALSE,
  col.names = NA
)

# ---------------------------------------------------------
# 6. PBMC longitudinal tracking
# PRE → RELAPSE → PROGRESSION
# ---------------------------------------------------------

pbmc_samples <- c(
  "PBMC_PRE",
  "PBMC_RELAPSE",
  "PBMC_PROGRESSION"
)

pbmc_tracking <- all_clones %>%
  filter(sample %in% pbmc_samples) %>%
  group_by(cdr3aa, sample) %>%
  summarise(
    fraction = sum(fraction),
    .groups = "drop"
  ) %>%
  pivot_wider(
    names_from = sample,
    values_from = fraction,
    values_fill = 0
  ) %>%
  mutate(
    max_fraction = pmax(
      PBMC_PRE,
      PBMC_RELAPSE,
      PBMC_PROGRESSION
    ),
    detected_timepoints =
      (PBMC_PRE > 0) +
      (PBMC_RELAPSE > 0) +
      (PBMC_PROGRESSION > 0)
  ) %>%
  arrange(desc(max_fraction))

write.table(
  pbmc_tracking,
  file.path(
    outdir,
    "tables",
    "pbmc_longitudinal_clonotypes.tsv"
  ),
  sep = "\t",
  row.names = FALSE,
  quote = FALSE
)

# ---------------------------------------------------------
# 7. Tumor longitudinal tracking
# ---------------------------------------------------------

tumor_tracking <- all_clones %>%
  filter(
    sample %in% c(
      "TUMOR_PRE",
      "TUMOR_PROGRESSION"
    )
  ) %>%
  group_by(cdr3aa, sample) %>%
  summarise(
    fraction = sum(fraction),
    .groups = "drop"
  ) %>%
  pivot_wider(
    names_from = sample,
    values_from = fraction,
    values_fill = 0
  ) %>%
  mutate(
    max_fraction = pmax(
      TUMOR_PRE,
      TUMOR_PROGRESSION
    ),
    fold_change =
      (TUMOR_PROGRESSION + 1e-8) /
      (TUMOR_PRE + 1e-8)
  ) %>%
  arrange(desc(max_fraction))

write.table(
  tumor_tracking,
  file.path(
    outdir,
    "tables",
    "tumor_longitudinal_clonotypes.tsv"
  ),
  sep = "\t",
  row.names = FALSE,
  quote = FALSE
)

# ---------------------------------------------------------
# 8. Tumor ↔ PBMC matched-timepoint overlap
# ---------------------------------------------------------

overlap_pairs <- list(
  PRE = c(
    "PBMC_PRE",
    "TUMOR_PRE"
  ),
  PROGRESSION = c(
    "PBMC_PROGRESSION",
    "TUMOR_PROGRESSION"
  )
)

matched_overlap <- bind_rows(
  lapply(names(overlap_pairs), function(stage) {

    pair <- overlap_pairs[[stage]]

    a <- repertoires[[pair[1]]]
    b <- repertoires[[pair[2]]]

    a_set <- unique(a$cdr3aa)
    b_set <- unique(b$cdr3aa)

    shared <- intersect(a_set, b_set)

    data.frame(
      stage = stage,
      pbmc_sample = pair[1],
      tumor_sample = pair[2],
      pbmc_clonotypes = length(a_set),
      tumor_clonotypes = length(b_set),
      shared_clonotypes = length(shared),
      jaccard =
        length(shared) /
        length(union(a_set, b_set))
    )
  })
)

write.table(
  matched_overlap,
  file.path(
    outdir,
    "tables",
    "tumor_pbmc_overlap.tsv"
  ),
  sep = "\t",
  row.names = FALSE,
  quote = FALSE
)

print(matched_overlap)

# ---------------------------------------------------------
# FIGURES
# ---------------------------------------------------------

# Diversity
p1 <- ggplot(
  diversity_table,
  aes(
    x = reorder(sample, shannon),
    y = shannon
  )
) +
  geom_col() +
  coord_flip() +
  labs(
    title = "TCRβ Repertoire Shannon Diversity",
    x = NULL,
    y = "Shannon diversity"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  file.path(
    outdir,
    "figures",
    "shannon_diversity.png"
  ),
  p1,
  width = 8,
  height = 5,
  dpi = 300
)

# Clonality
p2 <- ggplot(
  diversity_table,
  aes(
    x = reorder(sample, clonality),
    y = clonality
  )
) +
  geom_col() +
  coord_flip() +
  labs(
    title = "TCRβ Repertoire Clonality",
    x = NULL,
    y = "Clonality"
  ) +
  theme_minimal(base_size = 12)

ggsave(
  file.path(
    outdir,
    "figures",
    "clonality.png"
  ),
  p2,
  width = 8,
  height = 5,
  dpi = 300
)

# Top clonotypes
p3 <- ggplot(
  top_clonotypes,
  aes(
    x = reorder(cdr3aa, fraction),
    y = fraction
  )
) +
  geom_col() +
  coord_flip() +
  facet_wrap(
    ~ sample,
    scales = "free_y"
  ) +
  labs(
    title = "Top TCRβ Clonotypes",
    x = "CDR3 amino-acid sequence",
    y = "Clone fraction"
  ) +
  theme_minimal(base_size = 9)

ggsave(
  file.path(
    outdir,
    "figures",
    "top20_clonotypes.png"
  ),
  p3,
  width = 12,
  height = 10,
  dpi = 300
)

# Top V genes
top_v <- v_usage %>%
  group_by(v_gene) %>%
  summarise(total = sum(frequency)) %>%
  arrange(desc(total)) %>%
  slice_head(n = 15) %>%
  pull(v_gene)

p4 <- v_usage %>%
  filter(v_gene %in% top_v) %>%
  ggplot(
    aes(
      x = v_gene,
      y = frequency,
      fill = sample
    )
  ) +
  geom_col(position = "dodge") +
  coord_flip() +
  labs(
    title = "Top TRBV Gene Usage",
    x = "TRBV gene",
    y = "Repertoire frequency"
  ) +
  theme_minimal(base_size = 10)

ggsave(
  file.path(
    outdir,
    "figures",
    "trbv_usage.png"
  ),
  p4,
  width = 10,
  height = 7,
  dpi = 300
)

# J usage
p5 <- ggplot(
  j_usage,
  aes(
    x = j_gene,
    y = frequency,
    fill = sample
  )
) +
  geom_col(position = "dodge") +
  coord_flip() +
  labs(
    title = "TRBJ Gene Usage",
    x = "TRBJ gene",
    y = "Repertoire frequency"
  ) +
  theme_minimal(base_size = 10)

ggsave(
  file.path(
    outdir,
    "figures",
    "trbj_usage.png"
  ),
  p5,
  width = 10,
  height = 7,
  dpi = 300
)

# Pairwise Jaccard heatmap
jaccard_long <- as.data.frame(as.table(jaccard))

names(jaccard_long) <- c(
  "sample1",
  "sample2",
  "jaccard"
)

p6 <- ggplot(
  jaccard_long,
  aes(
    x = sample1,
    y = sample2,
    fill = jaccard
  )
) +
  geom_tile() +
  geom_text(
    aes(label = sprintf("%.2f", jaccard)),
    size = 3
  ) +
  labs(
    title = "Productive CDR3 Repertoire Overlap",
    x = NULL,
    y = NULL
  ) +
  theme_minimal(base_size = 10) +
  theme(
    axis.text.x =
      element_text(
        angle = 45,
        hjust = 1
      )
  )

ggsave(
  file.path(
    outdir,
    "figures",
    "pairwise_jaccard.png"
  ),
  p6,
  width = 8,
  height = 7,
  dpi = 300
)

# PBMC longitudinal top clones
pbmc_top <- pbmc_tracking %>%
  slice_head(n = 30) %>%
  select(
    cdr3aa,
    PBMC_PRE,
    PBMC_RELAPSE,
    PBMC_PROGRESSION
  ) %>%
  pivot_longer(
    -cdr3aa,
    names_to = "sample",
    values_to = "fraction"
  )

p7 <- ggplot(
  pbmc_top,
  aes(
    x = sample,
    y = reorder(cdr3aa, fraction),
    fill = fraction
  )
) +
  geom_tile() +
  labs(
    title = "Longitudinal PBMC TCRβ Clonotype Tracking",
    x = NULL,
    y = "CDR3"
  ) +
  theme_minimal(base_size = 9)

ggsave(
  file.path(
    outdir,
    "figures",
    "pbmc_longitudinal_heatmap.png"
  ),
  p7,
  width = 8,
  height = 10,
  dpi = 300
)

cat("\nTCRFlowX Phase 8 repertoire analysis complete.\n")
