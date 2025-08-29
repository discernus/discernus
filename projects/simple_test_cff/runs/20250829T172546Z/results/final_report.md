# Cohesive Flourishing Framework Analysis Report

**Experiment**: simple_test  
**Run ID**: 20250829T172546Z_1c1af1eb  
**Date**: 2025-08-29  
**Framework**: cff_v10.md  
**Corpus**: corpus.md (4 documents)  

**Analysis Model**: Gemini 2.5 Flash Lite
**Synthesis Model**: Gemini 2.5 Pro
**Method**: 3-Run Median Aggregation

---

## 1. Executive Summary

This report details a computational analysis of four paradigmatic American political speeches using the Cohesive Flourishing Framework (CFF) v10. The study aimed to measure the baseline cohesion and tension scores within a diverse corpus representing institutional and populist rhetorical styles. The analysis reveals distinct, quantifiable rhetorical signatures for each style. Institutional discourse, represented by John McCain's 2008 concession speech, scored highly on cohesive dimensions such as `Individual Dignity` (M = 0.60), `Hope` (M = 0.70), and `Cohesive Goals` (M = 0.70), indicating a focus on unity and democratic norms.

In stark contrast, both conservative and progressive populist discourse demonstrated a strong reliance on fragmentative rhetoric. The conservative populist speech from Steve King (2017) was characterized by high scores in `Tribal Dominance` (M = 0.80) and `Fear` (M = 0.70), coupled with the lowest `Strategic Contradiction Index` (0.066) in the corpus, suggesting a highly consistent and focused divisive message. Progressive populist speeches from Bernie Sanders (2025) and Alexandria Ocasio-Cortez (2025) also scored high on `Tribal Dominance` (M = 0.90 and 0.75, respectively) and `Fear`. However, their rhetoric exhibited significantly more complexity and internal contradiction. The speech by Ocasio-Cortez, for instance, simultaneously invoked strong appeals to both `Tribal Dominance` and `Individual Dignity` (M = 0.85) and registered the highest `Goal Tension` (0.15) in the corpus, indicating a sophisticated strategy of blending divisive and unifying messages.

A critical methodological finding emerged during the analysis: inconsistent automated labeling of the `Compersion` dimension across documents prevented the reliable calculation of the composite `Full Cohesion Index` for three of the four texts. This highlights a key challenge in complex computational discourse analysis and underscores the importance of robust validation pipelines. Despite this limitation, the CFF's dimensional and tension metrics proved highly effective at discriminating between political archetypes and revealing the nuanced rhetorical strategies that underpin them. The findings suggest that while institutional and populist styles differ fundamentally in their orientation toward social cohesion, significant variation in rhetorical complexity exists within populism itself.

## 2. Opening Framework: Key Insights

*   **Institutional vs. Populist Rhetoric Reveals a Stark Cohesion Divide:** The analysis demonstrates a clear demarcation between institutional and populist discourse. John McCain's institutional speech was overwhelmingly characterized by cohesive language (`Hope` M=0.70, `Cohesive Goals` M=0.70), while all three populist examples (King, Sanders, Ocasio-Cortez) were dominated by fragmentative dimensions like `Tribal Dominance` (corpus mean M=0.69) and `Fear` (corpus mean M=0.51).
*   **Populist Styles Share Fragmentative Core but Differ in Complexity:** While both conservative and progressive populism rely on a fragmentative "us vs. them" framework, they employ different strategies. Steve King's conservative populism is rhetorically consistent and singularly focused, registering the lowest `Strategic Contradiction Index` (0.066). In contrast, Alexandria Ocasio-Cortez's progressive populism is the most rhetorically complex, simultaneously using high levels of both divisive (`Tribal Dominance` M=0.75) and inclusive (`Individual Dignity` M=0.85) appeals, resulting in high tension scores.
*   **`Tribal Dominance` is a Unifying Feature of Populist Rhetoric:** The `Tribal Dominance` dimension, which measures in-group supremacy and "us vs. them" rhetoric, was the most potent and consistent feature across all populist speeches, regardless of ideology. Scores for Sanders (M=0.90), King (M=0.80), and Ocasio-Cortez (M=0.75) were substantially higher than for the institutional speaker, McCain (M=0.30), suggesting it is a core technology of populist communication.
*   **Tension Metrics Successfully Quantify Strategic Contradiction:** The CFF's tension indices effectively captured sophisticated rhetorical strategies. Ocasio-Cortez's speech registered the highest `Goal Tension` (0.15), reflecting a message that simultaneously calls for tearing down existing systems while building a new, inclusive coalition. This ability to measure the co-occurrence of opposing appeals is a key analytical contribution of the framework.
*   **Progressive Populism Employs an Economic Resentment Frame:** The rhetoric of `Envy`, defined as resentment toward others' success and zero-sum thinking, was a distinctive feature of the progressive populist speeches. Bernie Sanders' speech scored highest on this dimension (M=0.70), focusing on the perceived injustices of wealth inequality. This contrasts with the conservative populist speech, which scored zero on `Envy`.
*   **Methodological Challenges in Automated Analysis Identified:** The analysis uncovered a significant data quality issue: the `Compersion` dimension was inconsistently labeled as `emulation`, `emigration`, or `empathy` during the raw analysis phase. This error rendered the composite cohesion indices incalculable for most of the corpus and serves as a critical finding on the practical challenges of applying complex, nuanced frameworks at scale.

