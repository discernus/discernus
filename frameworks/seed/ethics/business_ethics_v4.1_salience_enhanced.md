# Business Ethics Framework v4.1 - Salience Enhanced
**Version**: v4.1 - Salience Enhanced
**Status**: Active

---

## Executive Summary

The Business Ethics Framework v4.1 analyzes business communications across three domains of ethical concern through **salience-enhanced stakeholder analysis**: stakeholder relationships, operational integrity, and strategic vision. This framework reveals which ethical domains and approaches speakers emphasize most strategically in business discourse.

**Version 4.1 Enhancement**: **Salience-weighted business ethics analysis** - captures not just ethical approach intensity, but which business ethics domains receive the most rhetorical investment, enabling empirically-grounded understanding of corporate responsibility priorities.

---

## What is Salience-Enhanced Business Ethics Analysis?

### **Salience in Business Ethics**

**Salience** = How much rhetorical emphasis the speaker places on each business ethics domain, regardless of raw intensity scores.

**Key Insight**: A speaker might demonstrate moderate Customer Service (0.6 intensity) throughout their discourse, while briefly mentioning intense Strategic Purpose language (1.0 intensity). Customer Service has higher **salience** (0.8) than Strategic Purpose (0.2), revealing business ethics priorities.

### **Dual-Track Business Ethics Analysis**

**Track 1**: **Ethics Domain Intensity** (0.0-1.0) - Traditional stakeholder vs exploitation measurement  
**Track 2**: **Salience Ranking** (0.0-1.0) - Business ethics emphasis and rhetorical prominence

**Result**: Complete business ethics analysis showing both stakeholder approach presence AND strategic corporate responsibility priorities.

---

## Framework Architecture: Enhanced Three-Domain Analysis

### **Stakeholder Relations Domain**

**Customer Service (0.0-1.0)**: Genuine customer benefit emphasis
- **Customer Success**: "customer success," "genuine value," "long-term relationship," "customer feedback"
- **Problem Solving**: "solving real problems," "transparent pricing," "honest communication," "customer-first"

**Employee Development (0.0-1.0)**: Workforce investment emphasis  
- **Employee Growth**: "employee development," "career advancement," "skills training," "professional growth"
- **Workplace Investment**: "employee wellbeing," "work-life balance," "fair compensation," "supportive environment"

### **Operational Integrity Domain**

**Governance Transparency (0.0-1.0)**: Accountability and openness
- **Transparency**: "transparent operations," "open communication," "accountable leadership," "clear reporting"
- **Ethical Governance**: "ethical standards," "compliance," "responsible management," "oversight"

**Financial Responsibility (0.0-1.0)**: Responsible financial management
- **Responsible Finance**: "responsible spending," "financial integrity," "honest reporting," "sustainable practices"
- **Long-term Thinking**: "long-term value," "sustainable growth," "responsible investment," "prudent management"

### **Strategic Vision Domain**

**Sustainable Purpose (0.0-1.0)**: Long-term value creation focus
- **Purpose-Driven**: "sustainable purpose," "long-term value," "responsible business," "meaningful impact"
- **Stakeholder Value**: "stakeholder value," "shared prosperity," "responsible capitalism," "social benefit"

---

## Version 4.1 Enhancements

### **New Capabilities**
- **Multi-Domain Salience Ranking**: Prominence assessment across all business ethics dimensions
- **Corporate Responsibility Strategy Analysis**: Understanding business ethics priority patterns
- **Stakeholder Emphasis Intelligence**: Which stakeholder relationships receive most attention

### **World-Class Agent Integration**
- **Enhanced Prompts**: Clear salience assessment for business ethics domains
- **Output Contract**: Comprehensive corporate responsibility strategic analysis

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "business_ethics_v4_1_salience_enhanced",
  "version": "v4.0",
  "display_name": "Business Ethics Framework v4.1 - Salience Enhanced",
  "analysis_variants": {
    "default": {
      "description": "Salience-enhanced business ethics analysis across three stakeholder domains",
      "analysis_prompt": "You are an expert in business ethics and stakeholder theory. Analyze using Business Ethics Framework v4.1 with SALIENCE-ENHANCED analysis. Assess INTENSITY and SALIENCE across domains. STAKEHOLDER RELATIONS: Customer Service - 'customer success', 'genuine value', 'transparent pricing'; Employee Development - 'employee development', 'career advancement', 'fair compensation'. OPERATIONAL INTEGRITY: Governance Transparency - 'transparent operations', 'accountable leadership', 'ethical standards'; Financial Responsibility - 'responsible spending', 'financial integrity', 'sustainable practices'. STRATEGIC VISION: Sustainable Purpose - 'sustainable purpose', 'long-term value', 'stakeholder value', 'responsible business'. CRITICAL: After intensity scoring, rank dimensions by SALIENCE - rhetorical prominence in business ethics discourse. Provide quotations, confidence, and corporate responsibility analysis."
    }
  },
  "calculation_spec": {
    "stakeholder_focus_index": "Average of stakeholder-oriented dimension scores - measures stakeholder capitalism emphasis",
    "operational_integrity_index": "Average of governance and financial responsibility scores - measures operational ethics",
    "strategic_sustainability_score": "Sustainable purpose dimension score - measures long-term ethical orientation",
    "salience_weighted_assessment": "Business ethics dimension salience enables empirical corporate responsibility priority analysis"
  },
  "output_contract": {
    "schema": {
      "business_ethics_analysis": "string",
      "domain_scores": "object",
      "salience_ranking": "array",
      "ethics_indices": "object", 
      "corporate_responsibility_strategy_analysis": "string"
    },
    "instructions": "JSON object only. Include salience_ranking for all dimensions with 'dimension', 'salience_score', 'rank'. Include corporate_responsibility_strategy_analysis explaining business ethics emphasis priorities."
  }
}
```

</details> 