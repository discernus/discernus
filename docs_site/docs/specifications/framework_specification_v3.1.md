# Framework Specification v3.1
**Version:** 3.1  
**Date:** June 23, 2025  
**Status:** PRODUCTION - Attribute-Based Architecture  
**Breaking Changes:** Flexible attribute system, simplified versioning, mandatory citation format  

## 🎯 **OVERVIEW**

Framework Specification v3.1 introduces **flexible attribute-based framework architecture** that eliminates rigid framework types in favor of component-driven design. Frameworks define their capabilities through the presence of specific attributes, enabling maximum research flexibility while maintaining system consistency.

## 🚀 **VERSION 3.1 ENHANCEMENTS**

### **Revolutionary Changes**
- ✅ **Attribute-Based Architecture**: No more rigid framework types - frameworks define themselves
- ✅ **Flexible Versioning**: Simple dot notation (v1.0, v1.204, v215.44) for maximum researcher freedom
- ✅ **Self-Documenting Frameworks**: All documentation integrated into framework files
- ✅ **Mandatory Citation Format**: "Discernus Framework: Name vX.Y (Author, Year)" for academic consistency
- ✅ **Run-Time Registration**: Only successfully validated frameworks enter database registry

### **Preserved Features**  
- ✅ **Configurable Algorithms**: Advanced algorithm customization from v3.0
- ✅ **Academic Rigor**: Theoretical foundation and validation requirements
- ✅ **Integrated Prompting**: LLM guidance embedded in framework configuration

### **Clean Slate Migration**
- ✅ **Database Purge**: Fresh start with current frameworks reset to v1.0
- ✅ **Provenance Guarantee**: Only production-validated frameworks registered

## 📋 **FRAMEWORK ARCHITECTURE**

### **Core Philosophy: Attribute Presence = Capability**

Frameworks are **component collections** rather than **rigid types**. The presence of specific attributes determines framework behavior:

```yaml
# Framework defines itself through component presence
name: my_research_framework
version: v1.0

# POSITIONING COMPONENTS (at least one required)
axes: {...}              # If present: framework uses opposing anchor pairs
anchors: {...}           # If present: framework uses independent anchors  
clusters: {...}          # If present: framework uses grouped positioning

# ALGORITHMIC COMPONENTS (optional)
algorithm_config: {...}  # If present: framework uses custom algorithms

# ANALYSIS COMPONENTS (optional)
metrics: {...}           # If present: framework provides custom metrics
prompt_configuration: {...} # If present: framework includes LLM guidance
```

### **Validation Logic**

The framework validator ensures **structural integrity** without imposing **architectural constraints**:

**Required Validation:**
1. **At least one positioning method** must be present (`axes`, `anchors`, or `clusters`)
2. **All angle assignments are unique** across all positioning components
3. **Required fields complete** for each component type used
4. **Cross-references valid** (cluster members exist, algorithm parameters in range)
5. **Version format correct** (flexible dot notation starting with 'v')

**Flexible Validation:**
- **No restriction on component combinations** - mix axes, anchors, and clusters freely
- **No naming conventions enforced** - researchers choose meaningful names
- **No structural hierarchy imposed** - organize components logically for your research

## 🔧 **COMPLETE FRAMEWORK SCHEMA**

