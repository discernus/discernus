---
name: "simple_test_pdaf"
description: "A simple test experiment to validate the PDAF analysis pipeline for populist discourse analysis."
framework: "pdaf_v10.md"
corpus: "corpus.md"
questions:
  - "How do different political communication styles score on populist discourse dimensions?"
  - "What are the strategic tension patterns between institutional and populist approaches?"
---

# Simple Test Experiment - PDAF

## Abstract
This experiment serves as a basic validation of the Populist Discourse Analysis Framework (PDAF v10.0) analysis pipeline. It uses PDAF to analyze a small, representative corpus of political speeches spanning institutional and populist approaches to democratic discourse.

## Research Questions
- How do different political communication styles score on populist discourse dimensions?
- What are the strategic tension patterns between institutional and populist approaches?
- How do populist conservative and progressive styles differ in their boundary construction and crisis narratives?

## Data Grouping and Custom Variable Mapping

This experiment requires statistical analysis using grouping variables for comparative analysis between different political communication styles.

### Primary Analysis Variables
- **Main Grouping Variable**: `political_era` - Categorizes speeches by political time period
- **Secondary Variable**: `speaker_category` - Groups speakers by their political role and approach

### Statistical Grouping Instructions
- **Primary Analysis Variable**: `political_era` with 3 groups for ANOVA comparison
- **Baseline References**: None - all groups must have n≥2 for inferential testing
- **Secondary Variables**: `speaker_category` for additional analysis dimensions
- **Corpus Manifest Mapping**: These variables should be derived from corpus manifest metadata
- **Missing Data Handling**: All documents must have complete grouping variable assignments

### Expected Statistical Tests
- ANOVA comparing populist discourse scores across `political_era` groups
- T-tests between institutional vs. populist approaches using `speaker_category`
- Correlation analysis of populist dimensions across different `political_era` periods

---

## Configuration Appendix
```yaml
# --- Start of Machine-Readable Appendix ---

# 4.1: Metadata
metadata:
  experiment_name: "simple_test_pdaf"
  author: "Discernus Project"
  spec_version: "10.0"

# 4.2: Components
components:
  framework: "pdaf_v10.md"
  corpus: "corpus.md"

# --- End of Machine-Readable Appendix ---
```
