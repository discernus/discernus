# Populist Discourse Analysis Framework (PDAF) Analysis Report

**Experiment**: experiment configuration
**Run ID**: bb62fa34d8c641edd68c37342a0c4f53bbab5859bf39c66e32a3920870270cb4
**Date**: 2025-08-25
**Framework**: Populist Discourse Analysis Framework (PDAF) v10.0.0
**Corpus**: Not available (4 documents)

---

## 1. Executive Summary

This computational social science report presents a preliminary analysis of populist discourse within a small, purposive corpus of four American political speeches using the Populist Discourse Analysis Framework (PDAF) v10.0.0. The analysis reveals the framework's potential to not only quantify the intensity of populist rhetoric but also to differentiate between distinct rhetorical archetypes. Due to the pilot nature of this study (N=4), all findings should be considered indicative and exploratory, requiring validation with larger datasets.

The central finding is the emergence of two distinct populist strategies. The first, an **"Economic Insurgent"** archetype exemplified by Bernie Sanders and Alexandria Ocasio-Cortez, is characterized by a strong focus on `economic_populist_appeals` (Mean = 1.00 for this group), claims of `elite_conspiracy_systemic_corruption` (Mean = 0.90), and a Manichaean division between the "people" and a wealthy oligarchy. The second, a **"Nationalist Defender"** archetype represented by Steve King, emphasizes `nationalist_exclusion` (Raw Score = 0.90) and `anti_pluralist_exclusion` (Raw Score = 0.80), framing threats as external and cultural. These two strategies are statistically distinguished by a negative correlation between `nationalist_exclusion` and `economic_populist_appeals` (r = -0.66) and the effective discriminatory power of the `internal_external_focus_tension` metric. John McCain's concession speech serves as a crucial non-populist baseline, scoring near zero on most populist indicators.

The PDAF demonstrates promising construct validity in this preliminary test. Core populist concepts like `manichaean_people_elite_framing` and `elite_conspiracy_systemic_corruption` are very strongly correlated (r = 0.90), suggesting they form a coherent rhetorical core. Furthermore, the framework's salience-weighted indices, particularly the `salience_weighted_overall_populism_index`, provide a robust, nuanced measure of populist intensity that aligns with qualitative expectations, ranking the speakers from most to least populist. These results, while preliminary, underscore the utility of multi-dimensional, tension-aware frameworks for moving beyond binary classification and capturing the complex strategic variations within populist communication.

## 2. Opening Framework: Key Insights

*   **Two Distinct Populist Archetypes Emerged:** The data strongly suggests the presence of two different populist strategies within the corpus. An "Economic Insurgent" style (Sanders, Ocasio-Cortez) is defined by its near-perfect scores on `economic_populist_appeals` and high scores on `elite_conspiracy_systemic_corruption`. In contrast, a "Nationalist Defender" style (King) is defined by high scores on `nationalist_exclusion` and `anti_pluralist_exclusion`. This is supported by the negative correlation (r = -0.66) between `nationalist_exclusion` and `economic_populist_appeals`.
*   **Manichaean Framing is the Populist Core:** The dimension of `manichaean_people_elite_framing` appears to be a foundational element of the populist speeches analyzed, correlating strongly with the overall populism index (r = 0.99). However, its meaning is context-dependent. For Sanders, it is an economic division, as he stated: "...you would not feel obliged to step on the backs of poor people to become even richer" (Source: bernie_sanders_2025_fighting_oligarchy.txt). For King, it is a political division against those who would "...push Obamacare down the throats of the American people" (Source: steve_king_2017_house_floor.txt).
*   **Tension Metrics Effectively Differentiate Populist Types:** The framework's derived `internal_external_focus_tension` metric proved highly effective. It registered a score of 0.0 for the economically-focused speakers (Sanders, Ocasio-Cortez) but a score of 0.16 for the nationalist-focused speaker (King), whose rhetoric centered on external threats. This is validated by the near-perfect correlation between this tension metric and `nationalist_exclusion` (r = 0.99).
*   **"Rigged System" Narrative Forms a Coherent Cluster:** The analysis reveals a powerful rhetorical cluster linking `elite_conspiracy_systemic_corruption`, `homogeneous_people_construction`, and `economic_populist_appeals`. The correlation between conspiracy claims and economic appeals is exceptionally high (r = 0.96). This suggests that in the economic populist variant, the construction of a unified "people" is achieved by defining them against a corrupt economic system, as Sanders claims: "That is what a rigged economy is about, and that is what we are going to change" (Source: bernie_sanders_2025_fighting_oligarchy.txt).
*   **Salience-Weighted Indices Provide Robust Measurement:** The composite indices, particularly the `salience_weighted_overall_populism_index`, effectively quantify the intensity of populist rhetoric. The scores clearly separate the non-populist baseline (McCain: 0.100) from the populist speakers (King: 0.734; Sanders: 0.802; Ocasio-Cortez: 0.807), providing a more nuanced measurement than a simple binary classification would allow.

