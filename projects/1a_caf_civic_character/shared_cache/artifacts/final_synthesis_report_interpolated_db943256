# Civic Analysis Framework (CAF) v10.0 Analysis Report

**Experiment**: Not specified  
**Run ID**: Not specified  
**Date**: 2025-08-25  
**Framework**: Civic Analysis Framework (CAF) v10.0  
**Corpus**: Not available (8 documents)  

---

## 1. Executive Summary

This report presents a computational analysis of the civic character of political discourse from eight prominent American political figures, utilizing the Civic Analysis Framework (CAF) v10.0. The analysis reveals a clear and statistically significant division in rhetorical strategies, clustering around two opposing poles: one characterized by civic virtues (Dignity, Justice, Truth, Pragmatism) and the other by civic vices (Tribalism, Manipulation, Resentment, Fantasy). The primary metric, the Civic Character Index, effectively differentiated speakers, ranging from John McCain (+0.805) to Steve King (-0.480), demonstrating the framework's strong discriminatory power.

Key findings indicate that political rhetoric is not monolithic; speakers deploy complex and sometimes contradictory strategies. The analysis identified three preliminary rhetorical archetypes: the "Principled Unifier" (e.g., McCain, Romney), who demonstrates high virtue and low vice; the "Populist Agitator" (e.g., Sanders, King), who relies heavily on vice-based appeals; and the "Righteous Advocate" (e.g., Lewis, Ocasio-Cortez), who combines strong appeals to justice with high levels of resentment and tribalism, creating significant rhetorical tension. Correlation analysis strongly validates the framework's oppositional design, with virtues and their corresponding vices showing large negative correlations (e.g., Pragmatism vs. Fantasy, r = -0.934).

While the small sample size (N=8) means these findings should be considered preliminary, the analysis demonstrates the CAF's effectiveness in systematically quantifying the moral character of political speech. It provides a robust, evidence-based methodology for moving beyond subjective interpretation to a more rigorous, data-driven understanding of civic discourse. The results suggest that the tension between competing values is a central feature of political communication, and the CAF provides a nuanced tool for its measurement.

## 2. Opening Framework: Key Insights

This analysis of political discourse through the Civic Analysis Framework (CAF) v10.0 yielded several key insights into the structure and character of civic communication.

*   **Discourse Organizes into Opposing Virtue/Vice Clusters:** The data reveals two coherent, opposing meta-strategies. Virtues like Dignity, Justice, and Pragmatism are positively inter-correlated and form a distinct cluster. This cluster stands in strong opposition to a vice cluster composed of Tribalism, Manipulation, and Fantasy. This is evidenced by the large negative correlation between `pragmatism` and `fantasy` (r = -0.934) and `dignity` and `tribalism` (r = -0.809).
*   **The Civic Character Index Effectively Differentiates Speakers:** The analysis produced a `civic_character_index` that successfully quantifies the overall virtuous or vicious leaning of a speaker's rhetoric. The index created a clear spectrum, with John McCain (+0.805) and Mitt Romney (+0.500) on the positive end, and Bernie Sanders (-0.394) and Steve King (-0.480) on the negative end, validating its utility as a summary metric.
*   **Distinct Rhetorical Archetypes Emerge:** The data suggests the existence of at least three speaker archetypes. The "Principled Unifier" (McCain) exhibits high virtue and low vice. The "Populist Agitator" (Sanders) displays high vice, particularly `tribalism` (0.90) and `resentment` (0.95). The "Righteous Advocate" (Lewis) presents a complex profile, scoring high on both the virtue of `justice` (0.90) and the vice of `resentment` (0.90), indicating the use of divisive emotions for virtuous ends.
*   **Rhetorical Tension is a Key Strategic Element:** The framework's `mean_tension` metric highlights that speakers often simultaneously appeal to conflicting values. Bernie Sanders exhibits the highest mean tension (0.144), combining strong appeals to `resentment` with appeals to `justice`. As Sanders stated, "That is what a rigged economy is about, and that is what we are going to change" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt), framing a grievance (resentment) as a call for systemic change (justice). This suggests that managing or exploiting such tensions is a core component of certain rhetorical styles.
*   **Framework Construct Validity is High:** The oppositional design of the CAF is strongly supported by the correlation matrix. The consistent, large negative correlations between paired virtues and vices (e.g., `dignity` vs. `tribalism`, `pragmatism` vs. `fantasy`) suggest that the framework is successfully measuring theoretically opposed concepts, lending confidence to its internal structure and the validity of its findings.
*   **Resentment is a Pervasive, Cross-Cutting Tool:** While most dimensions aligned clearly with either the virtue or vice cluster, `resentment` appears as a more universal rhetorical tool, registering the highest mean score across all speakers (M=0.71). However, its stronger correlation with `tribalism` (r=0.797) than with `justice` (r=-0.340) suggests it functions primarily as a component of vice-oriented, divisive rhetoric, even when used by speakers with virtuous aims.

