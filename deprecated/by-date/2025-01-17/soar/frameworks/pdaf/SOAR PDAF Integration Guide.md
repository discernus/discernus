# SOAR PDAF Integration Guide

## Populist Discourse Analysis Framework Implementation for SOAR v2.0

**Date**: July 10, 2025  
**Status**: Implementation Guide  
**Framework**: PDAF v1.0  
**SOAR Version**: 2.0+  
**Purpose**: Specialized populist discourse analysis through ensemble validation

-----

## PDAF Framework Registration

### Framework Metadata

```json
{
  "framework_registration": {
    "name": "Populist Discourse Analysis Framework",
    "acronym": "PDAF",
    "version": "1.0",
    "framework_type": "political_discourse_measurement",
    "analysis_scope": "Populist communication pattern detection and measurement",
    "academic_domain": "political_science",
    "context_tokens_required": 176000,
    "supported_languages": ["en"],
    "citation": "Political Communication Research Lab, 2025",
    
    "framework_characteristics": {
      "measurement_approach": "nine_anchor_orthogonal_with_competitive_dynamics",
      "normative_approach": "graduated_layering",
      "calibration_method": "extreme_composite_reference_texts",
      "validation_protocol": "cross_ideological_boundary_testing"
    }
  }
}
```

### Analysis Dimensions (9 Anchors)

```json
{
  "analysis_dimensions": [
    {
      "dimension_id": "manichaean_people_elite",
      "name": "Manichaean People-Elite Framing",
      "description": "Pure people vs. corrupt elite moral dichotomy",
      "cluster": "core_populist",
      "measurement_type": "bipolar",
      "scale": {
        "range": [0.0, 2.0],
        "poles": {
          "positive": "Pure people virtue vs. corrupt elite moral framing",
          "negative": "Pluralist democratic legitimacy acceptance"
        }
      },
      "divergence_threshold": 0.3,
      "importance_weight": 0.35,
      "competition_weight": 0.8
    },
    {
      "dimension_id": "crisis_restoration",
      "name": "Crisis-Restoration Temporal Narrative",
      "description": "Decline-crisis-redemption temporal structuring",
      "cluster": "core_populist",
      "measurement_type": "bipolar",
      "scale": {
        "range": [0.0, 2.0],
        "poles": {
          "positive": "Crisis decline with restoration possibility",
          "negative": "Institutional continuity and gradual improvement"
        }
      },
      "divergence_threshold": 0.3,
      "importance_weight": 0.30,
      "competition_weight": 0.6
    },
    {
      "dimension_id": "popular_sovereignty",
      "name": "Popular Sovereignty Claims",
      "description": "Direct people's will as ultimate political authority",
      "cluster": "core_populist",
      "measurement_type": "bipolar",
      "scale": {
        "range": [0.0, 2.0],
        "poles": {
          "positive": "Direct popular will supremacy over institutional mediation",
          "negative": "Constitutional constraint and institutional mediation"
        }
      },
      "divergence_threshold": 0.3,
      "importance_weight": 0.20,
      "competition_weight": 0.7
    },
    {
      "dimension_id": "anti_pluralist",
      "name": "Anti-Pluralist Exclusion",
      "description": "Rejection of legitimate opposition and institutional constraints",
      "cluster": "core_populist",
      "measurement_type": "bipolar",
      "scale": {
        "range": [0.0, 2.0],
        "poles": {
          "positive": "Opposition illegitimacy and institutional constraint rejection",
          "negative": "Democratic pluralism and opposition legitimacy"
        }
      },
      "divergence_threshold": 0.3,
      "importance_weight": 0.15,
      "competition_weight": 0.9
    },
    {
      "dimension_id": "elite_conspiracy",
      "name": "Elite Conspiracy/Systemic Corruption",
      "description": "Elite coordination against people's interests",
      "cluster": "mechanism",
      "measurement_type": "bipolar",
      "scale": {
        "range": [0.0, 2.0],
        "poles": {
          "positive": "Systematic elite conspiracy and coordination",
          "negative": "Institutional legitimacy and normal politics"
        }
      },
      "divergence_threshold": 0.3,
      "importance_weight": 0.12,
      "competition_weight": 0.5
    },
    {
      "dimension_id": "authenticity",
      "name": "Authenticity vs. Political Class",
      "description": "Genuine representation vs. professional politician artifice",
      "cluster": "mechanism",
      "measurement_type": "bipolar",
      "scale": {
        "range": [0.0, 2.0],
        "poles": {
          "positive": "Authentic representation through personal experience",
          "negative": "Professional political competence and expertise"
        }
      },
      "divergence_threshold": 0.3,
      "importance_weight": 0.12,
      "competition_weight": 0.9
    },
    {
      "dimension_id": "homogeneous_people",
      "name": "Homogeneous People Construction",
      "description": "Unified people identity transcending internal divisions",
      "cluster": "mechanism",
      "measurement_type": "bipolar",
      "scale": {
        "range": [0.0, 2.0],
        "poles": {
          "positive": "Natural unity with artificial divisions",
          "negative": "Legitimate diversity and democratic pluralism"
        }
      },
      "divergence_threshold": 0.3,
      "importance_weight": 0.11,
      "competition_weight": 0.7
    },
    {
      "dimension_id": "nationalist_exclusion",
      "name": "Nationalist Exclusion",
      "description": "Cultural/ethnic homogeneity and external threat emphasis",
      "cluster": "boundary",
      "measurement_type": "bipolar",
      "scale": {
        "range": [0.0, 2.0],
        "poles": {
          "positive": "Cultural homogeneity and exclusion emphasis",
          "negative": "Multicultural inclusion and diversity celebration"
        }
      },
      "divergence_threshold": 0.3,
      "importance_weight": 0.08,
      "competition_weight": 0.4
    },
    {
      "dimension_id": "economic_redistributive",
      "name": "Economic Redistributive Appeals",
      "description": "Elite wealth redistribution and economic justice focus",
      "cluster": "boundary",
      "measurement_type": "bipolar",
      "scale": {
        "range": [0.0, 2.0],
        "poles": {
          "positive": "Wealth redistribution and class struggle emphasis",
          "negative": "Market economy defense and entrepreneurship"
        }
      },
      "divergence_threshold": 0.3,
      "importance_weight": 0.07,
      "competition_weight": 0.3
    }
  ]
}
```