## 4. Methodology

### Framework Description and Analytical Approach

This study employs the Populist Discourse Analysis Framework (PDAF) v10.0.0, an analytical tool designed to measure the core components of populist political communication. As described in its specification, the PDAF moves beyond simple classification by using "advanced strategic tension analysis and salience-weighted measurement." The framework operationalizes populism across several key dimensions, including:

*   **Core Populism:** `manichaean_people_elite_framing`, `crisis_restoration_narrative`, `popular_sovereignty_claims`.
*   **Populist Mechanisms:** `elite_conspiracy_systemic_corruption`, `authenticity_vs_political_class`, `homogeneous_people_construction`.
*   **Boundary Distinctions:** `nationalist_exclusion`, `economic_populist_appeals`.

A key innovation of the PDAF is its calculation of derived metrics. These include **tension metrics** (e.g., `internal_external_focus_tension`) that measure the strategic balance between opposing rhetorical frames, and **salience-weighted indices** that aggregate dimensional scores into composite measures of populism, accounting for the prominence of each theme. This approach allows for a multi-faceted, quantitative assessment of rhetorical strategy.

### Data Structure and Corpus Description

The analysis was conducted on a small (N=4) but diverse corpus of political speeches from prominent American figures:

1.  **John McCain (2008):** Presidential concession speech, expected to be a non-populist baseline.
2.  **Steve King (2017):** House floor speech, representing a right-wing, nationalist perspective.
3.  **Bernie Sanders (2025):** Campaign-style speech ("Fighting Oligarchy"), representing a left-wing, economic perspective.
4.  **Alexandria Ocasio-Cortez (2025):** Campaign-style speech ("Fighting Oligarchy"), also representing a left-wing, economic perspective.

The data for each document consists of raw scores (0-1), salience scores (0-1), and confidence scores (0-1) for each of the nine primary PDAF dimensions, as well as the calculated values for the derived tension metrics and composite indices.

### Statistical Methods and Analytical Constraints

The analysis is primarily descriptive and correlational, appropriate for the exploratory nature of this pilot study. The primary statistical methods include:

1.  **Descriptive Statistics:** Calculation of mean, standard deviation, minimum, and maximum for each measured dimension across the corpus to identify central tendencies and variability.
2.  **Pearson Correlation Analysis:** A correlation matrix was computed to examine the relationships between all raw dimensional scores and derived indices. This helps identify rhetorical clusters and assess the internal consistency of the framework's constructs.

**Limitations:** The most significant limitation is the extremely small sample size (N=4). This prevents any form of inferential statistical testing or generalization of the findings. All correlations and patterns identified are suggestive and serve to generate hypotheses for future research rather than to confirm them. The analysis is also confined to the American political context. The absence of a corpus manifest (`corpus.md`) and specified research objectives means the analysis proceeds from the data upwards, in an exploratory fashion.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

