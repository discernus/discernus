# Alpha Quality & Hygiene Milestone

**Milestone**: Alpha Quality & Hygiene
**Status**: Active
**Issues**: Open issues related to code quality, testing, and system hygiene for Alpha release

---

## Open Issues

### Framework v7.4 Specification with Gasket Markers
- **Issue**: #431
- **Labels**: gasket-architecture
- **Assignees**: 
- **Created**: 2025-08-13
- **Updated**: 2025-08-13
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Framework v7.4 Specification with Gasket Markers

**Full Description**:
Create Framework v7.4 specification that standardizes on gasket markers for all framework components.

## Overview
Create a new framework specification version (v7.4) that standardizes on gasket markers for all framework components, including configuration, calculation specs, and other specifications.

## Current Status
- **Framework v7.3**: Includes gasket schema but not configuration
- **Framework Configuration**: Uses HTML details tags (already a form of gasket marker)
- **Calculation Specs**: Still embedded in JSON code blocks
- **Priority**: LONG-TERM (after other conversions complete)

## Implementation Details
### Changes Needed
1. Define Framework v7.4 specification with comprehensive gasket requirements
2. Standardize all framework components to use proprietary markers
3. Create migration guide for existing frameworks
4. Update validation agents to enforce v7.4 compliance

### Gasket Marker Standardization
All framework components should use proprietary markers:
- Configuration: <<<DISCERNUS_CONFIG_V1>>> ... <<<END_DISCERNUS_CONFIG_V1>>>
- Calculation Specs: <<<DISCERNUS_CALC_SPEC_V1>>> ... <<<END_DISCERNUS_CALC_SPEC_V1>>>
- Gasket Schema: <<<GASKET_SCHEMA_START>>> ... <<<GASKET_SCHEMA_END>>>

## Benefits
- Complete gasket architecture compliance
- Unified extraction approach across all framework components
- Better validation and error handling
- Future-proof framework specification
- Architectural consistency

## Risk Assessment
- **High Risk**: Requires updates to all existing frameworks
- **Migration Effort**: Significant work to update existing framework files
- **Backward Compatibility**: Need to maintain support for older versions

## Success Criteria
- Framework v7.4 specification defined and documented
- All new frameworks use v7.4 specification
- Migration guide created for existing frameworks
- Validation agents enforce v7.4 compliance
- 100% gasket compliance achieved

## Dependencies
- Epic #426: Complete Gasket Architecture Implementation
- All other gasket conversion issues completed
- Assessment document reference: @TRADITIONAL_PARSING_GASKET_ASSESSMENT.md

## Related Issues
- Part of systematic gasket conversion effort
- Final step in achieving complete gasket compliance
- Long-term architectural improvement

---

### Complete Synthesis Pipeline Gasket Implementation
- **Issue**: #430
- **Labels**: gasket-architecture
- **Assignees**: 
- **Created**: 2025-08-13
- **Updated**: 2025-08-13
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Complete Synthesis Pipeline Gasket Implementation

**Full Description**:
Complete the synthesis pipeline gasket implementation by converting framework calculation spec parsing to gasket architecture.

## Overview
Complete the synthesis pipeline gasket implementation by converting the remaining manual JSON parsing for framework calculation specs to use gasket architecture.

## Current Status
- **Gasket Schema Extraction**: ✅ Fully implemented with proprietary markers
- **Framework Calculation Specs**: ❌ Still uses manual JSON parsing with regex
- **Location**: discernus/agents/thin_synthesis/orchestration/pipeline.py
- **Priority**: MEDIUM (after higher-impact conversions)

## Implementation Details
### Changes Needed
1. Extend gasket schema specification to include calculation specs
2. Update framework specification to require calculation specs in gasket format
3. Modify _extract_gasket_schema function to include calculation spec extraction
4. Update existing frameworks to include calculation specs in gasket format

### Gasket Schema Extension
Extend gasket schema to include calculation specifications with execution_order, formulas, and dependencies.

## Benefits
- Unified extraction approach for all framework specifications
- LLM validation of mathematical formulas and execution order
- Better error handling for malformed calculation specs
- 100% gasket compliance for framework specifications
- Architectural consistency

## Risk Assessment
- **Medium Risk**: Framework calculation specs are important but not critical for basic operation
- **Compatibility**: MathToolkit expects standardized calculation spec format
- **Fallback**: Could maintain current parsing as fallback during transition

## Success Criteria
- All framework specifications use gasket format for calculation specs
- Calculation spec validation improved with LLM intelligence
- No regression in synthesis pipeline functionality
- Integration tests pass
- 100% gasket compliance achieved for framework specifications

## Dependencies
- Epic #426: Complete Gasket Architecture Implementation
- Framework specification updates
- Assessment document reference: @TRADITIONAL_PARSING_GASKET_ASSESSMENT.md

## Related Issues
- Part of systematic gasket conversion effort
- Completes framework specification gasket implementation
- Integrates with synthesis pipeline improvements

---

### Convert Evidence Extraction to Gasket Architecture
- **Issue**: #429
- **Labels**: gasket-architecture
- **Assignees**: 
- **Created**: 2025-08-13
- **Updated**: 2025-08-13
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Convert Evidence Extraction to Gasket Architecture

**Full Description**:
Convert Enhanced Analysis Agent evidence extraction from legacy regex parsing to gasket architecture.

## Overview
Convert the Evidence Extraction component from legacy regex parsing to full gasket architecture using proprietary markers and Intelligent Extractor.

## Current Status
- **Method**: Regex extraction with proprietary markers <<<DISCERNUS_ANALYSIS_JSON_v6>>> + json.loads in response_parser.py
- **Location**: discernus/agents/EnhancedAnalysisAgent/response_parser.py
- **Priority**: MEDIUM (after higher-impact conversions)

## Implementation Details
### Changes Needed
1. Update evidence extraction prompt to use gasket markers
2. Modify _extract_evidence_from_analysis_response function to use Intelligent Extractor
3. Update evidence format to include gasket metadata
4. Extend existing proprietary markers to gasket format

### Gasket Markers
Extend existing proprietary markers to gasket format:
- Start: <<<DISCERNUS_EVIDENCE_GASKET_V1>>>
- End: <<<END_DISCERNUS_EVIDENCE_GASKET_V1>>>

## Benefits
- Robust evidence extraction with LLM intelligence
- Better handling of malformed JSON and edge cases
- Partial evidence recovery when extraction fails
- Consistent with overall gasket architecture
- Improved synthesis pipeline reliability

## Risk Assessment
- **Medium Risk**: Evidence format is well-encapsulated but critical for synthesis
- **Compatibility**: Downstream consumers expect standardized evidence format
- **Fallback**: Could maintain regex parsing as fallback during transition

## Success Criteria
- Evidence extraction uses gasket markers consistently
- Error handling improved with LLM intelligence
- No regression in evidence extraction functionality
- Integration tests pass
- Synthesis pipeline continues to work reliably

## Dependencies
- Epic #426: Complete Gasket Architecture Implementation
- Intelligent Extractor infrastructure
- Assessment document reference: @TRADITIONAL_PARSING_GASKET_ASSESSMENT.md

## Related Issues
- Part of systematic gasket conversion effort
- Critical for synthesis pipeline reliability
- Integrates with Enhanced Analysis Agent improvements

---

### Convert Confidence Calibration to Gasket Architecture
- **Issue**: #428
- **Labels**: gasket-architecture
- **Assignees**: 
- **Created**: 2025-08-13
- **Updated**: 2025-08-13
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Convert Confidence Calibration to Gasket Architecture

**Full Description**:
Convert Evidence Confidence Calibrator from manual markdown extraction to gasket architecture.

## Overview
Convert the Confidence Calibration component from manual markdown code block extraction to full gasket architecture using proprietary markers.

## Current Status
- **Method**: Manual markdown code block extraction with json.loads in _parse_calibration_response function
- **Location**: discernus/core/evidence_confidence_calibrator.py
- **Priority**: HIGH (good candidate for early conversion)

## Implementation Details
### Changes Needed
1. Update calibration prompt to use gasket markers
2. Modify _parse_calibration_response function to use Intelligent Extractor
3. Update calibration response format to include gasket metadata

### Gasket Markers
Use proprietary markers for calibration responses:
- Start: <<<DISCERNUS_CALIBRATION_JSON_V1>>>
- End: <<<END_DISCERNUS_CALIBRATION_JSON_V1>>>

## Benefits
- Standardized calibration response format
- Better error recovery and handling
- Improved academic quality validation
- Better batch processing capabilities
- Aligns with architecture vision

## Risk Assessment
- **Low Risk**: Calibration response format is well-encapsulated
- **Compatibility**: Assessment generation expects standardized calibration format
- **Fallback**: Could maintain current parsing as fallback during transition

## Success Criteria
- Calibration responses use gasket markers consistently
- Error handling improved with LLM intelligence
- No regression in calibration functionality
- Integration tests pass
- Batch processing improved

## Dependencies
- Epic #426: Complete Gasket Architecture Implementation
- Intelligent Extractor infrastructure
- Assessment document reference: @TRADITIONAL_PARSING_GASKET_ASSESSMENT.md

## Related Issues
- Part of systematic gasket conversion effort
- Integrates with Evidence Confidence Calibrator improvements

---

### Convert Score Validation to Gasket Architecture
- **Issue**: #427
- **Labels**: gasket-architecture
- **Assignees**: 
- **Created**: 2025-08-13
- **Updated**: 2025-08-13
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Convert Score Validation to Gasket Architecture

**Full Description**:
Convert Score Validation Orchestrator from manual JSON extraction to gasket architecture.

## Overview
Convert the Score Validation component from manual JSON extraction with markdown fallback to full gasket architecture using proprietary markers.

## Current Status
- **Method**: Manual JSON extraction with markdown code block fallback in _parse_validation_response function
- **Location**: discernus/orchestration/score_validation_orchestrator.py
- **Priority**: HIGH (good candidate for early conversion)

## Implementation Details
### Changes Needed
1. Update validation prompt to use gasket markers
2. Modify _parse_validation_response function to use Intelligent Extractor
3. Update validation response format to include gasket metadata

### Gasket Markers
Use proprietary markers for validation responses:
- Start: <<<DISCERNUS_VALIDATION_JSON_V1>>>
- End: <<<END_DISCERNUS_VALIDATION_JSON_V1>>>

## Benefits
- Standardized validation response format
- Better error recovery and handling
- Improved researcher experience
- Aligns with architecture vision

## Risk Assessment
- **Low Risk**: Validation response format is well-encapsulated
- **Compatibility**: Report generation expects standardized validation format
- **Fallback**: Could maintain current parsing as fallback during transition

## Success Criteria
- Validation responses use gasket markers consistently
- Error handling improved with LLM intelligence
- No regression in validation functionality
- Integration tests pass

## Dependencies
- Epic #426: Complete Gasket Architecture Implementation
- Intelligent Extractor infrastructure
- Assessment document reference: @TRADITIONAL_PARSING_GASKET_ASSESSMENT.md

## Related Issues
- Part of systematic gasket conversion effort
- Integrates with Score Validation Orchestrator improvements

---

### Epic: Complete Gasket Architecture Implementation
- **Issue**: #426
- **Labels**: epic, architecture, gasket-architecture
- **Assignees**: 
- **Created**: 2025-08-13
- **Updated**: 2025-08-13
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Epic: Complete Gasket Architecture Implementation

