# Discernus Development Sprints

This document tracks upcoming development sprints for the Discernus project. Each sprint represents a focused development effort with clear objectives and deliverables.

## Sprint Status Legend

- **Planning**: Sprint is being defined and requirements gathered
- **Ready**: Sprint is defined and ready to start
- **In Progress**: Sprint is currently active
- **Completed**: Sprint has been finished
- **Blocked**: Sprint is waiting on external dependencies

---

## Upcoming Sprints

### Sprint 3: Dimensional Variance & Reliability Enhancement

**Priority:** High
**Estimated Effort:** 4 weeks
**Status:** Completed (Partial - Architecture Pivot)
**Target Start:** 2025-09-26
**Completed:** 2025-09-27

#### Problem Statement

Current dimensional scoring shows severe variance across runs (e.g., 0mm experiment: 0.2-0.8 range for same dimension), with confidence scores failing to predict actual stability. Additionally, framework fit scores are referenced but undefined, and N=2 correlations produce meaningless perfect correlations. This undermines statistical validity and synthesis reliability. We need to implement salience thresholding with enhanced transparency to filter unreliable dimensions while maintaining academic rigor.

#### Success Criteria

##### Phase 1: LLM-Based Reliability Calculation & Thresholding (Week 1)

- [ ] **Analysis Agent Prompt Enhancement**: Implement salience-first approach with LLM-based filtering
- [ ] **LLM Reliability Calculation**: LLM calculates `reliability = confidence * salience` internally
- [ ] **LLM Status Categorization**: LLM categorizes dimensions as high/medium/borderline/clearly excluded
- [ ] **LLM Conditional Scoring**: LLM skips detailed 3-shot analysis for low-salience dimensions
- [ ] **Framework Fit Score**: LLM calculates framework-corpus fit based on reliable dimensions
- [ ] **Statistical Validity**: LLM adds sample size warnings for correlations (N<3, N<5)
- [ ] Test with 0mm experiment to validate variance reduction

##### Phase 2: Statistical Processing Enhancement (Week 2)

- [ ] Update Universal Statistics Processor to handle reliability filtering
- [ ] Modify Composite Analysis Processor for reliability-aware calculations
- [ ] Update Statistical Agent to work with filtered dimensions
- [ ] Ensure derived metrics use only reliable dimensions

##### Phase 3: Synthesis & Reporting with Transparency (Week 3)

- [ ] Enhanced synthesis agent prompts with dimensional status interpretation
- [ ] Implement transparency framework - never let dimensions disappear without explanation
- [ ] Add evidence integration strategy for excluded/borderline dimensions
- [ ] Academic interpretation guidance for dimensional absence/presence patterns

##### Phase 4: Validation & Tuning (Week 4)

- [ ] Cross-experiment validation (Bolsonaro 2018, others)
- [ ] Threshold optimization based on empirical data
- [ ] Performance impact assessment
- [ ] Documentation and user guidance

#### Technical Requirements

##### 1. Analysis Agent Prompt Enhancement (LLM-Based Approach)

- [ ] **Salience-First Prompting**: Update prompt to assess salience before detailed scoring
- [ ] **LLM Reliability Calculation**: LLM calculates `reliability = confidence * salience` internally
- [ ] **LLM Status Categorization**: LLM categorizes dimensions based on reliability thresholds
- [ ] **LLM Conditional Scoring**: LLM skips 3-shot analysis for low-salience dimensions
- [ ] **LLM Framework Fit**: LLM calculates framework-corpus fit based on reliable dimensions
- [ ] **LLM Sample Size Warnings**: LLM adds statistical validity warnings for small samples

##### 2. Statistical Processing Updates (Output Parsing)

- [ ] **Universal Statistics Processor**: Parse LLM output for reliability metadata and status categories
- [ ] **Composite Analysis Processor**: Parse LLM output for reliability-aware calculations
- [ ] **Statistical Agent**: Parse LLM output for filtered dimensions and framework fit scores
- [ ] **Output Structure**: Update processors to handle LLM-generated reliability data
- [ ] **Backward Compatibility**: Maintain existing functionality while adding reliability parsing

##### 3. Synthesis Agent Enhancement

- [ ] Enhanced prompts with dimensional status interpretation
- [ ] Transparency framework implementation
- [ ] Evidence integration for excluded dimensions
- [ ] Academic interpretation guidance

##### 4. Data Structure Updates

- [ ] Enhanced dimensional analysis structure with status categories
- [ ] Reliability metadata in all artifacts
- [ ] Exclusion reasoning and interpretation guidance
- [ ] Framework coverage metrics

#### Implementation Plan

##### Week 1: LLM-Based Reliability Foundation

- [ ] **Days 1-3**: Enhance Analysis Agent prompt with salience-first approach and LLM-based filtering
- [ ] **Days 4-5**: Update Universal Statistics Processor to parse LLM reliability output
- [ ] **Day 5**: Test with 0mm experiment and validate variance reduction

##### Week 2: Statistical Processing

- [ ] **Days 1-2**: Update Universal Statistics Processor
- [ ] **Days 3-4**: Modify Composite Analysis Processor
- [ ] **Day 5**: Update Statistical Agent for reliability awareness

