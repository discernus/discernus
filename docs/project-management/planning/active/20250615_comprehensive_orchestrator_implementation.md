# Comprehensive Experiment Orchestrator Implementation

**Date:** June 15, 2025  
**Priority:** CRITICAL  
**Status:** Active Planning  
**Context:** Addressing critical gaps identified in IDITI validation study failure  

## Background

Today's IDITI framework validation study attempt revealed a critical gap in the platform: **no comprehensive experiment orchestrator exists**. The current system has fragmented tools that require manual component registration and don't maintain experiment context throughout the pipeline.

**Reference Documents:**
- `experiment_reports/FAILURE_REPORT_20250614.md` - Complete failure analysis
- `experiment_reports/COMPREHENSIVE_ORCHESTRATOR_SPEC.md` - Implementation specification
- `test_iditi_analysis.py` - Proof that DirectAPIClient works with IDITI framework

## Critical Issues to Address

### 🚨 **Phase 1: Core Orchestrator (CRITICAL - Day 1)**

#### TODO: Create Basic Orchestrator Structure
- [ ] **Create `scripts/comprehensive_experiment_orchestrator.py`**
  - [ ] Basic CLI interface with `--dry-run` and `--force-reregister` flags
  - [ ] JSON experiment definition loading and validation
  - [ ] Schema validation against enhanced format
  - [ ] Basic error handling and logging

#### TODO: Implement Component Validation
- [ ] **Framework existence checking**
  - [ ] Query database for framework ID + version
  - [ ] File path validation for new frameworks
  - [ ] Hash validation for framework files
  - [ ] Auto-registration capability

- [ ] **Prompt template existence checking**
  - [ ] Query database for template ID + version
  - [ ] File path validation for new templates
  - [ ] Hash validation for template files
  - [ ] Auto-registration capability

- [ ] **Weighting scheme existence checking**
  - [ ] Query database for scheme ID + version
  - [ ] File path validation for new schemes
  - [ ] Hash validation for scheme files
  - [ ] Auto-registration capability

- [ ] **Model availability checking**
  - [ ] Verify model access through DirectAPIClient
  - [ ] Provider-specific validation (OpenAI, Anthropic, etc.)
  - [ ] Cost estimation validation

#### TODO: Graceful Error Handling
- [ ] **Implement `MissingComponentsError` exception class**
- [ ] **Create helpful error message generator**
  - [ ] Component-specific guidance (frameworks, templates, schemes, corpus)
  - [ ] File path suggestions and examples
  - [ ] Documentation references
  - [ ] Hash generation instructions

- [ ] **Pre-flight validation report**
  - [ ] Summary of all components to be registered
  - [ ] Cost estimation for full experiment
  - [ ] Confirmation prompt before execution

### 🔧 **Phase 2: Auto-Registration (HIGH - Day 2)**

#### TODO: Framework Auto-Registration
- [ ] **Extend existing framework registration system**
  - [ ] Load framework.json from file path
  - [ ] Validate framework structure (wells, dipoles, etc.)
  - [ ] Register in database with proper versioning
  - [ ] Handle conflicts with existing frameworks

#### TODO: Prompt Template Auto-Registration
- [ ] **Research current template registration system**
  - [ ] Identify existing template manager
  - [ ] Understand template format requirements
  - [ ] Implement file-based registration
  - [ ] Version management for templates

#### TODO: Weighting Scheme Auto-Registration
- [ ] **Research current weighting system**
  - [ ] Identify existing weighting methodology storage
  - [ ] Understand scheme format requirements
  - [ ] Implement file-based registration
  - [ ] Version management for schemes

#### TODO: Hash Validation System
- [ ] **Implement file hash validation**
  - [ ] SHA-256 hash calculation for files
  - [ ] Hash comparison with expected values
  - [ ] Hash generation utility for new files
  - [ ] Hash manifest creation for corpus collections

### 📊 **Phase 3: Corpus Management (HIGH - Day 3)**

#### TODO: Corpus Integrity Checking
- [ ] **File collection validation**
  - [ ] Glob pattern expansion for file paths
  - [ ] File existence verification
  - [ ] File count validation against expected count
  - [ ] Content hash manifest validation

#### TODO: Corpus Auto-Ingestion
- [ ] **Extend existing corpus ingestion system**
  - [ ] Integrate with IntelligentIngestionService
  - [ ] Metadata preservation during ingestion
  - [ ] Batch ingestion for file collections
  - [ ] Progress reporting for large corpus sets

#### TODO: Hash Manifest System
- [ ] **Create corpus hash manifest generator**
  - [ ] Generate SHA-256 hashes for all corpus files
  - [ ] Create JSON manifest with file paths and hashes
  - [ ] Validation utility for existing manifests
  - [ ] Update detection for changed files

### 🔄 **Phase 4: Context Propagation (MEDIUM - Day 4)**

