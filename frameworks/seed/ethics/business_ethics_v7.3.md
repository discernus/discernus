# Business Ethics Framework v7.3

**Version**: 7.3  
**Status**: Active  
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

---

## Overview

The Business Ethics Framework v7.3 analyzes business communications across three domains of ethical concern: stakeholder relationships, operational integrity, and strategic vision with enhanced metadata scoring. This advanced framework examines business ethics through distinct domains that represent core areas of corporate responsibility with robust extraction patterns and validation rules.

**Purpose**: Analyzes business ethics across three domains with enhanced extraction patterns and validation rules for comprehensive corporate responsibility assessment.

**Innovation**: Multi-dimensional business ethics analysis examining stakeholder relations, operational integrity, and strategic vision.

**Applications**: Corporate responsibility analysis, business ethics assessment, stakeholder relationship evaluation, operational integrity studies.

---

## Framework Dimensions

### **Stakeholder Relations Domain**

#### Customer Service (0.0-1.0)
**Definition**: Prioritizes genuine customer benefit and transparent value delivery.
**Key Markers**: "customer success," "genuine value," "long-term relationship," "customer feedback," "solving real problems," "transparent pricing," "honest communication," "customer-first"

#### Customer Exploitation (0.0-1.0)
**Definition**: Prioritizes extraction of value from customers over genuine service.
**Key Markers**: "maximize extraction," "hidden fees," "planned obsolescence," "vendor lock-in," "dark patterns," "manipulative marketing," "bait and switch," "profit maximization"

#### Employee Development (0.0-1.0)
**Definition**: Invests in worker growth, safety, and meaningful contribution.
**Key Markers**: "employee growth," "professional development," "workplace safety," "meaningful work," "work-life balance," "fair compensation," "career advancement," "team empowerment"

#### Employee Exploitation (0.0-1.0)
**Definition**: Treats workers as disposable resources for profit extraction.
**Key Markers**: "human resources," "cost cutting," "efficiency gains," "lean operations," "expendable workforce," "maximize productivity," "reduce labor costs," "workforce optimization"

### **Operational Integrity Domain**

#### Accountability (0.0-1.0)
**Definition**: Demonstrates transparent governance and responsible decision-making.
**Key Markers**: "transparent governance," "accountable leadership," "open decision-making," "stakeholder input," "ethical standards," "responsible practices," "oversight mechanisms," "public reporting"

#### Opacity (0.0-1.0)
**Definition**: Conceals decision-making processes and avoids accountability.
**Key Markers**: "proprietary information," "confidential strategy," "need to know basis," "trade secrets," "competitive advantage," "internal matters," "executive privilege," "strategic confidentiality"

#### Financial Responsibility (0.0-1.0)
**Definition**: Demonstrates prudent financial management and honest reporting.
**Key Markers**: "sustainable growth," "prudent management," "accurate reporting," "financial discipline," "long-term stability," "responsible investment," "sound fundamentals," "fiscal responsibility"

#### Financial Manipulation (0.0-1.0)
**Definition**: Engages in accounting manipulation or unsustainable financial practices.
**Key Markers**: "aggressive accounting," "revenue recognition," "financial engineering," "off-balance sheet," "creative bookkeeping," "earnings management," "regulatory arbitrage," "financial optimization"

### **Strategic Vision Domain**

#### Sustainable Purpose (0.0-1.0)
**Definition**: Articulates long-term value creation for society and stakeholders.
**Key Markers**: "sustainable impact," "societal benefit," "long-term value," "positive contribution," "meaningful mission," "stakeholder capitalism," "social responsibility," "environmental stewardship"

#### Short Term Extraction (0.0-1.0)
**Definition**: Focuses solely on short-term profit extraction without regard for long-term consequences.
**Key Markers**: "quarterly results," "shareholder value," "cost optimization," "market efficiency," "competitive advantage," "profit maximization," "operational leverage," "margin expansion"

---

## Gasket Architecture

### Raw Analysis Log Format
The analysis agent outputs a raw analysis log containing:
- Business ethics dimension scores for all 10 dimensions
- Salience weights for each dimension
- Evidence quotes with confidence ratings
- Qualitative reasoning about business ethics patterns