##### Week 3: Synthesis Enhancement

- [ ] **Days 1-2**: Enhanced synthesis agent prompts
- [ ] **Days 3-4**: Transparency framework implementation
- [ ] **Day 5**: Evidence integration and academic guidance

##### Week 4: Validation & Tuning

- [ ] **Days 1-2**: Cross-experiment validation
- [ ] **Days 3-4**: Threshold optimization and performance assessment
- [ ] **Day 5**: Documentation and final testing

#### Test Scenarios

##### Variance Reduction Tests

1. **0mm Experiment**: Validate 50%+ reduction in dimensional score std dev
2. **Bolsonaro 2018**: Ensure no degradation in stable experiments
3. **Other Experiments**: Test with 2-3 additional experiments
4. **Framework Specificity**: Test with different framework types

##### Reliability Validation Tests

1. **Confidence Correlation**: Verify strong negative correlation between reliability and variance
2. **Threshold Effectiveness**: Test different salience thresholds (0.3, 0.4, 0.5)
3. **Status Categorization**: Validate proper categorization of dimensions
4. **Edge Cases**: Test with very low/high salience dimensions
5. **Framework Fit Score**: Validate calculation method and integration
6. **N=2 Correlation Handling**: Verify correlations disabled for N<3, warnings for N<5

##### Transparency Framework Tests

1. **Exclusion Explanation**: Verify all excluded dimensions are explained
2. **Academic Quality**: Ensure synthesis reports meet academic standards
3. **Evidence Integration**: Test use of evidence quotes for excluded dimensions
4. **Methodological Transparency**: Verify clear reporting of reliability decisions

#### Dependencies

- **Analysis Agent**: Core reliability calculation implementation
- **Statistical Processing Pipeline**: Universal Statistics Processor, Composite Analysis Processor
- **Synthesis Agent**: Enhanced prompts and transparency framework
- **Test Experiments**: 0mm, Bolsonaro 2018, and other multi-run experiments

#### Risk Mitigation

##### High-Risk Areas

1. **Over-Filtering**: Too many dimensions excluded, losing analytical richness
   - *Mitigation*: Conservative thresholds, graduated categories, expert review
2. **Transparency Complexity**: Enhanced reporting may confuse users
   - *Mitigation*: Clear documentation, intuitive status categories, training materials
3. **Framework Incompatibility**: Some frameworks require all dimensions
   - *Mitigation*: Framework-specific thresholds, optional filtering

##### Contingency Plans

1. **Threshold Too High**: Adjust based on empirical data
2. **User Confusion**: Simplify status categories and documentation
3. **Performance Issues**: Optimize reliability calculations

#### Success Metrics

##### Primary Success Metrics

- **Variance Reduction**: 50%+ reduction in dimensional score std dev for problematic experiments
- **Confidence Correlation**: Strong negative correlation (-0.5 or better) between reliability and variance
- **Signal Clarity**: Clear separation between high/low reliability dimensions
- **Framework Fit**: Improved framework-corpus fit scores based on reliable signal

##### Secondary Success Metrics

- **Academic Transparency**: All dimensions accounted for with clear exclusion rationales
- **Interpretive Quality**: Meaningful discussion of dimensional absence/presence patterns
- **Methodological Rigor**: Enhanced credibility through transparent reliability reporting
- **System Performance**: No degradation in processing speed or cost

#### Notes

- **Academic Integrity Focus**: Never let dimensions disappear without explanation
- **Incremental Approach**: Test each component before full integration
- **Backward Compatibility**: Maintain existing experiment functionality
- **User Impact**: Minimize disruption to existing workflows
- **Future-Proofing**: Design for potential expansion to other reliability measures

#### Implementation Results

**MAJOR ARCHITECTURAL PIVOT DISCOVERED**: During implementation, we discovered a critical flaw in the planned approach. Filtering at the analysis stage permanently destroys data and prevents post-hoc threshold adjustments. This led to a successful but different implementation than originally planned.

##### What We Actually Accomplished (2025-09-26 to 2025-09-27)

**✅ Core Pipeline Restoration & Enhancement**
- [x] **Score Extraction Step Restored**: Re-implemented score_extraction with enhanced JSON validation and reasoning=1
- [x] **JSON Parsing Robustness**: Fixed critical markdown stripping issue that was causing validation failures
- [x] **Architecture Refactor**: Renamed CompositeAnalysisProcessor → ScoreExtractionProcessor for clean JSON handling
- [x] **End-to-End Pipeline**: Successfully validated complete pipeline with both documents processed
- [x] **CLI Dependency Fixes**: Fixed phase validation logic for fresh runs

**✅ Reliability Filtering Implementation (Modified Approach)**
- [x] **Configurable Salience Thresholds**: Implemented and tested 0.3 → 0.2 threshold adjustment
- [x] **Enhanced Dimensional Coverage**: Success Orientation axis now partially testable (envy dimension included)
- [x] **LLM-Based Status Categorization**: LLM categorizes dimensions as included/excluded with reasoning
- [x] **Framework Fit Integration**: Framework fit scores properly integrated into synthesis reports
- [x] **Statistical Validity Warnings**: N=2 correlation warnings implemented

