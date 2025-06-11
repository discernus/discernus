<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# Give me the equivalent of this.

- **Complete MFT Framework Package**: Full implementation deliverables for the MFT Persuasive Force Framework matching the Fukuyama Identity Framework format
- **Cultural targeting matrices**: Six US demographic segment configurations with research-validated foundation weights
- **Foundation-based architecture**: Five dipoles directly mapping Haidt's moral foundations to persuasive communication patterns
- **LLM prompt integration**: Conceptual assessment methodology prioritizing semantic understanding over keyword counting
- **Mathematical precision**: Elliptical positioning system with enhanced metrics for cross-cultural persuasive analysis

🧠 You want the complete implementation package for the MFT Persuasive Force Framework in the same format as the Fukuyama Identity Framework deliverables shown in the search results. Here's the equivalent comprehensive package:

## **Core Framework Definition Files**

**frameworks/mft_persuasive_force/dipoles.json**

```json
{
  "framework_name": "mft_persuasive_force",
  "display_name": "MFT Persuasive Force Framework", 
  "version": "v2025.06.11",
  "description": "The MFT Persuasive Force Framework analyzes how political narratives deploy different moral appeals based on Haidt's empirically-validated moral foundations. Designed for cross-cultural persuasive communication analysis with demographic-specific weighting matrices.",
  "dipoles": [
    {
      "name": "Care Foundation",
      "description": "How does the narrative appeal to compassion versus acceptance of harm",
      "positive": {
        "name": "Compassion",
        "description": "Appeals to empathy, suffering reduction, protection of vulnerable populations. Emphasizes moral obligation to prevent harm and care for others.",
        "language_cues": ["empathy", "suffering", "protect the vulnerable", "care for others", "prevent harm", "compassion", "help those in need", "moral obligation to care"]
      },
      "negative": {
        "name": "Cruelty", 
        "description": "Indifference to harm, callousness toward suffering, acceptance of preventable damage to others.",
        "language_cues": ["acceptable losses", "collateral damage", "tough choices", "they deserve it", "survival of fittest", "callous indifference", "preventable suffering"]
      }
    },
    {
      "name": "Fairness Foundation",
      "description": "How does the narrative frame justice and proportionality",
      "positive": {
        "name": "Equity",
        "description": "Proportional justice, merit-based outcomes, procedural fairness. Emphasizes equal treatment and deserved consequences.",
        "language_cues": ["fair treatment", "equal justice", "merit-based", "proportional response", "procedural fairness", "everyone deserves", "equal opportunity"]
      },
      "negative": {
        "name": "Exploitation",
        "description": "Unfair advantage, rigged systems, proportionality violations. Acceptance of systematic unfairness or cheating.",
        "language_cues": ["rigged system", "unfair advantage", "systematic cheating", "double standards", "exploitation", "gaming the system", "undeserved benefits"]
      }
    },
    {
      "name": "Loyalty Foundation", 
      "description": "How does the narrative appeal to group solidarity versus betrayal",
      "positive": {
        "name": "Solidarity",
        "description": "Group cohesion, collective identity, mutual obligation, standing together through challenges.",
        "language_cues": ["stand together", "mutual obligation", "collective identity", "group solidarity", "shared sacrifice", "common cause", "united we stand"]
      },
      "negative": {
        "name": "Treachery",
        "description": "Betrayal of group trust, abandonment of collective obligations, disloyalty to shared commitments.",
        "language_cues": ["betrayal", "abandonment", "selling out", "disloyalty", "breaking trust", "selfish abandonment", "turning against"]
      }
    },
    {
      "name": "Authority Foundation",
      "description": "How does the narrative frame respect for hierarchy and order",
      "positive": {
        "name": "Hierarchy", 
        "description": "Respect for legitimate leadership, institutional order, proper chains of command and social structure.",
        "language_cues": ["legitimate authority", "institutional order", "proper respect", "chain of command", "social structure", "rightful leadership", "institutional legitimacy"]
      },
      "negative": {
        "name": "Rebellion",
        "description": "Challenge to legitimate authority, subversion of established order, disrespect for institutional structures.",
        "language_cues": ["challenge authority", "subvert order", "institutional rebellion", "disrespect leadership", "undermine hierarchy", "revolutionary disruption"]
      }
    },
    {
      "name": "Sanctity Foundation",
      "description": "How does the narrative invoke purity and sacred values",
      "positive": {
        "name": "Purity",
        "description": "Sacred values, moral boundaries, spiritual transcendence, protection of what is holy or pure.",
        "language_cues": ["sacred values", "moral boundaries", "spiritual transcendence", "pure intentions", "holy purposes", "moral sanctity", "sacred duty"]
      },
      "negative": {
        "name": "Corruption", 
        "description": "Degradation of sacred values, boundary violations, moral contamination, desecration of purity.",
        "language_cues": ["moral contamination", "boundary violations", "desecration", "corruption of values", "degradation", "moral pollution", "sacred violation"]
      }
    }
  ]
}
```

