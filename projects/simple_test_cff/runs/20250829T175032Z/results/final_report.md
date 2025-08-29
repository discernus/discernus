# Cohesive Flourishing Framework Analysis Report

**Experiment**: simple_test  
**Framework**: cff_v10.md  
**Corpus**: corpus.md (4 documents)  

**Analysis Model**: Gemini 2.5 Flash
**Synthesis Model**: Gemini 2.5 Pro
**Method**: 3-Run Median Aggregation

---

## 1. Executive Summary

This report presents a preliminary computational analysis of four paradigmatic American political speeches using the Cohesive Flourishing Framework (CFF) v10. The study aimed to assess the framework's capacity to differentiate rhetorical styles and measure their potential impact on social cohesion. The analysis reveals a stark divergence between institutional and populist discourse. Institutional rhetoric, as exemplified by John McCain's 2008 concession speech, scored exceptionally high on the Full Cohesion Index (0.78), indicating a rhetorical style that reinforces democratic norms and social unity. In contrast, all three populist speeches—from Steve King, Bernie Sanders, and Alexandria Ocasio-Cortez—exhibited negative cohesion scores (mean = -0.51), suggesting a reliance on fragmentative rhetorical strategies.

The data identifies two distinct and opposing rhetorical clusters. A "Pro-Cohesion" cluster (Individual Dignity, Hope, Amity, Compersion, Cohesive Goals) was strongly associated with McCain's speech, while an "Anti-Cohesion" cluster (Tribal Dominance, Fear, Envy, Enmity, Fragmentative Goals) characterized the populist speeches. The analysis further demonstrates the CFF's ability to capture nuanced rhetorical strategies. For instance, Alexandria Ocasio-Cortez's speech registered the highest Strategic Contradiction Index (0.12), indicating a sophisticated blend of fragmentative "us-versus-them" framing with inclusive appeals to universal dignity. Similarly, Bernie Sanders's speech showed the highest Goal Tension (0.24), simultaneously calling for the destruction of an oligarchic system and the creation of a more just nation.

These preliminary findings, while based on a small sample (N=4), suggest that the CFF is a potent tool for moving beyond simple sentiment analysis to quantify the complex ways in which political language can either build or break down social cohesion. The clear statistical separation between institutional and populist styles, and the framework's ability to identify specific rhetorical tensions within those styles, underscores its potential for more extensive research into the health of democratic discourse.

## 2. Opening Framework: Key Insights

