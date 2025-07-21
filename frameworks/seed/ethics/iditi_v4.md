# Individual Dignity Identity v Tribal Identity v4.0
**Version**: v4.0
**Status**: Active

---

## Executive Summary

The IDITI framework analyzes the fundamental tension between individual dignity and tribal identity in political discourse. This specialized framework focuses on how texts either affirm universal human worth or prioritize group-based identity and loyalty, examining the core moral question of whether human dignity is universal or conditional on group membership.

Based on Fukuyama's identity formation theory and Jung's collective psychology concepts, this framework evaluates the critical distinction between treating people as individuals with inherent worth versus defining people primarily through group membership and loyalty.

---

## Theoretical Foundation

This framework is grounded in Fukuyama's identity formation theory and Jung's collective psychology concepts. The framework applies dignity theory and collective psychology to analyze how discourse treats human moral worth as either universal or conditional on group membership.

### Core Identity Tension

The framework examines the fundamental philosophical and psychological tension between two approaches to human moral worth:

**Individual Dignity**: The principle that all humans possess inherent moral worth regardless of group identity, emphasizing agency, character, and universal rights.

**Tribal Identity**: The tendency to define moral worth and loyalty through group membership, creating in-group/out-group distinctions that condition dignity on tribal affiliation.

### Key References

- Fukuyama, F. (2018). Identity: The Demand for Dignity and the Politics of Resentment.
- Jung, C. G. (1921). Psychological Types. (Concepts of Individual vs. Collective Identity)

## Framework Dimensions

### Dignity

Affirms individual moral worth and universal rights, regardless of group identity. Emphasizes agency, pluralism, and character over affiliation. This represents the philosophical position that human dignity is inherent and universal.

**Key Indicators:**
- equal dignity, inherent worth, regardless of background, individual character
- universal rights, human agency, personal dignity, individual merit
- common humanity, respect for all, universal values, human dignity
- cross-group solidarity, individual autonomy, character-based judgment

### Tribalism

Prioritizes group dominance, loyalty, or identity over individual agency. Often frames moral worth in in-group/out-group terms. This represents the psychological tendency to condition respect and dignity on group membership.

**Key Indicators:**
- real Americans, our people, they don't belong, us vs them
- group loyalty, identity politics, blood and soil, true believers
- outsiders, not one of us, tribal unity, group supremacy
- in-group favoritism, group-based hierarchy, exclusion markers

## Analytical Methodology

This framework employs a focused approach to identity-based discourse analysis:

1. **Identity Recognition**: Identify how the text treats human moral worth and dignity
2. **Universal vs Conditional**: Assess whether dignity is presented as universal or group-conditional
3. **Individual vs Collective**: Analyze emphasis on individual agency versus group loyalty
4. **Evidence Collection**: Provide approximately 2 direct quotations supporting each assessment
5. **Confidence Assessment**: Rate analytical confidence based on evidence clarity

## Academic Validation

Framework validated through identity formation research and political psychology literature. Enhanced identity formation theory implementation with comprehensive analysis of dignity vs tribal identity dynamics. Applies Fukuyama's dignity theory and Jung's collective psychology for systematic evaluation of how discourse treats human moral worth.

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "iditi",
  "version": "v4.0",
  "display_name": "Individual Dignity Identity v Tribal Identity v4.0",
  "analysis_variants": {
    "default": {
      "description": "Complete implementation of the Individual Dignity Identity v Tribal Identity methodology",
      "analysis_prompt": "You are an expert analyst with deep knowledge of moral psychology, political discourse, and value analysis. Your task is to analyze the provided text using Individual Dignity Identity v Tribal Identity. The IDITI framework analyzes the fundamental tension between individual dignity and tribal identity in political discourse. This framework examines the following dimensions: - **Dignity**: Affirms individual moral worth and universal rights, regardless of group identity (look for: equal dignity, inherent worth, regardless of background, individual character, universal rights) - **Tribalism**: Prioritizes group dominance, loyalty, or identity over individual agency (look for: real Americans, our people, they don't belong, us vs them, group loyalty) For each dimension, follow this process: 1. Read the text systematically for relevant patterns and language 2. Identify specific evidence and quotations 3. Score the dimension from 0.0 to 1.0 based on strength and frequency of evidence 4. Provide approximately 2 direct quotations supporting each score 5. Assess your confidence in the scoring based on evidence clarity"
    }
  },
  "output_contract": {
    "schema": {
      "worldview": "string",
      "dignity_score": "number",
      "dignity_confidence": "number",
      "dignity_evidence": "array",
      "tribalism_score": "number",
      "tribalism_confidence": "number", 
      "tribalism_evidence": "array",
      "overall_analysis_confidence": "number",
      "key_patterns_observed": "string"
    },
    "instructions": "IMPORTANT: Your response MUST be a single, valid JSON object and nothing else. Do not include any text, explanations, or markdown code fences before or after the JSON object."
  },
  "calculation_spec": {
    "identity_axis_score": "Dignity score minus Tribalism score",
    "identity_intensity": "Absolute value of axis score"
  }
}
```

</details>