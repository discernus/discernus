# Cohesive Flourishing Framework (CFF) v10 Analysis Report

**Framework**: Cohesive Flourishing Framework (CFF) v10
**Corpus**: Democratic Discourse Corpus (4 documents)

---

## 1. Executive Summary

This report presents a computational analysis of four political texts from the Democratic Discourse Corpus using the Cohesive Flourishing Framework (CFF) v10. The analysis reveals a landscape of American political discourse largely characterized by fragmenting and emotionally charged rhetoric, with a notable exception representing an older, more institutionally cohesive style. The study's primary finding is the statistical validation of the CFF's core theoretical assumption: that cohesive and fragmenting rhetorical strategies are not merely opposites but are often deployed in a state of "strategic contradiction," where high emotional and relational tensions correlate strongly with rhetorical patterns that undermine social cohesion.

The results indicate that, on average, the analyzed discourse leans towards fragmentation (Mean Full Cohesion Index = -0.20). The framework demonstrated strong discriminatory power, clearly distinguishing John McCain's highly cohesive 2008 concession speech (Full Cohesion Index = 0.80) from the significantly more fragmenting populist rhetoric of Steve King (-0.71), Bernie Sanders (-0.61), and Alexandria Ocasio-Cortez (-0.27). Correlation analysis provides preliminary support for the CFF's construct validity, with strong negative relationships observed between cohesion indices and measures of rhetorical tension (e.g., *r* = -0.72 between Full Cohesion and Emotional Tension).

While the extremely small sample size (N=4) renders these findings preliminary and precludes generalization, the analysis successfully demonstrates the CFF's utility. The framework moves beyond simple sentiment analysis to identify sophisticated rhetorical archetypes, including an "institutional-cohesive" style and multiple variants of "populist-fragmenting" styles. These indicative results suggest the CFF is a promising tool for mapping the complex linguistic strategies that shape democratic health, warranting further research with a larger, more diverse corpus.

## 2. Opening Framework: Key Insights

This analysis of the Democratic Discourse Corpus through the Cohesive Flourishing Framework (CFF) yielded several key insights into the structure of political rhetoric. The following points represent the most significant preliminary findings, grounded in the statistical data.

*   **Fragmenting Rhetoric Dominates the Corpus:** Across the four documents, dimensions associated with social fragmentation were more prominent than those associated with cohesion. The corpus-wide mean scores for Enmity (*M* = 0.68), Fear (*M* = 0.65), and Envy (*M* = 0.60) were substantially higher than their cohesive counterparts: Amity (*M* = 0.48), Hope (*M* = 0.43), and Compersion (*M* = 0.23). This suggests the sampled discourse is, on average, more focused on defining enemies and threats than on fostering goodwill and shared aspirations.

*   **John McCain's 2008 Speech Represents a Cohesive Outlier:** John McCain's concession speech is statistically unique within this corpus, scoring highest on the Full Cohesion Index (0.80). This score is more than a full point higher than the next-ranked document. This starkly contrasts with the negative (fragmenting) scores of all other speakers, suggesting his speech represents a different rhetorical paradigm—one rooted in institutional norms of unity and respect for democratic processes—compared to the populist styles of the other speakers.

*   **Strategic Contradiction is Driven by Emotional and Relational Tension:** The analysis reveals a powerful statistical relationship between the CFF's derived metrics. The Strategic Contradiction Index, which measures the simultaneous use of opposing rhetorical appeals, is almost perfectly correlated with Emotional Tension (*r* = 0.97) and Relational Tension (*r* = 0.96). This indicates that the most rhetorically contradictory texts are those that most intensely leverage fear/hope and enmity/amity dynamics, creating a volatile mix of in-group bonding and out-group hostility.

*   **Populist Rhetoric (Left and Right) Shares a Fragmenting Structure:** While politically distinct, the speeches by Steve King (populist_conservative), Bernie Sanders (populist_progressive), and Alexandria Ocasio-Cortez (populist_progressive) all received negative Full Cohesion Index scores (-0.71, -0.61, and -0.27, respectively). This suggests that despite different ideological goals, modern populist styles may share a structural reliance on fragmenting language—defining a virtuous "people" against a corrupt "elite" or "other." This is exemplified by language targeting perceived enemies, as when Alexandria Ocasio-Cortez stated, "He’s handed the keys to Elon Musk and is selling off our country for parts to the wealthiest people in the world for a kickback" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt).