### Normative Layers

```json
{
  "normative_layers": [
    {
      "layer_id": "descriptive",
      "name": "Descriptive Populist Communication Assessment",
      "normative_status": "neutral",
      "description": "Neutral populist pattern identification with basic PDI measurement",
      "dimensions_included": ["manichaean_people_elite", "crisis_restoration", "popular_sovereignty", "anti_pluralist"],
      "composite_metrics": ["layer_1_pdi"]
    },
    {
      "layer_id": "engagement",
      "name": "Democratic Engagement Motivation Analysis",
      "normative_status": "implicit",
      "description": "Implicit democratic participation assumptions with intermediate PDI",
      "dimensions_included": ["manichaean_people_elite", "crisis_restoration", "popular_sovereignty", "anti_pluralist", "elite_conspiracy", "authenticity", "homogeneous_people"],
      "composite_metrics": ["layer_2_pdi"]
    },
    {
      "layer_id": "health",
      "name": "Democratic System Health Evaluation",
      "normative_status": "explicit",
      "description": "Explicit democratic consequences assessment with comprehensive PDI",
      "dimensions_included": ["manichaean_people_elite", "crisis_restoration", "popular_sovereignty", "anti_pluralist", "elite_conspiracy", "authenticity", "homogeneous_people", "nationalist_exclusion", "economic_redistributive"],
      "composite_metrics": ["layer_3_pdi"],
      "institutional_modifier": true
    }
  ]
}
```

### Composite Metrics

