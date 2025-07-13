# Single-LLM Pilot Results Structure

This directory contains bias isolation methodology validation results.

## Expected Files

### 1. `bias_detection_report.md`
**Purpose**: Human-readable bias analysis findings
**Content**:
- Bias magnitude measurements (original vs sanitized conditions)
- Cross-linguistic effectiveness (sanitized vs Esperanto conditions)
- Statistical significance testing
- Go/no-go decision for full study

### 2. `raw_pdaf_scores.json`
**Purpose**: Complete PDAF anchor scores across all conditions
**Content**:
```json
{
  "romney_speech": {
    "original": {
      "model": "claude-3.5-sonnet",
      "anchor_1_people_elite": 1.5,
      "anchor_2_crisis_urgency": 1.2,
      // ... all 10 anchors
    },
    "sanitized_english": {
      "model": "claude-3.5-sonnet", 
      "anchor_1_people_elite": 1.1,
      "anchor_2_crisis_urgency": 1.2,
      // ... all 10 anchors
    },
    "sanitized_esperanto": {
      "model": "claude-3.5-sonnet",
      "anchor_1_people_elite": 1.0,
      "anchor_2_crisis_urgency": 1.1,
      // ... all 10 anchors
    }
  }
  // ... for all 4 speeches
}
```

### 3. `statistical_analysis.md`
**Purpose**: Bias magnitude calculations and correlations
**Content**:
- Bias effect sizes (Cohen's d) for each anchor
- Correlation analysis (sanitized English vs Esperanto)
- Confidence intervals and significance tests
- Inter-condition variance analysis

### 4. `methodology_validation.md`
**Purpose**: Academic assessment of bias isolation protocol
**Content**:
- Protocol effectiveness assessment
- Cross-linguistic mitigation validation
- Framework performance across languages
- Recommendations for full study

### 5. `pilot_summary.json`
**Purpose**: Machine-readable summary for full study planning
**Content**:
```json
{
  "bias_detected": true,
  "bias_magnitude_range": [0.2, 0.8],
  "cross_linguistic_correlation": 0.85,
  "protocol_effectiveness": "validated",
  "ready_for_full_study": true,
  "recommended_models": ["claude-3.5-sonnet", "gpt-4o"],
  "estimated_full_study_cost": 28.50
}
```

## Success Criteria

**Bias Detection Validation**:
- [ ] Detectable score differences between original and sanitized conditions (≥ 0.3 on 2.0 scale for ≥ 3 anchors)
- [ ] Statistical significance (p < 0.05) for bias effects
- [ ] Consistent bias direction across speeches

**Cross-Linguistic Mitigation**:
- [ ] High correlation between sanitized English and Esperanto (r ≥ 0.8)
- [ ] Reduced bias magnitude in Esperanto condition
- [ ] Framework validity maintained across languages

**Methodology Validation**:
- [ ] Raw score collection works correctly (no synthesis contamination)
- [ ] Statistical pipeline generates meaningful measurements
- [ ] Protocol scalable to full study

**Decision Point**: If all criteria met → proceed to full study. If bias not detected → investigate methodology. If cross-linguistic mitigation fails → revise approach. 