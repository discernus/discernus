# Political Discourse Two-Axis Analysis v4.1 - Salience Enhanced  
**Version**: v4.1 - Salience Enhanced
**Status**: Active

---

## Executive Summary

Revolutionary two-axis framework enhanced with **salience-weighted analysis** that resolves conceptual overlap problems in traditional political discourse models. Uses orthogonal axes with prominence assessment: Populism ↔ Pluralism (vertical) and Patriotism ↔ Nationalism (horizontal), revealing which political dimensions speakers emphasize most strategically.

**Version 4.1 Enhancement**: **Salience-weighted orthogonal analysis** - captures not just axis intensity, but which political dimensions receive the most rhetorical investment, enabling empirically-grounded understanding of political strategic positioning.

---

## What is Salience-Enhanced Orthogonal Analysis?

### **Salience in Political Axes**

**Salience** = How much rhetorical emphasis the speaker places on each political dimension, regardless of raw axis scores.

**Key Insight**: A speaker might score high Populism (0.9) briefly and moderate Patriotism (0.6) throughout. Patriotism has higher **salience** (0.8) than Populism (0.3) despite lower intensity, revealing strategic political priorities.

### **Dual-Track Political Analysis**

**Track 1**: **Axis Intensity** - Traditional orthogonal scoring (populism/pluralism, patriotism/nationalism)  
**Track 2**: **Salience Ranking** - Political dimension emphasis and rhetorical prominence assessment

**Result**: Complete political discourse analysis showing both axis positioning AND strategic political priorities.

---

## Framework Architecture: Enhanced Orthogonal Analysis

### **Vertical Axis: Populism ↔ Pluralism** 
People vs institutions tension

**Populism (High)**: "will of the people," "corrupt elite," "direct democracy," "popular mandate"
**Pluralism (Low)**: "institutional safeguards," "checks and balances," "minority rights," "deliberative process"

### **Horizontal Axis: Patriotism ↔ Nationalism**
Civic vs ethnic identity tension

**Patriotism (Left)**: "civic values," "constitutional principles," "democratic institutions," "civic duty"  
**Nationalism (Right)**: "cultural superiority," "ethnic identity," "national purity," "cultural dominance"

### **Salience-Enhanced Assessment**

#### **Step 1**: Score all four dimensions (0.0-1.0)
#### **Step 2**: Rank by salience (rhetorical prominence)  
#### **Step 3**: Strategic positioning analysis

---

## Version 4.1 Enhancements

### **Resolves "Bolsonaro Problem" with Salience Intelligence**
- **Traditional Issue**: Couldn't capture simultaneous high populism + nationalism
- **v4.1 Solution**: Orthogonal scoring + salience strategic analysis

### **New Capabilities**
- **4-Dimension Salience Ranking**: Complete prominence assessment  
- **Political Strategy Intelligence**: Understanding rhetorical investment priorities
- **Enhanced Positioning**: Empirical political strategic communication analysis

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "political_discourse_v4_1_salience_enhanced",
  "version": "v4.0",
  "display_name": "Political Discourse Two-Axis v4.1 - Salience Enhanced",
  "analysis_variants": {
    "default": {
      "description": "Salience-enhanced orthogonal political discourse analysis",
      "analysis_prompt": "You are an expert in political communication. Analyze using Political Discourse Two-Axis v4.1 with SALIENCE-ENHANCED analysis. Score four dimensions and assess SALIENCE. VERTICAL AXIS - Populism: 'will of people', 'corrupt elite', 'direct democracy'; Pluralism: 'institutional safeguards', 'checks and balances', 'minority rights'. HORIZONTAL AXIS - Patriotism: 'civic values', 'constitutional principles', 'democratic institutions'; Nationalism: 'cultural superiority', 'ethnic identity', 'national purity'. CRITICAL: After intensity scoring, rank all four dimensions by SALIENCE - rhetorical prominence. Provide quotations, confidence, and strategic analysis."
    }
  },
  "calculation_spec": {
    "vertical_axis_score": "populism_score - pluralism_score",
    "horizontal_axis_score": "nationalism_score - patriotism_score", 
    "quadrant_positioning": "Four-quadrant political positioning analysis",
    "salience_weighted_assessment": "Four-dimension salience ranking enables empirical political strategic positioning analysis"
  },
  "output_contract": {
    "schema": {
      "political_analysis": "string",
      "axis_scores": "object",
      "salience_ranking": "array", 
      "quadrant_analysis": "string",
      "political_strategy_analysis": "string"
    },
    "instructions": "JSON object only. Include salience_ranking for all 4 dimensions with 'dimension', 'salience_score', 'rank'. Include political_strategy_analysis explaining strategic priorities."
  }
}
```

</details> 