# ecf_v10.md Analysis Report

**Experiment**: emotional_climate_factorial_analysis  
**Run ID**: 8f5c2a1b-453e-4f8d-8a6e-9c1b7d0e2f4a  
**Date**: 2024-05-21  
**Framework**: ecf_v10.md  
**Corpus**: corpus.md (8 documents)  

---

## 1. Executive Summary

This computational social science report presents a preliminary analysis of the emotional climate in a diverse corpus of eight American political speeches spanning from 1963 to 2025. Using the Emotional Climate Factorial (ECF) v10.0 framework, this study quantifies and examines six core emotional dimensions: Fear, Hope, Enmity, Amity, Envy, and Compersion. The analysis reveals a political discourse characterized by distinct, often oppositional, emotional strategies. The findings are based on a small sample (N=8) and should be considered exploratory.

The analysis identified two dominant and opposing emotional constellations. A positive-valence strategy strongly links expressions of **Hope** with **Amity** (salience correlation, *r* = .84), while a negative-valence strategy couples expressions of **Fear** with **Enmity** (*r* = .72). The framework's oppositional design is validated by a powerful negative correlation between the salience of **Enmity** and **Compersion** (*r* = -.91), indicating that rhetoric focused on antagonism systematically excludes the celebration of others' success. K-Means clustering further distilled these patterns into three distinct rhetorical archetypes: a "High-Conflict" profile mixing hope and grievance, a "Threat-Focused" profile centered on fear and enmity, and a rare "Conciliatory" profile built on hope and unity.

Overall, the ECF v10.0 framework demonstrates significant promise as an analytical tool. It effectively captures the structural tensions in political language and possesses strong discriminatory power, revealing coherent emotional strategies within the text. The derived metrics, such as the `emotional_climate_index`, provide a useful summary of a document's overall affective leaning. However, the small sample size is a major limitation, precluding more advanced inferential statistics and necessitating caution in generalizing these findings. Future research should apply this framework to a larger, diachronic corpus to validate these preliminary archetypes and explore their evolution over time.

## 2. Opening Framework: Key Insights

This analysis of the emotional climate in political discourse yielded several key insights, grounded in the statistical patterns of the ECF v10.0 framework:

*   **Political Emotion is Structurally Oppositional:** The data reveals a strong bifurcation in emotional strategy. The emphasis on **Hope** is tightly bound to an emphasis on **Amity** (salience *r* = .84), forming a constructive, unifying rhetorical axis. Conversely, the most powerful negative correlation in the dataset is between **Enmity** and **Compersion** salience (*r* = -.91), suggesting that a focus on out-groups and conflict is fundamentally incompatible with celebrating collective success.

*   **Fear and Enmity are a Potent Combination:** The intensity of **Fear** and **Enmity** are strongly correlated (*r* = .72). This indicates that rhetoric designed to evoke a sense of threat is frequently paired with language that identifies and vilifies an enemy, creating a powerful narrative of existential danger posed by a specific antagonist.

*   **Three Distinct Emotional Archetypes Emerge:** K-Means clustering identified three recurring emotional signatures. The most common is a **"High-Conflict"** archetype (5 of 8 documents) characterized by high scores across most dimensions, blending hope for an in-group with fear and enmity toward an out-group. A **"Threat-Focused"** archetype (2 of 8 documents) relies almost exclusively on fear and grievance. A rare **"Conciliatory"** archetype (1 of 8 documents) is defined by high hope and amity with minimal negativity.

*   **The Overall Emotional Climate is Negative:** Across this limited sample, the average `emotional_climate_index` is negative (*M* = -0.15, *SD* = 0.43), driven by a higher prevalence of negative emotions (*M* = 0.61) compared to positive ones (*M* = 0.46). This suggests that, on balance, the sampled discourse leans more towards threat, conflict, and grievance than towards hope, unity, and celebration.

*   **Rhetorical Emphasis Mirrors Emotional Content:** The correlation patterns for salience scores (rhetorical emphasis) are generally stronger and cleaner than for raw scores (emotional intensity). For instance, the negative link between Enmity and Compersion is more pronounced in salience (*r* = -.91) than in raw scores (*r* = -.73). This suggests that speakers make deliberate, strategic choices to emphasize these opposing emotional frames.

## 3. Methodology

### Framework and Analytical Approach

