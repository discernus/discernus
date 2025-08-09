# Experiment Report

### **Computational Discourse Analysis Synthesis Report**

**Experiment:** democratic_discourse_cohesion_study
**Framework:** Cohesive Flourishing Framework (CFF) v7.3
**Date:** October 26, 2023

This report presents the quantitative and qualitative findings from a computational analysis of two distinct political discourse styles: institutional concession (John McCain, 2008) and populist critique (Bernie Sanders, 2025). The analysis utilized the Cohesive Flourishing Framework v7.3 to measure social cohesion and fragmentation dynamics.

---

### **SECTION 1: HYPOTHESIS TESTING RESULTS**

#### **H1: Institutional Cohesion**
*Statement: McCain's institutional concession will demonstrate higher overall cohesion indices (dignity, hope, amity, cohesive goals) reflecting democratic norms of gracious transition.*

**Finding: SUPPORTED**

**Reasoning:**
The institutional discourse sample (McCain) registered higher scores across all specified cohesive dimensions compared to the populist sample (Sanders).

*   **Statistical Evidence:**
    *   **Individual Dignity:** McCain score = 0.8; Sanders score = 0.2
    *   **Hope:** McCain score = 0.9; Sanders score = 0.6
    *   **Amity:** McCain score = 0.9; Sanders score = 0.5
    *   **Cohesive Goals:** McCain score = 0.9; Sanders score = 0.5
    *   The derived `overall_cohesion_index` for the institutional discourse was **0.743**, compared to **-0.321** for the populist discourse.

**Data Limitations:**
The finding is based on a single text for each discourse category (n=1). The results reflect the characteristics of these specific samples and may not be generalizable to all institutional or populist discourse.

---

#### **H2: Populist Fragmentation**
*Statement: Sanders' populist critique will show higher fragmentative elements (tribal dominance, enmity) but with strategic contradictions indicating sophisticated rhetorical positioning.*

**Finding: SUPPORTED**

**Reasoning:**
The populist discourse sample (Sanders) exhibited higher scores in fragmentative dimensions. It also registered a higher `strategic_contradiction_index` (SCI), which quantifies the use of opposing rhetorical appeals.

*   **Statistical Evidence:**
    *   **Tribal Dominance:** Sanders score = 0.9; McCain score = 0.1. The populist text contained concepts of in-group supremacy and exclusionary framing ("us vs them") [6].
    *   **Enmity:** Sanders score = 0.9; McCain score = 0.1. The populist text utilized hostility language and antagonistic framing ("fight against," "defeat") [5].
    *   **Strategic Contradiction Index (SCI):** The populist discourse registered an SCI of **0.122**, while the institutional discourse registered an SCI of **0.072**.

**Data Limitations:**
This analysis is limited to two texts. The higher SCI in the populist sample is a quantitative observation of rhetorical tension within that specific text, and its strategic intent is an interpretation posited by the hypothesis.

---

#### **H3: Democratic Patterns**
*Statement: The two discourse types will exhibit distinct social cohesion signatures corresponding to institutional versus populist democratic approaches.*

**Finding: SUPPORTED**

**Reasoning:**
The quantitative profiles of the two discourse samples are distinct across nearly all CFF dimensions, producing divergent overall cohesion and fragmentation scores. The framework is designed to identify such differences through its scoring and weighting system [2, 8].

*   **Statistical Evidence:**
    *   **Institutional Signature (McCain):** Characterized by high cohesive scores (`individual_dign

ity_score`: 0.8, `hope_score`: 0.9, `amity_score`: 0.9) and low fragmentative scores (`tribal_dominance_score`: 0.1, `enmity_score`: 0.1). This resulted in a high `salience_weighted_cohesive_index` of **0.883** and a low `salience_weighted_fragmentative_index` of **0.14**.
    *   **Populist Signature (Sanders):** Characterized by high fragmentative scores (`tribal_dominance_score`: 0.9, `enmity_score`: 0.9, `envy_score`: 0.85) and comparatively lower cohesive scores (`individual_dignity_score`: 0.2, `amity_score`: 0.5). This resulted in a high `salience_weighted_fragmentative_index` of **0.843** and a lower `salience_weighted_cohesive_index` of **0.522**.

**Data Limitations:**
The distinct signatures are evident in the selected paradigmatic examples. The framework's potential biases, including cultural and selection bias, should be considered when evaluating these patterns [1].

---

### **SECTION 2: ADDITIONAL PATTERNS IN THE DATA**

#### **1. Inverse Relationship Between Overall Cohesion and Fragmentation**
A strong inverse relationship was observed between the final derived indices for the two discourse styles.

*   **Observation:** The institutional discourse (McCain) produced a positive `overall_cohesion_index` of **0.743**. The populist discourse (Sanders) produced a negative `overall_cohesion_index` of **-0.321**.
*   **Details:** This pattern is consistent in the underlying salience-weighted indices. The institutional text's cohesive index (0.883) was substantially higher than its fragmentative index (0.14). Conversely, the populist text's fragmentative index (0.843) was substantially higher than its cohesive index (0.522). This suggests the two rhetorical strategies, as captured by the CFF, operate on opposite ends of the cohesion/fragmentation spectrum.

#### **2. Rhetorical Tension in Emotional and Relational Dimensions**
The populist discourse sample demonstrated higher rhetorical tension scores, particularly in the emotional and relational dimensions, which contributes to its higher overall Strategic Contradiction Index.

*   **Observation:** The populist text (Sanders) had an `emotional_tension` score of **0.140** and a `relational_tension` score of **0.25**. The institutional text (McCain) had scores of **0.090** and **0.080** in these respective dimensions.
*   **Details:** The higher `emotional_tension` in the Sanders text corresponds to the simultaneous presence of high `fear_score` (0.8) and `hope_score` (0.6). The higher `relational_tension` corresponds to the co-occurrence of a high `enmity_score` (0.9) and a moderate `amity_score` (0.5). The CFF tension formula quantifies this dynamic [18], where opposing appeals are used within the same discourse.

#### **3. Mutually Exclusive Success Orientations**
The analysis of the Success Orientation dimension (Envy vs. Compersion) revealed two distinct, non-overlapping strategies.

*   **Observation:** The `success_tension` score was **0.0** for both texts, but for opposite reasons.
*   **Details:**
    *   The populist text (Sanders) scored **0.85** on `envy_score` and **0.0** on `compersion_score`. This indicates a focus on resentment and grievance framing ("unfair advantage," "privileged elite") [15].
    *   The institutional text (McCain) scored **0.0** on `envy_score` and **0.7** on `compersion_score`. This indicates a focus on celebrating the success of others.
*   The zero tension score for both suggests that each text employed a coherent, non-contradictory strategy within this specific dimension, though the strategies themselves were diametrically opposed.

## Technical Transparency
**Investigation Log**: 15 evidence queries performed
**Models Used**: Synthesis: vertex_ai/gemini-2.5-pro
**Evidence Interrogation**: Active RAG-powered investigation