The descriptive statistics reveal significant variation across the dimensions, highlighting which rhetorical features are most prevalent and which are most divisive within this corpus.

**Table 1: Descriptive Statistics of PDAF Raw Dimensions (N=4)**

| Dimension | Mean | Std. Dev. | Min | Max |
| :--- | :--- | :--- | :--- | :--- |
| manichaean_people_elite_framing_raw | 0.625 | 0.427 | 0.0 | 0.9 |
| crisis_restoration_narrative_raw | 0.500 | 0.294 | 0.1 | 0.8 |
| popular_sovereignty_claims_raw | 0.375 | 0.386 | 0.0 | 0.8 |
| anti_pluralist_exclusion_raw | 0.350 | 0.370 | 0.0 | 0.8 |
| elite_conspiracy_systemic_corruption_raw | 0.525 | 0.450 | 0.0 | 0.9 |
| authenticity_vs_political_class_raw | 0.275 | 0.427 | 0.0 | 0.9 |
| homogeneous_people_construction_raw | 0.425 | 0.386 | 0.0 | 0.8 |
| nationalist_exclusion_raw | 0.250 | 0.436 | 0.0 | 0.9 |
| economic_populist_appeals_raw | 0.500 | 0.577 | 0.0 | 1.0 |

The core populist dimension, `manichaean_people_elite_framing_raw`, shows a high mean (0.625), indicating its general importance in the three populist speeches. However, its standard deviation is also high (0.427), reflecting its near-total absence in the non-populist baseline text. The dimension with the highest standard deviation is `economic_populist_appeals_raw` (0.577), suggesting it is a key point of differentiation among the speakers. Indeed, the data shows two speakers scoring 1.0, one scoring 0.0, and one scoring 0.0, making it a powerful discriminator in this sample. Conversely, dimensions like `authenticity_vs_political_class_raw` have a lower mean (0.275), suggesting this is a less central or less consistently deployed rhetorical strategy in this specific corpus.

### 5.2 Advanced Metric Analysis

The derived metrics provide a higher-level view of rhetorical strategy. The salience-weighted indices quantify overall populist intensity, while the tension metrics reveal strategic positioning.

**Table 2: Document Scores on Key Derived PDAF Metrics**

| Document Name | Overall Populism Index | Core Populism Index | Populism Mechanisms Index | Boundary Distinctions Index | Internal/External Tension |
| :--- | :--- | :--- | :--- | :--- | :--- |
| john_mccain_2008_concession.txt | 0.100 | 0.100 | 0.000 | 0.099 | 0.000 |
| steve_king_2017_house_floor.txt | 0.734 | 0.731 | 0.266 | 0.899 | 0.160 |
| bernie_sanders_2025... | 0.802 | 0.763 | 0.742 | 0.999 | 0.000 |
| alexandria_ocasio_cortez_2025... | 0.807 | 0.668 | 0.868 | 0.908 | 0.000 |

The `salience_weighted_overall_populism_index` effectively ranks the documents. John McCain's speech (0.100) is clearly identified as non-populist. The three other speakers all score high, with Ocasio-Cortez (0.807) and Sanders (0.802) registering as slightly more intensely populist overall than King (0.734). This finding is supported by McCain's call for unity, which stands in stark contrast to the populist texts: As John McCain stated, "I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together..." (Source: john_mccain_2008_concession.txt).

The `internal_external_focus_tension` metric is particularly insightful. It scores 0.0 for Sanders and Ocasio-Cortez, whose rhetoric focuses on internal economic divisions. For instance, Ocasio-Cortez defines the struggle internally: "We are witnessing an oligarchy in America. And that is when those with the most economic, political, and technological power destroy the public good to enrich themselves while millions of Americans pay the price" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt). In contrast, Steve King scores 0.160, reflecting his focus on external threats like immigration. As Steve King stated: "Sarah Root would be alive today if the President had done his job, if law enforcement had been allowed to do their job, if ICE had responded when local law enforcement called them" (Source: steve_king_2017_house_floor.txt). This metric successfully captures the fundamental difference in the locus of the perceived threat.