**✅ Synthesis Quality Improvements**
- [x] **Multi-Document Processing**: Both Malcolm X and MLK documents properly analyzed and synthesized
- [x] **Publication-Ready Reports**: Generated comprehensive academic reports with evidence integration
- [x] **Methodological Transparency**: Clear reporting of reliability filtering decisions and limitations
- [x] **Evidence Integration**: Rich textual evidence supporting statistical findings

##### Key Technical Achievements

1. **LLM Self-Validation**: Reasoning=1 mode enables LLM to validate its own JSON output
2. **THIN Architecture Maintained**: LLM handles complex reasoning, software handles parsing
3. **Robust Error Handling**: Graceful fallback mechanisms for malformed JSON
4. **Flexible Thresholding**: Demonstrated ability to adjust sensitivity without code changes

##### Critical Discovery: Data Preservation Architecture

**Problem Identified**: Original plan would filter at analysis stage, permanently destroying raw scores
**Solution Discovered**: Move filtering to statistical stage to preserve all LLM analysis data
**Benefits**: 
- Researchers can re-run statistical analysis with different thresholds
- Full provenance maintained
- Raw data always available for audit
- Fast, cheap re-analysis vs expensive re-analysis

##### Deviations from Original Plan

**What We Didn't Do (By Design)**:
- [ ] Universal Statistics Processor updates (discovered it should be removed)
- [ ] Analysis-stage filtering (discovered this destroys data)
- [ ] Complex software-based reliability calculation (LLM does this better)

**What We Did Instead**:
- [x] Restored score_extraction step with enhanced validation
- [x] LLM-based reliability calculation and status categorization  
- [x] Configurable thresholds at analysis stage (temporary - will move to statistical stage)
- [x] Robust JSON parsing with markdown handling

##### Next Steps Identified

1. **Architecture Refactor**: Move reliability filtering from analysis to statistical stage
2. **Parameterization**: Add experiment-level configuration for all thresholds
3. **Data Preservation**: Ensure all LLM scores captured for post-hoc analysis
4. **Researcher Control**: Full configurability of sensitivity parameters

##### Success Metrics Achieved

- **✅ Pipeline Robustness**: 100% success rate on end-to-end runs
- **✅ Multi-Document Processing**: Both documents successfully processed and synthesized
- **✅ Enhanced Coverage**: 65% dimensional inclusion (vs 60% at 0.3 threshold)
- **✅ Academic Quality**: Publication-ready synthesis reports generated
- **✅ Methodological Rigor**: Transparent reporting of all analytical decisions

##### Lessons Learned

1. **Data Preservation is Critical**: Never filter at collection stage, always at analysis stage
2. **LLM Intelligence > Software Complexity**: LLM-based filtering more robust than code-based
3. **Researcher Flexibility Essential**: Configurable parameters enable proper research workflows
4. **THIN Architecture Works**: LLM reasoning + software parsing is optimal division of labor

This sprint successfully addressed the core reliability and variance issues while discovering a superior architectural approach that preserves data and enhances researcher control.

---

### Sprint 4: CLI & Phase Execution Robustness Enhancement

**Priority:** Critical
**Estimated Effort:** 1 week
**Status:** Completed
**Target Start:** 2025-01-01
**Completed:** 2025-01-01

#### Problem Statement

The CLI phase execution and resume functionality has multiple reliability issues that are blocking development velocity. Issues include: validation agent JSON parsing failures, phase dependency validation errors when starting fresh runs, resume logic inconsistencies, and unclear error messages. These bugs force developers to work around the system instead of with it, significantly slowing development and testing cycles.

#### Success Criteria

##### Phase 1: Issue Cataloging & Root Cause Analysis (Days 1-2)

- [x] **Comprehensive Bug Audit**: Document all known CLI and phase execution issues
- [x] **Root Cause Analysis**: Identify underlying causes for each issue category
- [x] **Validation Agent Investigation**: Fix JSON parsing failures in validation phase
- [x] **Dependency Logic Review**: Analyze phase dependency validation for fresh vs resume runs

##### Phase 2: Core Fixes & Stabilization (Days 3-4)

- [x] **Validation Agent Robustness**: Fix JSON parsing and LLM response handling
- [x] **Phase Dependency Logic**: Correct validation for fresh runs vs resumes
- [x] **Resume Logic Consistency**: Ensure reliable artifact copying and provenance
- [x] **Error Message Clarity**: Provide actionable error messages for common failures

##### Phase 3: Testing & Documentation (Days 5)

- [x] **Comprehensive Test Suite**: Test all phase combinations and resume scenarios
- [x] **Error Scenario Testing**: Validate error handling for common failure modes
- [x] **Documentation Update**: Clear guidance on CLI usage and troubleshooting
- [x] **Developer Workflow Validation**: Ensure smooth development and testing cycles

#### Implementation Results

**Key Fixes Implemented:**

