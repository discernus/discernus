# Discernus Coordinate System Framework Specification v3.2
**Version:** 3.2  
**Date:** June 27, 2025  
**Author:** Jeffrey Whatcott
**Status:** DEVELOPMENT - Advanced Multi-Dimensional Analysis  
**Breaking Changes:** Arc positioning, competitive dynamics, framework fit validation, Olympics protocols, polar constraint enforcement  

## 🎯 **OVERVIEW**

Framework Specification v3.2 introduces **advanced multi-dimensional analysis capabilities** including arc positioning with theoretical weighting modeling, competitive dynamics between theoretical concepts, comprehensive framework validation metrics, and systematic framework comparison protocols. This specification enables sophisticated computational discourse analysis while maintaining the flexible attribute-based architecture of v3.1.

## 🚀 **VERSION 3.2 ENHANCEMENTS**

### **Revolutionary Additions**
- ✅ **Arc Positioning Architecture**: Theoretical weighting modeling with clustered anchor positioning
- ✅ **Competitive Dynamics Engine**: Mathematical modeling of ideological competition and dilution effects  
- ✅ **Framework Fit Validation**: Comprehensive cartographic fidelity and territorial coverage metrics
- ✅ **Temporal Evolution Tracking**: Centroid displacement, velocity, and acceleration analysis
- ✅ **Olympics Validation Protocols**: Systematic framework comparison and optimization methodology
- ✅ **Theoretical Weighting Corrections**: Spatial bias compensation and cross-framework normalization
- ✅ **Cross-Framework Standards**: Rigorous comparison protocols for different analytical approaches
- ✅ **Hybrid Axes-Anchors Architecture**: Component registry with axes referencing anchors by ID and anchor_summary for rapid comprehension
- ✅ **Polar Constraint Enforcement**: Mathematical requirement that axes contain exactly 2 anchors for theoretical rigor and interpretability

### **Enhanced v3.1 Features**  
- ✅ **Semantic Agnostic Architecture**: No normative assumptions about anchor types or relationships
- ✅ **Advanced Algorithm Configuration**: Dominance amplification, adaptive scaling, competitive modeling
- ✅ **Flexible Positioning**: Mixed degrees/clock notation with arc distribution support
- ✅ **Academic Rigor**: Enhanced validation requirements and citation standards

### **Backward Compatibility**
- ✅ **v3.1 Framework Support**: All existing frameworks automatically compatible
- ✅ **Gradual Enhancement Path**: Optional v3.2 features can be added incrementally
- ✅ **Legacy Validation**: Existing frameworks pass validation without modification
- ✅ **Hybrid Architecture Compatibility**: Existing frameworks with inline or referenced anchors remain valid
- ✅ **Migration Path**: New frameworks SHOULD adopt the hybrid components + axes format for clarity and extensibility

## 📋 **ADVANCED FRAMEWORK ARCHITECTURE**

### **Core Philosophy: Multi-Dimensional Semantic Mapping**

v3.2 frameworks are **sophisticated analytical instruments** capable of capturing complex theoretical relationships, competitive dynamics, and temporal evolution patterns. Framework capabilities are determined by component presence and configuration sophistication:

### **Hybrid Axes-Anchors Architecture (v3.2 Recommended)**

**Framework Architecture Overview:**
- **Components**: All anchors must be registered as independent components with unique `component_id` values
- **Axes**: Reference anchors by their `anchor_ids` and include optional `anchor_summary` for rapid comprehension
- **Hybrid Clarity**: Combines structural rigor with human-readable summaries for optimal LLM and human consumption

**Axes-Anchors Relationship:**
- **Anchors** are independent semantic components, each with unique identifiers and comprehensive definitions
- **Axes** are bipolar relationships between exactly two anchor components, creating true oppositional dimensions
- **Polar Constraint** ensures mathematical rigor: each axis represents a single dimension with two endpoints
- **Anchor Summary** provides brief descriptions within axes for rapid understanding without dereferencing
- **Multi-Point Guidance** directs users to anchor-set frameworks when 3+ reference points are needed

```yaml
# Framework defines advanced capabilities through component sophistication
name: advanced_research_framework
version: v3.2

# POSITIONING COMPONENTS (enhanced with arc support)
anchors: {...}           # Independent semantic anchors
axes: {...}              # Opposing anchor pairs  
arcs: {...}              # Clustered positioning with theoretical weighting
positioning_strategy: {...} # Arc distribution and weighting configuration

# COMPETITIVE DYNAMICS (new in v3.2)
competitive_relationships: {...} # Ideological competition modeling
temporal_analysis: {...}        # Evolution tracking configuration
olympics_protocols: {...}       # Systematic comparison standards

# ALGORITHMIC ENHANCEMENT (expanded from v3.1)
algorithm_config: {...}         # Advanced mathematical processing
weighting_corrections: {...}      # Spatial bias compensation
```

## 📖 **FRAMEWORK CONSUMPTION GUIDE**

### **How to Process Hybrid Architecture Frameworks**

**For LLM and API Consumers:**

**1. Processing Order (Critical)**
```
Step 1: Parse component registry for anchor definitions
Step 2: Parse axes for anchor_ids and relationships  
Step 3: Use anchor_summary for rapid context (optional)
Step 4: Resolve anchor_ids to full component definitions for computation
```

**2. Data Authority Hierarchy**
- **Primary Source**: Component registry anchor definitions (complete data)
- **Reference Mechanism**: Axis anchor_ids (structural relationships)  
- **Convenience Layer**: anchor_summary (human-readable context only)
- **Rule**: If discrepancy exists, trust component registry over anchor_summary

**3. Validation Priorities**
```
✅ Required: Verify all anchor_ids in axes exist in component registry
✅ Required: Confirm each axis contains exactly 2 anchor_ids (polar constraint)
⚠️ Recommended: Validate anchor_summary matches component registry when present
❌ Never: Use anchor_summary for mathematical calculations
```

**For Framework Developers:**

**1. Design Decision Tree**
- **2 Reference Points** → Use axis-set framework (bipolar relationships)
- **3+ Reference Points** → Use anchor-set framework (independent positioning)
- **Non-oppositional concepts** → Use anchor-set framework

**2. Implementation Checklist**
- [ ] Register all anchors in component registry with unique IDs
- [ ] Reference exactly 2 anchors per axis using anchor_ids
- [ ] Include anchor_summary for clarity (recommended)
- [ ] Validate true oppositional relationship between axis poles
- [ ] Test framework with validator before deployment

**For System Implementers:**

**1. Parsing Requirements**
```python
# Required validation during framework loading:
assert len(axis.anchor_ids) == 2, "Polar constraint violation"
assert all(id in components for id in axis.anchor_ids), "Missing component"
assert axis.pole_a != axis.pole_b, "Identical poles invalid"
```

**2. Processing Workflow**
```
Framework Load → Component Registry Validation → Axis Validation → 
Anchor Resolution → Mathematical Processing
```

## 📦 **FRAMEWORK EMBEDDING BEST PRACTICES**

### **Experiment System Integration Considerations**

When frameworks are embedded in experiment definitions (see **[Experiment System Specification v3.2](Discernus_Experiment_System_Specification_v3.2.0.md)**), proper prompt element placement becomes critical for optimal LLM processing and cognitive context establishment.

### **Core Principle: Sequential LLM Processing Optimization**

**LLM Processing Challenge**: When frameworks are embedded in experiments, LLMs process content sequentially, requiring strategic placement of prompt elements to establish proper cognitive context before framework interpretation.

**Solution: Early Context Setting + Late Detailed References**

### **Recommended Prompt Placement Architecture**