This study employs the **Emotional Climate Factorial (ECF) v10.0 framework** to analyze the provided corpus. Although the framework's full specification was not available, the data structure implies an oppositional, six-dimension model organized into three axes:
1.  **Threat/Opportunity Axis:** Fear vs. Hope
2.  **Social Relations Axis:** Enmity vs. Amity
3.  **Resource Attitudes Axis:** Envy vs. Compersion

For each dimension, the analysis utilized three scores: a `_raw` score representing the intensity of the emotion (0-1 scale), a `_salience` score representing its rhetorical prominence (0-1 scale), and a `_confidence` score from the measurement model. The analysis also computed eleven derived metrics as specified by the `calculate_derived_metrics` function, including axis-level balance scores and summary measures like the `emotional_climate_index` and `climate_intensity`.

### Corpus Description

The corpus consists of eight text documents (`corpus.md`) containing American political speeches. The documents span a wide date range (1963-2025) and represent a variety of speakers and contexts, including historic addresses, legislative debates, and campaign speeches. The limited size of the corpus (N=8) makes this a preliminary, exploratory study.

### Statistical Methods and Constraints

The analysis was conducted using a suite of automated statistical functions. The primary methods included:
*   **Descriptive Statistics:** Calculation of mean, standard deviation, and range for all raw, salience, and derived metrics to provide a baseline understanding of the data distribution.
*   **Pearson Correlation:** A correlation matrix was computed for both raw and salience scores to identify relationships between the six core emotional dimensions. This is crucial for assessing the framework's construct validity, particularly its oppositional structure.
*   **K-Means Clustering:** An unsupervised machine learning algorithm was used to identify naturally occurring groups or "archetypes" of emotional expression within the corpus based on the six raw emotion scores. The number of clusters was set to three to identify major patterns.

### Limitations

The foremost limitation of this study is the **extremely small sample size (N=8)**. Consequently, the findings are suggestive rather than conclusive and lack statistical power. Generalizing these results to broader political discourse is not advisable without significant further research.

Furthermore, several planned analyses failed due to missing data. The `perform_two_way_anova` and `analyze_climate_polarization` functions could not be executed because the necessary grouping variables (e.g., 'ideology', 'era') were not present in the dataset. This prevented a formal examination of how emotional climates might differ across political affiliations or time periods. All interpretations are therefore based on descriptive and correlational patterns within the sample as a whole.

## 4. Comprehensive Results

### 4.1 Descriptive Statistics

Descriptive statistics for the core dimensions and key derived metrics reveal a landscape tilted towards negative emotionality. The mean raw score for negative dimensions (Fear, Enmity, Envy) was 0.61, while the mean for positive dimensions (Hope, Amity, Compersion) was 0.46. **Fear** (*M* = 0.71, *SD* = 0.22) and **Enmity** (*M* = 0.61, *SD* = 0.36) are among the most prevalent emotions. The overall `emotional_climate_index`, which balances positive and negative dimensions, has a negative mean (*M* = -0.15, *SD* = 0.43), confirming this slight negative skew across the corpus. The average `climate_intensity` (*M* = 0.53, *SD* = 0.16) indicates a moderate level of overall emotional activation in the texts.

**Table 1: Descriptive Statistics for Key ECF Metrics (N=8)**
| Metric                        | Mean   | SD     | Min     | Max    |
|-------------------------------|--------|--------|---------|--------|
| **Raw Scores**                |        |        |         |        |
| fear_raw                      | 0.71   | 0.22   | 0.20    | 0.90   |
| hope_raw                      | 0.56   | 0.17   | 0.30    | 0.85   |
| enmity_raw                    | 0.61   | 0.36   | 0.00    | 0.90   |
| amity_raw                     | 0.60   | 0.30   | 0.00    | 0.90   |
| envy_raw                      | 0.50   | 0.42   | 0.00    | 0.90   |
| compersion_raw                | 0.21   | 0.37   | 0.00    | 0.90   |
| **Derived Indices**           |        |        |         |        |
| emotional_climate_index       | -0.15  | 0.43   | -0.63   | 0.76   |
| climate_intensity             | 0.53   | 0.16   | 0.30    | 0.74   |
| positive_emotional_index      | 0.46   | 0.25   | 0.10    | 0.83   |
| negative_emotional_index      | 0.61   | 0.29   | 0.07    | 0.90   |

### 4.2 Correlation and Interaction Analysis

Correlation analysis provides strong evidence for the framework's internal coherence and reveals the underlying strategic logic of emotional expression in the corpus. The patterns observed in both raw intensity and rhetorical salience point to two primary, oppositional emotional strategies.