```json
{
  "composite_metrics": [
    {
      "metric_id": "layer_1_pdi",
      "name": "Layer 1 Populist Discourse Index",
      "description": "Basic populist communication measurement",
      "formula": "0.35(Manichaean) + 0.30(Crisis_Restoration) + 0.20(Popular_Sovereignty) + 0.15(Anti_Pluralist)",
      "applicable_layers": ["descriptive"],
      "scale": {
        "range": [0.0, 2.0],
        "interpretation": {
          "high_populist": [1.4, 2.0],
          "moderate_populist": [0.8, 1.4],
          "neutral_contested": [0.4, 0.8],
          "low_populist": [0.0, 0.4]
        }
      }
    },
    {
      "metric_id": "layer_2_pdi",
      "name": "Layer 2 Populist Discourse Index",
      "description": "Democratic engagement populist measurement",
      "formula": "0.20(Manichaean) + 0.18(Crisis_Restoration) + 0.15(Popular_Sovereignty) + 0.12(Anti_Pluralist) + 0.12(Elite_Conspiracy) + 0.12(Authenticity) + 0.11(Homogeneous_People)",
      "applicable_layers": ["engagement"],
      "scale": {
        "range": [0.0, 2.0],
        "interpretation": {
          "high_populist": [1.4, 2.0],
          "moderate_populist": [0.8, 1.4],
          "neutral_contested": [0.4, 0.8],
          "low_populist": [0.0, 0.4]
        }
      }
    },
    {
      "metric_id": "layer_3_pdi",
      "name": "Layer 3 Populist Discourse Index",
      "description": "Democratic health populist measurement with institutional modifier",
      "formula": "PDI_Layer2 + 0.08(Nationalist_Exclusion) + 0.07(Economic_Redistributive) + 0.15(Institutional_Respect - Institutional_Rejection)",
      "applicable_layers": ["health"],
      "scale": {
        "range": [0.0, 2.0],
        "interpretation": {
          "high_populist": [1.4, 2.0],
          "moderate_populist": [0.8, 1.4],
          "neutral_contested": [0.4, 0.8],
          "low_populist": [0.0, 0.4]
        }
      },
      "competitive_dynamics": true
    }
  ]
}
```

### Competitive Dynamics Integration

```json
{
  "competitive_dynamics": {
    "description": "Mathematical modeling of multi-actor populist competition effects",
    "formula": "Σ(Other_Actor_Scores) × Anchor_Competition_Weight × Temporal_Decay",
    "temporal_decay": "e^(-λt) where λ = 0.1 (weekly decay constant)",
    "anchor_competition_weights": {
      "manichaean_people_elite": 0.8,
      "crisis_restoration": 0.6,
      "popular_sovereignty": 0.7,
      "anti_pluralist": 0.9,
      "elite_conspiracy": 0.5,
      "authenticity": 0.9,
      "homogeneous_people": 0.7,
      "nationalist_exclusion": 0.4,
      "economic_redistributive": 0.3
    }
  }
}
```

-----

## PDAF-Specific Agent Configurations

### Framework Analysis Agent Template

```markdown
You are a SOAR Framework Analysis Agent specialized in the Populist Discourse Analysis Framework (PDAF) v1.0.

PDAF ANALYSIS PROTOCOL:
- Apply complete PDAF v1.0 specification with all 9 populist discourse anchors
- Use extensive calibration packet references for cross-ideological validity
- Generate anchor scores for {{LAYER_ID}} layer with evidence documentation
- Calculate appropriate PDI using layer-specific formula with competitive dynamics

POPULIST ANCHOR ANALYSIS:
- Core Populist Cluster (Parallel): Manichaean, Crisis-Restoration, Popular Sovereignty, Anti-Pluralist
- Mechanism Cluster (Parallel): Elite Conspiracy, Authenticity, Homogeneous People
- Boundary Cluster (Sequential): Nationalist Exclusion, Economic Redistributive
- Cross-ideological validation required for all anchors

EVIDENCE REQUIREMENTS:
- Utilize calibration packet references for score validation (extreme composite texts)
- Provide specific textual citations with exact position markers
- Document populist patterns with cross-ideological validity testing
- Validate boundary distinctions against nationalism and economic appeals

PDAF CALIBRATION STANDARDS:
- Apply extreme composite reference calibration for all anchors
- Score within populist range [0.0-2.0] with precise calibration alignment
- Calculate PDI using layer-appropriate mathematical formula
- Ensure boundary distinction clarity (populist vs. nationalist vs. economic)
- Apply competitive dynamics adjustments if multiple actors detected

COMPETITIVE DYNAMICS:
- Detect multiple populist actors in text for competition calculations
- Apply anchor-specific competition weights and temporal decay functions
- Adjust final PDI scores based on zero-sum populist competition effects

OUTPUT FORMAT: PDAF-specific JSON schema with anchor scores, PDI calculation, competitive dynamics, and boundary validation.
```

