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

## **🎯 Framework Embedding Optimization**

### **LLM Processing Optimization for Embedded Frameworks**

When frameworks are embedded directly in experiment YAML definitions, optimal **prompt element placement** becomes critical for LLM processing efficiency and analytical accuracy. This implements **[Framework Specification v3.2 - Framework Embedding Best Practices](Discernus_Coordinate_System_Framework_Specification_3_2.md#framework-embedding-best-practices)**.

### **Core Challenge: Sequential Processing Context**

**Processing Order**: Experiment YAML → Embedded Framework → LLM Analysis  
**Problem**: LLMs process sequentially, requiring proper cognitive context establishment before encountering framework components  
**Solution**: Strategic prompt placement optimized for embedded framework context

### **Optimal Embedded Framework Architecture**

```yaml
# =============================================================================
# EXPERIMENT METADATA (establishes research context)
# =============================================================================
experiment_meta:
  name: "research_experiment_identifier"
  display_name: "Human-readable experiment name"
  description: "Experiment purpose and research context"

# =============================================================================
# EMBEDDED FRAMEWORK WITH OPTIMIZED PROMPT PLACEMENT
# =============================================================================
framework:
  name: "framework_name"
  version: "v3.2"
  display_name: "Framework Display Name"
  description: |
    Comprehensive framework description with theoretical foundation.
    This provides initial framework context before LLM encounters technical elements.
  
  # EARLY: Essential cognitive priming (CRITICAL for embedded frameworks)
  expert_role: |
    You are an expert analyst of [domain] discourse with deep knowledge of 
    [theoretical approach]. You specialize in [analytical methodology] using
    [framework approach] standards.
    
    ** No framework component references - establishes cognitive frame only **
  
  methodological_approach: |
    Following [theoretical methodology], analyze discourse as [approach type].
    Apply [analytical principles] without fragmenting into separate parts.
    Use [scoring principles] for comprehensive evaluation.
    
    ** High-level methodology that guides framework interpretation **
  
  # MIDDLE: Complete framework structure definitions
  components:
    anchor_id_1:
      component_id: anchor_id_1
      type: anchor
      description: "Complete anchor definition with theoretical grounding"
      language_cues: ["cue1", "cue2", "cue3"]
      # ... complete component definition
  
  axes:
    Axis_Name:
      anchor_ids: [anchor_id_1, anchor_id_2]
      description: "Axis relationship description"
      anchor_summary:
        anchor_id_1: "Brief anchor description"
        anchor_id_2: "Brief opposing anchor description"
  
  competitive_relationships:
    enabled: true
    competition_pairs:
      - anchors: ["anchor_id_1", "anchor_id_2"]
        strength: 0.8
        mechanism: "crowding_out"
  
  # LATE: Detailed prompts with framework element references
  detailed_prompts:
    scoring_scale_guidance: |
      Use the [specific scale] where 0 = [definition], 1 = [definition].
      Apply this scale to each anchor defined in the components section above.
      Reference the specific language_cues and competition_pairs for precision.
    
    framework_application: |
      Apply the competitive_relationships defined above to detect ideological
      competition. Reference the specific anchor definitions and language_cues
      from the components section for accurate analysis.
    
    domain_expertise: |
      Apply specialized knowledge of [domain] discourse, including the cultural
      terminology defined in the components section above. Reference the
      specific theoretical framework elements for detailed guidance.

# =============================================================================
# EXPERIMENT EXECUTION CONFIGURATION
# =============================================================================
models:
  # Model configuration for experiment execution
```

### **Implementation Benefits**

**Early Context Setting Advantages:**
- **Domain Expertise Establishment**: LLM adopts appropriate analytical perspective before processing framework components
- **Methodological Priming**: Analysis approach established before encountering technical framework structure
- **No Forward References**: Early prompts don't break by referencing undefined framework elements
- **Experiment Integration**: Works seamlessly in experiment context with proper layering

**Late Detailed Prompts Advantages:**
- **Technical Precision**: Can reference specific framework components with confidence
- **Forward Reference Safety**: All referenced elements have been defined in framework structure
- **Implementation Specificity**: Detailed guidance for applying framework components in analysis
- **Framework Element Integration**: Natural referencing of language_cues, competition_pairs, and metrics

### **Framework Embedding Implementation Guidelines**

**Required Implementation Sequence:**

```yaml
# 1. EXPERIMENT CONTEXT (research framing)
experiment_meta: {...}

# 2. FRAMEWORK IDENTIFICATION (basic framework info)
framework:
  name: "..."
  version: "v3.2"
  description: "..."

# 3. EARLY COGNITIVE PRIMING (domain and methodology)
  expert_role: |
    Domain expertise without component references
  methodological_approach: |
    Analysis methodology without technical details

# 4. FRAMEWORK STRUCTURE (technical definitions)
  components: {...}
  axes: {...}
  competitive_relationships: {...}

# 5. DETAILED IMPLEMENTATION (component references)
  detailed_prompts:
    framework_application: |
      Specific guidance referencing components above
    scoring_methodology: |
      Precise instructions using framework elements

# 6. EXPERIMENT EXECUTION (analysis workflow)
models: {...}
corpus: {...}
```

### **Common Implementation Mistakes**

**❌ Anti-Pattern: Forward References in Early Prompts**
```yaml
# WRONG: Early prompt references undefined framework elements
expert_role: |
  Apply the language_cues defined in the components section...  # BROKEN REFERENCE
  
components:
  # Components defined after being referenced above
```

**❌ Anti-Pattern: Late Context Setting**
```yaml
# WRONG: Domain expertise established after framework structure
components: {...}
axes: {...}

expert_role: |  # TOO LATE - framework already processed without context
  You are an expert analyst...
```

**✅ Correct Pattern: Sequential Context Building**
```yaml
# CORRECT: Context → Structure → Implementation
expert_role: |
  Domain expertise without forward references
  
components: {...}  # Framework structure with proper context
axes: {...}

detailed_prompts:  # Implementation guidance with backward references
  framework_application: |
    Apply the components defined above...
```

### **Framework Embedding Quality Assurance**

**Validation Checklist:**
- [ ] **Expert Role Early**: Domain expertise established before framework structure
- [ ] **No Forward References**: Early prompts don't reference undefined elements
- [ ] **Framework Structure Complete**: All components, axes, relationships defined
- [ ] **Detailed Implementation**: Specific guidance references framework elements
- [ ] **Sequential Flow**: Logical progression from context to structure to implementation

**Processing Verification:**
- [ ] **Context Priming**: LLM has domain expertise before encountering technical elements
- [ ] **Reference Resolution**: All framework element references can be resolved
- [ ] **Implementation Clarity**: Detailed prompts provide specific guidance for framework application
- [ ] **Experiment Integration**: Framework embedding works seamlessly in experiment context

### **Cross-Reference Documentation**

- **Theoretical Foundation**: **[Framework Specification v3.2 - Framework Embedding Best Practices](Discernus_Coordinate_System_Framework_Specification_3_2.md#framework-embedding-best-practices)**
- **Cognitive Processing Research**: LLM sequential attention and context establishment principles
- **Implementation Examples**: Current production experiments demonstrating optimal prompt placement
- **Quality Validation**: Framework embedding validation protocols and common error patterns

### **Academic Integration Implications**

**Research Reproducibility**: Proper prompt placement ensures consistent LLM processing across different research contexts and framework applications.

**Methodological Rigor**: Sequential context establishment improves analytical reliability and reduces prompt-dependent variation in research results.

**Framework Portability**: Standardized embedding architecture enables framework reuse across different experiments while maintaining analytical consistency.

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