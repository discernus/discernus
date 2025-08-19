# Framework Specification (v8.0)

**Version**: 8.0  
**Status**: Current Standard  
**Replaces**: v7.3

---

## Introduction

A Discernus v8.0 framework is a human-readable markdown file that serves as the analytical lens for rigorous, repeatable text analysis. The v8.0 specification prioritizes **human readability** and **THIN architecture compliance** while maintaining the analytical rigor required for academic research.

The core innovation of v8.0 is the elimination of complex JSON appendices in favor of **semantic content that LLMs can understand directly**. This creates a more maintainable, readable, and THIN-compliant analytical tool.

---

## Core Principles

1. **Human-First Design**: Frameworks should be readable by researchers, not just machines
2. **THIN Architecture**: LLMs handle semantic understanding, not complex parsing
3. **Analytical Rigor**: Maintain scientific validity through clear methodology
4. **Evidence-Based Analysis**: All scores must be supported by textual evidence
5. **Sequential Analysis**: Chain-of-thought methodology for consistency
6. **Salience Weighting**: Dynamic emphasis-based scoring
7. **Confidence Assessment**: Explicit uncertainty quantification

---

## File Structure

### Required Sections

#### 1. **Framework Header**
```markdown
# Framework Name v8.0

## Research Purpose
Brief description of what the framework measures and why.
```

#### 2. **Analysis Requirements**
```markdown
## Analysis Requirements
- **Score Range**: All dimensions scored 0.0-1.0
- **Evidence Required**: Supporting textual quotes for each dimension score
- **Salience Weighting**: Score prominence based on textual frequency and emphasis
- **Confidence Assessment**: Analyst certainty for each dimensional score (0.0-1.0)
```

#### 3. **Dimensions**
Each dimension must include:
```markdown
### **Dimension Name** (0.0-1.0)
Brief conceptual definition
- **Linguistic Markers**: Specific textual patterns and semantic spaces
- **Evidence**: Type of supporting quotes required
- **Salience**: How to assess prominence/emphasis
```

#### 4. **Calculations** (Optional but Recommended)
```markdown
## Calculations

### **Derived Metrics**
- **Metric Name**: `mathematical_formula`
  - Conceptual explanation
  - Range and interpretation

### **Composite Indices** 
- **Index Name**: `complex_formula`
  - Comprehensive measure description
  - Range and interpretation
```

#### 5. **Analysis Methodology**
```markdown
## Analysis Methodology

**Sequential Chain-of-Thought Analysis**: Examine each dimension group independently before integration.

### **Step-by-Step Process**
1. **Step Name**: Focus description
2. **Step Name**: Focus description
...

### **For Each Step**
- **Score** the dimension (0.0-1.0) with specific textual evidence
- **Assess salience** (0.0-1.0): How central is this appeal?
- **State confidence** (0.0-1.0): How certain are you?
- **Show your work**: Explain reasoning and provide supporting quotes
```

#### 6. **Expected Output Structure**
```markdown
## Expected Output Structure
```yaml
analysis_metadata:
  framework_name: framework_identifier
  framework_version: v8.0
  analyst_confidence: 0.0-1.0
  analysis_notes: "Brief methodology description"

document_analyses:
  - document_id: "unique_identifier"
    document_name: "filename.txt"
    dimensional_scores:
      dimension_name:
        raw_score: 0.0-1.0
        salience: 0.0-1.0
        confidence: 0.0-1.0
    evidence:
      - dimension: "dimension_name"
        quote_text: "Supporting textual evidence"
        confidence: 0.0-1.0
        context_type: "direct_statement|implication|pattern"
```
```

### Optional Sections

#### **Advanced Metrics** (For Complex Frameworks)
Mathematical formulations for tension analysis, strategic indices, etc.

#### **Research Foundations** (For Academic Frameworks)  
Theoretical grounding with citations.

#### **Reliability and Validity**
Discussion of framework reliability measures and validation.

---

## Validation Rules

### Required Elements
- ✅ Framework name and version in header
- ✅ Research purpose statement
- ✅ Analysis requirements section
- ✅ At least 2 dimensions with linguistic markers
- ✅ Analysis methodology with sequential steps
- ✅ Expected output structure in YAML

