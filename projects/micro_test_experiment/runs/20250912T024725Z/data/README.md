# Data Directory

**Analysis-Ready CSV Files**

This directory contains the primary datasets for statistical analysis.

## Files

- **`scores.csv`** - Analysis scores and derived metrics
- **`evidence.csv`** - Supporting quotes and evidence  
- **`metadata.csv`** - Document and run metadata

## Usage

These files are ready for immediate import into statistical analysis tools:
- R, Python, STATA, SPSS, etc.
- See `../statistical_package/` for import scripts and examples

## Data Quality

- All scores normalized to 0-1 scale unless noted
- Missing values represented as empty cells
- Consistent document_id linking across all files
- UTF-8 encoding for international character support
