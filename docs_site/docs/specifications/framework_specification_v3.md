# Framework Specification v3.0
**Version:** 3.0  
**Date:** June 23, 2025  
**Status:** DRAFT - Implementation Phase  
**Breaking Changes:** Adds configurable algorithm support, deprecates JSON framework loading  

## 🎯 **OVERVIEW**

Framework Specification v3.0 introduces **configurable algorithms** to the Discernus framework architecture, enabling researchers to customize mathematical enhancement parameters for different research contexts. This specification maintains backward compatibility while adding sophisticated algorithmic configuration capabilities.

## 🚀 **VERSION 3.0 ENHANCEMENTS**

### **New Features**
- ✅ **Configurable Algorithm Parameters**: Researchers can customize dominance amplification and adaptive scaling
- ✅ **LLM-Mathematical Integration**: Documented methodology for prompting-amplification pipeline
- ✅ **Academic Transparency**: Algorithm parameters explicitly reportable in publications
- ✅ **Research Context Adaptation**: Framework-specific and study-specific algorithm configurations

### **Deprecated Features**  
- ❌ **JSON Framework Loading**: YAML-only architecture for consistency
- ❌ **Hardcoded Algorithm Parameters**: All parameters now configurable

### **Backward Compatibility**
- ✅ **Existing Frameworks**: Work unchanged with default algorithm configurations
- ✅ **API Compatibility**: No breaking changes to existing API calls
- ✅ **Experiment Definitions**: Existing experiments continue to work with sensible defaults

## 📋 **FRAMEWORK YAML STRUCTURE v3.0**

### **Complete Framework Schema**

```yaml
# =============================================================================
# FRAMEWORK METADATA
# =============================================================================
name: framework_identifier
framework_name: framework_identifier 
display_name: "Human-Readable Framework Name"
version: v2025.06.23
description: |
  Comprehensive framework description including theoretical foundation
  and methodological approach.
framework_type: anchors_based

# =============================================================================
# NEW IN v3.0: ALGORITHM CONFIGURATION
# =============================================================================
algorithm_config:
  dominance_amplification:
    enabled: true                    # Enable/disable dominance amplification
    threshold: 0.7                   # Score threshold for amplification (0.0-1.0)
    multiplier: 1.1                  # Amplification factor (1.0-2.0 recommended)
    rationale: "Enhances LLM-identified dominant themes for analytical clarity"
    
  adaptive_scaling:
    enabled: true                    # Enable/disable adaptive scaling
    base_scaling: 0.65              # Minimum scaling factor (0.3-0.8 range)
    max_scaling: 0.95               # Maximum scaling factor (0.8-1.0 range)
    variance_factor: 0.3            # Variance sensitivity (0.1-0.5 range)
    mean_factor: 0.1                # Mean score sensitivity (0.05-0.2 range)
    methodology: "Optimizes coordinate space utilization based on narrative characteristics"
    
  prompting_integration:
    dominance_instruction: "Identify hierarchical dominance patterns in the analyzed text"
    amplification_purpose: "Mathematical enhancement of computationally-identified dominance"
    methodology_reference: "LLM-prompting-amplification pipeline v3.0"

# =============================================================================
# COORDINATE SYSTEM
# =============================================================================
coordinate_system:
  type: circle
  radius: 1.0
  description: "Circular coordinate system using anchors for semantic positioning"

# =============================================================================  
# ANCHORS (SEMANTIC REFERENCE POINTS)
# =============================================================================
anchors:
  AnchorName:
    description: "Comprehensive description of the semantic anchor"
    angle: 0                        # Position in degrees (0-359)
    weight: 1.0                     # Relative importance (0.1-2.0)
    type: anchor_type               # Type for coloring and grouping
    language_cues:                  # Keywords/phrases associated with this anchor
      - keyword1
      - keyword2
      - phrase pattern

# =============================================================================
# VISUALIZATION CONFIGURATION  
# =============================================================================
anchor_type_colors:
  anchor_type: "#HEX_COLOR"         # Color mapping for visualization

# =============================================================================
# ANALYSIS METRICS (OPTIONAL)
# =============================================================================
metrics:
  metric_name:
    name: "Human-Readable Metric Name"
    description: "What this metric measures"
    calculation: "How the metric is calculated from anchor scores"

# =============================================================================
# PROMPT INTEGRATION
# =============================================================================
prompt_configuration:
  expert_role: |
    Role definition for the LLM analysis expert persona
  
  bias_neutral_analysis_focus: |
    Instructions for objective, unbiased analysis approach
  
  detection_approach: |
    Specific instructions for identifying framework elements in text
  
  scoring_methodology: |
    Guidelines for scoring framework elements on 0.0-1.0 scale

# =============================================================================
# SYSTEM COMPATIBILITY
# =============================================================================
compatibility:
  prompt_templates:
    - template_v1.0
  weighting_schemes:
    - scheme_name
  api_versions:
    - v2.0
    - v2.1

# =============================================================================
# ACADEMIC VALIDATION
# =============================================================================
validation:
  academic_standard: "Reference theoretical framework"
  measurement_instrument: "Validation instruments used"
  scope_limitation: "Known limitations and scope boundaries"

# =============================================================================
# FRAMEWORK VERSIONING
# =============================================================================
last_modified: "2025-06-23T12:00:00.000000"
```

