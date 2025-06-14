# Prompt Template Development Guide

**Complete guide for creating and optimizing LLM analysis instructions**

*Last Updated: June 14, 2025*  
*Based on: Formal Specification System v2.1*

---

## 🎯 **Overview**

Prompt templates are **framework-agnostic instructions** that tell evaluators (LLMs or humans) how to perform narrative analysis. They are separate from theoretical frameworks and focus purely on analysis methodology and response format.

### **Key Principles**
- **Framework Agnostic**: Work with any theoretical framework (civic virtue, political spectrum, etc.)
- **Evaluator Optimized**: Designed for specific LLM response patterns or human evaluation protocols
- **Structured Output**: Enforce consistent, parseable response formats
- **Evidence-Based**: Require justification and citation for analytical claims
- **Performance Validated**: Tested for reliability, consistency, and accuracy

---

## 📐 **Prompt Template Architecture**

### **Component Structure (v2.1 Specification)**

Every prompt template consists of **8 required components** in specific order:

#### **1. Header** (Order: 1)
```
You are analyzing this text using [FRAMEWORK_NAME] v[VERSION] with [TEMPLATE_NAME] v[VERSION].
```
**Purpose**: Version identification and reproducibility tracking

#### **2. Role Definition** (Order: 2)
```
You are an expert political analyst specializing in [DOMAIN] with deep knowledge of [THEORETICAL_FOUNDATION].
```
**Purpose**: Establish analytical authority and expertise context

#### **3. Scoring Requirements** (Order: 3)
```
CRITICAL: All scores must be between 0.0 and 1.0, where:
- 0.0 = No presence/relevance of this theme
- 1.0 = Dominant/central theme throughout the text
```
**Purpose**: Enforce consistent scoring scale across all evaluators

#### **4. Analysis Methodology** (Order: 4)
```
[SPECIFIC ANALYTICAL APPROACH - varies by template type]
```
**Purpose**: Define how to perform the analysis (hierarchical, traditional, evidence-based)

#### **5. Framework Wells** (Order: 5)
```
Analyze the text for these themes:
[DYNAMIC_FRAMEWORK_CONTENT]
```
**Purpose**: Framework-specific analysis targets (populated dynamically)

#### **6. Hierarchical Requirements** (Order: 6, Conditional)
```
RANKING REQUIREMENT: After scoring, rank themes from most to least prominent...
```
**Purpose**: Required only for hierarchical template types

#### **7. Response Format** (Order: 7)
```json
{
  "analysis": {
    "theme_scores": { "theme_name": 0.0 },
    "evidence_citations": { "theme_name": "Direct quote supporting score" },
    "ranking": ["theme1", "theme2", ...],
    "confidence": 0.0,
    "methodology_notes": "Brief explanation of analytical approach"
  }
}
```
**Purpose**: Enforce structured, parseable output format

#### **8. Quality Standards** (Order: 8)
```
Quality Requirements:
- Provide specific textual evidence for each score
- Justify ranking decisions with clear reasoning
- Include confidence assessment (0.0-1.0)
- Ensure reproducibility of analysis
```
**Purpose**: Academic rigor and validation requirements

---

## 🔧 **Template Types & Use Cases**

### **1. Hierarchical Analysis Template**

**Purpose**: Ranking-based analysis with dominance detection  
**Best For**: Texts with clear thematic hierarchy, political speeches, persuasive content  
**Output**: Scores + rankings + evidence citations

**Key Features**:
- **Dominance Detection**: Identifies primary vs secondary themes
- **Ranking Enforcement**: Forces prioritization of themes
- **Evidence Integration**: Requires textual support for rankings
- **Consistency Focus**: Optimized for reliable hierarchical judgments

**Performance Characteristics**:
- **Reliability**: High consistency across evaluators (CV < 0.20)
- **Discriminative Power**: Excellent at detecting thematic dominance
- **Cognitive Load**: Moderate - requires ranking decisions
- **Evidence Quality**: High - ranking justifications improve citations

### **2. Traditional Analysis Template**

**Purpose**: Comprehensive dimensional scoring without ranking  
**Best For**: Complex texts, literary analysis, multidimensional content  
**Output**: Detailed scores + evidence + analytical notes

**Key Features**:
- **Comprehensive Coverage**: Equal attention to all framework dimensions
- **Nuanced Scoring**: Captures subtle thematic variations
- **Analytical Depth**: Encourages detailed examination
- **Flexible Interpretation**: Allows complex thematic relationships