```yaml
# OPTIMAL: Early Context Setting (immediately after framework metadata)
name: framework_name
version: v3.2
display_name: "Framework Display Name"
description: |
  [Comprehensive framework description]

# EARLY: Essential cognitive priming elements
expert_role: |
  You are an expert analyst with specialized knowledge relevant to this framework's
  theoretical domain. This establishes analytical perspective before encountering
  framework components and guides interpretation of language cues and concepts.

methodological_approach: |
  High-level analytical methodology that affects how framework components should
  be interpreted. Places LLM in appropriate analytical mode before processing
  detailed framework structure.

# MIDDLE: Framework structure definitions
components:
  [Complete framework component definitions]

axes:
  [Axis definitions with anchor references]

competitive_relationships:
  [Competition modeling configurations]

# LATE: Detailed prompts referencing framework elements
detailed_prompts:
  specific_analysis_guidance: |
    Detailed instructions that reference specific components, language_cues,
    competitive_relationships, and other framework elements defined above.
    These can safely use forward references because the elements exist.
  
  scoring_methodology: |
    Precise scoring instructions that reference specific anchor definitions,
    competition_pairs, and metrics defined in the framework structure.
```

### **Cognitive Processing Benefits**

**Early Context Setting Advantages:**
- **Cognitive Priming**: LLM knows analytical perspective before encountering technical elements
- **Domain Contextualization**: Proper theoretical context for interpreting language cues
- **Methodological Frame**: Analysis approach guides framework component interpretation
- **No Forward References**: Early elements don't reference undefined framework components

**Late Detailed Prompts Advantages:**
- **Technical Precision**: Can reference specific framework elements with confidence
- **Forward Reference Resolution**: All referenced elements have been defined
- **Implementation Details**: Specific guidance for applying framework components
- **Embedded Context Clarity**: Works seamlessly when framework is embedded in experiments

### **Implementation Guidelines**

**For Framework Developers:**

**Required Sequence:**
1. **Framework Metadata** (name, version, description)
2. **Early Context Setting** (expert_role, methodological_approach)
3. **Framework Structure** (components, axes, competitive_relationships)
4. **Late Detailed Prompts** (detailed analysis guidance referencing framework elements)

**Early Context Elements:**
```yaml
expert_role: |
  Establish domain expertise and analytical perspective without referencing
  specific framework components. Focus on theoretical domain and approach.

methodological_approach: |
  High-level methodology that guides framework interpretation. Should work
  for any framework in this theoretical family.
```

**Late Detailed Elements:**
```yaml
detailed_prompts:
  component_application: |
    Specific guidance for applying framework components, referencing actual
    language_cues, competition_pairs, and metrics defined above.
  
  scoring_precision: |
    Detailed scoring instructions that reference specific framework elements
    and use precise technical terminology from component definitions.
```

**For Experiment System Integration:**

When frameworks are embedded in experiments, this architecture ensures:
- **Proper Context Layering**: Experiment → Framework → Analysis guidance
- **Sequential Processing**: Each layer builds on previous context
- **Reference Resolution**: No broken forward references
- **Cognitive Clarity**: LLM understanding improves with each processing layer

### **Theoretical Foundation**

**LLM Sequential Processing Research**: Studies of LLM attention mechanisms demonstrate that early context significantly affects interpretation of later content. Cognitive priming through early expert role and methodological guidance improves accuracy of framework component interpretation.

**Framework Embedding Context**: Unlike standalone frameworks, embedded frameworks must account for experiment-level context and sequential processing constraints. The dual-phase prompt architecture addresses these constraints while maintaining framework precision.

