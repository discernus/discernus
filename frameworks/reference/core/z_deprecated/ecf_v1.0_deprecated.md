# Emotional Climate Framework (ECF) v1.0
## Pure Emotional Atmosphere Assessment

---

## Overview

ECF analyzes emotional atmosphere in political discourse through six dimensions, independent of rhetorical strategy, speaker character, or institutional effects. Measures psychological environment that discourse generates.

**Purpose**: Objective measurement of emotional climate for audience response prediction and message optimization.

**Applications**: Emotional impact assessment, cross-platform analysis, longitudinal tracking, message optimization.

---

## Theoretical Foundation

**Core Principle**: Emotional climate exists independently of other discourse factors. Same emotional patterns appear across different rhetorical strategies, speakers, and institutional contexts.

**Basis**: Affective intelligence theory, social identity research, persuasion studies demonstrate emotions drive political behavior beyond rational evaluation.

**Innovation**: Preserves complete emotional information through independent dimension scoring, avoiding binary sentiment reduction.

---

## Dimensions

#### Fear (Crisis/Threat Climate) (0.0-1.0)
**Definition**: Language emphasizing danger, threat, vulnerability, crisis, or existential risk.
**Key Markers**: "emergency," "crisis," "under attack," "running out of time," "defenseless"

#### Hope (Opportunity/Progress Climate) (0.0-1.0)  
**Definition**: Language emphasizing positive possibilities, progress, improvement, or achievement potential.
**Key Markers**: "opportunity," "breakthrough," "bright future," "great potential," "optimistic"

#### Enmity (Hostility/Conflict Climate) (0.0-1.0)
**Definition**: Language creating antagonistic atmosphere toward opponents, enemies, or opposing groups.
**Key Markers**: "enemy," "betrayal," "fight against," "destroy," "combat"

#### Amity (Friendship/Unity Climate) (0.0-1.0)
**Definition**: Language fostering positive relationships, cooperation, solidarity, or shared purpose.
**Key Markers**: "together," "unity," "partnership," "cooperation," "shared values"

#### Envy (Resentment/Grievance Climate) (0.0-1.0)
**Definition**: Language expressing resentment toward others' advantages, success, or privileged positions.
**Key Markers**: "unfair advantage," "privileged elite," "deserve better," "left behind," "rigged system"

#### Compersion (Celebration/Merit Climate) (0.0-1.0)
**Definition**: Language celebrating others' success, merit, achievement, or positive developments.
**Key Markers**: "congratulations," "well-deserved," "earned success," "inspiring achievement," "celebration"

---

## Scoring Protocol

**Intensity Scale**: 0.0 (absent) to 1.0 (dominant theme)
**Salience Scale**: 0.0 (peripheral) to 1.0 (central to message)

**Requirements**:
- Score all six dimensions
- Provide 1-2 strongest quotes per dimension
- Explain scoring rationale
- Rank dimensions by salience

---

## Composite Calculations

- **Affective Climate**: Hope - Fear
- **Relational Climate**: Amity - Enmity  
- **Success Climate**: Compersion - Envy
- **Overall Intensity**: Average of all six dimensions
- **Balance Score**: Average of three climate indices

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "emotional_climate_framework",
  "version": "v1.0", 
  "display_name": "Emotional Climate Framework (ECF) v1.0",
  "analysis_variants": {
    "default": {
      "description": "Complete emotional climate analysis across six dimensions",
      "analysis_prompt": "You are an expert emotional climate analyst specializing in political discourse psychology. Your task is to analyze the provided text using the Emotional Climate Framework (ECF) v1.0. This framework measures the emotional atmosphere created by discourse through six fundamental dimensions: Fear (crisis/threat climate), Hope (opportunity/progress climate), Enmity (hostility/conflict climate), Amity (friendship/unity climate), Envy (resentment/grievance climate), and Compersion (celebration/merit climate). For each dimension, assess both intensity (0.0-1.0 how strongly expressed) and salience (0.0-1.0 how central to the message). Focus on the emotional atmosphere created rather than rhetorical strategy or speaker character. Provide 1-2 strongest quotes demonstrating each score. Include confidence assessment for each dimension. Rank dimensions by salience from most to least central. Calculate composite scores: affective climate (hope-fear), relational climate (amity-enmity), success climate (compersion-envy), overall intensity (average), and balance score (average of climate indices)."
    }
  },
  "calculation_spec": {
    "affective_climate_index": "(hope_score - fear_score)",
    "relational_climate_index": "(amity_score - enmity_score)", 
    "success_climate_index": "(compersion_score - envy_score)",
    "overall_emotional_intensity": "(fear_score + hope_score + enmity_score + amity_score + envy_score + compersion_score) / 6",
    "emotional_balance_score": "(affective_climate_index + relational_climate_index + success_climate_index) / 3"
  },
  "output_contract": {
    "schema": {
      "worldview": "string",
      "scores": "object",
      "evidence": "object", 
      "confidence": "object",
      "reasoning": "object",
      "salience_ranking": "array"
    },
    "instructions": "IMPORTANT: Your response MUST be a single, valid JSON object and nothing else. Do not include any text, explanations, or markdown code fences before or after the JSON object. The salience_ranking should be an ordered array of objects, each containing 'dimension' (string), 'salience_score' (0.0-1.0), and 'rank' (integer), ordered from most salient (rank 1) to least salient."
  }
}
```

</details> 