### PDAF Moderator Configuration

```python
def detect_pdaf_divergences(ensemble_results, pdaf_config):
    """PDAF-specific divergence detection with populist anchor priorities"""
    divergences = []
    
    # PDAF uses 0.3 threshold for populist anchors
    for anchor in pdaf_config.get_analysis_dimensions():
        scores = [result.anchors[anchor.id].score for result in ensemble_results]
        
        if max(scores) - min(scores) > 0.3:  # PDAF threshold
            # Prioritize core populist anchors with higher weights
            priority = anchor.importance_weight * (max(scores) - min(scores))
            
            # Extra priority for boundary anchors (critical for framework validity)
            if anchor.cluster == "boundary":
                priority *= 1.5  # Boundary distinction critical
            
            divergences.append({
                "anchor": anchor.id,
                "score_range": [min(scores), max(scores)],
                "models": [(model, score) for model, score in zip(model_ids, scores)],
                "priority": priority,
                "populist_context": anchor.calibration_references,
                "boundary_criticality": anchor.cluster == "boundary",
                "competitive_impact": calculate_competitive_impact(anchor, scores)
            })
    
    return divergences

def calculate_competitive_impact(anchor, scores):
    """Calculate impact of divergent scores on competitive dynamics"""
    competition_weight = anchor.competition_weight
    score_variance = abs(max(scores) - min(scores))
    return competition_weight * score_variance

def orchestrate_pdaf_debate(divergences):
    """PDAF-specific debate orchestration with cluster considerations"""
    # Prioritize core populist cluster debates (highest impact)
    core_debates = [d for d in divergences if d["anchor"] in CORE_POPULIST_ANCHORS]
    boundary_debates = [d for d in divergences if d["boundary_criticality"]]
    mechanism_debates = [d for d in divergences if d["anchor"] in MECHANISM_ANCHORS]
    
    # Sequential debate order: Core → Boundary → Mechanism
    debate_queue = sorted(core_debates, key=lambda x: x["priority"], reverse=True)
    debate_queue.extend(sorted(boundary_debates, key=lambda x: x["priority"], reverse=True))
    debate_queue.extend(sorted(mechanism_debates, key=lambda x: x["priority"], reverse=True))
    
    return debate_queue
```

### PDAF Referee Specialization

```markdown
You are the SOAR Referee Agent specialized in PDAF v1.0 populist discourse arbitration.

PDAF ARBITRATION PROTOCOL:
- Evaluate competing evidence chains for populist markers within PDAF methodology
- Assess calibration reference alignment using PDAF extreme composite texts
- Judge boundary distinctions crucial to PDAF validity (populist vs. nationalist vs. economic)
- Select argument with strongest populist pattern evidence according to PDAF standards

PDAF-SPECIFIC EVALUATION:
- Apply PDAF's calibration packet hierarchy for reference alignment assessment
- Use PDAF extreme composite texts for score validation and consistency
- Enforce PDAF boundary distinction tests (critical for framework validity)
- Respect PDAF normative layer constraints and anchor clustering logic

POPULIST EVIDENCE CRITERIA:
1. Calibration Alignment: Consistency with PDAF extreme composite reference texts
2. Cross-Ideological Validity: Populist patterns regardless of left/right ideology
3. Boundary Distinction: Clear separation from nationalist and economic content
4. Pattern Recognition: Systematic populist discourse markers and semantic patterns
5. Competitive Context: Evidence strength affects multi-actor competition calculations

PDAF BOUNDARY VALIDATION:
- Populist vs. Nationalist: People/elite moral dichotomy vs. cultural exclusion
- Populist vs. Economic: Anti-elite sentiment vs. redistributive policy mechanisms
- Core vs. Mechanism: Primary populist patterns vs. populist strategic approaches
- Layer Consistency: Anchor inclusion appropriate for normative layer analysis

COMPETITIVE DYNAMICS CONSIDERATIONS:
- Consider how divergent anchor scores affect competitive adjustment calculations
- Evaluate evidence quality impact on multi-actor populist effectiveness modeling
- Assess anchor competition weights in context of zero-sum populist dynamics
```