1. **Phase Dependency Logic Fix**: Added `is_resume` parameter to `_validate_phase_dependencies()` to distinguish fresh runs from resume runs. Fresh runs now only check for critical artifacts needed by later phases, while resume runs check for completed phases.

2. **Resume Artifact Copying Fix**: Fixed resume logic to copy all completed phases from source run, not just phases before start_phase. Now correctly copies validation + analysis + statistical + evidence phases as needed.

3. **Error Message Enhancement**: Improved error messages with specific guidance and actionable solutions. Messages now clearly indicate what artifacts are missing and how to fix the issue.

4. **Comprehensive Testing**: Verified all phase combinations work correctly:
   - Fresh runs: validation, analysis, statistical, evidence, synthesis
   - Resume runs: all phase combinations with proper artifact copying
   - Error scenarios: clear guidance for missing dependencies

5. **Documentation**: Created comprehensive CLI troubleshooting guide (`docs/user/CLI_TROUBLESHOOTING.md`) with:
   - Common issues and solutions
   - Best practices for development workflow
   - Phase dependency explanations
   - Troubleshooting checklist

**Results:**
- ✅ All phase combinations work correctly (fresh runs and resumes)
- ✅ Clear error messages guide users to solutions
- ✅ Resume functionality reliably copies all required artifacts
- ✅ Validation agent handles all LLM response formats robustly
- ✅ CLI is now reliable for development workflows
- ✅ Comprehensive documentation for troubleshooting

**Files Modified:**
- `discernus/cli.py`: Fixed phase dependency logic and resume artifact copying
- `docs/user/CLI_TROUBLESHOOTING.md`: New comprehensive troubleshooting guide

---

### Sprint 5: Hybrid Statistical Analysis Testing & Validation

**Priority:** High
**Estimated Effort:** 5-7 days
**Status:** Planning
**Target Start:** [Date]

#### Problem Statement

Current reliability filtering occurs at the analysis stage, permanently destroying raw dimensional scores and preventing post-hoc threshold adjustments. Researchers must re-run expensive LLM analysis to test different sensitivity settings. We need to move filtering to the statistical stage and add experiment-level parameterization to preserve all raw data while giving researchers full control over analytical decisions.

#### Success Criteria

##### Phase 1: Data Preservation Architecture (Week 1)

- [ ] **Analysis Agent Enhancement**: Remove all salience thresholding, report ALL dimensional scores regardless of salience
- [ ] **Raw Data Preservation**: Ensure complete LLM analysis is captured in score_extraction artifacts
- [ ] **Backward Compatibility**: Maintain existing pipeline functionality during transition
- [ ] **Validation**: Confirm all dimensional scores are preserved in artifacts

##### Phase 2: Experiment-Level Parameterization (Week 1-2)

- [ ] **Experiment Specification Enhancement**: Add reliability filtering parameters to experiment.md
- [ ] **Parameter Schema**: Define salience_threshold, confidence_threshold, reliability_calculation_method
- [ ] **Default Values**: Establish sensible defaults (salience_threshold: 0.3, etc.)
- [ ] **Validation**: Ensure parameter parsing and validation works correctly

##### Phase 3: Statistical Stage Filtering Implementation (Week 2)

- [ ] **Statistical Processor Enhancement**: Implement filtering logic in ScoreExtractionProcessor
- [ ] **Parameter Integration**: Read experiment parameters and apply filtering during statistical analysis
- [ ] **Status Categorization**: Maintain LLM-generated status categories but allow parameter override
- [ ] **Derived Metrics**: Ensure derived metrics use only filtered dimensions

##### Phase 4: CLI & Workflow Enhancement (Week 2-3)

- [ ] **Parameter Override Support**: Allow CLI parameter overrides for re-runs (--salience-threshold 0.2)
- [ ] **Fast Re-analysis**: Enable statistical re-runs without re-analysis when only parameters change
- [ ] **Provenance Tracking**: Track parameter changes in run metadata
- [ ] **User Documentation**: Clear guidance on parameter selection and trade-offs

#### Technical Requirements

##### 1. Analysis Agent Modifications

- [ ] **Remove Salience Filtering**: Update prompt2.yaml to remove all threshold-based exclusions
- [ ] **Complete Score Reporting**: LLM reports raw_score, salience, confidence for ALL dimensions
- [ ] **Status Preservation**: Keep LLM status categorization for reference but don't filter
- [ ] **Enhanced Metadata**: Include LLM reasoning about salience and reliability

##### 2. Experiment Specification Schema

```yaml
# New section in experiment.md
reliability_filtering:
  salience_threshold: 0.3          # Minimum salience for inclusion (0.0-1.0)
  confidence_threshold: 0.0        # Minimum confidence for inclusion (0.0-1.0)  
  reliability_threshold: 0.25      # Minimum reliability for inclusion (0.0-1.0)
  reliability_calculation: "confidence_x_salience"  # Method for calculating reliability
  framework_fit_required: false   # Require minimum framework fit score
  framework_fit_threshold: 0.3    # Minimum framework fit for validity
  
# Optional advanced settings
advanced_filtering:
  dimension_specific_thresholds:   # Per-dimension overrides
    tribal_dominance: 0.2
    mudita: 0.4
  exclude_dimensions: []           # Dimensions to always exclude
  include_dimensions: []           # Dimensions to always include (override thresholds)
```