```yaml
# =============================================================================
# FRAMEWORK IDENTIFICATION (required)
# =============================================================================
name: unique_framework_name        # Must be unique across all frameworks
version: v1.0                     # Flexible dot notation (v1.0, v1.204, v215.44)
display_name: "Framework Display Name"
description: |
  Self-documenting framework description replacing separate README files.
  Include all content that would typically be in documentation files.
  
  ## Theoretical Foundation
  Academic sources, theoretical grounding, and methodological approach.
  
  ## Usage Guidelines  
  How researchers should apply this framework in their analysis.
  
  ## Version History
  v1.0: Initial implementation with [key features]
  v1.1: Enhanced [specific improvements]
  
  ## Citation Format
  Discernus Framework: Framework Name v1.0 (Author, 2025)

# =============================================================================
# POSITIONING DEFINITION (at least one required)
# =============================================================================

# Option 1: Opposing Anchor Pairs (Axes)
axes:
  Care_Harm:
    description: "Foundation evolved from mammalian attachment systems"
    integrative:
      name: "Care"
      description: "Concern for suffering of others, compassion, protection"
      position: "12 o'clock"     # Clock position (alternative to angle)
      weight: 1.0
      type: individualizing
      opposite_of: "Harm"
    disintegrative:
      name: "Harm"
      description: "Actions causing suffering, cruelty, violence"
      angle: 180              # Degree position (alternative to position)
      weight: 1.0
      type: individualizing
      opposite_of: "Care"

# Option 2: Independent Anchors
anchors:
  AnchorName:
    description: "Independent semantic anchor description"
    angle: 0                  # Position using degrees (0-359)
    # OR
    position: "3 o'clock"     # Position using clock reference (alternative)
    weight: 1.0               # Relative importance
    type: semantic_type       # For visualization grouping
    language_cues:
      - anchor indicator 1
      - anchor indicator 2

# Option 3: Clustered Positioning
positioning_strategy:
  type: domain_arc_clustering  # Or another method
  description: "High-level description of the positioning methodology"
  
  clusters:
    cluster_name:
      description: "Cluster purpose and theoretical justification"
      center_angle: 45          # Center of cluster arc
      span: 60                  # Arc span in degrees
      arc_range: [15, 75]       # Explicit start/end angles
      positioning_method: even_distribution_within_arc
      
      # Clusters can contain axes, anchors, or both
      axes:
        ClusteredAxis: {...}    # Axis within cluster
      anchors:
        ClusteredAnchor: {...}  # Anchor within cluster

# =============================================================================
# ALGORITHMIC CONFIGURATION (optional)
# =============================================================================

algorithm_config:
  dominance_amplification:
    enabled: true
    threshold: 0.7
    multiplier: 1.1
    rationale: "Enhances LLM-identified dominant moral foundations"
    
  adaptive_scaling:
    enabled: true                    # Enable/disable adaptive scaling
    base_scaling: 0.65              # Minimum scaling factor (0.3-0.8)
    max_scaling: 0.95               # Maximum scaling factor (0.8-1.0)
    variance_factor: 0.3            # Variance sensitivity (0.1-0.5)
    mean_factor: 0.1                # Mean sensitivity (0.05-0.2)
    methodology: "Scaling methodology description and justification"
    
  prompting_integration:
    dominance_instruction: "LLM instructions for identifying hierarchical patterns"
    amplification_purpose: "Explanation of mathematical enhancement purpose"
    methodology_reference: "Reference to detailed methodology documentation"

# =============================================================================
# COORDINATE SYSTEM (optional)
# =============================================================================

coordinate_system:
  type: circle                      # Coordinate system geometry
  radius: 1.0                       # Coordinate space radius
  description: "Coordinate system description and properties"

# =============================================================================
# POSITIONING SYSTEM: DEGREES OR CLOCK FACE
# =============================================================================

positioning_options:
  degrees:
    format: "angle: 0-359"
    description: "Precise degree positioning on unit circle"
    examples: ["angle: 0", "angle: 127", "angle: 270"]
    
  clock_face:
    format: "position: 'X o'clock'"
    description: "Intuitive clock face positioning"
    examples: ["position: '12 o'clock'", "position: '3 o'clock'", "position: '6 o'clock'"]
    
  conversion_table:
    "12 o'clock": 0     # Top (North)
    "1 o'clock": 30
    "2 o'clock": 60
    "3 o'clock": 90     # Right (East)
    "4 o'clock": 120
    "5 o'clock": 150
    "6 o'clock": 180    # Bottom (South)
    "7 o'clock": 210
    "8 o'clock": 240
    "9 o'clock": 270    # Left (West)
    "10 o'clock": 300
    "11 o'clock": 330
    
  usage_guidelines:
    mixed_usage: "Frameworks can mix degrees and clock positions freely"
    validation: "System converts clock positions to degrees internally"
    precision: "Use degrees for exact positioning, clock for intuitive placement"
    academic_citation: "Both formats equally valid in academic work"

**What This Positioning System Means in Plain English:**

Think of your framework as a clock face where you can place concepts around the circle:

- **"12 o'clock" = top** - often used for positive, aspirational, or "good" concepts
- **"6 o'clock" = bottom** - often used for negative, problematic, or opposing concepts  
- **"3 o'clock" = right side, "9 o'clock" = left side** - useful for neutral distinctions or different domains
- **Precise degrees (0-359)** - when you need exact positioning that doesn't match a clock hour
- **Mix freely** - use "12 o'clock" for easy concepts and "127°" for precise positioning in the same framework

The system automatically converts everything to degrees internally, but keeps your original format for documentation. This means researchers can think in whatever way feels natural - intuitive clock positions or precise mathematical angles.

# =============================================================================
# ANALYSIS CONFIGURATION (optional)
# =============================================================================

metrics:
  metric_name:
    name: "Human-Readable Metric Name"
    description: "What this metric measures and how to interpret it"
    calculation: "Mathematical formula or calculation method"

# =============================================================================
# LLM INTEGRATION (optional)
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
  
  enhanced_detection_instructions: |
    Advanced detection patterns and sophisticated analysis techniques

# =============================================================================
# VISUALIZATION CONFIGURATION (optional)
# =============================================================================

visualization:
  type_colors:
    semantic_type: "#HEX_COLOR"     # Color mapping for semantic types
  
  supported_charts:
    - circular
    - radar
    - custom_type
  
  chart_specific_config:
    circular:
      show_grid: true
      highlight_clusters: true

# =============================================================================
# ACADEMIC VALIDATION (required)
# =============================================================================

theoretical_foundation:
  primary_sources:
    - "Haidt, J. (2012). The righteous mind: Why good people are divided by politics and religion."
  
  theoretical_approach: |
    Detailed explanation of theoretical foundation, methodological approach,
    and academic grounding for the framework design.
  
  academic_validation: |
    Description of validation methods, expert consultation, or empirical
    testing that supports the framework's academic credibility.

validation:
  academic_standard: "Reference theoretical framework or standard"
  measurement_instrument: "Validation instruments or methods used"
  scope_limitation: "Known limitations and appropriate scope of application"
  
  citation_format: "Discernus Framework: Framework Name v1.0 (Author, 2025)"
  academic_attribution: |
    When using this framework in academic work, cite as:
    "Discernus Framework: Framework Name v1.0 (Author, 2025)"
    
    Include framework version for reproducibility and provenance tracking.

# =============================================================================
# SYSTEM COMPATIBILITY (optional)
# =============================================================================

compatibility:
  prompt_templates:
    - template_v1.0
  weighting_schemes:
    - scheme_name
  api_versions:
    - v3.1
    - v3.0
  visualization_types:
    - circular
    - custom

# =============================================================================
# FRAMEWORK VERSIONING (required)
# =============================================================================

last_modified: "2025-06-23T12:00:00.000000"
framework_registry_key: "framework_name__v1.0"    # Composite unique identifier
implementation_status: "Production ready with attribute-based architecture"
```

