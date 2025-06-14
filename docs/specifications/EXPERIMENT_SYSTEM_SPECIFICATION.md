# Experiment System Specification
*Version: 2.1.0*
*Last Updated: June 13, 2025*

## **🎯 Overview**

The Narrative Gravity Analysis System provides a comprehensive experimental framework for systematic research using Large Language Models (LLMs) to analyze text narratives. This document specifies all available options, parameters, and capabilities for designing and executing experiments.

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

### **1. Framework Configurations**

**Purpose**: Define the theoretical space for narrative analysis through dimensional structures.

#### **Framework Structure**
```json
{
  "framework_name": "string (unique identifier)",
  "display_name": "string (human-readable name)",
  "version": "string (semantic versioning)",
  "description": "string (theoretical foundation description)",
  
  "coordinate_system": {
    "type": "enum[circle, ellipse, linear]",
    "radius": "number (for circle)",
    "semi_major_axis": "number (for ellipse)",
    "semi_minor_axis": "number (for ellipse)",
    "description": "string (geometric interpretation)"
  },
  
  "wells": {
    "WellName": {
      "angle": "number (0-360 degrees)",
      "weight": "number (relative importance)",
      "type": "enum[integrative, disintegrative]",
      "tier": "enum[primary, secondary, tertiary]",
      "description": "string (analytical dimension meaning)"
    }
  },
  
  "theoretical_foundation": {
    "primary_sources": ["array of academic references"],
    "theoretical_approach": "string (methodological foundation)"
  },
  
  "metrics": {
    "MetricName": {
      "name": "string (human-readable name)",
      "description": "string (calculation and interpretation)"
    }
  }
}
```

#### **Available Frameworks**

**Civic Virtue Framework** (`civic_virtue v2025.06.04`)
- **Dimensions**: 10 wells across 5 dipoles (Dignity/Tribalism, Truth/Resentment, Justice/Manipulation, Hope/Fear, Pragmatism/Fantasy)
- **Theoretical Foundation**: Aristotelian virtue ethics + contemporary civic republican theory
- **Use Case**: Political discourse analysis, democratic engagement assessment
- **Coordinate System**: Circular (clustered positioning)

**Political Spectrum Framework** (`political_spectrum v2025.06.04`)
- **Dimensions**: Traditional left-right political analysis
- **Theoretical Foundation**: Political science spectrum analysis
- **Use Case**: Partisan rhetoric analysis, political positioning
- **Coordinate System**: Linear or elliptical

**Moral-Rhetorical Posture Framework** (`moral_rhetorical_posture v2025.06.04`)
- **Dimensions**: Moral foundations + rhetorical strategies
- **Theoretical Foundation**: Haidt's moral foundations + rhetorical analysis
- **Use Case**: Moral argumentation patterns, persuasive strategy analysis
- **Coordinate System**: Elliptical

#### **Framework Development**
- **Versioning**: Semantic versioning (major.minor.patch)
- **Validation**: Theoretical coherence, dimensional distinctness, empirical testability
- **Compatibility**: Must specify compatible prompt templates and scoring algorithms

### **2. Prompt Templates**

**Purpose**: Define how LLMs should perform narrative analysis within the framework structure.

#### **Prompt Template Types**

**Hierarchical Analysis** (`hierarchical_v2.1`)
- **Approach**: LLM ranks dimensions by importance and provides evidence
- **Output Format**: Hierarchical ranking with primary/secondary/tertiary wells
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
```json
{
  "template_id": "string (unique identifier)",
  "name": "string (human-readable name)", 
  "version": "string (semantic versioning)",
  "type": "enum[hierarchical, traditional, evidence_based]",
  "description": "string (methodological approach)",
  
  "analysis_requirements": {
    "evidence_required": "boolean",
    "justification_depth": "enum[minimal, standard, comprehensive]",
    "ranking_required": "boolean", 
    "framework_fit_assessment": "boolean"
  },
  
  "output_format": {
    "structure": "enum[json, structured_text, hybrid]",
    "required_fields": ["array of mandatory response fields"],
    "scoring_scale": "string (e.g., '0.0-1.0', 'ordinal')"
  },
  
  "llm_guidance": {
    "temperature_recommendation": "number (0.0-1.0)",
    "max_tokens": "number (response length)",
    "model_compatibility": ["array of compatible LLM models"]
  }
}
```

