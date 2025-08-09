# Experiment Report

### **Computational Discourse Analysis Synthesis Report**

**Experiment:** democratic_discourse_cohesion_study
**Framework:** Cohesive Flourishing Framework (CFF) v7.3
**Date:** October 26, 2023

This report synthesizes the results of a computational analysis comparing two forms of political discourse: an institutional concession speech (McCain, 2008) and a populist critique speech (Sanders, 2025). The analysis utilized the Cohesive Flourishing Framework v7.3 to measure social cohesion and fragmentation indicators.

---

### **SECTION 1: HYPOTHESIS TESTING RESULTS**

This section evaluates the three pre-registered hypotheses against the collected statistical evidence.

---

#### **H1: Institutional Cohesion**
*Statement: McCain's institutional concession will demonstrate higher overall cohesion indices (dignity, hope, amity, cohesive goals) reflecting democratic norms of gracious transition.*

**Finding: SUPPORTED**

**Reasoning:**
The quantitative data shows that the institutional discourse sample scored higher than the populist sample on all specified cohesive metrics. The Overall Cohesion Index for the institutional text was 0.74, compared to -0.32 for the populist text.

**Statistical Evidence:**
*   **Individual Dignity Score:** Institutional 0.8 vs. Populist 0.2
*   **Hope Score:** Institutional 0.9 vs. Populist 0.6
*   **Amity Score:** Institutional 0.9 vs. Populist 0.5
*   **Cohesive Goals Score:** Institutional 0.9 vs. Populist 0.5

**Textual Evidence Context:**
The high `amity_score` (0.9) corresponds to framework definitions of amity that include "friendship appeals, cooperative framing, recognition of shared interests across political differences that strengthens democratic culture" [14].

**Limitations:**
The analysis is based on a single text for each discourse category (`count: 1`). The findings may not be generalizable to all institutional or populist discourse. The framework itself notes potential for cultural, ideological, and selection bias [1].

---

#### **H2: Populist Fragmentation**
*Statement: Sanders' populist critique will show higher fragmentative elements (tribal dominance, enmity) but with strategic contradictions indicating sophisticated rhetorical positioning.*

**Finding: SUPPORTED**

**Reasoning:**
The populist discourse sample registered substantially higher scores on fragmentative metrics. The Fragmentative Index for the populist text was 0.84, compared to 0.1 for the institutional text. Furthermore, the populist text exhibited a higher Strategic Contradiction Index (SCI), which quantifies the use of opposing rhetorical appeals.

**Statistical Evidence:**
*   **Tribal Dominance Score:** Populist 0.9 vs. Institutional 0.1
*   **Enmity Score:** Populist 0.9 vs. Institutional 0.1
*   **Fragmentative Goals Score:** Populist 0.75 vs. Institutional 0.1
*   **Strategic Contradiction Index (SCI):** Populist 0.122 vs. Institutional 0.072

**Textual Evidence Context:**
The high scores for `tribal_dominance` and `enmity` align with CFF definitions that look for concepts such as "In-group supremacy," "us vs them" [6] and "Hostility language," "Demonization patterns" [5]. A higher SCI is associated with the "Deliberate deployment of opposing appeals for complex rhetorical effects" [27].

**Limitations:**
This finding is based on one text per category. The higher SCI value is a relative difference and its rhetorical significance is a matter for qualitative interpretation.

---

#### **H3: Democratic Patterns**


*Statement: The two discourse types will exhibit distinct social cohesion signatures corresponding to institutional versus populist democratic approaches.*

**Finding: SUPPORTED**

**Reasoning:**
The quantitative profiles of the two texts are markedly different across the CFF dimensions. The institutional text is characterized by high cohesive scores (mean 0.88) and low fragmentative scores (mean 0.1). The populist text shows the inverse pattern, with high fragmentative scores (mean 0.84) and lower, more varied cohesive scores (mean 0.36). This demonstrates distinct, measurable signatures.

**Statistical Evidence:**
*   **Institutional Profile:** High scores in `individual_dignity` (0.8), `hope` (0.9), `amity` (0.9), and `cohesive_goals` (0.9).
*   **Populist Profile:** High scores in `tribal_dominance` (0.9), `fear` (0.8), `enmity` (0.9), and `fragmentative_goals` (0.75).
*   **Overall Cohesion Index:** Institutional 0.74 vs. Populist -0.32.

**Textual Evidence Context:**
The CFF is designed to produce these distinct signatures. The framework's methodology states that "Dynamic Salience Weighting... enables distinction between texts with similar dimension scores but fundamentally different rhetorical strategies" [2], providing a mechanism for identifying such patterns.

**Limitations:**
The two texts analyzed represent paradigmatic examples and may show clearer distinctions than would be found in a larger, more varied sample of political discourse. The representativeness of these signatures for the broader categories of "institutional" and "populist" discourse is not established by this analysis.

---

### **SECTION 2: ADDITIONAL PATTERNS IN THE DATA**

Further examination of the statistical output reveals additional patterns.

---

#### **Pattern 1: Inverse Relationship Between Cohesive and Fragmentative Dimensions**

A strong inverse relationship was observed between cohesive and fragmentative scores for each text. The institutional text paired a high Salience-Weighted Cohesive Index (0.883) with a low Salience-Weighted Fragmentative Index (0.14). Conversely, the populist text paired a high Salience-Weighted Fragmentative Index (0.843) with a lower Salience-Weighted Cohesive Index (0.522). This pattern is consistent with the framework's oppositional dimensions, such as `amity` vs. `enmity` and `hope` vs. `fear`.

**Statistical Evidence:**
*   **Institutional:** Salience-Weighted Cohesive Index = 0.883; Salience-Weighted Fragmentative Index = 0.14
*   **Populist:** Salience-Weighted Cohesive Index = 0.522; Salience-Weighted Fragmentative Index = 0.843

---

#### **Pattern 2: Distribution of Rhetorical Tension Scores**

The analysis of rhetorical tension, calculated as `min(Dimension_A_score, Dimension_B_score) × |Salience_A - Salience_B|` [18], did not uniformly favor one discourse type. The populist discourse showed higher tension in the Identity (0.17 vs. 0.06) and Emotional (0.14 vs. 0.09) dimensions. However, the institutional discourse registered higher tension in the Relational (0.25 vs. 0.08) and Goal (0.10 vs. 0.08) dimensions. This indicates that both texts contain rhetorical tension, but it manifests in different psychological dimensions.

**Statistical Evidence:**
*   **Identity Tension:** Populist (0.17) > Institutional (0.06)
*   **Emotional Tension:** Populist (0.14) > Institutional (0.09)
*   **Relational Tension:** Institutional (0.25) > Populist (0.08)
*   **Goal Tension:** Institutional (0.10) > Populist (0.08)

## Technical Transparency
**Investigation Log**: 15 evidence queries performed
**Models Used**: Synthesis: vertex_ai/gemini-2.5-pro
**Evidence Interrogation**: Active RAG-powered investigation