### 5.3 Correlation and Interaction Analysis

The correlation matrix reveals the underlying structure of populist rhetoric within this corpus, highlighting which dimensions tend to be deployed together. These patterns suggest coherent, yet distinct, meta-strategies.

**Table 3: Key Pearson Correlations (r) Among PDAF Dimensions and Indices**

| Variable 1 | Variable 2 | Correlation | Interpretation |
| :--- | :--- | :--- | :--- |
| `manichaean_people_elite_framing` | `elite_conspiracy_systemic_corruption` | 0.90 | Very Large, Positive |
| `elite_conspiracy_systemic_corruption` | `economic_populist_appeals` | 0.96 | Very Large, Positive |
| `elite_conspiracy_systemic_corruption` | `homogeneous_people_construction` | 0.99 | Very Large, Positive |
| `crisis_restoration_narrative` | `populist_strategic_contradiction_index` | 0.99 | Very Large, Positive |
| `nationalist_exclusion` | `internal_external_focus_tension` | 0.99 | Very Large, Positive |
| `nationalist_exclusion` | `economic_populist_appeals` | -0.66 | Large, Negative |
| `anti_pluralist_exclusion` | `nationalist_exclusion` | 0.77 | Large, Positive |

Two primary rhetorical clusters are evident.

**Cluster 1: The "Economic Insurgent" Strategy.** This cluster is defined by the extremely high positive correlations between `elite_conspiracy_systemic_corruption`, `economic_populist_appeals` (r = 0.96), and `homogeneous_people_construction` (r = 0.99). This indicates a strategy where a unified "people" is constructed through a shared grievance against a "rigged" economic system controlled by a corrupt elite. This is exemplified in the speeches of Sanders and Ocasio-Cortez. As Bernie Sanders stated: "We will not accept the richest guy in the world running all over Washington... all so that they could give over a trillion dollars in tax breaks to the wealthiest 1%" (Source: bernie_sanders_2025_fighting_oligarchy.txt). This statement seamlessly blends economic grievance with accusations of elite corruption.

**Cluster 2: The "Nationalist Defender" Strategy.** This cluster is suggested by the strong positive correlation between `anti_pluralist_exclusion` and `nationalist_exclusion` (r = 0.77). This strategy defines the "people" along national or cultural lines and excludes those who do not fit, either internal minorities or external threats. This is the pattern observed in Steve King's speech, which links a failure to enforce immigration law to a threat against the constitution. As Steve King stated: "We have a Constitution that's got to be restored. And instead of being restored, it would be destroyed by another presidential appointment" (Source: steve_king_2017_house_floor.txt).

The large negative correlation between `nationalist_exclusion` and `economic_populist_appeals` (r = -0.66) is a critical finding. It suggests that, in this sample, these two populist appeals are strategically distinct and potentially mutually exclusive. Speakers tended to focus heavily on one to the exclusion of the other, forming the basis for the two archetypes.

### 5.4 Pattern Recognition and Theoretical Insights

The statistical patterns provide preliminary evidence for the construct validity of the PDAF. The framework's dimensions group together in theoretically coherent ways. The strongest correlation observed is between `elite_conspiracy_systemic_corruption` and `homogeneous_people_construction` (r = 0.99). This suggests that the act of defining a unified, virtuous "people" is almost perfectly mirrored by the act of defining a corrupt, conspiratorial "elite." The "people" are given substance and unity primarily through their opposition to this elite.

This finding connects directly to theories of populism that define it as a "thin-centered ideology" which pits a "pure people" against a "corrupt elite." The data here suggests that for the economic populists in the sample, the elite is defined by its conspiratorial economic actions. As Alexandria Ocasio-Cortez stated: "He’s handed the keys to Elon Musk and is selling off our country for parts to the wealthiest people in the world for a kickback" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt). This quote directly alleges a conspiracy for economic gain, which in turn defines the "people" as the victims of this scheme.

