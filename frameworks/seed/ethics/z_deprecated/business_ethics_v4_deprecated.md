# Business Ethics Framework v4.0
**Version**: v4.0
**Status**: Active

---

## Executive Summary

The Business Ethics Framework analyzes business communications across three domains of ethical concern: stakeholder relationships, operational integrity, and strategic vision using advanced multi-dimensional analysis capabilities.

Based on Freeman's stakeholder theory and Solomon's ethics approach, this framework examines business ethics through three distinct domains that represent core areas of corporate responsibility. The framework implements stakeholder-based ethical analysis with domain-specific clustering, demonstrating how different ethical concerns manifest in distinct areas of business operation.

---

## Theoretical Foundation

This framework is grounded in Freeman's stakeholder theory and Solomon's virtue ethics approach for comprehensive business ethics assessment. The framework integrates stakeholder capitalism analysis with operational integrity evaluation across three distinct domains of corporate responsibility.

### Three Domains of Business Ethics

**1. Stakeholder Relations Domain** - How businesses treat key stakeholders:
- **Customer Relations**: Service orientation vs exploitation patterns
- **Employee Relations**: Development investment vs resource extraction approaches

**2. Operational Integrity Domain** - How businesses manage governance and operations:
- **Governance Transparency**: Accountability vs opacity in decision-making
- **Financial Integrity**: Responsible management vs manipulation practices

**3. Strategic Vision Domain** - How businesses frame long-term purpose:
- **Strategic Purpose**: Sustainable value creation vs short-term extraction focus

### Key References

- Freeman, R. E. (1984). Strategic Management: A Stakeholder Approach. Pitman.
- Solomon, R. C. (1992). Ethics and Excellence: Cooperation and Integrity in Business. Oxford University Press.
- Freeman, R. E., Harrison, J. S., Wicks, A. C., Parmar, B. L., & De Colle, S. (2010). Stakeholder Theory: The State of the Art. Cambridge University Press.

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

## Analytical Methodology

This framework employs a systematic approach to business ethics analysis:

1. **Domain Analysis**: Each of the three ethics domains (stakeholder relations, operational integrity, strategic vision) is evaluated independently
2. **Dimension Scoring**: Each ethical dimension is scored from 0.0 to 1.0 based on evidence strength
3. **Evidence Collection**: Approximately 2 direct quotations per dimension to support scoring
4. **Confidence Assessment**: Analyst confidence rated based on evidence clarity and consistency
5. **Pattern Recognition**: Identification of overall ethical orientation and stakeholder vs shareholder emphasis

## Academic Validation

Framework validated through stakeholder theory research and business ethics literature. Enhanced stakeholder theory implementation with comprehensive business ethics assessment across three distinct domains of corporate responsibility. Integrates Freeman's stakeholder approach with Solomon's virtue ethics for complete ethical evaluation framework.

---

<details><summary>Machine-Readable Configuration</summary>

```json
{
  "name": "business_ethics",
  "version": "v4.0",
  "display_name": "Business Ethics Framework v4.0",
  "analysis_variants": {
    "default": {
      "description": "Complete implementation of the Business Ethics Framework methodology",
      "analysis_prompt": "You are an expert analyst with deep knowledge of moral psychology, political discourse, and value analysis. Your task is to analyze the provided text using Business Ethics Framework. The Business Ethics Framework analyzes business communications across three domains of ethical concern: stakeholder relationships, operational integrity, and strategic vision using advanced multi-dimensional analysis capabilities. This framework examines the following dimensions: - **Customer Service**: Prioritizes genuine customer benefit and transparent value delivery (look for: customer success, genuine value, long-term relationship, customer feedback, solving real problems) - **Customer Exploitation**: Prioritizes extraction of value from customers over genuine service (look for: maximize extraction, hidden fees, planned obsolescence, vendor lock-in, dark patterns) - **Employee Development**: Invests in worker growth, safety, and meaningful contribution (look for: employee growth, professional development, workplace safety, meaningful work, work-life balance) - **Employee Exploitation**: Treats workers as disposable resources for profit extraction (look for: human resources, cost cutting, efficiency gains, lean operations, expendable workforce) - **Accountability**: Demonstrates transparent governance and responsible decision-making (look for: transparent governance, accountable leadership, open decision-making, stakeholder input, ethical standards) - **Opacity**: Conceals decision-making processes and avoids accountability (look for: proprietary information, confidential strategy, need to know basis, trade secrets, competitive advantage) - **Financial Responsibility**: Demonstrates prudent financial management and honest reporting (look for: sustainable growth, prudent management, accurate reporting, financial discipline, long-term stability) - **Financial Manipulation**: Engages in accounting manipulation or unsustainable financial practices (look for: aggressive accounting, revenue recognition, financial engineering, off-balance sheet, creative bookkeeping) - **Sustainable Purpose**: Articulates long-term value creation for society and stakeholders (look for: sustainable impact, societal benefit, long-term value, positive contribution, meaningful mission) - **Short Term Extraction**: Focuses solely on short-term profit extraction without regard for long-term consequences (look for: quarterly results, shareholder value, cost optimization, market efficiency, competitive advantage) For each dimension, follow this process: 1. Read the text systematically for relevant patterns and language 2. Identify specific evidence and quotations 3. Score the dimension from 0.0 to 1.0 based on strength and frequency of evidence 4. Provide approximately 2 direct quotations supporting each score 5. Assess your confidence in the scoring based on evidence clarity"
    }
  },
  "output_contract": {
    "schema": {
      "worldview": "string",
      "customer_service_score": "number",
      "customer_service_confidence": "number",
      "customer_service_evidence": "array",
      "customer_exploitation_score": "number",
      "customer_exploitation_confidence": "number",
      "customer_exploitation_evidence": "array",
      "employee_development_score": "number",
      "employee_development_confidence": "number",
      "employee_development_evidence": "array",
      "employee_exploitation_score": "number",
      "employee_exploitation_confidence": "number",
      "employee_exploitation_evidence": "array",
      "accountability_score": "number",
      "accountability_confidence": "number",
      "accountability_evidence": "array",
      "opacity_score": "number",
      "opacity_confidence": "number",
      "opacity_evidence": "array",
      "financial_responsibility_score": "number",
      "financial_responsibility_confidence": "number",
      "financial_responsibility_evidence": "array",
      "financial_manipulation_score": "number",
      "financial_manipulation_confidence": "number",
      "financial_manipulation_evidence": "array",
      "sustainable_purpose_score": "number",
      "sustainable_purpose_confidence": "number",
      "sustainable_purpose_evidence": "array",
      "short_term_extraction_score": "number",
      "short_term_extraction_confidence": "number",
      "short_term_extraction_evidence": "array",
      "overall_analysis_confidence": "number",
      "key_patterns_observed": "string"
    },
    "instructions": "IMPORTANT: Your response MUST be a single, valid JSON object and nothing else. Do not include any text, explanations, or markdown code fences before or after the JSON object."
  },
  "calculation_spec": {
    "stakeholder_focus_index": "Stakeholder-oriented scores vs shareholder-oriented scores",
    "operational_integrity_index": "Governance and financial responsibility anchor scores",
    "strategic_sustainability_score": "Strategic vision domain ethical positioning"
  }
}
```

</details>