# Experiment System Specification
*Version: 3.1.0*
*Last Updated: June 25, 2025*
*Framework Specification v3.1 Compatible*

## **🎯 Overview**

The Narrative Gravity Analysis System provides a comprehensive experimental framework for systematic research using Large Language Models (LLMs) to analyze text narratives. This document specifies all available options, parameters, and capabilities for designing and executing experiments.

**Framework Specification v3.1 Compatibility**: This specification is fully aligned with Framework Specification v3.1, supporting the new axes-based structure, flexible versioning, mandatory citation formats, and enhanced academic validation requirements.

## **📋 Experiment Architecture**

### **Core Experiment Components**

Every experiment consists of **four independent component types** that combine at runtime:

1. **Framework Configuration** - Defines the analytical dimensions and theoretical foundation
2. **Prompt Template** - Specifies how the LLM should perform the analysis
3. **Scoring Algorithm** - Determines mathematical interpretation of results
4. **LLM Configuration** - Controls model selection and analysis parameters

### **Experimental Design Philosophy**

**Component Independence**: Each component type has independent lifecycles and can be combined in any valid configuration, enabling systematic methodological research.

**Clean Separation of Concerns**:
- **Frameworks** = What theoretical dimensions to analyze
- **Prompts** = How to instruct the LLM to perform analysis
- **Algorithms** = How to mathematically interpret the results
- **Models** = Which LLM provider and configuration to use

## **🏗️ Component Type Specifications**

### **1. Framework Configurations (Framework Specification v3.1)**

**Purpose**: Define the theoretical space for narrative analysis through dimensional structures using the Framework Specification v3.1 standard.

#### **Framework Structure (v3.1)**
```yaml
# =============================================================================
# FRAMEWORK IDENTIFICATION (required)
# =============================================================================
name: "framework_name"
version: "flexible_version" # v1.0, v2025.06.04, etc.
display_name: "Human-readable Framework Name"
description: |
  Framework description with mandatory citation format:
  "Discernus Framework: Framework Name vX.Y (Author, Year)"

# =============================================================================
# POSITIONING DEFINITION (axes - opposing anchor pairs)
# =============================================================================
axes:
  Axis_Name:
    description: "Axis description explaining the opposing anchors"
    
    integrative:
      name: "Positive Anchor"
      description: "Description of the positive/constructive dimension"
      language_cues: ["keyword1", "keyword2", "keyword3"]
      position: "12 o'clock"  # or angle: 0
      weight: 1.0
      type: category_type
      opposite_of: "Negative Anchor"
    
    disintegrative:
      name: "Negative Anchor"
      description: "Description of the negative/destructive dimension"
      language_cues: ["keyword1", "keyword2", "keyword3"]
      position: "6 o'clock"  # or angle: 180
      weight: 1.0
      type: category_type
      opposite_of: "Positive Anchor"

# =============================================================================
# ALGORITHM CONFIGURATION (optional)
# =============================================================================
algorithm_config:
  dominance_amplification:
    enabled: true/false
    threshold: number
    multiplier: number
    rationale: "Description of algorithmic approach"

# =============================================================================
# ACADEMIC VALIDATION (required)
# =============================================================================
theoretical_foundation:
  primary_sources: ["Academic citation 1", "Academic citation 2"]
  theoretical_approach: "Description of methodological foundation"

validation:
  academic_standard: "Academic validation standard"
  measurement_instrument: "Measurement approach"
  scope_limitation: "Scope and limitations"
  citation_format: "Discernus Framework: Name vX.Y (Author, Year)"
  academic_attribution: "Academic attribution and source acknowledgment"

# =============================================================================
# FRAMEWORK VERSIONING (required)
# =============================================================================
last_modified: "ISO 8601 timestamp"
framework_registry_key: "unique_registry_identifier"
implementation_status: "Framework Specification v3.1 compliant"
```

#### **Available Frameworks (v3.1 Compliant)**

**Civic Virtue Framework** (`civic_virtue_v2025.06.04`)
- **Dimensions**: 5 axes with opposing anchor pairs (Dignity↔Tribalism, Truth↔Resentment, Justice↔Manipulation, Hope↔Fear, Pragmatism↔Fantasy)
- **Theoretical Foundation**: Aristotelian virtue ethics + contemporary civic republican theory
- **Use Case**: Political discourse analysis, democratic engagement assessment
- **Citation**: "Discernus Framework: Civic Virtue v2025.06.04 (Aristotle, 2025)"