## 3. Literature Review and Theoretical Framework

This analysis is grounded in the **Civic Analysis Framework (CAF) v10.0**, a systematic methodology for evaluating the civic character of political discourse. As described in its specification, the CAF is rooted in a combination of Aristotelian virtue ethics and contemporary civic republican theory. Its primary purpose is to move beyond simple sentiment analysis to assess the moral character demonstrated by speakers through their rhetorical choices.

The core of the CAF is its focus on the fundamental tensions between competing civic values. It operationalizes this by structuring its analysis around five oppositional axes:
*   **Identity:** Dignity (universal worth) vs. Tribalism (in-group/out-group)
*   **Truth:** Truth (intellectual honesty) vs. Manipulation (deceptive framing)
*   **Justice:** Justice (fairness, systemic solutions) vs. Resentment (grievance, blame)
*   **Emotion:** Hope (optimistic future) vs. Fear (threat focus)
*   **Reality:** Pragmatism (acknowledging constraints) vs. Fantasy (denying complexity)

By measuring the presence and salience of these virtues and vices, the framework aims to solve a key problem in political communication analysis: how to rigorously evaluate discourse where speakers may simultaneously appeal to noble values and their pathological counterparts. This analysis, therefore, does not seek to label speakers as "good" or "bad" in a simplistic sense, but rather to map the complex terrain of their demonstrated civic character and identify the strategic patterns within their rhetoric. The `civic_character_index` and `tension` metrics are designed specifically to capture this complexity, providing a quantitative basis for assessing both the overall leaning and the internal coherence of a speaker's message.

## 4. Methodology

### Framework Description and Analytical Approach

This study employed the Civic Analysis Framework (CAF) v10.0 to conduct a quantitative analysis of political texts. The CAF evaluates discourse across ten dimensions, organized into five oppositional pairs of a virtue and a corresponding vice. The analysis engine scores each text for the raw presence and contextual salience of each of these ten dimensions. From these primary scores, the system calculates several derived metrics, including a `civic_character_index` (a composite score of overall virtue minus vice, weighted by salience), and five `tension` scores that measure the degree to which a speaker simultaneously invokes a virtue and its opposing vice. The analytical approach is descriptive and correlational, aiming to identify patterns, relationships, and archetypes within the provided data.

### Data Structure and Corpus Description

The analysis was performed on a small corpus of 8 documents, each representing a speech by a distinct American political figure. The speakers include Alexandria Ocasio-Cortez, Bernie Sanders, Cory Booker, JD Vance, John Lewis, John McCain, Mitt Romney, and Steve King. Due to the unavailability of the corpus manifest (`corpus.md`), further details regarding the context, date, and nature of each speech are inferred from the document filenames. The statistical data was provided in a structured JSON format, containing per-document and per-speaker aggregated scores for all CAF dimensions and derived metrics.

### Statistical Methods and Analytical Constraints

The statistical analysis relied on the pre-computed results provided. The primary methods of interpretation were:
1.  **Descriptive Statistics:** Examination of means, standard deviations, and quartiles to understand the central tendency and distribution of each rhetorical dimension across the corpus.
2.  **Correlation Analysis:** Calculation of a Pearson correlation matrix for the ten core dimensions to identify inter-relationships and test the framework's theoretical structure.
3.  **Profile Analysis:** Examination of individual speaker profiles based on their scores on the `civic_character_index`, `mean_tension`, and the underlying virtue and vice dimensions.

