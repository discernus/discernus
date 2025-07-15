# Experiment Specification Validation Rubric v1.0
## Generic Requirements for Discernus-Compatible Research Experiments

**Purpose**: This specification provides validation criteria for determining whether a research experiment design is ready for Discernus analysis. Any experiment meeting these requirements can be validated by an LLM and approved for systematic execution.

**Usage**: LLMs will use this rubric to evaluate researcher-submitted experiment designs before analysis begins.

---

## Core Experiment Requirements

### 1. Research Foundation ✅

**Required Elements:**
- [ ] **Clear Research Question** - specific, answerable question
- [ ] **Literature Context** - relevant prior research and gaps
- [ ] **Theoretical Justification** - why this research matters
- [ ] **Scope Definition** - boundaries and limitations of the study
- [ ] **Expected Contribution** - what new knowledge this will generate

**Validation Questions for LLM:**
- Is the research question clearly articulated and specific?
- Is there adequate context from prior research?
- Is the theoretical justification compelling?

### 2. Hypothesis Specification ✅

**Required Elements:**
- [ ] **Falsifiable Hypotheses** - testable predictions that can be proven wrong
- [ ] **Directional Predictions** - specific expected outcomes
- [ ] **Operational Definitions** - precise definitions of key concepts
- [ ] **Causal Logic** - clear reasoning linking theory to predictions
- [ ] **Alternative Hypotheses** - competing explanations considered

**Validation Questions for LLM:**
- Are the hypotheses specific and testable?
- Can these hypotheses potentially be falsified by evidence?
- Are key concepts operationally defined?

### 3. Dataset Specification ✅

**Required Elements:**
- [ ] **Corpus Description** - what texts/materials will be analyzed
- [ ] **Sample Size Justification** - adequate sample for meaningful analysis
- [ ] **Selection Criteria** - clear inclusion/exclusion rules
- [ ] **Data Quality Assessment** - verification of data suitability
- [ ] **Representativeness** - how sample relates to broader population
- [ ] **Ethical Considerations** - appropriate use permissions and privacy

**Validation Questions for LLM:**
- Is the dataset adequate for testing the hypotheses?
- Are selection criteria clearly specified and appropriate?
- Is the sample size sufficient for meaningful conclusions?

### 4. Framework-Experiment Alignment ✅

**Required Elements:**
- [ ] **Framework Suitability** - analytical framework appropriate for research question
- [ ] **Variable Mapping** - clear connection between framework dimensions and research variables
- [ ] **Measurement Validity** - framework measures what the research claims to study
- [ ] **Framework Limitations** - acknowledgment of what framework cannot capture
- [ ] **Alternative Frameworks** - consideration of other analytical approaches

**Validation Questions for LLM:**
- Does the chosen framework actually measure the concepts in the research question?
- Are there clear connections between framework outputs and research variables?
- Have framework limitations been appropriately acknowledged?

### 5. Analysis Plan ✅

**Required Elements:**
- [ ] **Analysis Strategy** - step-by-step analysis approach
- [ ] **Statistical Methods** - appropriate analytical techniques
- [ ] **Validation Procedures** - how results will be verified
- [ ] **Quality Controls** - systematic quality assurance measures
- [ ] **Interpretation Guidelines** - how to interpret different types of findings
- [ ] **Ensemble Specifications** - if using multiple LLMs or multi-run analysis, specify requirements
  - Model selection criteria (e.g., "4 most advanced models", "mix of local and cloud")
  - Budget constraints (e.g., "$50 maximum cost")
  - Statistical requirements (e.g., "inter-rater reliability analysis", "Cronbach's alpha")
  - Performance requirements (e.g., "must handle 1000 texts per batch")
  - **Note**: System will evaluate feasibility and guide you toward viable alternatives if constraints cannot be met

**Validation Questions for LLM:**
- Is the analysis strategy appropriate for the research question and data?
- Are planned statistical methods suitable for the data type and sample size?
- Are there adequate quality control measures?

### 6. Expected Outcomes & Contingencies ✅

**Required Elements:**
- [ ] **Predicted Results** - specific expected findings
- [ ] **Significance Thresholds** - what constitutes meaningful results
- [ ] **Null Result Interpretation** - how to handle non-significant findings
- [ ] **Unexpected Findings Protocol** - how to handle surprising results
- [ ] **Practical Significance** - real-world importance beyond statistical significance

**Validation Questions for LLM:**
- Are expected outcomes clearly specified?
- Is there a plan for handling different types of results?
- Are significance thresholds appropriate and justified?