## ⚙️ **ALGORITHM CONFIGURATION SPECIFICATION**

### **Dominance Amplification Configuration**

```yaml
dominance_amplification:
  enabled: true                    # Boolean: Enable/disable amplification
  threshold: 0.7                   # Float (0.0-1.0): Score threshold for amplification
  multiplier: 1.1                  # Float (1.0-2.0): Amplification factor
  rationale: "String describing the methodological purpose"
```

**Parameter Specifications**:

| Parameter | Type | Range | Default | Purpose |
|-----------|------|-------|---------|---------|
| `enabled` | Boolean | true/false | true | Enable/disable amplification entirely |
| `threshold` | Float | 0.0-1.0 | 0.7 | Score above which amplification is applied |
| `multiplier` | Float | 1.0-2.0 | 1.1 | Factor by which qualifying scores are multiplied |
| `rationale` | String | N/A | Required | Methodological explanation for documentation |

**Validation Rules**:
- `threshold` must be between 0.0 and 1.0
- `multiplier` must be ≥ 1.0 (cannot reduce scores)
- `multiplier` > 2.0 generates warning (excessive amplification)
- `rationale` required for academic transparency

### **Adaptive Scaling Configuration**

```yaml
adaptive_scaling:
  enabled: true                    # Boolean: Enable/disable adaptive scaling
  base_scaling: 0.65              # Float: Minimum scaling factor
  max_scaling: 0.95               # Float: Maximum scaling factor
  variance_factor: 0.3            # Float: Variance sensitivity coefficient
  mean_factor: 0.1                # Float: Mean score sensitivity coefficient
  methodology: "String describing the scaling approach"
```

**Parameter Specifications**:

| Parameter | Type | Range | Default | Purpose |
|-----------|------|-------|---------|---------|
| `enabled` | Boolean | true/false | true | Enable/disable adaptive scaling |
| `base_scaling` | Float | 0.3-0.8 | 0.65 | Minimum coordinate scaling factor |
| `max_scaling` | Float | 0.8-1.0 | 0.95 | Maximum coordinate scaling factor |
| `variance_factor` | Float | 0.1-0.5 | 0.3 | Sensitivity to score variance |
| `mean_factor` | Float | 0.05-0.2 | 0.1 | Sensitivity to mean score levels |
| `methodology` | String | N/A | Required | Scaling methodology explanation |

**Validation Rules**:
- `base_scaling` < `max_scaling` (logical ordering)
- `base_scaling` ≥ 0.3 (minimum meaningful scaling)
- `max_scaling` ≤ 1.0 (cannot exceed coordinate space)
- Variance and mean factors must be positive

### **Prompting Integration Configuration**

```yaml
prompting_integration:
  dominance_instruction: "Instructions for LLM dominance identification"
  amplification_purpose: "Explanation of mathematical enhancement purpose"
  methodology_reference: "Reference to methodological documentation"
```

**Purpose**: Documents the integration between LLM prompting and mathematical amplification for academic transparency and methodological rigor.

## 🔬 **FRAMEWORK CONFIGURATION EXAMPLES**

### **Example 1: Moral Foundations Theory with Standard Configuration**