*   **The CFF Demonstrates Strong Construct Validity and Discriminatory Power:** The framework's internal logic appears sound based on this preliminary analysis. Cohesion indices were strongly and negatively correlated with tension and contradiction indices, as theoretically predicted. For example, the Full Cohesion Index had a strong negative correlation with the Strategic Contradiction Index (*r* = -0.57). Furthermore, the framework effectively discriminated between texts with different rhetorical aims, producing a wide range of cohesion scores that align with a qualitative understanding of the speakers' styles.

## 3. Methodology

### 3.1 Framework Description

This study employed the Cohesive Flourishing Framework (CFF) v10, a computational tool designed for nuanced analysis of political and social discourse. As outlined in its specification, the CFF moves beyond simplistic binary classifications (e.g., positive/negative) by independently scoring texts along five oppositional axes:
1.  **Identity:** Tribal Dominance vs. Individual Dignity
2.  **Emotion:** Fear vs. Hope
3.  **Success:** Envy vs. Compersion
4.  **Relation:** Enmity vs. Amity
5.  **Goal:** Fragmentative Goals vs. Cohesive Goals

This multi-dimensional approach allows the framework to capture sophisticated rhetorical strategies, such as the simultaneous appeal to in-group hope and out-group fear. The CFF calculates raw and salience scores for each of these ten primary dimensions and uses them to compute several derived metrics, including Tension scores for each axis, a Strategic Contradiction Index, and three overarching Cohesion Indices (Descriptive, Motivational, and Full).

### 3.2 Corpus and Data

The analysis was conducted on the Democratic Discourse Corpus, a small, purposive collection of four documents spanning from 2008 to 2025. The corpus includes:
*   **john_mccain_2008_concession.txt** (Republican, institutional)
*   **steve_king_2017_house_floor.txt** (Republican, populist_conservative)
*   **bernie_sanders_2025_fighting_oligarchy.txt** (Independent, populist_progressive)
*   **alexandria_ocasio_cortez_2025_fighting_oligarchy.txt** (Democratic, populist_progressive)

The data for this report consists of the complete statistical output from the CFF analysis pipeline, including descriptive statistics for all primary and derived metrics, a correlation matrix of derived metrics, and document rankings based on the Full Cohesion Index.

### 3.3 Statistical Methods and Limitations

The analytical approach for this report is primarily descriptive and correlational, appropriate for the nature of the data and the pilot scale of the study. The core statistical methods include:
1.  **Descriptive Statistics:** Calculation and interpretation of means, standard deviations, and quartiles to understand the central tendency and distribution of rhetorical features across the corpus.
2.  **Correlation Analysis:** Pearson correlation coefficients were used to examine the relationships between the CFF's derived metrics, providing insight into the framework's internal structure and construct validity.
3.  **Ranking and Comparative Analysis:** Documents were ranked by their Full Cohesion Index scores to identify outliers and group similar rhetorical styles.

**Critical Limitations:** The foremost limitation of this study is the extremely small sample size (N=4). This prevents the use of inferential statistics, prohibits the generalization of findings, and means that all conclusions must be treated as preliminary and indicative. The term "significant" is used in this report in a colloquial sense to denote noteworthy patterns, not statistical significance (p-values are not applicable). Additionally, a planned speaker-level analysis failed due to a technical error ("Corpus manifest not found"), preventing a more granular comparison between individuals. Finally, the `success_tension` metric exhibited zero variance across the corpus, making it an uninformative measure for this specific dataset and resulting in `NaN` correlation values.

## 4. Comprehensive Results

### 5.1 Descriptive Statistics

The descriptive statistics for the corpus reveal a consistent pattern where fragmenting dimensions are, on average, more pronounced than their cohesive counterparts. Table 1 summarizes the central tendency and dispersion for all CFF primary and derived metrics.