*   **Institutional vs. Populist Rhetoric Show Opposing Cohesion Profiles:** The analysis reveals a clear and significant divide. John McCain's institutional speech achieved a highly positive Full Cohesion Index (0.78), while the three populist speeches all scored negatively, ranging from -0.28 to -0.72. This suggests that rhetorical style is a primary determinant of a speech's cohesive or fragmentative potential.
*   **Data Reveals Two Mutually Exclusive Rhetorical 'Playbooks':** Correlation analysis identified two powerful, opposing clusters of rhetorical appeals. The "Anti-Cohesion" cluster (Tribal Dominance, Fear, Envy, Enmity, Fragmentative Goals) showed extremely high inter-correlation (e.g., Enmity and Tribal Dominance, *r* = .999). The "Pro-Cohesion" cluster (Individual Dignity, Hope, Amity, Compersion, Cohesive Goals) was similarly inter-correlated and stood in strong opposition to the first cluster. Speakers in this corpus drew almost exclusively from one playbook or the other.
*   **Populist Rhetoric is Characterized by Fragmentative Appeals:** Across the political spectrum, the populist speeches analyzed (King, Sanders, AOC) were characterized by high scores in Tribal Dominance, Envy, Enmity, and Fragmentative Goals. For example, Steve King's speech scored 0.8 in Tribal Dominance and 0.9 in Enmity, while Bernie Sanders's speech scored 0.9 in Envy and 0.9 in Enmity. This indicates a shared rhetorical strategy of identifying an in-group, defining an enemy, and framing success in zero-sum terms.
*   **The CFF's Tension Metrics Uncover Sophisticated Rhetorical Strategies:** The framework successfully identified nuanced rhetorical contradictions. Alexandria Ocasio-Cortez's speech had the highest Strategic Contradiction Index (0.12), driven by high Identity Tension (0.21). This reflects a complex strategy of combining strong Tribal Dominance ("The same billionaires are taking a wrecking ball to our country") with powerful appeals to Individual Dignity ("No matter who you voted for... you are welcome here").
*   **Success Orientation Appears Rhetorically Polarized:** The analysis found a perfect negative correlation (*r* = -1.00) between Compersion (joy in others' success) and Fragmentative Goals, and a near-perfect negative correlation (*r* = -0.99) between Compersion and Tribal Dominance. Furthermore, the Success Tension metric was 0.0 for all speakers, indicating that speakers employed either envy-based or compersion-based rhetoric, but never both in a way that created strategic tension. This suggests that how a speaker frames the success of others is a fundamental and non-negotiable element of their rhetorical strategy.

## 4. Methodology

### Framework Description
This analysis employed the Cohesive Flourishing Framework (CFF) v10, a multi-dimensional tool designed to evaluate the impact of discourse on social cohesion and democratic health. The CFF moves beyond traditional sentiment analysis by independently scoring ten conceptual anchors organized into five opposing pairs: Identity (Tribal Dominance vs. Individual Dignity), Emotional Climate (Fear vs. Hope), Success Orientation (Envy vs. Compersion), Relational Climate (Enmity vs. Amity), and Goal Orientation (Fragmentative vs. Cohesive Goals).

A key innovation of the CFF is its dual-track analysis of both *intensity* (a dimension's raw 0.0-1.0 score) and *salience* (its rhetorical prominence, also 0.0-1.0). This allows for the calculation of advanced metrics, including **Tension Indices** (measuring strategic contradictions between opposing pairs) and a **Strategic Contradiction Index** (the average of all tensions). The primary outcome measure is the **Full Cohesion Index**, a salience-weighted composite score ranging from -1.0 (maximally fragmentative) to +1.0 (maximally cohesive).

### Corpus Description
The analysis was conducted on the Democratic Discourse Corpus, a collection of four paradigmatic examples of American political communication. The corpus was selected to represent different rhetorical styles (institutional and populist) and political ideologies (conservative and progressive) across a 17-year span. The documents are:
1.  **John McCain 2008 Concession Speech** (Style: Institutional)
2.  **Steve King 2017 House Floor Speech** (Style: Populist Conservative)
3.  **Bernie Sanders 2025 Speech on Oligarchy** (Style: Populist Progressive)
4.  **Alexandria Ocasio-Cortez 2025 Speech on Oligarchy** (Style: Populist Progressive)

### Statistical Methods and Limitations
The analysis relied on descriptive statistics and Pearson correlation coefficients to identify patterns within the data. Given the preliminary nature of this study and the small sample size (N=4), no inferential statistical tests (e.g., t-tests, ANOVA) were performed, and findings should be interpreted as indicative rather than conclusive. All claims are based on the patterns observed within this specific corpus. Numerical results are reported to two decimal places for clarity and consistency, following APA guidelines. The primary goal was to assess the CFF's descriptive and discriminatory power and to generate hypotheses for future, larger-scale research.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics and Baseline Scores

The analysis of the four speeches reveals wide variance across all CFF dimensions, indicating the framework's ability to discriminate between different rhetorical approaches. The institutional speech by John McCain serves as a baseline for high-cohesion rhetoric, while the three populist speeches collectively establish a pattern for low-cohesion rhetoric.

John McCain's 2008 concession speech is characterized by extremely high scores on pro-cohesion dimensions: Individual Dignity (M = 0.90), Hope (M = 0.90), Amity (M = 0.90), and Cohesive Goals (M = 0.90). His scores on fragmentative dimensions were correspondingly low or absent, such as Envy (M = 0.00) and Enmity (M = 0.00). This profile resulted in a Full Cohesion Index of **0.78**, the highest in the corpus.

Conversely, the populist speeches scored highly on fragmentative dimensions. Steve King's speech registered the most extreme fragmentative profile, with high scores in Fear (M = 0.90), Enmity (M = 0.90), and Fragmentative Goals (M = 0.90), leading to the lowest Full Cohesion Index of **-0.72**. The progressive populist speeches from Bernie Sanders and Alexandria Ocasio-Cortez also showed negative cohesion, with scores of **-0.53** and **-0.28**, respectively. Both were marked by high Envy (M = 0.90 for both) and Enmity (M = 0.90 for Sanders, M = 1.00 for AOC).

### 5.2 Advanced Metric Analysis: Cohesion and Contradiction

The derived metrics provide a deeper understanding of the rhetorical strategies at play. The **Full Cohesion Index** clearly separates the institutional style from the populist styles.

| Speaker                    | Style                  | Full Cohesion Index | Strategic Contradiction Index |
| -------------------------- | ---------------------- | ------------------- | ----------------------------- |
| John McCain                | Institutional          | 0.78                | 0.06                          |
| Steve King                 | Populist Conservative  | -0.72               | 0.06                          |
| Bernie Sanders             | Populist Progressive   | -0.53               | 0.09                          |
| Alexandria Ocasio-Cortez   | Populist Progressive   | -0.28               | 0.12                          |

The **Strategic Contradiction Index** reveals the rhetorical complexity of each speech. While McCain and King presented highly consistent (low contradiction) messages, the progressive populist speakers employed more mixed messaging. Alexandria Ocasio-Cortez's speech registered the highest contradiction score (0.12), primarily driven by high **Identity Tension** (0.21) and **Relational Tension** (0.16). This indicates a sophisticated strategy that simultaneously leverages strong in-group/out-group rhetoric while also making broad, inclusive appeals. As she stated, "The same billionaires are taking a wrecking ball to our country and they derive their power from dividing working people apart," (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt), a clear example of Tribal Dominance. Yet, in the same speech, she offered a powerful appeal to Individual Dignity: "No matter who you voted for... No matter your race, religion, gender identity, or status... If you are willing to fight for someone you don't know, you are welcome here." (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt). This simultaneous use of opposing identity frames is precisely what the tension metric is designed to detect.

Similarly, Bernie Sanders's speech exhibited the highest **Goal Tension** (0.24), reflecting a message that combines calls for destruction with calls for creation. He articulated strong Fragmentative Goals, claiming the opposition is "prepared to destroy Social Security, Medicaid, Medicare" (Source: bernie_sanders_2025_fighting_oligarchy.txt), while also offering a vision of Cohesive Goals, stating that "if we stand together... we can create the kind of nation that we deserve." (Source: bernie_sanders_2025_fighting_oligarchy.txt).

### 5.3 Correlation and Interaction Analysis: Rhetorical Clusters

The correlation matrix reveals two powerful and mutually exclusive rhetorical clusters, suggesting that speakers in this corpus adopted one of two distinct "playbooks."

**The "Anti-Cohesion" Cluster:** The dimensions of Tribal Dominance, Fear, Envy, Enmity, and Fragmentative Goals are all strongly and positively inter-correlated.
*   `enmity_raw` & `tribal_dominance_raw`: *r* = .999
*   `fear_raw` & `tribal_dominance_raw`: *r* = .92
*   `fragmentative_goals_raw` & `enmity_raw`: *r* = .99
*   `envy_raw` & `tribal_dominance_raw`: *r* = .87

This cluster defines the rhetorical core of the populist speeches. For example, Steve King's speech combined high-salience Fear ("it's costing lives in America. And it's costing, it's costing in the end thousands of lives in America") with high-salience Tribal Dominance ("It's another life loss to an, an illegal criminal alien who was unlawfully present in America") (Source: steve_king_2017_house_floor.txt). Likewise, Bernie Sanders combined high-salience Envy ("there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about") with high-salience Enmity ("We will not accept an oligarchic form of society.") (Source: bernie_sanders_2025_fighting_oligarchy.txt).

**The "Pro-Cohesion" Cluster:** The dimensions of Individual Dignity, Hope, Compersion, Amity, and Cohesive Goals are also strongly and positively inter-correlated.
*   `individual_dignity_raw` & `amity_raw`: *r* = .995
*   `hope_raw` & `cohesive_goals_raw`: *r* = .96
*   `compersion_raw` & `full_cohesion_index`: *r* = .96

This cluster was the hallmark of John McCain's institutional speech. His rhetoric seamlessly blended appeals to Individual Dignity ("the election of an African-American to the presidency of the United States"), Amity ("We are fellow Americans"), Hope ("believe always in the promise and greatness of America"), and Cohesive Goals ("to find ways to come together, to find the necessary compromises to bridge our differences") (Source: john_mccain_2008_concession.txt). The strong positive correlation of these dimensions with the Full Cohesion Index validates the theoretical foundation of the CFF.

### 5.4 Pattern Recognition and Theoretical Insights

The stark opposition between the two rhetorical clusters is the most significant pattern in the data. The Full Cohesion Index was strongly and negatively correlated with every dimension in the "Anti-Cohesion" cluster (e.g., *r* = -.96 with Fragmentative Goals) and strongly and positively correlated with every dimension in the "Pro-Cohesion" cluster (e.g., *r* = .96 with Compersion). This provides strong preliminary evidence for the CFF's construct validity; the dimensions group together and predict overall cohesion as theoretically expected.

A particularly revealing finding is the perfect negative correlation (*r* = -1.00) between Compersion (celebrating others' success) and Fragmentative Goals. This suggests that a rhetorical posture of celebrating others' merit is fundamentally incompatible with a strategy aimed at social division. McCain's speech exemplifies this, scoring high on Compersion (0.80) by admiring his opponent's achievement—"His success alone commands my respect... something I deeply admire and commend him for achieving" (Source: john_mccain_2008_concession.txt)—while scoring zero on Fragmentative Goals. Conversely, the populist speakers, who all scored high on Fragmentative Goals, scored zero on Compersion. Instead, they relied on Envy, as when Alexandria Ocasio-Cortez accused billionaires of theft: "They're stealing them. They're stealing them. They're stealing them from you and you and me." (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt).

### 5.5 Framework Effectiveness Assessment

Based on this preliminary analysis, the CFF demonstrates high discriminatory power. It successfully distinguished between institutional and populist rhetorical styles, assigning them to opposite ends of the cohesion spectrum. The framework-corpus fit appears strong, as the variance in the results was high, and the dimensional patterns aligned with the theoretical constructs of the framework.

The framework's most significant contribution appears to be its ability to move beyond a simple "good vs. bad" dichotomy. The tension metrics provided a quantitative measure of rhetorical sophistication. McCain's speech, for example, had the highest **Emotional Tension** (0.24) because he paired a high-salience message of Hope (0.90) with a lower-salience acknowledgment of Fear (0.40), stating, "These are difficult times for our country" (Source: john_mccain_2008_concession.txt). This demonstrates a nuanced approach that validates audience concerns while directing them toward an optimistic vision. This is a level of strategic insight that a simple valence-based sentiment score could not provide.

## 6. Discussion

The findings from this pilot study, while limited by the small sample size, offer compelling insights into the rhetorical structures that may underpin social cohesion and fragmentation. The stark division between the institutional rhetoric of John McCain and the populist rhetoric of King, Sanders, and AOC suggests that rhetorical *style* may be as important as policy *content* in shaping democratic discourse. McCain's speech, rooted in the "Pro-Cohesion" cluster, aimed to reinforce the legitimacy of the democratic process and foster national unity, even in defeat. The populist speeches, drawing from the "Anti-Cohesion" cluster, aimed to mobilize a specific in-group against a perceived out-group enemy, a strategy that, according to the CFF, is inherently fragmentative.

This analysis also highlights that "populism" is not a monolith. While both conservative and progressive populism in this sample relied on fragmentative appeals, the CFF's tension metrics revealed different strategic flavors. The progressive populism of Sanders and Ocasio-Cortez was more rhetorically complex, blending fragmentative tactics with cohesive appeals to unity and dignity, resulting in higher contradiction scores. This may represent a strategy to mobilize a base with "us-vs-them" anger while simultaneously appealing to a broader audience with inclusive, hopeful language. Future research could investigate whether this "contradictory populism" is more or less effective than the more rhetorically consistent style of a speaker like Steve King.

The mutual exclusivity of the Compersion/Envy axis is a particularly noteworthy finding. It suggests that the framing of economic and social success is a fundamental, almost binary, choice in political rhetoric. A speaker either celebrates the success of others (even opponents) as a sign of a healthy system or frames it as evidence of a rigged system. This choice appears to be a powerful indicator of their overall rhetorical posture toward social cohesion.

The primary limitation of this study is its N=4 sample size, which prevents generalization. The findings should be considered a proof-of-concept for the CFF methodology and a source of hypotheses for future work. A larger, more diverse corpus would be needed to confirm these patterns and explore their relationship with factors like political context, speaker identity, and audience reception.

## 7. Conclusion

This computational analysis successfully demonstrated the utility of the Cohesive Flourishing Framework v10 for dissecting political rhetoric. The framework effectively quantified a profound difference between an institutional style that promotes social cohesion and a populist style that promotes social fragmentation. By identifying two opposing rhetorical clusters—one built on dignity, hope, and amity, the other on tribalism, fear, and enmity—this study provides a clear, data-driven model for understanding how language can be used to unite or divide.

The CFF's novel metrics for tension and contradiction proved capable of revealing sophisticated strategies that would be missed by simpler analytical tools. The preliminary evidence suggests that the CFF offers a robust and nuanced methodology for researchers, policymakers, and civic leaders seeking to understand and improve the health of our democratic discourse. Future research should apply this framework to larger corpora to validate these initial findings and further explore the complex dynamics of political communication.

## 8. Evidence Citations

**Source: john_mccain_2008_concession.txt**
*   On Cohesive Goals: "to find ways to come together, to find the necessary compromises to bridge our differences and help restore our prosperity, defend our security in a dangerous world, and leave our children and grandchildren a stronger, better country than we inherited."
*   On Hope: "believe always in the promise and greatness of America."
*   On Compersion: "His success alone commands my respect for his ability and perseverance. But that he managed to do so by inspiring the hopes of so many millions of Americans who had once wrongly believed that they had little at stake or little influence in the election of an American president is something I deeply admire and commend him for achieving."
*   On Amity: "We are fellow Americans, and please believe me when I say no association has ever meant more to me than that."
*   On Individual Dignity: "There is no better evidence of this than the election of an African-American to the presidency of the United States."
*   On Fear: "These are difficult times for our country, and I pledge to him tonight to do all in my power to help him lead us through the many challenges we face."

**Source: steve_king_2017_house_floor.txt**
*   On Tribal Dominance: "It's another life loss to an, an illegal criminal alien who was unlawfully present in America, who had no business to be here..."
*   On Fear: "it's costing lives in America. And it's costing, it's costing in the end thousands of lives in America."
*   On Enmity: 'lame duck President," "criminal alien," "perpetrator," "Supreme Court created a new command," "defies the very law,"'

**Source: bernie_sanders_2025_fighting_oligarchy.txt**
*   On Envy: "Meanwhile, there has been a $75 trillion transfer of wealth from the bottom 90% to the top 1%. That is what a rigged economy is about, and that is what we are going to change."
*   On Enmity: "We will not accept an oligarchic form of society. We will not accept the richest guy in the world running all over Washington... Trump has a government of the billionaires, by the billionaires, and for the billionaires."
*   On Fragmentative Goals: "They are prepared to destroy Social Security, Medicaid, Medicare, the Veterans Administration in order to make themselves even richer."
*   On Cohesive Goals: "if we stand together, are strong, are disciplined, are smart, I have every reason to believe deeply in my heart that not only will we defeat Trumpism, but we can create the kind of nation that we deserve."

**Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt**
*   On Tribal Dominance: "The same billionaires are taking a wrecking ball to our country and they derive their power from dividing working people apart."
*   On Individual Dignity: "No matter who you voted for in the past. No matter if you know all the right words to say, no matter your race, religion, gender identity, or status, no matter if you disagree with me on a couple of things. If you are willing to fight for someone you don't know, you are welcome here."
*   On Envy: "They're stealing them. They're stealing them. They're stealing them from you and you and me."
*   On Fragmentative Goals: "give Evans and Boebert the boot"