```yaml
name: moral_foundations_theory
display_name: "Moral Foundations Theory (Haidt)"
version: v2025.06.23

# Standard algorithm configuration for political discourse analysis
algorithm_config:
  dominance_amplification:
    enabled: true
    threshold: 0.7
    multiplier: 1.1
    rationale: "Enhances dominant moral concerns for clearer political positioning"
    
  adaptive_scaling:
    enabled: true
    base_scaling: 0.65
    max_scaling: 0.95
    variance_factor: 0.3
    mean_factor: 0.1
    methodology: "Optimizes coordinate space for moral foundation visualization"
    
  prompting_integration:
    dominance_instruction: "Identify which moral foundations dominate the text's moral reasoning"
    amplification_purpose: "Mathematical emphasis of LLM-identified dominant moral themes"
    methodology_reference: "MFT LLM-prompting-amplification pipeline v3.0"

anchors:
  Care:
    description: "Concern for suffering, compassion, protection"
    angle: 0
    weight: 1.0
    type: individualizing
    # ... (rest of anchor configuration)
```

### **Example 2: Conservative Analysis Configuration**

```yaml
# Conservative amplification for detailed traditional value analysis
algorithm_config:
  dominance_amplification:
    enabled: true
    threshold: 0.8              # Higher threshold for conservative amplification
    multiplier: 1.05            # Subtle enhancement to preserve nuance
    rationale: "Conservative amplification preserves subtle traditional value patterns"
    
  adaptive_scaling:
    enabled: true
    base_scaling: 0.7           # Higher base scaling for clearer pattern visibility
    max_scaling: 0.9            # Moderate maximum to maintain analytical precision
    variance_factor: 0.2        # Lower variance sensitivity for focused analysis
    mean_factor: 0.05           # Reduced mean sensitivity for traditional contexts
    methodology: "Conservative scaling optimized for traditional value analysis"
```

### **Example 3: Exploratory Research Configuration**

```yaml
# Exploratory configuration for discovering emerging patterns
algorithm_config:
  dominance_amplification:
    enabled: true
    threshold: 0.6              # Lower threshold to capture emerging themes
    multiplier: 1.15            # Moderate enhancement for pattern clarity
    rationale: "Exploratory amplification captures emerging thematic patterns"
    
  adaptive_scaling:
    enabled: true
    base_scaling: 0.5           # Lower base for detailed positioning
    max_scaling: 0.95           # Full range utilization for maximum sensitivity
    variance_factor: 0.4        # Higher variance sensitivity for diverse texts
    mean_factor: 0.15           # Increased mean sensitivity for pattern detection
    methodology: "Exploratory scaling maximizes sensitivity to emerging patterns"
```

### **Example 4: Control/No Enhancement Configuration**

```yaml
# Control configuration with no algorithmic enhancement
algorithm_config:
  dominance_amplification:
    enabled: false              # Disable amplification entirely
    rationale: "Control configuration uses raw LLM scores without enhancement"
    
  adaptive_scaling:
    enabled: false              # Disable adaptive scaling
    methodology: "Control scaling uses fixed 0.8 scaling factor"
    
  prompting_integration:
    dominance_instruction: "Standard analysis without dominance emphasis"
    amplification_purpose: "No mathematical enhancement applied"
    methodology_reference: "Control methodology - raw LLM assessment only"
```

## 🧪 **RESEARCH METHODOLOGY INTEGRATION**

### **LLM Prompting Enhancement**

The `prompting_integration` section enables coordination between LLM instruction and mathematical enhancement:

1. **Dominance Instruction**: Directs LLM to assess hierarchical dominance patterns
2. **Amplification Purpose**: Documents why mathematical enhancement is methodologically justified
3. **Methodology Reference**: Links to comprehensive methodological documentation

### **Algorithm Parameter Selection Guidelines**

#### **By Research Context**

**Exploratory Studies**:
- Lower `threshold` (0.6-0.7) to capture emerging patterns
- Moderate `multiplier` (1.05-1.15) for balance
- Higher `variance_factor` (0.3-0.4) for sensitivity

**Confirmatory Studies**:
- Standard `threshold` (0.7-0.8) for established patterns  
- Standard `multiplier` (1.1) for consistency
- Moderate parameters for replication

**Comparative Studies**:
- **Critical**: Identical configurations across all comparisons
- Document parameters explicitly in publications
- Consider sensitivity analysis across multiple configurations

#### **By Framework Type**

**Binary Frameworks** (e.g., Liberal-Conservative):
- Higher `multiplier` (1.2-1.3) for clear distinction
- Standard threshold and scaling parameters

**Multi-Dimensional Frameworks** (e.g., Moral Foundations):
- Standard parameters (defaults) work well
- Adjust `variance_factor` based on expected text diversity

**Custom/Experimental Frameworks**:
- Start with defaults, iterate based on pilot results
- Document parameter selection rationale thoroughly

