# Experiment Report

### **Computational Discourse Analysis Synthesis Report**

**Experiment:** democratic_discourse_cohesion_study
**Framework:** Cohesive Flourishing Framework (CFF) v7.3

This report presents the statistical and textual findings from a comparative analysis of two discourse styles: institutional concession and populist critique. The analysis utilized the Cohesive Flourishing Framework v7.3 to measure social cohesion indicators.

---

### **SECTION 1: HYPOTHESIS TESTING RESULTS**

#### **H1: Institutional Cohesion**
*Statement: McCain's institutional concession will demonstrate higher overall cohesion indices (dignity, hope, amity, cohesive goals) reflecting democratic norms of gracious transition.*

**Finding: SUPPORTED**

**Reasoning:**
The institutional discourse sample demonstrated markedly higher scores across all specified cohesive dimensions compared to the populist sample. The `overall_cohesion_index` for the institutional style was 0.7433, contrasted with -0.3210 for the populist style.

*   **Statistical Evidence:**
    *   **Individual Dignity:** Institutional score was 0.8, versus 0.2 for populist.
    *   **Hope:** Institutional score was 0.9, versus 0.6 for populist.
    *   **Amity:** Institutional score was 0.9, versus 0.5 for populist.
    *   **Cohesive Goals:** Institutional score was 0.9, versus 0.5 for populist.

*   **Textual Evidence:**
    The institutional discourse contains statements that align with these high cohesion scores. For example, the theme of amity and shared identity is present in the statement attributed to McCain: "Whatever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that" [16]. The theme of cohesive goals is reflected in the acknowledgement of the democratic process: "Senator Obama and I have had and argued our differences, and he has prevailed" [1].

*   **Limitations:**
    The findings are based on a single paradigmatic example for each discourse style (n=1). The results indicate a strong pattern for these specific cases but do not permit generalization to all institutional or populist discourse without a broader sample.

---

#### **H2: Populist Fragmentation**
*Statement: Sanders' populist critique will show higher fragmentative elements (tribal dominance, enmity) but with strategic contradictions indicating sophisticated rhetorical positioning.*

**Finding: SUPPORTED**

**Reasoning:**
The populist discourse sample registered substantially higher scores on fragmentative dimensions. It also exhibited a higher `strategic_contradiction_index` compared to the institutional sample, consistent with the second part of the hypothesis.

*   **Statistical Evidence:**
    *   **Fragmentative Elements:**
        *   **Tribal Dominance:** Populist score was 0.9, versus 0.1 for institutional.
        *   **Enmity:** Populist score was 0.9, versus 0.1 for institutional.
    *   **Strategic Contradiction:**
        *   The `strategic_contradiction_index` for the populist sample was 0.122, compared to 0.072 for the institutional sample.

*   **Textual Evidence:**
    Textual data attributed to Sanders aligns with the high fragmentation scores. The theme of tribal dominance (us-vs-them) and enmity is evident in the critique of corporate entities: "you have is a small number of extraordinarily large corporations who charge us outrageous prices for the products that we have to buy" [14]. Another statement reinforces this relational framing: "These guys, I want to tell you something because I bump into them in my line of work, they are not nice guys" [19].

*   **Limitations:**
    As with H1, the sample size is n=1 for each style. The `strategic_contradiction_index` is a derived metric specific to the CFF framework, and its interpretation is dependent on the framework's theoretical assumptions.

---

#### **H3: Democratic Patterns**
*Statement: The two discourse types will exhibit distinct social cohesion signatures corresponding to institutional versus populist democratic approaches.*

**Finding: SUPPORTED**

**Reasoning:**
The analysis reveals two distinct and largely opposing quantitative profiles for the institutional and populist discourse samples. The institutional sample is characterized by high cohesive scores and low fragmentative scores, whi

le the populist sample shows the inverse pattern.

*   **Statistical Evidence:**
    *   **Overall Cohesion:** The `overall_cohesion_index` shows a wide divergence: 0.7433 for institutional vs. -0.3210 for populist.
    *   **Cohesive vs. Fragmentative Balance:**
        *   Institutional: `cohesive_index` of 0.88 and `fragmentative_index` of 0.1.
        *   Populist: `cohesive_index` of 0.36 and `fragmentative_index` of 0.84.
    *   This contrast holds across the five primary dimensions of the CFF framework.

*   **Textual Evidence:**
    The textual evidence provides qualitative examples of these distinct signatures. The institutional discourse emphasizes unity and acceptance of results: "Whatever our differences, we are fellow Americans" [2], and "he has prevailed" [4]. The populist discourse, in contrast, focuses on conflict with an out-group: "concentration of ownership... outrageous prices" [20].

