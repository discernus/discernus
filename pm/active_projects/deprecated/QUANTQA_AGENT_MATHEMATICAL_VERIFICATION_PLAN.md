# QuantQAAgent: Mathematical Verification Enhancement Plan

**Date**: July 28, 2025  
**Context**: Trust-but-verify architecture for mathematical reliability in computational social science
**Status**: Design Phase

## Problem Statement

The current Discernus platform lacks mathematical verification capabilities, creating potential reliability issues:

1. **Stage 1 Math Risk**: Analysis agents perform framework calculations (tension scores, indices) that can contain errors
2. **Stage 2 Math Risk**: Synthesis agents perform statistical analysis that can be mathematically incorrect
3. **Error Propagation**: Calculation errors in Stage 1 poison all downstream statistical analysis
4. **Trust Gap**: No systematic way to verify mathematical claims in academic reports

## Solution: QuantQAAgent Architecture

Introduce a specialized **Quantitative Quality Assurance Agent** that provides mathematical verification at critical pipeline stages using a "trust but verify" approach.

### Core Principles

1. **Specialized Intelligence**: LLM trained specifically for mathematical verification
2. **Framework Agnostic**: Works with any v5.0 framework through dynamic prompt construction
3. **Batch Efficiency**: Verifies entire corpus calculations in single LLM calls
4. **Error Correction**: Fixes deterministic calculation errors automatically
5. **Transparency**: Documents verification results for academic integrity

## Architecture Design

### Two-Stage Verification Model

```
Stage 1: Analysis Verification (Deterministic Math)
AnalysisAgent → Aggregated CSV → QuantQAAgent → Verified CSV → Storage

Stage 2: Synthesis Verification (Statistical Claims)  
SynthesisAgent → Statistical Report → QuantQAAgent → Verified Report → Final Output
```

### Framework-Agnostic Implementation

**Dynamic Prompt Construction**:
```python
def build_verification_prompt(framework_config, csv_data):
    calculation_spec = framework_config["calculation_spec"]
    
    prompt = f"""
    You are verifying calculations for {framework_config["display_name"]}.
    
    Required calculations to verify:
    """
    
    for calc_name, formula in calculation_spec.items():
        prompt += f"- {calc_name}: {formula}\n"
    
    prompt += f"\nCSV Data:\n{csv_data}\n\nReturn corrected CSV if errors found."
    return prompt
```

**Framework Portability**:
- **CAF**: Verifies tension calculations and MC-SCI
- **PDAF**: Verifies dimensional aggregations and indices  
- **CFF**: Verifies cohesion metrics and calculations
- **Any v5.0 Framework**: Uses framework's `calculation_spec` for verification rules

## Integration with Current Pipeline

### Current Flow
```
AnalysisAgent → CSV Aggregation → MinIO Storage → SynthesisAgent → Final Report
```

### Enhanced Flow  
```
AnalysisAgent → CSV Aggregation → QuantQAAgent (Stage 1) → MinIO Storage → SynthesisAgent → QuantQAAgent (Stage 2) → Final Report
```

### Implementation Details

**Stage 1 Verification**:
```python
# After analysis aggregation completes
scores_csv_hash = analysis_complete_hash
verified_csv_hash = quant_qa_agent.verify_stage1_calculations(
    csv_hash=scores_csv_hash,
    framework_config=framework_json,
    verification_mode="fix_errors"  # Auto-correct deterministic math
)
```

**Stage 2 Verification**:
```python
# After synthesis completes
synthesis_report = synthesis_agent_output
verified_report = quant_qa_agent.verify_stage2_statistics(
    report=synthesis_report,
    csv_data_hashes=[scores_hash, evidence_hash],
    verification_mode="document_anomalies"  # Note but don't auto-fix
)
```

## Error Handling Strategy

### Stage 1 (Deterministic Calculations)
- **Approach**: Auto-correction
- **Rationale**: Mathematical formulas have objective correct answers
- **Example**: `dignity_tribalism_tension = |0.7 - 0.3| = 0.4` (not 0.6)
- **Process**: Fix error, update CSV, log correction

