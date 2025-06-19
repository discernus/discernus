# Civic Virtue Framework

**Version:** v2025.06.17  
**Status:** Production Ready  
**Framework Type:** Clustered Wells  

## Overview

The Civic Virtue Framework analyzes moral dimensions of persuasive political discourse through classical virtue ethics and contemporary civic republican theory. It identifies dimensions that strengthen or weaken democratic discourse and civic engagement using clustered positioning around a vertical moral hierarchy.

## Theoretical Foundation

Based on Aristotelian virtue ethics and contemporary civic republican theory, this framework examines civic virtues and vices in political communication:

- **Classical Foundation:** Aristotle's *Nicomachean Ethics* (Book VI) on virtue and character
- **Contemporary Application:** Sandel's civic republican theory on moral limits and civic engagement
- **Core Insight:** Democratic discourse quality depends on the balance of civic virtues versus civic vices

## Framework Architecture

### **Clustered Wells Structure**
- **Virtue Cluster (Top):** 5 wells clustered around 90° emphasizing civic strengths
- **Vice Cluster (Bottom):** 5 wells clustered around 270° emphasizing civic weaknesses
- **Moral Hierarchy:** Vertical orientation emphasizing virtue-vice distinction

### **Civic Virtues (Integrative Wells)**
1. **Dignity** (90°, weight: 1.0) - Individual moral worth and universal human dignity
2. **Truth** (75°, weight: 0.8) - Factual accuracy and intellectual honesty
3. **Justice** (105°, weight: 0.8) - Fairness, proportionality, and procedural equity
4. **Hope** (60°, weight: 0.6) - Constructive vision and democratic optimism
5. **Pragmatism** (120°, weight: 0.6) - Practical solutions and workable compromise

### **Civic Vices (Disintegrative Wells)**
1. **Tribalism** (270°, weight: 1.0) - Group loyalty over universal principles
2. **Resentment** (255°, weight: 0.8) - Grievance, victimization, and blame
3. **Manipulation** (285°, weight: 0.8) - Deceptive rhetoric and emotional exploitation
4. **Fear** (240°, weight: 0.6) - Anxiety appeals and catastrophic thinking
5. **Fantasy** (300°, weight: 0.6) - Unrealistic expectations and magical thinking

## Key Features

### **Clustered Positioning**
- Wells clustered by moral orientation rather than random distribution
- 60° span for each cluster with even distribution within arcs
- Clear separation between virtue and vice orientations

### **Hierarchical Weighting**
- **Primary** (1.0): Dignity and Tribalism - fundamental civic dimensions
- **Secondary** (0.8): Truth, Justice, Resentment, Manipulation - important civic impact
- **Tertiary** (0.6): Hope, Pragmatism, Fear, Fantasy - supporting dimensions

### **Analysis Capabilities**
- Civic discourse quality assessment
- Virtue-vice balance measurement
- Democratic engagement impact analysis
- Character dimension identification in political communication

## Usage Guidelines

### **Ideal Applications**
- Political speech analysis for civic virtue content
- Democratic discourse quality assessment
- Campaign communication ethics evaluation
- Public debate moral dimension analysis

### **Scoring Approach**
- Each well scored 0.0-1.0 based on presence/strength in text
- Specific textual evidence required for each score
- Cluster-based analysis considering virtue vs. vice balance
- Overall civic discourse quality metrics

### **Interpretation Framework**
- **High Virtue Cluster Scores:** Strengthens democratic discourse and civic engagement
- **High Vice Cluster Scores:** Undermines democratic discourse and civic participation
- **Balanced Patterns:** Mixed civic impact requiring detailed analysis
- **Cluster Dominance:** Clear moral orientation toward virtue or vice

## Academic Foundation

### **Theoretical Validation**
- Grounded in classical virtue ethics tradition
- Supported by contemporary civic republican theory
- Validated through democratic discourse research
- Aligned with political communication ethics standards

### **Research Applications**
- Democratic discourse health measurement
- Political communication ethics assessment
- Civic engagement impact evaluation
- Character-based political analysis

### **Quality Metrics**
- Center of mass calculation for overall civic orientation
- Narrative polarity score for civic orientation strength
- Directional purity score for virtue-vice clarity
- Virtue dominance index for cluster balance assessment

## Technical Specifications

### **Coordinate System**
- Circular geometry with 1.0 radius
- 0.8 scaling factor for visualization
- Cluster-based center of mass calculation
- Arc-bounded positioning strategy

### **Compatibility**
- Prompt templates: clustered_wells_v1.0, civic_virtue_v2.1
- Calculation methods: clustered_center_of_mass
- API versions: v2.1
- Visualization types: circular, clustered

---

**File Structure:**
```
civic_virtue/
├── framework.yaml          # Main framework specification
├── README.md               # This documentation
└── archive/                # Archived legacy JSON files
    ├── framework.json      # Original JSON format
    ├── dipoles.json        # Legacy dipole definitions
    ├── weights.json        # Legacy weighting scheme
    └── *.backup.*          # Historical backups
```

**Next Steps:** Framework ready for integration with production systems and validation experiments. 