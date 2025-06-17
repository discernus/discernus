# IDITI Framework Validation Study
**Experiment ID**: `iditi_validation_study_20250617`  
**Date**: June 17, 2025  
**Status**: Completed  
**Framework**: Identity-Ideology-Tribalism-Integration (IDITI)  
**LLM Provider**: OpenAI GPT-4o  

## Overview

This experiment validates the IDITI framework's ability to discriminate between dignity-oriented and tribalism-oriented discourse across political orientations. The study tests three core hypotheses using a carefully curated corpus of political texts.

## Experimental Design

### Corpus Composition
- **Conservative Dignity**: 6 texts (Reagan, Bush Sr., Romney, etc.)
- **Conservative Tribalism**: 6 texts (Trump, Cruz, Bannon, etc.)  
- **Progressive Dignity**: 6 texts (Obama, Biden, Clinton, etc.)
- **Progressive Tribalism**: 6 texts (Warren, AOC, Sanders, etc.)
- **Extreme Controls**: 4 texts (high tribalism validation)
- **Mixed Controls**: 4 texts (balanced scoring validation)

### Hypotheses Tested

**H1: Discriminative Validity**  
The framework can distinguish dignity-oriented from tribalism-oriented discourse within political orientations.
- Test: T-tests comparing dignity vs tribalism scores within conservative and progressive categories

**H2: Ideological Agnosticism**  
The framework measures dignity/tribalism independently of political orientation.
- Test: ANOVA comparing conservative vs progressive within dignity and tribalism categories

**H3: Ground Truth Alignment**  
The framework produces expected scores for extreme and mixed control texts.
- Test: Correlation analysis between expected and actual scores

### Execution Parameters
- **LLM Model**: OpenAI GPT-4o
- **API Cost**: $0.0915 total
- **Success Rate**: 8/8 analyses completed (100%)
- **Quality Control**: All analyses met confidence thresholds

## Directory Structure

```
iditi_validation_study_20250617/
├── inputs/                           # Experiment inputs
│   ├── iditi_multi_llm_validation.yaml    # Experiment definition
│   └── corpus_manifest.json               # Input texts metadata
├── outputs/                          # Raw experiment outputs  
│   ├── final_results.json                 # Complete analysis results
│   ├── intermediate_results.json          # Processing intermediate data
│   └── results.csv                        # Tabular results summary
├── analysis/                         # Statistical analysis
│   ├── iditi_analysis_report_20250617_082751.json  # Hypothesis testing results
│   ├── analyze_iditi_experiment_results.py         # Analysis script
│   └── visualizations/                             # Generated charts
├── documentation/                    # Study documentation
│   ├── methodology.md                     # Detailed methodology
│   ├── statistical_analysis_plan.md      # Pre-registered analysis plan
│   └── results_interpretation.md          # Results discussion
└── metadata/                         # Experiment metadata
    ├── experiment_log.json                # Execution log
    ├── system_info.json                   # Technical environment
    └── reproducibility_info.json          # Reproduction instructions
```

## Key Results

### Statistical Findings
- **H1 (Discriminative Validity)**: NOT SUPPORTED - framework did not reliably distinguish dignity from tribalism
- **H2 (Ideological Agnosticism)**: NOT SUPPORTED - systematic differences found between political orientations  
- **H3 (Ground Truth Alignment)**: NOT SUPPORTED - poor correlation with expected extreme/mixed control scores

### Implications
The IDITI framework requires significant refinement before use in academic research. Key issues identified:
1. Insufficient discriminative power between dignity/tribalism dimensions
2. Political orientation bias in scoring
3. Poor performance on validation controls

## Reproduction Instructions

### Prerequisites
- Python 3.9+ with narrative_gravity package installed
- OpenAI API key configured
- PostgreSQL database with narrative_gravity schema

### Execution Steps
1. **Setup Environment**: `cd narrative_gravity_analysis && source venv/bin/activate`
2. **Run Orchestrator**: `python3 scripts/comprehensive_experiment_orchestrator.py inputs/iditi_multi_llm_validation.yaml`
3. **Generate Analysis**: `python3 analysis/analyze_iditi_experiment_results.py outputs/final_results.json`
4. **View Results**: Open generated HTML report in browser

### Expected Runtime
- **Data Collection**: ~5 minutes (8 API calls)
- **Statistical Analysis**: ~30 seconds  
- **Visualization Generation**: ~45 seconds
- **Total**: <7 minutes

## Data Availability

All raw data, processed results, and analysis scripts are included in this package for full reproducibility. The experiment can be re-run exactly using the provided configuration files.

## Citation

If using this experiment or its methodology, please cite:
```
IDITI Framework Validation Study (2025). Narrative Gravity Analysis Project. 
Experiment ID: iditi_validation_study_20250617.
```

## Technical Notes

- **Database**: Results stored in narrative_gravity.experiment_results table
- **Quality Assurance**: All analyses passed confidence threshold validation
- **Error Handling**: No failures during execution  
- **Version Control**: Git commit hash recorded in metadata/system_info.json 