#### **Prompt Quality Standards**
- **Framework Agnostic**: Templates should work across multiple frameworks
- **Model Independent**: Compatible with different LLM providers  
- **Output Consistency**: Reliable JSON structure for parsing
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
```json
{
  "algorithm_id": "string (unique identifier)",
  "name": "string (human-readable name)",
  "version": "string (semantic versioning)",
  "type": "enum[linear, winner_take_most, hierarchical, exponential, nonlinear]",
  "description": "string (mathematical approach)",
  
  "mathematical_foundation": {
    "primary_formula": "string (LaTeX or description)",
    "normalization_method": "string",
    "edge_case_handling": "string"
  },
  
  "parameters": {
    "parameter_name": {
      "default_value": "number",
      "valid_range": "string (min-max)",
      "description": "string (parameter meaning)"
    }
  },
  
  "compatibility": {
    "framework_types": ["array of compatible frameworks"],
    "prompt_types": ["array of compatible prompt templates"],
    "mathematical_requirements": ["array of input requirements"]
  }
}
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
```json
{
  "llm_model": "string (model identifier)",
  "provider": "enum[openai, anthropic, mistral, google_ai]",
  "version": "string (model version)",
  
  "analysis_parameters": {
    "temperature": "number (0.0-1.0, creativity level)",
    "max_tokens": "number (response length limit)",
    "top_p": "number (nucleus sampling parameter)",
    "frequency_penalty": "number (repetition control)",
    "presence_penalty": "number (topic diversity)"
  },
  
  "cost_parameters": {
    "input_cost_per_1k": "number (USD per 1K input tokens)",
    "output_cost_per_1k": "number (USD per 1K output tokens)",
    "rate_limit": "number (requests per minute)"
  },
  
  "capability_profile": {
    "context_window": "number (maximum input tokens)",
    "json_reliability": "enum[high, medium, low]",
    "reasoning_depth": "enum[high, medium, low]",
    "evidence_quality": "enum[high, medium, low]",
    "consistency": "enum[high, medium, low]"
  }
}
```

## **⚙️ Experiment Configuration**

### **Experiment Definition Schema**

```json
{
  "experiment": {
    "name": "string (required, unique identifier)",
    "hypothesis": "string (research hypothesis)",
    "description": "string (experiment overview)",
    "research_context": "string (academic context and background)",
    
    "metadata": {
      "researcher": "string (creator identifier)",
      "institution": "string (research affiliation)",
      "tags": ["array of research tags"],
      "research_notes": "string (methodology notes)",
      "publication_status": "enum[draft, active, completed, published]"
    }
  },
  
  "configuration": {
    "framework_config_id": "string (required)",
    "prompt_template_id": "string (required)", 
    "scoring_algorithm_id": "string (required)",
    "analysis_mode": "enum[single_model, multi_model, comparative]",
    "selected_models": ["array of LLM model identifiers"]
  },
  
  "execution_parameters": {
    "runs_per_text": "number (reliability validation)",
    "randomize_order": "boolean (reduce order effects)",
    "cost_limit": "number (USD maximum)",
    "timeout_seconds": "number (per-run timeout)",
    "retry_attempts": "number (failure handling)"
  },
  
  "quality_assurance": {
    "enable_qa_validation": "boolean",
    "confidence_threshold": "number (minimum QA confidence)",
    "require_evidence": "boolean",
    "manual_review_triggers": ["array of conditions"]
  }
}
```

### **Analysis Modes**

**Single Model Analysis** (`single_model`)
- **Purpose**: Focused analysis with one LLM model
- **Use Cases**: Cost-efficient analysis, model-specific research
- **Reliability**: Multiple runs with same model for consistency
- **Output**: Single model results with statistical reliability measures

**Multi-Model Comparison** (`multi_model`)
- **Purpose**: Cross-model validation and consensus analysis
- **Use Cases**: Academic research, validation studies, bias detection
- **Reliability**: Correlation analysis across different LLM providers
- **Output**: Consensus analysis with inter-model agreement metrics

**Comparative Analysis** (`comparative`)
- **Purpose**: Systematic comparison across multiple experimental conditions
- **Use Cases**: Methodological research, framework validation, prompt optimization
- **Reliability**: Controlled comparison with statistical significance testing
- **Output**: Comparative results with effect size calculations

### **Quality Assurance Integration**

**6-Layer QA System**: All experiments can optionally include comprehensive quality validation:

1. **Input Validation**: Text quality, framework compatibility, parameter validation
2. **LLM Response Validation**: JSON format, required fields, score ranges
3. **Statistical Coherence**: Default value detection, variance analysis, pattern recognition
4. **Mathematical Consistency**: Position calculation validation, reproducibility verification
5. **Cross-Validation**: Second opinion requirements, anomaly flagging
6. **Anomaly Detection**: Perfect symmetry, outliers, identical scores

**QA Configuration Options**:
- **Confidence Thresholds**: HIGH (≥0.8), MEDIUM (0.5-0.79), LOW (<0.5)
- **Automatic Filtering**: Exclude low-confidence results from analysis
- **Manual Review Triggers**: Flag analyses requiring human validation
- **Reporting Integration**: Include QA metrics in all academic outputs

## **📊 Experimental Outputs**

### **Run-Level Results**

Each individual LLM analysis produces:
```json
{
  "run_id": "string (unique identifier)",
  "text_id": "string (source text identifier)",
  "llm_model": "string (model used)",
  "execution_time": "timestamp",
  "duration_seconds": "number",
  "api_cost": "number (USD)",
  
  "analysis_results": {
    "raw_scores": {"WellName": "number", ...},
    "hierarchical_ranking": {...} // if hierarchical prompt
    "well_justifications": {...} // if evidence required
    "framework_fit_score": "number (0.0-1.0)",
    "narrative_position": {"x": "number", "y": "number"}
  },
  
  "quality_metadata": {
    "qa_confidence_level": "enum[HIGH, MEDIUM, LOW]",
    "qa_confidence_score": "number (0.0-1.0)",
    "anomalies_detected": ["array of anomaly types"],
    "requires_second_opinion": "boolean"
  },
  
  "provenance": {
    "framework_version": "string",
    "prompt_template_version": "string",
    "scoring_algorithm_version": "string",
    "complete_configuration": {...}
  }
}
```

### **Experiment-Level Results**

Aggregated analysis across all runs:
```json
{
  "experiment_summary": {
    "total_runs": "number",
    "successful_runs": "number", 
    "total_cost": "number (USD)",
    "average_duration": "number (seconds)",
    "execution_period": "string (start - end dates)"
  },
  
  "reliability_analysis": {
    "coefficient_variation": "number (consistency measure)",
    "intraclass_correlation": "number (if multi-model)",
    "reliability_rate": "number (% achieving target CV)",
    "framework_fit_statistics": {...}
  },
  
  "academic_outputs": {
    "publication_ready_dataset": "path to CSV/Feather/JSON exports",
    "jupyter_analysis_notebook": "path to generated notebook",
    "r_analysis_scripts": "path to R statistical scripts",
    "methodology_documentation": "path to methods documentation",
    "replication_package": "path to complete replication materials"
  }
}
```

## **🔬 Advanced Experimental Capabilities**

### **Component Matrix Experiments**

Systematic testing across multiple component combinations:
```json
{
  "matrix_experiment": {
    "frameworks": ["civic_virtue", "political_spectrum"],
    "prompt_templates": ["hierarchical_v2.1", "traditional_v2.0"],
    "scoring_algorithms": ["linear_v1.0", "hierarchical_v1.0"],
    "models": ["gpt-4.1-mini", "claude-3-5-sonnet"]
  }
}
```

**Output**: Complete factorial analysis with:
- Component interaction effects
- Optimal configuration identification  
- Methodological recommendations
- Statistical significance testing

### **Longitudinal Studies**

Time-series analysis capabilities:
```json
{
  "longitudinal_experiment": {
    "temporal_corpus": {
      "time_periods": ["2020-01", "2020-02", ...],
      "texts_per_period": "number",
      "temporal_metadata": "required"
    },
    "trend_analysis": {
      "enable_trend_detection": "boolean",
      "periodicity_detection": "boolean", 
      "change_point_analysis": "boolean"
    }
  }
}
```

### **Validation Studies**

Human-LLM comparison protocols:
```json
{
  "validation_experiment": {
    "human_coding": {
      "expert_coders": "number",
      "inter_rater_reliability_target": "number",
      "coding_protocol": "string (methodology)"
    },
    "llm_comparison": {
      "correlation_targets": "number (human-LLM agreement)",
      "bias_detection": "boolean",
      "systematic_error_analysis": "boolean"
    }
  }
}
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