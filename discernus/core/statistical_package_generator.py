#!/usr/bin/env python3
"""
Statistical Package Generator for Discernus
==========================================

Creates comprehensive, researcher-ready statistical packages for external analysis.
Includes data files, codebooks, import scripts, and documentation for multiple
statistical software platforms.
"""

Copyright (C) 2025  Discernus Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.


import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
import pandas as pd


class StatisticalPackageGenerator:
    """
    Generates comprehensive statistical packages for external analysis.
    
    Creates researcher-ready packages with:
    - Clean, well-documented CSV files
    - Variable codebooks with descriptions
    - Import scripts for R, Python, and STATA
    - Usage instructions and examples
    """
    
    def __init__(self, run_directory: Path):
        self.run_dir = run_directory
        self.results_dir = run_directory / "data"
        self.package_dir = run_directory / "statistical_package"
        
    def generate_statistical_package(self) -> Path:
        """
        Generate complete statistical package for external analysis.
        
        Returns:
            Path to the created statistical package directory
        """
        # Create package directory
        self.package_dir.mkdir(exist_ok=True)
        
        # Copy and clean CSV files
        self._copy_and_clean_csv_files()
        
        # Generate variable codebook
        self._generate_variable_codebook()
        
        # Generate import scripts
        self._generate_import_scripts()
        
        # Generate usage instructions
        self._generate_usage_instructions()
        
        # Generate metadata file
        self._generate_package_metadata()
        
        return self.package_dir
    
    def _copy_and_clean_csv_files(self) -> None:
        """Copy and clean CSV files from results directory."""
        if not self.results_dir.exists():
            return
        
        # Copy CSV files with standardized names
        csv_mappings = {
            'scores.csv': 'analysis_scores.csv',
            'evidence.csv': 'supporting_evidence.csv', 
            'metadata.csv': 'document_metadata.csv'
        }
        
        for source_name, target_name in csv_mappings.items():
            source_file = self.results_dir / source_name
            if source_file.exists():
                target_file = self.package_dir / target_name
                shutil.copy2(source_file, target_file)
                
                # Clean and standardize the CSV
                self._clean_csv_file(target_file)
    
    def _clean_csv_file(self, csv_file: Path) -> None:
        """Clean and standardize CSV file for external analysis."""
        try:
            # Read CSV
            df = pd.read_csv(csv_file)
            
            # Standardize column names (remove spaces, make lowercase)
            df.columns = df.columns.str.replace(' ', '_').str.lower()
            
            # Remove any completely empty rows
            df = df.dropna(how='all')
            
            # Save cleaned CSV
            df.to_csv(csv_file, index=False)
            
        except Exception as e:
            print(f"⚠️ Warning: Could not clean CSV file {csv_file}: {e}")
    
    def _generate_variable_codebook(self) -> None:
        """Generate comprehensive variable codebook."""
        codebook_content = """# Statistical Package Codebook

## Overview
This package contains data from a Discernus statistical preparation run, formatted for external statistical analysis.

## Data Files

### analysis_scores.csv
Primary dataset containing analysis scores and derived metrics.

**Variables:**
- `document_id`: Unique identifier for each document
- `document_name`: Human-readable document name
- `framework_dimensions`: Analysis scores for each framework dimension
- `derived_metrics`: Calculated statistical metrics
- `confidence_scores`: Analysis confidence levels
- `processing_metadata`: Technical processing information

### supporting_evidence.csv
Supporting quotes and evidence for analysis scores.

**Variables:**
- `document_id`: Links to analysis_scores.csv
- `quote_text`: Supporting text evidence
- `reasoning`: Analysis reasoning
- `dimension`: Framework dimension this evidence supports
- `confidence`: Evidence quality rating
- `page_reference`: Source location (if available)

### document_metadata.csv
Document and run metadata for context and reproducibility.

**Variables:**
- `document_id`: Links to other datasets
- `source_file`: Original file path
- `file_size`: File size in bytes
- `processing_timestamp`: When analysis was performed
- `run_id`: Discernus run identifier
- `experiment_name`: Name of the experiment
- `framework_version`: Version of analytical framework used

## Data Quality Notes
- All scores are normalized to 0-1 scale unless otherwise noted
- Missing values are represented as empty cells
- Confidence scores range from 0 (low) to 1 (high)
- Timestamps are in ISO 8601 format (UTC)

## Usage Recommendations
1. Start with `analysis_scores.csv` for primary analysis
2. Use `supporting_evidence.csv` for qualitative validation
3. Reference `document_metadata.csv` for context and reproducibility
4. Check data quality notes above for interpretation guidelines

## File Formats
- All files are in CSV format with UTF-8 encoding
- First row contains variable names
- No missing value indicators (empty cells represent missing data)
- Consistent document_id linking across all files

---
Generated by Discernus Statistical Package Generator
"""
        
        with open(self.package_dir / "CODEBOOK.md", "w", encoding="utf-8") as f:
            f.write(codebook_content)
    
    def _generate_import_scripts(self) -> None:
        """Generate import scripts for R, Python, and STATA."""
        
        # Python import script
        python_script = """#!/usr/bin/env python3
\"\"\"
Discernus Statistical Package - Python Import Script
==================================================

Import and prepare data for statistical analysis in Python.
Compatible with pandas, numpy, scipy, statsmodels, and scikit-learn.
\"\"\"

import pandas as pd
import numpy as np
import os
from pathlib import Path

def load_discernus_data(package_dir="."):
    \"\"\"
    Load all datasets from Discernus statistical package.
    
    Args:
        package_dir: Path to statistical package directory
        
    Returns:
        dict: Dictionary containing all datasets
    \"\"\"
    package_path = Path(package_dir)
    
    datasets = {}
    
    # Load analysis scores
    scores_file = package_path / "analysis_scores.csv"
    if scores_file.exists():
        datasets['scores'] = pd.read_csv(scores_file)
        print(f"Loaded scores: {len(datasets['scores'])} documents")
    
    # Load supporting evidence
    evidence_file = package_path / "supporting_evidence.csv"
    if evidence_file.exists():
        datasets['evidence'] = pd.read_csv(evidence_file)
        print(f"Loaded evidence: {len(datasets['evidence'])} quotes")
    
    # Load document metadata
    metadata_file = package_path / "document_metadata.csv"
    if metadata_file.exists():
        datasets['metadata'] = pd.read_csv(metadata_file)
        print(f"Loaded metadata: {len(datasets['metadata'])} documents")
    
    return datasets

def prepare_for_analysis(datasets):
    \"\"\"
    Prepare data for statistical analysis.
    
    Args:
        datasets: Dictionary from load_discernus_data()
        
    Returns:
        dict: Prepared datasets ready for analysis
    \"\"\"
    prepared = {}
    
    if 'scores' in datasets:
        scores = datasets['scores'].copy()
        
        # Convert numeric columns
        numeric_cols = scores.select_dtypes(include=[np.number]).columns
        scores[numeric_cols] = scores[numeric_cols].apply(pd.to_numeric, errors='coerce')
        
        # Create analysis-ready dataframe
        prepared['analysis_data'] = scores
        
        print(f"Prepared analysis data: {prepared['analysis_data'].shape}")
    
    return prepared

# Example usage
if __name__ == "__main__":
    # Load data
    data = load_discernus_data()
    
    # Prepare for analysis
    prepared = prepare_for_analysis(data)
    
    # Basic descriptive statistics
    if 'analysis_data' in prepared:
        print("\\nDescriptive Statistics:")
        print(prepared['analysis_data'].describe())
        
        print("\\nMissing Values:")
        print(prepared['analysis_data'].isnull().sum())
"""
        
        with open(self.package_dir / "import_python.py", "w", encoding="utf-8") as f:
            f.write(python_script)
        
        # Make executable
        os.chmod(self.package_dir / "import_python.py", 0o755)
        
        # R import script
        r_script = """# Discernus Statistical Package - R Import Script
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
    cat("Loaded scores:", nrow(datasets$scores), "documents\\n")
  }
  
  # Load supporting evidence
  evidence_file <- file.path(package_dir, "supporting_evidence.csv")
  if (file.exists(evidence_file)) {
    datasets$evidence <- read_csv(evidence_file, show_col_types = FALSE)
    cat("Loaded evidence:", nrow(datasets$evidence), "quotes\\n")
  }
  
  # Load document metadata
  metadata_file <- file.path(package_dir, "document_metadata.csv")
  if (file.exists(metadata_file)) {
    datasets$metadata <- read_csv(metadata_file, show_col_types = FALSE)
    cat("Loaded metadata:", nrow(datasets$metadata), "documents\\n")
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
    cat("Prepared analysis data:", nrow(prepared$analysis_data), "x", ncol(prepared$analysis_data), "\\n")
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
    cat("\\nDescriptive Statistics:\\n")
    print(summary(prepared$analysis_data))
    
    cat("\\nMissing Values:\\n")
    print(sapply(prepared$analysis_data, function(x) sum(is.na(x))))
  }
}
"""
        
        with open(self.package_dir / "import_r.R", "w", encoding="utf-8") as f:
            f.write(r_script)
        
        # STATA import script
        stata_script = """* Discernus Statistical Package - STATA Import Script
* ================================================
* 
* Import and prepare data for statistical analysis in STATA.
* Compatible with STATA 14+.

* Set working directory (adjust as needed)
* cd "path/to/statistical_package"

* Import analysis scores
import delimited "analysis_scores.csv", clear
save analysis_scores, replace
describe
summarize

* Import supporting evidence
import delimited "supporting_evidence.csv", clear
save supporting_evidence, replace
describe

* Import document metadata
import delimited "document_metadata.csv", clear
save document_metadata, replace
describe

* Merge datasets for analysis
use analysis_scores, clear
merge 1:m document_id using supporting_evidence, keep(master match)
save merged_data, replace

* Basic descriptive statistics
describe
summarize
tabstat, statistics(mean sd min max) columns(statistics)

* Check for missing values
misstable summarize

* Example analysis commands
* regress score_variable predictor_variables
* anova score_variable group_variable
* correlate score_variable1 score_variable2

display "Data import and preparation complete"
display "Ready for statistical analysis"
"""
        
        with open(self.package_dir / "import_stata.do", "w", encoding="utf-8") as f:
            f.write(stata_script)
    
    def _generate_usage_instructions(self) -> None:
        """Generate plain text usage instructions."""
        instructions = """DISCERNUS STATISTICAL PACKAGE - USAGE INSTRUCTIONS
====================================================

This package contains data from a Discernus statistical preparation run,
formatted for external statistical analysis in R, Python, STATA, or other
statistical software.

QUICK START
-----------
1. Choose your statistical software (R, Python, or STATA)
2. Run the appropriate import script:
   - Python: python import_python.py
   - R: source("import_r.R")
   - STATA: do import_stata.do
3. Follow the examples in the import scripts

DATA FILES
----------
- analysis_scores.csv: Primary dataset with scores and metrics
- supporting_evidence.csv: Supporting quotes and evidence
- document_metadata.csv: Document and run metadata

IMPORT SCRIPTS
--------------
- import_python.py: Python import and preparation functions
- import_r.R: R import and preparation functions  
- import_stata.do: STATA import and preparation commands

DOCUMENTATION
-------------
- CODEBOOK.md: Detailed variable descriptions and data quality notes
- README.md: This file with usage instructions

RECOMMENDED WORKFLOW
--------------------
1. Load data using appropriate import script
2. Check data quality and missing values
3. Explore descriptive statistics
4. Conduct your statistical analysis
5. Validate findings using supporting evidence
6. Document your analysis process

DATA QUALITY
------------
- All scores normalized to 0-1 scale unless noted
- Missing values represented as empty cells
- Confidence scores range 0 (low) to 1 (high)
- Timestamps in ISO 8601 format (UTC)

TROUBLESHOOTING
---------------
- Check file paths in import scripts
- Ensure all CSV files are present
- Verify data types match expectations
- Check for encoding issues (files are UTF-8)

SUPPORT
-------
For questions about this data package or Discernus:
- See CODEBOOK.md for detailed variable information
- Check import scripts for usage examples
- Refer to Discernus documentation for methodology

Generated: {datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')}
Discernus Version: Alpha System
"""
        
        with open(self.package_dir / "README.md", "w", encoding="utf-8") as f:
            f.write(instructions)
    
    def _generate_package_metadata(self) -> None:
        """Generate package metadata file."""
        metadata = {
            "package_info": {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "discernus_version": "Alpha System",
                "package_type": "statistical_preparation",
                "run_directory": str(self.run_dir),
                "generator_version": "1.0.0"
            },
            "data_files": {
                "analysis_scores": "analysis_scores.csv",
                "supporting_evidence": "supporting_evidence.csv", 
                "document_metadata": "document_metadata.csv"
            },
            "import_scripts": {
                "python": "import_python.py",
                "r": "import_r.R",
                "stata": "import_stata.do"
            },
            "documentation": {
                "codebook": "CODEBOOK.md",
                "usage_instructions": "README.md"
            },
            "data_quality": {
                "score_scale": "0-1 normalized",
                "missing_values": "empty cells",
                "confidence_range": "0 (low) to 1 (high)",
                "timestamp_format": "ISO 8601 UTC",
                "encoding": "UTF-8"
            }
        }
        
        with open(self.package_dir / "package_metadata.json", "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=2)


def generate_statistical_package(run_directory: Path) -> Path:
    """
    Convenience function to generate statistical package for a single run.
    
    Args:
        run_directory: Path to the experiment run directory
        
    Returns:
        Path to the created statistical package directory
    """
    generator = StatisticalPackageGenerator(run_directory)
    return generator.generate_statistical_package()
