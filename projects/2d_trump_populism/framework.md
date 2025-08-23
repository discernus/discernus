# Framework Reference: Populist Discourse Analysis Framework (PDAF) v10.0

---

## Framework Overview

**Framework Name**: Populist Discourse Analysis Framework (PDAF)  
**Framework Version**: 10.0.0  
**Specification Version**: 10.0  
**Framework Type**: Reference Framework (Core Team Maintained)  
**Location**: `frameworks/reference/flagship/pdaf_v10.md`

---

## Framework Description

The Populist Discourse Analysis Framework (PDAF) v10.0 is a comprehensive analytical tool designed to identify, measure, and analyze the core rhetorical components of populist political communication through advanced strategic tension analysis and salience-weighted measurement.

**Core Innovation**: PDAF introduces cross-ideological populist measurement with salience-weighted tension analysis, enabling researchers to distinguish between coherent populist strategies and strategic overreach where speakers attempt contradictory populist appeals simultaneously.

---

## Analytical Dimensions

### **Primary Populist Core Anchors** (Based on Mudde's minimal definition and Müller's anti-pluralist theory):
1. **Manichaean People-Elite Framing** (0.0-1.0): Moral dichotomy between pure, virtuous people and corrupt, self-serving elites
2. **Crisis-Restoration Temporal Narrative** (0.0-1.0): Decline-crisis-redemption temporal structuring where current crisis stems from elite betrayal
3. **Popular Sovereignty Claims** (0.0-1.0): Direct people's will as ultimate political authority, bypassing representative institutions
4. **Anti-Pluralist Exclusion** (0.0-1.0): Rejection of legitimate opposition and institutional constraints on popular will

### **Populist Mechanism Anchors** (Grounded in mobilization and representation theories):
5. **Elite Conspiracy/Systemic Corruption** (0.0-1.0): Elite coordination against people's interests through hidden networks or institutional capture
6. **Authenticity vs. Political Class** (0.0-1.0): Genuine representation versus professional politician artifice
7. **Homogeneous People Construction** (0.0-1.0): Unified people identity transcending internal divisions of class, region, or interest

### **Boundary Distinction Anchors** (Based on exclusion mechanisms and boundary-drawing research):
8. **Nationalist Exclusion** (0.0-1.0): Cultural/ethnic homogeneity and external threat emphasis that defines populist community boundaries
9. **Economic Populist Appeals** (0.0-1.0): Populist economic discourse regardless of ideological direction

---

## Advanced Analytical Features

### **Salience-Weighted Analysis**
- Captures not just populist intensity but rhetorical emphasis patterns (0.0-1.0 salience scoring)
- Enables distinction between high-intensity/low-salience vs. moderate-intensity/high-salience patterns
- Provides strategic emphasis analysis beyond mere presence detection

### **Populist Strategic Tension Mathematics**
- Quantifies contradictory populist appeals using the formula: `Tension = min(Anchor_A_score, Anchor_B_score) × |Anchor_A_salience - Anchor_B_salience|`
- Measures strategic coherence vs. contradiction across tension pairs
- Enables identification of strategic overreach and rhetorical contradictions

### **Derived Metrics**
- **Strategic Tension Indices**: Democratic-authoritarian, internal-external focus, crisis-elite attribution tensions
- **Populist Strategic Contradiction Index (PSCI)**: Overall measure of strategic coherence vs. contradiction
- **Salience-Weighted Indices**: Core populism, mechanisms, boundary distinctions, and overall populism measures

---

## Analysis Variants

### **Default Analysis**
- Comprehensive single-pass analysis of all nine dimensions
- Ideal for initial exploration and overall assessment
- Provides holistic populist discourse overview

### **Sequential Analysis Variants** (Recommended for highest quality results)
- **Sequential Core Anchors**: Focus on primary populist dimensions
- **Sequential Mechanism Anchors**: Focus on mobilization strategies
- **Sequential Boundary Anchors**: Focus on exclusion and economic appeals

---

## Framework Rationale for Trump Analysis

**Theoretical Foundation**: PDAF is grounded in the ideational approach to populism (Mudde, 2004) that defines populism as a "thin-centered ideology" positing antagonism between virtuous "people" and corrupt "elite."