#### TODO: Experiment Context System
- [ ] **Create `ExperimentContext` class**
  - [ ] Store experiment metadata (name, hypotheses, research context)
  - [ ] Enrich analysis requests with experiment context
  - [ ] Propagate context through pipeline stages
  - [ ] Maintain context in database records

#### TODO: Hypothesis-Aware Analysis
- [ ] **Extend analysis service to accept experiment context**
  - [ ] Modify DirectAPIClient to include context in prompts
  - [ ] Update RealAnalysisService for context awareness
  - [ ] Store hypothesis information in Run records
  - [ ] Enable hypothesis-specific validation

#### TODO: Context-Aware Output Generation
- [ ] **Update academic export system**
  - [ ] Include experiment hypotheses in exported data
  - [ ] Generate hypothesis-specific analysis templates
  - [ ] Create validation reports tied to research questions
  - [ ] Preserve research context in replication packages

### 📈 **Phase 5: Integration & Testing (MEDIUM - Day 5)**

#### TODO: End-to-End Integration
- [ ] **Integrate orchestrator with existing systems**
  - [ ] Connect to DirectAPIClient for analysis
  - [ ] Integrate with RealAnalysisService
  - [ ] Connect to academic export pipeline
  - [ ] Integrate with visualization system

#### TODO: IDITI Validation Study Execution
- [ ] **Create proper IDITI experiment definition**
  - [ ] Follow enhanced JSON schema format
  - [ ] Include all three hypotheses with success criteria
  - [ ] Specify all required components with file paths
  - [ ] Generate hash manifests for validation corpus

- [ ] **Execute IDITI validation study**
  - [ ] Run with new comprehensive orchestrator
  - [ ] Validate all three hypotheses
  - [ ] Generate academic outputs
  - [ ] Create publication-ready visualizations
  - [ ] Produce final validation report

#### TODO: Testing & Validation
- [ ] **Create test suite for orchestrator**
  - [ ] Unit tests for component validation
  - [ ] Integration tests for auto-registration
  - [ ] End-to-end tests with sample experiments
  - [ ] Error handling tests for missing components

### 📚 **Phase 6: Documentation & Examples (LOW - Day 6)**

#### TODO: Documentation Updates
- [ ] **Update experiment definition documentation**
  - [ ] Document enhanced JSON schema
  - [ ] Provide component specification examples
  - [ ] Create hash manifest generation guide
  - [ ] Update troubleshooting documentation

#### TODO: Example Experiments
- [ ] **Create example experiment definitions**
  - [ ] Simple single-framework validation
  - [ ] Multi-framework comparison study
  - [ ] Corpus integrity validation example
  - [ ] Complete IDITI validation study example

#### TODO: Migration Guide
- [ ] **Create migration guide for existing experiments**
  - [ ] Convert existing experiment.json files to new format
  - [ ] Generate hash manifests for existing corpus
  - [ ] Update component references
  - [ ] Provide automated migration tools

## Success Criteria

### Immediate Success (End of Day 1)
- [ ] ✅ Basic orchestrator can validate experiment definitions
- [ ] ✅ Clear error messages for missing components
- [ ] ✅ Dry-run mode shows execution plan

### Short-term Success (End of Week)
- [ ] ✅ IDITI validation study executes successfully with single command
- [ ] ✅ All components auto-register from file paths
- [ ] ✅ Experiment context preserved throughout pipeline
- [ ] ✅ Hypothesis validation in final outputs

### Long-term Success (End of Month)
- [ ] ✅ All existing experiments migrated to new format
- [ ] ✅ Comprehensive test suite passing
- [ ] ✅ Documentation complete and examples working
- [ ] ✅ Zero manual intervention required for valid experiments

## Risk Mitigation

### High Risk: Database Schema Changes
- **Risk:** Component auto-registration may require database schema updates
- **Mitigation:** Review existing schema first, plan migrations carefully
- **Contingency:** Implement backward compatibility layer

### Medium Risk: Integration Complexity
- **Risk:** Orchestrator integration with existing systems may be complex
- **Mitigation:** Start with minimal integration, expand incrementally
- **Contingency:** Maintain existing workflow as fallback

### Low Risk: Performance Impact
- **Risk:** Hash validation and auto-registration may slow execution
- **Mitigation:** Implement caching and parallel processing
- **Contingency:** Make validation optional for trusted environments

## Dependencies

### External Dependencies
- [ ] Verify DirectAPIClient API stability
- [ ] Confirm database schema flexibility
- [ ] Check existing component registration systems

### Internal Dependencies
- [ ] Complete IDITI framework validation (already done)
- [ ] Understand existing corpus ingestion system
- [ ] Map current academic export pipeline

## Notes

- **Priority Focus:** Get basic orchestrator working first, then add features incrementally
- **Testing Strategy:** Use IDITI validation study as primary test case throughout development
- **Documentation:** Update as we go, don't wait until the end
- **User Experience:** Prioritize clear error messages and helpful guidance

---

**This TODO list addresses the critical infrastructure gap that caused today's failure and provides a clear path to a robust experiment orchestration system.** 