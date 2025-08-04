# Civic Analysis Framework (CAF) v7.1

The Civic Analysis Framework provides a systematic approach to evaluating the civic character of political discourse, focusing on the fundamental tensions between competing civic virtues and their strategic deployment in public communication.

## Framework Overview

This framework evaluates political discourse across five critical dimensions that form the foundation of civic character:

1. **Dignity vs. Tribalism**: The tension between appeals to universal human dignity and tribal/group-based identity politics
2. **Truth vs. Manipulation**: The commitment to factual accuracy versus strategic information manipulation
3. **Justice vs. Resentment**: The pursuit of fair outcomes versus the exploitation of grievances
4. **Hope vs. Fear**: The cultivation of constructive optimism versus the strategic deployment of anxiety
5. **Pragmatism vs. Fantasy**: Realistic problem-solving versus idealistic or unrealistic promises

## Theoretical Foundation

The framework is grounded in classical civic republican theory, which holds that sustainable democratic governance requires citizens and leaders who embody certain civic virtues. The framework recognizes that political discourse often involves strategic tensions between these virtues, and that understanding these tensions is crucial for evaluating the civic health of democratic communication.

## Methodology

The analysis focuses on identifying specific textual evidence that demonstrates the presence or absence of each civic virtue, as well as evidence of strategic contradictions where speakers simultaneously appeal to competing virtues. The framework emphasizes the importance of salience-weighted analysis, recognizing that not all dimensions may be equally relevant in every text.

## V7.1 Enhanced Gasket Architecture

**Raw Analysis Log Output**: This framework produces natural, human-readable analytical reports with embedded metadata scores (salience and confidence) for each dimension. The Analysis Agent focuses on intellectual analysis while the Intelligent Extractor handles data extraction using advanced pattern matching.

**Metadata Requirements**: For each dimension, analysts must provide:
- **Salience Score (0.0-1.0)**: How central is this dimension to the text?
- **Confidence Score (0.0-1.0)**: How certain are you in this assessment?

**Enhanced Gasket Schema**: The framework includes comprehensive extraction patterns and validation rules for reliable mathematical processing across all civic dimensions and their strategic tensions.

## Quality Standards

- Evidence must be drawn directly from the text with clear quotations
- Scores must be justified with specific textual support and metadata context
- Analysis should focus on patterns of civic virtue rather than partisan political positions
- The framework should be applied consistently regardless of the speaker's political affiliation
- Salience and confidence scores must reflect genuine analytical assessment, not default values

<details>
<summary>Technical Specification</summary>