*   **Limitations:**
    The finding of distinctness is robust for the two cases analyzed. However, these two examples may represent idealized or extreme poles of their respective discourse types. A larger dataset would be required to determine if these patterns represent a consistent dichotomy or points on a broader spectrum.

---

### **SECTION 2: ADDITIONAL PATTERNS IN THE DATA**

#### **1. Opposing Emotional Climates**
A consistent pattern of opposing emotional appeals was observed between the two discourse styles. The institutional discourse scored high on prosocial emotions, while the populist discourse scored high on antagonistic emotions.

*   **Statistical Finding:**
    *   **Hope vs. Fear:** The institutional sample scored 0.9 for `hope_score` and 0.2 for `fear_score`. The populist sample scored 0.8 for `fear_score` and 0.6 for `hope_score`.
    *   **Compersion vs. Envy:** The institutional sample scored 0.9 for `compersion_score` (joy in another's success) and 0.0 for `envy_score`. The populist sample scored 0.85 for `envy_score` and 0.0 for `compersion_score`.
*   **Textual Correlate:** The institutional text expresses "love for this country and for all its citizens, whether they supported me or Senator Obama" [10], aligning with high compersion. The populist text's focus on "extraordinarily large corporations who charge us outrageous prices" [20] aligns with the generation of envy or resentment.

#### **2. Divergence in Rhetorical Tension**
The calculated tension metrics, which measure the simultaneous use of opposing concepts, varied significantly, indicating different rhetorical strategies. The populist discourse consistently registered higher tension across multiple dimensions.

*   **Statistical Finding:**
    *   **Relational Tension (Amity vs. Enmity):** The populist sample had a tension score of 0.25, while the institutional sample scored 0.08.
    *   **Identity Tension (Dignity vs. Tribal Dominance):** The populist sample scored 0.17, while the institutional sample scored 0.06.
*   **Inference:** The higher tension scores in the populist sample reflect its combination of high enmity/tribal dominance scores with moderate amity/hope scores. For instance, it combines a high `enmity_score` (0.9) with a moderate `amity_score` (0.5). The institutional discourse shows low tension due to its consistently high cohesive scores and low fragmentative scores (e.g., `amity_score` of 0.9 vs. `enmity_score` of 0.1).

#### **3. Salience-Weighted vs. Raw Indices**
A comparison of raw and salience-weighted indices suggests that the core message of each discourse style is amplified by rhetorical emphasis.

*   **Statistical Finding:**
    *   For the institutional sample, the `salience_weighted_cohesive_index` (0.883) is slightly higher than the raw `cohesive_index` (0.880).
    *   For the populist sample, the `salience_weighted_fragmentative_index` (0.843) is slightly higher than the raw `fragmentative_index` (0.840).
*   **Inference:** While the numerical difference is small in these cases, it indicates that the most salient parts of the institutional speech were slightly more cohesive than the speech overall, and the most salient parts of the populist speech were slightly more fragmentative than the speech overall. This pattern suggests that rhetorical emphasis aligns with the primary cohesive or fragmentative orientation of the discourse.

## Technical Transparency
**Investigation Log**: 15 evidence queries performed
**Models Used**: Synthesis: vertex_ai/gemini-2.5-pro
**Evidence Interrogation**: Active RAG-powered investigation


---

## Research Transparency: Computational Cost Analysis

### Cost Summary
**Total Cost**: $0.1229 USD  
**Total Tokens**: 40,188  
**Run Timestamp**: 20250809T174657Z  

### Cost Breakdown by Operation
- **Raw Data Analysis Planning**: $0.0534 USD (18,563 tokens, 1 calls, $0.0534 avg/call)
- **Derived Metrics Analysis Planning**: $0.0695 USD (21,625 tokens, 1 calls, $0.0695 avg/call)

### Cost Breakdown by Model
- **vertex_ai/gemini-2.5-pro**: $0.1229 USD (40,188 tokens, 2 calls)

### Cost Breakdown by Agent
- **RawDataAnalysisPlanner**: $0.0534 USD (18,563 tokens, 1 calls)
- **DerivedMetricsAnalysisPlanner**: $0.0695 USD (21,625 tokens, 1 calls)

### Methodology Note
This research was conducted using the Discernus computational research platform, ensuring complete transparency in computational costs. All LLM interactions are logged with exact token counts and costs for reproducibility and academic integrity.

**Cost Calculation**: Based on provider pricing at time of execution  
**Token Counting**: Exact tokens reported by LLM providers  
**Audit Trail**: Complete logs available in experiment run directory  