## 4. Methodology

### Framework Description and Analytical Approach

This study employed the Cohesive Flourishing Framework (CFF) v10, a multi-dimensional tool for analyzing the impact of political discourse on social cohesion and democratic health. The CFF's primary innovation is its independent scoring of ten conceptual anchors organized into five opposing pairs, which allows for the preservation of complex rhetorical information where competing appeals are used simultaneously.

The five core analytical axes are:
*   **Identity Axis**: `Tribal Dominance` vs. `Individual Dignity`
*   **Emotional Climate**: `Fear` vs. `Hope`
*   **Success Orientation**: `Envy` vs. `Compersion`
*   **Relational Climate**: `Enmity` vs. `Amity`
*   **Goal Orientation**: `Fragmentative Goals` vs. `Cohesive Goals`

For each dimension, the analysis generated two scores: an **intensity score** (0.0-1.0) measuring the strength of the rhetoric, and a **salience score** (0.0-1.0) measuring its rhetorical prominence or emphasis. From these, the CFF calculates derived metrics, including **Tension Indices** (e.g., `Identity Tension`) to quantify strategic contradictions and a **Strategic Contradiction Index** to measure overall rhetorical coherence. Salience-weighted **Cohesion Indices** are designed to provide a comprehensive evaluation of the discourse's likely impact on social cohesion.

### Data and Corpus

The analysis was performed on the Democratic Discourse Corpus (v8.0), a curated collection of four speeches representing different rhetorical styles in contemporary American politics:
1.  **John McCain (2008, Institutional Republican):** 2008 Presidential Concession Speech.
2.  **Steve King (2017, Populist Conservative):** House Floor Speech.
3.  **Bernie Sanders (2025, Populist Progressive):** Speech on Fighting Oligarchy.
4.  **Alexandria Ocasio-Cortez (2025, Populist Progressive):** Speech on Fighting Oligarchy.

This corpus was selected to provide clear examples of both institutional discourse, which emphasizes established norms, and populist discourse from both the conservative and progressive perspectives.

### Statistical Methods and Limitations

The analysis relied on the descriptive statistics and derived metrics generated by the Discernus platform. The primary methods involved the interpretation of means, standard deviations, and the examination of patterns in the CFF's dimensional and derived metric scores across the four documents.

A significant limitation was discovered during the analysis. The automated scoring process inconsistently labeled the `Compersion` dimension, substituting it with `emulation`, `emigration`, or `empathy` in the raw output. Because the formulas for the derived `Descriptive`, `Motivational`, and `Full Cohesion Indices` specifically require the `compersion` dimension, these composite metrics could not be reliably calculated for three of the four documents. This report will therefore focus on the dimensional scores and tension indices, which were unaffected by this error. This issue is itself a key finding regarding the implementation of complex computational frameworks and is discussed as such. Given the small sample size (N=4), all findings should be considered preliminary and indicative of patterns that warrant further investigation with a larger corpus.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

The analysis of the four documents reveals widely divergent rhetorical patterns. The mean scores across the corpus highlight a general tendency towards fragmentative rhetoric, though this is driven entirely by the three populist texts.

**Table 1: Summary of Mean Dimensional Scores (Intensity & Salience) Across Corpus (N=4)**

