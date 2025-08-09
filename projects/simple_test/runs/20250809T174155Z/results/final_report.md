# Experiment Report

**Computational Discourse Analysis Synthesis Report**

**Experiment:** democratic_discourse_cohesion_study
**Framework:** Cohesive Flourishing Framework (CFF) v7.3
**Discourse Samples:**
1.  **Institutional:** John McCain's 2008 concession speech
2.  **Populist:** Bernie Sanders' 2016 populist critique speech

This report synthesizes the results of a computational analysis comparing two distinct types of political discourse. The analysis utilized the Cohesive Flourishing Framework v7.3 to quantify dimensions of social cohesion.

---

### **SECTION 1: HYPOTHESIS TESTING RESULTS**

#### **H1: Institutional Cohesion**
*Statement: McCain's institutional concession will demonstrate higher overall cohesion indices (dignity, hope, amity, cohesive goals) reflecting democratic norms of gracious transition.*

**Finding: SUPPORTED**

**Reasoning & Evidence:**
The institutional discourse sample (McCain) registered consistently higher scores on all specified cohesive dimensions compared to the populist sample (Sanders).
*   **Individual Dignity Score:** Institutional 0.8 vs. Populist 0.2
*   **Hope Score:** Institutional 0.9 vs. Populist 0.6
*   **Amity Score:** Institutional 0.9 vs. Populist 0.5
*   **Cohesive Goals Score:** Institutional 0.9 vs. Populist 0.5

Derived metrics confirm this pattern. The institutional discourse produced a `Cohesive Index` of 0.88 and an `Overall Cohesion Index` of 0.74. In contrast, the populist discourse produced a `Cohesive Index` of 0.36 and an `Overall Cohesion Index` of -0.32.

**Limitations:**
This finding is based on a single paradigmatic example for each discourse type (n=1 per group). The results demonstrate a clear pattern within this specific comparison, but the generalizability of this pattern to all institutional or populist discourse is not established by this data.

---

#### **H2: Populist Fragmentation**
*Statement: Sanders' populist critique will show higher fragmentative elements (tribal dominance, enmity) but with strategic contradictions indicating sophisticated rhetorical positioning.*

**Finding: SUPPORTED**

**Reasoning & Evidence:**
The populist discourse sample (Sanders) exhibited substantially higher scores on fragmentative dimensions.
*   **Tribal Dominance Score:** Populist 0.9 vs. Institutional 0.1
*   **Enmity Score:** Populist 0.9 vs. Institutional 0.1
*   **Fragmentative Goals Score:** Populist 0.75 vs. Institutional 0.1

The second part of the hypothesis, regarding strategic contradictions, is also supported by the data. The populist discourse registered a higher `Strategic Contradiction Index` (0.122) than the institutional discourse (0.072). This higher index corresponds with the co-occurrence of high fragmentative scores (e.g., `Enmity Score` of 0.9) and moderate cohesive scores (e.g., `Hope Score` of 0.6, `Amity Score` of 0.5) within the same text.

**Limitations:**
As with H1, the sample size of n=1 per group restricts the scope of the conclusion. The term "sophisticated rhetorical positioning" is an interpretation of the numerical finding; the data itself only confirms a higher level of measured contradiction.

---

#### **H3: Democratic Patterns**
*Statement: The two discourse types will exhibit distinct social cohesion signatures corresponding to institutional versus populist democratic approaches.*

**Finding: SUPPORTED**

**Reasoning & Evidence:**
The quantitat

ive profiles of the two discourse samples are markedly distinct and largely oppositional.
*   **Institutional Signature:** Characterized by high scores on cohesive dimensions (`Individual Dignity` 0.8, `Hope` 0.9, `Amity` 0.9, `Cohesive Goals` 0.9) and low scores on fragmentative dimensions (`Tribal Dominance` 0.1, `Enmity` 0.1).
*   **Populist Signature:** Characterized by high scores on fragmentative dimensions (`Tribal Dominance` 0.9, `Enmity` 0.9, `Fear` 0.8) and comparatively lower scores on cohesive dimensions (`Individual Dignity` 0.2, `Amity` 0.5).