## 📊 **FRAMEWORK EXAMPLES**

### **Example 1: Axis-Based Framework (MFT-style)**

```yaml
name: moral_foundations_theory
version: v1.0
display_name: "Moral Foundations Theory"

description: |
  Enhanced Moral Foundations Theory framework implementing Jonathan Haidt's research.
  
  ## Theoretical Foundation
  Based on Haidt's Moral Foundations Theory which identifies innate psychological 
  foundations that cultures build upon to create diverse moral systems.
  
  ## Citation Format
  Discernus Framework: Moral Foundations Theory v1.0 (Haidt, 2025)

axes:
  Care_Harm:
    description: "Foundation evolved from mammalian attachment systems"
    integrative:
      name: "Care"
      description: "Concern for suffering of others, compassion, protection"
      position: "12 o'clock"     # Clock position (alternative to angle)
      weight: 1.0
      type: individualizing
      opposite_of: "Harm"
    disintegrative:
      name: "Harm"
      description: "Actions causing suffering, cruelty, violence"
      angle: 180              # Degree position (alternative to position)
      weight: 1.0
      type: individualizing
      opposite_of: "Care"

algorithm_config:
  dominance_amplification:
    enabled: true
    threshold: 0.7
    multiplier: 1.1
    rationale: "Enhances LLM-identified dominant moral foundations"

theoretical_foundation:
  primary_sources:
    - "Haidt, J. (2012). The righteous mind: Why good people are divided by politics and religion."
```