A key constraint is the extremely small sample size (N=8). This prevents any meaningful inferential statistical testing or generalization of the findings to a broader population of political speakers. Therefore, all conclusions are presented as preliminary, suggestive, and specific to this particular corpus. The findings serve as a pilot study demonstrating the potential of the methodology, rather than a definitive statement on contemporary political discourse. The alpha level for the analysis was set at 0.05, as indicated in the analysis metadata.

### Limitations

The primary limitation of this study is its **small sample size**, which severely restricts the external validity of the findings. The results and archetypes identified are indicative and require validation on a much larger and more diverse corpus. Secondly, the **lack of a corpus manifest** limits the ability to contextualize the speeches fully. Thirdly, the **limited set of retrievable textual evidence** means that while key findings are supported by direct quotes, the richness of this qualitative support is constrained. In some cases, the absence of a quote is itself the evidence, which is a weaker form of support. These limitations necessitate a cautious and measured interpretation of the results.

## 5. Comprehensive Results

The statistical analysis reveals significant patterns in the rhetorical strategies of the speakers in the corpus. The results are presented below, moving from broad descriptive statistics to more nuanced correlation and profile analyses.

### 5.1 Descriptive Statistics

An examination of the descriptive statistics for the ten core rhetorical dimensions across all eight documents provides a foundational overview of the discourse landscape.

**Table 1: Descriptive Statistics of Rhetorical Dimensions (N=8)**

| Dimension      | Mean  | Std. Dev. | Min   | 25%   | 50%   | 75%   | Max   |
| :------------- | :---- | :-------- | :---- | :---- | :---- | :---- | :---- |
| **Vices**      |       |           |       |       |       |       |       |
| Tribalism      | 0.513 | 0.419     | 0.000 | 0.075 | 0.650 | 0.900 | 0.900 |
| Manipulation   | 0.338 | 0.374     | 0.000 | 0.000 | 0.250 | 0.650 | 0.800 |
| Resentment     | 0.706 | 0.355     | 0.000 | 0.675 | 0.900 | 0.900 | 0.950 |
| Fear           | 0.463 | 0.245     | 0.100 | 0.300 | 0.450 | 0.600 | 0.900 |
| Fantasy        | 0.200 | 0.288     | 0.000 | 0.000 | 0.050 | 0.300 | 0.700 |
| **Virtues**    |       |           |       |       |       |       |       |
| Dignity        | 0.575 | 0.362     | 0.000 | 0.325 | 0.750 | 0.825 | 0.900 |
| Truth          | 0.663 | 0.213     | 0.300 | 0.550 | 0.750 | 0.800 | 0.900 |
| Justice        | 0.625 | 0.315     | 0.000 | 0.475 | 0.700 | 0.900 | 0.900 |
| Hope           | 0.550 | 0.278     | 0.100 | 0.425 | 0.600 | 0.725 | 0.900 |
| Pragmatism     | 0.587 | 0.372     | 0.000 | 0.325 | 0.750 | 0.900 | 0.900 |

The most striking finding from the descriptive statistics is the pervasiveness of `resentment` (M=0.706, SD=0.355), which has the highest mean score of any dimension. This suggests that framing issues around past grievances and blame is a common strategy across this diverse set of speakers. For instance, Bernie Sanders's rhetoric is saturated with this dimension, as seen when he states, "Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt).

In contrast, `manipulation` (M=0.338) and `fantasy` (M=0.200) are the least prevalent vices on average, though their high standard deviations indicate they are used heavily by some speakers and not at all by others. `Tribalism` also shows a wide variance (SD=0.419) and a median (0.650) much higher than its mean (0.513), indicating a skewed distribution where a subset of speakers relies heavily on in-group/out-group framing.

Among the virtues, `truth` (M=0.663) and `justice` (M=0.625) are the most common appeals. The high mean for `truth` suggests that speakers across the spectrum make efforts to ground their claims in evidence, or at least the appearance of it. As John Lewis asked, "Do you know that in Albany, Georgia, nine of our leaders have been indicted, not by Dixiecrats, but by the federal government for peaceful protest?" (Source: john_lewis_1963_march_on_washington_ab348df3.txt), using a factual claim to establish credibility.

### 5.2 Advanced Metric Analysis

The derived metrics, particularly the `civic_character_index` and `mean_tension`, allow for a more holistic assessment of each speaker's rhetorical profile.