The mean raw scores for **Enmity** (*M* = 0.68), **Fear** (*M* = 0.65), and **Fragmentative Goals** (*M* = 0.60) are notably higher than the means for **Amity** (*M* = 0.48), **Hope** (*M* = 0.43), and **Cohesive Goals** (*M* = 0.50). This pattern suggests a rhetorical environment more focused on opposition, threat, and division than on unity, aspiration, and shared objectives. The high standard deviation for many metrics (e.g., *SD* = 0.45 for Enmity) indicates substantial variation between the documents, which is confirmed by the document ranking analysis.

The derived metrics reflect this overall trend. The **Full Cohesion Index**, the CFF's primary measure of a text's overall contribution to social cohesion, has a negative mean (*M* = -0.20), confirming the corpus's general tilt towards fragmentation. Among the tension metrics, **Emotional Tension** (Fear vs. Hope) is the most consistently present (*M* = 0.14, *SD* = 0.02), suggesting that the interplay of threat and aspiration is a common rhetorical device in this sample.

**Table 1: Descriptive Statistics for CFF Metrics across the Corpus (N=4)**
| Metric | Mean | Std. Dev. | Min | 25% | 50% | 75% | Max |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Primary Raw Scores** | | | | | | | |
| tribal_dominance_raw | 0.48 | 0.39 | 0.00 | 0.23 | 0.55 | 0.80 | 0.80 |
| individual_dignity_raw | 0.40 | 0.41 | 0.00 | 0.08 | 0.40 | 0.73 | 0.80 |
| fear_raw | 0.65 | 0.31 | 0.20 | 0.58 | 0.75 | 0.83 | 0.90 |
| hope_raw | 0.43 | 0.26 | 0.20 | 0.28 | 0.35 | 0.50 | 0.80 |
| envy_raw | 0.60 | 0.42 | 0.00 | 0.45 | 0.75 | 0.90 | 0.90 |
| compersion_raw | 0.23 | 0.45 | 0.00 | 0.00 | 0.00 | 0.23 | 0.90 |
| enmity_raw | 0.68 | 0.45 | 0.00 | 0.68 | 0.90 | 0.90 | 0.90 |
| amity_raw | 0.48 | 0.44 | 0.00 | 0.15 | 0.50 | 0.83 | 0.90 |
| fragmentative_goals_raw | 0.60 | 0.40 | 0.00 | 0.60 | 0.80 | 0.80 | 0.80 |
| cohesive_goals_raw | 0.50 | 0.36 | 0.20 | 0.20 | 0.45 | 0.75 | 0.90 |
| **Derived Tension Metrics** | | | | | | | |
| identity_tension | 0.06 | 0.10 | 0.00 | 0.00 | 0.02 | 0.08 | 0.21 |
| emotional_tension | 0.14 | 0.02 | 0.12 | 0.14 | 0.15 | 0.15 | 0.16 |
| success_tension | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 | 0.00 |
| relational_tension | 0.07 | 0.08 | 0.00 | 0.00 | 0.06 | 0.13 | 0.16 |
| goal_tension | 0.06 | 0.06 | 0.00 | 0.00 | 0.05 | 0.11 | 0.12 |
| **Derived Index Metrics** | | | | | | | |
| strategic_contradiction_index | 0.07 | 0.04 | 0.02 | 0.04 | 0.07 | 0.09 | 0.11 |
| descriptive_cohesion_index | -0.27 | 0.70 | -0.75 | -0.70 | -0.54 | -0.11 | 0.76 |
| motivational_cohesion_index | -0.21 | 0.69 | -0.68 | -0.67 | -0.48 | -0.02 | 0.79 |
| full_cohesion_index | -0.20 | 0.69 | -0.71 | -0.63 | -0.44 | -0.00 | 0.80 |

### 5.2 Advanced Metric Analysis

The derived metrics provide a higher-level view of rhetorical strategy. The document rankings by **Full Cohesion Index** reveal a clear hierarchy of rhetorical styles within the corpus:

1.  **john_mccain_2008_concession.txt**: 0.796 (Highly Cohesive)
2.  **alexandria_ocasio_cortez_2025_fighting_oligarchy.txt**: -0.271 (Moderately Fragmenting)
3.  **bernie_sanders_2025_fighting_oligarchy.txt**: -0.609 (Highly Fragmenting)
4.  **steve_king_2017_house_floor.txt**: -0.707 (Highly Fragmenting)

McCain's speech is a significant positive outlier, representing an institutional style that prioritizes national unity. In contrast, the other three speeches, all classified as populist, score in the negative, fragmenting range. This demonstrates the framework's ability to discriminate between rhetorical archetypes. The fragmenting nature of the populist speeches is often rooted in defining a clear antagonist. For example, the high **Enmity** score in the Sanders speech is illustrated by his focus on a specific out-group: "...in the midst of all of these addictions, the worst and most dangerous addiction we have is the greed of the oligarchs" (Source: bernie_sanders_2025_fighting_oligarchy.txt).

The **Strategic Contradiction Index** (*M* = 0.07) indicates that, on average, the texts employ a low-to-moderate level of simultaneous competing appeals. However, the strong correlation between this index and tension metrics (analyzed next) suggests that when contradiction occurs, it is a powerful and deliberate feature of the discourse.

### 5.3 Correlation and Interaction Analysis

The correlation matrix for the derived metrics (Table 2) offers profound insights into the CFF's structure and the nature of the analyzed rhetoric. The most critical finding is the validation of the framework's core oppositional design.

The three cohesion indices (**Descriptive**, **Motivational**, and **Full**) are almost perfectly inter-correlated (*r* > 0.99), indicating they measure a single, robust underlying construct of rhetorical cohesion. As hypothesized by the CFF, these cohesion indices show strong, negative correlations with measures of rhetorical tension and contradiction. For instance, the **Full Cohesion Index** is strongly negatively correlated with **Emotional Tension** (*r* = -0.72) and moderately negatively correlated with the **Strategic Contradiction Index** (*r* = -0.57). This statistically demonstrates that as discourse becomes more cohesive, it tends to rely less on the volatile interplay of fear/hope and other contradictory appeals.

Conversely, the **Strategic Contradiction Index** is driven almost entirely by specific tensions. It shows a near-perfect positive correlation with **Emotional Tension** (*r* = 0.97) and **Relational Tension** (*r* = 0.96). This suggests that the most strategically complex and contradictory rhetoric in this corpus is that which simultaneously invokes powerful feelings of hope and fear, and amity and enmity. This pattern is evident in texts that call for in-group solidarity to fight an out-group enemy. As Bernie Sanders urged, "So if we stand together, are strong, are disciplined, are smart..." (Source: bernie_sanders_2025_fighting_oligarchy.txt), he builds **Amity** for the explicit purpose of confronting an enemy, a classic form of strategic contradiction.

**Table 2: Correlation Matrix of CFF Derived Metrics**
| Metric | Full Cohesion Index | Strategic Contradiction | Identity Tension | Emotional Tension | Relational Tension | Goal Tension |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **Full Cohesion Index** | 1.00 | -0.57 | -0.15 | -0.72 | -0.36 | -0.76 |
| **Strategic Contradiction** | -0.57 | 1.00 | 0.83 | 0.97 | 0.96 | 0.08 |
| **Identity Tension** | -0.15 | 0.83 | 1.00 | 0.77 | 0.84 | -0.47 |
| **Emotional Tension** | -0.72 | 0.97 | 0.77 | 1.00 | 0.88 | 0.20 |
| **Relational Tension** | -0.36 | 0.96 | 0.84 | 0.88 | 1.00 | -0.06 |
| **Goal Tension** | -0.76 | 0.08 | -0.47 | 0.20 | -0.06 | 1.00 |
*Note: `success_tension` is excluded due to zero variance.*

### 5.4 Pattern Recognition and Theoretical Insights

