# Experiment Report

### **Computational Discourse Analysis Synthesis Report**

**Experiment:** democratic_discourse_cohesion_study
**Framework:** Cohesive Flourishing Framework (CFF) v7.3
**Date:** 2023-10-27

This report presents the statistical findings from a comparative analysis of two political discourse styles: institutional concession (McCain) and populist critique (Sanders). The analysis utilized the Cohesive Flourishing Framework v7.3 to quantify patterns related to social cohesion.

---

### **SECTION 1: HYPOTHESIS TESTING RESULTS**

#### **H1: Institutional Cohesion**
*Statement: McCain's institutional concession will demonstrate higher overall cohesion indices (dignity, hope, amity, cohesive goals) reflecting democratic norms of gracious transition.*

**Finding: SUPPORTED**

**Reasoning:**
The quantitative data shows that the institutional discourse scored consistently higher on all specified cohesive metrics when compared to the populist discourse. The `overall_cohesion_index` for the institutional discourse was 0.743, in contrast to -0.321 for the populist discourse.

**Statistical Evidence:**
*   **Individual Dignity Score:** Institutional: 0.8 vs. Populist: 0.2
*   **Hope Score:** Institutional: 0.9 vs. Populist: 0.6
*   **Amity Score:** Institutional: 0.9 vs. Populist: 0.5
*   **Cohesive Goals Score:** Institutional: 0.9 vs. Populist: 0.5
*   The derived `cohesive_index` was 0.88 for the institutional discourse, compared to 0.36 for the populist discourse.

**Textual Correlates:**
The high `amity_score` (0.9) in the institutional discourse corresponds to the CFF's definition of amity, which includes "friendship appeals, cooperative framing, recognition of shared interests across political differences" [14].

**Limitations:**
The analysis is based on a single text for each discourse type (n=1 per category). The findings reflect the characteristics of these specific examples and may not be generalizable to all institutional or populist discourse.

---

#### **H2: Populist Fragmentation**
*Statement: Sanders' populist critique will show higher fragmentative elements (tribal dominance, enmity) but with strategic contradictions indicating sophisticated rhetorical positioning.*

**Finding: SUPPORTED**

**Reasoning:**
The populist discourse registered substantially higher scores on fragmentative metrics. Concurrently, its `strategic_contradiction_index` (SCI) was higher than that of the institutional discourse, supporting the second part of the hypothesis.

**Statistical Evidence:**
*   **Fragmentative Elements:**
    *   **Tribal Dominance Score:** Populist: 0.9 vs. Institutional: 0.1
    *   **Enmity Score:** Populist: 0.9 vs. Institutional: 0.1
    *   The derived `fragmentative_index` was 0.84 for the populist discourse, compared to 0.1 for the institutional discourse.
*   **Strategic Contradiction:**
    *   The `strategic_contradiction_index` for the populist discourse was 0.122, while the institutional discourse scored 0.072.

**Textual Correlates:**
The high scores for `tribal_dominance` (0.9) and `enmity` (0.9) in the populist discourse align with the CFF's definitions, which identify linguistic patterns such as "us vs them" framing [6] and "hostility language" like "enemy" or "fight against" [5, 13]. The higher SCI points toward a pattern the framework describes as the "deliberate deployment of opposing appeals for complex rhetorical effects" [27].

**Limitations:**
This finding is based on a single sample of populist discourse. The framework itself notes potential for analytical bias based on ideological preferences for cohesive versus fragmentative discourse [1, 9].

---

#### **H3: Democratic Patterns**
*Statement: The two discourse types will exhibit distinct social cohesion signatures corresponding to institutional versus popu

list democratic approaches.*

**Finding: SUPPORTED**

**Reasoning:**
The analysis revealed two distinct and largely inverse quantitative profiles. The institutional discourse is characterized by high scores on cohesive dimensions and low scores on fragmentative dimensions. The populist discourse displays the opposite pattern. This differentiation is consistent across raw scores and derived indices.

**Statistical Evidence:**
*   **Overall Cohesion Index:** Institutional: 0.743 vs. Populist: -0.321
*   **Cohesive vs. Fragmentative Balance:**
    *   Institutional: `cohesive_index` (0.88) is much greater than `fragmentative_index` (0.1).
    *   Populist: `fragmentative_index` (0.84) is much greater than `cohesive_index` (0.36).
*   **Dimensional Opposition:** The pattern of opposition holds across the five core dimensions. For example, in the relational dimension, the institutional discourse scored 0.9 on `amity` and 0.1 on `enmity`, while the populist discourse scored 0.5 on `amity` and 0.9 on `enmity`.

**Textual Correlates:**
The framework is designed to capture such differences through its use of `Dynamic Salience Weighting`, which "enables distinction between texts with similar dimension scores but fundamentally different rhetorical strategies" [2, 8]. The distinct statistical signatures are the quantitative output of applying this method to texts with different linguistic patterns [7].

**Limitations:**
The sample size (n=2 total) is insufficient to establish these signatures as definitive models for their respective discourse categories. The framework's acknowledged `Temporal Bias` [10, 19] means that norms observed in these contemporary texts may not apply to other historical contexts.

---

### **SECTION 2: ADDITIONAL PATTERNS IN THE DATA**

**1. Mutually Exclusive Success Orientation**

A notable pattern emerged in the `success_orientation` dimension (Envy vs. Compersion). The two discourses occupied opposite poles with no overlap, resulting in a `success_tension` score of 0.0 for both.

*   **Institutional Discourse:** `envy_score` = 0.0, `compersion_score` = 0.9.
*   **Populist Discourse:** `envy_score` = 0.85, `compersion_score` = 0.0.

This suggests that, within these specific texts, the framing of others' success is a binary choice rather than a point of strategic tension. The populist discourse exclusively used language of resentment and grievance [15], while the institutional discourse exclusively used language of shared success.

**2. Locus of Rhetorical Tension**

While both texts contained some level of contradiction, the populist discourse registered higher tension scores across nearly all dimensions where tension was present.

*   **Identity Tension:** Populist (0.17) vs. Institutional (0.06)
*   **Emotional Tension:** Populist (0.14) vs. Institutional (0.09)
*   **Relational Tension:** Populist (0.25) vs. Institutional (0.08)

This pattern indicates that the populist discourse more frequently combines opposing appeals (e.g., fear and hope, enmity and amity). The institutional discourse, by contrast, shows lower tension, indicating a more internally consistent cohesive message, aligning with the CFF's "Coherent Cohesive Strategy" profile [27].

**3. Relationship Between Fragmentation and Contradiction**

The data shows a positive association between high fragmentation and high strategic contradiction. The populist discourse, which scored highest on the `fragmentative_index` (0.84), also had the highest `strategic_contradiction_index` (0.122). Conversely, the institutional discourse had low scores on both (`fragmentative_index` = 0.1, `strategic_contradiction_index` = 0.072). This suggests that, in this dataset, the fragmentative rhetorical strategy is correlated with the use of mixed and contradictory messaging.

## Technical Transparency
**Investigation Log**: 15 evidence queries performed
**Models Used**: Synthesis: vertex_ai/gemini-2.5-pro
**Evidence Interrogation**: Active RAG-powered investigation
