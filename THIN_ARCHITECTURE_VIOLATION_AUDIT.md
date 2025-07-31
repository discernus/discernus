# THIN Architecture Violation Audit Report

**Date**: 2025-07-31  
**Scope**: Complete codebase audit for framework/experiment/corpus-specific code  
**Status**: 🚨 **CRITICAL VIOLATIONS FOUND**

## Executive Summary

The codebase audit reveals **systematic violations** of THIN architecture principles throughout the infrastructure. Framework-specific code has been embedded in supposedly agnostic components, creating brittleness and violating the core principle that infrastructure should be thin and framework-agnostic.

## Critical Violations Found

### 1. **Synthesis Agent Prompts - Framework-Specific Column Names**

**File**: `discernus/agents/thin_synthesis/derived_metrics_analysis_planner/prompts/derived_metrics_planning.yaml`

**Violation**: Hardcoded CAF framework column names in synthesis prompt
```yaml
**DIMENSIONAL SCORES:**
- dignity_score, dignity_salience, dignity_confidence
- truth_score, truth_salience, truth_confidence  
- justice_score, justice_salience, justice_confidence
- hope_score, hope_salience, hope_confidence
- pragmatism_score, pragmatism_salience, pragmatism_confidence
```

**Impact**: 🚨 **CRITICAL** - Synthesis pipeline fails with non-CAF frameworks
**Status**: ✅ **FIXED** - Made framework-agnostic with dynamic column discovery

### 2. **Evidence Curator - Hardcoded CHF Dimensions**

**File**: `discernus/agents/thin_synthesis/evidence_curator/agent.py:934`

**Violation**: Hardcoded CHF framework dimension names
```python
for dim in ['procedural_legitimacy', 'institutional_respect', 'systemic_continuity']:
```

**Impact**: 🚨 **CRITICAL** - Evidence curation fails with non-CHF frameworks
**Status**: ❌ **UNFIXED** - Needs framework-agnostic approach

### 3. **Test Data Generator - Framework-Specific Logic**

**File**: `discernus/tests/realistic_test_data_generator.py:303-311`

**Violation**: Hardcoded framework branching logic
```python
if framework_type == "cff":
    patterns = self.cff_v4_1_patterns
elif framework_type == "pdaf":
    patterns = self.pdaf_patterns
elif framework_type == "generic":
    patterns = self.generic_patterns
```

**Impact**: 🔶 **MODERATE** - Test infrastructure not framework-agnostic
**Status**: ❌ **UNFIXED** - Should use framework specifications dynamically

### 4. **Widespread Framework-Specific Test Data**

**Files**: Multiple test files and artifacts

**Violation**: Hardcoded framework-specific dimension names throughout test suite:
- `dignity_score`, `truth_score`, `justice_score` (CAF-specific)
- `procedural_legitimacy`, `institutional_respect` (CHF-specific)
- `mc_sci`, `dignity_tribalism_tension` (CAF-specific derived metrics)

**Impact**: 🔶 **MODERATE** - Test suite not framework-agnostic
**Status**: ❌ **UNFIXED** - Tests should be generated from framework specifications

### 5. **Experiment Configuration Dependencies**

**Files**: Multiple experiment.md files

**Violation**: Experiment configurations hardcode framework-specific test names:
```yaml
required_tests: ["speaker_differentiation_anova", "character_signature_analysis", "mc_sci_coherence_patterns"]
```

**Impact**: 🔶 **MODERATE** - Experiments not framework-agnostic
**Status**: ❌ **UNFIXED** - Should derive tests from framework specifications

## Framework-Specific Code Distribution

### CAF Framework Violations
- **Dimension Names**: `dignity_score`, `truth_score`, `justice_score`, `hope_score`, `pragmatism_score`
- **Derived Metrics**: `mc_sci`, `dignity_tribalism_tension`, `character_tensions`
- **Files Affected**: 50+ files across test suite, synthesis agents, and experiments

### CHF Framework Violations  
- **Dimension Names**: `procedural_legitimacy`, `institutional_respect`, `systemic_continuity`
- **Derived Metrics**: `constitutional_direction_index`, `procedural_health_score`
- **Files Affected**: 20+ files in synthesis agents and experiments

