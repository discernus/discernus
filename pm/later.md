# Discernus Deferred Items

**Purpose**: Track complex features and approaches that are not immediately actionable but represent future strategic directions.

**Usage**: 
- Items that require significant orchestrator changes
- Complex ensemble approaches that need more research
- Features that would destabilize current working system
- Strategic directions for future major versions

---

## Ensemble Analysis Approaches

### Multi-Model Independent Self-Consistency Analysis

**Description**: Implement independent self-consistency using multiple different LLM models (Claude, GPT-4o, Gemini Pro) with confidence-weighted median aggregation

**Why Deferred**:
- Requires orchestrator changes to manage multiple model APIs
- Significant cost increase (8-12x baseline)
- Complex confidence extraction and weighting logic
- Would destabilize current working analysis pipeline

**Strategic Value**: 
- Maximum accuracy (95-98% of theoretical ceiling)
- Publication-ready methodological rigor
- Systematic error compensation across model architectures

**Implementation Requirements**:
- Multi-model orchestration layer
- Confidence-weighted aggregation system
- Cross-model consensus validation
- Comprehensive statistical validation

**Reference**: See [academic_ensemble_strategy.md](pm/active_projects/academic_ensemble_strategy.md) for detailed methodology

**Timeline**: Future major version (v11+)

---

## Synthesis Enhancement Approaches

### Multi-Report Synthesis Agent

**Description**: Generate 3 different synthesis reports from same analysis data, then use a "report synthesis agent" to combine best aspects of each

**Why Deferred**:
- Requires orchestrator changes to manage multiple synthesis runs
- Adds complexity to synthesis pipeline
- Synthesis variance is manageable with current approach
- Analysis variance is the primary concern

**Strategic Value**:
- Higher quality final reports
- Better coverage of different analytical perspectives
- Reduced synthesis variance through aggregation

**Implementation Requirements**:
- Multiple synthesis orchestration
- Report comparison and selection logic
- Report synthesis agent implementation
- Quality assessment metrics

**Timeline**: Post-analysis variance reduction (Phase 2)

---

## Advanced Statistical Analysis

### Ensemble Statistical Validation

**Description**: Implement statistical analysis using multiple independent runs with consensus validation and outlier detection

**Why Deferred**:
- Requires significant changes to statistical analysis pipeline
- Statistical analysis is currently stable and reliable
- Analysis variance is the primary concern, not statistical analysis variance

**Strategic Value**:
- More robust statistical conclusions
- Better handling of edge cases
- Publication-ready statistical rigor

**Implementation Requirements**:
- Multi-run statistical analysis orchestration
- Consensus measurement and validation
- Outlier detection and filtering
- Statistical significance testing across runs

**Timeline**: Future enhancement phase

---

## CLI Enhancement Features

### Analysis Mode Selection Flag

**Description**: Add CLI flag to allow researchers to choose between single run and internal multi-run analysis modes

**Why Deferred**:
- Current 3-run median aggregation is working well as the default
- Requires CLI argument parsing changes and prompt switching logic
- Need to validate that single-run mode maintains quality
- Should wait until 3-run mode is fully validated across diverse frameworks

**Strategic Value**:
- Flexibility for researchers who prefer single-run analysis
- Cost optimization for preliminary/exploratory experiments
- A/B testing capability between single and multi-run approaches
- Researcher choice and control over analysis depth

**Implementation Requirements**:
- CLI argument parsing for `--analysis-mode` flag
- Dynamic prompt loading (single vs. 3-run prompts)
- Validation that both modes produce compatible output formats
- Documentation of mode differences and use cases
- Cost and quality comparison metrics

**Timeline**: Post-3-run validation across diverse frameworks (Phase 3)

---

## Notes

- **Priority Order**: Analysis variance reduction → Synthesis enhancement → CLI enhancements → Advanced statistical analysis
- **Implementation Strategy**: Start with low-risk internal self-consistency, evaluate results, then consider more complex approaches
- **Risk Assessment**: Current system is working well, avoid changes that could destabilize core functionality
- **Cost-Benefit**: Focus on high-impact, low-risk improvements first

**Alternative Approach**: Accept current performance limitations and focus on core functionality for release

---

## Multi-Stage Model Validation System

**Description**: Implement comprehensive model validation at CLI, orchestrator, and agent levels to prevent runtime failures and provide better user experience.

**Why Deferred**:
- **Core Functionality**: Models work when correctly specified
- **Release Priority**: Not critical path for v1.0
- **User Error Handling**: Current system fails gracefully (eventually)
- **Complexity**: Requires changes across multiple system layers

**Current State**:
- ❌ **CLI Level**: No model validation against `models.yaml`
- ❌ **Orchestrator Level**: No model validation before phase execution
- ❌ **Agent Level**: No model availability checking
- ❌ **Error Handling**: Fails at execution time, not validation time

**Strategic Value**:
- **User Experience**: Fast failure with clear error messages
- **Resource Efficiency**: Prevents wasted experiment time
- **Debugging**: Clear identification of configuration issues
- **Professional Quality**: Expected behavior in production systems

**Implementation Plan**:

### Phase 1: CLI Model Validation
- **Model Registry Integration**: Load `models.yaml` in CLI
- **Pre-flight Validation**: Check all specified models before experiment start
- **Clear Error Messages**: Specific feedback on invalid models
- **Provider Validation**: Check API key availability for external providers

### Phase 2: Orchestrator Model Validation
- **Phase-Specific Validation**: Validate models before each phase execution
- **Fallback Logic**: Graceful degradation when models unavailable
- **Configuration Validation**: Ensure model compatibility with phase requirements

### Phase 3: Agent-Level Validation
- **Model Availability Checking**: Verify model access before LLM calls
- **Provider Health Checks**: Validate API endpoints and authentication
- **Dynamic Fallback**: Automatic model switching on validation failure

**Technical Requirements**:
- **Model Registry Integration**: CLI access to `models.yaml`
- **Validation Pipeline**: Multi-level validation chain
- **Error Handling**: Consistent error messages across layers
- **Fallback Mechanisms**: Graceful degradation strategies

**Risk Assessment**:
- **Low Risk**: CLI validation (simple file parsing)
- **Medium Risk**: Orchestrator integration (coordination complexity)
- **Low Risk**: User experience improvement (clear benefits)

**Estimated Effort**: 3-5 days for comprehensive implementation

**Timeline**: Post-v1.0 release, when user experience becomes priority

**Reference**: Current issue with `deepseek/deepseek-coder-33b-instruct` vs `openrouter/deepseek/deepseek-chat-v3.1`