**Political Worldview Triad Framework** (`political_worldview_triad_v1.0`)
- **Dimensions**: 3 axes representing core political orientations
- **Theoretical Foundation**: Political psychology and worldview analysis
- **Use Case**: Political orientation analysis, worldview assessment
- **Citation**: "Discernus Framework: Political Worldview Triad v1.0 (Political Scientists, 2025)"

**Moral Foundations Theory Framework** (`moral_foundations_theory_v1.0`)
- **Dimensions**: 6 axes based on Haidt's moral foundations (Care↔Harm, Fairness↔Cheating, Loyalty↔Betrayal, Authority↔Subversion, Sanctity↔Degradation, Liberty↔Oppression)
- **Theoretical Foundation**: Haidt's Moral Foundations Theory
- **Use Case**: Moral argumentation patterns, ethical stance analysis
- **Citation**: "Discernus Framework: Moral Foundations Theory v1.0 (Haidt, 2025)"

#### **Framework Development (v3.1 Standards)**
- **Versioning**: Flexible versioning (v1.0, v2025.06.04, etc.)
- **Validation**: 5-layer validation (Format → Structure → Semantics → Academic → Integration)
- **Citation Requirements**: Mandatory "Discernus Framework: Name vX.Y (Author, Year)" format
- **Academic Standards**: Required theoretical_foundation and validation sections
- **Compatibility**: Must specify compatible prompt templates and scoring algorithms

#### **Framework Quality Standards (v3.1)**
- **Academic Rigor**: Required theoretical foundation and academic validation
- **Self-Documentation**: Frameworks must document their theoretical basis and limitations
- **Citation Compliance**: All frameworks must include proper citation format
- **Validation Coverage**: Must pass all 5 validation layers
- **Mixed Positioning**: Support for both degree-based and clock-face positioning

### **2. Prompt Templates**

**Purpose**: Define how LLMs should perform narrative analysis within the framework structure.

#### **Prompt Template Types**

**Hierarchical Analysis** (`hierarchical_v2.1`)
- **Approach**: LLM ranks dimensions by importance and provides evidence
- **Output Format**: Hierarchical ranking with primary/secondary/tertiary anchors
- **Advantages**: Clear interpretability, evidence-based reasoning
- **Use Cases**: Academic research, detailed justification requirements

**Traditional Analysis** (`traditional_v2.0`)
- **Approach**: LLM provides scores for all dimensions simultaneously  
- **Output Format**: Numeric scores (0.0-1.0) for each framework dimension
- **Advantages**: Computational efficiency, statistical comparability
- **Use Cases**: Large-scale analysis, quantitative research

**Evidence-Based Analysis** (`evidence_based_v1.0`)
- **Approach**: Requires specific textual citations for all assessments
- **Output Format**: Scores + mandatory textual evidence for each dimension
- **Advantages**: Academic rigor, auditability
- **Use Cases**: Publication-quality research, validation studies

#### **Prompt Template Configuration**
```yaml
template_id: "unique_identifier"
name: "human-readable name"
version: "flexible_version"  # v3.1 flexible versioning
type: "hierarchical|traditional|evidence_based"
description: "methodological approach"

analysis_requirements:
  evidence_required: true/false
  justification_depth: "minimal|standard|comprehensive"
  ranking_required: true/false
  framework_fit_assessment: true/false

output_format:
  structure: "yaml|structured_text|hybrid"
  required_fields: ["array", "of", "mandatory", "response", "fields"]
  scoring_scale: "0.0-1.0, ordinal, etc."

llm_guidance:
  temperature_recommendation: 0.1  # 0.0-1.0
  max_tokens: 4000
  model_compatibility: ["array", "of", "compatible", "llm", "models"]
```

#### **Prompt Quality Standards**
- **Framework Agnostic**: Templates should work across multiple frameworks
- **Model Independent**: Compatible with different LLM providers  
- **Output Consistency**: Reliable YAML structure for parsing
- **Evidence Standards**: Clear requirements for supporting evidence

### **3. Scoring Algorithms**

**Purpose**: Define mathematical methods for interpreting LLM analysis results and calculating narrative positions.

#### **Available Scoring Algorithms**

**Linear Average** (`linear_v1.0`)
- **Method**: Standard averaging of all dimensional scores
- **Formula**: `position = Σ(score_i * unit_vector_i) / n`
- **Use Cases**: Baseline analysis, simple interpretability
- **Advantages**: Mathematically straightforward, equal treatment of dimensions

