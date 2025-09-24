# Enhanced Gauntlet Testing Protocol

## Overview

This protocol ensures experiment agnosticism and architectural compliance before alpha release. It includes deep inspection of logs and terminal output to detect framework-specific code violations.

## Pre-Gauntlet Architectural Audit

### Step 1: Run Architectural Audit
```bash
# Run comprehensive architectural audit
python3 scripts/gauntlet_architectural_audit.py

# Expected output: "✅ ARCHITECTURAL AUDIT PASSED"
# If violations found, fix them before proceeding
```

### Step 2: Verify Clean State
```bash
# Ensure no experiment-specific code in core system
grep -r "dignity\|truth\|justice\|sentiment\|populist" discernus/core/ discernus/agents/ --exclude-dir=__pycache__

# Should return no matches in core system files
```

## Enhanced Gauntlet Testing Protocol

### Phase 1: Nano Test (Baseline)
```bash
# Run nano test with enhanced logging
cd projects/nano_test_experiment
discernus run . --verbose 2>&1 | tee nano_test.log

# Post-run analysis
python3 scripts/gauntlet_architectural_audit.py --log-file nano_test.log
```

**Inspection Points:**
- [ ] No framework-specific keywords in logs
- [ ] No hardcoded experiment names in system output
- [ ] No error patterns suggesting framework-specific code
- [ ] Clean completion with final_report.md generated

### Phase 2: Micro Test (Validation)
```bash
# Run micro test with enhanced logging
cd projects/micro_test_experiment
discernus run . --verbose 2>&1 | tee micro_test.log

# Post-run analysis
python3 scripts/gauntlet_architectural_audit.py --log-file micro_test.log
```

**Inspection Points:**
- [ ] Derived metrics calculated without framework-specific code
- [ ] CSV export works with generic metric names
- [ ] No hardcoded sentiment-specific logic
- [ ] Statistical analysis uses generic calculations

### Phase 3: Framework Diversity Test
```bash
# Test with different framework types
for exp in business_ethics_experiment entman_framing_experiment lakoff_framing_experiment; do
    cd projects/$exp
    discernus run . --verbose 2>&1 | tee ${exp}_test.log
    python3 scripts/gauntlet_architectural_audit.py --log-file ${exp}_test.log
done
```

**Inspection Points:**
- [ ] Each experiment completes successfully
- [ ] No framework-specific code in any logs
- [ ] System adapts to different framework structures
- [ ] No hardcoded assumptions about specific dimensions

### Phase 4: Large Scale Test (Stress Test)
```bash
# Test with large experiment
cd projects/1a_caf_civic_character
discernus run . --verbose 2>&1 | tee civic_character_test.log
python3 scripts/gauntlet_architectural_audit.py --log-file civic_character_test.log
```

**Inspection Points:**
- [ ] System handles complex frameworks without hardcoded logic
- [ ] No framework-specific error handling
- [ ] Derived metrics work with any framework structure
- [ ] Synthesis adapts to different analysis results

## Log Analysis Checklist

### Critical Patterns to Detect
- [ ] **Framework Keywords**: dignity, truth, justice, sentiment, populist, civic
- [ ] **Experiment Names**: nano_test_experiment, micro_test_experiment, etc.
- [ ] **Hardcoded Paths**: /projects/, specific experiment directories
- [ ] **Error Patterns**: KeyError, AttributeError, NameError with framework terms
- [ ] **Template Violations**: Hardcoded prompts with framework-specific content

### Acceptable Patterns
- [ ] Test files with mock data (discernus/tests/)
- [ ] Documentation examples (docs/)
- [ ] Project-specific scripts (projects/*/scripts/)
- [ ] Comments explaining framework concepts

## Architectural Compliance Verification

### Core System Files to Verify
- [ ] `discernus/core/clean_analysis_orchestrator.py` - No framework-specific logic
- [ ] `discernus/agents/experiment_coherence_agent/agent.py` - Generic validation
- [ ] `discernus/agents/automated_derived_metrics/agent.py` - Framework-agnostic calculations
- [ ] `discernus/agents/automated_statistical_analysis/agent.py` - Generic statistical analysis
- [ ] `discernus/agents/unified_synthesis_agent/agent.py` - Adaptive synthesis

### Agent Prompts to Verify
- [ ] All agent prompts use generic language
- [ ] No hardcoded framework dimensions
- [ ] No experiment-specific examples
- [ ] Prompts adapt to any framework structure

## Success Criteria

### Must Pass (Alpha Blockers)
- [ ] Architectural audit passes with zero high-severity violations
- [ ] All experiments complete successfully
- [ ] No framework-specific code in core system
- [ ] System adapts to any valid framework
- [ ] No hardcoded experiment assumptions

### Should Pass (Quality Indicators)
- [ ] Medium-severity violations < 5
- [ ] All experiments produce consistent output format
- [ ] Derived metrics work with any framework
- [ ] Statistical analysis is framework-agnostic

### Nice to Pass (Optimization)
- [ ] Zero architectural violations
- [ ] Consistent performance across framework types
- [ ] Clean log output with no warnings

## Failure Response Protocol

### High Severity Violations
1. **Stop gauntlet testing immediately**
2. **Identify and fix framework-specific code**
3. **Re-run architectural audit**
4. **Restart gauntlet testing from Phase 1**

### Medium Severity Violations
1. **Document violations for post-alpha fixing**
2. **Continue gauntlet testing**
3. **Address violations in Sprint 19**

### Low Severity Violations
1. **Note for future improvement**
2. **Continue gauntlet testing**
3. **Address in post-alpha releases**

## Post-Gauntlet Validation

### Final Architectural Audit
```bash
# Run comprehensive final audit
python3 scripts/gauntlet_architectural_audit.py

# Verify all core system files
find discernus/core/ discernus/agents/ -name "*.py" -exec grep -l "dignity\|truth\|justice\|sentiment\|populist" {} \;

# Should return no files
```

### Documentation Update
- [ ] Update alpha release notes with architectural compliance
- [ ] Document any remaining medium/low severity violations
- [ ] Create roadmap for addressing post-alpha improvements

## Emergency Procedures

### If Framework-Specific Code Found
1. **Immediate**: Stop all testing
2. **Identify**: Use audit script to locate violations
3. **Fix**: Remove or generalize framework-specific code
4. **Verify**: Re-run architectural audit
5. **Restart**: Begin gauntlet testing from Phase 1

### If System Breaks on New Framework
1. **Document**: Record the specific failure
2. **Analyze**: Determine if it's architectural or framework-specific
3. **Fix**: Address architectural issues immediately
4. **Test**: Verify fix with original framework
5. **Continue**: Resume gauntlet testing

---

## Document Metadata

- **Version**: 1.0
- **Date**: 2025-09-12
- **Status**: Alpha Release Protocol
- **Next Review**: Post-Alpha Release