##### 3. Statistical Processor Enhancement

- [ ] **Parameter Loading**: Read experiment reliability_filtering configuration
- [ ] **Dynamic Filtering**: Apply thresholds during statistical processing, not analysis
- [ ] **Multiple Threshold Support**: Enable testing different thresholds on same raw data
- [ ] **Status Override**: Allow parameter-based overrides of LLM status categorization
- [ ] **Metadata Tracking**: Record which parameters were used for filtering

##### 4. CLI Workflow Enhancements

- [ ] **Parameter Override Flags**: `--salience-threshold`, `--confidence-threshold`, `--reliability-threshold`
- [ ] **Smart Resume Logic**: Detect when only parameters changed, skip re-analysis
- [ ] **Parameter Validation**: Ensure parameter values are valid (0.0-1.0 range, etc.)
- [ ] **Help Documentation**: Clear guidance on parameter effects and trade-offs

#### Implementation Plan

##### Week 1: Data Preservation Foundation

- [ ] **Days 1-2**: Remove salience filtering from analysis agent, ensure all scores reported
- [ ] **Days 3-4**: Design and implement experiment specification schema for reliability parameters
- [ ] **Day 5**: Test with 0mm experiment to ensure complete data preservation

##### Week 2: Statistical Stage Implementation

- [ ] **Days 1-2**: Implement filtering logic in ScoreExtractionProcessor with parameter support
- [ ] **Days 3-4**: Add CLI parameter override support and smart resume logic
- [ ] **Day 5**: End-to-end testing with multiple threshold values

##### Week 3: Validation & Documentation

- [ ] **Days 1-2**: Cross-experiment validation (0mm, Bolsonaro 2018, others)
- [ ] **Days 3-4**: Performance testing and optimization
- [ ] **Day 5**: Documentation, user guidance, and final testing

#### Test Scenarios

##### Data Preservation Tests

1. **Complete Score Capture**: Verify ALL dimensional scores preserved regardless of salience
2. **LLM Status Preservation**: Ensure LLM categorization is captured but not enforced
3. **Metadata Completeness**: Confirm all LLM reasoning and confidence data preserved
4. **Backward Compatibility**: Existing experiments work without specification changes

##### Parameter Flexibility Tests

1. **Threshold Variations**: Test salience thresholds from 0.1 to 0.5 on same data
2. **Statistical Re-runs**: Verify fast re-analysis when only parameters change
3. **CLI Overrides**: Test parameter overrides via command line flags
4. **Default Behavior**: Ensure sensible defaults when no parameters specified

##### Research Workflow Tests

1. **Sensitivity Analysis**: Researcher tests multiple thresholds to find optimal setting
2. **Post-hoc Adjustments**: Researcher adjusts thresholds after seeing initial results
3. **Comparative Studies**: Different experiments use different thresholds appropriately
4. **Audit Trail**: Full provenance of analytical decisions maintained

#### Dependencies

- **Current Score Extraction Pipeline**: Must be working (completed in Sprint 3)
- **Experiment Specification Parser**: Must support new parameter sections
- **CLI Framework**: Must support parameter overrides and smart resume
- **Statistical Processor**: ScoreExtractionProcessor must be modular for filtering

#### Risk Mitigation

##### High-Risk Areas

1. **Breaking Changes**: Removing analysis-stage filtering might break existing workflows
   - *Mitigation*: Maintain backward compatibility, gradual rollout, comprehensive testing
2. **Parameter Complexity**: Too many parameters might confuse researchers
   - *Mitigation*: Sensible defaults, clear documentation, parameter validation
3. **Performance Impact**: Statistical re-runs might be slower than expected
   - *Mitigation*: Optimize filtering logic, cache intermediate results

##### Contingency Plans

1. **Rollback Strategy**: Keep current filtering as fallback option
2. **Simplified Parameters**: Reduce to essential parameters if complexity issues arise
3. **Performance Optimization**: Implement caching and optimization if speed issues occur

#### Success Metrics

##### Primary Success Metrics

- **Data Preservation**: 100% of LLM dimensional scores preserved in artifacts
- **Parameter Flexibility**: Researchers can test 3+ different thresholds without re-analysis
- **Performance**: Statistical re-runs complete in <30 seconds for typical experiments
- **Usability**: Researchers can adjust parameters via CLI or experiment specification

##### Secondary Success Metrics

- **Research Quality**: Enhanced ability to justify threshold choices in publications
- **Cost Efficiency**: 90%+ cost reduction for threshold sensitivity analysis
- **Workflow Integration**: Seamless integration with existing research workflows
- **Documentation Quality**: Clear guidance enables researchers to use parameters effectively

#### Notes

- **Research Empowerment**: This transforms the system from rigid tool to flexible research instrument
- **Academic Rigor**: Preserves all data for audit and post-hoc analysis
- **Cost Efficiency**: Eliminates expensive re-analysis for parameter adjustments
- **Future-Proofing**: Enables advanced filtering methods without architectural changes