**What This Example Means in Plain English:**

This framework analyzes moral reasoning by looking at opposing concepts like Care vs Harm. When you analyze a text, the system:

- **Positions Care at "12 o'clock"** (top of the circle) - this represents positive moral concern for others' wellbeing
- **Positions Harm at 180°** (bottom of the circle) - this represents actions that cause suffering or damage  
- **Links them as opposites** using `opposite_of` - the system knows these are two ends of the same moral dimension
- **Uses algorithm enhancement** - when the system detects strong moral language, it amplifies those scores for clearer analysis
- **Creates a moral profile** - your text gets scored on how much it emphasizes care vs harm, with results plotted on this moral compass

The result is a visual map showing where your text falls on the Care-Harm spectrum, making moral reasoning patterns easy to see and compare across different texts.

### **Example 2: Anchor-Based Framework**

```yaml
name: political_theories
version: v1.0
display_name: "Political Theories Framework"

description: |
  Independent anchor framework analyzing liberal, conservative, and libertarian
  political theory orientations without opposing pole assumptions.
  Demonstrates mixed positioning: degrees and clock face references.
  
  ## Citation Format
  Discernus Framework: Political Theories v1.0 (Rawls, 2025)

anchors:
  Liberal:
    description: "Progressive political theory emphasizing equality and social justice"
    position: "12 o'clock"      # Clock positioning - top
    weight: 1.0
    type: progressive
  
  Conservative:
    description: "Traditional political theory emphasizing order and stability"
    angle: 120                  # Degree positioning - precise
    weight: 1.0
    type: traditional
  
  Libertarian:
    description: "Individual liberty theory emphasizing minimal government"
    position: "8 o'clock"       # Clock positioning - lower left
    weight: 1.0
    type: individualist
```

**What This Example Means in Plain English:**

This framework analyzes political philosophy using three independent reference points instead of opposing pairs. When you analyze a text, the system:

- **Liberal at "12 o'clock"** (top) - represents progressive thinking about equality and social justice
- **Conservative at 120°** (upper right) - represents traditional approaches to order and stability  
- **Libertarian at "8 o'clock"** (lower left) - represents individual liberty and minimal government approaches
- **Mixed positioning formats** - shows you can use intuitive clock positions ("12 o'clock") or precise degrees (120°) as needed
- **No opposing pairs** - each political theory stands alone, so a text can score high on multiple theories simultaneously

The result is a three-way political profile showing how much your text aligns with each political philosophy, without forcing false oppositions between them.

### **Example 3: Clustered Framework with Mixed Positioning**

```yaml
name: business_ethics
version: v1.0
display_name: "Business Ethics Framework"

description: |
  Clustered framework analyzing business ethics across stakeholder relations,
  operational integrity, and strategic vision domains.
  Uses both clock and degree positioning for different precision needs.
  
  ## Citation Format
  Discernus Framework: Business Ethics v1.0 (Freeman, 2025)

positioning_strategy:
  type: domain_arc_clustering
  description: "Three-domain business ethics clustering"

  clusters:
    stakeholder_relations:
      description: "Stakeholder relationship ethics cluster"
      center_angle: 45
      span: 60
      positioning_method: even_distribution_within_arc
      
      axes:
        Customer_Relations:
          integrative:
            name: "Customer_Service"
            position: "2 o'clock"    # Clock positioning
            weight: 1.0
          disintegrative:
            name: "Customer_Exploitation"
            angle: 210              # Degree positioning
            weight: 1.0
```