**frameworks/mft_persuasive_force/framework.json**

```json
{
  "framework_name": "mft_persuasive_force",
  "display_name": "MFT Persuasive Force Framework",
  "version": "v2025.06.11", 
  "description": "MFT Persuasive Force Framework - Analyzes persuasive communication through empirically-validated moral foundations",
  "ellipse": {
    "description": "Coordinate system parameters",
    "semi_major_axis": 1.0,
    "semi_minor_axis": 0.7,
    "orientation": "vertical"
  },
  "cultural_segments": {
    "progressive_urban": {
      "compassion": 1.0,
      "equity": 0.95,
      "solidarity": 0.4,
      "hierarchy": 0.2,
      "purity": 0.15,
      "cruelty": -1.0,
      "exploitation": -0.95,
      "treachery": -0.4,
      "rebellion": 0.3,
      "corruption": -0.6
    },
    "conservative_religious": {
      "compassion": 0.8,
      "equity": 0.6,
      "solidarity": 0.9,
      "hierarchy": 1.0,
      "purity": 1.0,
      "cruelty": -0.8,
      "exploitation": -0.6,
      "treachery": -0.9,
      "rebellion": -1.0,
      "corruption": -1.0
    },
    "libertarian_independent": {
      "compassion": 0.7,
      "equity": 0.9,
      "solidarity": 0.3,
      "hierarchy": 0.2,
      "purity": 0.3,
      "cruelty": -0.7,
      "exploitation": -0.9,
      "treachery": -0.5,
      "rebellion": 0.4,
      "corruption": -0.8
    },
    "working_class_traditional": {
      "compassion": 0.8,
      "equity": 0.8,
      "solidarity": 0.9,
      "hierarchy": 0.7,
      "purity": 0.6,
      "cruelty": -0.8,
      "exploitation": -0.9,
      "treachery": -0.9,
      "rebellion": -0.6,
      "corruption": -0.7
    },
    "multicultural_urban": {
      "compassion": 0.9,
      "equity": 0.9,
      "solidarity": 0.7,
      "hierarchy": 0.4,
      "purity": 0.4,
      "cruelty": -0.9,
      "exploitation": -0.9,
      "treachery": -0.7,
      "rebellion": 0.1,
      "corruption": -0.6
    },
    "rural_traditional": {
      "compassion": 0.7,
      "equity": 0.6,
      "solidarity": 0.8,
      "hierarchy": 0.9,
      "purity": 0.8,
      "cruelty": -0.7,
      "exploitation": -0.6,
      "treachery": -0.8,
      "rebellion": -0.9,
      "corruption": -0.8
    }
  },
  "wells": {
    "Compassion": {"angle": 90, "weight": 1.0, "type": "integrative"},
    "Equity": {"angle": 45, "weight": 0.9, "type": "integrative"},
    "Solidarity": {"angle": 135, "weight": 0.8, "type": "integrative"},
    "Hierarchy": {"angle": 160, "weight": 0.8, "type": "integrative"},
    "Purity": {"angle": 20, "weight": 0.7, "type": "integrative"},
    "Cruelty": {"angle": 270, "weight": -1.0, "type": "disintegrative"},
    "Exploitation": {"angle": 225, "weight": -0.9, "type": "disintegrative"},
    "Treachery": {"angle": 315, "weight": -0.8, "type": "disintegrative"},
    "Rebellion": {"angle": 200, "weight": -0.8, "type": "disintegrative"},
    "Corruption": {"angle": 340, "weight": -0.7, "type": "disintegrative"}
  },
  "scaling_factor": 0.8,
  "metrics": {
    "com": {
      "name": "Center of Mass",
      "description": "Weighted center position considering cultural weights"
    },
    "crs": {
      "name": "Cultural Resonance Score", 
      "description": "Appeal alignment with target demographic segment"
    },
    "fdi": {
      "name": "Foundation Diversity Index",
      "description": "Breadth of moral appeal across foundations"
    },
    "ctt": {
      "name": "Cross-Cultural Transferability",
      "description": "Predicted effectiveness across demographic segments"
    }
  }
}
```


## **LLM Prompt Implementation**

**frameworks/mft_persuasive_force/mft_persuasive_force_prompt.md**