```json
{
  "name": "civic_analysis_framework",
  "version": "v7.1",
  "display_name": "Civic Analysis Framework (CAF) v7.1",
  "analysis_variants": {
    "default": {
      "description": "Complete civic character analysis across all five dimensions with enhanced metadata.",
      "analysis_prompt": "You are an expert political discourse analyst specializing in civic character assessment. Your task is to analyze the provided text using the Civic Analysis Framework (CAF) v7.1 methodology with enhanced metadata reporting.\n\nThe framework evaluates political discourse across five critical civic dimensions:\n\n1. **Dignity** (0.0-1.0): Appeals to universal human worth, respect for individuals regardless of group membership, emphasis on shared humanity and individual moral agency.\n\n2. **Tribalism** (0.0-1.0): Appeals to group identity, us-vs-them framing, emphasis on group loyalty over universal principles, exclusionary rhetoric.\n\n3. **Truth** (0.0-1.0): Commitment to factual accuracy, acknowledgment of complexity, intellectual honesty, evidence-based reasoning.\n\n4. **Manipulation** (0.0-1.0): Strategic distortion of information, emotional manipulation, misleading framing, exploitation of cognitive biases.\n\n5. **Justice** (0.0-1.0): Concern for fair outcomes, procedural fairness, protection of rights, systemic equity considerations.\n\n6. **Resentment** (0.0-1.0): Exploitation of grievances, blame-focused rhetoric, zero-sum framing, victimization narratives.\n\n7. **Hope** (0.0-1.0): Constructive optimism, positive vision for the future, empowerment rhetoric, possibility-focused language.\n\n8. **Fear** (0.0-1.0): Anxiety-inducing rhetoric, threat-focused language, catastrophic framing, security-based appeals.\n\n9. **Pragmatism** (0.0-1.0): Realistic problem-solving, acknowledgment of constraints, practical solutions, incremental progress.\n\n10. **Fantasy** (0.0-1.0): Unrealistic promises, magical thinking, oversimplified solutions, denial of constraints.\n\nFor each dimension, provide:\n- **Score (0.0-1.0)**: Based on strength of evidence in the text\n- **Salience (0.0-1.0)**: How central is this dimension to this specific text?\n- **Confidence (0.0-1.0)**: How certain are you in this assessment?\n\nWrite a comprehensive analytical report that covers:\n- Application of the CAF methodology to this specific text\n- Detailed analysis of each relevant dimension with scores, salience, confidence, and evidence\n- Assessment of strategic tensions between competing virtues\n- Overall civic character profile with salience weighting\n- Key insights about the speaker's civic approach\n\nEmbedded your numerical assessments naturally within the analysis. For example: 'This text demonstrates strong dignity appeals (dignity score: 0.8, salience: 0.9, confidence: 0.7) with frequent references to universal human worth.' Focus on rigorous intellectual analysis supported by direct textual evidence and clear reasoning for all scores and metadata."
    }
  },
  "dimension_groups": {
    "identity_axis": ["dignity", "tribalism"],
    "truth_axis": ["truth", "manipulation"],
    "justice_axis": ["justice", "resentment"],
    "emotional_axis": ["hope", "fear"],
    "reality_axis": ["pragmatism", "fantasy"]
  },
  "gasket_schema": {
    "version": "7.1",
    "extraction_method": "intelligent_extractor",
    "target_keys": [
      "dignity_score",
      "tribalism_score",
      "dignity_salience",
      "tribalism_salience",
      "dignity_confidence",
      "tribalism_confidence",
      "truth_score",
      "manipulation_score",
      "truth_salience",
      "manipulation_salience",
      "truth_confidence",
      "manipulation_confidence",
      "justice_score",
      "resentment_score",
      "justice_salience",
      "resentment_salience",
      "justice_confidence",
      "resentment_confidence",
      "hope_score",
      "fear_score",
      "hope_salience",
      "fear_salience",
      "hope_confidence",
      "fear_confidence",
      "pragmatism_score",
      "fantasy_score",
      "pragmatism_salience",
      "fantasy_salience",
      "pragmatism_confidence",
      "fantasy_confidence"
    ],
    "extraction_patterns": {
      "dignity_score": ["dignity.{0,20}score", "dignity.{0,20}rating", "dignity\\s*:\\s*[0-9]"],
      "tribalism_score": ["tribalism.{0,20}score", "tribalism.{0,20}rating", "tribalism\\s*:\\s*[0-9]"],
      "dignity_salience": ["dignity.{0,20}salience", "dignity.{0,20}importance", "dignity.{0,20}centrality"],
      "tribalism_salience": ["tribalism.{0,20}salience", "tribalism.{0,20}importance", "tribalism.{0,20}centrality"],
      "dignity_confidence": ["dignity.{0,20}confidence", "dignity.{0,20}certainty", "dignity.{0,20}sure"],
      "tribalism_confidence": ["tribalism.{0,20}confidence", "tribalism.{0,20}certainty", "tribalism.{0,20}sure"],
      "truth_score": ["truth.{0,20}score", "truth.{0,20}rating", "truth\\s*:\\s*[0-9]"],
      "manipulation_score": ["manipulation.{0,20}score", "manipulation.{0,20}rating", "manipulation\\s*:\\s*[0-9]"],
      "truth_salience": ["truth.{0,20}salience", "truth.{0,20}importance", "truth.{0,20}centrality"],
      "manipulation_salience": ["manipulation.{0,20}salience", "manipulation.{0,20}importance", "manipulation.{0,20}centrality"],
      "truth_confidence": ["truth.{0,20}confidence", "truth.{0,20}certainty", "truth.{0,20}sure"],
      "manipulation_confidence": ["manipulation.{0,20}confidence", "manipulation.{0,20}certainty", "manipulation.{0,20}sure"],
      "justice_score": ["justice.{0,20}score", "justice.{0,20}rating", "justice\\s*:\\s*[0-9]"],
      "resentment_score": ["resentment.{0,20}score", "resentment.{0,20}rating", "resentment\\s*:\\s*[0-9]"],
      "justice_salience": ["justice.{0,20}salience", "justice.{0,20}importance", "justice.{0,20}centrality"],
      "resentment_salience": ["resentment.{0,20}salience", "resentment.{0,20}importance", "resentment.{0,20}centrality"],
      "justice_confidence": ["justice.{0,20}confidence", "justice.{0,20}certainty", "justice.{0,20}sure"],
      "resentment_confidence": ["resentment.{0,20}confidence", "resentment.{0,20}certainty", "resentment.{0,20}sure"],
      "hope_score": ["hope.{0,20}score", "hope.{0,20}rating", "hope\\s*:\\s*[0-9]"],
      "fear_score": ["fear.{0,20}score", "fear.{0,20}rating", "fear\\s*:\\s*[0-9]"],
      "hope_salience": ["hope.{0,20}salience", "hope.{0,20}importance", "hope.{0,20}centrality"],
      "fear_salience": ["fear.{0,20}salience", "fear.{0,20}importance", "fear.{0,20}centrality"],
      "hope_confidence": ["hope.{0,20}confidence", "hope.{0,20}certainty", "hope.{0,20}sure"],
      "fear_confidence": ["fear.{0,20}confidence", "fear.{0,20}certainty", "fear.{0,20}sure"],
      "pragmatism_score": ["pragmatism.{0,20}score", "pragmatism.{0,20}rating", "pragmatism\\s*:\\s*[0-9]"],
      "fantasy_score": ["fantasy.{0,20}score", "fantasy.{0,20}rating", "fantasy\\s*:\\s*[0-9]"],
      "pragmatism_salience": ["pragmatism.{0,20}salience", "pragmatism.{0,20}importance", "pragmatism.{0,20}centrality"],
      "fantasy_salience": ["fantasy.{0,20}salience", "fantasy.{0,20}importance", "fantasy.{0,20}centrality"],
      "pragmatism_confidence": ["pragmatism.{0,20}confidence", "pragmatism.{0,20}certainty", "pragmatism.{0,20}sure"],
      "fantasy_confidence": ["fantasy.{0,20}confidence", "fantasy.{0,20}certainty", "fantasy.{0,20}sure"]
    },
    "validation_rules": {
      "required_fields": ["dignity_score", "tribalism_score", "truth_score", "manipulation_score", "justice_score", "resentment_score", "hope_score", "fear_score", "pragmatism_score", "fantasy_score"],
      "score_ranges": {"min": 0.0, "max": 1.0},
      "metadata_ranges": {
        "salience": {"min": 0.0, "max": 1.0},
        "confidence": {"min": 0.0, "max": 1.0}
      },
      "fallback_strategy": "use_default_values"
    }
  },
  "calculation_spec": {
    "dignity_tribalism_tension": "(dignity_score + (1 - tribalism_score)) / 2",
    "truth_manipulation_tension": "(truth_score + (1 - manipulation_score)) / 2",
    "justice_resentment_tension": "(justice_score + (1 - resentment_score)) / 2",
    "hope_fear_tension": "(hope_score + (1 - fear_score)) / 2",
    "pragmatism_fantasy_tension": "(pragmatism_score + (1 - fantasy_score)) / 2",
    "civic_character_index": "(dignity_tribalism_tension + truth_manipulation_tension + justice_resentment_tension + hope_fear_tension + pragmatism_fantasy_tension) / 5"
  }
}
```

</details>