### PDAF Quality Assurance Protocols

```markdown
You are the SOAR Quality Assurance Agent specialized in PDAF v1.0 populist discourse validation.

PDAF VALIDATION PROTOCOL:
- Cross-check referee decisions against PDAF v1.0 populist analysis standards
- Monitor for systematic biases in populist anchor scoring across models and ideologies
- Validate PDI calculations using layer-appropriate formulas with competitive dynamics
- Generate PDAF-specific confidence metrics for populist discourse measurement

PDAF POPULIST CONSISTENCY MONITORING:
- Verify adherence to PDAF calibration packet references and boundary tests
- Check anchor score consistency with PDAF cross-ideological validity principles
- Validate PDI calculations per PDAF mathematical formulas across layers
- Monitor boundary distinction compliance (populist vs. nationalist vs. economic)

IDEOLOGICAL BIAS DETECTION:
- Track model performance patterns across left-populist vs. right-populist texts
- Identify systematic over/under-scoring relative to PDAF calibration standards
- Flag inconsistent application of cross-ideological validity requirements
- Monitor for systematic deviation from PDAF boundary distinction protocols

PDAF QUALITY METRICS:
- Calculate ensemble agreement levels using PDAF 0.3 divergence thresholds
- Assess populist evidence strength using PDAF calibration reference standards
- Generate confidence intervals for PDI reliability across normative layers
- Document populist methodology transparency per PDAF audit requirements

COMPETITIVE DYNAMICS VALIDATION:
- Verify mathematical accuracy of multi-actor competition adjustments
- Cross-check temporal decay functions and anchor-specific competition weights
- Validate competitive context detection and effectiveness calculations
- Monitor competitive dynamics impact on final PDI interpretations

BOUNDARY DISTINCTION QUALITY:
- Systematic validation of populist vs. nationalist distinction accuracy
- Cross-check populist vs. economic redistributive boundary maintenance
- Verify core populist vs. mechanism anchor clustering consistency
- Monitor calibration drift in boundary distinction protocols
```

-----

## PDAF Calibration Integration

### Extreme Composite Reference System

```json
{
  "calibration_system": {
    "description": "Extreme composite reference texts for systematic populist measurement",
    "methodology": "Authentic discourse synthesis across ideological boundaries",
    "total_size": "135K tokens across 9 anchors",
    
    "reference_categories": [
      {
        "category": "pure_left_populist",
        "source_patterns": "Sanders/Warren economic populism",
        "emphasis": "Billionaire class critique, working family representation"
      },
      {
        "category": "pure_right_populist", 
        "source_patterns": "Trump/MAGA cultural populism",
        "emphasis": "Political establishment critique, real Americans identity"
      },
      {
        "category": "nationalist_populist",
        "source_patterns": "Orbán/international nationalist rhetoric",
        "emphasis": "Cultural homogeneity, globalist elite opposition"
      },
      {
        "category": "pluralist_democratic",
        "source_patterns": "Institutional democracy rhetoric",
        "emphasis": "Constitutional process, expert governance, institutional respect"
      },
      {
        "category": "anti_populist",
        "source_patterns": "Explicit populism rejection rhetoric",
        "emphasis": "Populist oversimplification critique, institutional defense"
      }
    ]
  }
}
```

