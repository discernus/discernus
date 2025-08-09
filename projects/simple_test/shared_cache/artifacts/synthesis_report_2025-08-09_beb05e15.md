# Experiment Report

**Computational Discourse Analysis Synthesis Report**

**Experiment:** democratic_discourse_cohesion_study
**Framework:** Cohesive Flourishing Framework (CFF) v7.3
**Date:** October 26, 2023

This report synthesizes the results of a computational analysis comparing two forms of political discourse: an institutional concession (McCain) and a populist critique (Sanders). The analysis utilized the Cohesive Flourishing Framework v7.3 to measure discourse properties related to social cohesion.

---

### **SECTION 1: HYPOTHESIS TESTING RESULTS**

This section evaluates the three pre-registered hypotheses against the collected statistical evidence.

**H1: Institutional Cohesion**
*Statement: McCain's institutional concession will demonstrate higher overall cohesion indices (dignity, hope, amity, cohesive goals) reflecting democratic norms of gracious transition.*

*   **Finding:** SUPPORTED
*   **Statistical Evidence:** The institutional discourse sample registered higher mean scores on all four specified cohesive metrics compared to the populist discourse sample.
    *   `individual_dignity_score`: Institutional (0.8) vs. Populist (0.2)
    *   `hope_score`: Institutional (0.9) vs. Populist (0.6)
    *   `amity_score`: Institutional (0.9) vs. Populist (0.5)
    *   `cohesive_goals_score`: Institutional (0.9) vs. Populist (0.5)
*   **Reasoning:** The data shows a consistent pattern where the discourse attributed to McCain scored substantially higher on metrics measuring individual dignity, hope, positive relations, and shared objectives.
*   **Limitations:** The analysis is based on a single sample for each discourse type (n=1). The findings describe the characteristics of these specific texts but do not permit statistical generalization to broader categories of discourse.

**H2: Populist Fragmentation**
*Statement: Sanders' populist critique will show higher fragmentative elements (tribal dominance, enmity) but with strategic contradictions indicating sophisticated rhetorical positioning.*

*   **Finding:** SUPPORTED
*   **Statistical Evidence:** The populist discourse sample registered higher scores on the specified fragmentative metrics.
    *   `tribal_dominance_score`: Populist (0.9) vs. Institutional (0.1)
    *   `enmity_score`: Populist (0.9) vs. Institutional (0.1)
    *   The populist sample also registered non-zero scores on cohesive metrics, such as `hope_score` (0.6) and `amity_score` (0.5), concurrently with high fragmentative scores.
*   **Reasoning:** The first part of the hypothesis is supported by the higher scores in tribal dominance and enmity for the discourse attributed to Sanders. The second part is supported by the co-occurrence of high fragmentative scores with moderate cohesive scores, a pattern indicative of a mixed rhetorical appeal.
*   **Limitations:** The sample size is n=1 for each discourse type. The interpretation of co-occurring scores as a "strategic contradiction" is an analytic inference based on the framework's design.

**H3: Democratic Patterns**
*Statement: The two discourse types will exhibit distinct social cohesion signatures corresponding to institutional versus populist democratic approaches.*

*   **Finding:** SUPPORTED
*   **Statistical Evidence:** The overall scoring profiles for the two discourse samples are distinct and show contrasting patterns across multiple CFF dimensions.
    *   **Institutiona

l Profile:** Characterized by high scores on cohesive metrics (`individual_dignity_score`: 0.8, `hope_score`: 0.9, `amity_score`: 0.9, `cohesive_goals_score`: 0.9) and low scores on fragmentative metrics (`tribal_dominance_score`: 0.1, `fear_score`: 0.2, `enmity_score`: 0.1).
    *   **Populist Profile:** Characterized by high scores on fragmentative metrics (`tribal_dominance_score`: 0.9, `fear_score`: 0.8, `envy_score`: 0.85, `enmity_score`: 0.9) and moderate-to-low scores on cohesive metrics.
*   **Reasoning:** The data reveals two divergent signatures. The institutional discourse consistently scores high on cohesion and low on fragmentation. The populist discourse shows an inverse pattern, scoring high on fragmentation and comparatively lower on cohesion.
*   **Limitations:** With a single text representing each category (n=1), these distinct signatures apply only to the specific samples analyzed and cannot be generalized.

---

### **SECTION 2: ADDITIONAL PATTERNS IN THE DATA**

Further examination of the statistical results reveals additional patterns not explicitly covered by the primary hypotheses.

**1. Inverse Scoring within Core CFF Dimensions**
Across several core dimensions of the CFF, the two discourse types exhibit near-inverse scoring patterns.
*   **Identity Dimension:** The institutional discourse shows a low `tribal_dominance_score` (0.1) and a high `individual_dignity_score` (0.8). The populist discourse shows the reverse: a high `tribal_dominance_score` (0.9) and a low `individual_dignity_score` (0.2).
*   **Success Orientation Dimension:** The institutional discourse registers a `compersion_score` of 0.9 and an `envy_score` of 0.0. The populist discourse shows a `compersion_score` of 0.0 and an `envy_score` of 0.85.
*   **Relational Dimension:** The institutional discourse has a low `enmity_score` (0.1) and a high `amity_score` (0.9). The populist discourse has a high `enmity_score` (0.9) and a moderate `amity_score` (0.5). This pattern suggests the framework's oppositional constructs effectively differentiate these two communication styles.

**2. Contrasting Emotional Climates**
The data indicates a clear divergence in the emotional framing of the two discourses, as measured by the Fear/Hope dimension.
*   The institutional discourse is characterized by a high `hope_score` (0.9) and a low `fear_score` (0.2).
*   Conversely, the populist discourse is characterized by a high `fear_score` (0.8) and a moderate `hope_score` (0.6).
*   This pattern shows that while both discourses utilize appeals to hope, the populist sample does so alongside a dominant appeal to fear, whereas the institutional sample pairs hope with a low presence of fear.

**3. Salience and Score Correspondence in Institutional Discourse**
For the institutional discourse sample, there is a strong correspondence between high scores on cohesive metrics and high salience values for those same metrics.
*   **Hope:** `hope_score` (0.9) and `hope_salience` (0.9)
*   **Amity:** `amity_score` (0.9) and `amity_salience` (0.9)
*   **Cohesive Goals:** `cohesive_goals_score` (0.9) and `cohesive_goals_salience` (0.9)
This indicates that the themes the model scored as most prevalent were also identified as being most central to the discourse. A corresponding analysis for the populist discourse was not possible due to incomplete salience data in the provided evidence base.

## Technical Transparency
**Investigation Log**: 15 evidence queries performed
**Models Used**: Synthesis: vertex_ai/gemini-2.5-pro
**Evidence Interrogation**: Active RAG-powered investigation
