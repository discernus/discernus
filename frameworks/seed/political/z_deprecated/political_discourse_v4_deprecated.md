# Political Discourse Two-Axis Analysis v4.0
**Version**: v4.0
**Status**: Active

---

## Executive Summary

Revolutionary two-axis framework for political discourse analysis that resolves the fundamental conceptual overlap problems in traditional competitive models. Uses orthogonal axes to capture the core tensions in democratic political discourse without crowding-out effects.

This framework implements two independent dimensions: Populism ↔ Pluralism (vertical axis examining people vs institutions) and Patriotism ↔ Nationalism (horizontal axis examining civic vs ethnic identity). The orthogonal architecture eliminates the "Bolsonaro Problem" where traditional frameworks failed to accurately capture high populism and high nationalism simultaneously.

---

## Theoretical Foundation

This framework is based on enhanced democratic theory that recognizes two fundamental and independent tensions in political discourse. The orthogonal architecture resolves conceptual overlap problems present in traditional competitive models.

### Core Innovation: Orthogonal Architecture

**Vertical Axis**: Populism ↔ Pluralism represents the tension between direct popular sovereignty and institutional mediation in democratic governance.

**Horizontal Axis**: Patriotism ↔ Nationalism represents the distinction between civic attachment to political institutions versus ethnic/cultural supremacy claims.

### Resolves "Bolsonaro Problem"

Traditional frameworks scored figures like Bolsonaro as "somewhat populist" (0.5) because nationalist content was incorrectly seen as competing with populist content. This framework allows accurate scoring: High Populism + High Nationalism simultaneously, without theoretical contradiction.

### Key References

- Enhanced Framework for Political Discourse Analysis (2025)
- Mudde, C. (2004). The Populist Zeitgeist. Government and Opposition.
- Miller, D. (1995). On Nationality. Oxford University Press.
- Brubaker, R. (2020). Populism and nationalism. Nations and Nationalism.
- Singh, P. (2021). Populism, Nationalism, and Nationalist Populism.

## Framework Dimensions

### Populism (Vertical Axis - High)

Direct popular sovereignty, anti-elite sentiment, Manichaean worldview. This represents appeals to "the people" against corrupt institutions and elite interests.

**Key Indicators:**
- the people, corrupt elite, establishment, will of the people
- us versus them, drain the swamp, real Americans/citizens, ordinary people

### Pluralism (Vertical Axis - Low)

Institutional mediation, diverse representation, expert knowledge. This represents respect for democratic institutions, procedural norms, and diverse stakeholder input.

**Key Indicators:**
- institutions, experts, diverse perspectives, democratic process
- checks and balances, constitutional principles, stakeholder input, evidence-based

### Nationalism (Horizontal Axis - High)

Ethnic/cultural identity emphasis, national supremacy claims. This represents appeals to cultural heritage, traditional values, and ethnic/cultural superiority.

**Key Indicators:**
- our people, national greatness, cultural heritage, traditional values
- foreign influence, national identity, cultural purity, ancestral homeland

### Patriotism (Horizontal Axis - Low)

Civic attachment to political institutions and constitutional values. This represents pride in democratic institutions, constitutional principles, and civic participation.

**Key Indicators:**
- constitution, democratic values, rule of law, civic duty
- constitutional rights, democratic institutions, equal justice, civic participation

## Analytical Methodology

This framework employs orthogonal dimensional analysis with sequential scoring:

1. **Vertical Axis Analysis**: Focus exclusively on populism vs pluralism indicators, ignoring horizontal elements
2. **Horizontal Axis Analysis**: Focus exclusively on nationalism vs patriotism indicators, ignoring vertical elements  
3. **Independent Scoring**: Each axis scored 0.0-1.0 without consideration of the other axis
4. **Quadrant Classification**: Combine axis scores to determine political discourse quadrant
5. **Evidence Collection**: Provide quotations supporting each dimensional assessment

### Four Quadrants

- **High Populism + High Nationalism**: Populist Nationalism (e.g., Trump, Bolsonaro)
- **High Populism + Low Nationalism**: Civic Populism (e.g., Sanders, Warren)
- **Low Populism + High Nationalism**: Elite Nationalism (traditional conservatives)
- **Low Populism + Low Nationalism**: Liberal Pluralism (establishment liberals)

## Academic Validation

Framework validated through democratic theory research and political discourse analysis. Orthogonal two-axis framework eliminates conceptual overlap problems in traditional competitive models. Enables independent dimensional analysis without crowding-out effects, providing accurate measurement of complex political discourse that combines multiple democratic tensions simultaneously.

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "political_discourse_two_axis",
  "version": "v4.0",
  "display_name": "Political Discourse Two-Axis Analysis v4.0",
  "analysis_variants": {
    "default": {
      "description": "Complete implementation of the Political Discourse Two-Axis Analysis methodology",
      "analysis_prompt": "You are an expert analyst with deep knowledge of moral psychology, political discourse, and value analysis. Your task is to analyze the provided text using Political Discourse Two-Axis Analysis. Revolutionary two-axis framework for political discourse analysis that resolves the fundamental conceptual overlap problems in traditional competitive models. This framework examines the following dimensions along two orthogonal axes: VERTICAL AXIS (Populism ↔ Pluralism): - **Populism**: Direct popular sovereignty, anti-elite sentiment, Manichaean worldview (look for: the people, corrupt elite, establishment, will of the people, us versus them) - **Pluralism**: Institutional mediation, diverse representation, expert knowledge (look for: institutions, experts, diverse perspectives, democratic process, checks and balances) HORIZONTAL AXIS (Patriotism ↔ Nationalism): - **Nationalism**: Ethnic/cultural identity emphasis, national supremacy claims (look for: our people, national greatness, cultural heritage, traditional values, foreign influence) - **Patriotism**: Civic attachment to political institutions and constitutional values (look for: constitution, democratic values, rule of law, civic duty, constitutional rights) For each axis, follow this process: 1. Analyze the vertical axis (populism vs pluralism) independently, scoring from 0.0 (pure pluralism) to 1.0 (pure populism) 2. Analyze the horizontal axis (nationalism vs patriotism) independently, scoring from 0.0 (pure patriotism) to 1.0 (pure nationalism) 3. Identify specific evidence and quotations supporting each score 4. Assess confidence in scoring based on evidence clarity 5. Determine quadrant classification based on axis combination"
    }
  },
  "output_contract": {
    "schema": {
      "worldview": "string",
      "vertical_axis_score": "number",
      "vertical_axis_confidence": "number",
      "vertical_axis_evidence": "array",
      "horizontal_axis_score": "number", 
      "horizontal_axis_confidence": "number",
      "horizontal_axis_evidence": "array",
      "quadrant_classification": "string",
      "overall_analysis_confidence": "number",
      "key_patterns_observed": "string"
    },
    "instructions": "IMPORTANT: Your response MUST be a single, valid JSON object and nothing else. Do not include any text, explanations, or markdown code fences before or after the JSON object."
  },
  "calculation_spec": {
    "vertical_axis_score": "Single-pass analysis of vertical dimension indicators (0.0 = Pure Pluralism, 1.0 = Pure Populism)",
    "horizontal_axis_score": "Single-pass analysis of horizontal dimension indicators (0.0 = Pure Patriotism, 1.0 = Pure Nationalism)",
    "quadrant_classification": "Four-quadrant classification based on axis intersection"
  }
}
```

</details>