### Anchor-Specific Calibration Examples

```json
{
  "manichaean_calibration": {
    "anchor_id": "manichaean_people_elite",
    "reference_texts": [
      {
        "reference_id": "pure_left_populist_manichaean",
        "score": 2.0,
        "text_sample": "We are experiencing a government of the billionaires, by the billionaires, and for the billionaires. While working families struggle to put food on the table, the richest one percent live in their own fantasy world.",
        "marker_analysis": {
          "people_markers": ["working families", "all of us"],
          "elite_markers": ["billionaire class", "oligarchy"],
          "moral_dichotomy": ["democracy vs. oligarchy", "struggle vs. fantasy world"],
          "zero_sum_framing": ["you cannot have it all", "power competition"]
        }
      },
      {
        "reference_id": "pure_right_populist_manichaean",
        "score": 2.0,
        "text_sample": "This election will decide whether we are ruled by the people, or by the politicians. The special interests totally own her, and that will never change. I'm with you: the American people.",
        "marker_analysis": {
          "people_markers": ["the people", "American people", "All Americans"],
          "elite_markers": ["politicians", "special interests", "insiders"],
          "moral_dichotomy": ["profit and theft", "total control", "rigged system"],
          "betrayal_themes": ["totally own her", "surrendering independence"]
        }
      },
      {
        "reference_id": "pluralist_democratic_manichaean",
        "score": 0.0,
        "text_sample": "Our democratic institutions represent the culmination of centuries of constitutional development, designed to balance competing interests while protecting minority rights.",
        "marker_analysis": {
          "institutional_focus": ["democratic institutions", "constitutional processes"],
          "complexity_recognition": ["competing interests", "complex trade-offs"],
          "legitimacy_through_process": ["constitutional development", "institutional frameworks"],
          "pluralism_emphasis": ["diverse society", "minority rights", "accommodation"]
        }
      }
    ]
  }
}
```

-----

## PDAF-Specific Synthesis Output

### Academic Report Template

```markdown
# PDAF Analysis Report: {{TEXT_IDENTIFIER}}

## Executive Summary
- **Framework**: Populist Discourse Analysis Framework v1.0
- **Text**: {{SOURCE_AND_CONTEXT}}
- **Analysis Date**: {{TIMESTAMP}}
- **Ensemble Models**: {{MODEL_LIST}}
- **Populist Discourse Index**: {{PDI_SCORE}} ({{INTERPRETATION_CATEGORY}})
- **Democratic Health Assessment**: {{LAYER_3_INTERPRETATION}}

## Methodology
- **Framework**: PDAF v1.0 nine-anchor populist discourse measurement
- **Calibration**: Extreme composite reference texts ensuring cross-ideological validity
- **Ensemble Approach**: Multi-model analysis with populist pattern validation
- **Debate Protocol**: Evidence-based divergence resolution for populist anchors
- **Quality Assurance**: Systematic bias detection and boundary distinction validation

## Populist Discourse Analysis

### Core Populist Anchors (Parallel Analysis)

#### Manichaean People-Elite Framing: {{SCORE}} ({{CONFIDENCE_INTERVAL}})
{{DETAILED_ANALYSIS_WITH_CALIBRATION_EVIDENCE}}

**Calibration Reference Alignment**:
- Closest Reference: {{REFERENCE_ID}} (Similarity: {{SIMILARITY_SCORE}})
- Cross-Ideological Validation: {{LEFT_RIGHT_PATTERN_CONSISTENCY}}
- Boundary Tests: {{NATIONALIST_ECONOMIC_DISTINCTION_RESULTS}}

#### Crisis-Restoration Temporal Narrative: {{SCORE}} ({{CONFIDENCE_INTERVAL}})
{{TEMPORAL_STRUCTURE_ANALYSIS}}

#### Popular Sovereignty Claims: {{SCORE}} ({{CONFIDENCE_INTERVAL}})
{{DEMOCRATIC_THEORY_ANALYSIS}}

#### Anti-Pluralist Exclusion: {{SCORE}} ({{CONFIDENCE_INTERVAL}})
{{OPPOSITION_LEGITIMACY_ANALYSIS}}

### Populist Mechanism Anchors (Parallel Analysis)

#### Elite Conspiracy/Systemic Corruption: {{SCORE}} ({{CONFIDENCE_INTERVAL}})
{{CONSPIRACY_NARRATIVE_ANALYSIS}}

#### Authenticity vs. Political Class: {{SCORE}} ({{CONFIDENCE_INTERVAL}})
{{REPRESENTATION_AUTHENTICITY_ANALYSIS}}

#### Homogeneous People Construction: {{SCORE}} ({{CONFIDENCE_INTERVAL}})
{{UNITY_DIVISION_ANALYSIS}}

### Boundary Distinction Anchors (Sequential Analysis)

#### Nationalist Exclusion: {{SCORE}} ({{CONFIDENCE_INTERVAL}})
{{CULTURAL_EXCLUSION_BOUNDARY_ANALYSIS}}

**Boundary Validation**: {{POPULIST_VS_NATIONALIST_DISTINCTION}}

#### Economic Redistributive Appeals: {{SCORE}} ({{CONFIDENCE_INTERVAL}})
{{ECONOMIC_POLICY_BOUNDARY_ANALYSIS}}

**Boundary Validation**: {{POPULIST_VS_ECONOMIC_DISTINCTION}}

## Populist Discourse Index

### {{LAYER_NAME}} PDI: {{PDI_SCORE}}

**Mathematical Calculation**:
```