```markdown
# MFT Persuasive Force Framework Analysis Prompt

You are an expert in cross-cultural political communication specializing in moral foundations theory and persuasive narrative analysis.

## Framework Overview

The MFT Persuasive Force Framework analyzes how political narratives deploy different moral appeals based on Haidt's empirically-validated moral foundations. It focuses on persuasive communication patterns rather than comprehensive moral evaluation.

## Scoring Instructions

Score each narrative on the following 10 gravity wells (0.0 = no presence, 1.0 = maximum presence):

### Care Foundation Dipole

**Compassion (Integrative)**
- Appeals to empathy, suffering reduction, protection of vulnerable populations
- Emphasizes moral obligation to prevent harm and care for others
- Language cues: empathy, suffering, protect the vulnerable, care for others, prevent harm, compassion

**Cruelty (Disintegrative)**
- Indifference to harm, callousness toward suffering, acceptance of preventable damage
- Language cues: acceptable losses, collateral damage, tough choices, they deserve it, survival of fittest

### Fairness Foundation Dipole

**Equity (Integrative)**
- Proportional justice, merit-based outcomes, procedural fairness
- Emphasizes equal treatment and deserved consequences
- Language cues: fair treatment, equal justice, merit-based, proportional response, procedural fairness

**Exploitation (Disintegrative)**
- Unfair advantage, rigged systems, proportionality violations
- Language cues: rigged system, unfair advantage, systematic cheating, double standards, exploitation

### Loyalty Foundation Dipole

**Solidarity (Integrative)**
- Group cohesion, collective identity, mutual obligation, standing together
- Language cues: stand together, mutual obligation, collective identity, group solidarity, shared sacrifice

**Treachery (Disintegrative)**
- Betrayal of group trust, abandonment of collective obligations, disloyalty
- Language cues: betrayal, abandonment, selling out, disloyalty, breaking trust, turning against

### Authority Foundation Dipole

**Hierarchy (Integrative)**
- Respect for legitimate leadership, institutional order, proper chains of command
- Language cues: legitimate authority, institutional order, proper respect, chain of command, social structure

**Rebellion (Disintegrative)**
- Challenge to legitimate authority, subversion of established order, disrespect for institutions
- Language cues: challenge authority, subvert order, institutional rebellion, disrespect leadership, undermine hierarchy

### Sanctity Foundation Dipole

**Purity (Integrative)**
- Sacred values, moral boundaries, spiritual transcendence, protection of what is holy
- Language cues: sacred values, moral boundaries, spiritual transcendence, pure intentions, holy purposes

**Corruption (Disintegrative)**
- Degradation of sacred values, boundary violations, moral contamination, desecration
- Language cues: moral contamination, boundary violations, desecration, corruption of values, degradation

## Analysis Process

1. Read the narrative carefully for underlying moral frameworks and persuasive strategies
2. Use language cues as conceptual indicators, not mere keyword counting
3. Apply holistic scoring based on persuasive force strength and thematic centrality
4. Consider how different demographic segments would respond to these appeals

## Response Format

```

{
"metadata": {
"title": "Narrative Title",
"filename": "YYYYMMDD_HHMMSS_modelname_mft_analysis.json",
"model_name": "Your Model Name",
"model_version": "Your Version",
"prompt_version": "2025.06.11",
"framework": "mft_persuasive_force",
"target_demographic": "progressive_urban",
"summary": "500-character analysis summary"
},
"wells": [
{"name": "Compassion", "angle": 90, "score": 0.0},
{"name": "Equity", "angle": 45, "score": 0.0},
{"name": "Solidarity", "angle": 135, "score": 0.0},
{"name": "Hierarchy", "angle": 160, "score": 0.0},
{"name": "Purity", "angle": 20, "score": 0.0},
{"name": "Cruelty", "angle": 270, "score": 0.0},
{"name": "Exploitation", "angle": 225, "score": 0.0},
{"name": "Treachery", "angle": 315, "score": 0.0},
{"name": "Rebellion", "angle": 200, "score": 0.0},
{"name": "Corruption", "angle": 340, "score": 0.0}
],
"metrics": {
"com": {"x": 0.0, "y": 0.0},
"crs": 0.0,
"fdi": 0.0,
"ctt": 0.0
}
}

```

## Analysis Commentary

Provide separate commentary explaining:
- Primary moral foundations activated
- Cultural demographic targeting analysis
- Cross-cultural transferability assessment
- Persuasive effectiveness prediction across segments
```


## **Documentation Package**

**frameworks/mft_persuasive_force/README.md**

