# Discernus Experiment System Specification
*Version: 3.2.0*
*Last Updated: January 26, 2025*
*Framework Specification v3.2 Compatible*

## **🎯 Overview**

The Discernus Experiment System provides a YAML-based approach for defining and executing narrative analysis experiments using Large Language Models (LLMs). This **Experiment Specification** documents the current production capabilities of the system and defines the **Experiment Schema** that all **Experiment Definition** files must follow.

**Framework Specification v3.2 Compatibility**: This specification integrates with **[Framework Specification v3.2](Discernus_Coordinate_System_Framework_Specification_3_2.md)** by supporting both embedded framework definitions (for rapid development) and framework registry references (for academic publication).

## **📋 Current System Architecture**

### **Production Components (v3.2.0)**

The current system consists of three core components:

1. **YAML Experiment Definitions** - Self-contained experiment specifications
2. **REST API Backend** - Statistical comparison and analysis engine  
3. **Experiment Runner** - Python script that executes experiments via API calls

### **Execution Workflow**

```mermaid
graph TD
    A[Experiment Definition (YAML)] --> B[run_experiment.py]
    B --> C[REST API /compare-statistical]
    C --> D[Multi-Model Analysis]
    D --> E[Statistical Comparison]
    E --> F[Results & Reports]
```

**Current Capabilities:**
- ✅ Multi-model statistical comparison experiments
- ✅ Embedded framework definitions (Framework Spec v3.2 compatible)
- ✅ Corpus-based batch analysis
- ✅ Statistical similarity analysis (geometric distance, correlation)
- ✅ Cost estimation and resource management
- ✅ Interactive results reporting

**Planned Capabilities:**
- 🔄 Component-based architecture (Framework, Prompt, Scoring, LLM configs)
- 🔄 Framework registry system
- 🔄 Advanced academic export formats
- 🔄 Matrix experiments and validation studies

## **🏗️ Experiment Definition Schema (Current v3.2.0)**

### **Complete YAML Structure**

```yaml
# =============================================================================
# EXPERIMENT METADATA (required)
# =============================================================================
experiment_meta:
  name: "unique_experiment_identifier"
  display_name: "Human-readable experiment name"
  version: "1.0"
  description: "Comprehensive experiment description"
  tags: ["research", "domain", "methodology"]
  
  # Study design (for statistical experiments)
  study_design:
    comparison_type: "multi_model"  # Currently only supported type
    corpus_based: true              # true for batch analysis
    statistical_validation: true    # enables statistical comparison
    sample_size_target: 32          # expected number of texts
    statistical_methods:            # methods to apply
      - "geometric_similarity"
      - "dimensional_correlation"
      - "hypothesis_testing"

# =============================================================================
# CORPUS CONFIGURATION (required for multi-text experiments)
# =============================================================================
corpus:
  source_type: "directory_collection"  # or "single_text"
  file_path: "corpus/validation_set"   # path to text files
  pattern: "**/*.txt"                  # file pattern (glob)
  
  # Sampling strategy (optional)
  sampling_strategy: "stratified"     # or "random", "all"
  categories:                         # for stratified sampling
    - "category_1"
    - "category_2"
  sample_per_category: "all"          # or specific number
  total_expected_texts: 32            # for validation

# =============================================================================
# EMBEDDED FRAMEWORK DEFINITION (Framework Specification v3.2 compatible)
# =============================================================================
framework:
  name: "framework_name"
  version: "1.0"
  description: "Framework description"
  
  # Framework structure (see Framework Specification v3.2)
  axes:
    Axis_Name:
      description: "Axis description"
      integrative:
        name: "Positive_Anchor"
        angle: 90
        description: "Positive pole description"
        language_cues: ["keyword1", "keyword2"]
      disintegrative:
        name: "Negative_Anchor" 
        angle: 270
        description: "Negative pole description"
        language_cues: ["keyword3", "keyword4"]

# =============================================================================
# PROMPT GUIDANCE (current system)
# =============================================================================
prompt_guidance:
  role_definition: |
    Detailed role definition for the LLM
    
  framework_summary_instructions: |
    Instructions on how to apply the framework
    
  analysis_methodology: |
    Specific methodology for analysis
    
  scoring_requirements: |
    Requirements for scoring format and ranges
    
  json_format_instructions: |
    Exact JSON format specification with examples

# =============================================================================
# MODEL CONFIGURATION (current system)
# =============================================================================
models:
  comparison_set: "flagship_only"  # or "efficiency_focused"
  
  flagship_models:
    openai_flagship:
      model_id: "gpt-4o"
      provider: "openai"
      tier: "flagship"
      enabled: true
      estimated_cost_per_analysis: 0.015
      
    anthropic_flagship:
      model_id: "claude-3-5-sonnet-20241022"
      provider: "anthropic" 
      tier: "flagship"
      enabled: true
      estimated_cost_per_analysis: 0.018

# =============================================================================
# STATISTICAL ANALYSIS CONFIGURATION (current system)
# =============================================================================
statistical_analysis:
  primary_methods:
    geometric_similarity:
      enabled: true
      metrics: ["euclidean_distance", "manhattan_distance"]
      
    dimensional_correlation:
      enabled: true
      methods: ["pearson", "spearman"]
      
    hypothesis_testing:
      enabled: true
      tests: ["paired_t_test"]
      alpha: 0.05

  similarity_classification:
    thresholds:
      highly_similar:
        geometric_distance: 0.15
        correlation_threshold: 0.85
      moderately_similar:
        geometric_distance: 0.35
        correlation_threshold: 0.65
      statistically_different:
        geometric_distance: 0.50
        correlation_threshold: 0.40

# =============================================================================
# REPORT CONFIGURATION (current system)
# =============================================================================
report_configuration:
  template_type: "statistical_comparison"
  
  visualization_strategy:
    model_summary_charts: true
    individual_text_charts: false  # Not implemented yet
    statistical_summary_cards: true
    
  content_sections:
    - "executive_summary"
    - "methodology_overview"
    - "statistical_results"
    - "detailed_analysis"

# =============================================================================
# RESOURCE ESTIMATION (current system)
# =============================================================================
resource_estimation:
  total_analyses: 64  # calculated: texts × models
  estimated_total_cost: 1.06
  estimated_duration_minutes: 20
  
# =============================================================================
# QUALITY ASSURANCE (basic current implementation)
# =============================================================================
quality_assurance:
  validation_checks:
    - "corpus_file_availability"
    - "model_api_connectivity"
    - "prompt_template_validation"
```