**Full Description**:
Complete the transition from traditional parsing methods to full gasket architecture compliance across the Discernus system.

## Overview
This epic addresses the systematic conversion of traditional parsing methods to gasket architecture, as identified in the comprehensive assessment document @TRADITIONAL_PARSING_GASKET_ASSESSMENT.md.

## Current Status
The Discernus system is more gasket-compliant than initially assessed:
- ✅ **Fully Implemented**: Analysis → MathToolkit (Gasket #2), Framework Schema Extraction (Gasket #1)
- 🔄 **Partially Implemented**: Synthesis Pipeline (Gasket schema + manual parsing)
- ❌ **Legacy Parsing**: Evidence Extraction, Score Validation, Confidence Calibration

## Strategic Goals
1. Achieve 100% gasket architecture compliance
2. Improve system robustness and error recovery
3. Standardize LLM response parsing across all components
4. Maintain system stability during transition

## Success Criteria
- All five identified components converted to gasket architecture
- No regression in system functionality
- Improved error handling and recovery
- Consistent proprietary marker usage throughout
- Full gasket compliance achieved

## Dependencies
- Assessment document completion
- Existing gasket infrastructure (Intelligent Extractor, proprietary markers)
- Framework specification updates

## Epic Type
Architecture Improvement

---

### Harden calculation_spec extraction in synthesis pipeline
- **Issue**: #412
- **Labels**: tech-debt
- **Assignees**: 
- **Created**: 2025-08-11
- **Updated**: 2025-08-11
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Harden calculation_spec extraction in synthesis pipeline

**Full Description**:
The synthesis pipeline currently uses a brittle regex to extract the 'calculation_spec' from the framework's JSON appendix. This is a code smell and violates THIN principles. We should refactor this to use a more robust method, such as proprietary markers, similar to the recent fix for the 'gasket_schema'. This will improve the system's resilience to parsing failures and ensure that the synthesis pipeline is not making assumptions about the framework's structure.

---

### Phase 4: Summit the Extreme Case - Large Scale Reliability (47.1% → 99%)
- **Issue**: #398
- **Labels**: enhancement, performance
- **Assignees**: 
- **Created**: 2025-08-10
- **Updated**: 2025-08-12
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Phase 4: Summit the Extreme Case - Large Scale Reliability (47.1% → 99%)

**Epic**: 394

---

### Phase 3: Scale the Challenging Terrain - Multi-Framework Reliability (77.8% → 95%)
- **Issue**: #397
- **Labels**: enhancement
- **Assignees**: 
- **Created**: 2025-08-10
- **Updated**: 2025-08-12
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Phase 3: Scale the Challenging Terrain - Multi-Framework Reliability (77.8% → 95%)

**Epic**: 394

---

### Phase 2: Strengthen the Proven Path - CAF Reliability (80.6% → 90%)
- **Issue**: #396
- **Labels**: enhancement
- **Assignees**: 
- **Created**: 2025-08-10
- **Updated**: 2025-08-12
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Phase 2: Strengthen the Proven Path - CAF Reliability (80.6% → 90%)

**Epic**: 394

---

### Phase 1: Fix the Foundation - simple_test Reliability (66.2% → 85%)
- **Issue**: #395
- **Labels**: enhancement
- **Assignees**: 
- **Created**: 2025-08-10
- **Updated**: 2025-08-12
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Phase 1: Fix the Foundation - simple_test Reliability (66.2% → 85%)

**Epic**: 394

---

### Epic: Reliability Improvement Gauntlet (66% → 99%)
- **Issue**: #394
- **Labels**: enhancement, epic
- **Assignees**: 
- **Created**: 2025-08-10
- **Updated**: 2025-08-12
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Epic: Reliability Improvement Gauntlet (66% → 99%)

**Full Description**:
# Epic: Reliability Improvement Gauntlet (66% → 99%)

## Problem Statement

Current system reliability varies dramatically across experiments:
- `simple_test`: 66.2% (⚠️ Needs Attention) - validation failures
- `1a_caf_civic_character`: 80.6% (🟡 Good) - best performer
- `1b_chf_character_heuristics`: 77.8% (⚠️ Warning) - moderate issues  
- `3_large_batch_test`: 47.1% (🚨 Critical) - severe reliability issues

This inconsistency prevents reliable research workflows and undermines academic validity.

## Goal

Achieve systematic 99% reliability across all experiment types through data-driven improvement methodology using the new telemetry infrastructure.

## Success Criteria

**Primary Success Criteria:**
- [ ] `simple_test`: 66.2% → 90%+ (foundation reliability)
- [ ] `1a_caf_civic_character`: 80.6% → 95%+ (proven path optimization)
- [ ] `1b_chf_character_heuristics`: 77.8% → 95%+ (framework reliability)
- [ ] `3_large_batch_test`: 47.1% → 90%+ (scale reliability)
- [ ] All experiments: Overall system reliability >99%

**Internal Success Criteria:**
- [ ] Telemetry-driven improvement methodology established
- [ ] Common failure patterns identified and systematically addressed
- [ ] Framework-specific reliability patterns documented
- [ ] Scalability reliability issues resolved

## User Impact

**Before**: Unreliable experiment execution requiring manual intervention and debugging

**After**: Predictable, reliable research workflows with <1% failure rate for valid experiments

## Technical Approach

**"Base Camp to Summit" Strategy:**

### Phase 1: Fix the Foundation (Target: 85%)
- Focus: `simple_test` + validation infrastructure integration
- Fix critical validation failures preventing reliable operation
- Establish baseline reliability measurement and improvement workflow

### Phase 2: Strengthen the Proven Path (Target: 90%)  
- Focus: `1a_caf_civic_character` (already 80.6%)
- Analyze and fix the 7 failures out of 36 runs
- Establish framework-specific reliability patterns

### Phase 3: Scale the Challenging Terrain (Target: 95%)
- Focus: `1b_chf_character_heuristics` + similar experiments
- Cross-framework reliability pattern analysis
- Framework-agnostic reliability improvements

### Phase 4: Summit the Extreme Case (Target: 99%)
- Focus: `3_large_batch_test` (currently 47.1%)
- Large-scale experiment reliability challenges
- Resource and timeout optimization

## Implementation Strategy

**THIN Fix Protocol** for each phase:
1. **📊 Baseline Telemetry**: `discernus telemetry projects/X`
2. **🔍 Deep Analysis**: `discernus telemetry-report projects/X -o analysis.md`
3. **🎯 Identify Top 3 Failure Patterns**: Focus on highest-impact fixes
4. **⚡ Apply Targeted Fixes**: Use reliability agents for validation
5. **✅ Validate Fix**: Run experiment + measure improvement
6. **📈 Confirm Improvement**: Telemetry should show >5% improvement
7. **🔄 Iterate**: Repeat until target reliability reached

## Definition of Done

- All target experiments achieve >90% reliability
- Overall system reliability >99% for valid experiments
- Telemetry infrastructure demonstrates measurable improvement trends
- Systematic reliability improvement methodology documented
- Framework-specific reliability patterns documented for future development

## Dependencies

- ✅ Research Infrastructure Reliability Epic (#389) - COMPLETED
- ✅ Developer telemetry dashboard - COMPLETED  
- ✅ Reliability validation agents - COMPLETED


---

### Enhance rate limiting to use model-specific TPM/RPM data
- **Issue**: #385
- **Labels**: enhancement
- **Assignees**: 
- **Created**: 2025-08-10
- **Updated**: 2025-08-10
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Enhance rate limiting to use model-specific TPM/RPM data

**Full Description**:
# Enhance Rate Limiting System to Utilize Model-Specific TPM/RPM Data

## Problem Statement

The models.yaml file now contains comprehensive TPM (Tokens Per Minute) and RPM (Requests Per Minute) data for all models, including **Dynamic Shared Quota (DSQ) models** which have `null` rate limits. The current rate limiting implementation needs updating to handle both fixed quotas and DSQ models appropriately.

## Current State Analysis

**Rate Limiting Architecture:**
- ✅ **ratelimit library integrated** (Issue #382 completed)
- ✅ **models.yaml TPM/RPM data** complete for all models
- ✅ **Provider defaults configured** with Tier 2 account limits
- ❌ **DSQ models not handled** - they have `tpm: null, rpm: null`
- ❌ **Model-specific limits ignored** in favor of provider defaults

**Updated Models Configuration (2025-08-10):**
```yaml
# Fixed Quota Models (Anthropic, OpenAI)
anthropic/claude-4-sonnet:
  input_tpm: 450000
  output_tpm: 90000  
  rpm: 1000

# DSQ Models (Vertex AI) - No Fixed Limits
vertex_ai/gemini-2.5-pro:
  tpm: null           # Dynamic Shared Quota
  rpm: null           # No fixed limits
  dsq_enabled: true   # Handle 429 errors differently
```

## Required Enhancements

### 1. DSQ-Aware Rate Limiting
- **DSQ models (`tpm: null`)**: Skip traditional rate limiting, implement retry logic for 429 errors
- **Fixed quota models**: Use model-specific TPM/RPM limits
- **Hybrid approach**: Different strategies per quota type

### 2. Model-Specific Rate Limiting (Fixed Quota Only)
- Read `tpm`, `rpm`, `input_tpm`, `output_tpm` from individual model configs
- Fall back to provider defaults only when model limits undefined
- Implement per-model rate limiting for fixed-quota models

### 3. Enhanced Error Handling
- **DSQ 429 errors**: Exponential backoff with retry (capacity exhaustion, not quota violation)
- **Fixed quota 429 errors**: Traditional rate limiting with longer delays
- **Error differentiation**: Handle different provider error patterns

### 4. Token-Aware Rate Limiting
- Track input/output tokens separately for models with separate limits
- Implement sliding window token rate limiting for fixed-quota models
- Skip token limiting for DSQ models (handled by server-side capacity)

## Technical Implementation Strategy

### Enhanced Rate Limiter Architecture
```python
class ModelRateLimiter:
    def __init__(self, model_config: dict):
        self.model_config = model_config
        self.is_dsq = model_config.get('tpm') is None
        
        if not self.is_dsq:
            # Fixed quota - create rate limiters
            self.rpm_limiter = limits(calls=model_config.get('rpm', 100), period=60)
            self.tpm_limiter = token_limits(tokens=model_config.get('tpm', 60000), period=60)
        else:
            # DSQ - no pre-emptive limiting
            self.rpm_limiter = None
            self.tpm_limiter = None
    
    def execute_with_limiting(self, completion_func, *args, **kwargs):
        if self.is_dsq:
            # DSQ: Try direct call, handle 429s with retry
            return self._execute_dsq_with_retry(completion_func, *args, **kwargs)
        else:
            # Fixed quota: Pre-emptive rate limiting
            return self._execute_fixed_quota(completion_func, *args, **kwargs)
```

### Files to Modify
- `discernus/gateway/llm_gateway.py` - DSQ vs fixed quota handling
- `discernus/gateway/model_registry.py` - Model quota type detection
- Add DSQ retry logic with exponential backoff

## Updated Success Criteria

**DSQ Models (Vertex AI):**
- [ ] No pre-emptive rate limiting applied
- [ ] 429 errors handled with exponential backoff retry
- [ ] Retry logic distinguishes capacity exhaustion from quota violations
- [ ] Fallback to premium models after multiple DSQ failures

**Fixed Quota Models (Anthropic, OpenAI):**
- [ ] Model-specific RPM/TPM limits enforced when defined
- [ ] Separate input/output TPM limiting where applicable
- [ ] Traditional rate limiting prevents 429 errors proactively
- [ ] Fallback to provider defaults when model limits undefined

**Architecture:**
- [ ] Rate limiting strategy determined by quota type (`tpm: null` = DSQ)
- [ ] Performance: <5ms overhead for fixed quota, <1ms for DSQ
- [ ] Configuration-driven from updated models.yaml
- [ ] Clean integration with existing error handling

## Current Priority: Medium

**Rationale**: System works well with current architecture. This enhancement optimizes rate limiting for the mixed DSQ/fixed-quota environment but doesn't block core functionality.

**Dependencies**:
- ✅ Updated models.yaml with DSQ configuration (completed 2025-08-10)
- ✅ ratelimit library integration (Issue #382 completed)
- 🔄 DSQ-aware error handling implementation needed

**Implementation Approach**:
1. Detect quota type from model configuration (`tpm: null` indicates DSQ)
2. Apply different rate limiting strategies per quota type
3. Implement DSQ-specific retry logic with exponential backoff
4. Maintain existing fixed-quota rate limiting for Anthropic/OpenAI models

This enhancement aligns with the **Gemini-first DSQ architecture** while maintaining premium model reliability for validation tasks.

---

### Epic: Academic Quality & Standards Implementation
- **Issue**: #365
- **Labels**: enhancement, epic
- **Assignees**: 
- **Created**: 2025-08-09
- **Updated**: 2025-08-11
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Epic: Academic Quality & Standards Implementation

**Full Description**:
Epic: Academic Quality & Standards Implementation

## Objective
Implement comprehensive academic standards, peer review preparation, quality assurance frameworks, performance audit, LLM model selection guidance, complete agent architecture documentation, and THIN compliance cleanup to ensure Discernus outputs meet top-tier academic journal requirements and stakeholders have complete understanding of system capabilities, limitations, and clean implementation architecture. **Enhanced to support Sequential Synthesis Agent Architecture v2.0 quality standards.**

## Strategic Context
This epic focuses on elevating the quality and academic rigor of Discernus outputs, building upon the Sequential Synthesis Agent Architecture v2.0 foundation. These enhancements ensure research outputs are publication-ready, meet academic excellence standards, provide transparent performance documentation for release readiness, offer principled guidance for optimal system configuration across our multi-model architecture, bridge the gap between architectural vision and concrete implementation through comprehensive agent documentation, and eliminate THIN architecture violations through systematic cleanup. **Now includes validation of Evidence-First synthesis, Token-Budget discipline, and No-LM-Math constraints.**

## Requirements

### Academic Excellence Standards
- **REQ-AQ-001**: Implement evidence citation standards matching top journals
- **REQ-AQ-002**: Create evidence provenance transparency requirements  
- **REQ-AQ-003**: Build evidence strength validation protocols
- **REQ-AQ-004**: Implement evidence diversity requirements (>3 sources per claim)
- **REQ-AQ-005**: Create evidence synthesis quality benchmarks

### Sequential Synthesis Quality Standards (NEW)
- **REQ-SS-001**: Evidence-First Synthesis Validation - Every interpretive claim must be linked to at least one statistical result AND one textual quote
- **REQ-SS-002**: Token-Budget Discipline Enforcement - Each sequential step must operate under measurable token limits with automatic budget validation
- **REQ-SS-003**: No-LM-Math Constraint Validation - Automated detection and prevention of LLM mathematical computations in synthesis pipeline  
- **REQ-SS-004**: Framework Fit Assessment Quality Standards - Quantitative framework fit assessment must appear in every final report with appropriate tier methodology
- **REQ-SS-005**: Sequential Step Quality Validation - Each of the 5 sequential steps must meet specific quality thresholds and integration requirements

### Quality Assurance Framework
- **REQ-QA-001**: Implement automated quality scoring (target >80%)
- **REQ-QA-002**: Create evidence hallucination detection systems
- **REQ-QA-003**: Build evidence relevance validation algorithms
- **REQ-QA-004**: Implement evidence coverage optimization
- **REQ-QA-005**: Create evidence synthesis quality metrics
- **REQ-QA-006**: Sequential Synthesis Pipeline Quality Metrics - Validate query effectiveness, evidence diversity, and step-to-step coherence

### Performance & Scalability Audit
- **REQ-PA-001**: Comprehensive system-wide performance benchmarking
- **REQ-PA-002**: Scalability characterization from 10 to 2000+ documents
- **REQ-PA-003**: Resource requirement quantification across scales
- **REQ-PA-004**: Limitation documentation with honest assessment
- **REQ-PA-005**: Release readiness validation and SLA establishment
- **REQ-PA-006**: Sequential Synthesis Performance Validation - Benchmark 5-step pipeline performance and token budget compliance across document scales

### Framework Agnosticity Validation (NEW)
- **REQ-FA-001**: Zero Hardcoding Validation - Automated detection of experiment-specific assumptions in synthesis agents
- **REQ-FA-002**: Cross-Framework Compatibility Testing - Validate synthesis agent works with any CFF-compatible framework
- **REQ-FA-003**: Speaker-Agnostic Query Generation - Ensure no hardcoded speaker names or corpus-specific references
- **REQ-FA-004**: Framework Pollution Elimination Testing - Validate RAG queries return evidence, not framework definitions
- **REQ-FA-005**: Statistical-Driven Adaptation - Validate LLM adapts synthesis approach based on available statistical data

### LLM Model Selection & Optimization
- **REQ-LLM-001**: Document task-to-model mapping principles across 17+ agents
- **REQ-LLM-002**: Establish empirically validated model recommendations
- **REQ-LLM-003**: Create cost-performance optimization guidelines
- **REQ-LLM-004**: Build model selection decision framework
- **REQ-LLM-005**: Document provider-specific considerations and limitations
- **REQ-LLM-006**: Sequential Synthesis Model Optimization - Validate optimal model selection for each of the 5 synthesis steps

### Agent Architecture Documentation
- **REQ-AAD-001**: Document all 17+ agents with clear function descriptions
- **REQ-AAD-002**: Map agents to architectural principles they implement
- **REQ-AAD-003**: Document agent interaction patterns and orchestration flows
- **REQ-AAD-004**: Bridge architecture vision with concrete implementation
- **REQ-AAD-005**: Establish agent classification framework and extension patterns
- **REQ-AAD-006**: Sequential Synthesis Agent Documentation - Complete specification of v2.0 architecture, YAML prompts, and integration patterns

### THIN Architecture Compliance
- **REQ-TAC-001**: Eliminate all non-essential LLM output parsing
- **REQ-TAC-002**: Externalize all prompts to YAML files
- **REQ-TAC-003**: Deprecate obsolete and redundant agents
- **REQ-TAC-004**: Establish THIN compliance checklist for future agents
- **REQ-TAC-005**: Trust LLM intelligence instead of constraining it
- **REQ-TAC-006**: Sequential Synthesis THIN Validation - Validate v2.0 agent follows all THIN principles with minimal software coordination

### Narrative Excellence
- **REQ-NE-001**: Enhance synthesis structure and flow
- **REQ-NE-002**: Implement narrative quality with evidence rigor
- **REQ-NE-003**: Create academic writing style optimization
- **REQ-NE-004**: Build peer review readiness validation
- **REQ-NE-005**: Sequential Report Quality - Validate 5-step synthesis produces coherent, academically rigorous final reports

## Success Criteria
- [ ] Evidence standards match top academic journals
- [ ] Evidence diversity >3 sources per claim achieved
- [ ] Evidence strength validation >0.8 reliability
- [ ] Automated quality assurance framework operational
- [ ] Comprehensive performance audit completed with limitations documented
- [ ] Performance SLAs established for different user scenarios
- [ ] LLM model selection guide covering all agents with empirical validation
- [ ] Cost-performance optimization framework operational
- [ ] Complete agent architecture documented in system architecture document
- [ ] Architecture-implementation gap bridged through agent documentation
- [ ] All active agents THIN compliant with externalized YAML prompts
- [ ] Obsolete agents deprecated and agent ecosystem streamlined
- [ ] Peer review ready quality standards implemented
- [ ] Academic excellence validation across frameworks
- [ ] Release readiness assessment completed

### Sequential Synthesis Quality Criteria (NEW)
- [ ] **Evidence-First Compliance**: 100% of synthesis claims backed by statistical result + textual quote
- [ ] **Token Budget Discipline**: All 5 sequential steps operate under measurable token limits with automatic validation
- [ ] **No-LM-Math Enforcement**: Zero mathematical computations performed by LLM, only reasoning about pre-computed tables
- [ ] **Framework Fit Assessment**: Quantitative framework fit assessment (Gold/Silver/Bronze tier) in every final report
- [ ] **Framework Agnosticity**: Zero hardcoded assumptions validated across multiple framework types
- [ ] **RAG Precision**: >80% of evidence queries return relevant textual evidence (not framework definitions)
- [ ] **Sequential Coherence**: 5-step pipeline produces coherent, integrated final reports meeting academic standards

## Child Issues
- Issue #351: Academic Output Standards Implementation
- Issue #352: Quality Assurance & Scalability Validation
- Issue #353: Evidence Integration Testing & Validation  
- Issue #356: Narrative Quality Enhancement & Synthesis Structure
- Issue #358: Academic Standards & Peer Review Preparation
- Issue #368: Comprehensive Performance & Scalability Audit for Release Readiness
- Issue #369: LLM Model Selection & Task Assignment Guidelines Documentation
- Issue #370: Document Agent Architecture in System Architecture Document
- Issue #372: THIN Architecture Compliance Audit & Agent Cleanup - Complete

### New Child Issues for Sequential Synthesis Quality (TO BE CREATED)
- Issue #XXX: Sequential Synthesis Quality Standards Implementation
- Issue #XXX: Evidence-First Synthesis Validation Framework
- Issue #XXX: Token Budget Discipline Enforcement System
- Issue #XXX: Framework Agnosticity Validation Testing
- Issue #XXX: Framework Fit Assessment Quality Validation

## Dependencies
- **Sequential Synthesis Agent Architecture v2.0 (Epic #354)** - Primary dependency
- Evidence infrastructure foundation
- THIN synthesis pipeline
- Multi-model architecture and ModelRegistry
- Complete agent ecosystem (17+ agents)
- Clean data separation (Context vs Lookup)
- Statistical table contracts from MathToolkit
- Externalized YAML prompting framework

## Timeline
Estimated 4-5 weeks after Sequential Synthesis Architecture completion (reduced from 6-7 weeks due to integrated quality validation approach)

**Phase 1 (Week 1)**: Sequential synthesis quality standards implementation
**Phase 2 (Week 2-3)**: Framework agnosticity and THIN compliance validation  
**Phase 3 (Week 4)**: Performance audit and academic excellence validation
**Phase 4 (Week 5)**: Integration testing and release readiness assessment

## Validation
- Cross-framework evidence quality comparison
- Peer review standards implementation testing
- Academic excellence validation with narrative quality assessment
- System-wide performance audit with scalability characterization
- LLM model assignment validation through empirical testing
- Agent architecture documentation accuracy validation
- THIN compliance validation across all agents
- Architecture-implementation alignment verification
- Release readiness validation through comprehensive testing

### Sequential Synthesis Validation (NEW)
- **Evidence-First Synthesis Testing**: Validate every claim has statistical + textual backing
- **Token Budget Compliance Testing**: Validate all steps operate within defined limits
- **No-LM-Math Constraint Testing**: Automated detection of prohibited LLM calculations
- **Framework Agnosticity Testing**: Validate agent works across different frameworks without modification
- **Framework Fit Assessment Testing**: Validate appropriate tier selection and quality of fit analysis
- **Cross-Scale Performance Testing**: Validate quality maintenance from 10 to 2000+ documents
- **RAG Precision Testing**: Validate elimination of framework pollution in evidence retrieval


---

### Research Platform Scalability & Modern Architecture Validation
- **Issue**: #363
- **Labels**: enhancement
- **Assignees**: 
- **Created**: 2025-08-09
- **Updated**: 2025-08-11
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Research Platform Scalability & Modern Architecture Validation

**Full Description**:
Child issue for Epic #354: Modern RAG Synthesis Architecture

## Objective
Validate comprehensive RAG architecture at enterprise scale and demonstrate modern AI systems architecture patterns and scalability at unprecedented academic research scale.

## Requirements
- REQ-ES-001: Test with 100+ document corpus (medium scale)
- REQ-ES-002: Test with 500+ document corpus (large scale)  
- REQ-ES-003: Test with 2,000+ document corpus (enterprise scale - 40-200x academic practice)
- REQ-ES-004: Validate query performance <2 seconds at all scales
- REQ-ES-005: Measure synthesis quality maintenance across scales up to 2,000+ documents
- REQ-MA-001: Demonstrate modern AI systems architecture patterns at unprecedented scale
- REQ-MA-002: Validate comprehensive knowledge reasoning capabilities with thousands of documents
- REQ-MA-003: Prove academic-grade rigor with computational verification at enterprise scale

## Success Criteria
- Quality synthesis maintained at 2,000+ document scale (demonstrating 40-200x improvement over typical academic practice of 10-50 documents)
- Query performance <2 seconds across all scales including enterprise scale
- Memory usage optimized for production deployment with thousands of documents
- Architecture demonstrates modern AI research platform capabilities at unprecedented scale
- Documentation captures design philosophy and technical decisions for enterprise-scale processing
- Scalability benchmarks established for future development and competitive positioning

## Dependencies
- Issue #361: Comprehensive Knowledge RAG Implementation
- Issue #362: LLM-Powered Query Intelligence & Cross-Domain Reasoning
- Issue #366: Refactor ProductionThinSynthesisPipeline for Comprehensive RAG Integration
- Large-scale test corpus (2,000+ documents)
- Performance benchmarking infrastructure for enterprise-scale testing

## Validation
- Enterprise-scale corpus processing validation (2,000+ documents)
- Performance benchmarking across document scales up to thousands
- Architecture review and documentation for unprecedented scale capabilities
- Modern AI systems pattern demonstration at enterprise scale

---

### LLM-Powered Query Intelligence & Cross-Domain Reasoning
- **Issue**: #362
- **Labels**: enhancement
- **Assignees**: 
- **Created**: 2025-08-09
- **Updated**: 2025-08-11
- **Milestone**: Alpha Quality & Hygiene
- **Description**: LLM-Powered Query Intelligence & Cross-Domain Reasoning

**Full Description**:
Child issue for Epic #354

## Objective
Implement intelligent query generation and cross-domain reasoning capabilities for the comprehensive knowledge RAG system.

## Requirements
- REQ-MA-001: LLM-powered adaptive query generation
- REQ-MA-002: Intelligent query refinement based on result quality
- REQ-MA-003: Cross-domain reasoning capabilities
- REQ-MA-004: Evidence gap detection and targeted discovery
- REQ-MA-005: Multi-perspective investigation framework

## Success Criteria
- LLM generates optimized queries based on hypothesis + statistical context
- Query refinement loop improves results iteratively
- Cross-domain reasoning links statistics to evidence to framework
- Evidence gap detection identifies missing support for claims
- Multi-perspective investigation (validation, contradiction, explanation)

## Dependencies
- Issue #361: Comprehensive Knowledge RAG Implementation
- Investigative Synthesis Agent (already implemented)
- LLM Gateway (already implemented)

## Validation
- Hypothesis-driven evidence discovery testing
- Statistical anomaly investigation validation
- Cross-domain reasoning accuracy assessment

---

### Claude Synthesis Pipeline Failure - Cross-Model Compatibility Bug
- **Issue**: #360
- **Labels**: bug
- **Assignees**: 
- **Created**: 2025-08-08
- **Updated**: 2025-08-11
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Claude Synthesis Pipeline Failure - Cross-Model Compatibility Bug

**Full Description**:
# Issue #359: Claude Synthesis Pipeline Failure - Cross-Model Compatibility Bug

**Date**: August 8, 2025  
**Priority**: High  
**Status**: 🐛 Bug  
**Impact**: Prevents reliable execution across flagship model families  

## 🚨 **Problem Summary**

Claude 4 Sonnet synthesis pipeline fails completely while analysis phase works correctly. This creates a **cross-model compatibility issue** that prevents reliable execution across flagship model families (Anthropic, OpenAI, Google).

## 📊 **Evidence from Recent Test**

**Test Run**: `20250808T030048Z` with `anthropic/claude-3-5-sonnet-20241022`

### ✅ **What Worked**
- **Analysis Phase**: Complete success (4/8 documents, $0.6318 cost)
- **Rate Limit Handling**: Fixed and working (exponential backoff implemented)
- **Planning Stages**: Raw data and derived metrics planning completed
- **Cost Tracking**: Accurate cost breakdown shows Claude usage

### ❌ **What Failed**
- **Mathematical Execution**: No statistical calculations performed
- **Evidence Curation**: No evidence integration costs recorded
- **Statistical Analysis**: Missing correlation matrices, framework validation
- **Derived Metrics**: No Civic Character Index, Virtue Index calculations
- **Report Quality**: Minimal template-based report with no statistical grounding

## 🔍 **Root Cause Analysis**

### **1. Synthesis Pipeline Incompatibility**
The THIN synthesis pipeline appears to have **model-specific compatibility issues**:
- **Gemini Pro**: Works reliably with mathematical execution
- **Claude Sonnet**: Planning succeeds, mathematical execution fails
- **Unknown**: Whether this affects other model families (OpenAI, etc.)

### **2. Mathematical Execution Failure**
Evidence suggests the **MathToolkit** cannot process Claude's analysis plans:
- Planning stages complete successfully
- Mathematical execution stage fails silently
- No error propagation to report generation
- Fallback to basic template report

### **3. Evidence Curation Failure**
The evidence curation pipeline fails with Claude:
- No evidence integration costs recorded
- No RAG-enhanced synthesis
- No dynamic evidence queries
- Basic evidence format only

## 🎯 **Impact Assessment**

### **High Priority Issues**
1. **Cross-Model Reliability**: Cannot guarantee synthesis works across model families
2. **Research Continuity**: Breaks ability to compare model performance
3. **Production Risk**: Unreliable synthesis with flagship models
4. **Cost Inefficiency**: Analysis costs incurred without synthesis results

### **Affected Workflows**
- **Model Comparison Studies**: Cannot reliably test Claude vs Gemini
- **Production Runs**: Risk of failed synthesis with premium models
- **Research Validation**: Cannot verify cross-model consistency
- **Cost Optimization**: Cannot test cost-quality trade-offs

## 🔧 **Technical Investigation Needed**

### **1. MathToolkit Compatibility**
- Investigate why MathToolkit fails with Claude's analysis plans
- Check for model-specific prompt formatting issues
- Verify mathematical execution error handling
- Test with other model families (OpenAI, etc.)

### **2. Synthesis Pipeline Debugging**
- Add comprehensive error logging to synthesis stages
- Implement fallback mechanisms for failed mathematical execution
- Add model-specific compatibility checks
- Create synthesis pipeline health monitoring

### **3. Evidence Curation Investigation**
- Debug evidence curation pipeline with Claude
- Check txtai curator compatibility
- Verify evidence integration error handling
- Test RAG-enhanced synthesis across models

## 📋 **Success Criteria**

### **Immediate (This Sprint)**
- [ ] **Reproduce the issue** with systematic testing
- [ ] **Identify root cause** in mathematical execution
- [ ] **Add error logging** to synthesis pipeline
- [ ] **Create fallback mechanisms** for failed synthesis

### **Short Term (Next Sprint)**
- [ ] **Fix Claude compatibility** with mathematical execution
- [ ] **Test other model families** (OpenAI, etc.)
- [ ] **Implement model-specific optimizations**
- [ ] **Add synthesis pipeline health checks**

### **Long Term (Next Release)**
- [ ] **Cross-model synthesis validation** framework
- [ ] **Model family compatibility matrix**
- [ ] **Automated synthesis pipeline testing**
- [ ] **Production-ready cross-model reliability**

## 🧪 **Reproduction Steps**

1. **Run experiment with Claude**:
   ```bash
   python3 -m discernus.cli run projects/1a_caf_civic_character \
     --analysis-model anthropic/claude-3-5-sonnet-20241022 \
     --synthesis-model anthropic/claude-3-5-sonnet-20241022 \
     --skip-validation
   ```

2. **Check synthesis results**:
   - Verify mathematical calculations are missing
   - Confirm evidence curation failed
   - Validate report quality is minimal

3. **Compare with Gemini Pro**:
   - Run same experiment with `vertex_ai/gemini-2.5-pro`
   - Verify mathematical calculations present
   - Confirm evidence curation working

## 📊 **Expected vs Actual Results**

### **Expected (Gemini Pro)**
- ✅ Statistical correlations and framework validation
- ✅ Evidence integration with quotes and confidence
- ✅ Derived metrics (Civic Character Index, etc.)
- ✅ Comprehensive academic report

### **Actual (Claude Sonnet)**
- ❌ No statistical calculations
- ❌ Basic evidence format only
- ❌ Missing derived metrics
- ❌ Template-based minimal report

## 🔗 **Related Issues**

- **Epic #280**: Three-Track Evidence Architecture (quality standards)
- **Epic #354**: Evidence Quality Enhancement (academic rigor)
- **Issue #208**: Framework compatibility validation
- **Issue #297**: Provenance organization

## 💰 **Cost Impact**

**Failed Claude Run**: $0.7633 USD for incomplete synthesis
- Analysis: $0.6318 (working)
- Synthesis: $0.1315 (failed - no mathematical results)

**Successful Gemini Run**: $0.8965 USD for complete synthesis
- Analysis: $0.7862 (working)
- Synthesis: $0.1103 (working - full mathematical results)

**Cost Inefficiency**: 85% of Claude synthesis cost wasted on failed execution

## 🎯 **Next Steps**

1. **Immediate**: Create reproduction test case
2. **This Week**: Debug mathematical execution with Claude
3. **Next Week**: Test other model families for similar issues
4. **Next Sprint**: Implement cross-model compatibility framework

---

**Labels**: `bug`, `high-priority`, `synthesis-pipeline`, `cross-model-compatibility`, `mathematical-execution`  
**Milestone**: Alpha Feature Complete  
**Epic**: Epic #354 (Evidence Quality Enhancement)


---

### Academic Standards & Peer Review Preparation
- **Issue**: #358
- **Labels**: enhancement
- **Assignees**: 
- **Created**: 2025-08-08
- **Updated**: 2025-08-11
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Academic Standards & Peer Review Preparation

**Full Description**:
Child issue for Epic #365: Academic Quality & Standards Implementation

Child issue for Epic #354

## Objective
Implement peer review standards and academic excellence requirements for evidence integration with narrative quality.

## Requirements
- REQ-PR-001: Implement evidence citation standards matching top journals
- REQ-PR-002: Create evidence provenance transparency requirements
- REQ-PR-003: Build evidence strength validation protocols
- REQ-PR-004: Implement evidence diversity requirements
- REQ-PR-005: Create evidence synthesis quality benchmarks
- REQ-QA-001: Implement automated quality scoring (target >80%)
- REQ-QA-002: Create evidence hallucination detection systems
- REQ-QA-003: Build evidence relevance validation algorithms
- REQ-QA-004: Implement evidence coverage optimization
- REQ-QA-005: Create evidence synthesis quality metrics

## Success Criteria
- Evidence standards match top academic journals
- Evidence diversity >3 sources per claim
- Evidence strength validation >0.8
- Peer review ready quality standards
- Automated quality assurance framework
- Narrative excellence with evidence rigor

## Dependencies
- Epic #280 completion (evidence infrastructure foundation)
- Issue #355 completion (quality measurement implementation)
- Issue #356 completion (narrative quality enhancement)

## Validation
- Cross-framework evidence quality comparison
- Peer review standards implementation
- Academic excellence validation with narrative quality

---

### Narrative Quality Enhancement & Synthesis Structure
- **Issue**: #356
- **Labels**: enhancement
- **Assignees**: 
- **Created**: 2025-08-08
- **Updated**: 2025-08-11
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Narrative Quality Enhancement & Synthesis Structure

**Full Description**:
Child issue for Epic #365: Academic Quality & Standards Implementation

Child issue for Epic #354

## Objective
Implement narrative quality enhancement and synthesis structure optimization to match flagship chatbot standards while maintaining evidence rigor.

## Requirements
- REQ-NQ-001: Implement narrative coherence algorithms for smooth transitions
- REQ-NQ-002: Create framework context integration with theoretical foundations
- REQ-NQ-003: Build executive summary enhancement with comprehensive research context
- REQ-NQ-004: Develop qualitative-quantitative balance optimization
- REQ-NQ-005: Implement academic prose quality standards
- REQ-SS-001: Create logical flow optimization between sections
- REQ-SS-002: Implement hypothesis testing narrative integration
- REQ-SS-003: Build statistical-qualitative synthesis balance
- REQ-SS-004: Develop framework explanation integration
- REQ-SS-005: Create conclusion synthesis quality standards

## Success Criteria
- Narrative coherence score >0.8
- Framework context integration >90%
- Executive summary quality matches flagship chatbot standards
- Maintain evidence rigor while enhancing narrative quality

## Dependencies
- Epic #280 completion (evidence infrastructure foundation)
- Issue #355 completion (quality measurement implementation)

## Validation
- CAF experiment re-analysis with narrative enhancement
- Comparison with flagship chatbot narrative quality
- Cross-framework narrative coherence testing

---

### Evidence Integration Testing & Validation
- **Issue**: #353
- **Labels**: enhancement
- **Assignees**: 
- **Created**: 2025-08-07
- **Updated**: 2025-08-11
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Evidence Integration Testing & Validation

**Full Description**:
Child issue for Epic #365: Academic Quality & Standards Implementation

# Evidence Integration Testing & Validation

**Parent Epic**: #280 Three-Track Evidence Architecture  
**Milestone**: Alpha Feature Complete  
**Dependencies**: Core evidence infrastructure implementation (Epic #280 Milestones 1.1-1.3)

## 🎯 OBJECTIVE

Implement comprehensive testing framework for evidence integration across multiple experiment types, frameworks, and corpus sizes to validate architectural durability and academic integrity.

## 📋 REQUIREMENTS

### **End-to-End Integration Testing**
- **REQ-ET-001**: Automated testing pipeline for complete evidence flow (analysis → indexing → retrieval → synthesis)
- **REQ-ET-002**: Cross-framework evidence reuse validation (CAF, CHF, ECF compatibility)
- **REQ-ET-003**: Multi-corpus evidence integration testing (different document types and sizes)
- **REQ-ET-004**: Regression testing to prevent evidence architecture degradation

### **Evidence Quality Validation Framework**
- **REQ-EQ-001**: Automated evidence-claim alignment verification
- **REQ-EQ-002**: Quote accuracy validation against source documents
- **REQ-EQ-003**: Provenance chain integrity testing (end-to-end traceability)
- **REQ-EQ-004**: Confidence score calibration and validation
- **REQ-EQ-005**: Evidence diversity metrics (dimension coverage, document representation)

### **Academic Integrity Testing Suite**
- **REQ-AI-001**: Evidence hallucination detection and prevention testing
- **REQ-AI-002**: Attribution accuracy validation (proper quote sourcing)
- **REQ-AI-003**: Reproducibility verification (identical results from same inputs)
- **REQ-AI-004**: Peer review simulation (external validation of evidence usage)

### **Performance Integration Testing**
- **REQ-PI-001**: Load testing with progressive corpus sizes (8 → 50 → 200 → 500 docs)
- **REQ-PI-002**: Concurrent experiment testing (multiple evidence pools simultaneously)
- **REQ-PI-003**: Memory pressure testing (evidence handling under resource constraints)
- **REQ-PI-004**: Query performance profiling and optimization validation

## ✅ SUCCESS CRITERIA

1. **Integration Coverage**: 100% test coverage for evidence flow pipeline components
2. **Quality Validation**: All test experiments achieve >80% evidence integration quality score
3. **Academic Standards**: Zero evidence hallucination incidents across all test scenarios
4. **Framework Portability**: Evidence architecture works identically across CAF, CHF, ECF frameworks
5. **Scalability Confirmation**: Performance benchmarks met across all corpus size test scenarios

## 🧪 VALIDATION TEST MATRIX

### **Framework Compatibility Tests**
| Framework | Corpus Size | Expected Evidence Quality | Status |
|-----------|-------------|---------------------------|---------|
| CAF v7.3 | 8 docs | >85% | ⏳ Pending |
| CHF v7.3 | 12 docs | >85% | ⏳ Pending |
| ECF v7.3 | 15 docs | >85% | ⏳ Pending |
| CAF v7.3 | 50 docs | >80% | ⏳ Pending |

### **Scalability Stress Tests**
| Test Scenario | Corpus Size | Max Processing Time | Memory Limit | Status |
|---------------|-------------|--------------------|--------------|---------| 
| Small Scale | 8-15 docs | <5 minutes | <2GB | ⏳ Pending |
| Medium Scale | 50-75 docs | <15 minutes | <8GB | ⏳ Pending |
| Large Scale | 200-300 docs | <30 minutes | <16GB | ⏳ Pending |
| Enterprise Scale | 500+ docs | <60 minutes | <32GB | ⏳ Pending |

### **Evidence Quality Benchmarks**
- **Quote Accuracy**: 100% exact match with source documents
- **Provenance Integrity**: 100% traceable claim-to-source mapping
- **Confidence Calibration**: Evidence confidence scores within ±0.1 of analysis agent scores
- **Coverage Diversity**: >80% of available dimensions represented in synthesis
- **Claim Support**: >90% of interpretive claims backed by relevant evidence

## 🔧 TESTING INFRASTRUCTURE

### **Automated Test Pipeline**
1. **Evidence Pool Generation**: Automated creation of test evidence pools with known characteristics
2. **Synthetic Claim Injection**: Generate interpretive claims with expected evidence mappings
3. **Quality Score Calculation**: Automated measurement of evidence integration metrics
4. **Regression Detection**: Baseline comparison to detect architecture degradation
5. **Performance Profiling**: Automated benchmarking across test scenarios

### **Validation Reporting**
- **Test Results Dashboard**: Real-time test status and quality metrics
- **Evidence Usage Analytics**: Detailed breakdown of evidence utilization patterns
- **Performance Trend Analysis**: Long-term performance tracking and optimization insights
- **Academic Integrity Reports**: Comprehensive validation of evidence handling standards

## 🔗 IMPLEMENTATION DEPENDENCIES

- **Prerequisite**: Complete evidence integration infrastructure (Epic #280 all milestones)
- **Prerequisite**: Academic output standards implementation
- **Prerequisite**: Quality assurance framework implementation
- **Input**: Production-ready evidence architecture
- **Output**: Validated, production-certified evidence integration system

## 📋 TEST EXECUTION PLAN

### **Phase 1: Foundation Testing** *(Week 1)*
- [ ] Basic evidence flow integration tests
- [ ] Single-framework validation (CAF v7.3)
- [ ] Small-scale performance benchmarking

### **Phase 2: Cross-Framework Validation** *(Week 2)*
- [ ] CHF and ECF framework compatibility testing
- [ ] Evidence reuse across frameworks validation
- [ ] Medium-scale performance testing

### **Phase 3: Production Certification** *(Week 3)*
- [ ] Large-scale stress testing
- [ ] Academic integrity comprehensive validation
- [ ] Final performance optimization and certification

---

### Quality Assurance & Scalability Validation
- **Issue**: #352
- **Labels**: enhancement
- **Assignees**: 
- **Created**: 2025-08-07
- **Updated**: 2025-08-11
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Quality Assurance & Scalability Validation

**Full Description**:
Child issue for Epic #365: Academic Quality & Standards Implementation

# Quality Assurance & Scalability Validation

**Parent Epic**: #280 Three-Track Evidence Architecture  
**Milestone**: Alpha Feature Complete  
**Dependencies**: Academic Output Standards Implementation completion

## 🎯 OBJECTIVE

Implement comprehensive quality assurance framework and validate scalability requirements for evidence integration infrastructure across small to large-scale experiments.

## 📋 REQUIREMENTS

### **Quality Assurance Framework**
- **REQ-QA-001**: Implement evidence utilization rate tracking (pieces used / pieces available)
- **REQ-QA-002**: Create interpretive claim coverage metrics (claims backed / total claims)
- **REQ-QA-003**: Monitor evidence query efficiency (relevant results / total queries)
- **REQ-QA-004**: Validate evidence-claim alignment through automated confidence scoring
- **REQ-QA-005**: Implement evidence hallucination detection (reject non-retrieved evidence)
- **REQ-QA-006**: Create academic integrity validation (quote accuracy, source attribution)

### **Scalability Validation Requirements**
- **REQ-SC-001**: Performance testing: 2000+ documents without synthesis quality degradation
- **REQ-SC-002**: Speed benchmarks: Evidence indexing <5 minutes for large corpora
- **REQ-SC-003**: Query performance: Evidence retrieval <2 seconds per query
- **REQ-SC-004**: Synthesis efficiency: Report generation <10 minutes regardless of evidence pool size
- **REQ-SC-005**: Memory management: Efficient evidence loading for massive datasets
- **REQ-SC-006**: Concurrent processing: Support parallel evidence queries (future-proofing)

### **Performance Monitoring Dashboard**
- **REQ-PM-001**: Real-time evidence integration quality metrics
- **REQ-PM-002**: Evidence pool statistics and utilization analytics
- **REQ-PM-003**: Query performance monitoring and optimization alerts
- **REQ-PM-004**: Academic integrity compliance tracking

## ✅ SUCCESS CRITERIA

1. **Quality Metrics**: Evidence integration quality score >80% (coverage + accuracy + relevance)
2. **Scalability Proof**: System handles 100+ document corpus without quality degradation
3. **Performance Standards**: All speed benchmarks met consistently across test scenarios
4. **Academic Integrity**: Zero evidence hallucination incidents in validation testing
5. **Monitoring Infrastructure**: Complete quality dashboard operational with real-time metrics

## 🧪 VALIDATION EXPERIMENTS

### **Scalability Test Suite**
1. **Baseline Test**: 8-document CAF experiment (current performance baseline)
2. **Medium Scale**: 50-document corpus expansion (2-5x scale validation)
3. **Large Scale**: 200-document stress test (25x scale validation)
4. **Enterprise Scale**: 500+ document performance testing (future-proofing)

### **Quality Assurance Test Suite**
1. **Evidence Accuracy**: Automated quote verification against source documents
2. **Claim Coverage**: Ensure all interpretive claims have evidence backing
3. **Provenance Integrity**: Validate complete audit trails for reproducibility
4. **Multi-Framework**: Test evidence reuse across different analytical frameworks

## 🔗 IMPLEMENTATION DEPENDENCIES

- **Prerequisite**: Core evidence integration infrastructure (Epic #280 Milestones 1.1-1.2)
- **Prerequisite**: Academic output standards (footnotes, provenance) implementation
- **Input**: Functioning evidence-infused synthesis pipeline
- **Output**: Production-ready evidence architecture with quality guarantees

## 📊 PERFORMANCE TARGETS

| Metric | 8 Docs | 50 Docs | 200 Docs | 500+ Docs |
|--------|--------|---------|-----------|-----------|
| Evidence Integration Quality | >85% | >80% | >80% | >75% |
| Indexing Time | <30s | <2min | <5min | <10min |
| Query Response | <1s | <1.5s | <2s | <2.5s |
| Synthesis Time | <2min | <5min | <10min | <15min |
| Memory Usage | <1GB | <4GB | <8GB | <16GB |

---

### Academic Output Standards Implementation
- **Issue**: #351
- **Labels**: enhancement
- **Assignees**: 
- **Created**: 2025-08-07
- **Updated**: 2025-08-11
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Academic Output Standards Implementation

**Full Description**:
Child issue for Epic #365: Academic Quality & Standards Implementation

# Academic Output Standards Implementation

**Parent Epic**: #280 Three-Track Evidence Architecture  
**Milestone**: Alpha Feature Complete  
**Dependencies**: Milestone 1.1 and 1.2 completion from Epic #280

## 🎯 OBJECTIVE

Implement academic-grade output formatting standards for evidence-infused reports, including footnote systems, provenance transparency, and multi-audience integration.

## 📋 REQUIREMENTS

### **Footnote System Implementation**
- **REQ-OF-001**: Generate numbered footnotes for all evidence citations [1], [2], etc.
- **REQ-OF-002**: Link footnotes to full provenance chain in transparency section
- **REQ-OF-003**: Include confidence scores and metadata in footnote details
- **REQ-OF-004**: Support multiple evidence pieces per claim with distinct footnotes

### **Provenance Transparency Framework**
- **REQ-OF-005**: Create "Evidence Provenance" section with complete audit trail
- **REQ-OF-006**: Format provenance chains: `[1] steve_king_2017.txt → manipulation dimension → confidence=0.9 → "court wants to manufacture"`
- **REQ-OF-007**: Enable click-through traceability from any claim to source document
- **REQ-OF-008**: Include evidence extraction method and context type in metadata

### **Multi-Audience Integration Standards**
- **REQ-OF-009**: Scanner section: Evidence-backed key findings with inline footnotes
- **REQ-OF-010**: Collaborator section: Detailed analysis with integrated evidence quotes
- **REQ-OF-011**: Transparency section: Complete provenance chains and methodology
- **REQ-OF-012**: Consistent footnote numbering across all report sections

## ✅ SUCCESS CRITERIA

1. **Footnote Integration**: All interpretive claims include numbered footnote citations
2. **Provenance Completeness**: Every footnote traces back to source document with full metadata
3. **Academic Standards**: Output format meets peer-review publication standards
4. **Multi-Audience Coherence**: Evidence integration works across scanner/collaborator/transparency sections
5. **Reproducibility**: Independent researchers can verify all claims through provided provenance

## 🧪 VALIDATION

**Test Case**: 8-document CAF experiment should produce report with:
- 15+ footnoted evidence citations
- Complete provenance section with audit trails
- Academic-quality formatting across all sections
- Verifiable claim-to-source mapping

## 🔗 IMPLEMENTATION DEPENDENCIES

- **Prerequisite**: Evidence retrieval infrastructure (Epic #280 Milestone 1.1)
- **Prerequisite**: Basic evidence integration (Epic #280 Milestone 1.2)
- **Input**: Retrieved evidence with full provenance metadata
- **Output**: Academic-formatted report with footnotes and transparency section

---

### Enhance Methodology Transparency with Framework Operationalization
- **Issue**: #302
- **Labels**: enhancement
- **Assignees**: 
- **Created**: 2025-08-03
- **Updated**: 2025-08-05
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Enhance Methodology Transparency with Framework Operationalization

**Full Description**:
## Problem

Current reports fail to explain HOW abstract framework concepts are operationalized into measurable indicators. Academic readers cannot understand what specific linguistic features or thematic markers are being measured, making analysis difficult to evaluate or trust.

## Current State Issues

### Opaque Operationalization
- Framework Overview describes WHAT dimensions measure (e.g., 'appeals to direct popular sovereignty')
- Missing explanation of HOW these concepts become measurable instructions for analysis agent
- No detail on process from raw text to numerical scores
- Black box analysis that undermines academic credibility

### Missing Methodology Detail
- Methodology Notes section is appendix-style, not proper methods section
- No explanation of Analysis Agent scoring process
- Raw Analysis Log contents and structure unexplained
- Insufficient detail for replication or validation

## Proposed Solution

### Concise Methodology Section (1-2 Paragraphs)
**Framework Operationalization Example:**
'To measure the Populism-Pluralism Axis, the analysis agent was instructed to identify and score textual evidence related to anti-elite sentiment, direct appeals to the people over institutions, and critiques of mediated democracy. High scores were assigned to direct claims of representing a singular popular will (e.g., giving power back to you, the people), while low scores were assigned to affirmations of constitutional processes and institutional norms (e.g., the enduring strength of our Constitution).'

### Analysis Process Transparency
- Clear explanation of how Analysis Agent moves from raw text to scores
- Description of Raw Analysis Log structure and contents
- Scoring rubric and decision criteria made explicit
- Quality assurance and validation procedures documented

### Replication Information
- Sufficient detail for independent replication
- Framework-to-instruction translation process documented
- Scoring criteria and thresholds specified
- Edge case handling and fallback procedures explained

## Implementation Requirements

### Content Development
- Create framework operationalization templates for major framework types
- Document analysis agent scoring processes and criteria
- Develop replication-ready methodology descriptions
- Build quality assurance documentation standards

### Integration Points
- Methodology section becomes standard part of all final reports
- Operationalization details pulled from framework specifications
- Analysis process documentation auto-generated from agent logs
- Replication packages include complete methodology transparency

## Acceptance Criteria

- [ ] Every final report includes concise methodology section (1-2 paragraphs)
- [ ] Framework operationalization explicitly explained for each dimension
- [ ] Analysis process from raw text to scores clearly documented
- [ ] Sufficient detail provided for independent replication
- [ ] Academic readers can understand and evaluate methodology without expert knowledge
- [ ] Methodology transparency increases external reviewer confidence

## Benefits

- **Academic Credibility**: Methodology transparency enables proper evaluation
- **Replication Support**: Sufficient detail for independent validation
- **External Review**: Reviewers can assess methodological soundness
- **Quality Assurance**: Clear criteria enable better quality control

**Dependencies**: Integrates with Issue #300 (Report Structure) as key component of Collaborator Deep Dive section

---

### Implement Defensive Prompting to Constrain LLM Over-Generalization
- **Issue**: #301
- **Labels**: enhancement
- **Assignees**: 
- **Created**: 2025-08-03
- **Updated**: 2025-08-11
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Implement Defensive Prompting to Constrain LLM Over-Generalization

**Full Description**:
**Moved to Epic #319: Alpha Polish and Usability**

### Overview
This task is to implement a system of defensive prompting to make our analysis more robust against LLM over-generalization and hallucination.

### Acceptance Criteria
1. A new  object is added to the .
2. This object allows authors to define 'constraints' or 'negative instructions' (e.g., 'DO NOT score based on speaker identity').
3. The  is updated to parse these constraints and append them to its final prompt to the LLM.
4. The  methodology section includes a summary of the defensive prompts used in the analysis for transparency.

---

### EPIC: Research Integrity & Provenance Architecture Enhancement
- **Issue**: #292
- **Labels**: epic
- **Assignees**: 
- **Created**: 2025-08-03
- **Updated**: 2025-08-05
- **Milestone**: Alpha Quality & Hygiene
- **Description**: EPIC: Research Integrity & Provenance Architecture Enhancement

**Full Description**:
## 🎯 Strategic Context

**Problem**: Critical provenance chain breaks discovered through external reviewer feedback. Statistical results artifacts are created but not connected to final outputs due to field name mismatches and missing metadata.

**Discovery**: External reviewer found empty statistical_results.csv file, leading to concerns about fabricated results. Investigation revealed excellent cryptographic infrastructure exists but has connection gaps and usability issues.

**Solution**: Enhance existing provenance architecture by fixing connection points, adding validation, and improving human comprehension without sacrificing integrity.

## 🔍 Root Cause Analysis

### ✅ **EXCELLENT Infrastructure Already Exists**
- Cryptographic artifact storage with SHA-256 hashes
- Tamper-evident provenance stamps (ProvenanceStamp system)  
- Complete audit logging and timeline tracking
- Statistical calculations performed and stored as artifacts
- Evidence curation working and stored as artifacts

### ❌ **Critical Issues Identified**
1. **Field Name Mismatch**: Pipeline returns statistical_results_hash, orchestrator looks for statistical_results_artifact_hash
2. **Missing Artifact Metadata**: Statistical results stored with empty metadata, making them unidentifiable  
3. **Silent Failure Mode**: CSV export creates empty files instead of failing when data is missing
4. **No Hash Validation**: No verification that expected artifacts exist before proceeding
5. **Usability Problems**: Artifacts scattered across shared cache and run directories, hash-named files are human-incomprehensible
6. **Provenance Complexity**: Current system optimized for performance over human transparency

## 🏗️ Architecture Enhancement Strategy

**Threat Model**: Defend against unintended errors and prepare researchers for peer review and replication challenges. NOT defending against skilled, motivated adversarial users attempting to corrupt academic research.

**Principle**: Optimize for academic transparency first, performance second, theoretical security threats last.

## 📋 Sprint Organization

### Sprint 6: Provenance Connection Repair
- **#293**: Fix Statistical Results Artifact Field Name Mismatch
- **#294**: Add Comprehensive Artifact Metadata to Synthesis Pipeline  
- **#295**: Remove Silent Failure Mode from CSV Export Agent
- **#296**: Implement Artifact Hash Validation in Orchestrator

### Sprint 7: Human-Comprehensible Provenance Architecture
- **#297**: Implement Human-Readable Artifact Names with Short Hashes
- **#298**: Create Provenance-First File Organization (run-specific artifact directories)
- **#299**: Build Automated Provenance Visualization Tools
- **#300**: Add Human-Friendly Artifact Browser Interface

### Sprint 8: Academic Validation Ready
- **#301**: Complete Peer Review Packages with Clear Artifact Maps
- **#302**: Build External Validation Tools That Just Work
- **#303**: Add Academic Presentation Tools for Provenance Transparency
- **#304**: Create Automated Provenance Health Checks

## 🎯 Success Criteria

**Sprint 6**: Zero empty CSV files, all statistical results properly exported, immediate connection fixes
**Sprint 7**: Human-comprehensible artifact organization, any researcher can navigate provenance without detective work
**Sprint 8**: Platform meets highest academic standards, external reviewers can validate findings in <2 minutes

## 🔗 Integration with Existing Work

**Synergistic with current milestones:**
- **Epic #280 (Evidence Architecture)**: Enhances evidence artifact connection and usability
- **Epic #285 (Framework v7.1)**: Provides validation for new framework features
- **Alpha v1.3 Goals**: Delivers academic foundation and release readiness
- **Future Security Review**: Establishes appropriate threat model and security scenarios for provenance

## 🛡️ Security Review Integration

**Provenance Security Scenarios for Later Milestone:**
1. **Unintended Error Detection**: Verify system catches and reports accidental data corruption
2. **Academic Peer Review Preparation**: Validate that provenance trails withstand rigorous external scrutiny
3. **Replication Battle Readiness**: Ensure researchers can defend methodology with complete audit trails
4. **Right-Sized Security**: Confirm security measures match actual threat model (not theoretical nation-state adversaries)

## 🔄 Architectural Evolution Path

**Current State**: Performance-optimized, cryptographically secure, human-incomprehensible
**Target State**: Transparency-first, appropriately secure, performance-maintained through intelligent design

**Key Changes:**
- Provenance-first file organization with performance layer
- Human-readable artifact names with hash verification
- Clear separation: Git for source/results, hashes for computational artifacts
- Run-specific directories with complete provenance visibility

## 🎯 Expected Outcomes

**Immediate (Sprint 6)**: No more empty CSV files, all artifacts properly connected, immediate crisis resolved
**Medium-term (Sprint 7)**: Researchers can navigate provenance intuitively, no more cave diving through hash directories
**Long-term (Sprint 8)**: Platform sets new standard for computational social science transparency and usability

**Risk Mitigation**: Building on excellent existing infrastructure, enhancing rather than replacing, maintaining performance through intelligent caching.

---

### Default Ensemble Validation: Empirical Model Selection Strategy
- **Issue**: #291
- **Labels**: enhancement, performance
- **Assignees**: 
- **Created**: 2025-08-03
- **Updated**: 2025-08-11
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Default Ensemble Validation: Empirical Model Selection Strategy

**Full Description**:
**Moved to Epic #319: Alpha Polish and Usability**

### Overview
This task is to implement a default ensemble validation system to improve the methodological rigor and self-consistency of the analysis.

### Acceptance Criteria
1. The  schema is updated to include an  field (e.g., ).
2. If  is > 1, the  runs the  N times for each document.
3. A new  component is created that takes the N raw analysis logs.
4. The aggregator calculates median scores for all dimensions and a set of consensus metrics (e.g., variance, std dev).
5. The final report includes the aggregated scores and a summary of the ensemble consensus, flagging dimensions with low agreement.

---

### Retrospective: THIN Evidence Pre-Extraction Architecture Implementation
- **Issue**: #271
- **Labels**: enhancement, architecture, retrospective
- **Assignees**: 
- **Created**: 2025-08-01
- **Updated**: 2025-08-11
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Retrospective: THIN Evidence Pre-Extraction Architecture Implementation

**Problem Statement**: The original evidence curation approach had critical scaling issues:
- Registry Scanning: Evidence curator scanned artifact registry for raw_analysis_response_v6 artifacts (O(n) operation)
- Partial Evidence Loss: Only processed original_raw_artifacts[0], losing evidence from remaining documents
- Architectural Violation: Evidence curator performing complex artifact discovery violated THIN principles

At 1000 documents, this would create:
- 1000+ registry scans per synthesis
- 999 documents with lost evidence
- Exponential performance degradation

---

### Enhancement: Add LLM Response Caching to Synthesis Pipeline
- **Issue**: #251
- **Labels**: enhancement, synthesis, performance
- **Assignees**: 
- **Created**: 2025-07-31
- **Updated**: 2025-08-11
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Enhancement: Add LLM Response Caching to Synthesis Pipeline

**Full Description**:
## Background

The synthesis pipeline makes multiple expensive LLM calls (RawDataAnalysisPlanner, DerivedMetricsAnalysisPlanner, EvidenceCurator, ResultsInterpreter) that could benefit from individual response caching.

## Current Caching Status

✅ **Working Well:**
- Analysis stage: Fully cached (60+ second operations)
- Framework/corpus: Content-addressable caching
- Final artifacts: Analysis plans, statistical results, curated evidence cached
- Cross-run caching: Shared cache enables --synthesis-only mode

⚠️ **Optimization Opportunities:**
- Individual LLM responses not cached (only final stage outputs)
- Mathematical computations re-run each time
- Evidence curation LLM calls (60+ seconds) not cached separately

## Proposed Enhancements

### 1. LLM Response Caching
Cache individual LLM responses by (model + prompt_hash) to avoid re-running identical synthesis steps.

### 2. Mathematical Computation Caching  
Cache statistical calculations by (data_hash + analysis_plan_hash) since these are deterministic.

### 3. Evidence Curation LLM Caching
Cache the expensive evidence curation LLM response separately from parsed results.

### 4. Incremental Synthesis Resume
Allow resuming synthesis from any stage, not just analysis → synthesis.

## Implementation Considerations

- **Cache invalidation**: LLM responses depend on statistical results and framework changes
- **Development vs Production**: Different caching strategies may be needed
- **Storage overhead**: Balance cache hits vs disk usage
- **Debugging support**: Ability to bypass caches during development

## Benefits

- **Development velocity**: Faster iteration during synthesis debugging
- **Production efficiency**: Reduced API costs for repeated operations  
- **Resource optimization**: Better utilization of expensive LLM calls

## Priority

**Medium** - Current analysis caching handles the most expensive operations. This is an optimization for synthesis stage performance.

---

**Related Issues:**
- #250 - Parameter audit (some caching parameters may need review)
- Analysis caching is working well, this focuses on synthesis stage optimization

## Sprint Organization

**Sprint**: 5 (Post-Gasket Performance & UX)  
**Dependencies**: Blocked by Epic #259 (Gasket Architecture Implementation)  
**Rationale**: LLM response caching optimization should be implemented after gasket architecture is stable to avoid optimizing the wrong patterns.

---

### Create Unified Results Dashboard for Researcher-Centric Information Architecture
- **Issue**: #249
- **Labels**: enhancement, developer-experience
- **Assignees**: 
- **Created**: 2025-07-31
- **Updated**: 2025-08-11
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Create Unified Results Dashboard for Researcher-Centric Information Architecture

**Full Description**:
**Moved to Epic #319: Alpha Polish and Usability**

### Overview
This task is to design and implement a unified, human-readable results dashboard. The current output is a set of CSVs and a markdown report. A single, clear dashboard will significantly improve the user experience.

### Acceptance Criteria
1. A new  agent is created.
2. This agent ingests all the final artifacts from a run (, , ).
3. It generates a single, standalone HTML file () in the run's  directory.
4. The dashboard presents key findings, summary statistics, and visualizations in a clear, interactive format.

---

### [BUG] Fix Zero Dollar Cost and Time Estimates
- **Issue**: #209
- **Labels**: bug
- **Assignees**: 
- **Created**: 2025-07-29
- **Updated**: 2025-08-11
- **Milestone**: Alpha Quality & Hygiene
- **Description**: [BUG] Fix Zero Dollar Cost and Time Estimates

**Full Description**:
### Bug Description

The cli is showing incorrect cost and time estimates:

🚀 Starting THIN v2.0 experiment: 20250729T193535Z
🗄️ Stored artifact: b75db5fed32d... (6159 bytes)
📄 Loaded corpus manifest with 0 document metadata entries
🗄️ Stored artifact: e1760be72296... (2677 bytes)
🗄️ Stored artifact: af7878b2ed57... (3109 bytes)
💰 Total estimated cost: $0.0000
📊 Batch plan: 0 batches, ⏱️ ~0.0 minutes
🧠 EnhancedAnalysisAgent initialized with mathematical validation

<img width="998" height="415" alt="Image" src="https://github.com/user-attachments/assets/a0f5b522-b249-4490-863e-9a2eab2ea752" />

### Steps to Reproduce

source venv/bin/activate && python3 discernus/cli.py run projects/simple_test

### Expected Behavior

proper costs and time

### Environment

_No response_

### Impact Assessment

_No response_

### Additional Context

_No response_

---

### Implement smart mock detection for LLM calls
- **Issue**: #198
- **Labels**: enhancement, developer-experience
- **Assignees**: 
- **Created**: 2025-07-29
- **Updated**: 2025-08-06
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Implement smart mock detection for LLM calls

**Full Description**:
## Problem
Current State: Developers are unsure when to use mocks vs real LLM calls, leading to wasted API costs
Impact: Unnecessary expenses and slower development cycles

## Solution
Add --mock-strategy flag with intelligent auto-detection to determine when mocks are sufficient.

## Implementation

Smart mock strategy system:
- auto: Automatically determine based on experiment type and test scope
- all: Force all calls to use mocks
- none: Force all calls to use real LLMs

Auto-detection logic:
- Structure validation: Use mocks (no LLM intelligence needed)
- Pipeline testing: Use mocks (testing orchestration, not content)
- Framework testing: Mixed (mock analysis, real synthesis)
- Full experiments: Real LLMs (content quality matters)

## Implementation Areas
- Add CLI flag --mock-strategy with choices
- Create mock detection heuristics
- Integrate with existing MockLLMGateway
- Add cost estimation for both approaches
- Update experiment validation logic

## Success Criteria
- --mock-strategy auto correctly identifies when mocks are sufficient
- Clear cost implications shown to user
- Seamless integration with existing mock infrastructure
- 30% reduction in unnecessary API costs
- Developer confidence in mock usage decisions

## Files to Modify
- discernus/cli.py - Add CLI flag
- discernus/core/mock_strategy.py - New auto-detection logic
- discernus/tests/mocks/mock_llm_gateway.py - Enhanced integration
- discernus/gateway/llm_gateway.py - Mock routing logic

Estimated Effort: 3-4 hours
Priority: High - reduces API costs significantly

Parent Epic: #194 Developer Velocity & Debugging Epic

---

### Implement real-time progress streaming for pipeline visibility
- **Issue**: #196
- **Labels**: enhancement, developer-experience
- **Assignees**: 
- **Created**: 2025-07-29
- **Updated**: 2025-08-06
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Implement real-time progress streaming for pipeline visibility

**Full Description**:
## Problem
Current State: Pipeline execution is a black box until completion
Impact: Cursor agents can't monitor progress, leading to premature interruptions and debugging confusion

## Solution
Add --live-stream flag to CLI that provides real-time progress updates during pipeline execution.

## Implementation Areas
- Add CLI flag to discernus/cli.py
- Create DebugConfig dataclass 
- Add streaming to ThinOrchestrator
- Add streaming to THIN synthesis pipeline
- Add streaming to individual agents
- Add token counting and cost estimation
- Add timing and ETA calculations

## Success Criteria
- --live-stream flag works with all experiment types
- Real-time visibility into pipeline stages
- LLM call details visible (model, tokens, cost)
- Progress timing and ETA estimation
- No performance impact when flag not used

## Files to Modify
- discernus/cli.py - Add CLI flag
- discernus/core/thin_orchestrator.py - Add streaming
- discernus/agents/thin_synthesis/orchestration/pipeline.py - Add streaming
- All agent files - Add progress indicators

Estimated Effort: 2-3 hours  
Priority: Highest - directly addresses black box problem

Parent Epic: #194 Developer Velocity & Debugging Epic

---

### Phase 3: Quality Validation and Comparative Evaluation
- **Issue**: #173
- **Labels**: enhancement
- **Assignees**: 
- **Created**: 2025-07-29
- **Updated**: 2025-08-06
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Phase 3: Quality Validation and Comparative Evaluation

**Epic**: 166

---

### Phase 2: Framework Generalizability Testing
- **Issue**: #172
- **Labels**: enhancement
- **Assignees**: 
- **Created**: 2025-07-29
- **Updated**: 2025-08-06
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Phase 2: Framework Generalizability Testing

**Epic**: 166

---

### [ARCHITECTURAL FIX] Remove Hardcoded Global Scope Requirements from DiscernusLibrarian
- **Issue**: #106
- **Labels**: bug, research, framework
- **Assignees**: 
- **Created**: 2025-07-21
- **Updated**: 2025-08-11
- **Milestone**: Alpha Quality & Hygiene
- **Description**: [ARCHITECTURAL FIX] Remove Hardcoded Global Scope Requirements from DiscernusLibrarian

**Full Description**:
# CRITICAL: Remove Inappropriate Global Scope Requirements

**Problem Identified**: DiscernusLibrarian has hardcoded international scope requirements that are causing:
- Fabricated citations when global studies don't exist
- Confidence crashes due to irrelevant geographical bias penalties  
- Methodologically inappropriate validation for context-specific frameworks

## �� Specific Code Locations to Fix

### Line 315: Remove mandatory global diversity requirement
```python
# CURRENT (PROBLEMATIC):
"Include diverse methodological approaches and ensure geographic/cultural diversity where possible."

# PROPOSED FIX:  
"Include diverse methodological approaches. Focus on the geographical scope specified by the researcher."
```

### Line 334: Remove mandatory non-Western perspective requirement
```python
# CURRENT (PROBLEMATIC):
"Missing Perspectives": Research from underrepresented populations, non-Western contexts, or different disciplines

# PROPOSED FIX:
"Missing Perspectives": Research from underrepresented populations within the specified scope, alternative theoretical perspectives, or different disciplines
```

### Lines 1310-1318: Remove Western-centric bias penalties
```python
# CURRENT (PROBLEMATIC):
if western_ratio > 0.8:
    return f"HIGH RISK - Strong Western bias detected... May be missing non-Western perspectives"

# PROPOSED FIX:
# Only flag bias if it conflicts with researcher-specified scope
# If researcher specifies "western democracies" - don't penalize Western focus
```

## 🎯 Evidence of Problem

**Original A1 Research (International Scope)**:
- 8 studies found, but 1 fabricated citation ("Hui et al. 2020")
- Confidence crashed to 3/10 after Blue Team found fabrications
- Penalized for "Western bias" despite appropriate scope for framework

**Scoped A1 Research (Western Democracy Focus)**:  
- 2 verified studies found (fewer but real)
- Stable confidence 5-7/10 across claims
- No fabricated citations
- Appropriate scope acceptance

## 🔧 Proposed Solution

1. **Add scope parameter to research_question() method**
2. **Modify prompts to respect researcher-defined scope**
3. **Update geographical bias analysis to be scope-aware**
4. **Remove hardcoded "ensure geographic/cultural diversity" requirements**

## ✅ Success Criteria

- DiscernusLibrarian accepts researcher-specified geographical scope
- No inappropriate penalties for scope-appropriate research
- Reduced pressure leading to fabricated citations
- More honest, stable confidence assessments

**Priority**: HIGH - This is causing research integrity failures and undermining framework validation work.

---

### Audit and fix directory creation logic to comply with provenance standard
- **Issue**: #30
- **Labels**: chore, tech-debt, provenance
- **Assignees**: 
- **Created**: 2025-07-19
- **Updated**: 2025-08-11
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Audit and fix directory creation logic to comply with provenance standard

**Full Description**:
## Problem Statement
The system is still creating non-compliant directory structures (e.g., `projects/MVA/experiments/`) instead of the correct, provenance-compliant structure: `projects/{PROJECT_NAME}/sessions/{SESSION_ID}/`.

This issue has two parts:
1.  **Code Fix:** Audit the codebase (likely in `WorkflowOrchestrator` and any related components) to find and fix the logic that creates incorrect directory structures. All new experiments must strictly follow the v3 provenance standard.
2.  **Data Migration:** Create a migration script (`scripts/migrate_legacy_projects.py`) to move existing, non-compliant project artifacts into the new, standardized `sessions`-based structure.

## Requirements

### Code Audit & Fix
- [ ] Review `discernus/orchestration/workflow_orchestrator.py`'s directory creation logic.
- [ ] Search for any other code paths that might create project directories.
- [ ] Correct all directory creation to use the canonical `projects/{PROJECT}/sessions/{SESSION}` format.
- [ ] Add tests to verify correct directory structure creation.

### Migration Script
- [ ] Create a migration script (`scripts/migrate_legacy_projects.py`).
- [ ] The script must preserve file contents and history where possible.
- [ ] Add a `--dry-run` flag to the script for safety.
- [ ] Document the migration process.

## Acceptance Criteria
- Running any experiment creates the correct, provenance-compliant directory structure.
- The migration script successfully reorganizes all legacy project data.
- The root `/projects` directory is clean of non-compliant project folders.

## Parent Epic
Part of **Epic #15: Research Quality & Provenance Enhancements**.

## Priority
High - This is fundamental to research provenance and data integrity.

---

### Prepare models.yaml registry for ensemble model orchestration
- **Issue**: #28
- **Labels**: enhancement, tech-debt, performance
- **Assignees**: 
- **Created**: 2025-07-19
- **Updated**: 2025-08-11
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Prepare models.yaml registry for ensemble model orchestration

**Full Description**:
## Problem Statement
Current system works well with Gemini models through Vertex AI, but when we start using ensembles with higher costs, shorter context windows, and strict rate limiting, we'll need intelligent model orchestration.

## Future Challenges
- Higher cost models (GPT-4, Claude Pro)
- Shorter context windows requiring prompt optimization
- Draconian TPM (tokens per minute) rate limiting
- Need for model selection based on task requirements

## Requirements
- [ ] Audit current models.yaml registry
- [ ] Design intelligent model selection logic
- [ ] Implement rate limiting awareness
- [ ] Add cost-based model routing
- [ ] Create context window optimization
- [ ] Add fallback model chains

## Model Orchestration Features
- [ ] Automatic model selection based on task complexity
- [ ] Rate limit queuing and retry logic
- [ ] Cost optimization routing
- [ ] Context window management
- [ ] Model availability monitoring

## Integration with LiteLLM Proxy
- [ ] Coordinate with LiteLLM Proxy implementation (Issue #17)
- [ ] Leverage proxy for rate limiting and routing
- [ ] Use proxy for cost tracking and optimization

## Parent Epic
Part of Epic #14: Performance & Infrastructure Upgrades

## Priority
Medium - important for future scalability

---

### Restore health check system for environment validation
- **Issue**: #26
- **Labels**: enhancement, chore
- **Assignees**: 
- **Created**: 2025-07-19
- **Updated**: 2025-08-11
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Restore health check system for environment validation

**Full Description**:
## Problem Statement
We previously had health checks that verified local environment and API availability before starting analysis. This system appears to be missing and should be restored.

## Requirements
The health check should validate:
- [ ] Python environment and dependencies
- [ ] LLM API connectivity and authentication
- [ ] Model availability and response
- [ ] Required directories and permissions
- [ ] Database connectivity (if applicable)
- [ ] Sufficient disk space for session outputs

## Implementation
- [ ] Create health check module
- [ ] Add to CLI as `discernus health` command
- [ ] Integrate into experiment startup process
- [ ] Provide clear error messages and remediation steps
- [ ] Add optional --fix flag for automatic remediation

## Error Handling
- Clear, actionable error messages
- Suggestions for fixing common issues
- Links to documentation for complex problems
- Graceful degradation when possible

## Integration Points
- [ ] CLI startup sequence
- [ ] Web interface initialization
- [ ] Extension loading process

## Parent Epic
Part of Epic #16: Extension Architecture & Academic Tools

## Priority
Medium-High - prevents wasted time on broken environments

---

### Implement knowledgenaut as first reference extension
- **Issue**: #25
- **Labels**: enhancement
- **Assignees**: 
- **Created**: 2025-07-19
- **Updated**: 2025-08-11
- **Milestone**: Alpha Quality & Hygiene
- **Description**: Implement knowledgenaut as first reference extension

**Full Description**:
## Problem Statement
The knowledgenaut literature review agent exists and does useful work. It's a perfect candidate for our first reference extension using the documented extension architecture and governance model.

## Implementation Requirements

**Extension Architecture Setup:**
- [ ] Review and implement extension architecture from documentation
- [ ] Create extension development guidelines
- [ ] Set up extension testing framework
- [ ] Establish governance model for extension approval

**Knowledgenaut Migration:**
- [ ] Extract knowledgenaut from core system
- [ ] Package as standalone extension
- [ ] Create extension manifest and documentation
- [ ] Implement extension loading mechanism
- [ ] Add extension management commands to CLI

**Documentation:**
- [ ] Extension development guide
- [ ] Knowledgenaut usage documentation
- [ ] Extension marketplace planning
- [ ] Governance and approval process

## Success Criteria
- [ ] Knowledgenaut works as extension
- [ ] Extension system is documented and testable
- [ ] Clear path for future extensions
- [ ] No degradation in knowledgenaut functionality

## Benefits
- Proves extension architecture works
- Provides template for future extensions
- Separates specialized tools from core system
- Enables community contributions

## Parent Epic
Part of Epic #16: Extension Architecture & Academic Tools

## Priority
Medium - important for platform extensibility

---