### Stage 2 (Statistical Analysis)
- **Approach**: Document anomalies  
- **Rationale**: Statistical interpretations can have legitimate variation
- **Example**: "⚠️ Correlation calculation verification flagged 2/15 statistics"
- **Process**: Include verification confidence in final report

## Efficiency Considerations

### Batch Processing
- **Instead of**: 47 individual verification calls per document
- **We use**: 1 batch verification call per complete aggregated CSV
- **Prompt**: "Verify all calculations in this 47-row CSV using these formulas..."

### Cost Management
- **Stage 1**: Single verification call per experiment (minimal cost)
- **Stage 2**: Single verification call per synthesis (minimal cost)
- **Total overhead**: ~2 additional LLM calls per experiment

## Implementation Phases

### Phase 1: Stage 1 Verification (4 weeks)
**Goal**: Mathematical firewall for analysis calculations

**Deliverables**:
- QuantQAAgent base implementation
- Framework-agnostic prompt construction
- Integration with CSV aggregation pipeline
- Auto-correction for deterministic math errors

**Success Metrics**:
- 100% detection of planted mathematical errors
- Zero false positives on correct calculations
- Framework portability across CAF, PDAF, CFF

### Phase 2: Stage 2 Verification (3 weeks)  
**Goal**: Statistical verification for synthesis reports

**Deliverables**:
- Statistical verification capabilities
- Anomaly detection and documentation
- Integration with synthesis pipeline
- Verification confidence reporting

**Success Metrics**:
- Detection of statistical calculation errors
- Clear documentation of verification results
- No false alarms on valid statistical interpretations

### Phase 3: Enhanced Reporting (2 weeks)
**Goal**: Academic-grade verification transparency

**Deliverables**:
- Verification audit trails
- Mathematical confidence indicators
- Enhanced error reporting
- Documentation for academic peer review

**Success Metrics**:
- Complete audit trail of all mathematical verification
- Clear confidence indicators in final reports
- Peer-reviewable verification documentation

## Technical Requirements

### Agent Implementation
```python
class QuantQAAgent:
    def verify_stage1_calculations(self, csv_hash, framework_config, verification_mode):
        """Verify deterministic framework calculations"""
        
    def verify_stage2_statistics(self, report, csv_data_hashes, verification_mode):
        """Verify statistical claims in synthesis reports"""
        
    def build_framework_prompt(self, framework_config, verification_type):
        """Dynamically construct verification prompts from framework specs"""
```

### Infrastructure Integration
- **Storage**: MinIO integration for CSV verification and rewriting
- **Orchestration**: Integration with ThinOrchestrator workflow
- **Audit**: Complete logging of all verification actions
- **Security**: Verification within experiment security boundaries

## Success Criteria

### Reliability Metrics
- **Mathematical Accuracy**: 100% detection of calculation errors
- **Framework Portability**: Works with all v5.0 frameworks without modification
- **Efficiency**: <5% overhead on total experiment runtime

### Trust Metrics  
- **Verification Coverage**: All mathematical claims verified and documented
- **Error Correction**: Stage 1 errors automatically corrected
- **Transparency**: Complete audit trail of verification actions

### Academic Integrity
- **Peer Review Ready**: Verification methodology suitable for academic review
- **Reproducibility**: Same verification results across multiple runs
- **Documentation**: Complete mathematical methodology documentation

## Future Enhancements

### Advanced Statistical Verification
- Cross-validation of complex statistical models
- Bayesian confidence intervals for verification
- Integration with external statistical validation libraries

### Machine Learning Verification
- Training specialized models for mathematical error detection
- Pattern recognition for common calculation mistakes
- Automated verification rule learning from framework specifications

## Conclusion

The QuantQAAgent represents a critical enhancement to Discernus platform reliability, providing systematic mathematical verification while maintaining THIN architecture principles. By implementing trust-but-verify at both calculation and statistical levels, we ensure the mathematical integrity required for serious computational social science research.

The framework-agnostic design ensures this enhancement benefits all current and future analytical frameworks, while the batch processing approach maintains system efficiency and cost-effectiveness.

**Next Steps**: Create GitHub epic and implementation issues, then return to experiment specification v3 enhancement planning.