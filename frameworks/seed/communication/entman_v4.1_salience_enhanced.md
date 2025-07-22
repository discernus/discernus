# Entman Framing Functions Framework v4.1 - Salience Enhanced
**Version**: v4.1 - Salience Enhanced  
**Status**: Active

---

## Executive Summary

The Entman Framing Functions Framework v4.1 implements Robert Entman's communication analysis through **salience-enhanced framing function assessment**. This framework tests whether Problem Definition, Causal Attribution, Moral Evaluation, and Treatment Recommendation operate independently while revealing which framing functions speakers emphasize most strategically in message construction.

**Version 4.1 Enhancement**: **Salience-weighted framing analysis** - captures not just framing function intensity, but which framing functions receive the most rhetorical investment, enabling empirically-grounded understanding of strategic communication priorities.

---

## What is Salience-Enhanced Framing Analysis?

### **Salience in Strategic Communication**

**Salience** = How much rhetorical emphasis the speaker places on each framing function, regardless of raw function intensity scores.

**Key Insight**: A speaker might demonstrate moderate Problem Definition (0.6 intensity) throughout their discourse, while only briefly invoking intense Treatment Recommendation language (1.0 intensity). Problem Definition has higher **salience** (0.8) than Treatment Recommendation (0.2), revealing strategic communication priorities.

### **Dual-Track Framing Analysis**

**Track 1**: **Framing Function Intensity** (0.0-1.0) - Traditional function strength measurement  
**Track 2**: **Salience Ranking** (0.0-1.0) - Framing function emphasis and rhetorical prominence

**Result**: Complete communication analysis showing both framing function presence AND strategic message construction priorities.

---

## Framework Dimensions: Enhanced

### **Problem Definition (0.0-1.0)**
What issues are identified as requiring attention
- **Issue Identification**: "the real issue is," "we face a crisis of," "the challenge before us," "the problem we must address"
- **Crisis Framing**: "urgent need to," "what's really at stake," "fundamental issue," "core problem"
- **Scope Setting**: "this affects everyone," "widespread implications," "immediate action required"

### **Causal Attribution (0.0-1.0)**  
What factors or actors are presented as causing problems
- **Responsibility Assignment**: "caused by," "responsible for," "the reason is," "because of," "due to"
- **Blame Attribution**: "fault of," "led to this," "created the problem," "brought about"
- **Causal Explanation**: "resulted from," "stems from," "consequence of," "outcome of"

### **Moral Evaluation (0.0-1.0)**
What values and moral judgments are invoked
- **Value Invocation**: "right thing," "wrong approach," "moral obligation," "ethical imperative"  
- **Moral Judgment**: "just," "unjust," "fair," "unfair," "ethical," "unethical"
- **Values Framework**: "our values," "core principles," "moral foundation," "ethical standards"

### **Treatment Recommendation (0.0-1.0)**
What solutions are proposed and prioritized
- **Solution Advocacy**: "we must," "need to," "should," "the answer is," "the solution"
- **Policy Options**: "I propose," "recommend," "plan to," "will implement," "strategy"
- **Action Imperative**: "take action," "immediate steps," "urgent measures," "decisive action"

---

## Version 4.1 Enhancements

### **New Capabilities**
- **Salience Ranking**: Prominence assessment for all 4 framing functions
- **Strategic Communication Analysis**: Understanding message construction priorities  
- **Empirical Function Weighting**: Research-backed framing emphasis assessment

### **World-Class Agent Integration**
- **Enhanced Prompts**: Clear salience assessment instructions for framing functions
- **Output Contract**: Comprehensive strategic communication analysis

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "entman_v4_1_salience_enhanced",
  "version": "v4.0",
  "display_name": "Entman Framing Functions v4.1 - Salience Enhanced",
  "analysis_variants": {
    "default": {
      "description": "Salience-enhanced framing functions analysis across four independent dimensions",
      "analysis_prompt": "You are an expert in strategic communication and framing theory. Analyze using Entman Framing Functions v4.1 with SALIENCE-ENHANCED analysis. Assess both INTENSITY and SALIENCE for framing functions. PROBLEM DEFINITION: Issue identification - look for 'real issue is', 'face a crisis', 'challenge before us', 'urgent need', 'affects everyone'. CAUSAL ATTRIBUTION: Responsibility assignment - look for 'caused by', 'responsible for', 'fault of', 'resulted from', 'consequence of'. MORAL EVALUATION: Value judgments - look for 'right thing', 'moral obligation', 'just', 'ethical', 'our values', 'core principles'. TREATMENT RECOMMENDATION: Solutions proposed - look for 'we must', 'need to', 'propose', 'recommend', 'take action', 'solution'. CRITICAL: After intensity scoring, rank by SALIENCE - rhetorical prominence in message construction. For each: 1. Score intensity 0.0-1.0, 2. Assess salience 0.0-1.0, 3. Provide quotations and confidence."
    }
  },
  "calculation_spec": {
    "methodology_note": "Independent framing functions enhanced with salience weighting for strategic communication analysis",
    "framing_completeness": "Sum of all framing function scores - measures comprehensive message construction",
    "salience_weighted_assessment": "Function salience enables empirical strategic communication priority analysis"
  },
  "output_contract": {
    "schema": {
      "framing_analysis": "string",
      "function_scores": "object",
      "salience_ranking": "array",
      "strategic_communication_analysis": "string"
    },
    "instructions": "JSON object only. Include salience_ranking for all 4 functions with 'function', 'salience_score', 'rank'. Include strategic_communication_analysis explaining framing function priorities."
  }
}
```

</details> 