# Legacy Synthesis Decommissioning Plan

**Version**: 1.0  
**Epic**: #217 CSV-to-JSON Migration  
**Purpose**: Technical plan for safe removal of dual-paradigm synthesis architecture

---

## Overview

This document provides the technical roadmap for decommissioning the legacy `EnhancedSynthesisAgent` fallback system and establishing `ProductionThinSynthesisPipeline` as the sole synthesis pathway.

**Current State**: Dual-paradigm architecture with hidden fallback  
**Target State**: Unified synthesis architecture with internal resilience  
**Timeline**: 1 week execution after resilience model implementation

---

## Components to Decommission

### 1. ThinOrchestrator Fallback Logic

**Location**: `discernus/core/thin_orchestrator.py`

**Current Code (Lines 170-187)**:
```python
# PRODUCTION: Uncomment below for fallback to EnhancedSynthesisAgent
# print(f"⚠️ THIN synthesis failed: {response.error_message}")
# print(f"🔄 Falling back to EnhancedSynthesisAgent...")
# 
# audit_logger.log_agent_event(
#     "ThinOrchestrator",
#     "thin_synthesis_fallback",
#     {
#         "thin_error": response.error_message,
#         "fallback_reason": "THIN pipeline execution failed"
#     }
# )
# 
# # Use legacy synthesis as fallback
# return self._run_legacy_synthesis(
#     scores_hash, evidence_hash, [], experiment_config,
#     framework_content, {}, model, audit_logger, storage
# )
```

**Action**: Remove commented fallback code entirely

### 2. _run_legacy_synthesis Method

**Location**: `discernus/core/thin_orchestrator.py` (Lines 189-210)

**Current Code**:
```python
def _run_legacy_synthesis(self,
                         scores_hash: str,
                         evidence_hash: str,
                         analysis_results: List[Dict[str, Any]],
                         experiment_config: Dict[str, Any],
                         framework_content: str,
                         corpus_manifest: Dict[str, Any],
                         model: str,
                         audit_logger: AuditLogger,
                         storage: LocalArtifactStorage) -> Dict[str, Any]:
    
    synthesis_agent = EnhancedSynthesisAgent(self.security, audit_logger, storage)
    return synthesis_agent.synthesize_results(
        scores_hash=scores_hash,
        evidence_hash=evidence_hash,
        analysis_results=analysis_results,
        experiment_config=experiment_config,
        framework_content=framework_content,
        corpus_manifest=corpus_manifest,
        model=model
    )
```

**Action**: Delete entire method

### 3. use_thin_synthesis Parameter

**Location**: Multiple locations in `discernus/core/thin_orchestrator.py`

**Current Usage**:
- Line 218: `use_thin_synthesis: bool = True` (method parameter)
- Lines 470-504: Conditional logic for synthesis path selection
- Lines 592-621: Duplicate conditional logic for synthesis path selection

**Action**: Remove parameter and conditional logic, always use THIN pipeline

### 4. Legacy Synthesis Calls

**Location**: `discernus/core/thin_orchestrator.py`

**Lines 492-504**: Synthesis-only mode legacy path
**Lines 608-621**: Full experiment legacy path

**Action**: Remove conditional branches, keep only THIN pipeline calls

### 5. EnhancedSynthesisAgent Import

**Location**: `discernus/core/thin_orchestrator.py`

**Current Import**: 
```python
from discernus.agents.EnhancedSynthesisAgent.main import EnhancedSynthesisAgent
```

**Action**: Remove import (if no longer used elsewhere)

---

## Step-by-Step Decommissioning Process

### Step 1: Audit Current Usage

**Objective**: Ensure no active dependencies on legacy synthesis

**Tasks**:
1. **Search Codebase**: Find all references to `_run_legacy_synthesis`
2. **Check CLI Usage**: Verify no CLI flags force legacy synthesis
3. **Review Tests**: Identify tests that depend on legacy synthesis
4. **Validate Default**: Confirm `use_thin_synthesis=True` is default everywhere

**Validation**:
```bash
grep -r "_run_legacy_synthesis" discernus/
grep -r "use_thin_synthesis.*False" discernus/
grep -r "EnhancedSynthesisAgent" discernus/
```

### Step 2: Update Method Signatures

**Objective**: Remove `use_thin_synthesis` parameter from all methods

**Files to Update**:
- `discernus/core/thin_orchestrator.py`: `run_experiment()` method
- Any CLI code that passes the parameter
- Any test code that uses the parameter

**Changes**:
```python
# BEFORE
def run_experiment(self, 
                  analysis_model: str = "vertex_ai/gemini-2.5-flash-lite",
                  synthesis_model: str = "vertex_ai/gemini-2.5-pro",
                  synthesis_only: bool = False,
                  analysis_only: bool = False,
                  resume_stage: Optional[str] = None,
                  use_thin_synthesis: bool = True) -> Dict[str, Any]:

# AFTER  
def run_experiment(self, 
                  analysis_model: str = "vertex_ai/gemini-2.5-flash-lite",
                  synthesis_model: str = "vertex_ai/gemini-2.5-pro",
                  synthesis_only: bool = False,
                  analysis_only: bool = False,
                  resume_stage: Optional[str] = None) -> Dict[str, Any]:
```

### Step 3: Simplify Synthesis Logic

**Objective**: Remove conditional synthesis path selection

**Current Logic (Lines 470-504)**:
```python
if use_thin_synthesis:
    print("🏭 Using THIN Code-Generated Synthesis Architecture...")
    synthesis_result = self._run_thin_synthesis(...)
else:
    print("🔄 Using legacy EnhancedSynthesisAgent...")
    synthesis_result = self._run_legacy_synthesis(...)
```

