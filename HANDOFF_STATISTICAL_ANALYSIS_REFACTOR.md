# Statistical Analysis Framework Refactor - Session Handoff

**Date:** June 25, 2025  
**Previous Collaborator:** Claude Sonnet 4  
**Status:** 🚨 **CRITICAL ARCHITECTURAL ISSUE IDENTIFIED**

## 🎯 Current Situation

### ✅ TPM Rate Limiting - RESOLVED
- **TPM Rate Limiting System**: Production-ready and integrated
- **DirectAPIClient**: Automatic TPM protection working perfectly
- **Model Quality vs Cost Analysis**: Experiment definition ready
- **Cost Insights**: 40x difference revealed (GPT-3.5: $0.0003 vs GPT-4o: $0.12)

### 🚨 CRITICAL ISSUE DISCOVERED

**Problem:** Statistical analysis system (`src/analysis/statistics.py`) is **hardcoded to Civic Virtue framework** instead of being framework-agnostic.

**Impact:** 
- **All experiments using non-Civic Virtue frameworks FAIL statistical validation**
- Model Quality vs Cost Analysis (using Moral Foundations Theory) shows `"dignity_wells": [], "tribalism_wells": []`
- Every MFT experiment in project history has failed statistical analysis for this reason

## 🔍 Technical Details

### Hardcoded Framework Assumptions
**File:** `src/analysis/statistics.py`
**Lines 107-108:**
```python
# Look for dignity and tribalism wells  
dignity_cols = [col for col in well_columns if 'dignity' in col.lower()]
tribalism_cols = [col for col in well_columns if 'tribalism' in col.lower()]
```

### Affected Tests
- **H1 (Discriminative Validity)**: ❌ Hardcoded to dignity vs tribalism
- **H2 (Ideological Agnosticism)**: ✅ Already framework-agnostic  
- **H3 (Ground Truth Alignment)**: ❌ Hardcoded to look for dignity/tribalism in text IDs

### Current Experiment Context
**Experiment:** Model Quality vs Cost Analysis  
**Framework Used:** Moral Foundations Theory (Care_Harm, Fairness_Cheating, etc.)  
**Statistical Analysis Expected:** Civic Virtue (dignity_wells, tribalism_wells)  
**Result:** Complete statistical analysis failure

## 🎯 Required Refactor

### Scope
**Complete framework-agnostic rewrite** of statistical analysis system.

### Key Changes Needed

#### 1. Framework-Aware Test Design
```python
# Instead of hardcoded dignity/tribalism
def test_h1_discriminative_validity(self, df, well_columns, framework_structure):
    # Read actual framework definition
    # Design tests based on framework's axis pairs
    # E.g., Care vs Harm, Fairness vs Cheating for MFT
```

#### 2. Dynamic Hypothesis Generation
- Read framework YAML to understand axis structure
- Generate appropriate discriminative validity tests
- Create framework-specific ground truth expectations

#### 3. Terminology Standardization
- Update all "wells" references to v3.1 "axes/anchors" terminology
- Ensure consistent naming across analysis modules

## 🚀 Implementation Plan

### Phase 1: Framework Detection (30 min)
- Add framework definition reading to `StatisticalHypothesisTester`
- Parse framework YAML to extract axis pairs
- Create framework-specific test configurations

### Phase 2: H1 Refactor (45 min)  
- Rewrite discriminative validity tests to use actual framework axes
- Replace hardcoded dignity/tribalism with dynamic axis pairs
- Test with both Civic Virtue and MFT frameworks

### Phase 3: H3 Refactor (30 min)
- Update ground truth alignment to use framework-specific expectations
- Remove hardcoded dignity/tribalism text ID patterns
- Create generic extreme control detection

### Phase 4: Testing & Validation (30 min)
- Test with Model Quality vs Cost Analysis experiment
- Verify both Civic Virtue and MFT frameworks work
- Validate statistical outputs match framework structure

## 📋 Immediate Next Steps

### 1. Start Refactor
```bash
# Key file to modify
src/analysis/statistics.py

# Test with
research_workspaces/june_2025_research_dev_workspace/model_quality_vs_cost_analysis_experiment.yaml

# Framework files to reference
research_workspaces/june_2025_research_dev_workspace/frameworks/moral_foundations_theory/moral_foundations_theory_framework.yaml
```

### 2. Validation Approach
- Run Model Quality vs Cost Analysis experiment
- Verify statistical analysis completes without dignity/tribalism errors
- Check that H1 tests appropriate MFT axis pairs (Care vs Harm, etc.)

### 3. Success Criteria
- ✅ Statistical analysis works with any framework
- ✅ No more hardcoded dignity/tribalism assumptions
- ✅ Model Quality vs Cost Analysis generates valid statistical results
- ✅ H1, H2, H3 tests adapt to framework structure automatically

## 🔄 After Refactor: Return to Original Goal

### Complete Model Quality vs Cost Analysis
1. **Run fixed experiment** - should now pass statistical validation
2. **Generate quality vs cost comparison** - GPT-3.5 vs GPT-4o analysis
3. **Make strategic architecture decision** - Simple high-TPM vs LiteLLM complexity

### Strategic Decision Framework
- **If cheap models ≥85% quality**: Build simple high-throughput system
- **If premium models significantly better**: Implement LiteLLM multi-tier
- **If size-dependent patterns**: Smart routing based on complexity

## 💡 Key Insights for Next Collaborator

### Framework Architecture Pattern
The project shows a pattern of building systems for the first framework (Civic Virtue) then never making them framework-agnostic. This creates technical debt that breaks all subsequent frameworks.

### Refactor Priority
This is a **blocking architectural issue** that affects every experiment using non-Civic Virtue frameworks. Should be fixed before continuing with experiments.

### Testing Strategy
Use the Model Quality vs Cost Analysis as the validation case - it's ready to run and will immediately show if the refactor works.

## 📁 Key Files Reference

- **`src/analysis/statistics.py`** - Main file needing refactor
- **`src/analysis/results.py`** - Already partially fixed for v3.1 framework loading
- **Experiment YAML** - Ready to test with: `research_workspaces/june_2025_research_dev_workspace/model_quality_vs_cost_analysis_experiment.yaml`
- **Framework Definition** - Reference structure: `research_workspaces/june_2025_research_dev_workspace/frameworks/moral_foundations_theory/moral_foundations_theory_framework.yaml`

---

**Status:** Ready for framework-agnostic statistical analysis refactor. TPM rate limiting foundation is solid and production-ready. Focus on making statistical tests work with any framework, then complete the strategic Model Quality vs Cost Analysis. 