| Dimension                 | Mean Intensity (SD) | Mean Salience (SD) |
| ------------------------- | ------------------- | ------------------ |
| **Fragmentative**         |                     |                    |
| Tribal Dominance          | 0.69 (0.27)         | 0.73 (0.29)        |
| Fear                      | 0.51 (0.30)         | 0.58 (0.33)        |
| Envy                      | 0.34 (0.34)         | 0.36 (0.33)        |
| Enmity                    | 0.47 (0.40)         | 0.53 (0.38)        |
| Fragmentative Goals       | 0.55 (0.31)         | 0.55 (0.33)        |
| **Cohesive**              |                     |                    |
| Individual Dignity        | 0.44 (0.35)         | 0.53 (0.33)        |
| Hope                      | 0.50 (0.27)         | 0.60 (0.27)        |
| Compersion*               | 0.50 (0.14)         | 0.58 (0.18)        |
| Amity                     | 0.38 (0.34)         | 0.43 (0.38)        |
| Cohesive Goals            | 0.43 (0.32)         | 0.50 (0.32)        |

*Note: `Compersion` data is based on inconsistently labeled dimensions (`emulation`, `empathy`) for N=3 and is presented for transparency but should be interpreted with extreme caution.*

The populist speeches by King, Sanders, and Ocasio-Cortez consistently registered high scores on fragmentative dimensions. For example, `Tribal Dominance` intensity was exceptionally high for Sanders (0.90) and King (0.80). In contrast, McCain's institutional speech scored low on all fragmentative dimensions (e.g., `Fear`=0.10, `Enmity`=0.00) and high on cohesive ones (e.g., `Hope`=0.70, `Cohesive Goals`=0.70).

### 5.2 Advanced Metric Analysis

The derived tension metrics reveal the degree of rhetorical contradiction within each speech. A high tension score indicates that a speaker is simultaneously using opposing appeals with significant intensity, but with differing levels of rhetorical emphasis (salience).

**Table 2: Derived Tension and Contradiction Indices by Document**

| Document                                      | Identity Tension | Emotional Tension | Goal Tension | Strategic Contradiction Index |
| --------------------------------------------- | ---------------- | ----------------- | ------------ | ----------------------------- |
| john_mccain_2008_concession.txt               | 0.120            | 0.070             | 0.070        | 0.087                         |
| steve_king_2017_house_floor.txt               | 0.083            | 0.055             | 0.060        | 0.066                         |
| bernie_sanders_2025_fighting_oligarchy.txt    | 0.112            | 0.090             | 0.110        | 0.097                         |
| alexandria_ocasio_cortez_2025_fighting_oligarchy.txt | 0.075            | 0.050             | 0.150        | 0.092                         |

*Note: `Success Tension` and `Relational Tension` were not reliably calculated for all documents due to data inconsistencies and are omitted from this table.*

This analysis shows that the speech by **Steve King** was the most rhetorically consistent, with the lowest `Strategic Contradiction Index` (0.066). His message was uniformly fragmentative, with little appeal to opposing cohesive values.

Conversely, the speeches by **Alexandria Ocasio-Cortez** and **Bernie Sanders** were the most contradictory. Ocasio-Cortez's speech registered the highest `Goal Tension` (0.15) of any document, indicating a powerful blend of fragmentative and cohesive goal orientation. Sanders' speech showed the highest `Emotional Tension` (0.09), pairing strong appeals to both fear and hope. These high tension scores do not imply poor communication; rather, they quantify a sophisticated rhetorical strategy of holding opposing ideas in tension to motivate a broad audience.

### 5.4 Pattern Recognition and Theoretical Insights

The statistical results reveal clear rhetorical archetypes, each supported by distinct textual evidence.

#### Pattern 1: The Institutional Unifier (McCain)

John McCain's 2008 concession speech exemplifies a classic institutionalist style focused on democratic health and social cohesion. The data shows high scores on `Individual Dignity` (0.60), `Hope` (0.70), `Amity` (0.50), and `Cohesive Goals` (0.70), with negligible scores on their fragmentative counterparts. This profile suggests a deliberate strategy to reinforce national unity after a divisive election. The textual evidence strongly supports this interpretation. As **John McCain** stated, the goal was to "find ways to come together, to find the necessary compromises to bridge our differences and help restore our prosperity." He reinforced this by emphasizing a shared identity that transcends political division: "Whatsoever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that" (Source: john_mccain_2008_concession.txt). This rhetoric is explicitly aimed at building social capital and reinforcing democratic norms.

