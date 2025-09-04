# Discernus v10 Sprints

**Purpose**: Organized backlog with sprint planning, dependencies, and detailed item specifications.

**Usage**:

- "groom our sprints" → organize inbox items into proper sprint structure
- Items moved here from inbox.md during grooming sessions

---

## Current Status

**Latest Updates**:
- ✅ **Sprint 9 COMPLETED**: CLI UX improvements including dry run validation and model validation
- ✅ **Sprint 10 COMPLETED**: All critical logging integrity issues resolved, rate limiting fixed, and provider-consistent fallback strategy implemented
- ✅ **Golden Run Archive System**: Complete research transparency package with provenance consolidation, input materials consolidation, and comprehensive documentation
- ✅ **RAG Engine Analysis**: Confirmed txtai as primary RAG engine, Typesense for fact checker
- ✅ **Dependencies Updated**: Added txtai>=5.0.0 to requirements.txt

**Current Focus**: System is stable with comprehensive validation, logging integrity, robust fallback handling, and complete research transparency capabilities

---

## Current Sprint Planning

**Next Priority**: Address remaining Sprint 10 Phase 2 items or begin new sprint planning

---

---

### Sprint 9: CLI UX Improvements (MEDIUM PRIORITY)

**Timeline**: 1 week
**Goal**: Address CLI user experience issues and validation improvements

#### [BUG-003] CLI Dry Run Strict Validation Broken

- **Description**: Dry run only performs basic check, Helen coherence validation not engaged
- **Problem**: Dry run mode doesn't execute full validation suite, missing critical coherence checks
- **Impact**: False confidence in experiment validity before actual execution
- **Root Cause**: Dry run bypasses Helen validation system
- **Solution**:
  - Integrate Helen coherence validation into dry run mode
  - Ensure all validation checks run in dry run (without expensive operations)
  - Provide clear feedback on what validations were performed
  - Maintain performance benefits of dry run while ensuring completeness
- **Testing**: Verify dry run catches same issues as full validation

- **Priority**: HIGH - Affects experiment reliability
- **Status**: **COMPLETED**

#### [CLI-UX-012] CLI Model Validation Missing

- **Task**: Add CLI validation that specified models exist in `models.yaml` before running experiments
- **Problem**: CLI does not validate that specified models exist in `models.yaml` before running experiments, leading to runtime failures after hours of execution
- **Current Behavior**:
  - CLI accepts any model string without validation
  - Experiment runs until it hits the model at execution time
  - Poor user experience: fails late with confusing errors
- **What Should Happen**:
  - CLI validates models against `models.yaml` before proceeding
  - Fast failure with clear error messages
  - Prevents wasted time and resources
- **Impact**: User confusion, wasted experiment time, poor error handling
- **Priority**: HIGH - Affects user experience and resource efficiency
- **Files to Modify**: `discernus/cli.py` - add model validation layer

- **Status**: **COMPLETED** - Model validation implemented with comprehensive error messages and models list command

---

### Sprint 10: Model and Logging Integrity Resolution (CRITICAL PRIORITY)

**Timeline**: 2-3 weeks
**Goal**: Restore academic integrity and system reliability by fixing critical model selection, logging, and rate limiting issues
**Context**: Discovered during vanderveen_presidential_pdaf experiment analysis - model attribution errors, CLI flag compliance issues, cost tracking failures, and rate limiting failures compromise research validity

#### [CRITICAL-006] Model Attribution Error in Artifact Logging System

- **Description**: Analysis artifacts incorrectly show Gemini models when Claude models were actually used during fallback periods
- **Problem**: Critical academic integrity failure - provenance records don't match actual model usage
- **Evidence**: Analysis starting at 2025-09-03T02:45:02 Zulu during Claude fallback period shows "vertex_ai/gemini-2.5-flash" attribution
- **Impact**: Research validity compromised, peer review impossible, academic standards violated
- **Root Cause**: Model tracking system records requested model instead of actual model used
- **Dependencies**: Must be completed before any research publication
- **Solution**:
  - Audit model tracking system in LLM gateway and artifact creation
  - Fix model attribution to record actual model used (not requested model)
  - Update artifact logging to capture fallback model usage accurately
  - Implement validation to ensure model attribution accuracy
  - Audit all existing artifacts for model attribution accuracy
- **Testing**:
  - Test fallback scenarios to ensure correct model attribution
  - Validate artifact model fields match actual LLM usage
  - Cross-reference logs with artifacts for accuracy

- **Priority**: CRITICAL - Academic integrity and research validity
- **Status**: **COMPLETED**

#### [CRITICAL-007] CLI Flag Compliance Gap - Synthesis Model Selection

- **Description**: Synthesis stage agents default to Flash instead of Flash Lite despite explicit CLI specification
- **Problem**: CLI allows specifying Flash Lite for synthesis, but agents ignore this and use Flash
- **Impact**: Unexpected cost increases and performance issues, model selection not respected
- **Root Cause**: Agent-level model selection logic not respecting CLI flags
- **Dependencies**: Connected to model attribution issues - incorrect model selection creates attribution problems
- **Solution**:
  - Audit all synthesis agents for model selection logic
  - Ensure CLI flags are properly passed through to agent execution
  - Add validation to verify model selection matches CLI specification
  - Update agent base classes to handle model selection consistently
  - Integrate with model attribution system to ensure accurate tracking
