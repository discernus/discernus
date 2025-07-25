# Framework Specification Validation Rubric v1.0
## Generic Requirements for Discernus-Compatible Analytical Frameworks

**Purpose**: This specification provides validation criteria for determining whether an analytical framework is ready for Discernus analysis. Any framework meeting these requirements can be validated by an LLM and approved for systematic research.

**Usage**: LLMs will use this rubric to evaluate researcher-submitted frameworks before analysis begins.

---

## Core Framework Requirements

### 1. Framework Identity & Scope ✅

**Required Elements:**
- [ ] **Clear Framework Name** and version number
- [ ] **Explicit Purpose Statement** - what the framework analyzes and why
- [ ] **Defined Scope** - what types of texts/content it applies to
- [ ] **Theoretical Foundation** - underlying academic/theoretical basis
- [ ] **Analysis Unit Specification** - what gets analyzed (sentences, documents, etc.)

**Validation Questions for LLM:**
- Does the framework clearly state what it measures?
- Is the scope of application well-defined?
- Is there sufficient theoretical justification?

### 2. Dimensional Structure ✅

**Required Elements:**
- [ ] **Defined Dimensions/Axes** - at least 2, maximum 8 analytical dimensions
- [ ] **Dimension Descriptions** - clear explanation of what each dimension measures
- [ ] **Dimensional Relationships** - how dimensions relate to each other (orthogonal, competitive, hierarchical)
- [ ] **Weighting System** - relative importance of each dimension (if applicable)

**Validation Questions for LLM:**
- Are the dimensions clearly distinct from each other?
- Is the relationship between dimensions explicitly stated?
- Can each dimension be independently assessed?

### 3. Scoring Methodology ✅

**Required Elements:**
- [ ] **Scale Definition** - clear scoring scale (e.g., 0.0-1.0, 1-7, categorical)
- [ ] **Score Interpretation** - what each score level means
- [ ] **Evidence Requirements** - what constitutes evidence for each score
- [ ] **Confidence Assessment** - how to evaluate certainty of scores
- [ ] **Boundary Cases** - guidance for ambiguous situations

**Validation Questions for LLM:**
- Is the scoring scale clearly defined and consistently applicable?
- Are there clear criteria for determining scores?
- Is there guidance for handling uncertain cases?

### 4. Language and Evidence Specifications ✅

**Required Elements:**
- [ ] **Linguistic Indicators** - specific words, phrases, or patterns for each dimension
- [ ] **Evidence Types** - what constitutes valid evidence (lexical, semantic, rhetorical)
- [ ] **Context Sensitivity** - how context affects interpretation
- [ ] **Citation Requirements** - how to document evidence from source text
- [ ] **Multi-level Analysis** - guidance for analyzing at different text levels (word, sentence, paragraph, document)

**Validation Questions for LLM:**
- Are there specific, identifiable language patterns provided?
- Is there sufficient guidance for finding and interpreting evidence?
- Can evidence be clearly linked to specific scores?

### 5. Internal Coherence ✅

**Required Elements:**
- [ ] **Consistent Terminology** - terms used consistently throughout
- [ ] **Non-contradictory Logic** - no internal contradictions in framework logic
- [ ] **Complete Coverage** - all dimensions adequately specified
- [ ] **Clear Decision Rules** - unambiguous guidance for difficult cases
- [ ] **Theoretical Alignment** - all components align with stated theoretical foundation

**Validation Questions for LLM:**
- Are there any internal contradictions in the framework?
- Is the terminology used consistently?
- Do all components work together coherently?

### 6. Analytical Outputs ✅

**Required Elements:**
- [ ] **Output Format Specification** - exactly what the analysis should produce
- [ ] **Quantitative Components** - numerical scores, ratings, or measurements
- [ ] **Qualitative Components** - interpretive analysis, evidence citations, reasoning
- [ ] **Uncertainty Documentation** - how to express confidence and limitations
- [ ] **Synthesis Requirements** - how to integrate findings across dimensions

**Validation Questions for LLM:**
- Is it clear what the final analysis should look like?
- Are both quantitative and qualitative outputs specified?
- Is there guidance for expressing uncertainty?

---

## Framework Quality Standards

### Completeness Threshold: 85%
- Framework must meet at least 85% of all specified requirements
- Critical requirements (scoring, evidence, coherence) must be 100% complete
- Minor gaps in non-critical areas may be acceptable with clear documentation

### Validation Process ✅

**Step 1: Automated Checklist**
LLM evaluates framework against all required elements using binary pass/fail