**Table 2: Pearson Correlation Matrix for Raw Emotion Scores**
|             | fear_raw | hope_raw | enmity_raw | amity_raw | envy_raw | compersion_raw |
|-------------|----------|----------|------------|-----------|----------|----------------|
| **fear_raw**    | 1.00     | -0.41    | **0.72**   | -0.41     | 0.41     | -0.70          |
| **hope_raw**    | -0.41    | 1.00     | -0.32      | **0.77**  | 0.44     | **0.77**       |
| **enmity_raw**  | **0.72** | -0.32    | 1.00       | -0.40     | 0.64     | **-0.73**      |
| **amity_raw**   | -0.41    | **0.77** | -0.40      | 1.00      | 0.35     | 0.61           |
| **envy_raw**    | 0.41     | 0.44     | 0.64       | 0.35      | 1.00     | -0.19          |
| **compersion_raw**| -0.70    | **0.77** | **-0.73**  | 0.61      | -0.19    | 1.00           |

**Table 3: Pearson Correlation Matrix for Emotion Salience Scores**
|                     | fear_salience | hope_salience | enmity_salience | amity_salience | envy_salience | compersion_salience |
|---------------------|---------------|---------------|-----------------|----------------|---------------|---------------------|
| **fear_salience**     | 1.00          | -0.32         | **0.73**        | -0.32          | 0.23          | **-0.73**           |
| **hope_salience**     | -0.32         | 1.00          | -0.53           | **0.84**       | 0.27          | **0.75**            |
| **enmity_salience**   | **0.73**      | -0.53         | 1.00            | -0.31          | 0.56          | **-0.91**           |
| **amity_salience**    | -0.32         | **0.84**      | -0.31           | 1.00           | 0.48          | 0.49                |
| **envy_salience**     | 0.23          | 0.27          | 0.56            | 0.48           | 1.00          | -0.22               |
| **compersion_salience**| **-0.73**     | **0.75**      | **-0.91**       | 0.49           | -0.22         | 1.00                |

#### The Positive-Valence "Unity" Strategy
A very strong positive correlation exists between **Hope** and **Amity** salience (*r* = .84), indicating that when speakers choose to emphasize a hopeful vision for the future, they almost invariably also emphasize themes of solidarity and togetherness. This suggests a coherent "unity" strategy. This connection is visible in discourse that ties optimism directly to collective identity, as when one speaker notes, "We share those common values because we still live in a a nation where the ties that bind us are stronger than the lines that divide us" (Source: cory_booker_2018_first_step_act.txt). The raw scores for Hope and Compersion are also strongly linked (*r* = .77), showing that intense feelings of hope often co-occur with celebrating success, a sentiment captured in the call "to not despair of our present difficulties, but to believe always in the promise and greatness of America" (Source: john_mccain_2008_concession.txt).

#### The Negative-Valence "Conflict" Strategy
A powerful "conflict" strategy emerges from the strong positive correlation between the raw intensity of **Fear** and **Enmity** (*r* = .72). This pattern suggests that evoking threat and identifying an enemy are mutually reinforcing tactics. This is evident in rhetoric that defines a danger in antagonistic terms, such as, "The real threat to American democracy is that American voters keep on voting for less immigration and our politicians keep on rewarding us with more" (Source: jd_vance_2022_natcon_conference.txt). This strategy frames societal problems not as abstract challenges but as active threats perpetrated by a hostile force.

#### The Central Opposition: Enmity vs. Compersion
The most striking finding is the near-perfect negative correlation between the salience of **Enmity** and **Compersion** (*r* = -.91). This demonstrates a fundamental trade-off in rhetorical strategy: emphasizing conflict with an out-group appears to preclude any celebration of shared or others' success. It is the clearest statistical validation of the framework's oppositional design. Language high in enmity, which frames opponents as illegitimate actors who "write words into the law" (Source: steve_king_2017_house_floor.txt), exists at the opposite pole from language that fosters collective well-being. The intensity of these emotions is also strongly opposed (*r* = -.73), as seen in the contrast between antagonistic statements like "It is a system that inflicts poverty by concentrating its attacks on low-income neighborhoods" (Source: cory_booker_2018_first_step_act.txt) and unifying ones.

### 4.3 Pattern Recognition: Emotional Archetypes

K-Means clustering on the raw emotional scores identified three distinct rhetorical archetypes, revealing the different ways these emotional strategies are combined in practice.

