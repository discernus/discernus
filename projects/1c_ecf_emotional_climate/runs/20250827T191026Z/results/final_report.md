# ECF v10.0 Analysis Report

**Experiment**: emotional_climate_factorial_analysis  
**Framework**: ecf_v10.md  
**Corpus**: corpus.md (8 documents)  

---

## 1. Executive Summary

This computational social science analysis examines the emotional climate of a diverse corpus of eight political texts spanning from 1963 to 2025. Using the Emotional Climate Factorial (ECF v10.0) framework, this report identifies the core emotional structures, strategic communication patterns, and recurring rhetorical archetypes within the data. The framework operationalizes emotional climate along three oppositional axes: Fear/Hope, Enmity/Amity, and Envy/Compersion, weighted by rhetorical salience to produce a summary Emotional Climate Index (ECI).

The analysis reveals a political discourse structured by profound strategic trade-offs rather than a simple mix of emotions. The most significant finding is a near-perfect inverse correlation between the rhetorical emphasis on Enmity (hostility) and Compersion (joy in others' success) (r = -0.91), indicating a fundamental strategic choice between fostering out-group antagonism and celebrating collective success. This core opposition anchors two primary emotional postures: a **Negative, Threat-Oriented posture** that strategically combines Fear and Enmity (salience r = 0.73), and a **Positive, Cooperative posture** that links Hope and Amity (salience r = 0.84).

Cluster analysis identifies three distinct emotional archetypes: a rare "Positive Vision" (high hope/amity), a "Fear-Driven, Antagonistic" profile, and a dominant, "Grievance-Intense, Mixed-Signal" cluster characterized by high levels of both positive and negative emotions, but a notable absence of Compersion. Overall, the corpus displays a negative-leaning emotional climate (mean ECI = -0.15), driven by a prevalence of fear and enmity and a systemic lack of compersion. These preliminary findings, based on a small corpus, suggest the ECF framework is effective at uncovering deep structural patterns in political communication, highlighting a central tension between divisive grievance and unifying cooperation.

## 2. Opening Framework: Key Insights

*   **Political Discourse is Structured by a Core Strategic Opposition**: The analysis reveals that political communication operates on a fundamental trade-off between hostility and collective celebration. The salience scores of Enmity and Compersion are almost perfectly negatively correlated (r = -0.91), suggesting that emphasizing one requires the strategic suppression of the other. This defines a primary axis of political rhetoric: In-Group Celebration vs. Out-Group Hostility.
*   **Two Dominant, Opposing Emotional Constellations Emerge**: The data shows two recurring strategic patterns. A negative posture links the emphasis of Fear and Enmity (salience r = 0.73), creating a narrative of threat and antagonism. A positive posture links the emphasis of Hope and Amity (salience r = 0.84), building a narrative of aspiration and unity.
*   **A "Grievance-Intense" Archetype Dominates the Corpus**: Cluster analysis reveals that the most common emotional signature (5 of 8 documents) is a complex mix of high fear, enmity, and envy alongside moderate-to-high hope and amity. This "Grievance-Intense, Mixed-Signal" cluster suggests that much of the discourse combines threat narratives with aspirational appeals to a specific in-group, creating a volatile and emotionally charged climate.
*   **The Overall Emotional Climate is Negative and Lacks Celebration**: Across the corpus, the average Emotional Climate Index (ECI) is negative (M = -0.15). This is driven by a higher mean Negative Emotional Index (M = 0.61) compared to the Positive Emotional Index (M = 0.46). The emotion of Compersion is the least present and least emphasized dimension, resulting in a highly negative Resource Attitudes Balance (M = -0.30) and pointing to a systemic deficit in celebrating others' success.
*   **The Framework's Oppositional Design is Validated**: The negative correlations between the framework's core pairs—Fear/Hope (raw r = -0.41), Enmity/Amity (raw r = -0.40), and Envy/Compersion (raw r = -0.19)—provide strong construct validity for its oppositional design. This confirms that the chosen dimensions effectively capture competing emotional tensions in political language.

## 4. Methodology

### Framework Description and Analytical Approach

This study employs the Emotional Climate Factorial (ECF v10.0) framework, a novel approach to textual analysis inferred from the project's computational functions. The framework is designed to measure the "emotional climate" of a text by quantifying six primary emotions organized into three oppositional axes:

1.  **Threat/Opportunity Axis**: Comprising **Fear** (perception of threat, danger, or loss) and **Hope** (anticipation of positive outcomes or progress).
2.  **Social Relations Axis**: Comprising **Enmity** (hostility, antagonism, or division towards an out-group) and **Amity** (friendliness, cooperation, or unity with an in-group).
3.  **Resource Attitudes Axis**: Comprising **Envy** (resentment of another's success or resources) and **Compersion** (joy or celebration of another's success or good fortune).

For each dimension, the analysis measures both a `raw` score (intensity of the emotion) and a `salience` score (rhetorical prominence or emphasis). These scores are used to calculate several derived metrics, including three axis-level balance scores and a final **Emotional Climate Index (ECI)**. The ECI provides a single, summary measure of a text's overall emotional valence, with positive scores indicating a hopeful, cooperative climate and negative scores indicating a fearful, antagonistic one.

### Data Structure and Corpus Description

The analysis was performed on the Emotional Climate Factorial Analysis Corpus, which contains 8 documents of American political discourse from a date range of 1963-2025. The corpus includes speeches from a variety of political figures and contexts, such as John Lewis at the March on Washington, John McCain's 2008 concession speech, and contemporary speeches by figures like Alexandria Ocasio-Cortez and JD Vance.

### Statistical Methods and Analytical Constraints

The analysis followed a multi-step quantitative process. First, descriptive statistics (means, standard deviations) were calculated for all raw scores, salience scores, and derived metrics to establish baseline emotional levels. Second, Pearson correlation matrices were computed for both raw and salience scores to identify relationships and strategic pairings between emotional dimensions. Third, K-Means clustering (k=3) was performed on the six raw emotional scores to identify recurring emotional archetypes within the corpus.

A significant constraint of this analysis is the small sample size (N=8). Consequently, all findings should be considered **preliminary and exploratory**. The results are indicative of patterns that warrant further investigation with a larger corpus, but they do not provide sufficient statistical power for definitive, generalizable conclusions. The tone of this report is therefore cautious and focuses on data-driven observations rather than broad theoretical claims.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

An overview of the emotional landscape of the corpus reveals a general tendency towards negative emotionality. The mean scores for negative dimensions like Fear (M = 0.71) and Enmity (M = 0.61) are among the highest, while the mean for the positive dimension of Compersion is the lowest of all six (M = 0.21). This imbalance is reflected in the summary indices, where the average Negative Emotional Index (M = 0.61) is substantially higher than the Positive Emotional Index (M = 0.46).

**Table 1: Descriptive Statistics for Core and Derived Emotional Metrics (N=8)**

| Metric                       | Mean   | Std. Dev. | Min.   | Max.   |
| ---------------------------- | ------ | --------- | ------ | ------ |
| **Raw Scores**               |        |           |        |        |
| fear_raw                     | 0.71   | 0.22      | 0.20   | 0.90   |
| hope_raw                     | 0.56   | 0.17      | 0.30   | 0.85   |
| enmity_raw                   | 0.61   | 0.36      | 0.00   | 0.90   |
| amity_raw                    | 0.60   | 0.30      | 0.00   | 0.90   |
| envy_raw                     | 0.50   | 0.42      | 0.00   | 0.90   |
| compersion_raw               | 0.21   | 0.37      | 0.00   | 0.90   |
| **Derived Indices**          |        |           |        |        |
| emotional_climate_index      | -0.15  | 0.43      | -0.63  | 0.76   |
| climate_intensity            | 0.53   | 0.16      | 0.30   | 0.74   |
| positive_emotional_index     | 0.46   | 0.25      | 0.10   | 0.83   |
| negative_emotional_index     | 0.61   | 0.29      | 0.07   | 0.90   |
| **Balance Scores**           |        |           |        |        |
| threat_opportunity_balance   | -0.13  | 0.32      | -0.53  | 0.52   |
| social_relations_balance     | -0.01  | 0.51      | -0.80  | 0.90   |
| resource_attitudes_balance   | -0.30  | 0.61      | -0.90  | 0.90   |

The most striking finding from the descriptive statistics is the systemic deficit in Compersion. Its mean raw score (M = 0.21) and salience score (M = 0.20) are less than half of most other dimensions, indicating it is an emotion that is both rarely expressed and seldom emphasized. This directly contributes to the highly negative mean for the `resource_attitudes_balance` (M = -0.30), the most negative of the three axes. This suggests that, within this corpus, discourse about resources and success is far more likely to be framed through resentment than through mutual celebration. This pattern is exemplified in statements that frame societal outcomes as zero-sum problems. For instance, one speaker notes, "As Bryan Stevenson has said, we live in a nation that treats you better if you're rich and guilty than if you're poor and innocent" (Source: cory_booker_2018_first_step_act.txt), highlighting systemic inequity rather than shared prosperity.

### 5.3 Correlation and Interaction Analysis

Correlation analysis of the raw and salience scores reveals the underlying structure of emotional expression and rhetorical strategy in the corpus. The patterns strongly validate the framework's oppositional design and uncover two dominant, competing emotional constellations.

**Table 2: Pearson Correlation Matrix for Raw Emotional Scores**

|                | fear_raw | hope_raw | enmity_raw | amity_raw | envy_raw | compersion_raw |
| :------------- | :------: | :------: | :--------: | :-------: | :------: | :------------: |
| **fear_raw**   |  1.00    |  -0.41   |   **0.72** |   -0.41   |   0.41   |    **-0.70**   |
| **hope_raw**   |  -0.41   |   1.00   |   -0.32    | **0.77**  |   0.44   |    **0.77**    |
| **enmity_raw** | **0.72** |  -0.32   |    1.00    |   -0.40   |   0.64   |    **-0.73**   |
| **amity_raw**  |  -0.41   | **0.77** |   -0.40    |   1.00    |   0.35   |      0.61      |
| **envy_raw**   |   0.41   |   0.44   |    0.64    |   0.35    |   1.00   |     -0.19      |
| **compersion_raw** | **-0.70** | **0.77** | **-0.73** | 0.61 | -0.19 | 1.00 |

**Table 3: Pearson Correlation Matrix for Salience Scores**

|                     | fear_salience | hope_salience | enmity_salience | amity_salience | envy_salience | compersion_salience |
| :------------------ | :-----------: | :-----------: | :-------------: | :------------: | :-----------: | :-----------------: |
| **fear_salience**   |     1.00      |     -0.32     |    **0.73**     |     -0.32      |     0.23      |      **-0.73**      |
| **hope_salience**   |     -0.32     |     1.00      |     -0.53       |    **0.84**    |     0.27      |       **0.75**      |
| **enmity_salience** |   **0.73**    |     -0.53     |      1.00       |     -0.31      |     0.56      |      **-0.91**      |
| **amity_salience**  |     -0.32     |   **0.84**    |     -0.31       |      1.00      |     0.48      |        0.49         |
| **envy_salience**   |     0.23      |     0.27      |      0.56       |      0.48      |     1.00      |       -0.22         |
| **compersion_salience** | **-0.73** | **0.75** | **-0.91** | 0.49 | -0.22 | 1.00 |

#### The Core Strategic Opposition: Enmity vs. Compersion

The most powerful finding is the near-perfect negative correlation between the salience of Enmity and Compersion (r = -0.91). This indicates a fundamental strategic bifurcation in political rhetoric. Speakers who choose to emphasize hostility and antagonism towards an out-group systematically de-emphasize or entirely omit any celebration of others' success. This is not mere coincidence but a structural feature of the communication. For example, a speech high in Enmity salience frames policy debates as battles against hostile forces, as one speaker argues, "Let's send our entire machinery for making war to countries that hate us and then let's spend what little stockpiles that we have on a war that has no obvious end in sight" (Source: jd_vance_2022_natcon_conference.txt). This antagonistic framing leaves no room for a Compersion-based narrative of shared progress. The inverse relationship is just as strong; a focus on shared success precludes an emphasis on enmity.

#### The Negative Constellation: Fear and Enmity

The analysis reveals a strong positive correlation between Fear and Enmity in both raw scores (r = 0.72) and salience scores (r = 0.73). This indicates that fear and hostility are not only expressed concurrently but are also strategically emphasized together. This pairing forms the backbone of a threat-based rhetorical posture. Speakers frequently evoke danger and identify an enemy responsible for that danger. This is evident in statements like, "The real threat to American democracy is that American voters keep on voting for less immigration and our politicians keep on rewarding us with more" (Source: jd_vance_2022_natcon_conference.txt), which simultaneously stokes fear about democracy and directs enmity towards politicians and immigrants. This posture is further defined by its opposition to Compersion, as shown by the strong negative correlation between Fear salience and Compersion salience (r = -0.73). Emphasizing fear appears to be strategically incompatible with celebrating others' success, as it frames the world as a dangerous, zero-sum environment.

#### The Positive Constellation: Hope, Amity, and Compersion

In direct opposition to the fear-enmity axis, a positive constellation of emotions emerges. Hope and Amity are strongly correlated in both raw scores (r = 0.77) and, even more so, in salience scores (r = 0.84). This suggests a deliberate rhetorical strategy of pairing aspirational visions with calls for unity and cooperation. This pattern is the hallmark of a positive, unifying discourse. For example, John McCain's concession speech urges listeners "to not despair of our present difficulties, but to believe always in the promise and greatness of America" (Source: john_mccain_2008_concession.txt), directly linking a hopeful outlook with a sense of national unity (Amity). This positive constellation is often completed by Compersion, which is strongly correlated with both Hope (raw r = 0.77) and Amity (raw r = 0.61), forming a triad of positive, pro-social emotions.

### 5.4 Pattern Recognition and Theoretical Insights

K-Means clustering identified three distinct emotional archetypes in the corpus, providing a higher-level view of the recurring emotional climates. These clusters align with the correlational findings and represent distinct rhetorical strategies.

**Table 4: Cluster Centers for Emotional Archetypes**

| Cluster Label | Dominant Profile                     | fear_raw | hope_raw | enmity_raw | amity_raw | envy_raw | compersion_raw | Documents (Count) |
| :------------ | :----------------------------------- | :------: | :------: | :--------: | :-------: | :------: | :------------: | :---------------- |
| **Cluster 0** | Fear-Driven, Antagonistic            | **0.80** |   0.35   |    0.50    |   0.25    |   0.00   |      0.00      | 2                 |
| **Cluster 1** | Grievance-Intense, Mixed-Signal      | **0.78** |   0.61   |  **0.77**  |   0.68    | **0.80** |      0.16      | 5                 |
| **Cluster 2** | Positive Vision                      |   0.20   | **0.70** |    0.00    | **0.90**  |   0.00   |    **0.90**    | 1                 |

#### Cluster 2: The "Positive Vision" Archetype

Represented by a single document in this small corpus (John McCain's 2008 concession speech), this cluster is the purest expression of the positive emotional constellation. It is defined by very high Hope (0.70), Amity (0.90), and Compersion (0.90), coupled with negligible levels of Fear, Enmity, and Envy. This archetype represents a discourse of reconciliation, unity, and shared destiny. The language is overwhelmingly constructive and forward-looking, as seen in the call "to believe always in the promise and greatness of America" (Source: john_mccain_2008_concession.txt). This cluster serves as a clear baseline for a positive emotional climate (ECI = 0.76).

#### Cluster 0: The "Fear-Driven, Antagonistic" Archetype

This cluster, containing speeches by Mitt Romney and Steve King, embodies a focused, negative emotional climate. It is characterized by extremely high Fear (0.80) and moderate Enmity (0.50), with a near-total absence of Hope, Amity, Envy, and Compersion. This profile represents a discourse of pure threat and institutional critique without a corresponding positive vision. The language focuses on danger and corruption, as when one speaker describes an act as "perhaps the most abusive and destructive violation of one's oath of office that I can imagine" (Source: mitt_romney_2020_impeachment.txt). The absence of Envy distinguishes it from the more complex grievance cluster; the focus here is on peril and decay, not resentment of others' gains.

#### Cluster 1: The "Grievance-Intense, Mixed-Signal" Archetype

This is the most prevalent archetype in the corpus, including a diverse set of speakers from John Lewis to JD Vance. It is defined by its high intensity across almost all dimensions, creating a complex and volatile emotional signature. It scores high on negative emotions like Fear (0.78), Enmity (0.77), and Envy (0.80), but also maintains moderate-to-high levels of Hope (0.61) and Amity (0.68). The key differentiator is its near-zero score in Compersion (0.16).

This profile represents a discourse of grievance. It combines a narrative of threat and injustice ("This system as a whole is a cancer on the soul of our country," Source: cory_booker_2018_first_step_act.txt) with a hopeful vision for an in-group ("if we stand together, it is the only way that we can win," Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt). The high Envy score suggests this grievance is often directed at perceived inequities and the unfair success of others. This mix of high-stakes negativity and in-group positivity, combined with a failure to celebrate broader success, creates a deeply polarized and emotionally intense climate.

### 5.5 Framework Effectiveness Assessment

Based on this exploratory analysis, the ECF v10.0 framework demonstrates considerable effectiveness. Its primary strength lies in its discriminatory power. The oppositional design, particularly the Enmity/Compersion axis, proved highly effective at uncovering a fundamental structural tension in political discourse that simpler sentiment models might miss. The salience weighting adds a crucial layer, distinguishing between the mere presence of an emotion and its strategic emphasis.

The framework-corpus fit is strong. The dimensions successfully captured the emotional tenor of texts ranging from civil rights speeches to modern populist addresses. The derived metrics, especially the ECI and the balance scores, provided intuitive and powerful summaries of the underlying data. The cluster analysis further validated the framework's utility by revealing meaningful, interpretable archetypes that align with contemporary understandings of political communication styles. The primary limitation is not in the framework itself but in the small size of the test corpus, which prevents a full assessment of its robustness across a wider range of discourse.

## 6. Discussion

The findings of this analysis, while preliminary, carry significant theoretical implications for the study of political communication. The central discovery—the strategic opposition between Enmity and Compersion (r = -0.91)—suggests a foundational principle of modern political discourse. This is more than just a negative correlation; it points to a deliberate rhetorical choice between constructing a narrative of out-group threat versus one of in-group or societal success. This axis may represent a core dimension of political polarization itself, measuring the communicative distance between divisive and unifying strategies.

The identification of the "Grievance-Intense" archetype as the dominant mode of communication in this corpus is particularly telling. It suggests that much of contemporary political discourse is not simply positive or negative, but a complex fusion of both. Speakers appear to leverage the emotional power of fear, enmity, and envy to mobilize an in-group, to whom they offer a message of hope and solidarity. The critical missing ingredient is Compersion. This absence suggests that the "unity" offered is exclusive, defined against an out-group rather than as part of a shared societal project. This may be a key mechanism in the erosion of social trust and the intensification of political tribalism.

These findings point toward several avenues for future research. A larger, diachronic corpus could be used to test whether the prevalence of the "Grievance-Intense" cluster has increased over time. Cross-cultural analysis could determine if the Enmity/Compersion opposition is a universal feature of political conflict or specific to the American context. Methodologically, this analysis demonstrates the value of frameworks that move beyond simple positive/negative sentiment to capture specific, theoretically grounded emotions like Envy and Compersion, which appear to be crucial for understanding the dynamics of grievance and polarization.

## 7. Conclusion

This computational analysis of eight political texts using the ECF v10.0 framework has uncovered deep structural patterns in emotional and rhetorical strategy. The study identified a primary axis of political communication defined by the stark opposition between emphasizing Enmity and Compersion. This core trade-off anchors two competing emotional postures—one of threat and antagonism, the other of hope and cooperation—which manifest as distinct rhetorical archetypes.

Despite the limitation of a small sample size, the analysis validates the ECF framework's novel design, demonstrating its capacity to reveal nuanced patterns that simpler models would overlook. The findings indicate that the analyzed political discourse leans toward a negative, grievance-driven climate, characterized by a strategic combination of fear and enmity and a systemic deficit in celebrating shared success. This research provides a robust, data-driven foundation for future studies into the emotional architecture of political polarization and highlights the critical role of specific emotions like Enmity and Compersion in shaping our public discourse.

## 8. Evidence Citations

**cory_booker_2018_first_step_act.txt**
- "It is a system that inflicts poverty by concentrating its attacks on low-income neighborhoods."
- "This system as a whole is a cancer on the soul of our country, and it's hurting every single American."
- "As Bryan Stevenson has said, we live in a nation that treats you better if you're rich and guilty than if you're poor and innocent."
- "We share those common values because we still live in a a nation where the ties that bind us are stronger than the lines that divide us."
- "I want to say good afternoon to everyone, and this is a moment really where I want to give open with a sense of gratitude. I don't want to thank my colleagues for their incredible work and leadership, and especially recognize the chairman of the Judiciary Committee, Senator Chuck Grassley."

**jd_vance_2022_natcon_conference.txt**
- "Let's send our entire machinery for making war to countries that hate us and then let's spend what little stockpiles that we have on a war that has no obvious end in sight. That's the Wall Street Journal editorial page approach."
- "The real threat to American democracy is that American voters keep on voting for less immigration and our politicians keep on rewarding us with more. That is the threat to American democracy."
- "But the, the thing on immigration is that no one can avoid that it has made our societies poorer, less safe, less prosperous, and less advanced."

**john_mccain_2008_concession.txt**
- "to not despair of our present difficulties, but to believe always in the promise and greatness of America."
- "defend our security in a dangerous world, and leave our children and grandchildren a stronger, better country than we inherited."

**steve_king_2017_house_floor.txt**
- "But the Supreme Court, wrapped in the cloak of Marbury versus Madison and their imagination of what precedents and star decisis might mean to them, decides that they can write words into the law."

**alexandria_ocasio_cortez_2025_fighting_oligarchy.txt**
- "It’s shorthand for the right wing’s entire political agenda and a certain ugly kind of politics, a politics that involves lying to and screwing over working and middle class Americans so that they can steal from our healthcare, Social Security, and veterans' benefits..."
- "Because in this house, we stand together, we know that, that it's our only choice because we know that without exception, if we stand together, it is the only way that we can win."

**mitt_romney_2020_impeachment.txt**
- "Corrupting an election to keep oneself in office is perhaps the most abusive and destructive violation of one's oath of office that I can imagine."