The `Overall Cohesion Index` encapsulates this distinction, with the institutional sample scoring 0.74 and the populist sample scoring -0.32. The correlation matrix further reflects this oppositional structure, showing near-perfect negative correlations (e.g., -1.0 between `tribal_dominance_score` and `individual_dignity_score`).

**Limitations:**
The analysis confirms two distinct signatures for the two specific texts analyzed. Whether these signatures are representative of broader categories of "institutional" and "populist" discourse requires analysis of a larger and more diverse corpus of texts.

---

### **SECTION 2: ADDITIONAL PATTERNS IN THE DATA**

**1. Bipolar Correlation Structure**
A prominent pattern in the `task_04_generate_correlation_matrix` is the presence of perfect or near-perfect correlations (values of 1.0 or -1.0) across all dimensional scores. For instance, `tribal_dominance_score` is perfectly negatively correlated (-1.0) with `individual_dignity_score`, `hope_score`, `amity_score`, and `cohesive_goals_score`. This mathematical artifact is a direct result of the analysis being conducted on only two data points (one for each discourse type). While it visually reinforces the oppositional nature of the two selected texts, this perfect correlation would not be expected in a larger, more varied dataset.

**2. Divergent Dimensional Tension Profiles**
While the populist discourse had a higher overall `Strategic Contradiction Index` (0.122 vs. 0.072), the specific sources of internal tension differed between the two texts.
*   The **populist** discourse's highest tension scores were in the **Identity** (`identity_tension`: 0.17) and **Emotional** (`emotional_tension`: 0.14) dimensions. This corresponds to the co-occurrence of high `tribal_dominance` (0.9) with some `individual_dignity` (0.2), and high `fear` (0.8) with moderate `hope` (0.6).
*   The **institutional** discourse's highest tension score was in the **Relational** dimension (`relational_tension`: 0.25). This is numerically derived from the combination of very high `amity` (0.9) and low but non-zero `enmity` (0.1).

**3. Asymmetry in Overall Cohesion/Fragmentation Magnitude**
The derived `Overall Cohesion Index` shows an asymmetry in magnitude between the two samples. The institutional discourse score is 0.74, while the populist discourse score is -0.32. The absolute value of the institutional score (0.74) is more than twice that of the populist score (0.32). This suggests that, within this comparison, the institutional text is more uniformly cohesive than the populist text is uniformly fragmentative. The populist text's high fragmentation scores are moderated by non-trivial scores in cohesive dimensions (`hope_score`: 0.6, `amity_score`: 0.5), resulting in a less extreme negative overall index.

## Technical Transparency
**Investigation Log**: 15 evidence queries performed
**Models Used**: Synthesis: vertex_ai/gemini-2.5-pro
**Evidence Interrogation**: Active RAG-powered investigation


---

## Research Transparency: Computational Cost Analysis

### Cost Summary
**Total Cost**: $0.1216 USD  
**Total Tokens**: 40,064  
**Run Timestamp**: 20250809T174155Z  

### Cost Breakdown by Operation
- **Raw Data Analysis Planning**: $0.0554 USD (18,757 tokens, 1 calls, $0.0554 avg/call)
- **Derived Metrics Analysis Planning**: $0.0663 USD (21,307 tokens, 1 calls, $0.0663 avg/call)

### Cost Breakdown by Model
- **vertex_ai/gemini-2.5-pro**: $0.1216 USD (40,064 tokens, 2 calls)

### Cost Breakdown by Agent
- **RawDataAnalysisPlanner**: $0.0554 USD (18,757 tokens, 1 calls)
- **DerivedMetricsAnalysisPlanner**: $0.0663 USD (21,307 tokens, 1 calls)

### Methodology Note
This research was conducted using the Discernus computational research platform, ensuring complete transparency in computational costs. All LLM interactions are logged with exact token counts and costs for reproducibility and academic integrity.

**Cost Calculation**: Based on provider pricing at time of execution  
**Token Counting**: Exact tokens reported by LLM providers  
**Audit Trail**: Complete logs available in experiment run directory  
