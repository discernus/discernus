# Gasket Architecture Implementation Roadmap

## 1. Overview

This document provides a detailed implementation roadmap for transitioning from the current Discernus architecture to the new Gasket Architecture. It outlines the specific changes needed to existing components, new components to be built, and the sequence of implementation steps.

**Current State:** THICK architecture with brittle parsing, framework-specific code, and the `Data Sparsity` problem.

**Target State:** THIN architecture with three gaskets, framework-agnostic infrastructure, and robust LLM-to-Math interfaces.

## 2. Implementation Phases

### Phase 1: Foundation and Framework Specification v7.0
**Duration:** 1-2 weeks
**Priority:** Critical

#### 2.1. Create Framework Specification v7.0
- **File:** `docs/specifications/FRAMEWORK_SPECIFICATION_V7.md`
- **Changes:**
  - Radically simplify `output_contract` to "Raw Analysis Log" (free-form text)
  - Remove restrictive JSON formatting requirements from `analysis_prompt`
  - Add new `gasket_schema` section for Intelligent Extractor
  - Update `calculation_spec` to work with flat data structure
  - Add migration guide from v6.0 to v7.0

#### 2.2. Update Existing Frameworks
- **Files:** All framework files in `frameworks/` directory
- **Changes:**
  - Add `gasket_schema` sections to all active frameworks
  - Simplify `analysis_prompt` sections to focus on intellectual analysis
  - Update `output_contract` to specify "Raw Analysis Log"
  - Test compatibility with new specification

#### 2.3. Framework Validation Updates
- **File:** `discernus/core/framework_validator.py`
- **Changes:**
  - Add validation for new `gasket_schema` section
  - Update validation rules for simplified `output_contract`
  - Ensure backward compatibility with v6.0 frameworks during transition

### Phase 2: Intelligent Extractor Gasket Implementation
**Duration:** 2-3 weeks
**Priority:** Critical

#### 2.1. Create Intelligent Extractor Component
- **File:** `discernus/agents/intelligent_extractor_agent.py`
- **New Component:**
  - Implement `IntelligentExtractorAgent` class
  - Create focused LLM call with framework-agnostic prompt template
  - Handle extraction and semantic mapping from Raw Analysis Log
  - Implement error handling and retry logic
  - Add comprehensive unit tests

#### 2.2. Refactor ThinOrchestrator
- **File:** `discernus/core/thin_orchestrator.py`
- **Changes:**
  - Remove existing `regex` and `json.loads()` parsing logic
  - Add `_extract_and_map_with_gasket()` method
  - Update `_combine_analysis_results()` to use Intelligent Extractor
  - Remove framework-specific parsing code
  - Add integration tests for new gasket workflow

#### 2.3. Update MathToolkit Integration
- **File:** `discernus/core/math_toolkit.py` ✅ **ALREADY IMPLEMENTED**
- **Status:** MathToolkit is fully implemented with comprehensive mathematical functions
- **Current Functions:**
  - `calculate_descriptive_stats()` - Descriptive statistics with grouping support
  - `perform_independent_t_test()` - T-tests with defensive parameter handling
  - `calculate_pearson_correlation()` - Correlation analysis
  - `perform_one_way_anova()` - ANOVA analysis
  - `perform_two_way_anova()` - Two-way ANOVA
  - `calculate_effect_sizes()` - Effect size calculations
  - `calculate_derived_metrics()` - Framework-specific metric calculations
  - `execute_analysis_plan()` - Plan execution with error handling
  - And many more statistical functions
- **Changes Needed:**
  - Ensure compatibility with flat data structure from gasket
  - Remove defensive parsing code (no longer needed)
  - Update error handling for new data format
  - Add validation for gasket output format

### Phase 3: Evidence Distillation Enhancement
**Duration:** 1-2 weeks
**Priority:** High

#### 3.1. Refactor Evidence Curator
- **File:** `discernus/agents/thin_synthesis/evidence_curator/agent.py` ✅ **ALREADY IMPLEMENTED**
- **Status:** Evidence Curator is implemented with fan-out/fan-in pattern
- **Current Features:**
  - Evidence curation from analysis results
  - Fan-out/fan-in pattern for large datasets
  - Evidence selection algorithms
  - Framework-aware distillation logic
- **Changes Needed:**
  - Update to work with Raw Analysis Log input
  - Enhance existing fan-out/fan-in pattern
  - Improve evidence selection algorithms

#### 3.2. Update Synthesis Agent
- **File:** `discernus/agents/thin_synthesis/results_interpreter/agent.py` ✅ **ALREADY IMPLEMENTED**
- **Status:** Results Interpreter is implemented with comprehensive synthesis capabilities
- **Current Features:**
  - Narrative report generation
  - Executive summary creation
  - Key findings extraction
  - Statistical interpretation
- **Changes Needed:**
  - Modify to receive distilled evidence from Evidence Distillation
  - Update prompt to work with new data flow
  - Ensure compatibility with parallel stream architecture

### Phase 4: Pipeline-to-Human Gasket Enhancement
**Duration:** 1 week
**Priority:** Medium

#### 4.1. Implement Mid-Point Data Export
- **File:** `discernus/agents/csv_export_agent.py`
- **New Component:**
  - Create `CSVExportAgent` for mid-experiment data export
  - Generate clean CSV files with raw scores and calculated metrics
  - Include hash-linked evidence references
  - Add export options and configuration