### Dimension Requirements
Each dimension must specify:
- ✅ Conceptual definition
- ✅ Score range (0.0-1.0)
- ✅ Linguistic markers or semantic patterns
- ✅ Evidence requirements
- ✅ Salience assessment guidance

### Output Structure Requirements
- ✅ YAML format (not JSON)
- ✅ Structured dimensional scores with raw_score, salience, confidence
- ✅ Evidence array with quotes and confidence measures
- ✅ Analysis metadata with framework identification

---

## Migration from v7.3

### Key Changes
- **Removed**: JSON appendix with machine-executable instructions
- **Removed**: Collapsible `<details>` sections  
- **Added**: Inline YAML output specification
- **Enhanced**: Human-readable linguistic markers
- **Simplified**: Direct semantic content for LLM processing

### Compatibility
- **v8.0 frameworks** are NOT compatible with v7.3 orchestration systems
- **v7.3 frameworks** are NOT compatible with v8.0 function generation agents
- **Migration tools** are not provided - frameworks should be rewritten for v8.0

---

## Best Practices

### Framework Design
- **Focus on clarity**: Write for human researchers first
- **Provide examples**: Include specific linguistic markers
- **Explain rationale**: Justify analytical choices
- **Test iteratively**: Validate with sample analyses

### Dimension Definition
- **Be specific**: Avoid vague conceptual definitions
- **Provide markers**: Give concrete textual patterns to look for
- **Explain salience**: Clarify how to assess prominence
- **Require evidence**: Always demand supporting quotes

### Analysis Methodology
- **Sequential steps**: Break complex analysis into focused phases
- **Show work requirement**: Demand explicit reasoning
- **Confidence assessment**: Quantify analytical uncertainty
- **Integration phase**: Synthesize findings systematically

---

## Example v8.0 Framework Structure

```markdown
# Example Framework v8.0

## Research Purpose
Measure democratic discourse patterns through identity and emotional dimensions.

## Analysis Requirements
- **Score Range**: All dimensions scored 0.0-1.0
- **Evidence Required**: Supporting textual quotes for each dimension score
- **Salience Weighting**: Score prominence based on textual frequency and emphasis  
- **Confidence Assessment**: Analyst certainty for each dimensional score (0.0-1.0)

## Dimensions

### **Democratic Appeal** (0.0-1.0)
References to democratic values, processes, and institutions
- **Linguistic Markers**: "democracy", "voting", "representation", "constitution"
- **Evidence**: Direct statements about democratic processes
- **Salience**: Weight by centrality to main argument

### **Authoritarian Appeal** (0.0-1.0) 
References to strong leadership, order, and centralized control
- **Linguistic Markers**: "strong leader", "law and order", "decisive action"
- **Evidence**: Statements favoring centralized authority
- **Salience**: Weight by emphasis and repetition

## Analysis Methodology

**Sequential Chain-of-Thought Analysis**: Examine each dimension independently.

### **Step-by-Step Process**
1. **Democratic Patterns**: Focus ONLY on democratic appeal indicators
2. **Authoritarian Patterns**: Focus ONLY on authoritarian appeal indicators  
3. **Integration**: Calculate derived metrics and assess patterns

### **For Each Step**
- **Score** the dimension (0.0-1.0) with specific textual evidence
- **Assess salience** (0.0-1.0): How central is this appeal?
- **State confidence** (0.0-1.0): How certain are you?
- **Show your work**: Explain reasoning and provide supporting quotes

## Expected Output Structure
```yaml
analysis_metadata:
  framework_name: example_framework
  framework_version: v8.0
  analyst_confidence: 0.85
  analysis_notes: "Sequential analysis of democratic vs authoritarian appeals"

document_analyses:
  - document_id: "doc_001"
    document_name: "speech.txt"
    dimensional_scores:
      democratic_appeal:
        raw_score: 0.7
        salience: 0.8
        confidence: 0.9
      authoritarian_appeal:
        raw_score: 0.3
        salience: 0.4
        confidence: 0.8
    evidence:
      - dimension: "democratic_appeal"
        quote_text: "We must strengthen our democratic institutions"
        confidence: 0.9
        context_type: "direct_statement"
```
```

This example demonstrates the v8.0 approach: human-readable content that LLMs can process directly without complex parsing or JSON schemas.