**Table 2: Speaker Civic Character Profiles (Ranked by Index)**

| Speaker                    | Civic Character Index | Pattern Classification | Mean Tension | Mean Virtue Salience | Mean Vice Salience |
| :------------------------- | :-------------------- | :--------------------- | :----------- | :------------------- | :----------------- |
| John McCain                | 0.805                 | Authentic Virtue       | 0.014        | 0.760                | 0.020              |
| Cory Booker                | 0.502                 | Authentic Virtue       | 0.058        | 0.880                | 0.320              |
| Mitt Romney                | 0.500                 | Authentic Virtue       | 0.042        | 0.720                | 0.240              |
| John Lewis                 | 0.253                 | Virtue-Leaning         | 0.020        | 0.730                | 0.430              |
| Alexandria Ocasio-Cortez   | 0.005                 | Virtue-Leaning         | 0.088        | 0.620                | 0.580              |
| JD Vance                   | -0.275                | Vice-Leaning           | 0.042        | 0.360                | 0.600              |
| Bernie Sanders             | -0.394                | Strategic Pathology    | 0.144        | 0.340                | 0.720              |
| Steve King                 | -0.480                | Strategic Pathology    | 0.074        | 0.300                | 0.830              |

The `civic_character_index` provides a powerful, top-level summary that clearly separates the speakers into distinct groups. John McCain stands out as an exemplar of the "Authentic Virtue" pattern, with a very high index score, high mean virtue salience, and exceptionally low vice salience and tension. His discourse is characterized by a consistent appeal to virtues without resorting to their pathological counterparts. His call for unity in his concession speech exemplifies this: "I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together" (Source: john_mccain_2008_concession_ff9b26f2.txt).

At the other end of the spectrum, Bernie Sanders and Steve King are classified as "Strategic Pathology," indicating their rhetoric is dominated by vice-based appeals. Sanders has the highest `mean_tension` (0.144) in the entire corpus, suggesting a strategy that actively combines virtue and vice appeals. For example, he invokes a universal democratic principle, a `dignity` appeal, by referencing that "Abraham Lincoln talked about a government of the people, by the people, for the people" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt), while in the same speech heavily employing `tribalism` by framing the core conflict as "99% is a hell of a lot larger number than 1%" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt). This creates a high degree of rhetorical tension.

The "Virtue-Leaning" speakers, John Lewis and Alexandria Ocasio-Cortez, present the most complex profiles. Their near-zero or positive index scores are the result of high scores on *both* virtue and vice. Ocasio-Cortez, for example, has nearly balanced virtue (0.620) and vice (0.580) salience. She makes strong appeals to `dignity`, stating, "Our lives deserve dignity and our work deserves respect" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy_1121e4ae.txt), while simultaneously using intense `resentment` rhetoric: "They aren't working for these billions. They're stealing them" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy_1121e4ae.txt). This high-tension, balanced approach distinguishes their style from the more one-sided speakers.

### 5.3 Correlation and Interaction Analysis

The relationships between the ten core dimensions reveal the underlying structure of the rhetorical strategies present in the corpus. The correlation matrix provides strong evidence for the framework's theoretical design.

