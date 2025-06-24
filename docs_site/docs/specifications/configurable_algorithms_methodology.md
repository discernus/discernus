# Configurable Algorithms Methodology
**Version:** 3.0  
**Date:** June 23, 2025  
**Status:** DRAFT - Implementation Phase  

## 🎯 **OVERVIEW**

The Discernus Configurable Algorithms system represents a sophisticated methodological framework that integrates Large Language Model (LLM) analysis with mathematical coordinate positioning. This document provides comprehensive documentation of the **LLM-prompting-amplification pipeline** and guidance for researchers on configuring algorithmic parameters for different research contexts.

## 🧠 **THEORETICAL FOUNDATION**

### **The LLM-Mathematical Integration Paradigm**

Traditional text analysis approaches often treat computational assessment and mathematical positioning as separate processes. Discernus implements a **unified methodological approach** where:

1. **LLM Semantic Understanding**: Advanced language models identify nuanced patterns, hierarchies, and dominance relationships in text
2. **Mathematical Enhancement**: Optional algorithmic amplification of computationally-identified patterns for improved analytical clarity
3. **Coordinate Positioning**: Integration of researcher enhanced assessments into geometric coordinate space for visualization and comparison

This integration enables analysis that leverages both **human-like semantic understanding** (via LLMs) and **mathematical rigor** (via coordinate positioning algorithms).

## 🔄 **THE LLM-PROMPTING-AMPLIFICATION PIPELINE**

The following represents an optional configuration of frameworks to apply a particular form of amplification and describes how this amplification is achieved through a combination of framework definition parameters.

### **Stage 1: LLM Prompting for Dominance Identification**

**Objective**: Instruct the LLM to identify hierarchical dominance patterns within analyzed text.

**Methodology**:
- **Dominance Instruction Prompting**: Specialized prompts direct the LLM to assess not just presence/absence of framework elements, but their **relative dominance** and **hierarchical relationships**
- **Scoring Contextualization**: LLMs provide scores that reflect the **strength of dominance** rather than simple presence/absence
- **Evidence-Based Assessment**: LLMs are instructed to identify specific textual evidence supporting dominance hierarchies

**Example Prompting Strategy** (Moral Foundations Theory):
```
Analyze this text for moral foundation dominance patterns. For each foundation:
1. Assess its DOMINANCE level (not just presence) on a 0.0-1.0 scale
2. Identify hierarchical relationships between foundations ad defined in Moral Foundations Theory
3. Provide specific textual evidence for high-dominance (>0.7) assessments
4. Consider how foundations interact and compete for narrative control
```

### **Stage 2: Mathematical Amplification**

**Objective**: Apply algorithmic enhancement to LLM-identified dominance patterns for improved analytical clarity.

**Methodology**:
- **Dominance Amplification**: Scores above a configured threshold (default: 0.7) receive multiplicative enhancement (default: 1.1x)
- **Adaptive Scaling**: Dynamic scaling factors optimize coordinate space utilization based on narrative characteristics
- **Boundary Optimization**: Enhanced positioning ensures full utilization of coordinate space for maximum analytical clarity

**Mathematical Rationale**:
- **High-Score Enhancement**: LLM-identified dominant themes receive mathematical emphasis to reflect their analytical importance
- **Analytical Clarity**: Amplification increases separation between dominant and non-dominant elements in coordinate space
- **Visual Representation**: Enhanced coordinates produce clearer, more interpretable visualizations

### **Stage 3: Coordinate Integration**

**Objective**: Integrate enhanced assessments into geometric coordinate positioning for visualization and comparative analysis.

**Methodology**:
- **Vector Summation**: Enhanced scores are combined using weighted vector mathematics
- **Coordinate Calculation**: Final narrative position reflects both LLM assessment and mathematical enhancement
- **Visualization Representation**: Coordinate positions directly reflect the integrated LLM-mathematical assessment

## ⚙️ **CONFIGURABLE ALGORITHM PARAMETERS**