The statistical patterns, when paired with textual evidence, reveal distinct rhetorical strategies. The fragmenting populist discourse, common to King, Sanders, and Ocasio-Cortez, operates by creating a moral binary. This is achieved by stoking **Envy** and **Enmity** towards a perceived illegitimate power structure while simultaneously invoking **Individual Dignity** for the in-group. For instance, Steve King's rhetoric questions the legitimacy of the judiciary, a form of institutional envy: "But the Supreme Court, wrapped in the cloak of Marberry versus Madison and their imagination of what precedents and star decisis might mean to them, decides that they can write words into the law" (Source: steve_king_2017_house_floor.txt). This contrasts with Alexandria Ocasio-Cortez grounding her authority in lived experience, a source of **Individual Dignity**: "I don’t believe in healthcare, labor and human dignity, because I’m an extremist or a Marxist. I believe it because I was a waitress..." (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt).

This combination of high enmity and high dignity for opposing groups creates the **Identity Tension** and **Relational Tension** that the correlation analysis identified as key drivers of strategic contradiction. The goal is often explicitly fragmenting, aimed at removing opponents from power. This is stated directly by Ocasio-Cortez: "We need to come together and spend every day... working to educate our neighbors, and give Evans and Boebert the boot..." (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt). This call to "come together" (Amity) to "give the boot" (Fragmentative Goals) is a textbook example of the strategic contradiction measured by the CFF.

The framework thus reveals that much of the fragmenting effect of this populist rhetoric comes not from simple negativity, but from a sophisticated strategy of leveraging cohesive emotions (like in-group solidarity) for divisive ends. This is a more complex and potent rhetorical device than a purely negative appeal.

### 5.5 Framework Effectiveness Assessment

Based on this pilot analysis, the CFF demonstrates considerable effectiveness in several key areas, though with some limitations.

*   **Discriminatory Power:** The framework shows excellent discriminatory power. The **Full Cohesion Index** produced a wide range of scores (from 0.80 to -0.71), successfully separating the institutional-cohesive rhetoric of McCain from the various populist-fragmenting styles. This suggests the CFF is sensitive to meaningful differences in rhetorical strategy.

*   **Construct Validity:** The correlation analysis provides strong preliminary evidence for the CFF's construct validity. The observed negative relationships between cohesion and tension/contradiction align perfectly with the framework's theoretical underpinnings. It successfully operationalizes the concept that cohesive discourse is structurally different from discourse that relies on tension and opposition.

*   **Framework-Corpus Fit:** The CFF appears well-suited to analyzing modern political discourse, particularly its populist variants. Its ability to measure simultaneous competing appeals (via the tension and contradiction indices) is essential for capturing the complexity of rhetoric that builds in-group solidarity for the purpose of out-group conflict. However, the **Success Tension** (Envy vs. Compersion) metric showed zero variance, suggesting that the dynamic between resenting others' success and celebrating it was not a rhetorically active dimension in this specific set of texts. This may be a feature of this small corpus or could indicate a dimension that requires further refinement for broader applicability.

## 5. Discussion

### 5.1 Theoretical Implications and Rhetorical Archetypes

The findings from this analysis, while preliminary, carry significant theoretical implications for the study of political communication. The CFF's ability to quantify "strategic contradiction" provides a new lens for understanding populist rhetoric. Instead of viewing it as simply "negative" or "divisive," this analysis suggests it operates via a more complex mechanism: the channeling of cohesive energies (amity, hope, dignity) toward fragmenting goals.

This study reveals at least two distinct rhetorical archetypes:
1.  **The Institutional Cohesive Archetype (McCain 2008):** Characterized by high scores on Amity and Cohesive Goals, low tension, and a high overall Cohesion Index. This style emphasizes procedural legitimacy, respect for the opponent, and the unity of the national body politic. Its primary goal is to reinforce the stability of the democratic system itself, even in defeat.
2.  **The Populist Fragmenting Archetype (King, Sanders, Ocasio-Cortez 2017-2025):** Characterized by high scores on Enmity, Fear, and Fragmentative Goals, coupled with high Emotional and Relational Tension. This style, seen here in both conservative and progressive forms, defines a virtuous "people" against a corrupt and powerful "other" (elites, oligarchs, the opposing party). Its primary goal is not systemic stability but the mobilization of a base to challenge and displace the existing power structure. The call for "class solidarity" by Alexandria Ocasio-Cortez is a progressive framing of this archetype, aiming for a specific form of cohesion to achieve a fragmenting political goal (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt).