**Step 2: Coherence Assessment**
LLM assesses internal consistency and logical coherence

**Step 3: Practical Application Test**
LLM attempts to apply framework to a sample text to verify usability

**Step 4: Gap Documentation**
LLM documents any missing elements or areas needing clarification

**Step 5: Approval Recommendation**
LLM provides clear pass/fail recommendation with rationale

---

## Common Framework Types Supported

### Dimensional Frameworks (like CFF)
- Multiple orthogonal or competitive dimensions
- Quantitative scoring on each dimension
- Examples: Political psychology frameworks, emotional analysis frameworks

### Categorical Frameworks
- Discrete categories rather than continuous dimensions
- Classification-based analysis
- Examples: Speech act frameworks, discourse type classification

### Process Frameworks
- Sequential or developmental analysis
- Focus on patterns over time or stages
- Examples: Argumentation frameworks, narrative structure analysis

### Hybrid Frameworks
- Combination of dimensional and categorical elements
- Multiple analysis types within single framework
- Examples: Multi-level discourse analysis, integrated rhetorical frameworks

---

## Framework Specification Template

### Basic Template Structure:
```yaml
framework_name: "Your Framework Name"
version: "1.0"
purpose: "What this framework analyzes and why"
scope: "Types of texts/content this applies to"
theoretical_foundation: "Academic basis and citations"

dimensions:
  dimension_1:
    name: "Dimension Name"
    description: "What this measures"
    scale: "0.0-1.0" # or other scale
    evidence_types: ["lexical", "semantic", "rhetorical"]
    language_indicators:
      - "specific words or phrases"
      - "semantic patterns"
    scoring_criteria:
      low: "0.0-0.3: Description of low scores"
      medium: "0.4-0.6: Description of medium scores"
      high: "0.7-1.0: Description of high scores"

output_requirements:
  quantitative: "Numerical scores for each dimension"
  qualitative: "Evidence citations and reasoning"
  confidence: "Uncertainty assessment for each score"
  synthesis: "Overall interpretation and conclusions"
```

---

## LLM Validation Instructions

When evaluating a framework submission, follow this protocol:

### 1. **Initial Assessment**
- Read through entire framework submission
- Identify all components present
- Note any obvious gaps or issues

### 2. **Systematic Evaluation**
- Use the checklist above to evaluate each requirement
- Score each section as Pass/Fail with brief justification
- Document specific missing elements

### 3. **Coherence Check**
- Look for internal contradictions
- Verify terminology consistency
- Check theoretical alignment

### 4. **Practical Test**
- Select a short sample text (provided separately)
- Attempt to apply the framework
- Note any difficulties or ambiguities

### 5. **Final Recommendation**
```
FRAMEWORK VALIDATION RESULT

Framework: [Name and Version]
Overall Assessment: PASS/FAIL
Completeness Score: [X]%

Required Improvements (if any):
- Specific gap 1
- Specific gap 2

Approval Status: APPROVED/NEEDS REVISION/REJECTED
Rationale: [Clear explanation of decision]

Ready for Discernus Analysis: YES/NO
```

---

## Success Criteria

A framework **PASSES** validation if:
- ✅ Meets 85%+ of all requirements
- ✅ 100% complete on critical elements (scoring, evidence, coherence)
- ✅ No internal contradictions
- ✅ Successfully applies to sample text
- ✅ Produces interpretable results

A framework **NEEDS REVISION** if:
- ⚠️ Meets 70-84% of requirements
- ⚠️ Minor gaps in critical elements
- ⚠️ Minor inconsistencies that can be easily fixed

A framework **FAILS** validation if:
- ❌ Meets <70% of requirements
- ❌ Major gaps in critical elements
- ❌ Significant internal contradictions
- ❌ Cannot be successfully applied

---

## Benefits of This Approach

### For Researchers:
- **Clear Standards**: Know exactly what's required before submission
- **Quality Assurance**: Confidence that framework will work in Discernus
- **Flexibility**: Many different framework types supported

### For Discernus:
- **Quality Control**: Only well-defined frameworks enter the system
- **Framework Agnostic**: Works with any framework meeting standards
- **Automated Validation**: LLMs can efficiently evaluate submissions

### For the Research Community:
- **Reproducibility**: Clear standards enable replication
- **Innovation**: Encourages development of novel frameworks
- **Quality**: Raises bar for analytical framework development

This rubric ensures that researchers come to Discernus with well-prepared, coherent frameworks while maintaining flexibility for diverse analytical approaches. 