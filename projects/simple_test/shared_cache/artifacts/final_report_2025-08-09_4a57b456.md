# Experiment Report

**Computational Discourse Analysis Synthesis Report**

**Experiment:** democratic_discourse_cohesion_study
**Framework:** Cohesive Flourishing Framework (CFF) v7.3

This report presents a factual synthesis of statistical findings from the analysis of two distinct discourse types: institutional concession and populist critique. The analysis utilized the Cohesive Flourishing Framework v7.3 to measure social cohesion indicators.

---

### **SECTION 1: HYPOTHESIS TESTING RESULTS**

This section evaluates the three pre-registered hypotheses against the collected statistical evidence.

**H1: Institutional Cohesion**
*Statement: McCain's institutional concession will demonstrate higher overall cohesion indices (dignity, hope, amity, cohesive goals) reflecting democratic norms of gracious transition.*

*   **Finding:** **SUPPORTED**
*   **Statistical Evidence:** The institutional discourse sample registered higher scores on all four specified cohesive metrics compared to the populist discourse sample.
    *   **Individual Dignity Score:** Institutional (0.8) vs. Populist (0.2)
    *   **Hope Score:** Institutional (0.9) vs. Populist (0.6)
    *   **Amity Score:** Institutional (0.9) vs. Populist (0.5)
    *   **Cohesive Goals Score:** Institutional (0.9) vs. Populist (0.5)
*   **Reasoning:** The quantitative results align directly with the hypothesis. The discourse attributed to McCain's institutional concession consistently scored higher on the four measures of social cohesion. The derived `overall_cohesion_index` further reflects this pattern, with the institutional discourse scoring 0.743 and the populist discourse scoring -0.321.
*   **Limitations:** The finding is based on a sample size of one discourse for each category (N=2 total). The results describe the characteristics of these specific samples and may not be generalizable without further study.

**H2: Populist Fragmentation**
*Statement: Sanders' populist critique will show higher fragmentative elements (tribal dominance, enmity) but with strategic contradictions indicating sophisticated rhetorical positioning.*

*   **Finding:** **SUPPORTED**
*   **Statistical Evidence:** The populist discourse sample registered higher scores on the specified fragmentative metrics. It also registered a higher `strategic_contradiction_index`.
    *   **Tribal Dominance Score:** Populist (0.9) vs. Institutional (0.1)
    *   **Enmity Score:** Populist (0.9) vs. Institutional (0.1)
    *   **Strategic Contradiction Index:** Populist (0.122) vs. Institutional (0.072)
*   **Reasoning:** The data supports both components of the hypothesis. The discourse attributed to Sanders' populist critique scored substantially higher on fragmentative elements. The higher `strategic_contradiction_index` for the populist sample, combined with the co-occurrence of high scores for opposing concepts (e.g., `fear_score` of 0.8 alongside a `hope_score` of 0.6; `enmity_score` of 0.9 alongside an `amity_score` of 0.5), is consistent with the "strategic contradictions" portion of the hypothesis.
*   **Limitations:** This analysis is based on a single populist discourse sample. The interpretation of "strategic contradiction" is based on the framework's derived metric, and the specific rhetorical mechanisms are not detail

ed in this statistical summary.

**H3: Democratic Patterns**
*Statement: The two discourse types will exhibit distinct social cohesion signatures corresponding to institutional versus populist democratic approaches.*

*   **Finding:** **SUPPORTED**
*   **Statistical Evidence:** The two discourse types produced highly distinct and largely inverse quantitative profiles.
    *   **Overall Cohesion Index:** Institutional (0.743) vs. Populist (-0.321)
    *   **Cohesive Index:** Institutional (0.88) vs. Populist (0.36)
    *   **Fragmentative Index:** Institutional (0.1) vs. Populist (0.84)
*   **Reasoning:** The summary metrics show a clear differentiation between the two samples. The institutional discourse profile is characterized by high cohesive scores and low fragmentative scores. Conversely, the populist discourse profile is characterized by high fragmentative scores and lower cohesive scores. This marked quantitative divergence constitutes distinct social cohesion signatures as measured by the CFF framework.
*   **Limitations:** As with the other hypotheses, the finding is based on a small sample (N=1 per type) and describes the patterns within this specific dataset.

---

### **SECTION 2: ADDITIONAL PATTERNS IN THE DATA**

Further examination of the statistical results reveals additional patterns beyond the primary hypothesis tests.

**1. Inverse Relationship Between Cohesion and Fragmentation Indices**
A strong inverse pattern exists between the primary `cohesive_index` and `fragmentative_index` for each discourse type.
*   The institutional discourse sample scored 0.88 on the `cohesive_index` and 0.1 on the `fragmentative_index`.
*   The populist discourse sample scored 0.36 on the `cohesive_index` and 0.84 on the `fragmentative_index`.
This shows a near-mirroring effect where a high score on one index corresponds to a low score on its counterpart within each discourse type in this dataset.

**2. Distribution of Dimensional Tension Scores**
While the populist discourse registered a higher overall `strategic_contradiction_index` (0.122 vs. 0.072), the distribution of tension across the five CFF dimensions was not uniform.
*   The populist discourse showed higher tension in the **Identity** (0.17 vs. 0.06) and **Emotional** (0.14 vs. 0.09) dimensions.
*   Conversely, the institutional discourse showed higher tension in the **Relational** (0.25 vs. 0.08) and **Goal** (0.10 vs. 0.08) dimensions.
The `relational_tension` score for the institutional discourse (0.25) was the single highest tension score recorded across all dimensions for either sample.

**3. Effect of Salience Weighting**
The application of salience weighting to the primary indices resulted in a slight increase in the dominant characteristic of each discourse type, without altering the overall finding.
*   For the institutional discourse, the `salience_weighted_cohesive_index` (0.883) was marginally higher than the unweighted `cohesive_index` (0.88).
*   For the populist discourse, the `salience_weighted_fragmentative_index` (0.843) was marginally higher than the unweighted `fragmentative_index` (0.84).
This suggests that the elements with the highest rhetorical salience in each text sample aligned with that sample's primary cohesive or fragmentative orientation.

## Technical Transparency
**Investigation Log**: 0 evidence queries performed
**Models Used**: Synthesis: vertex_ai/gemini-2.5-pro
**Evidence Interrogation**: Active RAG-powered investigation


---

## Research Transparency: Computational Cost Analysis

### Cost Summary
**Total Cost**: $0.1104 USD  
**Total Tokens**: 39,838  
**Run Timestamp**: 20250809T173314Z  

### Cost Breakdown by Operation
- **Raw Data Analysis Planning**: $0.0525 USD (18,915 tokens, 1 calls, $0.0525 avg/call)
- **Derived Metrics Analysis Planning**: $0.0580 USD (20,923 tokens, 1 calls, $0.0580 avg/call)

### Cost Breakdown by Model
- **vertex_ai/gemini-2.5-pro**: $0.1104 USD (39,838 tokens, 2 calls)

### Cost Breakdown by Agent
- **RawDataAnalysisPlanner**: $0.0525 USD (18,915 tokens, 1 calls)
- **DerivedMetricsAnalysisPlanner**: $0.0580 USD (20,923 tokens, 1 calls)

### Methodology Note
This research was conducted using the Discernus computational research platform, ensuring complete transparency in computational costs. All LLM interactions are logged with exact token counts and costs for reproducibility and academic integrity.

**Cost Calculation**: Based on provider pricing at time of execution  
**Token Counting**: Exact tokens reported by LLM providers  
**Audit Trail**: Complete logs available in experiment run directory  