**Performance Characteristics**:
- **Reliability**: Moderate consistency (CV 0.15-0.25)
- **Discriminative Power**: Good at capturing nuanced patterns
- **Cognitive Load**: High - comprehensive analysis required
- **Evidence Quality**: Moderate - broader scope may reduce detail

### **3. Evidence-Based Analysis Template**

**Purpose**: Citation-focused analysis with justification requirements  
**Best For**: Academic research, validation studies, human comparison  
**Output**: Scores + extensive citations + methodological notes

**Key Features**:
- **Citation Requirements**: Mandatory textual evidence for every score
- **Justification Focus**: Detailed reasoning for analytical decisions
- **Methodology Transparency**: Clear explanation of analytical approach
- **Academic Standards**: Designed for peer review compatibility

**Performance Characteristics**:
- **Reliability**: Variable - depends on evidence requirements
- **Discriminative Power**: Moderate - focus on justification over detection
- **Cognitive Load**: Very High - extensive documentation required
- **Evidence Quality**: Excellent - comprehensive citation requirements

---

## 🔬 **Development Workflow**

### **Phase 1: Design & Specification** (1-2 hours)

#### **Step 1: Define Purpose & Use Case**
```markdown
Template Name: evidence_enhanced_hierarchical
Purpose: Combine hierarchical ranking with enhanced evidence requirements
Target Use Case: Academic validation studies requiring both ranking and justification
Target Evaluators: GPT-4, Claude-3, trained human experts
Expected Performance: CV < 0.18, evidence quality > 0.85
```

#### **Step 2: Create Component Structure**
```bash
# Create template directory
mkdir prompt_templates/evidence_enhanced_hierarchical_v1.0/

# Create component files
echo "Header component..." > header.txt
echo "Role definition..." > role_definition.txt
echo "Scoring requirements..." > scoring_requirements.txt
# ... (create all 8 components)
```

#### **Step 3: Framework Compatibility Assessment**
```bash
# Test compatibility with available frameworks
python src/narrative_gravity/cli/component_manager.py check-framework-compatibility \
    --template-draft "evidence_enhanced_hierarchical" \
    --frameworks "civic_virtue,political_spectrum,fukuyama_identity"
```

### **Phase 2: Implementation & Assembly** (2-3 hours)

#### **Step 4: Component Development**

**Header Component**:
```
You are analyzing this text using {framework_name} v{framework_version} with Evidence Enhanced Hierarchical Analysis v1.0.
```

**Role Definition** (Framework-specific examples):
```
# For civic_virtue framework:
You are an expert political ethicist specializing in civic virtue theory with deep knowledge of classical and contemporary virtue ethics, political philosophy, and moral reasoning in public discourse.

# For political_spectrum framework:
You are an expert political scientist specializing in ideological analysis with deep knowledge of left-right political positioning, authority relationships, and comparative political systems.
```

**Analysis Methodology** (Template-specific):
```
EVIDENCE-ENHANCED HIERARCHICAL ANALYSIS METHODOLOGY:

1. COMPREHENSIVE READING: Read the entire text carefully, noting all thematic elements
2. EVIDENCE COLLECTION: For each potential theme, collect specific textual citations
3. SCORING WITH JUSTIFICATION: Score each theme 0.0-1.0 with required textual evidence
4. HIERARCHICAL RANKING: Rank themes by prominence with justification for ranking decisions
5. CONFIDENCE ASSESSMENT: Evaluate certainty of analysis (0.0-1.0)
6. METHODOLOGY DOCUMENTATION: Record analytical decisions and approach
```

#### **Step 5: Template Assembly**
```python
# Use template assembly tool
python src/narrative_gravity/cli/template_assembler.py \
    --template-name "evidence_enhanced_hierarchical" \
    --version "1.0.0" \
    --components-dir "prompt_templates/evidence_enhanced_hierarchical_v1.0/" \
    --output "templates/evidence_enhanced_hierarchical_v1.0.txt"
```

### **Phase 3: Validation & Testing** (3-4 hours)

#### **Step 6: Component Validation**
```bash
# Validate template structure
python src/narrative_gravity/cli/validate_component.py \
    --component-type prompt_template \
    --file "templates/evidence_enhanced_hierarchical_v1.0.txt" \
    --template-type hierarchical

# Check framework compatibility
python src/narrative_gravity/cli/component_manager.py validate-compatibility \
    "evidence_enhanced_hierarchical v1.0.0" \
    "civic_virtue v2.1.0" \
    "hierarchical_weighted v2.1.0"
```