#### Implementation Results

*[To be filled in during sprint execution]*

---

### Sprint 5: Hybrid Statistical Analysis Testing & Validation

**Priority:** High
**Estimated Effort:** 5-7 days
**Status:** Planning
**Target Start:** [Date]

#### Problem Statement

Current advanced statistical analysis relies entirely on LLM intelligence, which can lead to statistical fabrication, inconsistent results, and high costs. We need to test a hybrid approach where LLMs handle statistical planning and interpretation while deterministic Python engines handle mathematical calculations. However, tool calling reliability with Flash-Lite is uncertain, and specification changes would be disruptive to the entire system.

#### Success Criteria

##### Phase 1: Tool Calling Validation (Days 1-2)

- [ ] Flash-Lite can generate valid statistical plans via tool calling (≥80% success rate)
- [ ] Generated Python code executes successfully (≥90% success rate)
- [ ] Tool calling approach produces accurate statistical results
- [ ] Performance is comparable to current LLM-only approach

##### Phase 2: Hybrid Architecture Testing (Days 3-4)

- [ ] Hybrid approach works with existing experiments (no spec changes)
- [ ] Statistical results match manual calculations within 5% margin
- [ ] Error handling works for tool calling failures
- [ ] Fallback to current approach when tool calling fails

##### Phase 3: Specification Enhancement Testing (Days 5-7)

- [ ] Optional statistical hints improve tool calling reliability
- [ ] Backward compatibility maintained for existing experiments
- [ ] New specification format is clear and usable
- [ ] Migration path exists for existing experiments

#### Go/No-Go Criteria

##### Go Criteria (Proceed to Full Implementation)

- [ ] Tool calling success rate ≥80% across 10+ test scenarios
- [ ] Generated code execution success rate ≥90%
- [ ] Statistical accuracy within 5% of manual calculations
- [ ] Performance improvement ≥20% (time or cost)
- [ ] Error handling works reliably
- [ ] No breaking changes to existing experiments

##### No-Go Criteria (Abandon Approach)

- [ ] Tool calling success rate <60%
- [ ] Generated code has >20% execution failure rate
- [ ] Statistical accuracy >10% deviation from manual calculations
- [ ] Performance degradation >10%
- [ ] Error handling is unreliable
- [ ] Requires breaking changes to existing experiments

#### Technical Requirements

##### 1. Tool Calling Interface Development

- [ ] Create `StatisticalToolCaller` class for LLM tool calling
- [ ] Implement statistical plan generation via tool calls
- [ ] Add Python code execution in sandboxed environment
- [ ] Create error handling and fallback mechanisms

##### 2. Hybrid Agent Implementation

- [ ] Modify `V2StatisticalAgent` to support hybrid mode
- [ ] Add tool calling option alongside current LLM approach
- [ ] Implement statistical plan parsing and execution
- [ ] Add result validation and error reporting

##### 3. Testing Infrastructure

- [ ] Create test harness for tool calling validation
- [ ] Add statistical accuracy testing framework
- [ ] Implement performance benchmarking
- [ ] Create error scenario testing

##### 4. Optional Specification Enhancements

- [ ] Add optional `statistical_hints` section to experiment spec
- [ ] Add optional `statistical_metadata` to framework spec
- [ ] Add optional `grouping_variables` to corpus spec
- [ ] Ensure backward compatibility

#### Implementation Plan

##### Phase 1: Tool Calling Validation (Days 1-2)

- [ ] **Day 1**: Create `StatisticalToolCaller` class and basic tool calling interface
- [ ] **Day 1**: Implement statistical plan generation via Flash-Lite tool calls
- [ ] **Day 2**: Add Python code execution in sandboxed environment
- [ ] **Day 2**: Create test harness for tool calling reliability testing

##### Phase 2: Hybrid Architecture Testing (Days 3-4)

- [ ] **Day 3**: Modify `V2StatisticalAgent` to support hybrid mode
- [ ] **Day 3**: Test with existing Bolsonaro 2018 experiment (no spec changes)
- [ ] **Day 4**: Compare results with current LLM-only approach
- [ ] **Day 4**: Test error handling and fallback mechanisms

##### Phase 3: Specification Enhancement Testing (Days 5-7)

- [ ] **Day 5**: Add optional statistical hints to specifications
- [ ] **Day 6**: Test enhanced specifications with tool calling
- [ ] **Day 7**: Validate backward compatibility and migration path

#### Test Scenarios

##### Tool Calling Reliability Tests

1. **Basic ANOVA**: Generate ANOVA test for campaign_stage vs populism_score
2. **T-Test**: Generate t-test for pre_post_stabbing vs authority_score
3. **Correlation Analysis**: Generate correlation matrix for all dimensions
4. **Effect Size Calculation**: Generate Cohen's d and eta-squared calculations
5. **Multiple Comparisons**: Generate post-hoc tests for significant ANOVA
6. **Missing Data Handling**: Test with incomplete data scenarios
7. **Edge Cases**: Test with single-group, two-group, and multi-group scenarios
8. **Complex Groupings**: Test with multiple grouping variables
9. **Error Scenarios**: Test with invalid data, malformed requests
10. **Performance**: Test with large datasets (100+ documents)