### ECF Framework Violations
- **Dimension Names**: `hope_score`, `fear_score`, `affective_climate_index`
- **Files Affected**: 10+ deprecated framework files

## Root Cause Analysis

### 1. **Lack of Framework Abstraction**
The codebase evolved with specific frameworks in mind rather than building framework-agnostic abstractions from the start.

### 2. **Copy-Paste Development**
Framework-specific code was copied between components instead of creating reusable abstractions.

### 3. **Insufficient THIN Discipline**
Developers embedded framework knowledge in infrastructure components rather than keeping them thin and letting LLMs handle framework-specific logic.

### 4. **Test-Driven Framework Coupling**
Tests were written for specific frameworks rather than testing framework-agnostic capabilities.

## Remediation Strategy

### Phase 1: Critical Infrastructure (Immediate)
1. ✅ **Fixed**: Synthesis prompt framework-agnosticism
2. ❌ **TODO**: Fix evidence curator hardcoded dimensions
3. ❌ **TODO**: Make math toolkit fully framework-agnostic
4. ❌ **TODO**: Remove framework-specific logic from orchestration

### Phase 2: Test Infrastructure (High Priority)
1. ❌ **TODO**: Refactor test data generator to use framework specifications
2. ❌ **TODO**: Create framework-agnostic test patterns
3. ❌ **TODO**: Generate test data dynamically from framework specs
4. ❌ **TODO**: Remove hardcoded dimension names from all tests

### Phase 3: Experiment Configuration (Medium Priority)
1. ❌ **TODO**: Make experiment configurations framework-agnostic
2. ❌ **TODO**: Derive statistical tests from framework specifications
3. ❌ **TODO**: Create framework-agnostic experiment templates
4. ❌ **TODO**: Remove framework-specific test requirements

### Phase 4: Documentation and Validation (Low Priority)
1. ❌ **TODO**: Update documentation to emphasize framework-agnosticism
2. ❌ **TODO**: Create validation rules to prevent future violations
3. ❌ **TODO**: Add linting rules to catch framework-specific code
4. ❌ **TODO**: Establish code review guidelines for THIN compliance

## THIN Architecture Principles Violated

### Principle 1: Thin Infrastructure
**Violation**: Infrastructure components contain framework-specific knowledge
**Solution**: Move all framework knowledge to LLM prompts and specifications

### Principle 2: Framework Agnosticism  
**Violation**: Components hardcode framework-specific dimension names and logic
**Solution**: Use framework specifications as the single source of truth

### Principle 3: LLM Intelligence
**Violation**: Infrastructure attempts to parse and understand framework concepts
**Solution**: Let LLMs handle all framework interpretation and column discovery

### Principle 4: Binary Data Flow
**Violation**: Components make assumptions about data structure and content
**Solution**: Pass raw data to LLMs and let them interpret structure

## Success Metrics

### Immediate Success (Phase 1)
- [ ] All synthesis agents work with any framework without code changes
- [ ] Evidence curator works with any framework dimensions
- [ ] Math toolkit requires no framework-specific modifications

### Medium-term Success (Phase 2-3)
- [ ] Test suite generates data for any framework specification
- [ ] Experiments can be configured for any framework without hardcoded tests
- [ ] New frameworks can be added without touching infrastructure code

### Long-term Success (Phase 4)
- [ ] Automated validation prevents framework-specific code introduction
- [ ] Documentation clearly establishes THIN discipline
- [ ] Code review process enforces framework-agnosticism

## Conclusion

The audit reveals that while the THIN architecture vision is sound, the implementation has drifted significantly from these principles. The recent fix to the synthesis prompt demonstrates that framework-agnostic solutions are both possible and more robust.

**Immediate Action Required**: Fix the evidence curator hardcoded dimensions to prevent synthesis failures with different frameworks.

**Strategic Priority**: Establish automated validation to prevent future THIN violations and gradually refactor the codebase to achieve true framework-agnosticism.

The investment in making infrastructure truly framework-agnostic will pay dividends in system robustness, maintainability, and the ability to rapidly support new analytical frameworks without infrastructure modifications.