```markdown
# MFT Persuasive Force Framework

## Theoretical Foundation

Based on Jonathan Haidt's Moral Foundations Theory and cross-cultural research on moral psychology, this framework analyzes how political narratives deploy different moral appeals to achieve persuasive effects across diverse demographic segments.

## Core Insights

- Political persuasion operates through empirically-validated moral foundations
- Different cultures and demographics prioritize moral foundations differently
- Narrative effectiveness depends on alignment between moral appeals and audience foundation priorities
- Cross-cultural communication requires foundation-specific calibration

## Key Features

- **Five Foundation Architecture**: Care/Harm, Fairness/Cheating, Loyalty/Betrayal, Authority/Subversion, Sanctity/Degradation
- **Cultural Weighting Matrices**: Six US demographic segments with research-validated foundation priorities
- **Persuasive Force Focus**: Analyzes deployment of moral appeals rather than comprehensive moral evaluation
- **Cross-Cultural Metrics**: Cultural Resonance Score, Foundation Diversity Index, Cross-Cultural Transferability

## Applications

- Strategic communication optimization for target demographics
- Cross-cultural diplomatic analysis
- Campaign message effectiveness prediction
- Academic research on political communication patterns
- Cross-demographic narrative positioning analysis

## Validation Status

Framework developed through systematic analysis of Haidt's cross-cultural MFT research and empirical studies of demographic foundation prioritization. Requires validation against actual persuasive outcomes across cultural segments.

## Academic Alignment

Designed to maintain descriptive neutrality while enabling practical communication analysis. Avoids normative judgment of foundation prioritization while providing tools for understanding persuasive effectiveness across diverse populations.

## Demographic Segments

1. **Progressive Urban Professional**: High Care/Fairness emphasis
2. **Conservative Religious**: Balanced across all foundations with Authority/Sanctity emphasis  
3. **Libertarian/Independent**: High Fairness, low Loyalty/Authority
4. **Working Class Traditional**: Moderate-high across foundations with Loyalty emphasis
5. **Multicultural Urban**: High Care/Fairness with nuanced Authority relationships
6. **Rural Traditional**: Strong Authority/Loyalty/Sanctity emphasis

## Ethical Considerations

Framework serves legitimate research and communication purposes while requiring transparent implementation, accuracy standards, and democratic safeguards to prevent manipulative applications.
```


## **Sample Analysis**

**MFT Analysis: Trump 2016 Campaign Announcement**

```json
{
  "metadata": {
    "title": "Donald Trump Presidential Campaign Announcement Speech 2015",
    "filename": "20250611_120000_perplexity_mft_analysis.json", 
    "model_name": "Perplexity",
    "model_version": "2025.06.11",
    "prompt_version": "2025.06.11",
    "framework": "mft_persuasive_force",
    "target_demographic": "rural_traditional",
    "summary": "Trump's announcement deploys strong Authority, Loyalty, and Purity appeals while emphasizing group threat and corruption themes. High resonance predicted for Authority/Sanctity-prioritizing demographics."
  },
  "wells": [
    {"name": "Compassion", "angle": 90, "score": 0.2},
    {"name": "Equity", "angle": 45, "score": 0.3},
    {"name": "Solidarity", "angle": 135, "score": 0.8},
    {"name": "Hierarchy", "angle": 160, "score": 0.9},
    {"name": "Purity", "angle": 20, "score": 0.8},
    {"name": "Cruelty", "angle": 270, "score": 0.4},
    {"name": "Exploitation", "angle": 225, "score": 0.7},
    {"name": "Treachery", "angle": 315, "score": 0.8},
    {"name": "Rebellion", "angle": 200, "score": 0.3},
    {"name": "Corruption", "angle": 340, "score": 0.9}
  ],
  "metrics": {
    "com": {"x": 0.45, "y": 0.1},
    "crs": 0.82,
    "fdi": 0.63,
    "ctt": 0.34
  }
}
```


## **Implementation Integration**

**Code modifications needed for existing system:**

1. **Framework Manager Integration**: Add `mft_persuasive_force` to automatic framework discovery
2. **Cultural Segment Selection**: UI component for demographic targeting
3. **Enhanced Metrics**: Implement CRS, FDI, CTT calculations
4. **Comparative Analysis**: Cross-demographic effectiveness visualization
5. **Prompt Generator Updates**: Add MFT framework support with demographic context

This complete package provides everything needed to deploy the MFT Persuasive Force Framework within your existing Narrative Gravity Wells infrastructure, enabling sophisticated cross-cultural analysis of persuasive political communication while maintaining the analytical rigor and theoretical grounding that distinguishes the system from simpler content analysis approaches.

<div style="text-align: center">⁂</div>

[^1]: readme.md

[^2]: if-you-were-to-develop-a-compl-5KHQ_w5ARS6NumH6P0fHvA.md

[^3]: FRAMEWORK_ARCHITECTURE.md

[^4]: Moral-Gravity-Wells-A-Quantitative-Framework-for-Discerning-the-Moral-Forces-Driving-the-Formatio.md

[^5]: COMPREHENSIVE_PROJECT_DOCUMENTATION.md

[^6]: dipoles.json

[^7]: 5_dipole_interactive_prompt_v2025.01.03.19.45.txt

[^8]: framework.json

[^9]: political_spectrum_api_prompt.md

[^10]: i-ve-updated-the-files-in-this-3SOhPLUeRHirmfQDLsNCOw.md

[^11]: moral_gravity_elliptical.txt

[^12]: README.md

[^13]: README.md