#### **Step 7: Performance Testing**
```bash
# Create test experiment
python src/narrative_gravity/cli/experiment_manager.py create \
    --name "Template_Validation_Evidence_Enhanced" \
    --hypothesis "Evidence-enhanced template improves justification quality while maintaining reliability" \
    --prompt-template "evidence_enhanced_hierarchical v1.0.0" \
    --framework "civic_virtue v2.1.0" \
    --weighting "hierarchical_weighted v2.1.0" \
    --test-mode \
    --validation-texts "corpus/validation_set/"

# Run validation analysis
python src/narrative_gravity/cli/run_template_validation.py \
    --template "evidence_enhanced_hierarchical v1.0.0" \
    --frameworks "civic_virtue,political_spectrum" \
    --runs 5 \
    --metrics "reliability,evidence_quality,response_format_compliance"
```

### **Phase 4: Optimization & Refinement** (2-3 hours)

#### **Step 8: Performance Analysis**
```bash
# Generate performance report
python src/narrative_gravity/cli/template_performance_report.py \
    --template "evidence_enhanced_hierarchical v1.0.0" \
    --include-benchmarks \
    --output-dir "analysis_results/template_validation/"

# Launch analysis notebook
jupyter notebook analysis_results/template_validation/performance_analysis.ipynb
```

#### **Step 9: Iterative Improvement**
Based on performance metrics:
- **CV > 0.20**: Improve instruction clarity, reduce cognitive load
- **Evidence Quality < 0.80**: Strengthen citation requirements, add examples
- **Format Compliance < 0.95**: Simplify JSON structure, add format examples
- **Cross-Model Variance High**: Add model-specific guidance or simplify instructions

### **Phase 5: Production Deployment** (1 hour)

#### **Step 10: Final Validation & Registration**
```bash
# Final comprehensive validation
python src/narrative_gravity/cli/validate_component.py \
    --component-type prompt_template \
    --file "templates/evidence_enhanced_hierarchical_v1.0.txt" \
    --comprehensive-validation \
    --require-performance-benchmarks

# Register in component database
python src/narrative_gravity/cli/component_manager.py create-prompt \
    "evidence_enhanced_hierarchical" \
    "1.0.0" \
    "templates/evidence_enhanced_hierarchical_v1.0.txt" \
    --description "Hierarchical analysis with enhanced evidence requirements for academic validation" \
    --framework-compatibility "civic_virtue,political_spectrum,fukuyama_identity" \
    --performance-validated
```

---

## 📊 **Performance Optimization**

### **Reliability Optimization**

**Target**: Coefficient of Variation (CV) < 0.20

**Common Issues & Solutions**:

#### **High Variance (CV > 0.25)**
- **Cause**: Ambiguous instructions, complex cognitive load
- **Solution**: Simplify language, add step-by-step guidance, include examples
- **Example Fix**: Replace "Analyze the prominence of themes" with "Score each theme 0.0-1.0 based on frequency and emphasis in the text"

#### **Model-Specific Variance**
- **Cause**: Different LLMs interpret instructions differently
- **Solution**: Add model-agnostic phrasing, test across multiple models
- **Example Fix**: Avoid model-specific reasoning patterns, use universal analytical concepts

#### **Framework Interaction Effects**
- **Cause**: Template works well with some frameworks but not others
- **Solution**: Test across all intended frameworks, adjust for theoretical differences
- **Example Fix**: Generalize instructions to work with different theoretical vocabularies

### **Evidence Quality Optimization**

**Target**: Evidence Quality Score > 0.85

**Quality Metrics**:
- **Citation Accuracy**: Quotes accurately reflect textual content
- **Relevance**: Citations support analytical claims
- **Specificity**: Detailed rather than vague references
- **Coverage**: Evidence provided for all scored themes

**Improvement Strategies**:
```
# Low Evidence Quality Fix
BEFORE: "Provide evidence for your scores"
AFTER: "For each theme score, include a specific quote (5-15 words) that best demonstrates the theme's presence and supports your numerical score"

# Relevance Improvement
BEFORE: "Support your analysis with text"
AFTER: "Quote specific phrases that directly illustrate each theme. Explain how each quote supports your score (0.0-1.0)"

# Coverage Enhancement
BEFORE: "Include relevant quotations"
AFTER: "Required: Provide at least one specific textual citation for every theme score above 0.1"
```

### **Response Format Compliance**

**Target**: Format Compliance > 0.95

**Common Format Issues**:
- **Invalid JSON**: Syntax errors, missing brackets, incorrect quotes
- **Missing Fields**: Incomplete responses, missing required elements
- **Type Errors**: Strings instead of numbers, arrays instead of objects