**What This Example Means in Plain English:**

This framework analyzes business ethics by grouping related concepts into clusters around the circle. When you analyze a text, the system:

- **Creates ethical domains** - groups related business concerns into clusters like "stakeholder relations" in one area of the circle
- **Positions clusters strategically** - the stakeholder cluster spans 60° around the "2 o'clock" area, focusing ethical analysis on that region
- **Mixes positioning methods** - Customer Service uses intuitive "2 o'clock" positioning while Customer Exploitation uses precise 210° positioning
- **Analyzes within domains** - your text gets scored on how it treats customers (service vs exploitation) within the broader stakeholder domain
- **Shows ethical emphasis** - results reveal which domains of business ethics your text prioritizes

The result is a business ethics profile that shows not just what ethical stances your text takes, but which areas of business responsibility it focuses on most.

## 🔄 **VERSIONING SYSTEM**

### **Version Format: Flexible Dot Notation**

**Allowed Formats:**
- `v1.0` - Initial version
- `v1.204` - Many iterations  
- `v215.44` - Years of development
- `v2.1.3.7` - Hierarchical versioning

**Version Rules:**
- Must start with lowercase `v`
- Must have at least two numbers (major.minor)
- Unlimited decimal places allowed
- Researchers decide increment meaning

### **Version Increment Guidelines**

```yaml
version_guidance: |
  🔄 VERSION FORMAT RULES:
  - Must start with lowercase 'v'
  - At least two numbers (major.minor): v1.0
  - No leading zeros: Automatically normalized (v1.01 → v1.1)
  - Unlimited decimal places allowed: v1.2.3.4.5
  
  🔄 WHEN TO INCREMENT:
  - v1.0 → v1.1: Minor prompt adjustments, language cues updates
  - v1.0 → v2.0: Major theoretical changes, new anchors/axes
  - v1.0 → v1.0.1: Bug fixes, typo corrections
  - v1.0 → v1.204: Extensive iterative refinement
  
  💡 RESEARCHER FREEDOM:
  - You decide what constitutes major vs minor changes
  - Increment whenever you want reproducible separation
  - Use as many decimal places as needed
  - Document major changes in framework description
  
  🔧 AUTO-NORMALIZATION:
  The system automatically removes leading zeros for consistency:
  - v01.001 → v1.1 (with notification)
  - v1.0 → v1.0 (no change needed)
  - v2.010 → v2.10 (normalized)
  
  This prevents citation ambiguity and database conflicts.
  
  📚 ACADEMIC CITATION REQUIREMENT:
  All frameworks must be cited using the standard format:
  "Discernus Framework: [Framework Name] v[Version] ([Author], [Year])"
  
  This ensures proper attribution and version-specific reproducibility.
```

### **Framework Registration: Run-Time Validation**

Frameworks enter the system registry **only after successful validation**:

```python
def register_framework_on_successful_run(name, version, framework_yaml):
    """Register framework when it successfully completes full experimental run"""
    composite_key = f"{name}__{version}"
    
    if not framework_registry.exists(composite_key):
        framework_registry.insert({
            'name': name,
            'version': version,
            'composite_key': composite_key,
            'framework_yaml': framework_yaml,
            'first_successful_run': timestamp(),
            'validation_status': 'production_validated',
            'run_count': 1
        })
    else:
        framework_registry.increment_run_count(composite_key)
```

**Benefits:**
- **Clean Database**: Only working frameworks registered
- **Provenance Guarantee**: All registered frameworks production-tested
- **Automatic Curation**: Self-cleaning registry of functional frameworks

## ✅ **VALIDATION REQUIREMENTS**

### **Structural Validation**

**Required Elements:**
- [ ] Framework identification complete (`name`, `version`, `display_name`, `description`)
- [ ] At least one positioning method present (`axes`, `anchors`, or `clusters`)
- [ ] All angle assignments unique (no conflicts across components)
- [ ] Version format valid (flexible dot notation starting with 'v')
- [ ] Citation format included in description
- [ ] Theoretical foundation documented