**Winner-Take-Most** (`winner_take_most_v1.0`)
- **Method**: Amplifies dominant dimensions while suppressing weaker ones
- **Formula**: `weight_i = score_i^boost_factor if score_i > threshold else score_i * suppress_factor`
- **Parameters**: `dominance_threshold`, `boost_factor`, `suppress_factor`
- **Use Cases**: Clear thematic dominance, reducing noise from weak signals

**Hierarchical Dominance** (`hierarchical_v1.0`)
- **Method**: Uses LLM-provided rankings and weights from hierarchical prompts
- **Formula**: `position = primary_weight * primary_vector + secondary_weight * secondary_vector + tertiary_weight * tertiary_vector`
- **Parameters**: `primary_weight` (0.6), `secondary_weight` (0.3), `tertiary_weight` (0.1)
- **Use Cases**: Evidence-based weighting, academic research

**Exponential Weighting** (`exponential_v1.0`)
- **Method**: Exponential transformation to enhance score differences
- **Formula**: `weight_i = score_i^exponent / Σ(score_j^exponent)`
- **Parameters**: `exponent`, `normalization`
- **Use Cases**: Emphasizing clear patterns, reducing ambiguous middle-ground results

**Nonlinear Transform** (`nonlinear_v1.0`)
- **Method**: Sigmoid transformation to exaggerate pole positions
- **Formula**: `transformed_score = 1 / (1 + exp(-steepness * (score - center)))`
- **Parameters**: `steepness`, `center_point`
- **Use Cases**: Clear categorization, reducing center-bias

#### **Algorithm Configuration**
```yaml
algorithm_id: "unique_identifier"
name: "human-readable name"
version: "flexible_version"  # v3.1 flexible versioning
type: "linear|winner_take_most|hierarchical|exponential|nonlinear"
description: "mathematical approach"

mathematical_foundation:
  primary_formula: "LaTeX or description"
  normalization_method: "normalization approach"
  edge_case_handling: "edge case handling strategy"

parameters:
  parameter_name:
    default_value: 0.7
    valid_range: "0.0-1.0"
    description: "parameter meaning and usage"

compatibility:
  framework_types: ["array", "of", "compatible", "frameworks"]
  prompt_types: ["array", "of", "compatible", "prompt", "templates"]
  mathematical_requirements: ["array", "of", "input", "requirements"]
```

### **4. LLM Configurations**

**Purpose**: Specify model providers, versions, and analysis parameters.

#### **Supported LLM Providers**

**OpenAI Models**
- **GPT-4.1 Series**: `gpt-4.1`, `gpt-4.1-mini`, `gpt-4.1-nano`
- **GPT-4o Series**: `gpt-4o`, `gpt-4o-mini`
- **O-Series Reasoning**: `o1`, `o3`, `o4-mini`
- **Cost Range**: $0.0001-0.06 per 1K tokens
- **Strengths**: Consistency, JSON reliability, cost-effectiveness

**Anthropic Models**
- **Claude 4 Series**: `claude-4-opus`, `claude-4-sonnet`
- **Claude 3.7 Series**: `claude-3.7-sonnet` (extended thinking)
- **Claude 3.5 Series**: `claude-3-5-sonnet-20241022`, `claude-3-5-haiku-20241022`
- **Cost Range**: $0.0003-0.075 per 1K tokens
- **Strengths**: Evidence quality, analytical depth, reasoning

**Mistral Models**
- **Large Series**: `mistral-large-2411`
- **Efficient Series**: `mistral-tiny`, `mistral-small`
- **Cost Range**: $0.0002-0.024 per 1K tokens
- **Strengths**: Multilingual, efficiency, European perspective

**Google AI Models**
- **Gemini 2.x Series**: `gemini-2.0-flash-exp`
- **Gemini 1.5 Series**: `gemini-1.5-flash`, `gemini-1.5-pro`
- **Cost Range**: $0.000125-0.05 per 1K tokens
- **Strengths**: Multimodal capabilities, technical analysis

#### **Model Configuration Parameters**
```yaml
llm_model: "model_identifier"
provider: "openai|anthropic|mistral|google_ai"
version: "model_version"

analysis_parameters:
  temperature: 0.1  # 0.0-1.0, creativity level
  max_tokens: 4000  # response length limit
  top_p: 0.9  # nucleus sampling parameter
  frequency_penalty: 0.0  # repetition control
  presence_penalty: 0.0  # topic diversity

cost_parameters:
  input_cost_per_1k: 0.001  # USD per 1K input tokens
  output_cost_per_1k: 0.003  # USD per 1K output tokens
  rate_limit: 60  # requests per minute

capability_profile:
  context_window: 128000  # maximum input tokens
  yaml_reliability: "high|medium|low"
  reasoning_depth: "high|medium|low"
  evidence_quality: "high|medium|low"
  consistency: "high|medium|low"
```