An unexpected finding is the extremely high correlation between `crisis_restoration_narrative` and the `populist_strategic_contradiction_index` (r = 0.99). This suggests that the more a speaker frames the present as a deep crisis requiring restoration, the more they employ a mix of democratic and authoritarian appeals. This may indicate that the urgency of the crisis narrative is used to justify rhetorical moves that might otherwise be seen as contradictory to democratic principles.

### 5.5 Framework Effectiveness Assessment

Based on this pilot analysis, the PDAF demonstrates considerable effectiveness in two key areas:

1.  **Discriminatory Power:** The framework successfully distinguishes between non-populist and populist discourse. More importantly, it demonstrates the capacity to discriminate *between different types* of populism. The combination of the raw scores (e.g., `economic_populist_appeals` vs. `nationalist_exclusion`) and the derived tension metrics (`internal_external_focus_tension`) provides a robust toolkit for identifying and categorizing rhetorical strategies.

2.  **Framework-Corpus Fit:** The PDAF appears to be well-suited for analyzing contemporary American political discourse. Its dimensions capture the key themes of both left-wing and right-wing populist actors. The high confidence scores reported in the underlying data suggest that the analytical model was able to identify these features with a high degree of certainty. The framework's multi-dimensional nature prevents the oversimplification that might arise from a single populism score, instead revealing the distinct "flavor" of each speaker's rhetoric.

## 6. Discussion

### Theoretical Implications of Findings

The preliminary findings from this analysis have several theoretical implications for the study of populism. The clear statistical separation between an economic-focused and a nationalist-focused populist strategy suggests that populism may be best understood not as a single, monolithic style, but as a flexible rhetorical structure or "chassis." The core element of this chassis appears to be the `manichaean_people_elite_framing`. However, different "engines" of grievance—primarily economic inequality or national/cultural threat—can be attached to this chassis to create distinct political appeals.

This "chassis and engine" model challenges approaches that attempt to create a single, universal definition or measurement scale for populism. The data indicates that *how* the people and the elite are constructed, and *what* the central crisis is about, are as important as the presence of the populist structure itself. Future research could investigate whether this modular structure holds across different political and national contexts.

### Comparative Analysis and Archetypal Patterns

This analysis reveals three distinct rhetorical archetypes within the corpus:

1.  **The Institutionalist (John McCain):** Characterized by an almost complete absence of populist rhetoric (`salience_weighted_overall_populism_index` = 0.100). This style emphasizes pluralism, respect for democratic outcomes, and calls for unity. The discourse acknowledges challenges but frames them as problems to be solved collaboratively, not as an existential crisis caused by a malevolent elite. As John McCain stated: "These are difficult times for our country, and I pledge to him tonight to do all in my power to help him lead us through the many challenges we face" (Source: john_mccain_2008_concession.txt).

2.  **The Economic Insurgent (Bernie Sanders & Alexandria Ocasio-Cortez):** This archetype scores highest on the overall populism index. Its strategy is defined by a fusion of `manichaean_people_elite_framing`, `elite_conspiracy_systemic_corruption`, and `economic_populist_appeals`. The "elite" is a wealthy oligarchy, the "people" are the working and middle classes, and the "crisis" is economic inequality caused by a rigged system. This style constructs a broad, inclusive "people" united by economic interest, as Ocasio-Cortez does by welcoming anyone "willing to fight for someone you don’t know" regardless of identity (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt).

3.  **The Nationalist Defender (Steve King):** This archetype scores high on populism but with a different configuration. The strategy is driven by `nationalist_exclusion`, `anti_pluralist_exclusion`, and a `crisis_restoration_narrative` centered on constitutional and cultural decay. The threat is located externally (immigrants) or in internal actors seen as disloyal to a specific, traditionalist vision of the nation. The "people" are implicitly defined as the true, patriotic members of the nation-state who must be defended. As Steve King stated: "This is the time we must defend our Constitution..." (Source: steve_king_2017_house_floor.txt).