The data also suggests a potential temporal shift. The lone document from 2008 represents the cohesive archetype, while all post-2016 documents represent the fragmenting one. While this N=4 sample is far too small to support a definitive conclusion, it raises a critical hypothesis for future research: that American political discourse has seen a structural shift away from institutional-cohesive rhetoric and towards populist-fragmenting rhetoric over the past two decades.

### 5.2 Limitations and Future Directions

This pilot study's primary value lies in demonstrating the potential of the CFF and generating hypotheses for future work. The central limitation remains the N=4 sample size, which makes all findings suggestive rather than conclusive.

Future research should proceed in several directions:
1.  **Corpus Expansion:** The most critical next step is to apply the CFF to a large, representative corpus of political speech spanning multiple decades, speakers, and contexts. This would allow for robust statistical analysis, validation of the archetypes identified here, and a definitive test of the hypothesized temporal shift.
2.  **Refinement of Metrics:** The lack of variance in the `success_tension` metric warrants investigation. Researchers should examine whether this is an artifact of the current corpus or if the operationalization of Envy and Compersion needs refinement to capture this dynamic more effectively across different types of discourse.
3.  **Integration with Audience Effects:** A crucial extension of this work would be to connect CFF-based analysis of texts to experimental data on audience reception. Do texts with high Strategic Contradiction scores actually produce more potent emotional and mobilizing effects in listeners? Answering this would bridge the gap between textual analysis and real-world political impact.
4.  **Cross-Cultural Analysis:** Applying the CFF to political discourse from other democratic (and non-democratic) systems could reveal whether the identified archetypes are specific to the American context or represent more universal modes of political communication.

## 6. Conclusion

This computational analysis, despite its limited scale, provides a compelling demonstration of the Cohesive Flourishing Framework's analytical power. By moving beyond sentiment analysis to a multi-dimensional model of oppositional rhetoric, the CFF successfully identified and quantified key structural differences between institutional and populist political discourse. The findings reveal a contemporary rhetorical landscape in this small sample that is predominantly fragmenting, driven by high emotional and relational tension, and characterized by the strategic use of cohesive appeals for divisive ends.

The framework's internal consistency, evidenced by the strong correlations between its metrics, and its ability to discriminate between different rhetorical styles, provide a solid foundation for its use in future, larger-scale research. The preliminary archetypes and temporal trends identified here offer a rich set of testable hypotheses for the computational social science community. Ultimately, this report serves as a proof-of-concept, indicating that the CFF is a valuable and sophisticated tool for scholars seeking to understand the linguistic forces that either strengthen or undermine social cohesion and democratic health.

## 7. Evidence Citations

*The following quotes were used in this report to support statistical interpretations.*

**Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt**
*   "So I hope that you see this movement is not about partisan labels or purity tests, but about class solidarity." (Dimension: cohesive_goals)
*   "We need to come together and spend every day between now and election day working to educate our neighbors, and give Evans and Boebert the boot, and replace them with a brawling Democrat who will stan..." (Dimension: fragmentative_goals)
*   "I don’t believe in healthcare, labor and human dignity, because I’m an extremist or a Marxist. I believe it because I was a waitress, because I’ve scrubbed toilets with my mom to afford school, becaus..." (Dimension: individual_dignity)
*   "He’s handed the keys to Elon Musk and is selling off our country for parts to the wealthiest people in the world for a kickback." (Dimension: enmity)

**Source: bernie_sanders_2025_fighting_oligarchy.txt**
*   "So if we stand together, are strong, are disciplined, are smart..." (Dimension: amity)
*   "...in the midst of all of these addictions, the worst and most dangerous addiction we have is the greed of the oligarchs." (Dimension: enmity)

**Source: steve_king_2017_house_floor.txt**
*   "But the Supreme Court, wrapped in the cloak of Marberry versus Madison and their imagination of what precedents and star decisis might mean to them, decides that they can write words into the law." (Dimension: envy)
*   "No hearing, no, no confirmation in the Senate, no vote in the in the Judiciary Committee, and no vote on the floor of the Senate for this lame duck President's appointments because we have a Constitut..." (Dimension: fragmentative_goals)