## **🚀 Execution Guide**

### **Step 1: Create Experiment Definition**

```bash
# Create your experiment definition file
nano my_experiment.yaml
```

### **Step 2: Execute Experiment** [[memory:6066560174742780108]]

```bash
# Navigate to experiments directory
cd discernus/experiments

# Run experiment
python3 run_experiment.py my_experiment.yaml
```

### **Step 3: View Results**

The system automatically generates:
- Interactive web report at `http://localhost:8000/reports/{job_id}`
- Statistical comparison summary
- Model performance analysis

## **📊 Current Output Format**

### **API Response Structure**

```json
{
  "job_id": "unique_job_identifier",
  "comparison_type": "multi_model",
  "similarity_classification": "highly_similar|moderately_similar|statistically_different",
  
  "condition_results": [
    {
      "condition_identifier": "gpt-4o",
      "centroid": [0.123, 0.456],
      "total_analyses": 32
    }
  ],
  
  "statistical_metrics": {
    "geometric_similarity": {
      "mean_distance": 0.142,
      "distance_matrix": [[0.0, 0.142], [0.142, 0.0]]
    },
    "dimensional_correlation": {
      "correlation_matrix": [[1.0, 0.87], [0.87, 1.0]],
      "average_correlation": 0.87
    }
  },
  
  "report_url": "/reports/job_12345",
  "execution_metadata": {
    "total_cost": 1.06,
    "duration_seconds": 1200
  }
}
```

## **🛠️ Framework Integration (v3.2 Compatible)**

### **Embedded Framework Mode (Current)**

For rapid development and iteration, frameworks are embedded directly in the experiment YAML:

```yaml
framework:
  name: "my_research_framework"
  version: "1.0"
  axes:
    # Complete framework definition here
```

**Advantages:**
- ✅ Self-contained experiment definitions
- ✅ Rapid iteration and testing
- ✅ No external dependencies
- ✅ Version control friendly

### **Framework Registry Mode (Planned)**

For academic publication and framework reuse, future versions will allow referencing canonical framework definitions from a registry:

```yaml
framework:
  registry_key: "moral_foundations_theory_v3.2"
  citation_format: "Discernus Reference Framework: Moral Foundations Theory v3.2 (Haidt, 2025)"
  override_parameters:
    # Optional customizations
```

**Advantages:**
- 🔄 Framework reusability across experiments
- 🔄 Academic citation compliance
- 🔄 Version management
- 🔄 Quality assurance

## **📈 Statistical Analysis Capabilities**

### **Current Methods**

**Geometric Similarity Analysis:**
- Euclidean distance between model centroids
- Manhattan distance calculation
- Distance matrices for multi-model comparison