**Component Validation:**
- [ ] **Axes**: Both integrative and disintegrative anchors defined with proper `opposite_of` links
- [ ] **Anchors**: Complete anchor specifications with unique angles or clock positions
- [ ] **Clusters**: Valid arc ranges, existing member references
- [ ] **Algorithm Config**: Parameters within valid ranges if present
- [ ] **Prompting**: Complete LLM guidance if present
- [ ] **Angle Conflicts**: No duplicate angles except legitimate opposites linked via `opposite_of`
- [ ] **Positioning Format**: Each anchor uses either `angle` OR `position`, not both
- [ ] **Clock Validation**: Clock positions use valid format ("1 o'clock" through "12 o'clock")
- [ ] **Version Format**: Proper dot notation (auto-normalized if needed)
- [ ] **Attribute Consistency**: At least one positioning method present

### **Academic Validation**

**Required Documentation:**
- [ ] Theoretical foundation with primary sources
- [ ] Academic validation methodology
- [ ] Scope limitations acknowledged  
- [ ] Proper citation format specified
- [ ] Framework description comprehensive and self-contained

### **System Validation**

**Integration Requirements:**
- [ ] Framework loads without errors
- [ ] All cross-references resolve correctly
- [ ] Algorithm parameters within safe ranges
- [ ] Visualization configuration valid
- [ ] Compatibility specifications accurate

### **Validation Algorithm Specification**

**Angle Conflict Detection with Opposite Support:**
```python
CLOCK_POSITIONS = {
    "12 o'clock": 0, "1 o'clock": 30, "2 o'clock": 60, "3 o'clock": 90,
    "4 o'clock": 120, "5 o'clock": 150, "6 o'clock": 180, "7 o'clock": 210,
    "8 o'clock": 240, "9 o'clock": 270, "10 o'clock": 300, "11 o'clock": 330
}

def normalize_positioning(anchor_config):
    """Convert clock position to degrees or validate existing angle"""
    has_angle = 'angle' in anchor_config
    has_position = 'position' in anchor_config
    
    if has_angle and has_position:
        raise ValidationError("Use either 'angle' OR 'position', not both")
    
    if has_position:
        position = anchor_config['position']
        if position in CLOCK_POSITIONS:
            anchor_config['angle'] = CLOCK_POSITIONS[position]
            # Keep position for documentation, but angle is used internally
        else:
            raise ValidationError(f"Invalid clock position: {position}. Use '1 o'clock' through '12 o'clock'")
    
    elif not has_angle:
        raise ValidationError("Must specify either 'angle' or 'position'")
    
    # Validate angle range
    if not (0 <= anchor_config['angle'] <= 359):
        raise ValidationError(f"Angle must be 0-359 degrees, got: {anchor_config['angle']}")

def validate_angle_conflicts(framework):
    """Validate angle assignments allowing legitimate opposites"""
    # First normalize all positioning (convert clock to degrees)
    normalize_all_positions(framework)
    
    all_angles = collect_all_angles(framework)
    
    for angle in all_angles:
        conflicts = [a for a in all_angles if a.angle == angle.angle and a != angle]
        
        for conflict in conflicts:
            # Allow if they're properly linked opposites within same axis
            if (hasattr(angle, 'opposite_of') and hasattr(conflict, 'opposite_of') and
                angle.opposite_of == conflict.name and conflict.opposite_of == angle.name):
                continue  # This is a legitimate opposing pair
            else:
                raise ValidationError(f"Angle conflict: {angle.angle}° used by both {angle.name} and {conflict.name}")

def normalize_version(version):
    """Auto-normalize version removing leading zeros"""
    if not version.startswith('v'):
        raise ValidationError("Version must start with 'v'")
    
    parts = version[1:].split('.')
    normalized_parts = []
    
    for part in parts:
        if not part.isdigit():
            raise ValidationError(f"Non-numeric version part: {part}")
        # Strip leading zeros but preserve single '0'
        normalized_parts.append(str(int(part)))
    
    normalized_version = 'v' + '.'.join(normalized_parts)
    
    if normalized_version != version:
        logger.warning(f"Auto-normalized version: {version} → {normalized_version}")
    
    return normalized_version
```