### **Dominance Amplification Configuration**

```yaml
dominance_amplification:
  enabled: true                    # Enable/disable amplification
  threshold: 0.7                   # Score threshold for amplification
  multiplier: 1.1                  # Amplification factor
  rationale: "Enhances LLM-identified dominant themes"
```

**Parameter Guidance**:

| Parameter | Research Context | Recommended Value | Rationale |
|-----------|------------------|-------------------|-----------|
| `threshold` | Conservative Analysis | 0.8 | Higher threshold for amplification |
| `threshold` | Exploratory Analysis | 0.6 | Lower threshold captures emerging themes |
| `multiplier` | Subtle Enhancement | 1.05 | Minimal mathematical enhancement |
| `multiplier` | Strong Enhancement | 1.2 | Pronounced dominance highlighting |

### **Adaptive Scaling Configuration**

```yaml
adaptive_scaling:
  enabled: true                    # Enable/disable adaptive scaling
  base_scaling: 0.65              # Minimum scaling factor
  max_scaling: 0.95               # Maximum scaling factor  
  variance_factor: 0.3            # Variance sensitivity
  mean_factor: 0.1                # Mean score sensitivity
  methodology: "Optimizes boundary utilization"
```

**Parameter Guidance**:

| Parameter | Research Context | Recommended Range | Rationale |
|-----------|------------------|-------------------|-----------|
| `base_scaling` | Detailed Analysis | 0.5-0.7 | Lower scaling for fine-grained positioning |
| `base_scaling` | Overview Analysis | 0.7-0.9 | Higher scaling for broad patterns |
| `variance_factor` | Homogeneous Texts | 0.1-0.2 | Less variance sensitivity |
| `variance_factor` | Diverse Texts | 0.3-0.5 | More variance sensitivity |

### **Prompting Integration Configuration**

```yaml
prompting_integration:
  dominance_instruction: "Identify hierarchical dominance patterns"
  amplification_purpose: "Mathematical enhancement of identified dominance"
  methodology_reference: "LLM-prompting-amplification pipeline"
```

## 🔬 **RESEARCH APPLICATIONS**

### **When to Configure Algorithm Parameters**

#### **Framework-Specific Configurations**

**Moral Foundations Theory**:
- **Standard Configuration**: Default parameters work well for most political/moral texts
- **Religious Texts**: Increase `threshold` to 0.8 for conservative amplification
- **Political Speeches**: Decrease `threshold` to 0.6 for capturing rhetorical nuances

**Custom Frameworks**:
- **Binary Frameworks**: Higher `multiplier` (1.2-1.3) for clear dominance patterns
- **Complex Frameworks**: Lower `multiplier` (1.05-1.1) for subtle interactions
- **Experimental Frameworks**: Enable/disable amplification for methodological comparison

#### **Research Context Configurations**

**Exploratory Studies**:
- Lower thresholds and multipliers to capture emerging patterns
- Higher variance factors to adapt to diverse text characteristics
- Conservative scaling to maintain analytical nuance

**Confirmatory Studies**:
- Standard or higher thresholds for established pattern confirmation
- Moderate multipliers for clear visualization
- Adaptive scaling optimized for the specific corpus characteristics

**Comparative Studies**:
- **Critical**: Use identical algorithm configurations across all comparisons
- Document algorithm parameters in academic publications
- Consider algorithm sensitivity analysis as part of methodological rigor

### **Methodological Implications**

#### **Reproducibility Requirements**

1. **Algorithm Parameter Documentation**: All parameters must be explicitly reported in academic publications
2. **Configuration Preservation**: Experiment configurations should be saved and archived
3. **Sensitivity Analysis**: Consider testing multiple parameter configurations for robustness
4. **Comparative Consistency**: Use identical parameters when comparing across texts/conditions

#### **Interpretive Guidelines**