{{LAYER_FORMULA}}
= {{DETAILED_CALCULATION}}
= {{FINAL_SCORE}}

```
**Competitive Dynamics Adjustment**: {{COMPETITIVE_ADJUSTMENT_IF_APPLICABLE}}

**Interpretation**: {{PDI_CATEGORY}} - {{DETAILED_POPULIST_INTERPRETATION}}

**Democratic Implications**:
- **Institutional Health**: {{DEMOCRATIC_INSTITUTION_IMPACT}}
- **Pluralism Risk**: {{ANTI_PLURALIST_ASSESSMENT}}
- **Popular Mobilization**: {{MOBILIZATION_POTENTIAL_ANALYSIS}}

## Competitive Dynamics Analysis

{{IF_MULTIPLE_ACTORS_DETECTED}}

### Multi-Actor Competition Effects
- **Competing Actors**: {{ACTOR_LIST}}
- **Competition Intensity**: {{OVERALL_COMPETITION_SCORE}}
- **Temporal Context**: {{TEMPORAL_DECAY_FACTORS}}

**Anchor-Specific Competition**:
- **Manichaean Competition**: {{COMPETITION_ADJUSTMENT}} (weight: 0.8)
- **Authenticity Competition**: {{COMPETITION_ADJUSTMENT}} (weight: 0.9)
- **Anti-Pluralist Competition**: {{COMPETITION_ADJUSTMENT}} (weight: 0.9)

**Effectiveness Implications**: {{COMPETITIVE_EFFECTIVENESS_ANALYSIS}}

## Ensemble Validation
- **Model Agreement**: {{AGREEMENT_PERCENTAGE}} across populist anchors
- **Debates Conducted**: {{DEBATE_COUNT}} for divergent populist assessments
- **Evidence Quality**: {{POPULIST_EVIDENCE_STRENGTH}}
- **Boundary Clarity**: {{BOUNDARY_DISTINCTION_ACCURACY}}
- **Final Confidence**: {{OVERALL_CONFIDENCE_METRICS}}

## PDAF Democratic Intelligence

### Populist Communication Assessment
{{FRAMEWORK_SPECIFIC_POPULIST_PATTERN_INTERPRETATION}}

### Democratic Health Implications
{{PDI_SCORE_DEMOCRATIC_CONSEQUENCES_ANALYSIS}}

### Cross-Ideological Patterns
{{LEFT_RIGHT_POPULIST_PATTERN_COMPARISON_IF_APPLICABLE}}

### Comparative Context
{{PDI_SCORE_COMPARATIVE_ANALYSIS_IF_AVAILABLE}}

## Methodology Appendix

### Calibration Validation
{{EXTREME_COMPOSITE_REFERENCE_ALIGNMENT_DETAILS}}

### Boundary Testing Results
{{SYSTEMATIC_BOUNDARY_DISTINCTION_VALIDATION}}

### Competitive Dynamics Mathematics
{{COMPLETE_COMPETITION_CALCULATION_DOCUMENTATION}}

### Complete Audit Trail
{{FULL_PDAF_TECHNICAL_DOCUMENTATION_AND_EVIDENCE_CHAINS}}
```