**New Logic**:
```python
print("🏭 Using THIN Code-Generated Synthesis Architecture...")
synthesis_result = self._run_thin_synthesis(...)
```

### Step 4: Remove Legacy Methods

**Objective**: Delete all legacy synthesis code

**Methods to Remove**:
- `_run_legacy_synthesis()` (entire method)
- Commented fallback code in `_run_thin_synthesis()` (lines 170-187)

**Imports to Remove**:
- `from discernus.agents.EnhancedSynthesisAgent.main import EnhancedSynthesisAgent` (if unused elsewhere)

### Step 5: Update Agent Name Logic

**Objective**: Simplify agent name assignment

**Current Logic (Lines 626-627)**:
```python
agent_name = "ProductionThinSynthesisPipeline" if use_thin_synthesis else "EnhancedSynthesisAgent"
```

**New Logic**:
```python
agent_name = "ProductionThinSynthesisPipeline"
```

### Step 6: Update CLI Integration

**Objective**: Remove any CLI options for legacy synthesis

**Files to Check**:
- `discernus/cli.py`
- Any CLI argument parsing that includes synthesis options

**Action**: Remove any `--legacy-synthesis` or similar flags

### Step 7: Update Documentation

**Objective**: Remove references to dual synthesis paths

**Files to Update**:
- Class docstrings in `ThinOrchestrator`
- Any user documentation mentioning synthesis options
- Architecture documentation

**Example Update**:
```python
# BEFORE
"""
THIN v2.0 orchestrator implementing direct function call coordination.

Simplified 2-agent pipeline:
1. Enhanced Analysis Agent (with mathematical validation)
2. Enhanced Synthesis Agent (with mathematical spot-checking)
"""

# AFTER
"""
THIN v2.0 orchestrator implementing direct function call coordination.

Unified 2-agent pipeline:
1. Enhanced Analysis Agent (with mathematical validation)  
2. Production THIN Synthesis Pipeline (with code-generated analysis)
"""
```

---

## Testing Strategy

### Pre-Decommissioning Tests

**Objective**: Establish baseline functionality before changes

**Test Cases**:
1. **Full Experiment Run**: Verify current system works end-to-end
2. **Synthesis-Only Mode**: Verify synthesis works with existing artifacts
3. **Analysis-Only Mode**: Verify analysis produces compatible outputs
4. **Error Handling**: Verify current error handling works

**Commands**:
```bash
# Test current system
python3 -m discernus.cli run projects/simple_test/
python3 -m discernus.cli run --synthesis-only projects/simple_test/
python3 -m discernus.cli run --analysis-only projects/simple_test/
```

### Post-Decommissioning Tests

**Objective**: Verify unified system maintains all functionality

**Test Cases**:
1. **Unified Pipeline**: Same experiments produce same results
2. **Error Handling**: Failures handled gracefully without legacy fallback
3. **Performance**: No significant performance regression
4. **Audit Trails**: All synthesis remains auditable

**Validation**:
- Compare output hashes before/after decommissioning
- Verify no `EnhancedSynthesisAgent` references in audit logs
- Confirm all statistical calculations traceable to explicit code

### Regression Testing

**Objective**: Ensure no functionality lost in decommissioning

**Test Matrix**:
- All reference frameworks (CAF, ECF, CHF)
- Both v5.0 (CSV) and v6.0 (JSON) frameworks
- Various corpus sizes and content types
- Error conditions that previously triggered fallbacks

---

## Rollback Plan

### Rollback Triggers

**Immediate Rollback Required If**:
- Synthesis success rate drops below 95%
- Any experiment that previously succeeded now fails
- Audit trail integrity compromised
- Performance degradation >20%

### Rollback Process

**Step 1**: Revert git commit containing decommissioning changes
**Step 2**: Verify rollback with same test cases that failed
**Step 3**: Analyze failure root cause before re-attempting decommissioning
**Step 4**: Update resilience model based on failure analysis

### Rollback Prevention

**Comprehensive Testing**: Complete test suite before decommissioning
**Gradual Deployment**: Test on non-critical experiments first
**Monitoring**: Real-time monitoring of synthesis success rates
**Backup Strategy**: Keep legacy code in separate branch until validation complete

---

## Success Criteria

### Technical Success

- ✅ Zero references to `_run_legacy_synthesis` in codebase
- ✅ Zero references to `EnhancedSynthesisAgent` in synthesis paths
- ✅ All experiments use `ProductionThinSynthesisPipeline` exclusively
- ✅ No conditional synthesis path logic remains

### Functional Success

- ✅ 100% of previously working experiments continue to work
- ✅ Synthesis success rate maintained or improved
- ✅ All outputs remain fully auditable
- ✅ Performance maintained within 10% of baseline

### Architectural Success

- ✅ Single synthesis pathway with internal resilience
- ✅ No hidden fallback mechanisms
- ✅ Clear, maintainable codebase
- ✅ Research integrity assured through auditability

---

## Timeline

**Day 1**: Steps 1-2 (Audit usage, Update signatures)
**Day 2**: Steps 3-4 (Simplify logic, Remove methods)  
**Day 3**: Steps 5-6 (Update naming, CLI integration)
**Day 4**: Step 7 + Testing (Documentation, Comprehensive testing)
**Day 5**: Validation and monitoring

**Total Duration**: 1 week
**Prerequisites**: Unified Resilience Model implemented and tested

---

**Author**: AI Agent  
**Date**: July 30, 2025  
**Epic**: #217 CSV-to-JSON Migration  
**Status**: Ready for Implementation