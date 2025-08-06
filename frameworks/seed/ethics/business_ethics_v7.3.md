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
      "description": "Complete multi-dimensional business ethics analysis with raw analysis log output.",
      "analysis_prompt": "You are an expert analyst specializing in business ethics and corporate responsibility across diverse contexts. Your task is to analyze the provided text using the Business Ethics Framework v7.3, which captures business ethics patterns through three domains with enhanced metadata scoring and comprehensive corporate responsibility assessment.\n\nThe framework evaluates business ethics across three domains:\n\n**Stakeholder Relations Domain**: Customer Service (0.0-1.0) - genuine customer benefit and transparent value delivery vs. Customer Exploitation (0.0-1.0) - extraction of value from customers over genuine service; Employee Development (0.0-1.0) - worker growth, safety, and meaningful contribution vs. Employee Exploitation (0.0-1.0) - treating workers as disposable resources.\n\n**Operational Integrity Domain**: Accountability (0.0-1.0) - transparent governance and responsible decision-making vs. Opacity (0.0-1.0) - concealing decision-making processes; Financial Responsibility (0.0-1.0) - prudent financial management and honest reporting vs. Financial Manipulation (0.0-1.0) - accounting manipulation or unsustainable practices.\n\n**Strategic Vision Domain**: Sustainable Purpose (0.0-1.0) - long-term value creation for society and stakeholders vs. Short Term Extraction (0.0-1.0) - focusing solely on short-term profit extraction.\n\nFor each dimension, provide:\n- **Score (0.0-1.0)**: Based on strength of evidence in the text\n- **Salience (0.0-1.0)**: How central is this dimension to this specific text?\n- **Confidence (0.0-1.0)**: How certain are you in this assessment?\n\nWrite a comprehensive analytical report that covers:\n- Application of the Business Ethics methodology to this specific text\n- Detailed analysis of each relevant dimension with scores, salience, confidence, and evidence\n- Assessment of business ethics patterns across all three domains\n- Overall corporate responsibility profile with domain weighting\n- Key insights about the organization's ethical approach and stakeholder orientation\n\nEmbed your numerical assessments naturally within the analysis. For example: 'This text demonstrates strong customer service orientation (customer service score: 0.8, salience: 0.9, confidence: 0.7) with frequent references to genuine customer benefit.' Focus on rigorous intellectual analysis supported by direct textual evidence and clear reasoning for all scores and metadata."
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
    "salience_weighted_stakeholder_focus_index": "((customer_service_score * customer_service_salience + employee_development_score * employee_development_salience) - (customer_exploitation_score * customer_exploitation_salience + employee_exploitation_score * employee_exploitation_salience)) / (customer_service_salience + employee_development_salience + customer_exploitation_salience + employee_exploitation_salience)",
    "salience_weighted_operational_integrity_index": "((accountability_score * accountability_salience + financial_responsibility_score * financial_responsibility_salience) - (opacity_score * opacity_salience + financial_manipulation_score * financial_manipulation_salience)) / (accountability_salience + financial_responsibility_salience + opacity_salience + financial_manipulation_salience)",
    "salience_weighted_strategic_sustainability_score": "(sustainable_purpose_score * sustainable_purpose_salience - short_term_extraction_score * short_term_extraction_salience + (sustainable_purpose_salience + short_term_extraction_salience) / 2) / (sustainable_purpose_salience + short_term_extraction_salience)",
    "salience_weighted_business_ethics_index": "(stakeholder_focus_index * ((customer_service_salience + employee_development_salience + customer_exploitation_salience + employee_exploitation_salience) / 4) + operational_integrity_index * ((accountability_salience + financial_responsibility_salience + opacity_salience + financial_manipulation_salience) / 4) + strategic_sustainability_score * ((sustainable_purpose_salience + short_term_extraction_salience) / 2)) / (((customer_service_salience + employee_development_salience + customer_exploitation_salience + employee_exploitation_salience) / 4) + ((accountability_salience + financial_responsibility_salience + opacity_salience + financial_manipulation_salience) / 4) + ((sustainable_purpose_salience + short_term_extraction_salience) / 2))"
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