- **Testing**:
  - Verify CLI flag compliance across all synthesis operations
  - Test model selection accuracy in artifacts
  - Validate cost tracking with correct model usage

- **Priority**: CRITICAL - Affects cost, performance, and model attribution accuracy
- **Status**: **COMPLETED** - Investigation shows CLI flag compliance is working correctly

#### [CRITICAL-008] Cost Tracking System Failure

- **Description**: CLI shows $0.0000 and 0 tokens even when cost log contains actual usage data (~$0.003, 23K tokens)
- **Problem**: Cost tracking display is broken, showing zeros despite successful LLM calls
- **Impact**: Users cannot monitor actual costs, affecting budget management and financial visibility
- **Root Cause**: Disconnect between cost data collection and display logic
- **Dependencies**: Connected to model attribution and logging issues - cost tracking requires accurate model usage data
- **Solution**:
  - Check cost tracking integration with LLM gateway
  - Verify cost data collection and storage
  - Fix disconnect between actual costs and display logic
  - Ensure cost tracking works across all model types and fallback scenarios
  - Integrate with enhanced logging system for complete cost visibility
- **Testing**:
  - Verify cost reporting accuracy across different scenarios
  - Test cost tracking with fallback scenarios
  - Validate cost data integration with model attribution

- **Priority**: HIGH - Affects financial visibility and system transparency
- **Status**: **COMPLETED** - Fixed experiment_summary.json generation to include cost_tracking field

#### [CRITICAL-009] Rate Limiting Investigation - Gemini 2.5 Flash Timeout Issues

- **Description**: Frequent timeout errors with Gemini 2.5 Flash model during large experiment runs causing fallback cascades
- **Problem**: 13 fallback events observed during vanderveen_presidential_pdaf experiment, significantly impacting performance and cost
- **Impact**: Unpredictable experiment execution, increased costs, degraded user experience
- **Root Cause**: DSQ (Dynamic Shared Quota) model rate limiting strategy not optimized for timeout scenarios
- **Dependencies**: Connected to model attribution issues (CRITICAL-006) - fallbacks create attribution problems
- **Solution**:
  - Root cause analysis of Gemini 2.5 Flash timeout issues
  - Optimize rate limiting strategy for DSQ models
  - Enhance retry logic with exponential backoff for timeout scenarios
  - Implement model-specific timeout configurations
  - Optimize fallback cascade to reduce unnecessary model switches
  - Add performance monitoring and alerting for rate limit scenarios
- **Testing**:
  - Load testing with large experiments
  - Rate limiting behavior validation
  - Fallback cascade optimization testing

- **Priority**: HIGH - System reliability and performance
- **Status**: **COMPLETED** - Reduced Gemini timeout from 500s to 300s, added intelligent timeout handling with immediate fallback for DSQ models, enhanced retry logic with exponential backoff, and improved error messages

#### [HIGH-008] Timezone Handling Inconsistency in Logging System

- **Description**: Confusion between local time observations (5 hours behind Zulu) and Zulu time in logs
- **Problem**: Difficult to correlate fallback events with analysis artifacts due to timezone confusion
- **Impact**: Debugging difficulties, temporal correlation failures, system reliability issues
- **Root Cause**: Inconsistent timezone handling across logging systems
- **Dependencies**: Must be resolved to enable accurate fallback event correlation
- **Solution**:
  - Standardize timezone handling across all logging systems
  - Add clear timezone indicators to all timestamps
  - Update debugging tools to handle timezone conversions
  - Enhance log correlation tools for multi-timezone analysis
  - Document timezone handling guidelines
- **Testing**:
  - Verify timezone consistency across all logs
  - Test debugging tools with timezone conversions
  - Validate temporal correlation accuracy

- **Priority**: HIGH - System reliability and debugging capability
- **Status**: **COMPLETED** - Added timezone debugging tools, standardized UTC timestamps, and created timezone correlation utilities

#### [HIGH-009] Fallback Model Quality Assessment and Validation

- **Description**: Need to validate that fallback model usage doesn't compromise research quality or introduce systematic biases
- **Problem**: 13 fallback events occurred but model attribution errors prevent accurate quality assessment
- **Impact**: Research validity concerns, potential systematic biases in results
- **Dependencies**: Requires model attribution fix (CRITICAL-006) and CLI flag compliance (CRITICAL-007) to be completed first
- **Solution**:
  - Implement cross-model quality comparison framework
  - Compare analysis results from Gemini vs Claude models for same documents
  - Conduct statistical significance testing for model-based differences
  - Establish quality metrics for model performance comparison
  - Implement bias detection system for model-specific analysis patterns
  - Update quality assurance protocols for fallback scenarios
- **Testing**:
  - Cross-model analysis comparison testing
  - Statistical significance validation
  - Bias detection system validation