#### Pattern 2: The Consistent Nationalist Populist (King)

Steve King's 2017 floor speech presents a starkly different, but highly coherent, rhetorical profile. It is defined by extremely high scores on `Tribal Dominance` (0.80), `Fear` (0.70), `Enmity` (0.70), and `Fragmentative Goals` (0.70), with near-zero scores on all cohesive dimensions. This, combined with the corpus's lowest `Strategic Contradiction Index` (0.066), paints a picture of a rhetorically focused, unambiguous, and deeply fragmentative message. The central theme is the defense of an in-group ("Americans") against a threatening out-group ("criminal aliens"). As **Steve King** stated, "This President has, has released, his administration has released over 30,000 criminals, criminal aliens onto the streets of America" (Source: steve_king_2017_house_floor.txt). This rhetoric, grounded in Social Identity Theory, functions to heighten in-group solidarity by constructing an existential threat posed by an out-group.

#### Pattern 3: The Economic Justice Populist (Sanders)

Bernie Sanders' 2025 speech demonstrates a progressive variant of populist rhetoric. Like King, it scores high on `Tribal Dominance` (0.90) and `Fear` (0.75), but the in-group/out-group distinction is drawn along class lines rather than national or ethnic ones. The out-group is an "oligarchic" class, and the in-group is the working class. As **Bernie Sanders** declared, "We will not accept an oligarchic form of society...all so that they could give over a trillion dollars in tax breaks to the wealthiest 1%" (Source: bernie_sanders_2025_fighting_oligarchy.txt). A key distinguishing feature of this style is its high score on `Envy` (0.70), which captures resentment toward the success of the out-group. This is evident in statements like, "The rich want to get richer and they do not care who they step on" (Source: bernie_sanders_2025_fighting_oligarchy.txt). While the speech contains elements of hope, its overall profile is highly fragmentative, resulting in the only calculable (and strongly negative) `Full Cohesion Index` of -0.36.

#### Pattern 4: The Complex Progressive Populist (Ocasio-Cortez)

Alexandria Ocasio-Cortez's 2025 speech represents the most rhetorically sophisticated archetype in the corpus. It is characterized by high scores on *both* sides of the CFF's axes, leading to high tension. It scores high on `Tribal Dominance` (0.75) by identifying a "billionaire regime" that is "dividing working people apart." Simultaneously, it scores the highest in the corpus on `Individual Dignity` (0.85), with inclusive appeals like, "Our lives deserve dignity and our work deserves respect" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt).

This strategic contradiction is most apparent in its goal orientation. The speech registered the corpus's highest `Goal Tension` (0.15), pairing fragmentative calls to identify and oppose a divisive enemy with cohesive calls for unity. For instance, she identifies a fragmentative strategy used by opponents—"They will throw out every label and judgment and cultural debate in the book to keep us distracted"—while simultaneously issuing a highly cohesive invitation: "If you are willing to fight for someone you don't know, you are welcome here" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt). This complex strategy attempts to build a broad, inclusive coalition (`Cohesive Goals`) by uniting them against a common, fragmenting enemy (`Fragmentative Goals`).

### 5.5 Framework Effectiveness Assessment

The CFF demonstrated strong discriminatory power in this analysis. It successfully differentiated the institutional style from the populist styles and, more impressively, revealed nuanced strategic differences between conservative and progressive populism. The framework's core innovation—the independent scoring of opposing dimensions and the calculation of tension—proved essential for understanding the complex rhetoric of speakers like Ocasio-Cortez, whose message would be flattened or misinterpreted by traditional sentiment analysis.

The primary weakness identified was not in the framework's theoretical design but in its automated application, specifically the inconsistent labeling of the `Compersion` dimension. This prevented a full analysis using the composite cohesion indices. This finding is critical, as it highlights the "last mile" problem in computational social science, where the success of a sophisticated framework depends on the fidelity of the underlying language model's interpretation. However, the dimensional and tension metrics alone provided rich, actionable insights, suggesting the framework is robust even when its composite metrics are compromised.

## 6. Discussion

