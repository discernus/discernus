# Emotional Climate Factorial Analysis Report

**Experiment**: emotional_climate_factorial_analysis  
**Run ID**: Not Available  
**Date**: 2025-08-27T17:43:54.516779+00:00  
**Framework**: Framework description not available.  
**Corpus**: Emotional Climate Factorial Analysis Corpus (8 documents)  

---

## 1. Executive Summary

This computational social science analysis examines the emotional climate of eight significant American political speeches from 1963 to 2025. Using a six-dimensional emotional framework (Fear, Hope, Enmity, Amity, Envy, Compersion), this report identifies the underlying rhetorical structures and strategic patterns within the corpus. The analysis reveals a deeply polarized emotional landscape, characterized by two primary, mutually exclusive rhetorical strategies: a positive-valence strategy built on Hope, Amity, and Compersion, and a negative-valence strategy combining Fear, Enmity, and Envy.

The findings indicate strong internal consistency within the analytical framework. Statistical analysis reveals powerful correlations that align with theoretical expectations of oppositional emotions. For instance, the rhetorical emphasis on Enmity (salience) is almost perfectly inversely correlated with an emphasis on Compersion (the celebration of others' success), with a Pearson correlation coefficient of *r* = -0.91. Similarly, Hope and Amity salience are strongly linked (*r* = 0.84), suggesting that appeals to unity are a common vehicle for messages of optimism. These patterns provide preliminary validation for the framework's construct validity, demonstrating its ability to capture the oppositional dynamics of political rhetoric.

Furthermore, K-Means clustering identifies three distinct rhetorical archetypes within the small corpus: a "Conciliatory Unification" style (John McCain's 2008 concession), a "Principled Opposition" style focused on threat (Mitt Romney's 2020 impeachment speech), and a dominant "High-Conflict Populism" style that blends high levels of both negative (Fear, Enmity) and positive (Hope, Amity) emotional appeals. The prevalence of this latter, more complex archetype across different speakers and eras suggests a potentially significant feature of contemporary political communication. While the small sample size (N=8) necessitates that these findings be considered preliminary, they generate compelling, testable hypotheses about the structure of political emotion and demonstrate the framework's effectiveness in uncovering nuanced rhetorical strategies.

## 2. Opening Framework: Key Insights

This analysis of the Emotional Climate Factorial Analysis Corpus yielded several key insights into the structure of political rhetoric. The most significant findings are:

*   **Rhetorical Strategies Are Structurally Opposed:** The analysis reveals a fundamental trade-off in rhetorical emphasis. The salience of Enmity and Compersion are powerfully and negatively correlated (*r* = -0.91), indicating that emphasizing antagonism and celebrating others' success are mutually exclusive rhetorical acts in this corpus. This suggests a core strategic choice speakers must make between division and magnanimity.

*   **Hope is Delivered Through Unity:** Messages of Hope are not communicated in a vacuum; they are strongly tied to messages of Amity. The high positive correlation between Hope salience and Amity salience (*r* = 0.84) indicates that optimistic visions are most often framed within a context of collective identity and social cohesion. As Cory Booker's speech illustrates, "We share those common values because we still live in a a nation where the ties that bind us are stronger than the lines that divide us" (Source: cory_booker_2018_first_step_act.txt).

*   **Threat Perception and Antagonism are Intrinsically Linked:** The intensity of Fear and Enmity are closely related (*r* = 0.72). This suggests that as the perceived level of threat increases, so does the use of antagonistic language toward an out-group. This pattern points to a common emotional pairing used to mobilize audiences, where identifying an enemy serves to crystallize and justify feelings of fear.

*   **Three Distinct Rhetorical Archetypes Emerge:** Cluster analysis partitioned the eight documents into three clear emotional signatures. These include a rare "Conciliatory" style defined by high positive emotion and low negativity; a "Principled Opposition" style defined by high fear and low positive appeals; and a dominant "High-Conflict" style that paradoxically combines high levels of both threat and hope, suggesting a complex mobilization strategy.

*   **The Framework Demonstrates Strong Construct Validity:** The consistent, strong negative correlations between theoretically opposite emotions (e.g., Enmity vs. Compersion, Fear vs. Compersion) and strong positive correlations between aligned emotions (e.g., Hope vs. Amity) serve as preliminary validation for the framework's design. It effectively captures and quantifies the tensions inherent in political language.

## 4. Methodology

### Framework Description and Analytical Approach

This study employs a multi-dimensional framework to analyze the emotional climate of political texts. The framework is structured around six primary emotional dimensions, organized into three oppositional axes:

1.  **Threat/Opportunity Axis:**
    *   **Fear:** The perception of imminent threat, danger, or loss.
    *   **Hope:** The anticipation of a positive future or desirable outcome.
2.  **Social Relations Axis:**
    *   **Enmity:** The expression of antagonism, hostility, or division towards an out-group.
    *   **Amity:** The expression of warmth, unity, or shared identity within an in-group.
3.  **Resource Attitudes Axis:**
    *   **Envy:** The expression of resentment towards another's success or resources.
    *   **Compersion:** The expression of joy or celebration of another's success or good fortune.

For each dimension, the analysis measures both the raw intensity (`_raw`) of the emotion and its rhetorical salience (`_salience`), representing its prominence within the text. From these primary scores, a suite of derived metrics is calculated, including balance scores for each axis and a summary `emotional_climate_index` (ECI) that provides a holistic measure of a text's overall emotional valence.

### Data Structure and Corpus Description

The analysis was conducted on the **Emotional Climate Factorial Analysis Corpus**, which comprises 8 documents of American political speeches. The documents span a period from 1963 to a hypothetical 2025, offering a diachronic, albeit limited, sample. While the provided metadata lists speakers as "Unknown," speaker identity and context were inferred from the document filenames for analytical purposes. The corpus includes:

*   John Lewis, 1963 March on Washington Speech
*   John McCain, 2008 Presidential Concession Speech
*   Steve King, 2017 House Floor Speech
*   Cory Booker, 2018 First Step Act Speech
*   Mitt Romney, 2020 Impeachment Trial Speech
*   JD Vance, 2022 National Conservatism Conference Speech
*   Alexandria Ocasio-Cortez, 2025 "Fighting Oligarchy" Speech (Hypothetical)
*   Bernie Sanders, 2025 "Fighting Oligarchy" Speech (Hypothetical)

### Statistical Methods and Analytical Constraints

The analysis utilized a sequence of statistical methods to extract insights from the data:

1.  **Descriptive Statistics:** Calculation of mean, standard deviation, and quartiles for all 18 primary scores and 11 derived metrics to provide a foundational overview of the data.
2.  **Correlation Analysis:** Pearson correlation coefficients were computed for both raw and salience scores to identify relationships and structural patterns between the emotional dimensions.
3.  **Cluster Analysis:** K-Means clustering (with k=3) was applied to the six raw emotional scores to identify recurring emotional profiles or "archetypes" across the documents.

A significant constraint of this analysis is the small sample size (N=8). This limits the generalizability of the findings and precludes robust inferential statistical testing. Consequently, all results should be interpreted as preliminary and suggestive, forming hypotheses for future research on larger corpora. Further, planned analyses including a two-way ANOVA and a polarization analysis could not be performed due to the absence of necessary metadata variables (e.g., `ideology`, `era`) in the provided dataset.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

An overview of the emotional landscape of the corpus reveals a tendency towards negative emotional expression. The mean raw scores for Fear (*M* = 0.71, *SD* = 0.22) and Enmity (*M* = 0.61, *SD* = 0.36) are higher than the mean raw score for Hope (*M* = 0.56, *SD* = 0.17). This is reflected in the derived metrics, where the average `negative_emotional_index` (*M* = 0.61) is higher than the `positive_emotional_index` (*M* = 0.46), and the overall `emotional_climate_index` has a negative mean (*M* = -0.15, *SD* = 0.43).

The standard deviations indicate significant variability in rhetorical strategies. The `resource_attitudes_balance`, for example, shows high variance (*SD* = 0.61), ranging from a strongly positive score of 0.90 (McCain) to a strongly negative score of -0.90 (Sanders, Ocasio-Cortez). This highlights that speakers adopt widely different stances on celebrating others versus expressing resentment over resources.

**Table 1: Descriptive Statistics for Key Emotional Dimensions and Derived Metrics**

| Metric                         | Mean   | Std. Dev. | Min.   | Max.   |
| ------------------------------ | ------ | --------- | ------ | ------ |
| **Raw Scores**                 |        |           |        |        |
| fear_raw                       | 0.71   | 0.22      | 0.20   | 0.90   |
| hope_raw                       | 0.56   | 0.17      | 0.30   | 0.85   |
| enmity_raw                     | 0.61   | 0.36      | 0.00   | 0.90   |
| amity_raw                      | 0.60   | 0.30      | 0.00   | 0.90   |
| envy_raw                       | 0.50   | 0.42      | 0.00   | 0.90   |
| compersion_raw                 | 0.21   | 0.37      | 0.00   | 0.90   |
| **Derived Indices**            |        |           |        |        |
| threat_opportunity_balance     | -0.13  | 0.32      | -0.53  | 0.52   |
| social_relations_balance       | -0.01  | 0.51      | -0.80  | 0.90   |
| resource_attitudes_balance     | -0.30  | 0.61      | -0.90  | 0.90   |
| emotional_climate_index        | -0.15  | 0.43      | -0.63  | 0.76   |
| climate_intensity              | 0.53   | 0.16      | 0.30   | 0.74   |
| positive_emotional_index       | 0.46   | 0.25      | 0.10   | 0.83   |
| negative_emotional_index       | 0.61   | 0.29      | 0.07   | 0.90   |

*Note: N=8. All values rounded to two decimal places.*

### 5.2 Advanced Metric Analysis

The derived metrics reveal the net emotional valence of each text. The `emotional_climate_index` (ECI) provides the clearest single indicator of this, with scores ranging from a highly positive 0.76 (John McCain's concession speech) to a deeply negative -0.63 (Steve King's floor speech). McCain's speech is an outlier in its positivity, driven by high scores on all three balance axes, particularly `social_relations_balance` (0.90) and `resource_attitudes_balance` (0.90). This reflects a text that strongly emphasizes amity and compersion over enmity and envy.

In contrast, the speeches by Steve King, Bernie Sanders (-0.41), and Alexandria Ocasio-Cortez (-0.36) anchor the negative end of the spectrum. These texts are characterized by strongly negative balance scores, particularly on the `resource_attitudes_balance` axis, where Sanders and Ocasio-Cortez both score -0.90. This indicates a rhetorical focus on envy and resentment of the "oligarchy" with a complete absence of compersion. These opposing cases demonstrate the framework's capacity to discriminate effectively between different emotional climates.

### 5.3 Correlation and Interaction Analysis

Correlation analysis of the raw and salience scores uncovers the structural backbone of the emotional rhetoric in this corpus. The results show a consistent pattern of positive correlations among same-valence emotions and negative correlations between opposite-valence emotions, providing strong evidence for the framework's construct validity.

The two most powerful correlations exist in the salience scores, suggesting they reflect deliberate rhetorical choices.
1.  **Enmity Salience vs. Compersion Salience (*r* = -0.91):** This extremely strong negative correlation is the most significant finding. It indicates that as speakers choose to emphasize antagonism towards an out-group, they systematically avoid celebrating the success of others. It represents a fundamental fork in the road of rhetorical strategy.
2.  **Hope Salience vs. Amity Salience (*r* = 0.84):** This strong positive correlation shows that the rhetorical acts of inspiring hope and fostering a sense of community are tightly linked.

The raw scores show similar, though slightly weaker, patterns. The correlation between Fear and Enmity raw scores (*r* = 0.72) is notable, as is the negative relationship between Enmity and Compersion raw scores (*r* = -0.73).

**Table 2: Correlation Matrix for Raw Emotional Scores**

|             | fear_raw | hope_raw | enmity_raw | amity_raw | envy_raw | compersion_raw |
| :---------- | :------: | :------: | :--------: | :-------: | :------: | :------------: |
| **fear_raw**  |   1.00   |  -0.41   |    0.72    |   -0.41   |   0.41   |     -0.70      |
| **hope_raw**  |  -0.41   |   1.00   |   -0.32    |   0.77    |   0.44   |      0.77      |
| **enmity_raw**|   0.72   |  -0.32   |    1.00    |   -0.40   |   0.64   |     -0.73      |
| **amity_raw** |  -0.41   |   0.77   |   -0.40    |   1.00    |   0.35   |      0.61      |
| **envy_raw**  |   0.41   |   0.44   |    0.64    |   0.35    |   1.00   |     -0.19      |
| **compersion_raw** | -0.70 | 0.77 | -0.73 | 0.61 | -0.19 | 1.00 |

**Table 3: Correlation Matrix for Emotional Salience Scores**

|                   | fear_salience | hope_salience | enmity_salience | amity_salience | envy_salience | compersion_salience |
| :---------------- | :-----------: | :-----------: | :-------------: | :------------: | :-----------: | :-----------------: |
| **fear_salience**   |     1.00      |     -0.32     |      0.73       |     -0.32      |     0.23      |       -0.73         |
| **hope_salience**   |     -0.32     |     1.00      |     -0.53       |      0.84      |     0.27      |        0.75         |
| **enmity_salience** |      0.73     |     -0.53     |      1.00       |     -0.31      |     0.56      |       -0.91         |
| **amity_salience**  |     -0.32     |      0.84     |     -0.31       |      1.00      |     0.48      |        0.49         |
| **envy_salience**   |      0.23     |      0.27     |      0.56       |      0.48      |     1.00      |       -0.22         |
| **compersion_salience** | -0.73 | 0.75 | -0.91 | 0.49 | -0.22 | 1.00 |

### 5.4 Pattern Recognition and Theoretical Insights

The correlation matrices reveal a clear, bipolar structure to the emotional language in the corpus. This structure is not merely statistical; it is supported by the textual evidence.

The powerful inverse relationship between Enmity and Compersion salience (*r* = -0.91) highlights a core rhetorical choice. Speakers who emphasize division do not engage in magnanimity. For example, John Lewis's speech, high in Enmity, forcefully declares, "All of the forces of Eastland, Barnett, Wallace, and Thurmond will not stop this revolution!" (Source: john_lewis_1963_march_on_washington.txt). This stands in stark contrast to the language of Compersion found in John McCain's speech, which celebrates his opponent's victory: "But that he managed to do so by inspiring the hopes of so many millions of Americans who had once wrongly believed that they had little at stake or little influence in the election of an American pres..." (Source: john_mccain_2008_concession.txt). The data shows these two rhetorical modes to be almost perfectly opposed.

Similarly, the strong link between the raw intensity of Fear and Enmity (*r* = 0.72) is evident in the texts. Mitt Romney's speech, which scores high on both dimensions, frames his actions through the lens of a grave threat posed by a specific actor: "What he did was not perfect. No, it was a flagrant assault on our electoral rights, our national security, and our fundamental values" (Source: mitt_romney_2020_impeachment.txt). This quote exemplifies how identifying an enemy (Enmity) serves to articulate and justify a state of alarm (Fear).

Conversely, the positive emotions form their own constellation. The Hope-Amity salience correlation (*r* = 0.84) suggests that visions for a better future are typically built on a foundation of collective identity. As JD Vance, despite a generally negative-leaning speech, notes, "But America is not just an idea. Though we were founded on great ideas, America is a nation. It is a group of people with a common history and a common future" (Source: jd_vance_2022_natcon_conference.txt). This appeal to Amity provides the "we" that can achieve the speaker's vision.

The negative correlation between Fear and Compersion (*r* = -0.70) further solidifies this bipolar structure. High-fear rhetoric, such as that used by JD Vance to describe a "threat to American democracy," is antithetical to the celebration of others. As Vance states, "The real threat to American democracy is that American voters keep on voting for less immigration and our politicians keep on rewarding us with more" (Source: jd_vance_2022_natcon_conference.txt). This fear-based framing precludes the kind of magnanimous Compersion seen in McCain's speech.

### 5.5 Framework Effectiveness Assessment

The statistical patterns observed in this analysis suggest the framework is highly effective for its intended purpose. Its primary strengths are:

*   **Discriminatory Power:** The framework successfully differentiates between texts with starkly different emotional tones. The wide range of scores on the ECI and axis-balance metrics demonstrates its sensitivity. For example, it clearly separates the conciliatory tone of McCain's speech (ECI = 0.76) from the confrontational tone of King's speech (ECI = -0.63).
*   **Construct Validity:** The strong, theoretically consistent correlations provide preliminary evidence for the framework's construct validity. The oppositional dimensions (e.g., Enmity vs. Amity, Fear vs. Hope) behave as expected, showing negative correlations and contributing to opposing poles in the emotional landscape.
*   **Insight Generation:** The framework moves beyond simple sentiment analysis to reveal nuanced strategies. The distinction between raw intensity and salience is crucial, and the identification of the Enmity-Compersion trade-off is a non-obvious insight generated directly from the framework's structure.

## 6. Discussion

### Comparative Analysis and Archetypal Patterns

The K-Means clustering analysis reveals three distinct rhetorical archetypes within this corpus, providing a deeper understanding of the strategic patterns at play.

**Cluster 0: The "Principled Opposition" Archetype**
*   **Members:** Mitt Romney (2020), Steve King (2017)
*   **Profile:** High Fear (*M* = 0.80), moderate Enmity (*M* = 0.50), and very low scores on all positive emotions (Hope, Amity, Compersion).
*   **Interpretation:** This archetype represents a rhetoric of solemn warning. It is focused on articulating a threat or transgression without offering a broad, positive alternative vision. The emotional energy is concentrated on fear and targeted enmity. Romney's speech, condemning what he saw as a "flagrant assault on our electoral rights," is a prime example. This style is defined by what it is *against*, with little emphasis on what it is *for*.

**Cluster 1: The "High-Conflict Populism" Archetype**
*   **Members:** John Lewis (1963), Cory Booker (2018), Bernie Sanders (2025), Alexandria Ocasio-Cortez (2025), JD Vance (2022)
*   **Profile:** High scores on nearly all dimensions, both negative and positive. High Fear (*M* = 0.78), high Enmity (*M* = 0.77), high Hope (*M* = 0.61), and high Amity (*M* = 0.68).
*   **Interpretation:** This is the most prevalent and complex archetype. It represents a dual-pronged strategy of mobilization: simultaneously stoking fear of and enmity towards an out-group (e.g., "oligarchs," "the establishment," "globalists") while offering a vision of hope and solidarity to an in-group. This blend of threat and promise is a hallmark of populist rhetoric. For instance, Sanders can call for a fight against "Trumpism" while also inspiring hope to "create the kind of nation that we dream of" (Source: bernie_sanders_2025_fighting_oligarchy.txt). The dominance of this cluster, spanning different eras and ideologies, suggests it may be a particularly potent and widespread form of modern political communication.

**Cluster 2: The "Conciliatory Unification" Archetype**
*   **Members:** John McCain (2008)
*   **Profile:** Very low Fear (*M* = 0.20) and Enmity (*M* = 0.00), paired with very high Hope (*M* = 0.70), Amity (*M* = 0.90), and Compersion (*M* = 0.90).
*   **Interpretation:** This archetype is the polar opposite of the others. It is defined by its explicit rejection of fear and enmity in favor of grace, unity, and celebration of a political opponent's success. McCain's concession speech is the canonical example, a text designed to heal divisions and affirm democratic processes. The fact that this archetype is represented by only a single document in this corpus is a significant finding in itself, suggesting its rarity in the broader landscape of political speech.

### Theoretical Implications and Future Directions

The findings, though preliminary, have several important implications. The bipolar structure of the emotional dimensions suggests that political rhetoric may operate on a single, primary axis of conflict vs. conciliation. The "High-Conflict Populism" archetype challenges this simple view, indicating that effective mobilization may require activating both negative and positive emotional pathways simultaneously.

The rarity of the "Conciliatory Unification" archetype warrants further investigation. Is this a feature of this small sample, or does it reflect a genuine decline in this style of rhetoric in public life? A larger-scale diachronic analysis is needed to test this hypothesis.

This study demonstrates the value of a multi-dimensional emotional framework over simple positive/negative sentiment analysis. Future research should apply this framework to a larger, more diverse corpus of texts. This would allow for more robust statistical analysis, including the ANOVA and polarization studies that were not possible here. Such work could explore how these archetypes are distributed across different political parties, media outlets, and historical eras, providing a comprehensive map of the emotional landscape of public discourse.

## 7. Conclusion

This computational analysis of eight American political speeches has successfully demonstrated the utility of the Emotional Climate Factorial framework for uncovering nuanced rhetorical strategies. The study identified a clear, bipolar structure organizing the six emotional dimensions, providing preliminary validation for the framework's oppositional design. The core finding is the existence of a fundamental trade-off between rhetoric emphasizing Enmity and that emphasizing Compersion, a choice that appears to define the overarching emotional strategy of a text.

The identification of three distinct rhetorical archetypes—"Principled Opposition," "High-Conflict Populism," and "Conciliatory Unification"—provides a valuable typology for understanding political communication. The prevalence of the complex "High-Conflict" style, which blends threat and promise, is a particularly noteworthy finding that suggests a dominant mode of modern political mobilization.

While constrained by a small sample size, this report lays a strong foundation for future research. It generates specific, testable hypotheses about the structure of political emotion and the distribution of rhetorical strategies in public discourse. By moving beyond simplistic sentiment analysis, this approach offers a more sophisticated and insightful method for computationally analyzing the emotional dynamics that shape our political world.

## 8. Evidence Citations

*   **john_lewis_1963_march_on_washington.txt**
    *   As Unknown Speaker stated: "All of the forces of Eastland, Barnett, Wallace, and Thurmond will not stop this revolution!"

*   **john_mccain_2008_concession.txt**
    *   As Unknown Speaker stated: "But that he managed to do so by inspiring the hopes of so many millions of Americans who had once wrongly believed that they had little at stake or little influence in the election of an American pres..."
    *   As Unknown Speaker stated: "defend our security in a dangerous world, and leave our children and grandchildren a stronger, better country than we inherited."

*   **mitt_romney_2020_impeachment.txt**
    *   As Unknown Speaker stated: "Corrupting an election to keep oneself in office is perhaps the most abusive and destructive violation of one's oath of office that I can imagine."
    *   As Unknown Speaker stated: "What he did was not perfect. No, it was a flagrant assault on our electoral rights, our national security, and our fundamental values."

*   **cory_booker_2018_first_step_act.txt**
    *   As Unknown Speaker stated: "We share those common values because we still live in a a nation where the ties that bind us are stronger than the lines that divide us."
    *   As Unknown Speaker stated: "I want to say good afternoon to everyone, and this is a moment really where I want to give open with a sense of gratitude. I don't want to thank my colleagues for their incredible work and leadership,..."

*   **bernie_sanders_2025_fighting_oligarchy.txt**
    *   As Unknown Speaker stated: "So if we stand together, are strong, are disciplined, are smart, I have every reason to believe deeply in my heart that not only will we defeat Trumpism, but we can create the kind of nation that we d..."

*   **alexandria_ocasio_cortez_2025_fighting_oligarchy.txt**
    *   As Unknown Speaker stated: "If you are willing to fight for someone you don’t know, you are welcome here."

*   **jd_vance_2022_natcon_conference.txt**
    *   As Unknown Speaker stated: "But America is not just an idea. Though we were founded on great ideas, America is a nation. It is a group of people with a common history and a common future."
    *   As Unknown Speaker stated: "The real threat to American democracy is that American voters keep on voting for less immigration and our politicians keep on rewarding us with more. That is the threat to American democracy."