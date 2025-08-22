# Lakoff Framing Framework v4.1 - Salience Enhanced
**Version**: v4.1 - Salience Enhanced
**Status**: Active

---

## Executive Summary

Revolutionary family model framework enhanced with **salience-weighted analysis** examining Strict Father vs Nurturant Parent moral systems in political communication. Uses three bipolar dimensions with prominence assessment, revealing which family model components speakers emphasize most strategically in their moral and political reasoning.

**Version 4.1 Enhancement**: **Salience-weighted family model analysis** - captures not just family model intensity, but which moral system components receive the most rhetorical investment, enabling empirically-grounded understanding of moral political communication strategies.

---

## What is Salience-Enhanced Family Model Analysis?

### **Salience in Moral Political Systems**

**Salience** = How much rhetorical emphasis the speaker places on each family model dimension, regardless of raw bipolar scores.

**Key Insight**: A speaker might score moderate Authority (0.6) consistently throughout discourse, while briefly invoking intense Competition language (1.0). Authority has higher **salience** (0.8) than Competition (0.3), revealing core moral political priorities.

### **Dual-Track Moral Analysis**

**Track 1**: **Family Model Intensity** - Traditional bipolar scoring across 3 dimensions  
**Track 2**: **Salience Ranking** - Moral system emphasis and rhetorical prominence

**Result**: Complete moral political analysis showing both family model positioning AND strategic moral communication priorities.

---

## Framework Architecture: Enhanced Bipolar Analysis

### **Authority vs Empathy (0.0-1.0 bipolar)**
Moral authority vs empathetic understanding

**Strict Father (1.0)**: "strong leadership," "moral authority," "decisive action," "respect authority," "clear rules"
**Nurturant Parent (0.0)**: "listen to voices," "understand perspectives," "inclusive dialogue," "empathetic understanding"

### **Competition vs Cooperation (0.0-1.0 bipolar)**
Individual achievement vs collective support

**Strict Father (1.0)**: "natural hierarchy," "merit-based," "winners and losers," "individual achievement," "competitive advantage"  
**Nurturant Parent (0.0)**: "working together," "shared responsibility," "collective effort," "mutual support," "collaboration"

### **Self-Reliance vs Interdependence (0.0-1.0 bipolar)**
Individual responsibility vs social connection

**Strict Father (1.0)**: "personal responsibility," "self-reliance," "individual accountability," "self-determination," "bootstrap"
**Nurturant Parent (0.0)**: "we're connected," "stronger together," "mutual dependence," "common good," "social fabric"

---

## Salience-Enhanced Assessment

### **Family Model Coherence with Salience Intelligence**
- **Traditional Coherence**: Component clustering analysis  
- **v4.1 Enhancement**: Salience-weighted coherence showing strategic moral emphasis patterns
- **Strategic Insight**: Distinguish core moral commitments from tactical appeals

---

## Version 4.1 Enhancements

### **New Capabilities**
- **3-Dimension Salience Ranking**: Complete prominence assessment for family model components
- **Moral Strategy Intelligence**: Understanding rhetorical investment in moral systems
- **Enhanced Coherence Analysis**: Salience-weighted family model consistency assessment

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "lakoff_framing_v4_1_salience_enhanced",
  "version": "v4.0", 
  "display_name": "Lakoff Framing Framework v4.1 - Salience Enhanced",
  "analysis_variants": {
    "default": {
      "description": "Salience-enhanced family model analysis across three bipolar dimensions",
      "analysis_prompt": "You are an expert in cognitive linguistics and political psychology, specializing in Lakoff's family model theory. Analyze using Lakoff Framing Framework v4.1 with SALIENCE-ENHANCED analysis. Score three bipolar dimensions and assess SALIENCE. AUTHORITY vs EMPATHY: Strict Father (1.0) - 'strong leadership', 'moral authority', 'decisive action'; Nurturant Parent (0.0) - 'listen to voices', 'understand perspectives', 'inclusive dialogue'. COMPETITION vs COOPERATION: Strict Father (1.0) - 'natural hierarchy', 'merit-based', 'individual achievement'; Nurturant Parent (0.0) - 'working together', 'shared responsibility', 'collaboration'. SELF-RELIANCE vs INTERDEPENDENCE: Strict Father (1.0) - 'personal responsibility', 'self-reliance', 'bootstrap'; Nurturant Parent (0.0) - 'stronger together', 'mutual dependence', 'common good'. CRITICAL: After bipolar scoring, rank dimensions by SALIENCE - rhetorical prominence in moral reasoning. Provide quotations, confidence, and family model coherence analysis."
    }
  },
  "calculation_spec": {
    "strict_father_model_score": "(authority_score + competition_score + self_reliance_score) / 3",
    "nurturant_parent_model_score": "(empathy_score + cooperation_score + interdependence_score) / 3", 
    "family_model_coherence_index": "Math.abs(strict_father_model_score - nurturant_parent_model_score)",
    "salience_weighted_assessment": "Dimension salience enables empirical family model strategic communication analysis"
  },
  "output_contract": {
    "schema": {
      "family_model_analysis": "string",
      "dimension_scores": "object",
      "salience_ranking": "array",
      "coherence_assessment": "string",
      "moral_strategy_analysis": "string"
    },
    "instructions": "JSON object only. Include salience_ranking for all 3 dimensions with 'dimension', 'salience_score', 'rank'. Include moral_strategy_analysis explaining family model emphasis priorities."
  }
}
```

</details> 