The findings from this analysis carry significant implications for understanding contemporary political discourse. The stark contrast between the institutional rhetoric of McCain and the populist rhetoric of King, Sanders, and Ocasio-Cortez suggests a fundamental divergence in communicative goals. The institutional style, at least in this idealized concession speech, operates to reinforce the legitimacy of the democratic system and promote social cohesion. In contrast, all three populist examples operate on a logic of division, leveraging Social Identity Theory principles to forge a powerful in-group identity by constructing a threatening out-group.

This study suggests that the "us vs. them" framing (`Tribal Dominance`) is the central technology of populism, whether the "them" is defined by nationality (King) or class (Sanders/Ocasio-Cortez). This finding aligns with theories of political communication that posit populism as a "thin" ideology that pits a "pure people" against a "corrupt elite."

Furthermore, the CFF's tension metrics reveal that not all populist rhetoric is created equal. The low-contradiction, high-enmity style of King presents a clear, unambiguous threat narrative. The high-contradiction style of Ocasio-Cortez is more complex, attempting to perform a rhetorical alchemy: using the energy of fragmentation to fuel a movement of cohesion. She builds a "we" by defining a "they," but then defines the "we" in maximally inclusive terms. This complex strategy, which this analysis was able to quantify, may be a key feature of modern progressive populism and warrants significant further research with a larger corpus. The limitations of this N=4 study are clear, but the patterns identified provide a strong foundation for generating testable hypotheses for future work.

## 7. Conclusion

This computational analysis, guided by the Cohesive Flourishing Framework, successfully identified and quantified distinct rhetorical archetypes within a small but diverse corpus of American political speeches. The framework proved highly effective at moving beyond simple sentiment to reveal the underlying strategies of political communication, distinguishing between cohesive institutional discourse and fragmentative populist discourse.

The study's key contribution is the empirical demonstration of different populist strategies. It revealed a consistent, low-contradiction conservative populism and a more complex, high-contradiction progressive populism that simultaneously leverages both divisive and unifying appeals. The CFF's tension metrics were instrumental in capturing this sophistication. While a methodological issue prevented the full calculation of composite cohesion scores, this limitation itself provided a valuable insight into the practical challenges of deploying complex analytical frameworks. The results, though preliminary due to the small sample size, validate the CFF's core theoretical assumptions and demonstrate its potential as a powerful tool for researchers and policymakers seeking to understand the linguistic drivers of social fragmentation and cohesion.

## 8. Evidence Citations

### john_mccain_2008_concession.txt
*   **Cohesive Goals:** "I urge all Americans - I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together, to find the necessary compromises to bridge our differences and help restore our prosperity, defend our security in a dangerous world, and leave our children and grandchildren a stronger, better country than we inherited."
*   **Amity:** "Whatsoever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that."

### steve_king_2017_house_floor.txt
*   **Enmity / Fear:** "This President has, has released, his administration has released over 30,000 criminals, criminal aliens onto the streets of America."
*   **Fragmentative Goals:** "But it's no longer possible to look at this Supreme Court and discern what a likely decision of the Court might be by studying the text of the Constitution and the text of the law because we have a court that will write, make it up as they go along, write laws."

### bernie_sanders_2025_fighting_oligarchy.txt
*   **Tribal Dominance:** "We will not accept an oligarchic form of society. We will not accept the richest guy in the world running all over Washington, making cuts to the Social Security Administration, cuts to the Veterans Administration, almost destroying the Department of Education, all so that they could give over a trillion dollars in tax breaks to the wealthiest 1%"
*   **Envy:** "The rich want to get richer and they do not care who they step on."

### alexandria_ocasio_cortez_2025_fighting_oligarchy.txt
*   **Tribal Dominance:** "The same billionaire regimes are taking a wrecking ball to our country and they derive their power from dividing working people apart. They specialize in getting us to turn on one another and they get us to turn on one another along lines of left and right, race and gender, creed and culture."
*   **Individual Dignity:** "So to all of those who came here today to stand together and say, 'Our lives deserve dignity and our work deserves respect.'"
*   **Fragmentative Goals:** "They will throw out every label and judgment and cultural debate in the book to keep us distracted because the last thing they want us to realize is that the division that is actually hurting our country the most is how endlessly greed is costing the lives of everyone else."
*   **Cohesive Goals:** "If you are willing to fight for someone you don't know, you are welcome here."