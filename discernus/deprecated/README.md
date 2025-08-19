# Deprecated Components

This directory contains components that have been deprecated during infrastructure cleanup.

## Deprecated Components

### Orchestrators
- **thin_orchestrator.py** - Legacy THIN v2.0 orchestrator with CFF contamination
- **v8_orchestrator.py** - Unused V8 orchestrator with architectural confusion
- **cli_v8.py** - V8 CLI that used deprecated orchestrators

### Agents  
- **notebook_generator_agent/** - CFF v7.3 hardcoded calculations, replaced by AutomatedDerivedMetricsAgent
- **reliability_analysis_agent/** - Framework validation, only used in deprecated ThinOrchestrator
- **intelligent_extractor_agent/** - LLM-based extraction, only used in deprecated ThinOrchestrator  
- **sequential_synthesis/** - 5-step synthesis pipeline, valuable patterns preserved in reference copy
- **thin_synthesis/** - Complex multi-agent synthesis, valuable patterns preserved in reference copy

## Reason for Deprecation

These components were deprecated during CRIT-007 infrastructure cleanup (2025-01-19) due to:

1. **Framework-specific hardcoding** (CFF v7.3/v8.0 assumptions)
2. **Experiment-specific dependencies** (simple_test path hardcoding)
3. **Architectural confusion** (multiple parallel systems)
4. **Legacy complexity** not aligned with THIN principles

## Current Active Pipeline

The clean, active pipeline uses:
- **ExperimentOrchestrator** (main orchestrator)
- **NotebookGenerationOrchestrator** (transactional notebook generation)
- **AutomatedDerivedMetricsAgent** (framework-agnostic calculations)
- **EnhancedAnalysisAgent** (framework-agnostic analysis)
- **ExperimentCoherenceAgent** (framework-agnostic validation)

## Recovery Instructions

If any deprecated component is needed:
1. **Review for contamination** before reactivating
2. **Fix framework/experiment agnosticism** issues
3. **Test with non-CFF frameworks** to validate
4. **Update architecture documentation** to reflect changes

## Cleanup Date
- **Date**: 2025-01-19
- **Issue**: CRIT-007 Infrastructure Cruft Cleanup
- **Status**: Surgical removal of contaminated/unused components