### Limitations and Future Directions

The primary limitation of this study is its N=4 sample size, which makes the findings highly preliminary and illustrative. The strong correlations observed could be artifacts of this small, purposive sample. Therefore, the most critical direction for future research is to apply the PDAF to a large, diverse corpus of political texts from various countries and ideological positions. This would allow for robust statistical testing of the archetypes and correlational patterns identified here.

Furthermore, this analysis is synchronic. A longitudinal analysis could track how rhetorical strategies evolve over time for individual speakers or political movements. Researchers may wish to explore whether populist actors shift between economic and nationalist appeals depending on the political context. Finally, integrating this quantitative textual analysis with other data, such as polling or voting records, could help establish the real-world effects of these different populist strategies.

## 7. Conclusion

This computational analysis, despite its limited scope, demonstrates the significant potential of the Populist Discourse Analysis Framework (PDAF) v10.0.0. By moving beyond a simple binary classification, the framework provides a nuanced, multi-dimensional, and quantitative assessment of populist rhetoric. The analysis successfully identified a non-populist baseline and distinguished between two distinct populist archetypes—the "Economic Insurgent" and the "Nationalist Defender"—present in the corpus.

The internal consistency of the statistical results, such as the theoretically coherent clustering of dimensions and the discriminatory power of the derived tension metrics, offers preliminary support for the framework's construct validity. The study suggests that populism is not a monolithic phenomenon but a flexible rhetorical structure that can be animated by different core grievances, primarily economic or nationalist in nature.

The key contribution of this report is the data-driven generation of testable hypotheses about the structure of populist communication. It provides a methodological blueprint for how advanced computational frameworks can deepen our understanding of complex political phenomena. The clear patterns that emerge even from a sample of four documents underscore the power of this approach and call for expanded research to validate these indicative findings on a larger scale.

## 8. Evidence Citations

**alexandria_ocasio_cortez_2025_fighting_oligarchy.txt**
*   As Alexandria Ocasio-Cortez stated: "We are witnessing an oligarchy in America. And that is when those with the most economic, political, and technological power destroy the public good to enrich themselves while millions of Americans pay the price."
*   As Alexandria Ocasio-Cortez stated: "He’s handed the keys to Elon Musk and is selling off our country for parts to the wealthiest people in the world for a kickback."
*   As Alexandria Ocasio-Cortez stated: "Honestly, no matter who you voted for in the past. No matter if you know all the right words to say, no matter your race, religion, gender identity, or status, no matter if you disagree with me on a couple of things. If you are willing to fight for someone you don’t know, you are welcome here."

**bernie_sanders_2025_fighting_oligarchy.txt**
*   As Bernie Sanders stated: "...you would not feel obliged to step on the backs of poor people to become even richer. But that is exactly what they are doing right now."
*   As Bernie Sanders stated: "That is what a rigged economy is about, and that is what we are going to change."
*   As Bernie Sanders stated: "We will not accept the richest guy in the world running all over Washington, making cuts to the Social Security Administration, cuts to the Veteran Administration, almost destroying the Department of Education, all so that they could give over a trillion dollars in tax breaks to the wealthiest 1%."

**john_mccain_2008_concession.txt**
*   As John McCain stated: "These are difficult times for our country, and I pledge to him tonight to do all in my power to help him lead us through the many challenges we face."
*   As John McCain stated: "I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together..."

**steve_king_2017_house_floor.txt**
*   As Steve King stated: "...to push Obamacare down the throats of the American people."
*   As Steve King stated: "We have a Constitution that's got to be restored. And instead of being restored, it would be destroyed by another presidential appointment."
*   As Steve King stated: "Sarah Root would be alive today if the President had done his job, if law enforcement had been allowed to do their job, if ICE had responded when local law enforcement called them."
*   As Steve King stated: "This is the time we must defend our Constitution and we must nominate and elect a president of the United States who will make those appointments to the Supreme Court who believe the Constitution means what it says."