# Character Assessment Framework v4.3 - Tension Enhanced

**Version**: v4.3 - Tension Enhanced  
**Status**: Implementation Ready

---

## Overview

CAF assesses character through systematic evaluation of ten core dimensions organized in five complementary pairs. Each pair represents fundamental tension in human character and decision-making.

**Purpose**: Objective character measurement through evidence-based analysis of moral priorities and behavioral patterns.

**Applications**: Leadership assessment, discourse analysis, character development evaluation.

---

## Character Dimensions

#### Dignity vs Tribalism
- **Dignity (0.0-1.0)**: Respect for inherent worth of all people, regardless of differences
- **Tribalism (0.0-1.0)**: Favoring one's own group at expense of outsiders

#### Truth vs Manipulation  
- **Truth (0.0-1.0)**: Commitment to honesty, accuracy, transparency in communication
- **Manipulation (0.0-1.0)**: Deliberately distorting information to achieve desired outcomes

#### Justice vs Resentment
- **Justice (0.0-1.0)**: Fairness, impartiality, proportionality in treatment and judgment  
- **Resentment (0.0-1.0)**: Bitterness toward those perceived as more fortunate or successful

#### Hope vs Fear
- **Hope (0.0-1.0)**: Optimism about future and confidence in positive possibilities
- **Fear (0.0-1.0)**: Anxiety about future and focus on potential threats or losses

#### Pragmatism vs Fantasy
- **Pragmatism (0.0-1.0)**: Practical, realistic approach to solving problems and achieving goals
- **Fantasy (0.0-1.0)**: Unrealistic expectations disconnected from practical realities

---

## Scoring Protocol

**Intensity Scale**: 0.0 (absent) to 1.0 (dominant expression)  
**Salience Scale**: 0.0 (peripheral) to 1.0 (central to character presentation)

**Requirements**:
- Score all ten dimensions for intensity and salience
- Provide 1-2 strongest quotes per dimension  
- Calculate tension scores for each pair
- Compute Moral Character-Strategic Coherence Index (MC-SCI)

---

## Character Calculations

**Tension Scores**: |Virtue Score - Vice Score| for each pair
**MC-SCI**: Overall character coherence measure across all dimensions
**Character Profile**: Primary moral identity based on highest-salience dimensions

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "character_assessment_framework_tension_enhanced",
  "version": "v4.3",
  "display_name": "Character Assessment Framework v4.3 - Tension Enhanced",
  "analysis_variants": {
    "default": {
      "description": "Complete character assessment with tension analysis",
      "analysis_prompt": "You are an expert character assessment analyst specializing in moral psychology and behavioral analysis. Your task is to analyze the provided text using the Character Assessment Framework (CAF) v4.3. This framework evaluates character through ten dimensions organized in five complementary pairs: Dignity vs Tribalism, Truth vs Manipulation, Justice vs Resentment, Hope vs Fear, Pragmatism vs Fantasy. For each dimension, assess both intensity (0.0-1.0 how strongly expressed) and salience (0.0-1.0 how central to character presentation). Focus on character revelation rather than policy positions. Provide 1-2 strongest quotes demonstrating each score. Calculate tension scores (absolute difference) for each pair and overall MC-SCI coherence measure. Identify primary moral identity based on highest-salience dimensions."
    }
  },
  "calculation_spec": {
    "dignity_tribalism_tension": "|(dignity_intensity * dignity_salience) - (tribalism_intensity * tribalism_salience)|",
    "truth_manipulation_tension": "|(truth_intensity * truth_salience) - (manipulation_intensity * manipulation_salience)|",
    "justice_resentment_tension": "|(justice_intensity * justice_salience) - (resentment_intensity * resentment_salience)|",
    "hope_fear_tension": "|(hope_intensity * hope_salience) - (fear_intensity * fear_salience)|",
    "pragmatism_fantasy_tension": "|(pragmatism_intensity * pragmatism_salience) - (fantasy_intensity * fantasy_salience)|",
    "mc_sci": "(dignity_tribalism_tension + truth_manipulation_tension + justice_resentment_tension + hope_fear_tension + pragmatism_fantasy_tension) / 5"
  },
  "output_contract": {
    "schema": {
      "worldview": "string",
      "scores": "object",
      "evidence": "object",
      "reasoning": "object",
      "salience_ranking": "array",
      "character_priorities": "string",
      "tension_analysis": "object",
      "character_clusters": "object"
    },
    "instructions": "IMPORTANT: Your response MUST be a single, valid JSON object and nothing else. Do not include any text, explanations, or markdown code fences before or after the JSON object. The scores object should contain intensity and salience scores for all 10 dimensions. The salience_ranking should be an ordered array of objects with 'dimension', 'salience_score', and 'rank'. The tension_analysis should contain calculated tensions and MC-SCI score."
  }
}
```

</details> 