# Entman Framing Functions Experiment Corpus: Strategic Communications Analysis

**Corpus Name**: Strategic Communications Framing Analysis  
**Framework**: Entman Framing Functions Framework v10.0  
**Documents**: 4 strategic communications  
**Date**: August 29, 2025  

---

## Corpus Overview

This corpus contains 4 diverse strategic communications designed to test Entman's framing functions theory. The documents range from political campaigns to corporate communications, representing different strategic goals and framing function deployments. Each text is selected to exercise specific dimensions of the four independent framing functions.

## Document Collection

### 1. Crisis Management Statement (synthetic)
**Organization**: TechCorp Inc.  
**Context**: Data breach response  
**Framing Focus**: Problem Definition + Treatment Recommendation  
**Content**: Emphasizes crisis scope and immediate response actions, minimal causal attribution or moral evaluation.

### 2. Political Campaign Attack Ad (synthetic)
**Speaker**: Senator Johnson Campaign  
**Context**: Negative campaign advertisement  
**Framing Focus**: Problem Definition + Causal Attribution + Moral Evaluation  
**Content**: Defines opponent as problem, assigns blame, provides moral judgment, but offers no solutions.

### 3. Corporate Apology Statement (synthetic)
**Organization**: GreenEnergy Corp  
**Context**: Environmental incident apology  
**Framing Focus**: Causal Attribution + Moral Evaluation + Treatment Recommendation  
**Content**: Takes responsibility, expresses moral regret, and outlines corrective actions.

### 4. Policy Advocacy Speech (synthetic)
**Speaker**: Congresswoman Davis  
**Context**: Healthcare reform advocacy  
**Framing Focus**: Problem Definition + Treatment Recommendation  
**Content**: Defines healthcare crisis and proposes comprehensive solutions with minimal blame assignment.


## Corpus Design Rationale

This corpus is designed to provide maximum analytical leverage for the Entman Framing Functions Framework:

1. **Function Variation**: Documents represent different combinations and emphasis patterns of the four framing functions
2. **Strategic Diversity**: Different organizational contexts (political, corporate, NGO) to test framework robustness
3. **Function Independence**: Several documents emphasize specific functions while minimizing others to test independence hypothesis
4. **Message Completeness**: Range from single-function focus to comprehensive four-function deployment
5. **Strategic Complexity**: Documents with varying levels of strategic framing sophistication

## Expected Framework Exercise

The corpus will test the framework's ability to:
- Distinguish between independent framing functions
- Measure the independence of function deployment
- Assess strategic communication patterns
- Validate Entman's systematic framing analysis approach

This corpus design ensures comprehensive testing of the framework's analytical capabilities while maintaining the coherence necessary for meaningful research outcomes.

---

## Document Manifest

```yaml
name: "Strategic Communications Framing Analysis"
version: "1.0"
spec_version: "8.0.2"
total_documents: 4
date_range: "2025"

documents:
  - filename: "crisis_management.txt"
    document_id: "crisis_management"
    metadata:
      organization: "TechCorp Inc"
      context: "crisis_response"
      framing_focus: "problem_definition_treatment"
  - filename: "political_attack_ad.txt"
    document_id: "political_attack_ad"
    metadata:
      speaker: "Senator Johnson Campaign"
      context: "campaign_advertisement"
      framing_focus: "problem_cause_moral"
  - filename: "corporate_apology.txt"
    document_id: "corporate_apology"
    metadata:
      organization: "GreenEnergy Corp"
      context: "apology_statement"
      framing_focus: "cause_moral_treatment"
  - filename: "policy_advocacy.txt"
    document_id: "policy_advocacy"
    metadata:
      speaker: "Congresswoman Davis"
      context: "policy_advocacy"
      framing_focus: "problem_treatment"
```