## **⚙️ Experiment Configuration (v3.1 Compatible)**

### **Experiment Definition Schema (v3.1)**

```yaml
# =============================================================================
# EXPERIMENT METADATA (required)
# =============================================================================
experiment:
  name: "Unique experiment identifier"
  version: "flexible_version"  # v1.0, v2025.06.04, etc.
  description: "Comprehensive experiment description"
  hypothesis: "Research hypothesis"
  research_context: "Academic context and background"
  
  metadata:
    researcher: "Creator identifier"
    institution: "Research affiliation"
    tags: ["array", "of", "research", "tags"]
    research_notes: "Methodology notes"
    publication_status: "draft|active|completed|published"
    citation_format_compliance: true  # v3.1 requirement

# =============================================================================
# COMPONENT CONFIGURATION (v3.1)
# =============================================================================
configuration:
  framework_config:
    name: "framework_name"
    version: "flexible_version"  # v3.1 flexible versioning
    registry_key: "framework_registry_key"
    citation_format: "Discernus Framework: Name vX.Y (Author, Year)"
    
  prompt_template:
    name: "template_name"
    version: "flexible_version"
    type: "hierarchical|traditional|evidence_based"
    
  scoring_algorithm:
    name: "algorithm_name"
    version: "flexible_version"
    type: "linear|winner_take_most|hierarchical|exponential|nonlinear"
    
  analysis_mode: "single_model|multi_model|comparative"
  selected_models: ["array", "of", "llm", "models"]

# =============================================================================
# EXECUTION PARAMETERS (v3.1)
# =============================================================================
execution_parameters:
  runs_per_text: 3  # Reliability validation
  randomize_order: true  # Reduce order effects
  cost_limit: 50.00  # USD maximum
  timeout_seconds: 300  # Per-run timeout
  retry_attempts: 3  # Failure handling

# =============================================================================
# QUALITY ASSURANCE (v3.1 Enhanced)
# =============================================================================
quality_assurance:
  enable_qa_validation: true
  confidence_threshold: 0.7  # Minimum QA confidence
  require_evidence: true  # v3.1 academic standards
  framework_compliance_check: true  # v3.1 validation
  citation_format_validation: true  # v3.1 requirement
  manual_review_triggers: ["low_confidence", "anomaly_detected", "framework_mismatch"]

# =============================================================================
# ACADEMIC STANDARDS (v3.1)
# =============================================================================
academic_standards:
  theoretical_validation_required: true
  citation_format_enforcement: true
  academic_attribution_required: true
  replication_package_generation: true
  methodology_documentation: true
```

### **Framework Specification v3.1 Integration**

**Enhanced Validation Pipeline**:
1. **Framework Validation**: Verify v3.1 compliance before experiment execution
2. **Citation Format Validation**: Ensure all components use proper citation formats
3. **Academic Standards Validation**: Check theoretical foundation and academic rigor
4. **Component Compatibility**: Verify framework-prompt-algorithm compatibility
5. **Versioning Validation**: Support flexible versioning patterns

**Academic Enhancement Features**:
- **Mandatory Academic Attribution**: All frameworks must include proper academic sources
- **Self-Documenting Requirements**: Frameworks must explain their theoretical basis
- **Enhanced Quality Assurance**: 6-layer QA system with v3.1 compliance checking
- **Replication Package Generation**: Automatic generation of complete replication materials
- **Citation Format Enforcement**: Systematic validation of "Discernus Framework: Name vX.Y (Author, Year)" format

## **📊 Experimental Outputs**

### **Run-Level Results**

Each individual LLM analysis produces:
```yaml
run_id: "unique_identifier"
text_id: "source_text_identifier"
llm_model: "model_used"
execution_time: "2025-06-25T10:00:00Z"
duration_seconds: 45.2
api_cost: 0.15  # USD

analysis_results:
  raw_scores:
    Care_Harm: 0.8
    Fairness_Cheating: 0.6
    # ... other axes
  hierarchical_ranking:
    primary: "Care"
    secondary: "Fairness"
    tertiary: "Authority"
  anchor_justifications:
    Care: "Evidence text supporting care emphasis"
    # ... other justifications
  framework_fit_score: 0.85  # 0.0-1.0
  narrative_position:
    x: 0.4
    y: 0.7

quality_metadata:
  qa_confidence_level: "HIGH|MEDIUM|LOW"
  qa_confidence_score: 0.92  # 0.0-1.0
  anomalies_detected: ["anomaly_type_1", "anomaly_type_2"]
  requires_second_opinion: false

provenance:
  framework_version: "v1.0"
  prompt_template_version: "v2.1"
  scoring_algorithm_version: "v1.0"
  complete_configuration:
    # ... full configuration details
```