**Dimensional Correlation Analysis:**
- Pearson correlation between model outputs
- Spearman rank correlation
- Correlation matrices and significance testing

**Classification System:**
- **Highly Similar**: Distance < 0.15, Correlation > 0.85
- **Moderately Similar**: Distance < 0.35, Correlation > 0.65  
- **Statistically Different**: Distance > 0.50, Correlation < 0.40

### **Planned Statistical Enhancements**

- 🔄 Effect size analysis (Cohen's d, Hedges' g)
- 🔄 Confidence intervals and bootstrap testing
- 🔄 Bonferroni correction for multiple comparisons
- 🔄 Power analysis and sample size recommendations

## **🎓 Academic Standards Compliance**

### **Current Academic Features**

- ✅ Complete experiment replication via YAML experiment definitions
- ✅ Statistical validation with established methods
- ✅ Cost and resource tracking for transparency
- ✅ Framework Specification v3.2 compatibility

### **Academic Publication Readiness**

**Methodology Documentation:**
- Complete experiment definition in version-controlled YAML
- Statistical analysis parameters explicitly specified
- Model configurations and costs documented

**Reproducibility:**
- Self-contained experiment definitions
- Deterministic statistical analysis
- Complete provenance tracking

**Quality Assurance:**
- Multi-model comparison reduces single-model bias
- Statistical significance testing
- Transparent similarity classification

## **🚧 Development Roadmap**

### **Phase 1: Current Production (v3.2.0)** ✅
- YAML-based experiment definitions
- Multi-model statistical comparison
- Basic statistical analysis and reporting
- Framework Specification v3.2 integration

### **Phase 2: Component Architecture (v3.3.0)** 🔄
- Separate Framework, Prompt, Scoring, LLM configuration components
- Framework registry system
- Advanced prompt templates
- Scoring algorithm library

### **Phase 3: Advanced Analytics (v3.4.0)** 📋
- Matrix experiments (framework × prompt × model combinations)
- Longitudinal analysis capabilities
- Validation studies (human-LLM comparison)
- Academic export packages (R, Python, Stata)

### **Phase 4: Production Platform (v4.0.0)** 📋
- Web-based experiment builder
- Distributed execution and queuing
- Real-time monitoring and cost tracking
- Advanced visualization and reporting

## **💡 Best Practices**

### **Experiment Design**

1. **Start Simple**: Use embedded frameworks for initial development
2. **Statistical Power**: Target 20+ texts for meaningful statistical comparison
3. **Model Selection**: Include at least 2 flagship models for comparison
4. **Cost Management**: Set realistic cost estimates and monitor spending

### **Framework Development**

1. **Framework Spec Compliance**: Follow Framework Specification v3.2 standards
2. **Language Cues**: Provide diverse keyword examples for each anchor
3. **Prompt Precision**: Write detailed, unambiguous instructions for LLMs
4. **JSON Reliability**: Test prompt formats across different models

### **Academic Rigor**

1. **Hypothesis Specification**: Clearly state research questions and expectations
2. **Statistical Validation**: Use multiple statistical methods for robustness
3. **Transparency**: Document all parameters and decision points
4. **Replication**: Ensure experiments can be independently reproduced

## **⚠️ Current Limitations**

### **Known Constraints**

- **Single Experiment Type**: Only multi-model statistical comparison supported
- **Framework Embedding**: No framework registry system yet for referencing canonical Reference Framework Definitions.
- **Limited Export**: Basic reporting only, no academic package generation
- **API Dependency**: Requires running REST API backend
- **Local Execution**: No distributed or cloud execution yet

### **Workarounds**

- **Framework Reuse**: Copy-paste framework definitions between experiment definitions.
- **Result Export**: Screenshot reports or copy JSON results for external analysis
- **Manual Statistics**: Export raw data for advanced statistical analysis in R/Python
- **Cost Monitoring**: Track costs manually through API responses

## **🔗 Related Specifications**

- **[Framework Specification v3.2](Discernus_Coordinate_System_Framework_Specification_3_2.md)** - Framework definition standards
- **[Mathematical Foundations v1.0](Discernus_Coordinate_System_Mathematical_Foundations_1_0.md)** - Coordinate system mathematics
- **[Research Workflow v1.0](DCS_Research_Workflow_Specification_1_0.md)** - Overall research process
- **[Research Vocabulary v2.0](DCS_Research_Vocabulary_Comprehensive_Glossary_2_0.md)** - Terminology and concepts

---

*This specification documents the current production capabilities of the Discernus Experiment System v3.2.0. For advanced features described in earlier versions, see the development roadmap above.* 