### Intelligent Extractor Schema
```json
{
  "gasket_schema": {
    "target_keys": [
      "customer_service_score", "customer_exploitation_score", "employee_development_score", "employee_exploitation_score",
      "accountability_score", "opacity_score", "financial_responsibility_score", "financial_manipulation_score",
      "sustainable_purpose_score", "short_term_extraction_score",
      "customer_service_salience", "customer_exploitation_salience", "employee_development_salience", "employee_exploitation_salience",
      "accountability_salience", "opacity_salience", "financial_responsibility_salience", "financial_manipulation_salience",
      "sustainable_purpose_salience", "short_term_extraction_salience",
      "customer_service_confidence", "customer_exploitation_confidence", "employee_development_confidence", "employee_exploitation_confidence",
      "accountability_confidence", "opacity_confidence", "financial_responsibility_confidence", "financial_manipulation_confidence",
      "sustainable_purpose_confidence", "short_term_extraction_confidence"
    ]
  }
}
```

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "business_ethics_v7_1",
  "version": "v7.3",
  "display_name": "Business Ethics Framework v7.3",
  "analysis_variants": {
    "default": {
      "description": "Sequential business ethics analysis with chain-of-thought methodology",
      "analysis_prompt": "You are an expert analyst specializing in business ethics and corporate responsibility across diverse contexts. Analyze this text through focused sequential steps, examining each ethics domain independently before integration.\n\nSTEP 1 - STAKEHOLDER RELATIONS DOMAIN ANALYSIS\nFocus ONLY on stakeholder relations patterns (ignore other domains for now):\n- Look for customer service patterns: benefit language ('genuine customer benefit,' 'transparent value delivery,' 'customer success'), service orientation ('serve customers,' 'meet needs,' 'customer-centric') - Note: These are semantic concepts, look for emphasis on genuine customer benefit and transparent value delivery, not just these exact approaches\n- Look for customer exploitation patterns: extraction language ('extract value,' 'maximize revenue,' 'customer acquisition cost'), manipulative practices ('hidden fees,' 'deceptive marketing,' 'lock-in strategies') - Note: These are semantic concepts, look for extraction of value from customers over genuine service, not just these exact tactics\n- Look for employee development patterns: growth language ('worker development,' 'employee growth,' 'meaningful contribution'), investment focus ('training programs,' 'career advancement,' 'worker safety') - Note: These are semantic concepts, look for worker growth and meaningful contribution, not just these exact programs\n- Look for employee exploitation patterns: resource language ('human resources,' 'disposable workforce,' 'cost reduction'), exploitation indicators ('minimum wage,' 'no benefits,' 'unsafe conditions') - Note: These are semantic concepts, look for treating workers as disposable resources, not just these exact conditions\n- Score each dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central are stakeholder relations to the overall message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nSTEP 2 - OPERATIONAL INTEGRITY DOMAIN ANALYSIS\nNow focus ONLY on operational integrity patterns:\n- Look for accountability patterns: transparency language ('transparent governance,' 'responsible decision-making,' 'open processes'), governance focus ('board oversight,' 'stakeholder input,' 'ethical guidelines') - Note: These are semantic concepts, look for transparent governance and responsible decision-making, not just these exact structures\n- Look for opacity patterns: concealment language ('confidential processes,' 'proprietary methods,' 'need to know basis'), secrecy indicators ('undisclosed,' 'internal only,' 'classified') - Note: These are semantic concepts, look for concealing decision-making processes, not just these exact methods\n- Look for financial responsibility patterns: prudent language ('sound financial management,' 'honest reporting,' 'sustainable practices'), integrity focus ('accurate accounting,' 'ethical reporting,' 'long-term stability') - Note: These are semantic concepts, look for prudent financial management and honest reporting, not just these exact practices\n- Look for financial manipulation patterns: manipulation language ('creative accounting,' 'aggressive reporting,' 'short-term gains'), deceptive practices ('hidden liabilities,' 'inflated revenues,' 'misleading metrics') - Note: These are semantic concepts, look for accounting manipulation or unsustainable practices, not just these exact techniques\n- Score each dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central is operational integrity to the message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nSTEP 3 - STRATEGIC VISION DOMAIN ANALYSIS\nNow focus ONLY on strategic vision patterns:\n- Look for sustainable purpose patterns: long-term language ('long-term value creation,' 'stakeholder benefit,' 'societal impact'), purpose focus ('mission-driven,' 'social responsibility,' 'sustainable growth') - Note: These are semantic concepts, look for long-term value creation for society and stakeholders, not just these exact missions\n- Look for short-term extraction patterns: extraction language ('maximize shareholder value,' 'quarterly profits,' 'cost cutting'), short-term focus ('immediate returns,' 'quick profits,' 'exit strategy') - Note: These are semantic concepts, look for focusing solely on short-term profit extraction, not just these exact strategies\n- Score each dimension (0.0-1.0) with specific textual evidence\n- Assess salience (0.0-1.0): How central is strategic vision to the message?\n- State confidence (0.0-1.0): How certain are you in this assessment?\nShow your analytical work and evidence before proceeding.\n\nFINAL STEP - INTEGRATION AND VALIDATION\nReview your step-by-step analysis:\n- Check for scoring consistency across all ethics domains\n- Validate that evidence quality meets academic standards\n- Calculate domain indices and overall corporate responsibility profile\n- Confirm confidence levels are appropriately calibrated\n- Identify business ethics patterns and stakeholder orientation\n- Apply pattern classifications based on overall ethical approach\n\nProvide your final structured analysis following this format:\n\n**BUSINESS ETHICS ASSESSMENT**\n\n**Stakeholder Relations**: Customer Service [score]/Customer Exploitation [score], Employee Development [score]/Employee Exploitation [score] (salience: [score], confidence: [score])\n**Operational Integrity**: Accountability [score]/Opacity [score], Financial Responsibility [score]/Financial Manipulation [score] (salience: [score], confidence: [score])\n**Strategic Vision**: Sustainable Purpose [score]/Short Term Extraction [score] (salience: [score], confidence: [score])\n\n**Calculated Metrics**:\n- Stakeholder Focus Index: [calculated score]\n- Operational Ethics Index: [calculated score]\n- Strategic Ethics Index: [calculated score]\n- Overall Corporate Responsibility Profile: [classification]\n\n**Key Insights**: [Summary of business ethics patterns, stakeholder orientation, and corporate responsibility approach]"
    }
  },
  "dimension_groups": {
    "stakeholder_relations": ["customer_service", "customer_exploitation", "employee_development", "employee_exploitation"],
    "operational_integrity": ["accountability", "opacity", "financial_responsibility", "financial_manipulation"],
    "strategic_vision": ["sustainable_purpose", "short_term_extraction"]
  },
  "calculation_spec": {
    "stakeholder_focus_index": "(customer_service_score + employee_development_score - customer_exploitation_score - employee_exploitation_score) / 4",
    "operational_integrity_index": "(accountability_score + financial_responsibility_score - opacity_score - financial_manipulation_score) / 4",
    "strategic_sustainability_score": "(sustainable_purpose_score - short_term_extraction_score + 1) / 2",
    "salience_weighted_stakeholder_focus_index": "((customer_service_score * customer_service_salience + employee_development_score * employee_development_salience) - (customer_exploitation_score * customer_exploitation_salience + employee_exploitation_score * employee_exploitation_salience)) / (customer_service_salience + employee_development_salience + customer_exploitation_salience + employee_exploitation_salience + 1e-9)",
    "salience_weighted_operational_integrity_index": "((accountability_score * accountability_salience + financial_responsibility_score * financial_responsibility_salience) - (opacity_score * opacity_salience + financial_manipulation_score * financial_manipulation_salience)) / (accountability_salience + financial_responsibility_salience + opacity_salience + financial_manipulation_salience + 1e-9)",
    "salience_weighted_strategic_sustainability_score": "(sustainable_purpose_score * sustainable_purpose_salience - short_term_extraction_score * short_term_extraction_salience + (sustainable_purpose_salience + short_term_extraction_salience + 1e-9) / 2) / (sustainable_purpose_salience + short_term_extraction_salience + 1e-9)",
    "salience_weighted_business_ethics_index": "(stakeholder_focus_index * ((customer_service_salience + employee_development_salience + customer_exploitation_salience + employee_exploitation_salience + 1e-9) / 4) + operational_integrity_index * ((accountability_salience + financial_responsibility_salience + opacity_salience + financial_manipulation_salience + 1e-9) / 4) + strategic_sustainability_score * ((sustainable_purpose_salience + short_term_extraction_salience + 1e-9) / 2)) / (((customer_service_salience + employee_development_salience + customer_exploitation_salience + employee_exploitation_salience + 1e-9) / 4) + ((accountability_salience + financial_responsibility_salience + opacity_salience + financial_manipulation_salience + 1e-9) / 4) + ((sustainable_purpose_salience + short_term_extraction_salience + 1e-9) / 2))"
  },
  "reliability_rubric": {
    "cronbachs_alpha": {
      "excellent": [0.80, 1.0],
      "good": [0.70, 0.79],
      "acceptable": [0.60, 0.69],
      "poor": [0.0, 0.59]
    },
    "notes": "Defines quality thresholds for framework reliability. The Synthesis Agent uses this for automated fit assessment."
  },
  "gasket_schema": {
    "version": "v7.3",
    "extraction_method": "intelligent_extractor",
    "target_keys": [
      "customer_service_score", "customer_exploitation_score", "employee_development_score", "employee_exploitation_score",
      "accountability_score", "opacity_score", "financial_responsibility_score", "financial_manipulation_score",
      "sustainable_purpose_score", "short_term_extraction_score",
      "customer_service_salience", "customer_exploitation_salience", "employee_development_salience", "employee_exploitation_salience",
      "accountability_salience", "opacity_salience", "financial_responsibility_salience", "financial_manipulation_salience",
      "sustainable_purpose_salience", "short_term_extraction_salience",
      "customer_service_confidence", "customer_exploitation_confidence", "employee_development_confidence", "employee_exploitation_confidence",
      "accountability_confidence", "opacity_confidence", "financial_responsibility_confidence", "financial_manipulation_confidence",
      "sustainable_purpose_confidence", "short_term_extraction_confidence"
    ],
    "extraction_patterns": {
      "customer_service_score": ["customer.{0,20}service.{0,20}score", "customer.{0,20}service.{0,20}rating", "customer\\s*service\\s*:\\s*[0-9]"],
      "customer_exploitation_score": ["customer.{0,20}exploitation.{0,20}score", "customer.{0,20}exploitation.{0,20}rating", "customer\\s*exploitation\\s*:\\s*[0-9]"],
      "employee_development_score": ["employee.{0,20}development.{0,20}score", "employee.{0,20}development.{0,20}rating", "employee\\s*development\\s*:\\s*[0-9]"],
      "employee_exploitation_score": ["employee.{0,20}exploitation.{0,20}score", "employee.{0,20}exploitation.{0,20}rating", "employee\\s*exploitation\\s*:\\s*[0-9]"],
      "accountability_score": ["accountability.{0,20}score", "accountability.{0,20}rating", "accountability\\s*:\\s*[0-9]"],
      "opacity_score": ["opacity.{0,20}score", "opacity.{0,20}rating", "opacity\\s*:\\s*[0-9]"],
      "financial_responsibility_score": ["financial.{0,20}responsibility.{0,20}score", "financial.{0,20}responsibility.{0,20}rating", "financial\\s*responsibility\\s*:\\s*[0-9]"],
      "financial_manipulation_score": ["financial.{0,20}manipulation.{0,20}score", "financial.{0,20}manipulation.{0,20}rating", "financial\\s*manipulation\\s*:\\s*[0-9]"],
      "sustainable_purpose_score": ["sustainable.{0,20}purpose.{0,20}score", "sustainable.{0,20}purpose.{0,20}rating", "sustainable\\s*purpose\\s*:\\s*[0-9]"],
      "short_term_extraction_score": ["short.{0,20}term.{0,20}extraction.{0,20}score", "short.{0,20}term.{0,20}extraction.{0,20}rating", "short\\s*term\\s*extraction\\s*:\\s*[0-9]"],
      "customer_service_salience": ["customer.{0,20}service.{0,20}salience", "customer.{0,20}service.{0,20}importance", "customer.{0,20}service.{0,20}centrality"],
      "customer_exploitation_salience": ["customer.{0,20}exploitation.{0,20}salience", "customer.{0,20}exploitation.{0,20}importance", "customer.{0,20}exploitation.{0,20}centrality"],
      "employee_development_salience": ["employee.{0,20}development.{0,20}salience", "employee.{0,20}development.{0,20}importance", "employee.{0,20}development.{0,20}centrality"],
      "employee_exploitation_salience": ["employee.{0,20}exploitation.{0,20}salience", "employee.{0,20}exploitation.{0,20}importance", "employee.{0,20}exploitation.{0,20}centrality"],
      "accountability_salience": ["accountability.{0,20}salience", "accountability.{0,20}importance", "accountability.{0,20}centrality"],
      "opacity_salience": ["opacity.{0,20}salience", "opacity.{0,20}importance", "opacity.{0,20}centrality"],
      "financial_responsibility_salience": ["financial.{0,20}responsibility.{0,20}salience", "financial.{0,20}responsibility.{0,20}importance", "financial.{0,20}responsibility.{0,20}centrality"],
      "financial_manipulation_salience": ["financial.{0,20}manipulation.{0,20}salience", "financial.{0,20}manipulation.{0,20}importance", "financial.{0,20}manipulation.{0,20}centrality"],
      "sustainable_purpose_salience": ["sustainable.{0,20}purpose.{0,20}salience", "sustainable.{0,20}purpose.{0,20}importance", "sustainable.{0,20}purpose.{0,20}centrality"],
      "short_term_extraction_salience": ["short.{0,20}term.{0,20}extraction.{0,20}salience", "short.{0,20}term.{0,20}extraction.{0,20}importance", "short.{0,20}term.{0,20}extraction.{0,20}centrality"],
      "customer_service_confidence": ["customer.{0,20}service.{0,20}confidence", "customer.{0,20}service.{0,20}certainty", "customer.{0,20}service.{0,20}sure"],
      "customer_exploitation_confidence": ["customer.{0,20}exploitation.{0,20}confidence", "customer.{0,20}exploitation.{0,20}certainty", "customer.{0,20}exploitation.{0,20}sure"],
      "employee_development_confidence": ["employee.{0,20}development.{0,20}confidence", "employee.{0,20}development.{0,20}certainty", "employee.{0,20}development.{0,20}sure"],
      "employee_exploitation_confidence": ["employee.{0,20}exploitation.{0,20}confidence", "employee.{0,20}exploitation.{0,20}certainty", "employee.{0,20}exploitation.{0,20}sure"],
      "accountability_confidence": ["accountability.{0,20}confidence", "accountability.{0,20}certainty", "accountability.{0,20}sure"],
      "opacity_confidence": ["opacity.{0,20}confidence", "opacity.{0,20}certainty", "opacity.{0,20}sure"],
      "financial_responsibility_confidence": ["financial.{0,20}responsibility.{0,20}confidence", "financial.{0,20}responsibility.{0,20}certainty", "financial.{0,20}responsibility.{0,20}sure"],
      "financial_manipulation_confidence": ["financial.{0,20}manipulation.{0,20}confidence", "financial.{0,20}manipulation.{0,20}certainty", "financial.{0,20}manipulation.{0,20}sure"],
      "sustainable_purpose_confidence": ["sustainable.{0,20}purpose.{0,20}confidence", "sustainable.{0,20}purpose.{0,20}certainty", "sustainable.{0,20}purpose.{0,20}sure"],
      "short_term_extraction_confidence": ["short.{0,20}term.{0,20}extraction.{0,20}confidence", "short.{0,20}term.{0,20}extraction.{0,20}certainty", "short.{0,20}term.{0,20}extraction.{0,20}sure"]
    },
    "validation_rules": {
      "required_fields": [
        "customer_service_score", "customer_exploitation_score", "employee_development_score", "employee_exploitation_score",
        "accountability_score", "opacity_score", "financial_responsibility_score", "financial_manipulation_score",
        "sustainable_purpose_score", "short_term_extraction_score"
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
```

</details>