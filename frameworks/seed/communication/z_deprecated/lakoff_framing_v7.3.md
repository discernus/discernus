# Lakoff Framing Framework v7.3

**Version**: 7.3
**Status**: Active
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

---

## Executive Summary

The Lakoff Framing Framework v7.3 analyzes political and social discourse using George Lakoff's model of family-based morality with enhanced metadata analysis. It identifies whether communication is framed through a "Strict Father" model (emphasizing authority, discipline, and self-reliance) or a "Nurturant Parent" model (emphasizing empathy, cooperation, and interdependence), with advanced extraction patterns and validation rules for robust analysis.

**Innovation**: Salience-weighted analysis captures not just family model presence but which moral frameworks receive the most rhetorical emphasis.

---

## Framework Dimensions

### **Three Bipolar Dimensions: Family Model Architecture**

**1. Authority vs Empathy**
- **Strict Father (1.0)**: Strong leadership, moral authority, decisive action
- **Nurturant Parent (0.0)**: Understanding, inclusive dialogue, listening to voices

**2. Competition vs Cooperation**  
- **Strict Father (1.0)**: Natural hierarchy, merit-based systems, individual achievement
- **Nurturant Parent (0.0)**: Working together, shared responsibility, collaborative approaches

**3. Self-Reliance vs Interdependence**
- **Strict Father (1.0)**: Personal responsibility, self-reliance, bootstrap philosophy  
- **Nurturant Parent (0.0)**: Stronger together, mutual dependence, common good emphasis

---

## Family Model Tension Mathematics

### **Family Model Tension Scoring**

**Formula**: `Family Model Tension = min(Strict_Father_score, Nurturant_Parent_score) × |Strict_Father_salience - Nurturant_Parent_salience|`

### **Family Model Strategic Contradiction Index (FMSCI)**