**Cross-Reference**: For complete implementation details and experiment-specific considerations, see **[Experiment System Specification v3.2 - Framework Embedding Optimization](Discernus_Experiment_System_Specification_v3.2.0.md#framework-embedding-optimization)**.

## 🏗️ **HYBRID AXES-ANCHORS ARCHITECTURE SPECIFICATION**

### **Hybrid Architecture Overview**

The v3.2 specification introduces a **recommended hybrid approach** that clarifies the relationship between axes and anchors while maintaining backward compatibility. This architecture provides structural rigor with human-readable clarity.

### **Core Principles**

**1. Anchors as Independent Components**
- All anchors must be registered as independent components in a top-level `components` section
- Each anchor has a unique `component_id` for reference and computational processing
- Full anchor definitions include positioning, weights, language cues, and theoretical grounding

**2. Axes Reference Exactly Two Anchors by ID (Polar Constraint)**
- Axes define bipolar relationships between exactly two anchor components by referencing their `component_id` values
- Axes specify `anchor_ids` array containing exactly 2 anchor IDs (mathematical requirement for true axes)
- Axes may include additional relationship properties (theoretical basis, validation method, pole assignments)
- **Critical Constraint**: Axes MUST contain exactly 2 anchors to maintain mathematical rigor and interpretability

**3. Anchor Summary for Rapid Comprehension**
- **Recommended**: Axes include an `anchor_summary` block mapping anchor IDs to brief descriptions
- Enables rapid understanding without dereferencing full component definitions
- Optimizes both human comprehension and LLM processing efficiency

### **Complete Hybrid Framework Example**

```yaml
# ================================================================
# FRAMEWORK IDENTIFICATION
# ================================================================
name: political_orientation_framework
version: v3.2
display_name: "Political Orientation Analysis Framework"
description: |
  Analyzes political discourse along democratic theory dimensions using
  hybrid axes-anchors architecture with polar constraint enforcement.

# ================================================================
# COMPONENT REGISTRY (All anchors defined once)
# ================================================================
components:
  pluralism:
    component_id: pluralism
    type: anchor
    description: "Democratic theory emphasizing institutional mediation, minority rights, and constitutional constraints on majority power"
    angle: 0
    weight: 1.0
    language_cues:
      - "institutional checks and balances"
      - "minority rights protection"
      - "constitutional democracy"
  
  populism:
    component_id: populism
    type: anchor
    description: "Democratic theory emphasizing direct popular will, anti-elite sentiment, and majoritarianism"
    angle: 180
    weight: 1.0
    language_cues:
      - "will of the people"
      - "anti-establishment"
      - "elite corruption"

  liberalism:
    component_id: liberalism
    type: anchor
    description: "Political theory emphasizing individual freedoms, civil liberties, and limited government"
    angle: 90
    weight: 1.0
    language_cues:
      - "individual liberty"
      - "civil rights"
      - "limited government"

  authoritarianism:
    component_id: authoritarianism
    type: anchor
    description: "Political theory emphasizing strong central authority and limited individual freedoms"
    angle: 270
    weight: 1.0
    language_cues:
      - "strong leadership"
      - "social order"
      - "state authority"

# ================================================================
# AXES (Reference exactly 2 anchors each - polar constraint)
# ================================================================
axes:
  Democracy:
    component_id: democracy_axis
    anchor_ids: [pluralism, populism]  # Exactly 2 anchors
    description: "Bipolar dimension from pluralist to populist democratic approaches"
    
    # Optional but recommended: Brief descriptions for rapid understanding
    anchor_summary:
      pluralism: "Institutional mediation and minority rights"
      populism: "Direct popular will and anti-elite sentiment"
    
    axis_type: bipolar
    theoretical_basis: "Democratic theory (Dahl, Mudde, Müller)"
    pole_a: pluralism     # First pole
    pole_b: populism      # Opposing pole

  Authority:
    component_id: authority_axis
    anchor_ids: [liberalism, authoritarianism]  # Exactly 2 anchors
    description: "Bipolar dimension from liberal to authoritarian governance approaches"
    
    anchor_summary:
      liberalism: "Individual freedoms and limited government"
      authoritarianism: "Strong central authority and state control"
    
    axis_type: bipolar
    theoretical_basis: "Political authority theory (Berlin, Hayek, Schmitt)"
    pole_a: liberalism
    pole_b: authoritarianism

# ================================================================
# FRAMEWORK METADATA
# ================================================================
validation:
  polar_constraint_satisfied: true
  component_registry_complete: true
  academic_standard: "Political Science Framework v3.2"

framework_registry_key: "political_orientation__v3.2"
```

### **Quick Reference: Minimal Valid Framework**

```yaml
# Minimal hybrid framework example
name: simple_demo
version: v3.2

# Component registry (required)
components:
  concept_a:
    component_id: concept_a
    angle: 0
    weight: 1.0
    description: "First theoretical concept"
  concept_b:
    component_id: concept_b
    angle: 180
    weight: 1.0
    description: "Opposing theoretical concept"

# Axes (exactly 2 anchors each)
axes:
  MainDimension:
    anchor_ids: [concept_a, concept_b]
    description: "Primary theoretical dimension"
    anchor_summary:
      concept_a: "First pole"
      concept_b: "Second pole"
```

### **Implementation Guidelines**

**For Framework Developers:**
- **Required**: Register all anchors as independent components with unique IDs
- **Required**: Reference exactly 2 anchors in each axis using `anchor_ids` array (polar constraint)
- **Required**: Ensure true oppositional relationship between axis poles for mathematical validity
- **Recommended**: Include `anchor_summary` in axes for clarity and usability
- **Optional**: Migrate existing frameworks gradually (legacy format remains valid)
- **Important**: If you need 3+ reference points, use anchor-set framework instead of multi-anchor axes

**When to Use Anchor-Set Instead of Axes:**
- **Multiple reference points**: "Left-Center-Right" → Use 3 independent anchors, not 1 axis
- **Non-oppositional concepts**: Concepts that don't form true polar opposites
- **Categorical dimensions**: Nominal categories rather than continuous spectra
- **Complex theoretical space**: Multiple theoretical positions without clear binary opposition

**For LLM and API Consumers:**
- **Primary**: Use `anchor_summary` within axes for rapid context and processing
- **Secondary**: Reference full component definitions for detailed analysis and computation
- **Validation**: Ensure anchor IDs in axes match component IDs in components section

**For System Implementers:**
- **Validation**: Verify anchor ID consistency between components and axes sections
- **Processing**: Support both hybrid and legacy formats seamlessly
- **Migration**: Provide tools for converting legacy formats to hybrid approach

### **Theoretical Justification: Polar Constraint**

**Mathematical Rigor**: Traditional coordinate systems, factor analysis, and psychometric frameworks define axes as having exactly two endpoints. This constraint ensures:
- **Clear interpretation**: Each axis represents a single dimensional continuum
- **Mathematical soundness**: Distance calculations and interpolation are unambiguous  
- **Cognitive clarity**: LLMs and researchers expect axes to mean "between two extremes"
- **Statistical validity**: Avoids ill-defined multi-point scales that reduce analytical precision

**Framework Selection Guidance**:
- **2 Reference Points**: Use axis-set framework (e.g., "Populism vs Pluralism")
- **3+ Reference Points**: Use anchor-set framework (e.g., "Left, Center, Right" as independent anchors)
- **Non-oppositional Concepts**: Use anchor-set framework for concepts without true polarity

### **Edge Cases and Common Questions**

**Q: What if I need 3 or more reference points along a dimension?**
A: Use an **anchor-set framework** instead of axes. Example:
```yaml
# CORRECT for 3+ points:
anchors:
  left: { angle: 45, description: "Progressive position" }
  center: { angle: 135, description: "Moderate position" }  
  right: { angle: 225, description: "Conservative position" }

# WRONG - violates polar constraint:
# axes:
#   PoliticalSpectrum:
#     anchor_ids: [left, center, right]  # Invalid!
```

**Q: Can I reuse anchors across multiple axes?**
A: Yes! This is encouraged for frameworks analyzing overlapping theoretical dimensions:
```yaml
components:
  freedom: { component_id: freedom, angle: 0 }
  security: { component_id: security, angle: 180 }
  equality: { component_id: equality, angle: 90 }
  hierarchy: { component_id: hierarchy, angle: 270 }

axes:
  Liberty: { anchor_ids: [freedom, security] }
  SocialOrder: { anchor_ids: [equality, hierarchy] }
  # freedom and security can be reused in other axes
```

**Q: What if my concepts aren't truly oppositional?**
A: Use **anchor-set framework**. True axes require genuine opposition:
```yaml
# GOOD for axes (true opposites):
# Democracy axis: [pluralism, populism]
# Authority axis: [liberalism, authoritarianism]

# BETTER as anchor-set (not truly oppositional):
anchors:
  economic_focus: { angle: 0 }
  cultural_focus: { angle: 120 }
  environmental_focus: { angle: 240 }
```

**Q: How do I handle overlapping or similar concepts?**
A: Ensure sufficient semantic separation (minimum 45° recommended):
```yaml
# GOOD - clear separation:
components:
  nationalism: { angle: 0 }
  cosmopolitanism: { angle: 180 }  # Clear opposition

# PROBLEMATIC - too similar:
# nationalism: { angle: 0 }
# patriotism: { angle: 15 }  # Too similar, poor separation
```

**Q: Can axes share anchor summaries with different descriptions?**
A: anchor_summary should be consistent across axes referencing the same anchor:
```yaml
# GOOD - consistent summaries:
axes:
  Dimension1:
    anchor_ids: [freedom, security]
    anchor_summary:
      freedom: "Individual liberty and autonomy"  # Consistent
  Dimension2:
    anchor_ids: [freedom, equality]
    anchor_summary:
      freedom: "Individual liberty and autonomy"  # Same description
```

### **Backward Compatibility Guarantee**

The hybrid approach is **fully backward compatible**:
- Existing frameworks with inline anchor definitions remain valid
- Legacy axis formats continue to function without modification  
- New frameworks SHOULD adopt hybrid format for enhanced clarity and extensibility
- Mixed approaches (some hybrid, some legacy) are supported during transition
- **Breaking Change**: New frameworks must satisfy polar constraint (2 anchors per axis)

## 🔧 **COMPLETE FRAMEWORK SCHEMA v3.2**

```yaml
# =============================================================================
# FRAMEWORK IDENTIFICATION (required)
# =============================================================================
name: unique_framework_name        # Must be unique across all frameworks
version: v3.2                      # Flexible dot notation  
display_name: "Framework Display Name"
description: |
  Self-documenting framework description with comprehensive theoretical foundation.
  
  ## Theoretical Foundation
  Complete academic grounding including primary sources and methodological approach.
  
  ## v3.2 Capabilities
  - Arc positioning with theoretical weighting modeling
  - Competitive dynamics between theoretical concepts  
  - Framework fit validation with mathematical metrics
  - Temporal evolution tracking and analysis
  - Cross-framework comparison protocols
  
  ## Usage Guidelines  
  Detailed instructions for appropriate application contexts and interpretation methods.
  
  ## Version History
  v3.2: Advanced multi-dimensional analysis with arc positioning and competitive dynamics
  v3.1: Attribute-based architecture with flexible positioning
  v3.0: Enhanced algorithmic configuration
  
  ## Citation Format
  Discernus Framework: Framework Name v3.2 (Jeffrey Whatcott, 2025)

# =============================================================================
# POSITIONING DEFINITION (at least one required)
# =============================================================================

# =============================================================================
# COMPONENTS DEFINITION (Hybrid Axes-Anchors Architecture)
# =============================================================================

# Top-level component registry for anchor definitions
components:
  ComponentAnchor1:
    component_id: unique_anchor_identifier
    type: anchor
    description: "Complete semantic anchor description with theoretical grounding"
    angle: 0                      # Degree position (0-359) OR
    position: "12 o'clock"        # Clock position alternative
    weight: 1.0                   # Relative importance (0.1-2.0)
    semantic_category: category_name  # Optional organizational attribute
    tier: primary                 # Optional: primary/secondary/tertiary
    language_cues:                # Enhanced language detection
      - "primary indicator phrase"
      - "secondary indicator phrase"
      - "contextual usage pattern"
    
    # v3.2 Enhancement: Competitive Relationships
    competes_with: ["other_anchor_id"]  # Optional competition modeling
    competition_strength: 0.7     # Competition coefficient (0.0-1.0)
    
    # v3.2 Enhancement: Temporal Sensitivity  
    temporal_stability: high      # high/medium/low expected stability
    evolution_pattern: gradual    # gradual/sudden/cyclical expected change

# =============================================================================
# POSITIONING OPTIONS
# =============================================================================

# Option 1: Independent Anchors (Enhanced v3.2)
anchors:
  AnchorName:
    description: "Complete semantic anchor description with theoretical grounding"
    angle: 0                      # Degree position (0-359) OR
    position: "12 o'clock"        # Clock position alternative
    weight: 1.0                   # Relative importance (0.1-2.0)
    type: semantic_category       # Optional organizational attribute
    tier: primary                 # Optional: primary/secondary/tertiary
    language_cues:                # Enhanced language detection
      - "primary indicator phrase"
      - "secondary indicator phrase"
      - "contextual usage pattern"
    
    # v3.2 Enhancement: Competitive Relationships
    competes_with: ["OtherAnchor1", "OtherAnchor2"]  # Optional competition modeling
    competition_strength: 0.7     # Competition coefficient (0.0-1.0)
    
    # v3.2 Enhancement: Temporal Sensitivity  
    temporal_stability: high      # high/medium/low expected stability
    evolution_pattern: gradual    # gradual/sudden/cyclical expected change

# Option 2: Axes Referencing Component Anchors (Enhanced v3.2 Hybrid Architecture)
# Axes are defined as bipolar relationships between EXACTLY TWO anchor components.
# Anchors must be registered as independent components, each with a unique component_id.
# Axes reference anchors by their anchor_ids and may include an anchor_summary block.
# CONSTRAINT: axes MUST contain exactly 2 anchor_ids (polar axis requirement).

axes:
  Democracy:
    component_id: democracy_axis
    anchor_ids: [pluralism, populism]  # EXACTLY 2 anchors required
    description: "Theoretical dimension with true oppositional relationship between two poles"
    
    # Recommended: anchor_summary mapping anchor IDs to brief descriptions
    anchor_summary:
      pluralism: "Emphasizes institutional mediation, minority rights, and constitutional democracy"
      populism: "Emphasizes direct popular will, anti-elite sentiment, and majoritarianism"
    
    # v3.2 Enhancement: Axis Properties
    axis_type: bipolar            # All axes are bipolar by definition
    theoretical_basis: "Source theoretical framework or literature"
    validation_method: "How opposition relationship was established"
    
    # Polar axis validation
    pole_a: pluralism            # First pole anchor ID
    pole_b: populism             # Second pole anchor ID (opposite)

# Legacy Format (Still Supported - Backward Compatible):
# AxisName:
#   description: "Theoretical dimension with true oppositional relationship"
#   anchor_a:
#     name: "ConceptA"
#     description: "First pole of opposition with complete definition"
#     angle: 0                    # OR position: "12 o'clock"
#     weight: 1.0
#     type: semantic_category
#     opposite_of: "ConceptB"     # Required linkage
#     language_cues: [...]
#   anchor_b:
#     name: "ConceptB" 
#     description: "Opposing pole with complete definition"
#     angle: 180                  # OR position: "6 o'clock"  
#     weight: 1.0
#     type: semantic_category
#     opposite_of: "ConceptA"     # Required linkage
#     language_cues: [...]

# Option 3: Arc Positioning (New in v3.2)
positioning_strategy:
  type: arc_clustering            # arc_clustering/domain_clustering/theoretical_grouping
  description: "High-level positioning methodology and theoretical justification"
  
  # v3.2 Core Feature: Arc Definitions
  arcs:
    arc_name:
      description: "Theoretical purpose and semantic coherence of anchor grouping"
      center_angle: 90            # Arc center position (degrees)
      span: 60                    # Angular span in degrees
      distribution_method: even   # even/weighted/custom/theoretical
      
      # Arc-specific anchors
      anchors:
        ArcAnchor1:
          description: "Anchor within arc cluster"
          relative_position: 0.2  # Position within arc (0.0-1.0)
          weight: 1.0
          type: cluster_semantic_type
          language_cues: [...]
          
      # v3.2 Enhancement: Theoretical Weighting Modeling
      weighting_profile: gaussian   # gaussian/uniform/custom
      weighting_strength: 1.5       # Relative weighting compared to baseline
      bandwidth: 15               # Weighting calculation bandwidth (degrees)
      
      # v3.2 Enhancement: Cluster Competition
      competes_with_arcs: ["other_arc_name"]
      inter_arc_competition: 0.4  # Competition strength between arcs

# =============================================================================
# COMPETITIVE DYNAMICS CONFIGURATION (new in v3.2)
# =============================================================================

competitive_relationships:
  enabled: true
  competition_model: semantic_space_allocation  # Options: semantic_space_allocation, 
                                               #          ideological_dilution,
                                               #          discourse_crowding
  
  # Global competition parameters
  global_competition_strength: 0.3    # Base competition effect (0.0-1.0)
  competition_decay_distance: 45      # Angular distance for competition falloff (degrees)
  
  # Specific competition definitions
  competition_pairs:
    - anchors: ["Nationalism", "Cosmopolitanism"] 
      strength: 0.8
      type: ideological_opposition
      mechanism: "dilution"  # dilution/crowding/replacement
      
    - anchors: ["Populism", "Pluralism"]
      strength: 0.6  
      type: democratic_theory_competition
      mechanism: "crowding"
      
  # Advanced competition modeling
  semantic_space_allocation:
    total_space: 1.0                  # Normalized discourse space
    allocation_method: proportional   # proportional/competitive/hierarchical
    crowding_threshold: 0.7           # When crowding effects activate
    
  # Temporal competition effects  
  competition_evolution:
    enabled: true
    learning_rate: 0.1               # How quickly competition adapts
    temporal_decay: 0.05             # Competition strength decay over time

# =============================================================================
# FRAMEWORK FIT VALIDATION (new in v3.2)
# =============================================================================

framework_fit_metrics:
  # Core validation requirements
  territorial_coverage:
    enabled: true
    minimum_threshold: 0.85          # Minimum acceptable coverage
    pca_components: 3                # Components for 95% variance
    theoretical_weighting: true          # Account for theoretical weighting
    
  anchor_independence:
    enabled: true
    minimum_threshold: 0.70          # Minimum independence score
    correlation_method: pearson      # pearson/spearman/cosine
    max_correlation: 0.7             # Maximum allowed correlation
    
  cartographic_resolution: 
    enabled: true
    minimum_silhouette: 0.60         # Minimum silhouette score
    cluster_method: kmeans           # kmeans/hierarchical/custom
    weighting_correction: true         # Apply weighting corrections
    
  navigational_accuracy:
    enabled: true
    external_criteria: []            # List of validation criteria
    minimum_correlation: 0.65        # Minimum predictive accuracy
    cross_validation: temporal       # temporal/k_fold/bootstrap
    
  # Advanced validation metrics
  survey_completeness:
    functional_mece: true            # Mutually exclusive, collectively exhaustive
    theoretical_coverage: 0.90       # Minimum theoretical space coverage
    redundancy_threshold: 0.3        # Maximum acceptable redundancy
    
  weighting_bias_detection:
    systematic_bias_threshold: 0.15  # Maximum acceptable systematic bias
    arc_bias_compensation: true      # Compensate for arc positioning effects
    uniformity_requirement: 0.75     # Minimum weighting uniformity score

# =============================================================================
# TEMPORAL ANALYSIS CONFIGURATION (new in v3.2)
# =============================================================================

temporal_analysis:
  enabled: true
  
  # Centroid tracking
  centroid_evolution:
    track_displacement: true         # Monitor centroid movement
    track_velocity: true             # Calculate movement speed
    track_acceleration: true         # Detect acceleration/deceleration
    smoothing_window: 3              # Temporal smoothing window size
    
  # Evolution pattern detection
  pattern_detection:
    drift_threshold: 0.1             # Minimum drift for significance
    velocity_threshold: 0.05         # Minimum velocity for significance  
    acceleration_threshold: 0.02     # Minimum acceleration for significance
    
    # Pattern classification
    classify_patterns: true          # Enable automatic pattern classification
    pattern_types:                   # Types of patterns to detect
      - linear_drift
      - cyclical_movement
      - sudden_shift
      - gradual_evolution
      - oscillation
      
  # Temporal validation
  temporal_coherence:
    measure_coherence: true          # Calculate temporal coherence score
    stability_window: 5              # Window for stability measurement
    prediction_horizon: 2            # Periods ahead for prediction testing
    
  # Weighting-corrected temporal analysis
  weighting_corrections:
    apply_corrections: true          # Apply weighting corrections to temporal analysis
    path_weighting: true     # Weight by theoretical weighting along path
    arc_bias_compensation: true      # Compensate for arc positioning effects

# =============================================================================
# OLYMPICS VALIDATION PROTOCOLS (new in v3.2)
# =============================================================================

olympics_protocols:
  enabled: true
  
  # Framework comparison standards
  comparison_metrics:
    - territorial_coverage
    - cartographic_resolution  
    - navigational_accuracy
    - temporal_coherence
    - theoretical_alignment
    - computational_efficiency
    
  # Scoring methodology
  scoring_weights:
    territorial_coverage: 0.25       # Explanation of variance
    cartographic_resolution: 0.25    # Clustering quality
    navigational_accuracy: 0.20      # Predictive validity
    temporal_coherence: 0.15         # Stability over time
    theoretical_alignment: 0.10      # Match to established theory
    computational_efficiency: 0.05   # Processing requirements
    
  # Validation protocols
  validation_requirements:
    baseline_corpus: required        # Must test against standard corpus
    cross_validation: k_fold         # Required validation method
    significance_testing: permutation # Statistical significance method
    effect_size_minimum: 0.3         # Minimum meaningful effect size
    
  # Olympic categories
  framework_categories:
    - single_axis_frameworks
    - multi_axis_frameworks  
    - anchor_set_frameworks
    - clustered_frameworks
    - hybrid_architectures
    
  # Medal criteria
  medal_thresholds:
    gold: 0.90                       # Composite score for gold medal
    silver: 0.80                     # Composite score for silver medal  
    bronze: 0.70                     # Composite score for bronze medal

# =============================================================================
# ALGORITHMIC CONFIGURATION (enhanced from v3.1)
# =============================================================================

algorithm_config:
  # Enhanced dominance amplification
  dominance_amplification:
    enabled: true
    threshold: 0.7                   # Threshold for amplification
    multiplier: 1.1                  # Amplification factor
    competition_aware: true          # Account for competitive effects
    rationale: "Enhance dominant theoretical orientations while preserving competitive dynamics"
    
  # Enhanced adaptive scaling  
  adaptive_scaling:
    enabled: true
    base_scaling: 0.65               # Minimum scaling factor
    max_scaling: 0.95                # Maximum scaling factor
    variance_factor: 0.3             # Variance sensitivity
    mean_factor: 0.1                 # Mean sensitivity
    weighting_adjustment: true         # Adjust for theoretical weighting
    methodology: "Weighting-aware adaptive scaling for optimal discrimination"
    
  # v3.2 Enhancement: Competitive Algorithm Integration
  competitive_processing:
    enabled: true
    competition_order: parallel      # parallel/sequential/hierarchical
    dilution_calculation: multiplicative  # multiplicative/additive/threshold
    crowding_effects: gaussian       # gaussian/linear/exponential
    
  # v3.2 Enhancement: Weighting Correction Integration
  weighting_corrections:
    enabled: true
    correction_strength: 0.8         # How strongly to apply corrections (0.0-1.0)
    bias_compensation: true          # Compensate for systematic biases
    cross_framework_normalization: true  # Enable cross-framework comparison
    
  # Enhanced prompting integration
  prompting_integration:
    dominance_instruction: "Advanced instructions for hierarchical pattern detection"
    competition_instruction: "Instructions for detecting competitive theoretical relationships"
    temporal_instruction: "Instructions for identifying evolution patterns"
    amplification_purpose: "Mathematical enhancement maintaining theoretical validity"
    methodology_reference: "Advanced Multi-Dimensional Analysis Methodology v3.2"

# =============================================================================
# COORDINATE SYSTEM (enhanced)
# =============================================================================

coordinate_system:
  type: circle                       # Enhanced circular coordinate system
  radius: 1.0                        # Standard unit circle
  weighting_modeling: true             # Enable theoretical weighting modeling
  weighting_resolution: 360            # Angular resolution for weighting calculation (points)
  description: "Advanced DCS with theoretical weighting modeling and competitive dynamics"
  
  # v3.2 Enhancement: Weighting Configuration
  weighting_configuration:
    baseline_weighting: 1.0            # Baseline theoretical weighting
    max_weighting_ratio: 5.0           # Maximum weighting relative to baseline
    weighting_smoothing: gaussian      # gaussian/linear/none
    smoothing_bandwidth: 15          # Smoothing bandwidth (degrees)

# =============================================================================
# ANALYSIS CONFIGURATION (enhanced)
# =============================================================================

metrics:
  # Core metrics (enhanced)
  territorial_coverage:
    name: "Territorial Coverage Score"  
    description: "PCA-based measure of theoretical space explanation with weighting"
    calculation: "Weighting-adjusted explained variance ratio for 95% coverage"
    target_range: [0.85, 1.0]
    
  anchor_independence:
    name: "Anchor Independence Index"
    description: "Measure of semantic separation between anchors"
    calculation: "1 - max(|correlation_matrix_off_diagonal|)"
    target_range: [0.70, 1.0]
    
  cartographic_resolution:
    name: "Cartographic Resolution Score"
    description: "Silhouette-based clustering quality with weighting corrections"
    calculation: "Weighting-corrected silhouette coefficient"
    target_range: [0.60, 1.0]
    
  # v3.2 New Metrics
  competitive_dynamics_score:
    name: "Competitive Dynamics Quality"
    description: "Measure of how well competitive relationships are modeled"
    calculation: "Correlation between predicted and observed competition effects"
    target_range: [0.65, 1.0]
    
  temporal_coherence:
    name: "Temporal Evolution Coherence"
    description: "Consistency and predictability of centroid movement patterns"
    calculation: "Inverse of temporal variance with trend detrending"
    target_range: [0.70, 1.0]
    
  framework_fitness:
    name: "Overall Framework Fitness Score"
    description: "Composite measure of all validation criteria"
    calculation: "Weighted average of all component scores"
    target_range: [0.75, 1.0]
    
  # Advanced validation metrics
  weighting_bias_index:
    name: "Systematic Weighting Bias Index"
    description: "Measure of systematic positioning bias from arc configuration"
    calculation: "Magnitude of systematic centroid deviation from expected"
    target_range: [0.0, 0.15]
    
  cross_framework_portability:
    name: "Cross-Framework Comparison Validity"
    description: "Ability to meaningfully compare with other frameworks"
    calculation: "Correlation stability under weighting normalization"
    target_range: [0.80, 1.0]

# =============================================================================
# LLM INTEGRATION (enhanced)
# =============================================================================

prompt_configuration:
  expert_role: |
    You are an expert analyst of theoretical discourse with deep knowledge of 
    multi-dimensional conceptual relationships, competitive dynamics between ideas,
    and temporal evolution patterns in complex discourse systems.
  
  bias_neutral_analysis_focus: |
    Evaluate theoretical positioning across multiple dimensions simultaneously,
    detecting competitive relationships between concepts, theoretical weighting variations,
    and temporal evolution patterns without imposing normative judgments on 
    theoretical orientations.
  
  detection_approach: |
    Analyze discourse for multi-layered theoretical positioning, competitive 
    dynamics between concepts, clustered semantic relationships, and evolutionary
    patterns. Consider both explicit theoretical statements and implicit assumptions
    about conceptual relationships and temporal development.
  
  scoring_methodology: |
    Provide precise 0.0-1.0 scores with detailed textual evidence. Account for
    competitive relationships between concepts, theoretical weighting effects, and
    temporal positioning. Consider theoretical clustering and hierarchical
    importance when assigning scores across multiple dimensions.
    
  # v3.2 Enhanced Instructions
  competitive_dynamics_detection: |
    Identify instances where multiple theoretical concepts compete for discursive
    space, creating dilution effects or semantic crowding. Look for evidence of
    ideological tension, conceptual trade-offs, and competitive relationships
    between theoretical frameworks within the same discourse.
    
  temporal_pattern_recognition: |
    Detect evolution patterns, consistency changes, and directional shifts in
    theoretical positioning. Identify gradual drift, sudden changes, cyclical
    patterns, and acceleration/deceleration in conceptual emphasis over time.
    
  weighting_awareness_instructions: |
    Consider semantic clustering effects and weighting variations when interpreting
    theoretical positioning. Account for anchor concentration effects and 
    systematic biases introduced by clustered positioning strategies.
    
  # v3.2 Enhancement: Hybrid Axes-Anchors LLM Guidance
  hybrid_architecture_consumption: |
    Consumers SHOULD use the `anchor_summary` block within each axis (when provided) 
    to facilitate rapid understanding of the anchor positions without dereferencing 
    IDs in the components section. For full analytic or computational purposes, 
    anchors MUST be defined and referenced by their unique `component_id`.
    
    When processing axes with `anchor_ids`, prioritize the `anchor_summary` for 
    immediate context while maintaining awareness that complete anchor definitions 
    exist in the components section for detailed analysis.

# =============================================================================
# VISUALIZATION CONFIGURATION (enhanced)
# =============================================================================

visualization:
  coordinate_system: "DCS_v3.2"      # Enhanced coordinate system
  
  # Enhanced visualization types
  supported_charts:
    - circular                       # Standard circular plot
    - weighting_heatmap               # Theoretical weighting visualization  
    - temporal_evolution            # Centroid movement over time
    - competitive_dynamics          # Competition relationship network
    - framework_comparison          # Multi-framework overlay
    - arc_clustering               # Arc-based cluster visualization
    - olympics_scoreboard          # Framework performance comparison
    
  # v3.2 Enhancement: Advanced Styling
  semantic_type_colors:
    primary_anchor: "#1565C0"        # Blue for primary theoretical concepts
    secondary_anchor: "#F57C00"      # Orange for secondary concepts  
    tertiary_anchor: "#9E9E9E"       # Gray for supporting concepts
    competitive_relationship: "#D32F2F"  # Red for competitive links
    temporal_evolution: "#388E3C"    # Green for evolution paths
    
  # Arc visualization configuration
  arc_visualization:
    show_weighting_gradients: true     # Display theoretical weighting gradients
    weighting_opacity_range: [0.3, 0.9]  # Opacity range for weighting visualization
    arc_boundary_style: "dashed"     # Arc boundary visualization style
    cluster_highlight: true          # Highlight anchor clusters
    
  # Temporal visualization
  temporal_visualization:
    trajectory_style: "arrow"        # arrow/line/points for centroid paths
    velocity_scaling: true           # Scale trajectory thickness by velocity
    acceleration_highlighting: true  # Highlight acceleration/deceleration
    pattern_annotation: true         # Annotate detected patterns
    
  # Competitive dynamics visualization  
  competition_visualization:
    show_competition_links: true     # Display competitive relationships
    link_thickness_by_strength: true # Scale link thickness by competition strength
    competition_color_coding: true   # Color code competition types
    dilution_effect_animation: true  # Animate dilution effects

# =============================================================================
# ACADEMIC VALIDATION (enhanced)
# =============================================================================

theoretical_foundation:
  primary_sources:
    - "Complete academic citations for theoretical foundation"
    - "Methodological sources for validation approaches"
    - "Mathematical sources for algorithmic foundations"
  
  theoretical_approach: |
    Comprehensive explanation of theoretical grounding, methodological innovation,
    competitive dynamics modeling approach, temporal analysis methodology,
    and framework fit validation principles. Include discussion of theoretical
    weighting modeling and cross-framework comparison strategies.
  
  # v3.2 Enhancement: Advanced Validation
  validation_methodology: |
    Complete description of Olympics validation protocols, framework fit
    assessment procedures, competitive dynamics validation, temporal coherence
    testing, and cross-framework comparison standards. Include mathematical
    foundations and statistical significance testing approaches.
    
  innovation_contributions: |
    Specific theoretical or methodological innovations introduced by this
    framework, including novel anchor arrangements, competitive modeling
    approaches, temporal analysis methods, or validation techniques.

validation:
  academic_standard: "Advanced Multi-Dimensional Discourse Analysis Framework v3.2"
  measurement_instrument: "Comprehensive framework with competitive dynamics and temporal analysis"
  scope_limitation: "Detailed limitations and appropriate application contexts"
  
  # v3.2 Enhancement: Olympics Validation
  olympics_compliance: true          # Framework designed for Olympics competition
  olympics_category: "specify_category"  # Target competition category
  baseline_performance: "minimum_scores"  # Minimum acceptable performance levels
  
  citation_format: "Discernus Framework: Framework Name v3.2 (Jeffrey Whatcott, 2025)"
  academic_attribution: |
    When using this framework in academic work, cite as:
    "Discernus Framework: Framework Name v3.2 (Jeffrey Whatcott, 2025)"
    
    Include complete version number and specify v3.2 capabilities used:
    - Arc positioning and theoretical weighting modeling (if applicable)
    - Competitive dynamics analysis (if applicable)  
    - Temporal evolution tracking (if applicable)
    - Olympics validation protocols (if applicable)
    
    Provide framework registry key for exact reproducibility.

# =============================================================================
# SYSTEM COMPATIBILITY (enhanced)
# =============================================================================

compatibility:
  framework_specification_version: "3.2"
  backward_compatibility: ["3.1", "3.0"]
  
  prompt_templates:
    - advanced_multi_dimensional_v3.2
    - competitive_dynamics_v1.0
    - temporal_analysis_v1.0
    - olympics_validation_v1.0
  
  weighting_schemes:
    - weighting_corrected_weighting
    - competitive_dynamics_weighting
    - temporal_coherence_weighting
    - olympics_composite_scoring
  
  api_versions:
    - v3.2
    - v3.1
    - v3.0
  
  visualization_types:
    - circular_with_weighting
    - temporal_evolution
    - competitive_network
    - olympics_comparison
    - arc_clustering

# =============================================================================
# FRAMEWORK VERSIONING (required)
# =============================================================================

last_modified: "2025-06-27T12:00:00.000000"
framework_registry_key: "framework_name__v3.2"
implementation_status: "Production ready - v3.2 Advanced Research Architecture with full Olympics compatibility"

# v3.2 Enhancement: Framework Capabilities Declaration
capabilities:
  arc_positioning: true              # Supports clustered anchor positioning
  competitive_dynamics: true        # Models ideological competition
  temporal_analysis: true           # Tracks evolution over time
  framework_fit_validation: true    # Comprehensive validation metrics
  olympics_protocols: true          # Olympics competition ready
  weighting_corrections: true         # Theoretical weighting bias compensation
  cross_framework_comparison: true  # Rigorous comparison standards
```

## ✅ **VALIDATION REQUIREMENTS v3.2**

### **Comprehensive Validator Checklist**

**🔍 Framework Structure Validation**
```yaml
# Required validation checks for all frameworks:
framework_validation:
  basic_structure:
    - [ ] Framework name is unique and descriptive
    - [ ] Version follows semantic versioning (e.g., v3.2)
    - [ ] Description includes theoretical foundation
    - [ ] At least one positioning method defined
    
  schema_compliance:
    - [ ] YAML syntax is valid and parseable
    - [ ] All required fields are present
    - [ ] Field types match specification
    - [ ] No invalid field names or typos
```

**⚡ Hybrid Architecture Validation (Critical)**
```yaml
# Polar constraint and component registry validation:
hybrid_validation:
  component_registry:
    - [ ] All anchors registered with unique component_id
    - [ ] Each component has required fields (angle/position, weight, description)
    - [ ] No duplicate component_ids across framework
    
  axis_validation:
    - [ ] Each axis contains exactly 2 anchor_ids (CRITICAL - polar constraint)
    - [ ] All anchor_ids referenced in axes exist in component registry
    - [ ] No axis references non-existent components
    - [ ] Axis pole assignments (pole_a, pole_b) are distinct
    
  consistency_checks:
    - [ ] anchor_summary (if present) matches component registry descriptions
    - [ ] No orphaned components (components never referenced by axes)
    - [ ] Registry completeness ratio > 0.5 (recommended)
```

**🧮 Mathematical Validation**
```yaml
# Mathematical soundness checks:
mathematical_validation:
  positioning:
    - [ ] All angles are within [0, 360) degrees
    - [ ] All weights are positive numbers
    - [ ] Clock positions (if used) map to valid angles
    
  oppositional_relationship:
    - [ ] Axis poles represent true theoretical opposites
    - [ ] Angular separation between poles ≥ 90° (recommended)
    - [ ] No identical anchors on same axis
    
  semantic_coherence:
    - [ ] Framework captures distinct theoretical dimensions
    - [ ] No excessive anchor correlation (independence check)
    - [ ] Sufficient theoretical coverage
```

**📋 Validator Implementation Checklist**

**For Validator Developers:**
```python
def validate_framework(framework):
    """Complete framework validation with detailed error reporting."""
    
    errors = []
    warnings = []
    
    # 1. CRITICAL: Polar constraint validation
    for axis_name, axis in framework.axes.items():
        if len(axis.anchor_ids) != 2:
            errors.append(f"POLAR VIOLATION: Axis '{axis_name}' has {len(axis.anchor_ids)} anchors, requires exactly 2")
    
    # 2. CRITICAL: Component registry consistency
    components = set(framework.components.keys())
    for axis_name, axis in framework.axes.items():
        for anchor_id in axis.anchor_ids:
            if anchor_id not in components:
                errors.append(f"MISSING COMPONENT: Axis '{axis_name}' references unknown anchor '{anchor_id}'")
    
    # 3. RECOMMENDED: anchor_summary validation
    for axis_name, axis in framework.axes.items():
        if hasattr(axis, 'anchor_summary'):
            for anchor_id in axis.anchor_ids:
                if anchor_id not in axis.anchor_summary:
                    warnings.append(f"Missing anchor_summary for '{anchor_id}' in axis '{axis_name}'")
    
    return {
        'valid': len(errors) == 0,
        'errors': errors,
        'warnings': warnings,
        'polar_constraint_satisfied': all(len(axis.anchor_ids) == 2 for axis in framework.axes.values())
    }
```

### **Enhanced Structural Validation**

**Required Elements:**
- [ ] Framework identification complete with v3.2 capabilities declared
- [ ] At least one positioning method with optional arc configuration
- [ ] Competitive relationships defined if multiple theoretical concepts present
- [ ] Framework fit metrics configuration if validation required
- [ ] Temporal analysis configuration if evolution tracking needed
- [ ] Olympics protocols configuration if comparison intended

**Hybrid Axes-Anchors Requirements:**
- [ ] If using axes, anchors must be registered as independent components with unique `component_id` values
- [ ] Axes must reference exactly 2 anchors by their `anchor_ids` (polar constraint enforcement)
- [ ] Axes must demonstrate true oppositional relationship between the two referenced anchors
- [ ] **Recommended**: Axes should include `anchor_summary` field mapping anchor IDs to brief descriptions
- [ ] **Backward Compatibility**: Legacy inline anchor definitions remain valid but hybrid format preferred
- [ ] **Multi-Reference Guidance**: Frameworks needing 3+ reference points should use anchor-set architecture

**Advanced Component Validation:**
- [ ] **Arc Positioning**: Valid center angles, span ranges, distribution methods
- [ ] **Competitive Dynamics**: Valid competition pairs, strength coefficients, mechanisms
- [ ] **Framework Fit**: Appropriate thresholds, validation methods, correction factors
- [ ] **Temporal Analysis**: Coherent evolution tracking, pattern detection, stability measures
- [ ] **Olympics Integration**: Valid category, metrics, baseline requirements

### **Academic Validation Enhancement**

**v3.2 Requirements:**
- [ ] Theoretical foundation includes competitive dynamics methodology
- [ ] Validation methodology covers all enabled v3.2 capabilities
- [ ] Innovation contributions clearly documented
- [ ] Olympics compliance and category specified
- [ ] Cross-framework comparison standards defined

## 🎯 **v3.2 SUCCESS METRICS**

### **Technical Achievement**
- [ ] **Arc Positioning**: Theoretical weighting modeling fully functional
- [ ] **Competitive Dynamics**: Mathematical modeling operational
- [ ] **Framework Fit**: All validation metrics implemented
- [ ] **Temporal Analysis**: Evolution tracking with weighting corrections
- [ ] **Olympics Protocols**: Systematic comparison methodology complete

### **Academic Impact**
- [ ] **Advanced Validation**: Rigorous mathematical foundation
- [ ] **Cross-Framework Standards**: Meaningful comparison protocols
- [ ] **Methodological Innovation**: Novel analytical capabilities
- [ ] **Reproducibility**: Complete specification for replication

### **Research Enablement**
- [ ] **Sophisticated Analysis**: Multi-dimensional theoretical positioning
- [ ] **Competitive Modeling**: Ideological competition and dilution effects
- [ ] **Evolution Tracking**: Temporal pattern detection and analysis
- [ ] **Quality Assurance**: Comprehensive validation and comparison

---

**Document Version**: 3.2 PRODUCTION  
**Last Updated**: June 27, 2025  
**Breaking Changes**: Arc positioning, competitive dynamics, framework fit validation, Olympics protocols, polar constraint enforcement  
**Migration Path**: v3.1 frameworks automatically compatible, v3.2 features optional, new frameworks must satisfy polar constraint  
**Related Documents**:
- Discernus Coordinate System: Mathematical Foundations v1.0
- DCS Research Vocabulary: Comprehensive Glossary v2.0
- Framework Olympics: Systematic Validation Methodology (planned)

## 🧠 **LLM-OPTIMIZED PROMPTING ARCHITECTURE**

### **Core Principle: Make the Right Thing Easy**

The v3.2 specification introduces **systematic prompting guidelines** that make LLM-optimized patterns the default, easy path for framework authors. This eliminates the need to discover optimal prompting patterns independently.

### **The Five-Phase Prompting Architecture**

Based on LLM sequential processing research, optimal framework prompts follow a **five-phase cognitive flow**:

```yaml
# PHASE 1: COGNITIVE PRIMING (No forward references)
expert_role: |
  Establish domain expertise and analytical perspective.
  Language should match text language for analysis.
  No references to specific framework components.

# PHASE 2: FRAMEWORK METHODOLOGY (High-level approach)  
methodological_approach: |
  High-level methodology that guides framework interpretation.
  Should work for any framework in this theoretical family.
  Sets analytical frame before technical details.

# PHASE 3: FRAMEWORK STRUCTURE (Complete technical definitions)
components: {...}    # All anchor definitions with language_cues
axes: {...}         # Axis relationships  
competitive_relationships: {...}  # Competition modeling

# PHASE 4: DETAILED ANALYSIS INSTRUCTIONS (Reference framework elements)
detailed_analysis_instructions: |
  Comprehensive guidance that references specific components,
  language_cues, and relationships defined in Phase 3.
  Can safely use forward references because elements exist.

# PHASE 5: OUTPUT SPECIFICATION (Complete examples)
output_format: |
  Complete JSON structure with examples in target language.
  Shows exactly what the expected output should look like.
```

### **Language Consistency Principle**

**Rule**: All prompting elements must use **consistent language** that matches the analysis target:
- **Brazilian Portuguese texts** → All prompts in Portuguese
- **English texts** → All prompts in English
- **Mixed corpus** → Use framework's primary language consistently

**Anti-Pattern** (breaks LLM processing):
```yaml
# WRONG - Language switching within single framework
expert_role: |
  You are an expert analyst...  # English

analysis_methodology: |
  Análise sistemática de...     # Portuguese  

# This creates cognitive disruption
```

**Correct Pattern**:
```yaml
# RIGHT - Consistent language throughout
expert_role: |
  Você é um especialista...     # Portuguese

analysis_methodology: |  
  Análise sistemática de...     # Portuguese

# Maintains cognitive coherence
```

### **Framework Prompting Templates**

#### **Template 1: Political Discourse Analysis (Brazilian Portuguese)**

```yaml
# Use this template for Brazilian political discourse frameworks
prompting_architecture:
  # PHASE 1: COGNITIVE PRIMING
  expert_role: |
    Você é um especialista em análise de discurso político brasileiro com profundo 
    conhecimento de [THEORETICAL_DOMAIN]. Você possui expertise específica em 
    [METHODOLOGY_NAME] e nas dinâmicas políticas do Brasil.
    
    Sua tarefa é analisar discursos políticos brasileiros usando o [FRAMEWORK_NAME], 
    focando em [PRIMARY_DIMENSIONS].

  # PHASE 2: FRAMEWORK METHODOLOGY  
  methodological_approach: |
    **METODOLOGIA DE ANÁLISE:**
    
    Use o [FRAMEWORK_NAME] com [STRUCTURE_TYPE]:
    - **[DIMENSION_1]**: [BRIEF_DESCRIPTION]
    - **[DIMENSION_2]**: [BRIEF_DESCRIPTION]
    
    Avalie cada dimensão independentemente para evitar efeitos de halo, focando 
    nos indicadores linguísticos específicos definidos no framework.

  # PHASE 3: Framework structure goes here (components, axes, etc.)

  # PHASE 4: DETAILED INSTRUCTIONS
  detailed_analysis_instructions: |
    **INSTRUÇÕES DETALHADAS DE ANÁLISE:**
    
    **Para [ANCHOR_1]** (ângulo [ANGLE]°):
    - Procure por: [CORE_INDICATORS]
    - Indicadores-chave: [LANGUAGE_CUES_LIST]
    - Foque em: [FOCUS_AREAS]
    
    **Para [ANCHOR_2]** (ângulo [ANGLE]°):
    - Procure por: [CORE_INDICATORS]  
    - Indicadores-chave: [LANGUAGE_CUES_LIST]
    - Foque em: [FOCUS_AREAS]
    
    [REPEAT_FOR_ALL_ANCHORS]

  # PHASE 5: OUTPUT FORMAT
  output_format: |
    Retorne um objeto JSON com as [NUMBER] dimensões. Cada entrada deve conter:
    
    ```json
    {
      "[ANCHOR_1]": {
        "score": 0.0-1.0,
        "evidence": "[citação direta do texto em português]",
        "reasoning": "[justificativa baseada nos indicadores do framework]"
      }
    }
    ```
    
    **CRÍTICO**: Sempre inclua evidência textual em português e raciocínio 
    baseado nos indicadores específicos do framework.
```

#### **Template 2: English Academic Analysis**

```yaml
# Use this template for English academic discourse frameworks
prompting_architecture:
  # PHASE 1: COGNITIVE PRIMING
  expert_role: |
    You are an expert analyst of [DISCOURSE_TYPE] with deep knowledge of 
    [THEORETICAL_DOMAIN]. You specialize in [METHODOLOGY_NAME] using established 
    academic frameworks for analyzing [CONTENT_TYPE].
    
    Your task is to analyze [TEXT_TYPE] using the [FRAMEWORK_NAME], focusing 
    on [PRIMARY_DIMENSIONS].

  # PHASE 2: FRAMEWORK METHODOLOGY
  methodological_approach: |
    **ANALYSIS METHODOLOGY:**
    
    Apply the [FRAMEWORK_NAME] with [STRUCTURE_TYPE]:
    - **[DIMENSION_1]**: [BRIEF_DESCRIPTION]
    - **[DIMENSION_2]**: [BRIEF_DESCRIPTION]
    
    Evaluate each dimension independently to avoid halo effects, focusing on 
    specific linguistic indicators and textual evidence defined in the framework.

  # PHASE 3: Framework structure goes here

  # PHASE 4: DETAILED INSTRUCTIONS  
  detailed_analysis_instructions: |
    **DETAILED ANALYSIS INSTRUCTIONS:**
    
    **For [ANCHOR_1]** (angle [ANGLE]°):
    - Look for: [CORE_INDICATORS]
    - Key indicators: [LANGUAGE_CUES_LIST]
    - Focus on: [FOCUS_AREAS]
    
    **For [ANCHOR_2]** (angle [ANGLE]°):
    - Look for: [CORE_INDICATORS]
    - Key indicators: [LANGUAGE_CUES_LIST]
    - Focus on: [FOCUS_AREAS]
    
    [REPEAT_FOR_ALL_ANCHORS]

  # PHASE 5: OUTPUT FORMAT
  output_format: |
    Return a JSON object with the [NUMBER] dimensions. Each entry should contain:
    
    ```json
    {
      "[ANCHOR_1]": {
        "score": 0.0-1.0,
        "evidence": "[direct quote from text]",
        "reasoning": "[brief justification based on framework indicators]"
      }
    }
    ```
    
    **CRITICAL**: Always include textual evidence and reasoning based on 
    specific framework indicators.
```

### **Prompting Quality Validation**

Framework authors should validate their prompting using this checklist:

#### **✅ Language Consistency Check**
- [ ] All prompting elements use the same language
- [ ] Language matches the target text corpus language  
- [ ] No mid-prompt language switching
- [ ] Cultural/regional context appropriate (e.g., Brazilian Portuguese vs European Portuguese)

#### **✅ Sequential Flow Check**
- [ ] Phase 1: Context established before framework details
- [ ] Phase 2: Methodology explained before technical components
- [ ] Phase 3: All framework elements defined before being referenced
- [ ] Phase 4: Detailed instructions reference existing framework elements
- [ ] Phase 5: Complete output examples provided

#### **✅ Forward Reference Check**
- [ ] Early prompts don't reference undefined framework components
- [ ] All referenced elements exist in framework structure
- [ ] References use exact component_ids and language_cues
- [ ] No broken or circular references

#### **✅ Cognitive Load Check**
- [ ] Expert role establishes domain without overwhelming detail
- [ ] Each section has single, clear purpose
- [ ] Instructions progress from general to specific
- [ ] Examples are complete and realistic
- [ ] Total prompt length manageable (< 3000 words recommended)

### **Common Anti-Patterns to Avoid**

#### **❌ Anti-Pattern 1: Language Inconsistency**
```yaml
# WRONG
expert_role: |
  You are an expert analyst...          # English
analysis_instructions: |
  Procure por retórica anti-elite...     # Portuguese
```

#### **❌ Anti-Pattern 2: Forward References**
```yaml
# WRONG  
expert_role: |
  Apply the language_cues defined in the components section below...
# Problem: components section doesn't exist yet in LLM context
```

#### **❌ Anti-Pattern 3: Information Fragmentation**
```yaml
# WRONG
prompt_guidance:
  role_definition: "Brief role"
  framework_instructions: "Brief framework"  
  scoring_requirements: "Brief scoring"
  json_format: "Brief format"
# Problem: Information scattered, no logical flow
```

#### **❌ Anti-Pattern 4: Technical Details First**
```yaml  
# WRONG
expert_role: |
  Score the populism anchor at angle 90° using language_cues...
# Problem: Technical details before cognitive context
```

### **Implementation Guidelines for Framework Authors**

#### **Step 1: Choose Language**
Determine target corpus language and use consistently throughout all prompting elements.

#### **Step 2: Use Template**  
Select appropriate template (Brazilian Portuguese Political, English Academic, etc.) and fill in framework-specific details.

#### **Step 3: Validate Flow**
Ensure prompting follows five-phase architecture with proper forward reference resolution.

#### **Step 4: Test with Examples**
Include complete, realistic JSON examples that demonstrate expected output format.

#### **Step 5: Quality Check**
Run through validation checklist to catch common anti-patterns.

### **Framework Specification Integration**

The prompting architecture integrates seamlessly with other v3.2 features:

```yaml
# Complete framework with optimized prompting
name: example_framework
version: v3.2

# Standard framework structure
components: {...}
axes: {...}
competitive_relationships: {...}

# LLM-Optimized prompting (follows five-phase architecture)
prompting_architecture:
  expert_role: |
    [Phase 1: Cognitive priming]
  methodological_approach: |
    [Phase 2: Framework methodology]
  detailed_analysis_instructions: |
    [Phase 4: Component-referencing instructions]
  output_format: |
    [Phase 5: Complete examples]
  
# Other v3.2 features
temporal_analysis: {...}
framework_fit_metrics: {...}
```

This architecture ensures framework authors naturally create LLM-optimized prompts without needing to understand the underlying cognitive processing principles.