---

## Experiment Quality Standards

### Completeness Threshold: 90%
- Experiment must meet at least 90% of all specified requirements
- Critical requirements (hypotheses, dataset, analysis plan) must be 100% complete
- Higher bar than frameworks due to importance of experimental rigor

### Validation Process ✅

**Step 1: Foundation Assessment**
LLM evaluates research question, literature context, and theoretical justification

**Step 2: Hypothesis Evaluation**
LLM assesses falsifiability, specificity, and operational definitions

**Step 3: Dataset Validation**
LLM checks dataset adequacy, selection criteria, and ethical considerations

**Step 4: Framework-Experiment Fit**
LLM evaluates alignment between analytical framework and research objectives

**Step 5: Analysis Plan Review**
LLM assesses appropriateness of planned analytical approach

**Step 6: Contingency Planning**
LLM evaluates preparedness for different types of results

**Step 7: Overall Viability Assessment**
LLM provides integrated evaluation of experiment feasibility and quality

---

## Common Experiment Types Supported

### Descriptive Studies
- **Purpose**: Map patterns and characteristics in corpus
- **Requirements**: Representative sampling, clear measurement criteria
- **Examples**: Emotional climate analysis, rhetorical strategy prevalence

### Comparative Studies  
- **Purpose**: Compare different groups, time periods, or conditions
- **Requirements**: Appropriate comparison groups, controlled variables
- **Examples**: Speaker comparisons, temporal trend analysis, cross-cultural studies

### Hypothesis-Testing Studies
- **Purpose**: Test specific theoretical predictions
- **Requirements**: Falsifiable hypotheses, adequate statistical power
- **Examples**: Framework validation, intervention effects, causal claims

### Exploratory Studies
- **Purpose**: Generate insights for future hypothesis development
- **Requirements**: Systematic exploration protocols, discovery validation
- **Examples**: New framework development, pattern identification, theory building

### Mixed-Method Studies
- **Purpose**: Combine quantitative and qualitative approaches
- **Requirements**: Integration strategy, complementary methods
- **Examples**: Framework analysis + qualitative validation, multi-level analysis

---

## Experiment Specification Template

### Basic Template Structure:
```yaml
experiment_name: "Your Experiment Title"
research_question: "Specific question being investigated"
theoretical_background: "Relevant theory and prior research"

hypotheses:
  primary_hypothesis:
    statement: "Specific testable prediction"
    rationale: "Why you expect this result"
    operationalization: "How concepts are measured"
  
  alternative_hypotheses:
    - "Competing explanation 1"
    - "Competing explanation 2"

dataset:
  corpus_description: "What texts will be analyzed"
  sample_size: 100  # Number of texts/documents
  selection_criteria:
    inclusion: ["Criterion 1", "Criterion 2"]
    exclusion: ["Criterion 1", "Criterion 2"]
  representativeness: "How sample relates to population"
  
framework_specification:
  framework_name: "Name of analytical framework"
  framework_version: "Version number"
  suitability_justification: "Why this framework is appropriate"
  variable_mapping:
    research_variable_1: "framework_dimension_1"
    research_variable_2: "framework_dimension_2"

analysis_plan:
  primary_analysis: "Main analytical approach"
  statistical_methods: ["Method 1", "Method 2"]
  quality_controls: ["Control 1", "Control 2"]
  validation_procedures: ["Validation 1", "Validation 2"]
  
  # Optional: Ensemble/Multi-Run Specifications
  ensemble_requirements:
    model_selection_criteria: "4 most advanced models available"
    budget_constraint: "$50.00 USD maximum"
    statistical_requirements: ["inter-rater reliability", "Cronbach's alpha"]
    performance_requirements: "must handle 100+ texts per batch"
    multi_run_specifications: "3 runs per model for consistency testing"
    # Note: System will evaluate feasibility and provide alternatives if needed

expected_outcomes:
  predicted_results: "Specific expected findings"
  significance_criteria: "What constitutes meaningful results"
  null_result_interpretation: "How to interpret non-significant findings"

resources_timeline:
  estimated_duration: "Expected analysis time"
  computational_requirements: "Processing needs"
  cost_estimate: "Expected expenses"
```

---

## LLM Validation Instructions

When evaluating an experiment submission, follow this protocol:

### 1. **Research Foundation Check**
- Assess clarity and specificity of research question
- Evaluate theoretical background and literature context
- Check for clear scope and expected contribution

### 2. **Hypothesis Evaluation**
- Verify hypotheses are falsifiable and specific
- Check for appropriate operational definitions
- Assess logical connection between theory and predictions