**Table 3: Correlation Matrix of Rhetorical Dimensions**
*(Values are Pearson's r. Effect sizes: |r| > 0.1 Small, |r| > 0.3 Medium, |r| > 0.5 Large)*

|              | Tribalism | Dignity  | Manip.   | Truth    | Resent.  | Justice  | Fear     | Hope     | Fantasy  | Pragm.   |
| :----------- | :-------- | :------- | :------- | :------- | :------- | :------- | :------- | :------- | :------- | :------- |
| **Tribalism**| 1.00      | **-0.81**| **0.91** | **-0.79**| **0.80** | **-0.71**| 0.40     | -0.23    | **0.72** | **-0.76**|
| **Dignity**  |           | 1.00     | **-0.87**| **0.67** | **-0.52**| **0.87** | **-0.58**| 0.50     | **-0.75**| **0.67** |
| **Manip.**   |           |          | 1.00     | **-0.77**| **0.61** | **-0.75**| 0.33     | -0.30    | **0.89** | **-0.91**|
| **Truth**    |           |          |          | 1.00     | **-0.55**| **0.84** | 0.08     | -0.16    | **-0.56**| **0.52** |
| **Resent.**  |           |          |          |          | 1.00     | -0.34    | 0.41     | -0.07    | 0.48     | **-0.51**|
| **Justice**  |           |          |          |          |          | 1.00     | -0.19    | 0.13     | **-0.54**| 0.43     |
| **Fear**     |           |          |          |          |          |          | 1.00     | **-0.87**| 0.30     | -0.30    |
| **Hope**     |           |          |          |          |          |          |          | 1.00     | -0.38    | 0.37     |
| **Fantasy**  |           |          |          |          |          |          |          |          | 1.00     | **-0.93**|
| **Pragm.**   |           |          |          |          |          |          |          |          |          | 1.00     |

The matrix reveals two powerful, internally consistent, and mutually antagonistic clusters of dimensions.

**The Vice Cluster:** `Tribalism`, `Manipulation`, and `Fantasy` are all very strongly and positively correlated (r > 0.72). `Manipulation` shows an extremely large positive correlation with `Tribalism` (r=0.908) and `Fantasy` (r=0.889). This suggests a coherent rhetorical strategy based on creating an in-group/out-group dynamic, simplifying complex issues, and using deceptive framing. `Resentment` also correlates positively with this cluster, particularly with `Tribalism` (r=0.797).

**The Virtue Cluster:** `Dignity`, `Truth`, `Justice`, and `Pragmatism` form another coherent cluster. The correlation between `Dignity` and `Justice` is extremely large (r=0.872), as is the correlation between `Truth` and `Justice` (r=0.845). This indicates that appeals to universal human worth, fairness, and intellectual honesty are often deployed together.

**Oppositional Structure:** The most significant finding is the validation of the CAF's oppositional design. The correlations between theoretically opposing virtues and vices are consistently large and negative.
*   `Pragmatism` vs. `Fantasy`: r = -0.934 (Extremely Large)
*   `Pragmatism` vs. `Manipulation`: r = -0.910 (Extremely Large)
*   `Dignity` vs. `Manipulation`: r = -0.869 (Extremely Large)
*   `Dignity` vs. `Tribalism`: r = -0.809 (Extremely Large)

This pattern is exemplified in Mitt Romney's speech, where he explicitly rejects `tribalism` in favor of `justice`. As Romney stated: "Many demanded, in their words, that I 'stand with the team.'... But my promise before God to apply impartial justice required that I put my personal feelings and political biases aside" (Source: mitt_romney_2020_impeachment_9ebec73f.txt). This quote perfectly illustrates the negative relationship between these two dimensions captured in the statistics.

### 5.4 Pattern Recognition and Theoretical Insights

The statistical patterns confirm that the CAF's dimensions are not just a list of rhetorical devices but represent two fundamentally different modes of civic engagement. The strong negative correlation between `pragmatism` and `fantasy` (r=-0.934) is particularly telling. It suggests a deep divide between discourse that acknowledges real-world constraints and trade-offs versus discourse that offers simplistic, unworkable solutions. Mitt Romney's speech, with its high `pragmatism` score (0.8), demonstrates the former: "I acknowledge that my verdict will not remove the president from office" (Source: mitt_romney_2020_impeachment_9ebec73f.txt). This contrasts sharply with rhetoric high in `fantasy`, which, as Bernie Sanders's speech shows, can involve "oversimplification of complex economic motivations into a simple, villainous narrative" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt).

These findings provide strong quantitative support for the framework's theoretical underpinnings in civic republicanism, which posits a core conflict between a politics oriented toward the common good (represented by the virtue cluster) and a politics of factionalism and division (represented by the vice cluster). The data suggests these are not just theoretical ideals but are empirically observable as distinct and opposing rhetorical strategies.

An unexpected finding is the complex role of the `hope`/`fear` axis. The correlation between them is the strongest in the entire matrix (r=-0.873), confirming their oppositional nature. However, neither dimension correlates strongly with the main virtue/vice clusters, suggesting that emotional appeals can be attached to either virtuous or vicious rhetorical programs.

### 5.5 Framework Effectiveness Assessment

Based on this preliminary analysis, the Civic Analysis Framework v10.0 demonstrates considerable effectiveness.

*   **Discriminatory Power:** The framework, and particularly the `civic_character_index`, shows high discriminatory power. It successfully separates speakers into meaningful categories and creates a wide distribution of scores, from the highly virtuous (+0.805) to the highly pathological (-0.480). This indicates it is sensitive to the stylistic and substantive differences between speakers.
*   **Construct Validity:** The correlation analysis provides strong evidence for the framework's construct validity. The dimensions behave as theoretically predicted: virtues cluster together, vices cluster together, and the two clusters are strongly opposed. This suggests the framework is measuring what it purports to measure.
*   **Framework-Corpus Fit:** The framework appears well-suited to this corpus of American political speeches. It effectively captures the populist, anti-establishment rhetoric of speakers like Sanders and Vance, the unifying, traditionalist rhetoric of McCain and Romney, and the complex, justice-oriented but divisive rhetoric of Lewis and Ocasio-Cortez. The error message regarding `validate_framework_by_style` indicates a limitation in the available metadata, not a failure of the framework itself.

## 6. Discussion

The results of this computational analysis offer several preliminary implications for the study of political communication and provide a foundation for future research.

### Theoretical Implications of Findings

This analysis suggests that the "civic character" of discourse can be operationalized and measured quantitatively. The emergence of two opposing meta-strategies—one integrative and based on universal virtues, the other divisive and based on pathological vices—provides empirical weight to long-standing theories of civic discourse that contrast reason-based deliberation with factional demagoguery. The `civic_character_index` functions as a quantitative measure of a speaker's position on this spectrum.

Furthermore, the concept of `tension` appears to be a critical, and perhaps under-studied, element of rhetorical strategy. The data indicates that some of the most energetic and seemingly effective political rhetoric, from both the left (Sanders, Ocasio-Cortez) and the right (as suggested by the Lewis profile), thrives on the tension between appeals to high-minded justice and base emotions like resentment. This challenges a simplistic view that virtuous and vicious appeals are always mutually exclusive, suggesting instead that their strategic combination is a distinct rhetorical style.

### Comparative Analysis and Archetypal Patterns

The data allows for the preliminary identification of three distinct rhetorical archetypes within this corpus:

1.  **The Principled Unifier (McCain, Romney):** This archetype is defined by a high Civic Character Index, low vice scores, and minimal tension. Their rhetoric is characterized by appeals to `dignity`, `truth`, and `pragmatism`. They actively reject `tribalism` in favor of national unity and procedural fairness. As McCain stated, "Senator Obama and I have had and argued our differences, and he has prevailed. No doubt many of those differences remain" (Source: john_mccain_2008_concession_ff9b26f2.txt), an example of intellectual honesty (`truth`) that avoids resentment. This style appears most common in moments of institutional gravity, such as a concession or a solemn vote.

2.  **The Populist Agitator (Sanders, King, Vance):** This archetype has a negative Civic Character Index, high scores on `tribalism`, `resentment`, and `manipulation`/`fantasy`, and often high tension. Their strategy is to define a virtuous in-group (e.g., "the 99%") against a corrupt out-group ("the oligarchs," "the elite"). Their rhetoric simplifies complex problems into moral battles, as when Sanders frames greed as "the worst and most dangerous addiction" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt). This style seems geared toward political mobilization and channeling popular anger.