1. **Enhanced Scores**: Amplified values reflect LLM-identified dominance, not raw presence
2. **Coordinate Positioning**: Final positions integrate both semantic assessment and mathematical enhancement
3. **Visualization Interpretation**: Charts display the combined LLM-mathematical assessment, not raw LLM scores
4. **Statistical Analysis**: Use enhanced values for coordinate-based statistics, raw values for score-based analysis

## 📊 **ACADEMIC REPORTING GUIDELINES**

### **Methods Section Requirements**

**Minimum Reporting Standards**:
```
Narrative positioning analysis employed the Discernus LLM-prompting-amplification 
pipeline with the following algorithmic configuration:

- Dominance amplification: [enabled/disabled]
  - Threshold: [value] (scores above this threshold received amplification)
  - Multiplier: [value] (amplification factor applied to dominant themes)
- Adaptive scaling: [enabled/disabled]  
  - Base scaling: [value] (minimum coordinate scaling factor)
  - Maximum scaling: [value] (maximum coordinate scaling factor)
  - Variance factor: [value] (sensitivity to score variance)
  - Mean factor: [value] (sensitivity to mean score levels)

Framework: [Framework Name] v[Version]
LLM Model: [Model Name and Version]
Analysis Date: [Date Range]
```

### **Results Section Considerations**

1. **Coordinate Values**: Report that displayed coordinates reflect enhanced values, not raw LLM scores
2. **Dominance Patterns**: Explicitly note when themes received amplification enhancement
3. **Methodological Integration**: Acknowledge the LLM-mathematical integration approach
4. **Parameter Sensitivity**: Consider reporting sensitivity analysis if parameters were varied

## 🔧 **IMPLEMENTATION EXAMPLES**

### **Conservative Political Analysis**

```yaml
algorithm_config:
  dominance_amplification:
    enabled: true
    threshold: 0.8        # Higher threshold for conservative amplification
    multiplier: 1.05      # Subtle enhancement
  adaptive_scaling:
    enabled: true
    base_scaling: 0.7     # Higher base for clearer patterns
    max_scaling: 0.9      # Moderate maximum
    variance_factor: 0.2  # Lower sensitivity for focused analysis
```

### **Exploratory Cultural Analysis**

```yaml
algorithm_config:
  dominance_amplification:
    enabled: true
    threshold: 0.6        # Lower threshold for emerging themes
    multiplier: 1.15      # Moderate enhancement
  adaptive_scaling:
    enabled: true
    base_scaling: 0.6     # Lower base for detailed positioning
    max_scaling: 0.95     # Full range utilization
    variance_factor: 0.4  # Higher sensitivity for diverse texts
```

### **Methodological Comparison Study**

```yaml
# Configuration A: Standard Enhancement
algorithm_config:
  dominance_amplification:
    enabled: true
    threshold: 0.7
    multiplier: 1.1
    
# Configuration B: Conservative Enhancement  
algorithm_config:
  dominance_amplification:
    enabled: true
    threshold: 0.8
    multiplier: 1.05
    
# Configuration C: No Enhancement (Control)
algorithm_config:
  dominance_amplification:
    enabled: false
```

## 🚀 **FUTURE DEVELOPMENTS**

### **Planned Enhancements**

1. **Dynamic Parameter Learning**: Machine learning approaches to optimize parameters for specific corpora
2. **Context-Aware Configuration**: Automatic parameter adjustment based on text characteristics
3. **Multi-Model Integration**: Support for different LLM models with model-specific configurations
4. **Statistical Validation**: Built-in sensitivity analysis and robustness testing

### **Research Opportunities**

1. **Algorithm Sensitivity Studies**: Systematic analysis of parameter impact on results
2. **Cross-Framework Validation**: Comparing algorithmic approaches across different theoretical frameworks
3. **Methodological Development**: Advancing the LLM-mathematical integration paradigm
4. **Reproducibility Research**: Best practices for algorithmic transparency in computational text analysis