### 3. **Dataset Assessment**
- Evaluate adequacy of corpus for research question
- Check sample size justification and selection criteria
- Assess representativeness and ethical considerations

### 4. **Framework Alignment Analysis**
- Verify framework appropriately measures research concepts
- Check clear mapping between framework and research variables
- Assess acknowledgment of framework limitations

### 5. **Analysis Plan Review**
- Evaluate appropriateness of analytical strategy
- Check statistical methods for data type and research question
- Assess quality control and validation procedures

### 6. **Contingency Planning Check**
- Review preparedness for different result types
- Assess significance criteria and practical importance
- Check protocol for unexpected findings

### 7. **Integration Assessment**
- Evaluate overall coherence and feasibility
- Check for potential problems or gaps
- Assess likelihood of producing meaningful results

### 8. **Final Recommendation**
```
EXPERIMENT VALIDATION RESULT

Experiment: [Title]
Research Question: [Question]
Overall Assessment: PASS/FAIL
Completeness Score: [X]%

Strengths:
- Strength 1
- Strength 2

Required Improvements (if any):
- Specific gap 1
- Specific gap 2

Feasibility Assessment: HIGH/MEDIUM/LOW
Risk Factors: [Any significant risks or concerns]

Approval Status: APPROVED/NEEDS REVISION/REJECTED
Rationale: [Clear explanation of decision]

Ready for Discernus Analysis: YES/NO
Estimated Analysis Scope: [Brief scope assessment]
```

---

## Success Criteria

An experiment **PASSES** validation if:
- ✅ Meets 90%+ of all requirements
- ✅ 100% complete on critical elements (hypotheses, dataset, analysis plan)
- ✅ Clear falsifiable hypotheses
- ✅ Adequate dataset for testing hypotheses
- ✅ Appropriate framework-experiment alignment
- ✅ Feasible analysis plan
- ✅ Prepared for contingencies

An experiment **NEEDS REVISION** if:
- ⚠️ Meets 80-89% of requirements
- ⚠️ Minor gaps in critical elements
- ⚠️ Hypotheses need clarification
- ⚠️ Dataset marginally adequate
- ⚠️ Analysis plan needs refinement

An experiment **FAILS** validation if:
- ❌ Meets <80% of requirements
- ❌ Major gaps in critical elements
- ❌ Non-falsifiable or vague hypotheses
- ❌ Inadequate dataset
- ❌ Poor framework-experiment fit
- ❌ Infeasible analysis plan

---

## Special Considerations

### Exploratory vs. Confirmatory Research
- **Exploratory**: More flexibility in hypotheses, emphasis on discovery protocols
- **Confirmatory**: Stricter hypothesis requirements, emphasis on testing procedures

### Sample Size Guidelines
- **Minimum**: 30 texts for basic descriptive analysis
- **Comparative**: 50+ texts per comparison group
- **Complex Analysis**: 100+ texts for robust statistical analysis
- **Corpus Studies**: 200+ texts for population-level claims

### Framework Validation Studies
- **Requirements**: Multiple frameworks, comparison protocols, validation criteria
- **Special Considerations**: Framework development vs. framework application

### Cross-Cultural Studies
- **Additional Requirements**: Cultural sensitivity protocols, interpretation guidelines
- **Validation Emphasis**: Appropriateness across cultural contexts

### Ensemble and Multi-Run Studies
- **Additional Requirements**: Clear model selection criteria, budget constraints, statistical analysis plan
- **Validation Emphasis**: Feasibility assessment, constraint satisfaction, statistical validity
- **Special Considerations**: System will evaluate technical feasibility and guide toward viable alternatives
- **Examples**: Multi-LLM bias testing, inter-rater reliability studies, consistency validation

---

## Benefits of This Approach

### For Researchers:
- **Research Quality**: Ensures methodological rigor before analysis
- **Efficiency**: Prevents wasted effort on poorly designed studies
- **Learning**: Validation feedback improves research skills

### For Discernus:
- **Quality Assurance**: Only well-designed experiments enter the system
- **Resource Efficiency**: Focus computational resources on viable studies
- **Scientific Credibility**: Maintains high standards for platform

### For the Research Community:
- **Reproducibility**: Clear experimental standards enable replication
- **Quality**: Raises bar for computational social science research
- **Innovation**: Encourages thoughtful experimental design

This rubric ensures that researchers come to Discernus with carefully planned, methodologically sound experiments while maintaining flexibility for diverse research approaches and novel investigations. 