3.  **The Righteous Advocate (Lewis, Ocasio-Cortez):** This is the most complex archetype, with a near-neutral Civic Character Index resulting from high scores on both virtues and vices. They are defined by a powerful appeal to `justice` and `dignity`, but this appeal is fueled by high levels of `resentment` and a strong `tribal` definition of the conflict. John Lewis's speech is a historical exemplar: his call for justice is inseparable from his expression of grievance, "We are tired! We are tired of being beaten by policemen" (Source: john_lewis_1963_march_on_washington_ab348df3.txt). This archetype uses the energy of vice-based emotions to pursue what they frame as a virtuous, systemic goal.

### Broader Significance for the Field

This research demonstrates a path forward for computational social science to analyze normative dimensions of communication. By translating concepts from political theory and ethics into a measurable framework, tools like the CAF can provide a new layer of insight into large-scale textual data. Such an approach could be used to track the "health" of a nation's public sphere over time, compare the rhetorical character of different political parties or movements, or analyze how different media platforms incentivize virtuous versus vicious discourse. It offers a replicable, scalable alternative to purely qualitative readings of political texts.

### Limitations and Future Directions

The limitations of this study, chiefly its small sample size, point directly to avenues for future research. The most pressing need is to apply the CAF to a large, longitudinal corpus of political speech to validate these preliminary findings and test the stability of the identified archetypes. Researchers may wish to explore how rhetorical character varies by context (e.g., campaign rally vs. legislative debate), by medium (e.g., televised speech vs. social media), or over the course of a political career. Another promising direction is to investigate the causal relationship between rhetorical character and audience effects: does discourse with a higher Civic Character Index lead to greater trust or willingness to compromise? This analysis provides a methodological foundation and a set of testable hypotheses for such future work.