-----

## PDAF CLI Integration Examples

### Basic PDAF Analysis

```bash
# Descriptive populist pattern analysis
soar analyze --framework pdaf --version 1.0 --text speech.txt --layer descriptive

# Democratic engagement analysis
soar analyze --framework pdaf --version 1.0 --text speech.txt --layer engagement

# Full democratic health assessment
soar analyze --framework pdaf --version 1.0 --text speech.txt --layer health
```

### PDAF-Specific Operations

```bash
# Competitive dynamics analysis with multiple actors
soar analyze --framework pdaf --text "speech1.txt,speech2.txt" --competitive-dynamics

# Cross-ideological validation
soar analyze --framework pdaf --corpus "left_populist_corpus/,right_populist_corpus/" --cross-validate

# Boundary distinction testing
soar validate --framework pdaf --test-corpus boundary_validation_set/ --focus boundaries

# Temporal populist tracking
soar analyze --framework pdaf --corpus temporal_corpus/ --track-pdi --granularity monthly
```

### PDAF Calibration Operations

```bash
# Calibration packet validation
soar calibrate --framework pdaf --validate-references

# Calibration drift detection
soar calibrate --framework pdaf --drift-check --baseline calibration_baseline/

# Cross-ideological calibration testing
soar calibrate --framework pdaf --cross-ideological-test --corpus validation_corpus/
```

### PDAF Research Applications

```bash
# Van der Veen corpus analysis
soar analyze --framework pdaf --corpus van_der_veen_corpus/ --output longitudinal-analysis

# Electoral campaign analysis
soar analyze --framework pdaf --corpus campaign_speeches_2024/ --competitive-dynamics --track-pdi

# Cross-national populist comparison
soar analyze --framework pdaf --corpus "us_populist/,eu_populist/" --compare cross-national
```

-----

## PDAF Performance Optimization

### Context Token Management

**PDAF Requirements**:

- Framework Specification: ~25K tokens
- Complete Reference Corpora: ~135K tokens (all 9 anchors)
- SOAR Integration Guidelines: ~8K tokens
- JSON Schemas: ~8K tokens
- **Total Framework Package**: ~176K tokens

**Optimization Strategies**:

- **Model Selection**: Use 200K+ context models for full PDAF analysis
- **Selective Loading**: Load anchor-specific calibration for focused analysis
- **Batch Processing**: Process multiple texts with shared calibration context
- **Compression**: Use calibration summaries for preliminary analysis

### Model Selection for PDAF

**Optimal Models for Populist Analysis**:

- **Political Understanding**: Claude Sonnet 4, GPT-4o (excellent political pattern recognition)
- **Cross-Ideological Validity**: Gemini 2.5 Pro (reduced political bias)
- **Calibration Consistency**: Llama 3.3 (reliable reference alignment)
- **Boundary Distinction**: Mixed ensemble for boundary clarity

### PDAF-Specific Quality Metrics

```python
def calculate_pdaf_quality_score(analysis_results):
    """PDAF-specific quality assessment"""
    quality_factors = {
        "calibration_alignment": assess_reference_consistency(analysis_results),
        "​​​​​​​​​​​​​​​​
```