#### 4.2. Update Replication Package
- **File:** `discernus/core/replication_package.py` ✅ **ALREADY IMPLEMENTED**
- **Status:** Replication package functionality is implemented
- **Current Features:**
  - Complete provenance tracking
  - Artifact storage and retrieval
  - Documentation generation
- **Changes Needed:**
  - Ensure compatibility with new data structures
  - Update documentation generation
  - Include both quantitative and qualitative streams
  - Add provenance tracking for gasket operations

### Phase 5: Validation and Testing
**Duration:** 1-2 weeks
**Priority:** Critical

#### 5.1. Comprehensive Testing
- **Files:** Various test files
- **Activities:**
  - Create integration tests for complete gasket workflow
  - Test with multiple framework types
  - Validate data integrity across all streams
  - Performance testing for large datasets
  - Error handling and recovery testing

#### 5.2. Migration Testing
- **Activities:**
  - Test migration from v6.0 to v7.0 frameworks
  - Validate backward compatibility where needed
  - Test existing experiments with new architecture
  - Performance comparison with old system

## 3. Component Dependencies

### Critical Dependencies
1. **Framework Specification v7.0** must be completed before Intelligent Extractor implementation
2. **Intelligent Extractor** must be implemented before refactoring ThinOrchestrator
3. **Raw Analysis Log** concept must be implemented before Evidence Distillation updates

### Parallel Development Opportunities
- CSV Export Agent can be developed independently
- Framework updates can be done in parallel with core gasket development
- Testing infrastructure can be set up early

## 4. Risk Mitigation

### High-Risk Areas
1. **Framework Migration:** Risk of breaking existing experiments
   - **Mitigation:** Maintain backward compatibility during transition period
   - **Mitigation:** Create comprehensive migration tools and documentation

2. **Data Integrity:** Risk of data loss during gasket transition
   - **Mitigation:** Implement comprehensive validation and error handling
   - **Mitigation:** Create data recovery mechanisms

3. **Performance Impact:** Risk of slower processing with additional LLM calls
   - **Mitigation:** Use fast, cheap models for gasket operations
   - **Mitigation:** Implement caching and optimization strategies

### Rollback Plan
- Maintain ability to switch between old and new architectures
- Keep v6.0 framework support during transition
- Create automated rollback procedures

## 5. Success Criteria

### Phase 1 Success Criteria
- [ ] Framework Specification v7.0 completed and documented
- [ ] All active frameworks updated to v7.0
- [ ] Framework validation working correctly
- [ ] No breaking changes to existing experiments

### Phase 2 Success Criteria
- [ ] Intelligent Extractor successfully extracts scores from Raw Analysis Log
- [ ] No more `Data Sparsity` warnings in experiment runs
- [ ] MathToolkit receives clean, flat data structure
- [ ] All existing experiments pass with new architecture

### Phase 3 Success Criteria
- [ ] Evidence Distillation works with Raw Analysis Log
- [ ] Parallel streams (quantitative and qualitative) function correctly
- [ ] Synthesis Agent produces high-quality reports
- [ ] Performance meets or exceeds current system

### Phase 4 Success Criteria
- [ ] Mid-point data export provides clean CSV files
- [ ] Replication package includes all necessary data
- [ ] Researchers can successfully use exported data in external tools

### Phase 5 Success Criteria
- [ ] All tests pass consistently
- [ ] Performance benchmarks met
- [ ] No data integrity issues
- [ ] Successful migration of all existing experiments

## 6. Timeline Summary

- **Week 1-2:** Framework Specification v7.0 and framework updates
- **Week 3-5:** Intelligent Extractor implementation and ThinOrchestrator refactoring
- **Week 6-7:** Evidence Distillation enhancement
- **Week 8:** Pipeline-to-Human gasket enhancement
- **Week 9-10:** Comprehensive testing and validation
- **Week 11:** Final integration and deployment

**Total Estimated Duration:** 11 weeks

## 7. Resource Requirements

### Development Resources
- 1 Senior Developer (full-time) for core gasket implementation
- 1 Developer (part-time) for framework updates and testing
- 1 QA Engineer (part-time) for comprehensive testing

### Infrastructure Resources
- Additional LLM API calls for gasket operations (estimated 20% increase)
- Storage for additional intermediate data (minimal impact)
- Processing time for additional LLM calls (mitigated by fast models)

## 8. Already Implemented Components

### ✅ Fully Implemented and Operational
- **MathToolkit** (`discernus/core/math_toolkit.py`) - Comprehensive mathematical functions
- **THIN Synthesis Pipeline** (`discernus/agents/thin_synthesis/`) - Complete 4-agent architecture
- **Evidence Curator** - Fan-out/fan-in pattern with evidence selection
- **Results Interpreter** - Narrative synthesis and report generation
- **Replication Package** - Provenance tracking and artifact management
- **Validation Agent** (`discernus/agents/experiment_coherence_agent.py`) - Gasket #1

### 🔄 Partially Implemented (Needs Updates)
- **ThinOrchestrator** - Needs gasket integration
- **Framework Validation** - Needs v7.0 schema support

### ❌ Not Yet Implemented
- **Intelligent Extractor Gasket** - Critical gap (Gasket #2)
- **CSV Export Agent** - Mid-point data export (Gasket #3a)
- **Framework Specification v7.0** - New specification with gasket schema

This roadmap provides a clear path from the current THICK architecture to the new THIN Gasket Architecture while minimizing risk and ensuring data integrity throughout the transition. 