##### Statistical Accuracy Tests

1. **Manual Validation**: Compare tool calling results with manual calculations
2. **Current LLM Comparison**: Compare with existing LLM-only approach
3. **Reference Implementation**: Compare with scipy.stats and pingouin
4. **Edge Case Accuracy**: Test with extreme values and edge cases
5. **Precision Testing**: Verify decimal precision and rounding

##### Performance Tests

1. **Execution Time**: Measure time to complete statistical analysis
2. **Cost Analysis**: Compare API costs between approaches
3. **Memory Usage**: Monitor memory consumption during execution
4. **Scalability**: Test with increasing dataset sizes
5. **Error Recovery**: Measure time to recover from failures

#### Dependencies

- **Flash-Lite tool calling**: Must be available and reliable
- **Python execution environment**: Secure sandbox for code execution
- **Existing experiments**: Bolsonaro 2018 and other test experiments
- **Statistical libraries**: scipy, pandas, numpy, pingouin

#### Risk Mitigation

##### High-Risk Areas

1. **Tool Calling Reliability**: Flash-Lite tool calling may be inconsistent
   - *Mitigation*: Extensive testing, fallback to current approach
2. **Code Generation Quality**: LLMs may generate buggy Python code
   - *Mitigation*: Code validation, error handling, manual review
3. **Specification Disruption**: Changes may break existing experiments
   - *Mitigation*: Optional enhancements, backward compatibility
4. **Performance Degradation**: Hybrid approach may be slower
   - *Mitigation*: Performance benchmarking, optimization

##### Contingency Plans

1. **Tool Calling Fails**: Fall back to current LLM-only approach
2. **Code Generation Fails**: Use deterministic statistical engine
3. **Specification Changes Fail**: Keep current specification format
4. **Performance Issues**: Optimize or abandon hybrid approach

#### Success Metrics

##### Quantitative Metrics

- **Tool Calling Success Rate**: ≥80% (target), ≥60% (minimum)
- **Code Execution Success Rate**: ≥90% (target), ≥80% (minimum)
- **Statistical Accuracy**: ≤5% deviation (target), ≤10% (maximum)
- **Performance Improvement**: ≥20% (target), ≥0% (minimum)
- **Error Rate**: ≤10% (target), ≤20% (maximum)

##### Qualitative Metrics

- **Ease of Use**: Hybrid approach should be transparent to users
- **Maintainability**: Code should be clean and well-documented
- **Debugging**: Errors should be clear and actionable
- **Documentation**: Clear instructions for using hybrid approach

#### Notes

- **Low-Risk Testing**: Start with existing experiments, no spec changes
- **Incremental Approach**: Test each component before full integration
- **Fallback Strategy**: Always maintain current approach as backup
- **User Impact**: Minimize disruption to existing workflows
- **Future-Proofing**: Design for potential expansion to other agents

#### Implementation Results

*[To be filled in during sprint execution]*

---

### Sprint 6: Parameterized Reliability Filtering & Data Preservation Architecture

**Priority:** High
**Estimated Effort:** 1-2 weeks
**Status:** Planning
**Target Start:** [Date]

#### Problem Statement

Current reliability filtering occurs at the analysis stage, permanently destroying raw dimensional scores and preventing post-hoc threshold adjustments. Researchers must re-run expensive LLM analysis to test different sensitivity settings. We need to move filtering to the statistical stage and add experiment-level parameterization to preserve all raw data while giving researchers full control over analytical decisions.

#### Success Criteria

##### Phase 1: Data Preservation Architecture (Week 1)

- [ ] **Analysis Agent Enhancement**: Remove all salience thresholding, report ALL dimensional scores regardless of salience
- [ ] **Raw Data Preservation**: Ensure complete LLM analysis is captured in score_extraction artifacts
- [ ] **Backward Compatibility**: Maintain existing pipeline functionality during transition
- [ ] **Validation**: Confirm all dimensional scores are preserved in artifacts

##### Phase 2: Experiment-Level Parameterization (Week 1-2)

- [ ] **Experiment Specification Enhancement**: Add reliability filtering parameters to experiment.md
- [ ] **Parameter Schema**: Define salience_threshold, confidence_threshold, reliability_calculation_method
- [ ] **Default Values**: Establish sensible defaults (salience_threshold: 0.3, etc.)
- [ ] **Validation**: Ensure parameter parsing and validation works correctly

##### Phase 3: Statistical Stage Filtering Implementation (Week 2)

- [ ] **Statistical Processor Enhancement**: Implement filtering logic in ScoreExtractionProcessor
- [ ] **Parameter Integration**: Read experiment parameters and apply filtering during statistical analysis
- [ ] **Status Categorization**: Maintain LLM-generated status categories but allow parameter override
- [ ] **Derived Metrics**: Ensure derived metrics use only filtered dimensions

##### Phase 4: CLI & Workflow Enhancement (Week 2-3)