**Table 4: Emotional Archetype Cluster Centers**
| Cluster Label | Archetype Name      | fear_raw | hope_raw | enmity_raw | amity_raw | envy_raw | compersion_raw |
|---------------|---------------------|----------|----------|------------|-----------|----------|----------------|
| 0             | **Threat-Focused**  | 0.80     | 0.35     | 0.50       | 0.25      | 0.00     | 0.00           |
| 1             | **High-Conflict**   | 0.78     | 0.61     | 0.77       | 0.68      | 0.80     | 0.16           |
| 2             | **Conciliatory**    | 0.20     | 0.70     | 0.00       | 0.90      | 0.00     | 0.90           |

1.  **Cluster 0: The "Threat-Focused" Archetype:** This profile is defined by high Fear (*M* = 0.80) and moderate Enmity (*M* = 0.50), with a near-total absence of positive emotions. It represents a pure grievance or siege mentality. The speeches by Mitt Romney and Steve King fall into this category, characterized by a focus on perceived transgressions and dangers without a corresponding hopeful vision.

2.  **Cluster 1: The "High-Conflict" Archetype:** This is the most common profile in the corpus, containing five of the eight documents (Lewis, Booker, Sanders, Ocasio-Cortez, Vance). It is characterized by high emotional intensity across the board, blending strong negative emotions (Fear, Enmity, Envy) with significant positive emotions (Hope, Amity). This archetype represents a populist or revolutionary struggle, one that articulates a hopeful vision for an in-group ("us") that is contingent on defeating a threatening out-group ("them").

3.  **Cluster 2: The "Conciliatory" Archetype:** This rare profile, represented only by John McCain's 2008 concession speech, is the inverse of the "Threat-Focused" archetype. It is defined by very high Hope (*M* = 0.70), Amity (*M* = 0.90), and Compersion (*M* = 0.90), with minimal negative emotion. This archetype embodies a rhetoric of unity, grace, and shared success.

**Table 5: Document Classification by Emotional Archetype**
| Document                                              | Cluster Label | Archetype Name    |
|-------------------------------------------------------|---------------|-------------------|
| john_mccain_2008_concession.txt                       | 2             | Conciliatory      |
| mitt_romney_2020_impeachment.txt                      | 0             | Threat-Focused    |
| steve_king_2017_house_floor.txt                       | 0             | Threat-Focused    |
| john_lewis_1963_march_on_washington.txt               | 1             | High-Conflict     |
| cory_booker_2018_first_step_act.txt                   | 1             | High-Conflict     |
| bernie_sanders_2025_fighting_oligarchy.txt            | 1             | High-Conflict     |
| alexandria_ocasio_cortez_2025_fighting_oligarchy.txt  | 1             | High-Conflict     |
| jd_vance_2022_natcon_conference.txt                   | 1             | High-Conflict     |

### 4.4 Framework Effectiveness Assessment

The ECF v10.0 framework demonstrates considerable effectiveness even with this limited dataset.
*   **Construct Validity:** The strong, theoretically consistent correlations serve as preliminary validation of the framework's constructs. Opposing dimensions like Enmity and Compersion are strongly negatively correlated, while allied dimensions like Hope and Amity are strongly positively correlated. This suggests the framework is measuring distinct and meaningful aspects of emotional language.
*   **Discriminatory Power:** The framework successfully differentiates between texts. The clustering analysis shows that the six dimensions, when used together, can sort documents into coherent and interpretable archetypes. The wide range of scores on the `emotional_climate_index` (from -0.63 to 0.76) further indicates its ability to capture the diverse emotional tones of the documents.
*   **Insight Generation:** The framework facilitates insights that go beyond simple sentiment analysis. By separating emotions like Enmity and Envy, and by including concepts like Compersion, it allows for a more nuanced understanding of political strategy. The distinction between raw intensity and salience is also analytically useful, highlighting the gap between latent emotion and deliberate rhetorical emphasis.

The primary limitation in assessing its effectiveness is the inability to test its performance with external variables like ideology, which would allow for hypothesis testing about group differences.

## 5. Discussion

This preliminary analysis, despite its small scale, offers a window into the emotional architecture of modern American political discourse. The findings suggest that political language is not a random assortment of emotions but is organized around coherent, and often conflicting, strategic imperatives. The two dominant strategies identified—a "Unity" strategy linking hope and amity, and a "Conflict" strategy linking fear and enmity—represent fundamental choices in how to frame political reality.

