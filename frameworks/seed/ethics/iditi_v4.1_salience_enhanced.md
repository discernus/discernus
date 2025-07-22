# Individual Dignity Identity v Tribal Identity v4.1 - Salience Enhanced  
**Version**: v4.1 - Salience Enhanced
**Status**: Active

---

## Executive Summary

The IDITI Framework v4.1 analyzes the fundamental tension between individual dignity and tribal identity through **salience-enhanced moral worth analysis**. This framework examines both the presence and rhetorical prominence of universal human dignity appeals versus group-based identity and loyalty, revealing which moral worth approaches speakers prioritize strategically.

**Version 4.1 Enhancement**: **Salience-weighted dignity analysis** - captures not just dignity vs tribal intensity, but which moral worth approaches speakers emphasize most rhetorically, enabling empirically-grounded assessment of moral identity priorities.

---

## What is Salience-Enhanced Dignity Analysis?

### **Salience in Moral Worth**

**Salience** = How much rhetorical emphasis the speaker places on each moral worth approach, regardless of raw intensity scores.

**Key Insight**: A speaker might demonstrate moderate Individual Dignity appeals (0.6 intensity) consistently throughout their discourse, while only briefly invoking intense Tribal Identity language (1.0 intensity). Individual Dignity has higher **salience** (0.8) than Tribal Identity (0.2), revealing core moral worth priorities.

### **Dual-Track Dignity Analysis**

**Track 1**: **Moral Worth Intensity** (0.0-1.0) - Traditional dignity vs tribal strength measurement  
**Track 2**: **Salience Assessment** (0.0-1.0) - Moral worth emphasis and rhetorical prominence

**Result**: Complete moral analysis showing both dignity positioning AND strategic moral worth priorities.

---

## Framework Dimensions: Enhanced

### **Individual Dignity (0.0-1.0)**
Universal human worth regardless of group identity
- **Universal Worth**: "equal dignity," "inherent worth," "regardless of background," "individual character"
- **Universal Rights**: "universal rights," "human agency," "personal dignity," "individual merit"
- **Common Humanity**: "common humanity," "respect for all," "universal values," "human dignity"
- **Cross-Group Solidarity**: "cross-group solidarity," "individual autonomy," "character-based judgment"

### **Tribal Identity (0.0-1.0)**  
Group-based moral worth and loyalty conditioning
- **Group Supremacy**: "real Americans," "our people," "they don't belong," "us vs them"
- **Identity-Based Worth**: "group loyalty," "identity politics," "blood and soil," "true believers"
- **In-Group Favoritism**: "our kind," "people like us," "group membership," "tribal belonging"
- **Out-Group Exclusion**: "not one of us," "different," "outsiders," "foreign influence"

---

## Version 4.1 Enhancements

### **New Capabilities**
- **Salience Ranking**: Rhetorical prominence assessment for dignity vs tribal approaches
- **Moral Worth Strategy Analysis**: Understanding speaker priorities in human dignity
- **Strategic Dignity Assessment**: Empirical weighting of universal vs conditional dignity

### **World-Class Agent Integration**
- **Enhanced Prompts**: Clear salience assessment instructions for moral worth analysis
- **Output Contract**: Comprehensive moral dignity strategic analysis

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "iditi_v4_1_salience_enhanced",
  "version": "v4.0",
  "display_name": "Individual Dignity Identity v Tribal Identity v4.1 - Salience Enhanced",
  "analysis_variants": {
    "default": {
      "description": "Salience-enhanced individual dignity vs tribal identity moral analysis",
      "analysis_prompt": "You are an expert in moral philosophy and political psychology. Analyze using IDITI v4.1 with SALIENCE-ENHANCED analysis. Assess both INTENSITY and SALIENCE for moral worth approaches. INDIVIDUAL DIGNITY: Universal human worth - look for 'equal dignity', 'inherent worth', 'regardless of background', 'universal rights', 'human agency', 'common humanity', 'respect for all', 'individual autonomy'. TRIBAL IDENTITY: Group-based moral worth - look for 'real Americans', 'our people', 'us vs them', 'group loyalty', 'identity politics', 'our kind', 'not one of us', 'outsiders'. CRITICAL: After intensity scoring, rank by SALIENCE - rhetorical prominence regardless of intensity. For each: 1. Score intensity 0.0-1.0, 2. Assess salience 0.0-1.0, 3. Provide quotations and confidence."
    }
  },
  "calculation_spec": {
    "methodology_note": "Simple dignity vs tribal comparison enhanced with salience weighting",
    "dignity_balance": "individual_dignity_score - tribal_identity_score", 
    "salience_weighted_assessment": "Moral worth salience enables empirical dignity priority analysis"
  },
  "output_contract": {
    "schema": {
      "dignity_analysis": "string",
      "moral_scores": "object",
      "salience_ranking": "array",
      "moral_strategy_analysis": "string"
    },
    "instructions": "JSON object only. Include salience_ranking with 'approach', 'salience_score', 'rank'. Include moral_strategy_analysis explaining moral worth priorities."
  }
}
```

</details> 