# Results Format Example: Single-LLM Pilot

This example shows what the new bias-focused results format looks like compared to the current synthesis-focused approach.

## Current Results Format Problems

### Typical JSONL Chronolog (3,000+ lines)
```jsonl
{"timestamp": "2025-01-13T10:15:23Z", "speaker": "analysis_agent_1", "message": "I will now analyze this speech using the PDAF framework..."}
{"timestamp": "2025-01-13T10:16:45Z", "speaker": "analysis_agent_1", "message": "The people-elite framing appears in multiple sections..."}
{"timestamp": "2025-01-13T10:17:32Z", "speaker": "synthesis_agent", "message": "Aggregating results from 4 analysis agents..."}
{"timestamp": "2025-01-13T10:18:15Z", "speaker": "moderator_agent", "message": "I notice disagreement on anchor 3 scores..."}
{"timestamp": "2025-01-13T10:19:01Z", "speaker": "referee_agent", "message": "After reviewing the evidence..."}
```
**Problem**: Process documentation, not research findings.

### Typical Markdown Summary (synthesis-focused)
```markdown
# Analysis Results

## Synthesis Discussion
The synthesis agent identified outliers in anchor scoring, leading to moderator discussion about methodological approaches. The referee agent resolved disagreements through careful examination of textual evidence...

## Final Scores
After adversarial review: Anchor 1: 1.2, Anchor 2: 0.8...
```
**Problem**: Focuses on agent process, not bias analysis.

## New Results Format

### 1. `bias_detection_report.md` (Human-readable findings)
```markdown
# Bias Detection Report: Single-LLM Pilot

## Executive Summary
**Bias Detected**: Yes - systematic scoring differences based on speaker identity  
**Bias Magnitude**: 0.4-0.7 point differences on 2.0 scale  
**Cross-Linguistic Mitigation**: Effective - Esperanto reduces bias by 73%  
**Ready for Full Study**: Yes ✅

## Bias Analysis by Speech

### Romney Speech (Conservative Dignity)
- **Original condition**: People-Elite framing = 1.5, Crisis urgency = 1.2  
- **Sanitized condition**: People-Elite framing = 1.1, Crisis urgency = 1.2  
- **Esperanto condition**: People-Elite framing = 1.0, Crisis urgency = 1.1  
- **Bias magnitude**: 0.4 points (27% variation)

### McCain Speech (Conservative Dignity)
- **Original condition**: People-Elite framing = 1.3, Crisis urgency = 0.9  
- **Sanitized condition**: People-Elite framing = 1.0, Crisis urgency = 0.9  
- **Esperanto condition**: People-Elite framing = 0.9, Crisis urgency = 0.8  
- **Bias magnitude**: 0.3 points (23% variation)

## Statistical Validation
- **Bias effect size (Cohen's d)**: 0.65 (medium effect)
- **Statistical significance**: p < 0.01
- **Cross-linguistic correlation**: r = 0.84 (high validity preservation)

## Methodology Assessment
✅ **Protocol effective**: Bias consistently detected across speeches  
✅ **Cross-linguistic mitigation**: Esperanto reduces bias while maintaining analytical validity  
✅ **Framework performance**: PDAF v1.1 works correctly across language conditions  
✅ **Scalability confirmed**: Ready for 6-model full study

## Recommendation
**Proceed to full study** with confidence in methodology.
```

### 2. `raw_pdaf_scores.json` (Data for statistical analysis)
```json
{
  "romney_speech": {
    "original": {
      "model": "claude-3.5-sonnet",
      "anchor_1_people_elite": 1.5,
      "anchor_2_crisis_urgency": 1.2,
      "anchor_3_manichaean": 1.0,
      "anchor_4_crisis_temporality": 0.8,
      "anchor_5_popular_sovereignty": 1.3,
      "anchor_6_authenticity": 1.1,
      "anchor_7_homogeneous_people": 0.7,
      "anchor_8_common_will": 1.0,
      "anchor_9_elite_corruption": 1.4,
      "anchor_10_economic_direction": 0.2
    },
    "sanitized_english": {
      "model": "claude-3.5-sonnet",
      "anchor_1_people_elite": 1.1,
      "anchor_2_crisis_urgency": 1.2,
      "anchor_3_manichaean": 0.9,
      "anchor_4_crisis_temporality": 0.8,
      "anchor_5_popular_sovereignty": 1.2,
      "anchor_6_authenticity": 0.8,
      "anchor_7_homogeneous_people": 0.7,
      "anchor_8_common_will": 1.0,
      "anchor_9_elite_corruption": 1.2,
      "anchor_10_economic_direction": 0.2
    },
    "sanitized_esperanto": {
      "model": "claude-3.5-sonnet",
      "anchor_1_people_elite": 1.0,
      "anchor_2_crisis_urgency": 1.1,
      "anchor_3_manichaean": 0.9,
      "anchor_4_crisis_temporality": 0.7,
      "anchor_5_popular_sovereignty": 1.1,
      "anchor_6_authenticity": 0.8,
      "anchor_7_homogeneous_people": 0.6,
      "anchor_8_common_will": 0.9,
      "anchor_9_elite_corruption": 1.1,
      "anchor_10_economic_direction": 0.1
    }
  }
}
```

### 3. `statistical_analysis.md` (Academic-quality analysis)
```markdown
# Statistical Analysis: Bias Effect Sizes

## Bias Magnitude by Anchor

| Anchor | Original Mean | Sanitized Mean | Bias Effect | Cohen's d | p-value |
|--------|---------------|----------------|-------------|-----------|---------|
| People-Elite | 1.40 | 1.05 | 0.35 | 0.67 | <0.01 |
| Crisis Urgency | 1.05 | 1.05 | 0.00 | 0.00 | 0.98 |
| Authenticity | 1.15 | 0.80 | 0.35 | 0.71 | <0.01 |
| Elite Corruption | 1.30 | 1.15 | 0.15 | 0.32 | 0.04 |

## Cross-Linguistic Correlation Analysis

**Sanitized English vs Esperanto**: r = 0.84, p < 0.001  
**95% Confidence Interval**: [0.72, 0.91]  
**Interpretation**: High correlation indicates framework validity preserved across languages

## Effect Size Interpretation
- **Medium bias effects** detected for identity-sensitive anchors
- **No bias effects** for content-dependent anchors (crisis urgency)
- **Consistent bias direction** across speeches
```

## Key Differences

### Old Format → New Format

**Focus**: Process documentation → Research findings  
**Length**: 3,000+ lines → 3 focused files  
**Audience**: System debugging → Academic publication  
**Content**: Agent conversations → Statistical analysis  
**Utility**: Hard to parse → Immediately actionable  

### Academic Impact

**Old**: "We ran some analysis and agents discussed things"  
**New**: "We detected systematic bias with 0.65 effect size and validated cross-linguistic mitigation with r=0.84 correlation"

The new format directly supports the academic objectives outlined in the strategic overview, providing publication-ready findings rather than process documentation. 