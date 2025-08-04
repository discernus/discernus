# Business Ethics Framework v7.1

**Version**: 7.1  
**Status**: Active  
**Major Change**: Enhanced Gasket Schema with Metadata Scores and Advanced Extraction Patterns

---

## Overview

The Business Ethics Framework v7.1 analyzes business communications across three domains of ethical concern: stakeholder relationships, operational integrity, and strategic vision with enhanced metadata scoring. This advanced framework examines business ethics through distinct domains that represent core areas of corporate responsibility with robust extraction patterns and validation rules.

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
    ],
    "target_dimensions": [
      "stakeholder_focus_index",
      "operational_integrity_index",
      "strategic_sustainability_score"
    ]
  }
}
```

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "business_ethics_v7_1",
  "version": "v7.1",
  "display_name": "Business Ethics Framework v7.1",
  "analysis_variants": {
    "default": {
      "description": "Complete multi-dimensional business ethics analysis with raw analysis log output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert analyst specializing in business ethics and corporate responsibility across diverse contexts. Phase 2: Framework Methodology: Your task is to analyze the provided text using the Business Ethics Framework v7.1, which captures business ethics patterns through three domains with enhanced metadata scoring. Phase 3: Operational Definitions: Evaluate 10 dimensions across three domains: Stakeholder Relations (Customer Service/Exploitation, Employee Development/Exploitation), Operational Integrity (Accountability/Opacity, Financial Responsibility/Manipulation), and Strategic Vision (Sustainable Purpose/Short-Term Extraction). Each dimension receives a score (0.0-1.0), salience weight (0.0-1.0), and confidence rating (0.0-1.0). Phase 4: Scoring Protocol: For each dimension, provide ONLY: (1) score (0.0-1.0), (2) salience (0.0-1.0), (3) confidence (0.0-1.0), (4) evidence quotes with justification. Phase 5: Raw Analysis Log Requirements: Your response must be a raw analysis log containing dimensional scores, evidence, and reasoning - NO JSON structure or derived calculations. Phase 6: Output Specification: Return raw analysis log with dimension scores only - NO calculations of ethics indices or derived metrics (these will be computed by code)."
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
    "strategic_sustainability_score": "(sustainable_purpose_score - short_term_extraction_score + 1) / 2"
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
    "version": "7.1",
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
      "customer_service_score": ["customer.{0,20}service.{0,20}score"],
      "customer_exploitation_score": ["customer.{0,20}exploitation.{0,20}score"],
      "employee_development_score": ["employee.{0,20}development.{0,20}score"],
      "employee_exploitation_score": ["employee.{0,20}exploitation.{0,20}score"],
      "accountability_score": ["accountability.{0,20}score"],
      "opacity_score": ["opacity.{0,20}score"],
      "financial_responsibility_score": ["financial.{0,20}responsibility.{0,20}score"],
      "financial_manipulation_score": ["financial.{0,20}manipulation.{0,20}score"],
      "sustainable_purpose_score": ["sustainable.{0,20}purpose.{0,20}score"],
      "short_term_extraction_score": ["short.{0,20}term.{0,20}extraction.{0,20}score"],
      "customer_service_salience": ["customer.{0,20}service.{0,20}salience"],
      "customer_exploitation_salience": ["customer.{0,20}exploitation.{0,20}salience"],
      "employee_development_salience": ["employee.{0,20}development.{0,20}salience"],
      "employee_exploitation_salience": ["employee.{0,20}exploitation.{0,20}salience"],
      "accountability_salience": ["accountability.{0,20}salience"],
      "opacity_salience": ["opacity.{0,20}salience"],
      "financial_responsibility_salience": ["financial.{0,20}responsibility.{0,20}salience"],
      "financial_manipulation_salience": ["financial.{0,20}manipulation.{0,20}salience"],
      "sustainable_purpose_salience": ["sustainable.{0,20}purpose.{0,20}salience"],
      "short_term_extraction_salience": ["short.{0,20}term.{0,20}extraction.{0,20}salience"],
      "customer_service_confidence": ["customer.{0,20}service.{0,20}confidence"],
      "customer_exploitation_confidence": ["customer.{0,20}exploitation.{0,20}confidence"],
      "employee_development_confidence": ["employee.{0,20}development.{0,20}confidence"],
      "employee_exploitation_confidence": ["employee.{0,20}exploitation.{0,20}confidence"],
      "accountability_confidence": ["accountability.{0,20}confidence"],
      "opacity_confidence": ["opacity.{0,20}confidence"],
      "financial_responsibility_confidence": ["financial.{0,20}responsibility.{0,20}confidence"],
      "financial_manipulation_confidence": ["financial.{0,20}manipulation.{0,20}confidence"],
      "sustainable_purpose_confidence": ["sustainable.{0,20}purpose.{0,20}confidence"],
      "short_term_extraction_confidence": ["short.{0,20}term.{0,20}extraction.{0,20}confidence"]
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
  },
  "raw_analysis_log_format": {
    "description": "Raw analysis log containing business ethics scores, evidence, and reasoning without structured JSON",
    "content": "Free-form text with business ethics analysis including scores, evidence quotes, and qualitative reasoning"
  }
}
```

</details>