## 📊 **ACADEMIC REPORTING REQUIREMENTS**

### **Methods Section Template**

```text
Framework Analysis Configuration:
- Framework: [Framework Name] v[Version]
- Algorithm Configuration:
  - Dominance amplification: [enabled/disabled]
    - Threshold: [value] (scores above this value received amplification)
    - Multiplier: [value] (amplification factor applied)
    - Rationale: [rationale text]
  - Adaptive scaling: [enabled/disabled]
    - Base scaling: [value] (minimum coordinate scaling)
    - Maximum scaling: [value] (maximum coordinate scaling)  
    - Variance factor: [value] (sensitivity to score variance)
    - Mean factor: [value] (sensitivity to score means)
    - Methodology: [methodology text]
  - LLM Model: [Model name and version]
  - Analysis Date: [Date range]

Methodological Approach: Analysis employed the Discernus LLM-prompting-amplification 
pipeline, where LLM-identified dominance patterns receive mathematical enhancement 
for improved analytical clarity. [Additional methodological details as needed.]
```

### **Results Section Considerations**

1. **Coordinate Interpretation**: Report that visualized coordinates reflect enhanced values integrating LLM assessment and mathematical amplification
2. **Amplification Transparency**: Note which themes/elements received amplification enhancement
3. **Parameter Sensitivity**: Consider sensitivity analysis if multiple configurations were tested

## 🔄 **MIGRATION GUIDE**

### **From Framework Specification v2.x**

**Automatic Compatibility**: 
- Existing frameworks work unchanged with default algorithm configurations
- No manual migration required for basic functionality

**Optional Enhancement**:
- Add `algorithm_config` section for custom configurations
- Update prompting instructions to reference dominance identification
- Document algorithm choices for academic publications

### **From JSON Framework Format**

**Breaking Change**: JSON framework loading is deprecated in v3.0

**Migration Steps**:
1. Convert existing JSON frameworks to YAML format
2. Add required v3.0 sections (`algorithm_config`, updated `prompt_configuration`)
3. Test framework loading with coordinate engine v3.0
4. Update experiment definitions to reference YAML frameworks

**Automated Migration Tool**: `scripts/utilities/migrate_json_to_yaml_v3.py` (planned)

## ✅ **VALIDATION & TESTING**

### **Framework Validation Checklist**

- [ ] **YAML Syntax**: Valid YAML format with proper indentation
- [ ] **Required Sections**: All mandatory sections present
- [ ] **Algorithm Parameters**: All parameters within valid ranges
- [ ] **Anchor Definitions**: Complete anchor specifications with angles 0-359°
- [ ] **Color Mapping**: All anchor types have corresponding colors
- [ ] **Prompt Integration**: Complete prompting configuration
- [ ] **Academic Documentation**: Validation and compatibility sections complete

### **Algorithm Configuration Validation**

- [ ] **Parameter Ranges**: All numeric parameters within specified ranges
- [ ] **Logical Consistency**: `base_scaling` < `max_scaling`, `threshold` ≤ 1.0
- [ ] **Required Strings**: `rationale` and `methodology` fields completed
- [ ] **Integration Documentation**: Prompting integration properly specified

### **Backward Compatibility Testing**

- [ ] **Existing Experiments**: Run without modification using default configurations
- [ ] **API Consistency**: No breaking changes to public API methods
- [ ] **Visualization Compatibility**: Charts render correctly with enhanced algorithms

## 🚀 **IMPLEMENTATION STATUS**

### **Current Status** (June 23, 2025)
- [ ] **Specification**: DRAFT Complete ✅
- [ ] **Algorithm Loading**: In Development
- [ ] **Coordinate Engine**: In Development
- [ ] **Validation Tools**: Planned
- [ ] **Migration Tools**: Planned
- [ ] **Documentation**: In Progress

### **Deployment Timeline**
- **Week 1**: Framework specification and algorithm loading implementation
- **Week 2**: Coordinate engine enhancement and validation tools
- **Week 3**: Integration testing and documentation completion
- **Target Release**: July 14, 2025

---

**Document Version**: 3.0 DRAFT  
**Last Updated**: June 23, 2025  
**Next Review**: Post-Implementation Validation  
**Related Documents**:
- Configurable Algorithms Methodology v3.0
- Implementation Plan: Configurable Algorithms Enhancement
- Migration Guide: JSON to YAML v3.0 (planned)
- User Guide: Configuring Algorithms (planned) 