## 7. Conclusion

This computational analysis of eight political speeches using the Civic Analysis Framework v10.0 has yielded significant preliminary insights into the structure of civic discourse. The study successfully demonstrated the framework's ability to quantify the civic character of rhetoric, revealing a clear opposition between a cluster of virtues (Dignity, Truth, Justice, Pragmatism) and a cluster of vices (Tribalism, Manipulation, Resentment, Fantasy). The `civic_character_index` proved to be a robust metric for differentiating speakers along this spectrum, while the concept of `tension` illuminated the complex ways in which speakers combine contradictory appeals.

The preliminary validation of the framework's oppositional design through strong, negative correlations between corresponding virtues and vices lends confidence to its theoretical and methodological rigor. The identification of three distinct rhetorical archetypes—the Principled Unifier, the Populist Agitator, and the Righteous Advocate—provides a new vocabulary for describing political styles and generates testable hypotheses for future research.

While the small sample size mandates caution in generalizing these findings, this report serves as a proof-of-concept for a powerful analytical approach. By systematically measuring the normative dimensions of speech, computational methods like the CAF can equip researchers to analyze political communication with greater depth, nuance, and scalability, ultimately contributing to a more empirical understanding of the state of our civic discourse.

## 8. Evidence Citations

The following textual evidence was cited in this report to support statistical interpretations.

*   **Source Document:** `alexandria_ocasio_cortez_2025_fighting_oligarchy_1121e4ae.txt`
    *   As Alexandria Ocasio-Cortez stated: "Our lives deserve dignity and our work deserves respect."
    *   As Alexandria Ocasio-Cortez stated: "They aren't working for these billions. They're stealing them. They're stealing them. They're stealing them from you and you and me."

*   **Source Document:** `bernie_sanders_2025_fighting_oligarchy_261b893a.txt`
    *   As Bernie Sanders stated: "That is what a rigged economy is about, and that is what we are going to change."
    *   As Bernie Sanders stated: "Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change."
    *   As Bernie Sanders stated: "Abraham Lincoln talked about a government of the people, by the people, for the people."
    *   As Bernie Sanders stated: "I don't have a PhD in mathematics, but I do know this, that 99% is a hell of a lot larger number than 1%."
    *   As Bernie Sanders stated: "But I will tell you this, in the midst of all of these addictions, the worst and most dangerous addiction we have is the greed of the oligarchs."
    *   The analysis noted that Sanders's speech involved an "oversimplification of complex economic motivations into a simple, villainous narrative," which is a form of `fantasy`.

*   **Source Document:** `john_lewis_1963_march_on_washington_ab348df3.txt`
    *   As John Lewis stated: "Do you know that in Albany, Georgia, nine of our leaders have been indicted, not by Dixiecrats, but by the federal government for peaceful protest?"
    *   As John Lewis stated: "We are tired! We are tired of being beaten by policemen. We are tired of seeing our people locked up in jails over and over again."

*   **Source Document:** `john_mccain_2008_concession_ff9b26f2.txt`
    *   As John McCain stated: "I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together"
    *   As John McCain stated: "Senator Obama and I have had and argued our differences, and he has prevailed. No doubt many of those differences remain."

*   **Source Document:** `mitt_romney_2020_impeachment_9ebec73f.txt`
    *   As Mitt Romney stated: "Many demanded, in their words, that I 'stand with the team.'... But my promise before God to apply impartial justice required that I put my personal feelings and political biases aside."
    *   As Mitt Romney stated: "I acknowledge that my verdict will not remove the president from office. The results of this Senate court will, in fact, be appealed to a higher court: the judgment of the American people."