**Formula**: `FMSCI = (Sum of all Family Model Tension Scores) / Number of Dimensions`

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "lakoff_framing_v7_1",
  "version": "v7.3",
  "display_name": "Lakoff Framing Framework v7.1",
  "analysis_variants": {
    "default": {
      "description": "Sequential family model analysis with chain-of-thought methodology",
      "analysis_prompt": "You are an expert in cognitive linguistics and political psychology, specializing in Lakoff's family model theory across diverse cultural contexts. Analyze this text through focused sequential steps, examining each family model axis independently before integration.\n\nSTEP 1 - AUTHORITY VS EMPATHY AXIS ANALYSIS\nFocus ONLY on authority vs empathy patterns (ignore other dimensions for now):\n- Look for Strict Father authority patterns: strong leadership ('decisive action,' 'moral authority,' 'clear direction'), hierarchical language ('strong leadership,' 'moral authority,' 'take charge') - Note: These are semantic concepts, look for emphasis on strong leadership and moral authority, not just these exact phrases (Score toward 1.0)\n- Look for Nurturant Parent empathy patterns: understanding language ('listen to voices,' 'understand perspectives,' 'inclusive dialogue'), collaborative leadership ('work together,' 'shared leadership,' 'consensus building') - Note: These are semantic concepts, look for emphasis on understanding and inclusive dialogue, not just these exact expressions (Score toward 0.0)\n- Score authority vs empathy dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central are authority/empathy appeals to the overall message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nSTEP 2 - COMPETITION VS COOPERATION AXIS ANALYSIS\nNow focus ONLY on competition vs cooperation patterns:\n- Look for Strict Father competition patterns: hierarchy language ('natural hierarchy,' 'merit-based systems,' 'individual achievement'), competitive framing ('compete to win,' 'survival of fittest,' 'earned success') - Note: These are semantic concepts, look for emphasis on natural hierarchy and individual achievement, not just these exact terms (Score toward 1.0)\n- Look for Nurturant Parent cooperation patterns: collaboration language ('working together,' 'shared responsibility,' 'collective action'), mutual support ('help each other,' 'common effort,' 'shared success') - Note: These are semantic concepts, look for emphasis on working together and shared responsibility, not just these exact approaches (Score toward 0.0)\n- Score competition vs cooperation dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central are competition/cooperation appeals to the message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nSTEP 3 - SELF-RELIANCE VS INTERDEPENDENCE AXIS ANALYSIS\nNow focus ONLY on self-reliance vs interdependence patterns:\n- Look for Strict Father self-reliance patterns: independence language ('personal responsibility,' 'self-reliance,' 'bootstrap philosophy'), individual accountability ('stand on own,' 'take responsibility,' 'self-sufficient') - Note: These are semantic concepts, look for emphasis on personal responsibility and self-reliance, not just these exact philosophies (Score toward 1.0)\n- Look for Nurturant Parent interdependence patterns: mutual dependence ('stronger together,' 'we need each other,' 'interconnected'), common good ('collective welfare,' 'shared prosperity,' 'community support') - Note: These are semantic concepts, look for emphasis on mutual dependence and common good, not just these exact values (Score toward 0.0)\n- Score self-reliance vs interdependence dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central are self-reliance/interdependence appeals to the message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nFINAL STEP - INTEGRATION AND VALIDATION\nReview your step-by-step analysis:\n- Check for scoring consistency across all family model axes\n- Validate that evidence quality meets academic standards\n- Calculate family model tension scores and strategic contradiction index\n- Confirm confidence levels are appropriately calibrated\n- Identify overall family model profile (Strict Father vs Nurturant Parent orientation)\n- Apply pattern classifications based on family-based moral reasoning\n\nProvide your final structured analysis following this format:\n\n**FAMILY MODEL ASSESSMENT**\n\n**Authority vs Empathy**: [score] (salience: [score], confidence: [score])\n**Competition vs Cooperation**: [score] (salience: [score], confidence: [score])\n**Self-Reliance vs Interdependence**: [score] (salience: [score], confidence: [score])\n\n**Calculated Metrics**:\n- Family Model Strategic Contradiction Index: [calculated score]\n- Overall Family Model Profile: [Strict Father/Nurturant Parent orientation]\n\n**Key Insights**: [Summary of family-based moral reasoning, strategic moral framework deployment, and cognitive linguistic patterns]"
    }
  },
  "dimension_groups": {
    "family_model_axes": ["authority_vs_empathy", "competition_vs_cooperation", "self_reliance_vs_interdependence"]
  },
  "calculation_spec": {
    "family_model_tension_mathematics": "Family model tension quantification for bipolar dimensions using formula: Family Model Tension = min(dimension_score, 1.0 - dimension_score) × |salience_effect|.",
    "family_model_tensions": {
      "authority_empathy_tension": "min(authority_vs_empathy_score, 1.0 - authority_vs_empathy_score) * authority_vs_empathy_salience",
      "competition_cooperation_tension": "min(competition_vs_cooperation_score, 1.0 - competition_vs_cooperation_score) * competition_vs_cooperation_salience",
      "self_reliance_interdependence_tension": "min(self_reliance_vs_interdependence_score, 1.0 - self_reliance_vs_interdependence_score) * self_reliance_vs_interdependence_salience"
    },
    "family_model_strategic_contradiction_index": "(authority_empathy_tension + competition_cooperation_tension + self_reliance_interdependence_tension) / 3"
  },
  "reliability_rubric": {
    "cronbachs_alpha": {
      "excellent": [0.80, 1.0],
      "good": [0.70, 0.79],
      "acceptable": [0.60, 0.69],
      "poor": [0.0, 0.59]
    },
    "notes": "Defines quality thresholds for framework reliability. The Synthesis Agent uses this for automated fit assessment."
  }
}
```

</details>

<GASKET_SCHEMA_START>
{
  "gasket_schema": {
    "version": "v7.3",
    "extraction_method": "intelligent_extractor",
    "target_keys": [
      "authority_vs_empathy_score", "authority_vs_empathy_salience", "authority_vs_empathy_confidence",
      "competition_vs_cooperation_score", "competition_vs_cooperation_salience", "competition_vs_cooperation_confidence",
      "self_reliance_vs_interdependence_score", "self_reliance_vs_interdependence_salience", "self_reliance_vs_interdependence_confidence"
    ],
    "extraction_patterns": {
      "authority_vs_empathy_score": ["authority.*?vs.*?empathy.*?score.*?([0-9]\\.[0-9])", "authority.*?empathy.*?([0-9]\\.[0-9])", "authority\\s*vs\\s*empathy\\s*:\\s*([0-9]\\.[0-9])"],
      "competition_vs_cooperation_score": ["competition.*?vs.*?cooperation.*?score.*?([0-9]\\.[0-9])", "competition.*?cooperation.*?([0-9]\\.[0-9])", "competition\\s*vs\\s*cooperation\\s*:\\s*([0-9]\\.[0-9])"],
      "self_reliance_vs_interdependence_score": ["self.*?reliance.*?vs.*?interdependence.*?score.*?([0-9]\\.[0-9])", "self.*?reliance.*?([0-9]\\.[0-9])", "self\\s*reliance\\s*vs\\s*interdependence\\s*:\\s*([0-9]\\.[0-9])"]
    },
    "validation_rules": {
      "required_fields": [
        "authority_vs_empathy_score", "competition_vs_cooperation_score", "self_reliance_vs_interdependence_score"
      ],
      "score_ranges": {"min": 0.0, "max": 1.0},
      "metadata_ranges": {
        "salience": {"min": 0.0, "max": 1.0},
        "confidence": {"min": 0.0, "max": 1.0}
      },
      "fallback_strategy": "use_default_values"
    }
  }
}
<GASKET_SCHEMA_END>