## 📊 **CHART OUTPUT OPTIONS FOR ACADEMIC TRANSPARENCY**

### **Academic Reporting Flexibility**

To enhance academic transparency and methodological validation, experiments can specify how algorithmic enhancement is presented in visualizations:

#### **Raw Scores Only**
```yaml
visualization_config:
  chart_output_mode: "raw_only"
  rationale: "Control condition or baseline analysis without algorithmic enhancement"
```

**Use Cases**:
- Control conditions in algorithm sensitivity studies
- Baseline analysis for comparison with enhanced results
- Studies where amplification is disabled or inappropriate

#### **Enhanced Scores Only** 
```yaml
visualization_config:
  chart_output_mode: "enhanced_only"
  rationale: "Final results with researcher-configured algorithmic enhancement"
```

**Use Cases**:
- Applied research with established algorithmic parameters
- Studies where space constraints limit figure count
- Final presentation of validated algorithmic approach

#### **Both Raw and Enhanced (Recommended for Academic Work)**
```yaml
visualization_config:
  chart_output_mode: "both_comparison"
  layout: "side_by_side"  # Options: "side_by_side", "overlay", "separate_figures"
  rationale: "Academic transparency - demonstrate algorithmic impact"
```

**Use Cases**:
- **Methodological papers**: Demonstrating algorithm effectiveness
- **Peer review**: Allowing assessment of algorithmic appropriateness  
- **Sensitivity analysis**: Explicitly testing algorithm impact
- **Reproducibility**: Enabling validation of algorithmic influence

### **Academic Reporting Standards**

When using `both_comparison` mode, the following documentation is recommended:

#### **Methods Section Addition**
```
Visualization Analysis: Charts present both raw LLM scores and algorithmically-enhanced 
scores to demonstrate the impact of [specific algorithmic configuration]. Raw scores 
represent direct LLM assessment, while enhanced scores reflect the application of 
dominance amplification (threshold: X.X, multiplier: X.X) and adaptive scaling 
(range: X.X-X.X). This dual presentation enables assessment of algorithmic influence 
on narrative positioning and coordinate calculations.
```

#### **Figure Captions**
```
Figure X: Narrative positioning comparison showing (A) raw LLM scores and (B) 
algorithmically-enhanced scores. Enhancement applied dominance amplification 
[parameters] and adaptive scaling [parameters]. Algorithm configuration detailed 
in Methods section.
```

### **Methodological Implications**

#### **For Algorithm Development Studies**
- **Required**: `both_comparison` mode to validate algorithmic contribution
- **Documentation**: Detailed comparison of raw vs. enhanced positioning
- **Analysis**: Statistical testing of algorithmic impact on results

#### **For Applied Research Studies**  
- **Recommended**: `enhanced_only` for clear presentation
- **Documentation**: Full algorithmic parameter reporting in methods
- **Justification**: Rationale for algorithmic configuration choices

#### **For Comparative Studies**
- **Critical**: Identical chart output mode across all conditions
- **Transparency**: Algorithm parameters must be identical or differences explicitly noted
- **Validation**: Consider sensitivity analysis with multiple configurations

### **Implementation in Experiment Definitions**

Example experiment configuration:

```yaml
enhanced_analysis:
  enabled: true
  configuration:
    visualizations:
      chart_output_mode: "both_comparison"
      layout: "side_by_side"
      include_algorithm_attribution: true
      academic_citation_ready: true
    
    academic_reporting:
      generate_methods_text: true
      generate_figure_captions: true
      include_sensitivity_analysis: false  # Set true for methodological studies
```

This approach ensures that algorithmic enhancement serves academic rigor rather than obscuring methodological transparency.

---

**Document Version**: 3.0 DRAFT  
**Last Updated**: June 23, 2025  
**Next Review**: Post-Implementation Validation  
**Related Documents**: 
- Framework Specification v3.0
- Configurable Algorithms Implementation Plan  
- User Guide: Configuring Algorithms 