# Discernus Statistical Package - R Import Script
# ================================================
# 
# Import and prepare data for statistical analysis in R.
# Compatible with base R, tidyverse, and other statistical packages.

# Load required libraries
library(readr)
library(dplyr)
library(ggplot2)

# Function to load all datasets
load_discernus_data <- function(package_dir = ".") {
  #' Load all datasets from Discernus statistical package
  #' 
  #' @param package_dir Path to statistical package directory
  #' @return List containing all datasets
  
  datasets <- list()
  
  # Load analysis scores
  scores_file <- file.path(package_dir, "analysis_scores.csv")
  if (file.exists(scores_file)) {
    datasets$scores <- read_csv(scores_file, show_col_types = FALSE)
    cat("Loaded scores:", nrow(datasets$scores), "documents\n")
  }
  
  # Load supporting evidence
  evidence_file <- file.path(package_dir, "supporting_evidence.csv")
  if (file.exists(evidence_file)) {
    datasets$evidence <- read_csv(evidence_file, show_col_types = FALSE)
    cat("Loaded evidence:", nrow(datasets$evidence), "quotes\n")
  }
  
  # Load document metadata
  metadata_file <- file.path(package_dir, "document_metadata.csv")
  if (file.exists(metadata_file)) {
    datasets$metadata <- read_csv(metadata_file, show_col_types = FALSE)
    cat("Loaded metadata:", nrow(datasets$metadata), "documents\n")
  }
  
  return(datasets)
}

# Function to prepare data for analysis
prepare_for_analysis <- function(datasets) {
  #' Prepare data for statistical analysis
  #' 
  #' @param datasets List from load_discernus_data()
  #' @return List of prepared datasets
  
  prepared <- list()
  
  if ("scores" %in% names(datasets)) {
    scores <- datasets$scores
    
    # Convert to numeric where appropriate
    scores <- scores %>%
      mutate(across(where(is.character), ~as.numeric(.x)))
    
    prepared$analysis_data <- scores
    cat("Prepared analysis data:", nrow(prepared$analysis_data), "x", ncol(prepared$analysis_data), "\n")
  }
  
  return(prepared)
}

# Example usage
if (interactive()) {
  # Load data
  data <- load_discernus_data()
  
  # Prepare for analysis
  prepared <- prepare_for_analysis(data)
  
  # Basic descriptive statistics
  if ("analysis_data" %in% names(prepared)) {
    cat("\nDescriptive Statistics:\n")
    print(summary(prepared$analysis_data))
    
    cat("\nMissing Values:\n")
    print(sapply(prepared$analysis_data, function(x) sum(is.na(x))))
  }
}