**Format Optimization**:
```json
# Robust Format Specification
{
  "analysis": {
    "theme_scores": {
      "theme_1": 0.0,
      "theme_2": 0.0,
      "note": "All scores must be numbers between 0.0 and 1.0"
    },
    "evidence_citations": {
      "theme_1": "Direct quote supporting score",
      "theme_2": "Direct quote supporting score",
      "note": "All citations must be actual text quotes"
    },
    "ranking": ["theme_1", "theme_2"],
    "confidence": 0.0,
    "methodology_notes": "Brief explanation"
  }
}
```

---

## 🔬 **Advanced Template Patterns**

### **Multi-Stage Analysis Templates**

**Purpose**: Complex analysis requiring multiple reasoning steps  
**Use Case**: Literary analysis, complex political documents, theoretical texts

**Structure**:
```
STAGE 1: Initial thematic identification
STAGE 2: Evidence collection and validation  
STAGE 3: Comparative assessment and scoring
STAGE 4: Hierarchical ranking with justification
STAGE 5: Confidence assessment and methodology documentation
```

### **Comparative Analysis Templates**

**Purpose**: Direct comparison between texts or within-text comparisons  
**Use Case**: Longitudinal studies, author comparisons, rhetorical evolution

**Key Features**:
- **Baseline Establishment**: Reference point for comparisons
- **Relative Scoring**: Scores relative to comparison targets
- **Change Detection**: Identification of differences and similarities
- **Comparative Evidence**: Citations supporting comparative claims

### **Domain-Specific Templates**

**Purpose**: Optimized for specific text types or research domains  
**Use Case**: Historical texts, social media, legal documents, literary works

**Customization Areas**:
- **Vocabulary Adaptation**: Domain-appropriate analytical language
- **Evidence Requirements**: Format-specific citation patterns
- **Scoring Calibration**: Domain-appropriate scoring ranges
- **Quality Standards**: Field-specific academic requirements

---

## 📚 **Integration with Research Workflow**

### **Template Selection Guidelines**

#### **For Methodological Research**
- **A/B Testing**: Use multiple templates with identical frameworks and weighting
- **Component Optimization**: Systematic comparison across template dimensions
- **Performance Benchmarking**: Standardized validation across research contexts

#### **For Substantive Research**
- **Research Question Alignment**: Choose template type matching analytical goals
- **Quality Requirements**: Select based on evidence and reliability needs
- **Resource Constraints**: Balance quality requirements with time/cost limitations

### **Academic Publication Integration**

#### **Methods Section Documentation**
```markdown
## Analytical Methodology

Text analysis was conducted using [Template Name] v[Version], a validated prompt template implementing [analytical approach]. The template enforces structured output format with required evidence citations and confidence assessment. Template performance characteristics include reliability (CV = X.XX) and evidence quality (score = X.XX) validated across [N] frameworks and [N] text types.

Full template specification and validation results are available in the replication package.
```

#### **Replication Package Contents**
- **Complete Template**: Full prompt text with all components
- **Validation Results**: Performance metrics and benchmarking data
- **Framework Compatibility**: Tested combinations and compatibility matrix
- **Usage Guidelines**: Recommended applications and limitations

---

## 🎯 **Quality Assurance Checklist**

### **Pre-Development** ✅
- [ ] Clear purpose and use case definition
- [ ] Target performance metrics established
- [ ] Framework compatibility requirements specified
- [ ] Resource and timeline estimates completed

### **Development** ✅
- [ ] All 8 components implemented following v2.1 specification
- [ ] Framework-agnostic language throughout
- [ ] Structured JSON response format specified
- [ ] Evidence requirements clearly defined

### **Validation** ✅
- [ ] Component structure validation passed
- [ ] Framework compatibility testing completed
- [ ] Performance benchmarking conducted (CV, evidence quality, format compliance)
- [ ] Cross-model validation performed

### **Production Deployment** ✅
- [ ] Final comprehensive validation passed
- [ ] Performance meets established targets
- [ ] Documentation and usage guidelines completed
- [ ] Component registered in database with metadata

### **Post-Deployment** ✅
- [ ] Usage monitoring and feedback collection active
- [ ] Performance tracking over time implemented
- [ ] Version control and update procedures established
- [ ] Academic integration and citation guidelines available

---

**This guide provides everything needed to develop high-quality prompt templates that advance the state of computational narrative analysis while maintaining academic rigor and reproducibility.**

*Next Steps*: See [`WEIGHTING_SCHEME_DEVELOPMENT.md`](WEIGHTING_SCHEME_DEVELOPMENT.md) for mathematical interpretation of template results, or [`../practical-guides/CLI_EXPERIMENT_GUIDE.md`](../practical-guides/CLI_EXPERIMENT_GUIDE.md) for template usage in experiments. 