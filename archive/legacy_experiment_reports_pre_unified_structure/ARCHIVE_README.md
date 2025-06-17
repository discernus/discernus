# Legacy Experiment Reports Archive

**Archive Date**: June 18, 2025  
**Reason**: Transition to unified experiment package system  
**Status**: ARCHIVED - Superseded by `experiments/` directory structure

## Overview

This archive contains all experiment files from the pre-unified structure period (prior to June 18, 2025). These files have been superseded by the new unified experiment package system implemented in the `experiments/` directory.

## What Was Archived

### From `experiment_reports/` Directory
All scattered experiment files that were previously organized inconsistently across multiple directories:

**IDITI-Related Files** (now in `experiments/iditi_validation_study_20250617/`):
- `iditi_validation_20250617_083549/` - Raw results directory
- `iditi_validation_study.json` - Study definition
- `iditi_validation_study.yaml` - YAML configuration  
- `iditi_validation_study_report.html` - HTML report
- `iditi_validation_config.yaml` - Configuration file
- `iditi_validation_corpus.jsonl` - Corpus data
- `run_iditi_experiment.py` - Execution script
- `IDITI_Framework_Validation_Study_results_20250617_005158.html` - Results report

**Other Experiment Files**:
- `civic_virtue_real_validation_study.json`
- `declarative_experiment_33_20250613_154806.json`
- `declarative_experiment_34_20250613_155743.json` 
- `declarative_experiment_35_20250613_155859.json`
- `experiment_27_20250613/` - Complete experiment directory
- `experiment_28_20250613/` - Complete experiment directory
- `experiment_33/`, `experiment_34/`, `experiment_35/` - Experiment directories

**Analysis and Documentation**:
- `analysis/` - Statistical analysis files
- `documentation/` - Various documentation files
- `validation/` - Validation study results
- `data/` - Raw data files
- `COMPREHENSIVE_ORCHESTRATOR_SPEC.md`
- `FAILURE_REPORT_20250614.md`

### From `experiment_definitions/` Directory
- `iditi_multi_llm_validation.yaml` - IDITI experiment definition (now in unified package)

## Migration Status

### ✅ Successfully Migrated
**IDITI Validation Study**: Complete migration to `experiments/iditi_validation_study_20250617/`
- All inputs, outputs, analysis, documentation, and metadata properly organized
- Self-contained package with comprehensive documentation
- Full reproducibility information included

### 🔄 Pending Migration
**Other Experiments**: The following experiments could be migrated to unified packages if needed:
- Civic Virtue validation studies
- Declarative experiments 33-35
- MFT experiments 27-28
- Various framework validation studies

## Why This Archive Exists

### Problems with Old Structure
1. **Scattered Organization**: Files spread across multiple directories with no clear structure
2. **Inconsistent Naming**: No standardized naming conventions
3. **Poor Reproducibility**: Missing context and incomplete documentation
4. **Difficult Sharing**: No self-contained packages for collaboration
5. **Version Control Issues**: Mixed inputs/outputs made Git management difficult

### New Unified System Benefits
1. **Self-Contained Packages**: Everything needed for reproduction in one directory
2. **Standardized Structure**: Consistent organization across all experiments
3. **Complete Documentation**: Comprehensive README, methodology, and reproducibility guides
4. **Easy Sharing**: Packages can be shared as complete units
5. **Version Control Friendly**: Clear separation of inputs/outputs

## How to Use This Archive

### If You Need Legacy Data
1. **Check Unified Packages First**: Most important experiments have been migrated to `experiments/`
2. **Reference Archive**: Use this archive only for historical reference or unmigrated experiments
3. **Consider Migration**: Use `scripts/create_experiment_package.py` to migrate important experiments

### For Historical Research
- All original file structures and naming preserved
- Complete execution logs and results available
- Original documentation and analysis scripts included

## Migration Instructions

If you need to migrate any of these archived experiments to the new unified structure:

```bash
# Create new experiment package
python3 scripts/create_experiment_package.py experiment_name_YYYYMMDD --framework="Framework Name"

# Manually copy relevant files to appropriate directories:
# - Experiment configs → inputs/
# - Results and data → outputs/  
# - Analysis scripts → analysis/
# - Documentation → documentation/
# - Execution logs → metadata/
```

## Archive Maintenance

### Retention Policy
- **Keep Indefinitely**: Contains valuable research data and execution history
- **No Active Updates**: Archive is read-only, no new files should be added
- **Reference Only**: Use for historical reference, not active research

### If Archive Becomes Obsolete
- Verify all important data has been migrated to unified packages
- Consider creating compressed backup before deletion
- Update this documentation with final disposition

## Related Documentation

- `experiments/EXPERIMENT_ORGANIZATION_SUMMARY.md` - Overview of new unified system
- `scripts/create_experiment_package.py` - Tool for creating new experiment packages
- `docs/project-management/planning/daily/20250618_todo_comprehensive_analysis_pipeline.md` - Implementation planning
- `CHANGELOG.md` - Complete history of system changes

---

**Note**: This archive represents the transition from scattered, inconsistent experiment organization to a unified, reproducible research package system. The new system provides significantly better organization, documentation, and reproducibility for academic research. 