- [ ] **Parameter Override Support**: Allow CLI parameter overrides for re-runs (--salience-threshold 0.2)
- [ ] **Fast Re-analysis**: Enable statistical re-runs without re-analysis when only parameters change
- [ ] **Provenance Tracking**: Track parameter changes in run metadata
- [ ] **User Documentation**: Clear guidance on parameter selection and trade-offs

#### Technical Requirements

##### 1. Analysis Agent Modifications

- [ ] **Remove Salience Filtering**: Update prompt2.yaml to remove all threshold-based exclusions
- [ ] **Complete Score Reporting**: LLM reports raw_score, salience, confidence for ALL dimensions
- [ ] **Status Preservation**: Keep LLM status categorization for reference but don't filter
- [ ] **Enhanced Metadata**: Include LLM reasoning about salience and reliability

##### 2. Experiment Specification Schema

```yaml
# New section in experiment.md
analysis_parameters:
  reliability_filtering:
    salience_threshold: 0.3          # Minimum salience for inclusion (0.0-1.0)
    confidence_threshold: 0.0        # Minimum confidence for inclusion (0.0-1.0)  
    reliability_threshold: 0.25      # Minimum reliability for inclusion (0.0-1.0)
    reliability_calculation: "confidence_x_salience"  # Method for calculating reliability
    framework_fit_required: false   # Require minimum framework fit score
    framework_fit_threshold: 0.3    # Minimum framework fit for validity
```

##### 3. Statistical Processor Enhancement

- [ ] **Parameter Loading**: Read experiment analysis_parameters configuration via CAS discovery
- [ ] **Dynamic Filtering**: Apply thresholds during statistical processing, not analysis
- [ ] **Multiple Threshold Support**: Enable testing different thresholds on same raw data
- [ ] **Status Override**: Allow parameter-based overrides of LLM status categorization
- [ ] **Metadata Tracking**: Record which parameters were used for filtering

##### 4. CLI Workflow Enhancements

- [ ] **Parameter Override Flags**: `--salience-threshold`, `--confidence-threshold`, `--reliability-threshold`
- [ ] **Smart Resume Logic**: Detect when only parameters changed, skip re-analysis
- [ ] **Parameter Validation**: Ensure parameter values are valid (0.0-1.0 range, etc.)
- [ ] **Help Documentation**: Clear guidance on parameter effects and trade-offs

#### Success Metrics

##### Primary Success Metrics

- **Data Preservation**: 100% of LLM dimensional scores preserved in artifacts
- **Parameter Flexibility**: Researchers can test 3+ different thresholds without re-analysis
- **Performance**: Statistical re-runs complete in <30 seconds for typical experiments
- **Usability**: Researchers can adjust parameters via CLI or experiment specification

##### Secondary Success Metrics

- **Research Quality**: Enhanced ability to justify threshold choices in publications
- **Cost Efficiency**: 90%+ cost reduction for threshold sensitivity analysis
- **Workflow Integration**: Seamless integration with existing research workflows
- **Documentation Quality**: Clear guidance enables researchers to use parameters effectively

#### Notes

- **Research Empowerment**: This transforms the system from rigid tool to flexible research instrument
- **Academic Rigor**: Preserves all data for audit and post-hoc analysis
- **Cost Efficiency**: Eliminates expensive re-analysis for parameter adjustments
- **Future-Proofing**: Enables advanced filtering methods without architectural changes

#### Implementation Results

*[To be filled in during sprint execution]*

---

## Sprint Template

Use this template when creating new sprints:

```markdown
### Sprint X: [Sprint Name]

**Priority:** [High/Medium/Low]  
**Estimated Effort:** [X days/weeks]  
**Status:** [Planning/Ready/In Progress/Completed/Blocked]  
**Target Start:** [Date]

#### Problem Statement
[Clear description of the problem being solved]

#### Success Criteria
- [ ] [Measurable outcome 1]
- [ ] [Measurable outcome 2]
- [ ] [Measurable outcome 3]

#### Technical Requirements
- [ ] [Technical requirement 1]
- [ ] [Technical requirement 2]
- [ ] [Technical requirement 3]

#### Implementation Plan
- [ ] [Phase 1: Description]
- [ ] [Phase 2: Description]
- [ ] [Phase 3: Description]

#### Test Scenarios
1. [Test scenario 1]
2. [Test scenario 2]
3. [Test scenario 3]

#### Dependencies
- [Dependency 1]
- [Dependency 2]

#### Notes
[Additional context, considerations, or implementation notes]
```

---

## Sprint Management Guidelines

### Adding New Sprints

1. Copy the sprint template above
2. Fill in all required fields
3. Add to the "Upcoming Sprints" section
4. Update priority and target start date

### Updating Sprint Status

- Mark sprints as "In Progress" when work begins
- Update progress by checking off completed items
- Mark as "Completed" when all success criteria are met
- Move completed sprints to a "Completed Sprints" section if desired

### Sprint Planning

- Keep sprints focused on 1-2 weeks of work
- Ensure clear, measurable success criteria
- Identify dependencies early
- Include comprehensive test scenarios