**Strategic Analysis**: The framework's tension analysis is particularly valuable for Trump's discourse, as it can identify:
- How populist strategies adapt across different political roles
- Strategic coherence vs. contradiction patterns over time
- Evolution of rhetorical emphasis and audience targeting
- Balance between different populist appeals

**Longitudinal Capability**: PDAF's comprehensive dimensional coverage enables robust comparison across different time periods and political contexts, making it ideal for tracking populist rhetoric evolution.

**Cross-Contextual Analysis**: The framework's cross-ideological approach allows for consistent measurement across campaign, governance, and opposition contexts.

---

## Usage in This Experiment

**Primary Application**: Multi-phase populist discourse analysis across Trump's political career  
**Analysis Approach**: Sequential analysis variants for highest quality results  
**Temporal Comparison**: Cross-phase analysis using consistent dimensional measurement  
**Strategic Insights**: Focus on strategic evolution and coherence patterns over time  

**Expected Value**: PDAF will enable comprehensive identification of how Trump's populist strategies evolve across different political roles and contexts, providing insights into populist rhetoric adaptation and strategic coherence.

---

## Machine-Readable Framework Configuration

```yaml
metadata:
  framework_name: "Populist Discourse Analysis Framework"
  framework_version: "10.0"
  author: "PDAF Research Consortium"
  spec_version: "10.0"

analysis_variants:
  default:
    description: "Standard PDAF analysis with all nine dimensions"
    analysis_prompt: "Analyze the provided text using the Populist Discourse Analysis Framework (PDAF) v10.0. Evaluate each of the nine dimensions: Manichaean People-Elite Framing, Crisis-Restoration Narrative, Popular Sovereignty Claims, Anti-Pluralist Exclusion, Elite Conspiracy/Systemic Corruption, Authenticity vs. Political Class, Homogeneous People Construction, Strategic Tension Management, and Salience-Weighted Populist Intensity. For each dimension, provide a raw score (0-10), salience weight (0-1), confidence level (0-1), and supporting evidence."

dimensions:
  - name: "Manichaean People-Elite Framing"
    description: "Binary opposition between virtuous people and corrupt elite"
    markers: ["us vs them", "elite corruption", "people power", "establishment"]
    scoring_calibration: "0.0-0.2: No framing, 0.3-0.4: Weak framing, 0.5-0.6: Moderate framing, 0.7-0.8: Strong framing, 0.9-1.0: Extreme framing"
  
  - name: "Crisis-Restoration Narrative"
    description: "Portrayal of current crisis requiring populist restoration"
    markers: ["crisis", "decline", "restoration", "great again", "save"]
    scoring_calibration: "0.0-0.2: No crisis narrative, 0.3-0.4: Weak crisis, 0.5-0.6: Moderate crisis, 0.7-0.8: Strong crisis, 0.9-1.0: Extreme crisis"
  
  - name: "Popular Sovereignty Claims"
    description: "Appeals to direct popular will and democratic legitimacy"
    markers: ["will of the people", "democracy", "mandate", "voice"]
    scoring_calibration: "0.0-0.2: No sovereignty claims, 0.3-0.4: Weak claims, 0.5-0.6: Moderate claims, 0.7-0.8: Strong claims, 0.9-1.0: Extreme claims"
  
  - name: "Anti-Pluralist Exclusion"
    description: "Exclusion of groups from legitimate political community"
    markers: ["real Americans", "true patriots", "enemies", "traitors"]
    scoring_calibration: "0.0-0.2: No exclusion, 0.3-0.4: Weak exclusion, 0.5-0.6: Moderate exclusion, 0.7-0.8: Strong exclusion, 0.9-1.0: Extreme exclusion"
  
  - name: "Elite Conspiracy/Systemic Corruption"
    description: "Claims of coordinated elite conspiracy against the people"
    markers: ["deep state", "swamp", "rigged", "conspiracy", "corrupt system"]
    scoring_calibration: "0.0-0.2: No conspiracy claims, 0.3-0.4: Weak conspiracy, 0.5-0.6: Moderate conspiracy, 0.7-0.8: Strong conspiracy, 0.9-1.0: Extreme conspiracy"
  
  - name: "Authenticity vs. Political Class"
    description: "Contrast between authentic populist and artificial political class"
    markers: ["authentic", "real", "politician", "outsider", "establishment"]
    scoring_calibration: "0.0-0.2: No authenticity claims, 0.3-0.4: Weak authenticity, 0.5-0.6: Moderate authenticity, 0.7-0.8: Strong authenticity, 0.9-1.0: Extreme authenticity"
  
  - name: "Homogeneous People Construction"
    description: "Construction of unified, homogeneous popular identity"
    markers: ["we the people", "all Americans", "united", "together"]
    scoring_calibration: "0.0-0.2: No homogeneous construction, 0.3-0.4: Weak construction, 0.5-0.6: Moderate construction, 0.7-0.8: Strong construction, 0.9-1.0: Extreme construction"
  
  - name: "Strategic Tension Management"
    description: "Management of tensions between populist claims and political reality"
    markers: ["compromise", "pragmatism", "strategy", "timing"]
    scoring_calibration: "0.0-0.2: No tension management, 0.3-0.4: Weak management, 0.5-0.6: Moderate management, 0.7-0.8: Strong management, 0.9-1.0: Extreme management"
  
  - name: "Salience-Weighted Populist Intensity"
    description: "Overall populist intensity weighted by salience of populist themes"
    markers: ["overall populist tone", "theme prominence", "rhetorical intensity"]
    scoring_calibration: "0.0-0.2: No populist intensity, 0.3-0.4: Weak intensity, 0.5-0.6: Moderate intensity, 0.7-0.8: Strong intensity, 0.9-1.0: Extreme intensity"

output_schema:
  dimensional_scores:
    type: "object"
    properties:
      manichaean_framing:
        type: "object"
        properties:
          raw_score: { type: "number", minimum: 0.0, maximum: 1.0 }
          salience: { type: "number", minimum: 0, maximum: 1 }
          confidence: { type: "number", minimum: 0, maximum: 1 }
          evidence: { type: "string" }
      crisis_restoration:
        type: "object"
        properties:
          raw_score: { type: "number", minimum: 0.0, maximum: 1.0 }
          salience: { type: "number", minimum: 0, maximum: 1 }
          confidence: { type: "number", minimum: 0, maximum: 1 }
          evidence: { type: "string" }
      popular_sovereignty:
        type: "object"
        properties:
          raw_score: { type: "number", minimum: 0.0, maximum: 1.0 }
          salience: { type: "number", minimum: 0, maximum: 1 }
          confidence: { type: "number", minimum: 0, maximum: 1 }
          evidence: { type: "string" }
      anti_pluralist_exclusion:
        type: "object"
        properties:
          raw_score: { type: "number", minimum: 0.0, maximum: 1.0 }
          salience: { type: "number", minimum: 0, maximum: 1 }
          confidence: { type: "number", minimum: 0, maximum: 1 }
          evidence: { type: "string" }
      elite_conspiracy:
        type: "object"
        properties:
          raw_score: { type: "number", minimum: 0.0, maximum: 1.0 }
          salience: { type: "number", minimum: 0, maximum: 1 }
          confidence: { type: "number", minimum: 0, maximum: 1 }
          evidence: { type: "string" }
      authenticity_claims:
        type: "object"
        properties:
          raw_score: { type: "number", minimum: 0.0, maximum: 1.0 }
          salience: { type: "number", minimum: 0, maximum: 1 }
          confidence: { type: "number", minimum: 0, maximum: 1 }
          evidence: { type: "string" }
      homogeneous_people:
        type: "object"
        properties:
          raw_score: { type: "number", minimum: 0.0, maximum: 1.0 }
          salience: { type: "number", minimum: 0, maximum: 1 }
          confidence: { type: "number", minimum: 0, maximum: 1 }
          evidence: { type: "string" }
      strategic_tension:
        type: "object"
        properties:
          raw_score: { type: "number", minimum: 0.0, maximum: 1.0 }
          salience: { type: "number", minimum: 0, maximum: 1 }
          confidence: { type: "number", minimum: 0, maximum: 1 }
          evidence: { type: "string" }
      populist_intensity:
        type: "object"
        properties:
          raw_score: { type: "number", minimum: 0.0, maximum: 1.0 }
          salience: { type: "number", minimum: 0, maximum: 1 }
          confidence: { type: "number", minimum: 0, maximum: 1 }
          evidence: { type: "string" }
```
