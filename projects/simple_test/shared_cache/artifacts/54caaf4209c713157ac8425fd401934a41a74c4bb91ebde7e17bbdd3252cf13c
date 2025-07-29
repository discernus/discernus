# Business Ethics Framework v5.0
**Version**: 5.0
**Status**: Active
**Major Change**: Embedded CSV Architecture for Synthesis Scalability

---

## Executive Summary

The Business Ethics Framework analyzes business communications across three domains of ethical concern: stakeholder relationships, operational integrity, and strategic vision using advanced multi-dimensional analysis capabilities.

Based on Freeman's stakeholder theory and Solomon's ethics approach, this framework examines business ethics through three distinct domains that represent core areas of corporate responsibility. The framework implements stakeholder-based ethical analysis with domain-specific clustering, demonstrating how different ethical concerns manifest in distinct areas of business operation.

---

## Framework Dimensions

### Customer Service

Prioritizes genuine customer benefit and transparent value delivery. This represents authentic commitment to customer success through honest communication and transparent practices.

**Key Indicators:**
- customer success, genuine value, long-term relationship, customer feedback
- solving real problems, transparent pricing, honest communication, customer-first

### Customer Exploitation

Prioritizes extraction of value from customers over genuine service. This represents manipulative practices designed to maximize revenue extraction rather than deliver authentic value.

**Key Indicators:**
- maximize extraction, hidden fees, planned obsolescence, vendor lock-in
- dark patterns, manipulative marketing, bait and switch, profit maximization

### Employee Development

Invests in worker growth, safety, and meaningful contribution. This represents viewing employees as valuable assets deserving investment and development opportunities.

**Key Indicators:**
- employee growth, professional development, workplace safety, meaningful work
- work-life balance, fair compensation, career advancement, team empowerment

### Employee Exploitation

Treats workers as disposable resources for profit extraction. This represents viewing employees primarily as costs to be minimized rather than assets to develop.

**Key Indicators:**
- human resources, cost cutting, efficiency gains, lean operations
- expendable workforce, maximize productivity, reduce labor costs, workforce optimization

### Accountability

Demonstrates transparent governance and responsible decision-making. This represents commitment to open processes and stakeholder engagement in business decisions.

**Key Indicators:**
- transparent governance, accountable leadership, open decision-making, stakeholder input
- ethical standards, responsible practices, oversight mechanisms, public reporting

### Opacity

Conceals decision-making processes and avoids accountability. This represents preference for closed, secretive decision-making without external scrutiny.

**Key Indicators:**
- proprietary information, confidential strategy, need to know basis, trade secrets
- competitive advantage, internal matters, executive privilege, strategic confidentiality

### Financial Responsibility

Demonstrates prudent financial management and honest reporting. This represents commitment to accurate, conservative financial practices and transparent reporting.

**Key Indicators:**
- sustainable growth, prudent management, accurate reporting, financial discipline
- long-term stability, responsible investment, sound fundamentals, fiscal responsibility

### Financial Manipulation

Engages in accounting manipulation or unsustainable financial practices. This represents using accounting flexibility to obscure true financial performance.

**Key Indicators:**
- aggressive accounting, revenue recognition, financial engineering, off-balance sheet
- creative bookkeeping, earnings management, regulatory arbitrage, financial optimization

### Sustainable Purpose

Articulates long-term value creation for society and stakeholders. This represents commitment to creating lasting positive impact beyond immediate profit.

**Key Indicators:**
- sustainable impact, societal benefit, long-term value, positive contribution
- meaningful mission, stakeholder capitalism, social responsibility, environmental stewardship

### Short Term Extraction

Focuses solely on short-term profit extraction without regard for long-term consequences. This represents prioritizing immediate financial returns over sustainable value creation.

**Key Indicators:**
- quarterly results, shareholder value, cost optimization, market efficiency
- competitive advantage, profit maximization, operational leverage, margin expansion

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "business_ethics_v5_0",
  "version": "v5.0",
  "display_name": "Business Ethics Framework v5.0",
  "analysis_variants": {
    "default": {
      "description": "Complete multi-dimensional business ethics analysis with embedded CSV output.",
      "analysis_prompt": "Phase 1: Cognitive Priming: You are an expert analyst in business ethics. Phase 2: Framework Methodology: Your task is to analyze the text using the Business Ethics Framework v5.0. Phase 3: Operational Definitions: Evaluate ten dimensions across three domains: Stakeholder Relations (Customer Service/Exploitation, Employee Development/Exploitation), Operational Integrity (Accountability/Opacity, Financial Responsibility/Manipulation), and Strategic Vision (Sustainable Purpose/Short-Term Extraction). Phase 4: Scoring Protocol: Score each of the ten dimensions from 0.0 to 1.0 and provide the strongest 1-2 quotes as evidence. Phase 5: Embedded CSV Generation: CRITICAL: Your response must include two embedded CSV segments using these exact delimiters: <<<DISCERNUS_SCORES_CSV_v1>>> and <<<DISCERNUS_EVIDENCE_CSV_v1>>>. The scores CSV must have columns for each of the ten dimension scores. The evidence CSV must have columns for dimension, quote, and confidence. Phase 6: Output Specification: Return a complete response containing both a comprehensive JSON analysis and the embedded CSV segments as specified in the output_contract."
    }
  },
  "dimension_groups": {
    "stakeholder_relations": ["customer_service", "customer_exploitation", "employee_development", "employee_exploitation"],
    "operational_integrity": ["accountability", "opacity", "financial_responsibility", "financial_manipulation"],
    "strategic_vision": ["sustainable_purpose", "short_term_extraction"]
  },
  "calculation_spec": {
    "stakeholder_focus_index": "(customer_service + employee_development) - (customer_exploitation + employee_exploitation)",
    "operational_integrity_index": "(accountability + financial_responsibility) - (opacity + financial_manipulation)",
    "strategic_sustainability_score": "sustainable_purpose - short_term_extraction"
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
  "output_contract": {
    "schema": {
      "worldview": "string",
      "scores": "object",
      "evidence": "object",
      "reasoning": "object"
    },
    "embedded_csv_requirements": {
      "scores_csv": {
        "delimiter_start": "<<<DISCERNUS_SCORES_CSV_v1>>>",
        "delimiter_end": "<<<END_DISCERNUS_SCORES_CSV_v1>>>",
        "description": "CSV for all dimensional scores and calculated indices."
      },
      "evidence_csv": {
        "delimiter_start": "<<<DISCERNUS_EVIDENCE_CSV_v1>>>",
        "delimiter_end": "<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>",
        "description": "CSV for structured evidence data for audit and replication."
      }
    },
    "instructions": "IMPORTANT: Your response MUST include both a complete JSON analysis AND embedded CSV segments using the exact delimiters specified."
  }
}
```

</details> 