### **Experiment-Level Results**

Aggregated analysis across all runs:
```yaml
experiment_summary:
  total_runs: 72
  successful_runs: 70
  total_cost: 25.50  # USD
  average_duration: 42.3  # seconds
  execution_period: "2025-06-25T10:00:00Z - 2025-06-25T12:30:00Z"

reliability_analysis:
  coefficient_variation: 0.15  # consistency measure
  intraclass_correlation: 0.82  # if multi-model
  reliability_rate: 0.95  # % achieving target CV
  framework_fit_statistics:
    mean_fit_score: 0.87
    std_fit_score: 0.08

academic_outputs:
  publication_ready_dataset: "path/to/experiment_data.csv"
  jupyter_analysis_notebook: "path/to/analysis.ipynb"
  r_analysis_scripts: "path/to/analysis.R"
  methodology_documentation: "path/to/methods.md"
  replication_package: "path/to/replication_package.zip"
```

## **🔬 Advanced Experimental Capabilities**

### **Component Matrix Experiments**

Systematic testing across multiple component combinations:
```yaml
matrix_experiment:
  frameworks: ["civic_virtue", "political_worldview_triad"]
  prompt_templates: ["hierarchical_v2.1", "traditional_v2.0"]
  scoring_algorithms: ["linear_v1.0", "hierarchical_v1.0"]
  models: ["gpt-4.1-mini", "claude-3-5-sonnet"]
```

**Output**: Complete factorial analysis with:
- Component interaction effects
- Optimal configuration identification  
- Methodological recommendations
- Statistical significance testing

### **Longitudinal Studies**

Time-series analysis capabilities:
```yaml
longitudinal_experiment:
  temporal_corpus:
    time_periods: ["2020-01", "2020-02", "2020-03"]
    texts_per_period: 10
    temporal_metadata: true
  trend_analysis:
    enable_trend_detection: true
    periodicity_detection: true
    change_point_analysis: true
```

### **Validation Studies**

Human-LLM comparison protocols:
```yaml
validation_experiment:
  human_coding:
    expert_coders: 3
    inter_rater_reliability_target: 0.8
    coding_protocol: "standardized methodology description"
  llm_comparison:
    correlation_targets: 0.7  # human-LLM agreement
    bias_detection: true
    systematic_error_analysis: true
```

## **📚 Usage Guidelines**

### **Experimental Design Best Practices**

1. **Component Selection Strategy**:
   - Choose frameworks appropriate for text type and research question
   - Select prompt templates matching analytical depth requirements
   - Pick scoring algorithms aligned with interpretability needs
   - Balance model cost/quality based on research budget

2. **Reliability Requirements**:
   - Single model: ≥3 runs per text for statistical validation
   - Multi-model: ≥2 models with correlation analysis
   - Academic research: Target CV ≤ 0.20, ICC ≥ 0.80

3. **Quality Assurance Standards**:
   - Enable QA validation for academic research
   - Set HIGH confidence thresholds for publication-quality work
   - Include evidence requirements for peer review
   - Plan manual review for edge cases

### **Component Development Workflow**

1. **Framework Development**:
   - Literature review and theoretical foundation
   - Dimensional definition and differentiation testing
   - Pilot testing with representative texts
   - Academic validation with expert review

2. **Prompt Engineering**:
   - Framework-agnostic design principles
   - Multi-model compatibility testing
   - Output format standardization
   - Evidence quality optimization

3. **Algorithm Innovation**:
   - Mathematical soundness verification
   - Edge case handling
   - Computational efficiency
   - Interpretability validation

### **Academic Integration Workflow**

1. **Experimental Design**: Use this specification to design methodologically sound experiments
2. **Execution**: Run experiments with complete provenance tracking
3. **Analysis**: Generate academic outputs with QA-enhanced data
4. **Publication**: Include complete replication packages
5. **Validation**: Support independent replication and verification

---

*This specification provides the complete experimental design space for systematic narrative analysis research using the Narrative Gravity Analysis System.* 