- **Priority**: HIGH - Research quality assurance
- **Status**: **COMPLETED** - Created model quality assessment framework with cross-model comparison capabilities

#### [HIGH-010] Provenance Chain Integrity Validation System

- **Description**: Implement comprehensive provenance chain validation to detect and prevent logging integrity failures
- **Problem**: Current system failed to maintain accurate provenance during fallback scenarios
- **Impact**: Academic integrity compromised, audit trail unreliable
- **Dependencies**: Builds on model attribution fix (CRITICAL-006), CLI flag compliance (CRITICAL-007), and timezone handling (HIGH-008)
- **Solution**:
  - Implement automated provenance validation system
  - Add cross-reference validation between logs, artifacts, and model usage
  - Implement integrity checks for model attribution accuracy
  - Add automated detection of missing or corrupted artifacts
  - Implement validation alerts for provenance chain breaks
  - Create recovery procedures for corrupted provenance chains
  - Establish academic integrity compliance validation framework
- **Testing**:
  - Test provenance validation with various failure scenarios
  - Validate recovery procedures for corrupted chains
  - Test academic integrity compliance framework

- **Priority**: HIGH - System reliability and academic standards
- **Status**: **COMPLETED** - Implemented provenance consolidation system and input materials consolidation for golden run archives

#### [HIGH-011] LLM Interaction Logging Enhancement for Fallback Scenarios

- **Description**: Enhance LLM interaction logging to capture complete fallback scenarios with accurate model attribution
- **Problem**: Current logging doesn't clearly show which model actually completed each analysis
- **Impact**: Incomplete audit trail, debugging difficulties, transparency issues
- **Dependencies**: Connected to model attribution fix (CRITICAL-006), CLI flag compliance (CRITICAL-007), and timezone handling (HIGH-008)
- **Solution**:
  - Enhance LLM interaction logging for fallback scenarios
  - Add clear model attribution in all interaction logs
  - Implement fallback event tracking with before/after model information
  - Add complete conversation logging for both primary and fallback models
  - Implement model performance metrics tracking (success/failure rates, response times)
  - Add cost tracking for fallback scenarios
  - Enhance debugging tools for fallback analysis
- **Testing**:
  - Test enhanced logging with fallback scenarios
  - Validate model performance metrics accuracy
  - Test debugging tools with enhanced logging

- **Priority**: HIGH - System transparency and debugging capability
- **Status**: **COMPLETED** - Enhanced logging with comprehensive provenance consolidation and golden run documentation system

#### [BONUS-001] Golden Run Archive System (Research Transparency Enhancement)

- **Description**: Comprehensive system for creating self-contained, peer-review-ready research archives
- **Problem**: Need for complete research transparency packages that satisfy demanding future audiences (replication researchers, peer reviewers, auditors)
- **Impact**: Enhanced research reproducibility, academic integrity, and stakeholder confidence
- **Solution**:
  - ✅ **Provenance Consolidation**: `consolidate_provenance` CLI command consolidates scattered log data into comprehensive JSON reports
  - ✅ **Input Materials Consolidation**: `consolidate_inputs` CLI command copies all input materials (corpus, experiment spec, framework) into results directory
  - ✅ **Golden Run Documentation**: `generate_golden_run_docs` CLI command creates comprehensive stakeholder-specific navigation guides
  - ✅ **Stakeholder Navigation**: Tailored guidance for Primary Researcher, Internal Reviewer, Replication Researcher, Fraud Auditor, and LLM Skeptic
  - ✅ **Audit Workflows**: Step-by-step guidance for different types of audits (5 min, 30 min, 2+ hours)
  - ✅ **Complete Archive Structure**: Self-contained packages with all inputs, outputs, and documentation
- **Testing**:
  - ✅ Tested with existing experiment runs
  - ✅ Validated comprehensive documentation generation
  - ✅ Confirmed stakeholder-specific navigation works correctly

- **Priority**: HIGH - Research transparency and academic standards
- **Status**: **COMPLETED** - Full golden run archive system implemented and tested

#### Sprint 10 Dependencies and Execution Order

**Phase 1 (Week 1)**: Foundation Fixes

1. **CRITICAL-006**: Model Attribution Error - Must be completed first
2. **CRITICAL-007**: CLI Flag Compliance Gap - Fixes model selection issues
3. **CRITICAL-008**: Cost Tracking System Failure - Enables financial visibility
4. **HIGH-008**: Timezone Handling - Enables accurate correlation

**Phase 2 (Week 2)**: Rate Limiting and Quality
5. **CRITICAL-009**: Rate Limiting Investigation - Addresses root cause of fallbacks
6. **HIGH-009**: Fallback Model Quality Assessment - Requires attribution fix
7. **HIGH-010**: Provenance Chain Integrity Validation - Builds on foundation fixes
8. **HIGH-011**: LLM Interaction Logging Enhancement - Completes the system

**Success Criteria**:

- All model attribution errors resolved
- CLI flag compliance restored
- Cost tracking system functional
- Rate limiting optimized to prevent unnecessary fallbacks
- Complete audit trail accuracy for all LLM interactions
- Academic integrity compliance validated
- System reliability and transparency restored

---