## 🚀 **MIGRATION STRATEGY**

### **Clean Slate Approach**

**Database Purge:**
```sql
-- Clean slate: remove all existing framework data
TRUNCATE framework_registry;
TRUNCATE experiments WHERE framework_version IS NULL;
TRUNCATE runs WHERE framework_composite_key IS NULL;
```

**Framework Reset:**
```bash
# Reset all current frameworks to v1.0
mv moral_foundations_theory_framework.yaml moral_foundations_theory_v1.0.yaml
mv business_ethics_framework.yaml business_ethics_v1.0.yaml
mv civic_virtue_framework.yaml civic_virtue_v1.0.yaml

# Update internal version numbers to v1.0
# Add mandatory citation formats
# Integrate README content into descriptions
```

### **Framework File Updates**

**Required Changes:**
1. **Version Reset**: All frameworks become v1.0
2. **Citation Integration**: Add mandatory citation format to description
3. **Documentation Integration**: Move README content into framework description
4. **Attribute Alignment**: Ensure component structure matches v3.1 schema
5. **Validation Compliance**: Meet all validation requirements

### **System Integration**

**Code Updates Required:**
- Framework loader updated for attribute-based validation
- Registry system implemented for run-time registration
- Version validation for flexible dot notation
- Citation format validation
- Database schema updates for composite keys

## 📚 **ACADEMIC REPORTING REQUIREMENTS**

### **Mandatory Citation Format**

**All academic work using Discernus frameworks must cite using:**
```
Discernus Framework: [Framework Name] v[Version] ([Developer], [Year])
```

**Examples:**
- Discernus Framework: Moral Foundations Theory v3.0 (Haidt, 2025)
- Discernus Framework: Business Ethics v1.2 (Freeman, 2025)
- Discernus Framework: Political Spectrum v2.15 (Smith, 2025)

### **Methods Section Template**

```text
Framework Analysis Configuration:
- Framework: [Citation using standard format]
- Algorithm Configuration: [Document any custom parameters]
- Positioning Method: [Axes/Anchors/Clustered description]
- Analysis Date: [Date range]
- Framework Registry Key: [name__version for reproducibility]

Methodological Approach: Analysis employed the Discernus coordinate system
using [framework description]. [Additional methodological details as needed.]
```

## 🎯 **SUCCESS METRICS**

### **Technical Metrics**
- [ ] **100% Attribute Flexibility**: Any combination of axes/anchors/clusters supported
- [ ] **Zero Framework Type Constraints**: No artificial architectural limitations
- [ ] **Complete Version Flexibility**: Unlimited dot notation support
- [ ] **Positioning Options**: Both degrees and clock face positioning supported
- [ ] **Mixed Positioning**: Frameworks can combine degrees and clock positions seamlessly
- [ ] **Automatic Registration**: Only validated frameworks in registry
- [ ] **Self-Documentation**: All frameworks contain integrated documentation

### **Academic Metrics**
- [ ] **Consistent Citations**: All academic work uses standard format
- [ ] **Provenance Tracking**: Complete version history for reproducibility
- [ ] **Theoretical Rigor**: All frameworks document academic foundation
- [ ] **Research Flexibility**: Researchers can innovate without constraint

### **System Metrics**
- [ ] **Clean Database**: Registry contains only production-validated frameworks
- [ ] **Validation Integrity**: All registered frameworks meet quality standards
- [ ] **Migration Success**: All existing frameworks upgraded to v3.1
- [ ] **Documentation Quality**: Framework descriptions comprehensive and clear

---

**Document Version**: 3.1 PRODUCTION  
**Last Updated**: June 23, 2025  
**Breaking Changes**: Attribute-based architecture, flexible versioning, mandatory citations  
**Migration Required**: All existing frameworks must update to v3.1 schema  
**Related Documents**:
- Configurable Algorithms Methodology v3.0
- Framework Validation Guide v3.1 (planned)
- Academic Citation Standards v3.1 (planned)
- Framework Migration Toolkit v3.1 (planned) 