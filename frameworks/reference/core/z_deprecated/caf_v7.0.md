# Civic Analysis Framework (CAF) v7.0

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

## Quality Standards

- Evidence must be drawn directly from the text with clear quotations
- Scores must be justified with specific textual support
- Analysis should focus on patterns of civic virtue rather than partisan political positions
- The framework should be applied consistently regardless of the speaker's political affiliation

## V7.0 Gasket Architecture Integration

**Raw Analysis Log Output**: This framework produces natural, human-readable analytical reports instead of complex JSON structures. The Analysis Agent focuses on intellectual analysis while the Intelligent Extractor handles data extraction.

**Gasket Schema**: The framework includes a complete gasket_schema that maps civic dimensions to flat JSON keys for reliable mathematical processing:
- Individual virtue scores (dignity_score, truth_score, justice_score, hope_score, pragmatism_score)
- Counter-virtue scores (tribalism_score, manipulation_score, resentment_score, fear_score, fantasy_score)  
- Strategic tension calculations (dignity_tribalism_tension, truth_manipulation_tension, etc.)
- Composite civic character index (civic_character_index)

<details>
<summary>Technical Specification</summary>

```json
{
  "name": "civic_analysis_framework",
  "version": "v7.0",
  "display_name": "Civic Analysis Framework (CAF) v7.0",
  "analysis_variants": {
    "default": {
      "description": "Complete civic character analysis across all five dimensions.",
      "analysis_prompt": "You are an expert political discourse analyst specializing in civic character assessment. Your task is to analyze the provided text using the Civic Analysis Framework (CAF) v7.0 methodology.\n\nThe framework evaluates political discourse across five critical civic dimensions:\n\n1. **Dignity** (0.0-1.0): Appeals to universal human worth, respect for individuals regardless of group membership, emphasis on shared humanity and individual moral agency.\n\n2. **Tribalism** (0.0-1.0): Appeals to group identity, us-vs-them framing, emphasis on group loyalty over universal principles, exclusionary rhetoric.\n\n3. **Truth** (0.0-1.0): Commitment to factual accuracy, acknowledgment of complexity, intellectual honesty, evidence-based reasoning.\n\n4. **Manipulation** (0.0-1.0): Strategic distortion of information, emotional manipulation, misleading framing, exploitation of cognitive biases.\n\n5. **Justice** (0.0-1.0): Concern for fair outcomes, procedural fairness, protection of rights, systemic equity considerations.\n\n6. **Resentment** (0.0-1.0): Exploitation of grievances, blame-focused rhetoric, zero-sum framing, victimization narratives.\n\n7. **Hope** (0.0-1.0): Constructive optimism, positive vision for the future, empowerment rhetoric, possibility-focused language.\n\n8. **Fear** (0.0-1.0): Anxiety-inducing rhetoric, threat-focused language, catastrophic framing, security-based appeals.\n\n9. **Pragmatism** (0.0-1.0): Realistic problem-solving, acknowledgment of constraints, practical solutions, incremental progress.\n\n10. **Fantasy** (0.0-1.0): Unrealistic promises, magical thinking, oversimplified solutions, denial of constraints.\n\nFor each dimension, provide a clear numerical score (0.0-1.0) based on the strength of evidence in the text. Include direct quotes that support your assessment and explain your reasoning. Focus on the civic character implications rather than partisan political positions.\n\nWrite a comprehensive analytical report that covers:\n- Application of the CAF methodology to this specific text\n- Detailed analysis of each relevant dimension with scores and evidence\n- Assessment of strategic tensions between competing virtues\n- Overall civic character profile with salience weighting\n- Key insights about the speaker's civic approach\n\nFocus on rigorous intellectual analysis rather than data formatting. Provide clear numerical scores within your natural language analysis, supported by direct textual evidence and reasoning."
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
    "target_keys": [
      "dignity_score",
      "tribalism_score",
      "dignity_tribalism_tension",
      "truth_score",
      "manipulation_score",
      "truth_manipulation_tension",
      "justice_score",
      "resentment_score",
      "justice_resentment_tension",
      "hope_score",
      "fear_score",
      "hope_fear_tension",
      "pragmatism_score",
      "fantasy_score",
      "pragmatism_fantasy_tension",
      "civic_character_index"
    ],
    "target_dimensions": [
      "Dignity",
      "Tribalism",
      "Dignity-Tribalism Tension",
      "Truth",
      "Manipulation",
      "Truth-Manipulation Tension",
      "Justice",
      "Resentment",
      "Justice-Resentment Tension",
      "Hope",
      "Fear",
      "Hope-Fear Tension",
      "Pragmatism",
      "Fantasy",
      "Pragmatism-Fantasy Tension",
      "Civic Character Index"
    ]
  },
  "calculation_spec": {
    "civic_character_index": "(dignity_tribalism_tension + truth_manipulation_tension + justice_resentment_tension + hope_fear_tension + pragmatism_fantasy_tension) / 5",
    "dignity_tribalism_tension": "abs(dignity_score - tribalism_score)",
    "truth_manipulation_tension": "abs(truth_score - manipulation_score)",
    "justice_resentment_tension": "abs(justice_score - resentment_score)",
    "hope_fear_tension": "abs(hope_score - fear_score)",
    "pragmatism_fantasy_tension": "abs(pragmatism_score - fantasy_score)"
  },
  "reliability_rubric": {
    "cronbachs_alpha": {
      "excellent": [0.80, 1.0],
      "good": [0.70, 0.79],
      "acceptable": [0.60, 0.69],
      "poor": [0.0, 0.59]
    },
    "notes": "Framework reliability assessment based on internal consistency of civic virtue measurements."
  },
  "output_contract": {
    "format": "raw_analysis_log",
    "description": "Analysis Agent produces a comprehensive, human-readable civic character assessment",
    "requirements": {
      "content_sections": [
        "Framework application and civic methodology",
        "Dimensional analysis with clear numerical scores (0.0-1.0)",
        "Direct textual evidence with civic character justification",
        "Strategic tension analysis between competing virtues",
        "Salience assessment and overall civic profile",
        "Key insights and civic character implications"
      ],
      "scoring_format": "Natural language with embedded numerical scores and clear justification",
      "evidence_format": "Direct quotes with civic character context and reasoning",
      "tone": "Rigorous academic analysis focused on civic virtue assessment",
      "structure": "Coherent analytical narrative, not rigid data formatting"
    },
    "instructions": "Write a comprehensive civic character analysis in natural language. Include clear numerical scores (0.0-1.0) for each relevant dimension, supported by direct textual evidence and civic virtue reasoning. Focus on the civic implications of the discourse rather than partisan positions. Assess strategic tensions between competing virtues. The Intelligent Extractor will handle all structured data extraction from your natural language report."
  }
}
```

</details>