The prevalence of the "High-Conflict" archetype (Cluster 1) is particularly noteworthy. This hybrid model, which combines a hopeful vision for an in-group with a fearful, antagonistic posture toward an out-group, appears to be a dominant mode of political communication in this sample, used by figures across different eras and ideological positions. It suggests that a purely positive or purely negative appeal is less common than one that mobilizes supporters through a narrative of righteous struggle. The rarity of the purely "Conciliatory" archetype (Cluster 2) may be an artifact of the small sample, but it could also reflect a broader trend in contemporary politics where unity-focused rhetoric is less common or effective.

The framework's structure, particularly the Enmity/Compersion axis, proves to be a powerful lens for examining political polarization. The finding that an emphasis on Enmity systematically crowds out Compersion (*r* = -.91) provides a stark, quantitative measure of zero-sum political thinking. This dynamic is visible in the contrast between rhetoric that attacks institutions and rhetoric that seeks common ground. For example, a speaker attacking the Supreme Court's legitimacy by claiming they "write words into the law" (Source: steve_king_2017_house_floor.txt) is engaging in a rhetorical act that is structurally opposed to one that calls for unity and belief in "the promise and greatness of America" (Source: john_mccain_2008_concession.txt). This suggests that a key feature of polarizing discourse is the erasure of any possibility of shared success with the "other side."

### Limitations and Future Directions

This study's conclusions are highly provisional due to the N=8 sample size. The immediate priority for future research is to apply the ECF v10.0 framework to a large, representative, and diachronic corpus of political texts. This would allow for:
1.  **Validation of Archetypes:** Testing whether the three emotional archetypes identified here are robust and replicable in a larger dataset.
2.  **Hypothesis Testing:** Including metadata on speaker ideology, party, and the date of the speech would enable inferential statistical analysis (e.g., ANOVA, regression) to formally test hypotheses about how emotional climates have evolved over time and how they differ between political groups.
3.  **Exploring Polarization:** A larger corpus would allow for a more robust analysis of polarization by tracking the mean and variance of the `emotional_climate_index` and axis-balance scores within and between parties over several decades.

## 6. Conclusion

This report details a preliminary but insightful computational analysis of emotional climates in a small sample of American political discourse. Through the application of the ECF v10.0 framework, this study identified clear, structured, and often oppositional emotional strategies. The core findings highlight a fundamental tension between a "Unity" strategy (Hope/Amity) and a "Conflict" strategy (Fear/Enmity), which manifest in three distinct rhetorical archetypes.

The analysis provides strong preliminary evidence for the ECF v10.0 framework's construct validity and discriminatory power. Its ability to capture the inverse relationship between Enmity and Compersion is a particularly valuable contribution to the quantitative study of political polarization. While the small sample size mandates caution, the results lay a clear and promising foundation for future research. By scaling this analysis to a larger corpus, researchers can move from identifying these patterns to explaining their causes and tracking their consequences for democratic life.

## 7. Evidence Citations

*   **cory_booker_2018_first_step_act.txt**
    *   "We share those common values because we still live in a a nation where the ties that bind us are stronger than the lines that divide us."
    *   "It is a system that inflicts poverty by concentrating its attacks on low-income neighborhoods."
    *   "This system as a whole is a cancer on the soul of our country, and it's hurting every single American."
*   **jd_vance_2022_natcon_conference.txt**
    *   "But neither here nor there, um, the reason I'm most optimistic about the future of this movement and the future of our country is because for the first time in a very long time, it is clear that the l..."
    *   "Let's send our entire machinery for making war to countries that hate us and then let's spend what little stockpiles that we have on a war that has no obvious end in sight. That's the Wall Street Jour..."
    *   "The real threat to American democracy is that American voters keep on voting for less immigration and our politicians keep on rewarding us with more. That is the threat to American democracy."
*   **john_lewis_1963_march_on_washington.txt**
    *   "By the forces of our demands, our determination, and our numbers, we shall splinter the segregated South into a thousand pieces and put them together in the image of God and democracy."
*   **john_mccain_2008_concession.txt**
    *   "to not despair of our present difficulties, but to believe always in the promise and greatness of America."
    *   "defend our security in a dangerous world, and leave our children and grandchildren a stronger, better country than we inherited."
*   **bernie_sanders_2025_fighting_oligarchy.txt**
    *   "So if we stand together, are strong, are disciplined, are smart, I have every reason to believe deeply in my heart that not only will we defeat Trumpism, but we can create the kind of nation that we d..."
*   **steve_king_2017_house_floor.txt**
    *   "But the Supreme Court, wrapped in the cloak of Marbury versus Madison and their imagination of what precedents and star decisis might mean to them, decides that they can write words into the law."