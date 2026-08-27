# TCRFlowX R dependency installer

options(repos = c(CRAN = "https://cloud.r-project.org"))

required_packages <- c(
  "immunarch",
  "immundata",
  "duckplyr",
  "airr",
  "ggplot2",
  "dplyr",
  "patchwork"
)

installed <- rownames(installed.packages())

to_install <- setdiff(required_packages, installed)

if (length(to_install) > 0) {
  install.packages(to_install, Ncpus = 2)
}

cat("TCRFlowX R dependencies ready.\n")
