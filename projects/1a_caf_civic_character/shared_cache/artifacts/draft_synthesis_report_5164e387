# Civic Analysis Framework (CAF) Analysis Report

**Experiment**: caf_civic_character_pattern_analysis  
**Framework**: framework.md  
**Corpus**: corpus.md (8 documents)  

---

## 1. Executive Summary

This report presents a computational analysis of eight political speeches using the Civic Analysis Framework (CAF) v10.0. The CAF evaluates political discourse based on ten dimensions organized into five oppositional axes: Dignity vs. Tribalism, Truth vs. Manipulation, Justice vs. Resentment, Hope vs. Fear, and Pragmatism vs. Fantasy. The analysis aimed to identify distinct rhetorical patterns and assess the framework's utility in characterizing political communication.

The findings reveal a clear polarization of civic character within the corpus. The analysis successfully identified two distinct archetypes: "Authentic Virtue" and "Strategic Pathology." Speakers such as John McCain and Mitt Romney exemplify the former, with discourse characterized by high scores in virtues like Dignity and Justice and a high, positive Salience-Weighted Civic Character Index (CCI) (e.g., McCain, CCI = 0.757). Conversely, speakers like JD Vance and Steve King represent the latter, with discourse dominated by salient vices like Tribalism and Resentment, resulting in strongly negative CCI scores (e.g., Vance, CCI = -0.496).

The framework's most significant contribution is its ability to quantify and interpret complex, contradictory rhetoric. Speakers like Alexandria Ocasio-Cortez and Bernie Sanders exhibit high "Character Tension," simultaneously appealing to virtues like Justice and vices like Resentment. While Ocasio-Cortez's profile balances these tensions to achieve a near-neutral CCI (0.018), Sanders's emphasis on vices results in a negative CCI (-0.314), demonstrating how salience-weighting provides a more nuanced assessment than raw scores alone. The analysis also identified a key methodological limitation in the framework's Tension Index, which may underrepresent contradiction when opposing dimensions are given equal rhetorical emphasis. These preliminary findings, based on a small corpus, suggest the CAF is a promising tool for dissecting the moral and strategic complexity of political language.

## 2. Opening Framework: Key Insights

- **Clear Rhetorical Archetypes Identified:** The analysis successfully distinguished between two primary rhetorical patterns. "Authentic Virtue" is characterized by high positive CCI scores and a dominance of virtues, as seen in John McCain (CCI = 0.757) and Mitt Romney (CCI = 0.556). "Strategic Pathology" is marked by high negative CCI scores and a salience of vices, exemplified by JD Vance (CCI = -0.496) and Steve King (CCI = -0.348).

- **Populist Rhetoric Exhibits High "Character Tension":** Speakers like Alexandria Ocasio-Cortez and Bernie Sanders display significant tension between competing values. Both score high on Tribalism and Resentment while also appealing to Dignity and Justice. Ocasio-Cortez, for instance, has high raw scores for both Dignity (0.80) and Tribalism (0.80), and her speech registers a high Justice Tension score (0.24), indicating a strategic blend of unifying and divisive appeals.

- **Salience-Weighting Reveals Deeper Rhetorical Strategy:** The Salience-Weighted Civic Character Index (CCI) effectively differentiates between speakers with similar raw score patterns. Alexandria Ocasio-Cortez (CCI = 0.018) and Bernie Sanders (CCI = -0.314) both employ high-tension rhetoric. However, the CCI reveals that the greater salience of vices in Sanders's speech results in a more negative overall civic character assessment, highlighting the importance of rhetorical emphasis.

- **Absence of Specific Vices Marks Virtuous Discourse:** Speakers classified as "Authentic Virtue" consistently scored at or near zero on the dimensions of Manipulation and Fantasy. John McCain, for example, registered a 0.00 for both Manipulation and Fantasy raw scores. This suggests that the avoidance of deceptive or reality-detached rhetoric is a key indicator of a discourse oriented toward civic virtue.

- **Framework Reveals Nuance in Civil Rights Rhetoric:** The analysis of John Lewis's 1963 speech shows high raw scores for both Justice (0.90) and its opposing vice, Resentment (0.90). This reflects a demand for justice born from deep-seated grievance. As Lewis stated, "We are tired! We are tired of being beaten by policemen. We are tired of seeing our people locked up in jails over and over again" (Source: john_lewis_1963_march_on_washington_ab348df3.txt).

- **Methodological Limitation Identified in Tension Metric:** The John Lewis case also exposed a limitation in the Tension Index formula (`min(Virtue_Score, Vice_Score) * abs(Virtue_Salience - Vice_Salience)`). Because the salience for Justice (0.90) and Resentment (0.90) was identical, the calculated Justice Tension was 0.00. This indicates the metric may fail to capture potent contradictions when a speaker gives equal weight to opposing values, a crucial area for future refinement.

## 4. Methodology

### Framework Description
This analysis utilizes the Civic Analysis Framework (CAF) v10.0, a systematic methodology for evaluating the civic character of political discourse. The framework is grounded in Aristotelian virtue ethics and contemporary civic republican theory. It operationalizes this by measuring discourse along five core axes, each representing a tension between a civic virtue and its corresponding vice:

- **Identity Axis:** Dignity vs. Tribalism
- **Truth Axis:** Truth vs. Manipulation
- **Justice Axis:** Justice vs. Resentment
- **Emotional Axis:** Hope vs. Fear
- **Reality Axis:** Pragmatism vs. Fantasy

For each of the ten dimensions, the framework produces a raw intensity score (0.0 to 1.0) and a salience score (0.0 to 1.0), indicating the dimension's rhetorical prominence.

### Derived Metrics
The CAF's primary innovation lies in its derived metrics, which were calculated for this analysis:

- **Character Tension Index:** Calculated for each axis, this metric quantifies strategic contradiction. The formula, `min(Virtue_Score, Vice_Score) * abs(Virtue_Salience - Vice_Salience)`, captures instances where a speaker appeals to both a virtue and its opposing vice, particularly when their rhetorical emphasis (salience) differs.
- **Salience-Weighted Civic Character Index (CCI):** This is the primary summary metric, providing a single, normalized score from -1.0 (pathological) to +1.0 (virtuous). It is calculated as `(Weighted_Virtue_Sum - Weighted_Vice_Sum) / Total_Salience`. This index provides a holistic assessment of a text's overall civic character, weighted by the prominence of each expressed virtue and vice.

### Corpus and Data
The analysis was performed on the CAF Civic Character Political Speeches Corpus, comprising eight documents from a date range of 1963-2025. The dataset for each document included raw and salience scores for the ten CAF dimensions, from which the derived metrics were computed. Speaker identities were parsed from document filenames.

### Statistical Methods and Limitations
The analysis is primarily descriptive and exploratory. The core statistical method involved calculating the mean scores for all dimensions and derived metrics for each speaker to generate a "character signature." These signatures were then compared to identify patterns, clusters, and archetypes. Rhetorical patterns were classified based on predefined thresholds for average virtue/vice scores and salience, as specified in the analytical code.

The primary limitation of this study is its small sample size (N=8). Consequently, the findings should be considered preliminary and indicative rather than generalizable. The analysis does not employ inferential statistics, and all conclusions are drawn directly from the descriptive patterns observed in the provided data. The goal is to demonstrate the framework's analytical potential and generate hypotheses for future, larger-scale research.

## 5. Comprehensive Results

### 5.1 Speaker Character Signatures

The analysis produced a distinct "character signature" for each of the eight speakers, summarizing their average rhetorical profile across all CAF dimensions. The Salience-Weighted Civic Character Index (CCI) provides a top-level measure of each speaker's discourse. The results show a wide distribution of civic character, from highly virtuous to highly pathological.

**Table 1: Speaker Character Signatures and Civic Character Index (CCI)**

| Speaker                 | Dignity (Raw) | Tribalism (Raw) | Justice (Raw) | Resentment (Raw) | Hope (Raw) | Fear (Raw) | CCI (Salience-Weighted) | Rhetorical Pattern      |
|-------------------------|:-------------:|:---------------:|:-------------:|:----------------:|:----------:|:----------:|:-----------------------:|-------------------------|
| John McCain             | 0.90          | 0.05            | 0.80          | 0.00             | 0.60       | 0.10       | **0.757**               | Authentic Virtue        |
| Mitt Romney             | 0.80          | 0.10            | 0.90          | 0.20             | 0.40       | 0.20       | **0.556**               | Authentic Virtue        |
| Cory Booker             | 0.90          | 0.10            | 0.90          | 0.70             | 0.80       | 0.30       | **0.527**               | Authentic Virtue        |
| John Lewis              | 0.80          | 0.20            | 0.90          | 0.90             | 0.60       | 0.70       | **0.263**               | Authentic Virtue        |
| Alexandria Ocasio-Cortez| 0.80          | 0.80            | 0.60          | 0.90             | 0.80       | 0.70       | **0.018**               | Authentic Virtue        |
| Bernie Sanders          | 0.40          | 0.80            | 0.60          | 0.90             | 0.70       | 0.70       | **-0.314**              | Balanced/Mixed          |
| Steve King              | 0.10          | 0.80            | 0.50          | 0.90             | 0.00       | 0.90       | **-0.348**              | Strategic Pathology     |
| JD Vance                | 0.10          | 0.80            | 0.10          | 0.90             | 0.40       | 0.60       | **-0.496**              | Strategic Pathology     |

*Note: Raw scores are on a 0.0-1.0 scale. CCI is on a -1.0 to +1.0 scale. Rhetorical Pattern is from the `classify_rhetorical_patterns` function.*

The data reveals a clear divide. McCain, Romney, and Booker form a cluster of high-virtue speakers. Vance and King form an opposing cluster characterized by vice-dominant rhetoric. Lewis, Ocasio-Cortez, and Sanders occupy a more complex middle ground, which is explored below.

### 5.2 Advanced Metric Analysis: Tension and Contradiction

The framework's derived metrics reveal strategic complexities not apparent from raw scores alone. The Character Tension Index is particularly insightful for understanding mixed-motive rhetoric.

**High-Tension Populist Rhetoric:**
The analysis identifies Bernie Sanders and Alexandria Ocasio-Cortez as speakers who employ high-tension rhetoric. Both exhibit high scores on the Justice Tension and Dignity/Tribalism Tension axes.

- **Bernie Sanders** registered a Justice Tension of 0.24 and a Dignity Tension of 0.24. This quantifies a strategy of simultaneously appealing to unifying principles while employing divisive, tribal language. For example, his rhetoric targets a specific out-group ("billionaires") as the source of societal problems, a classic high-Resentment and high-Tribalism strategy. As Sanders stated, "Abraham Lincoln talked about a government of the people, by the people, for the people. Well, Trump has a government of the billionaires, by the billionaires, and for the billionaires" (Source: bernie_sanders_2025_fighting_oligarchy_261b893a.txt). This statement frames the political conflict in stark, oppositional terms.

- **Alexandria Ocasio-Cortez** also shows a high Justice Tension score of 0.24. Her discourse combines appeals to universal dignity with strong tribal identification. She makes inclusive calls, stating, "If you are willing to fight for someone you don’t know, you are welcome here" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy_1121e4ae.txt), which scores high on Dignity. Yet, this is combined with language that defines a clear political in-group and out-group, for instance, calling to "replace them with a brawling Democrat," a statement indicative of Tribalism.

This high-tension pattern, where appeals to both virtue and vice are prominent, appears to be a signature of the populist style represented in this corpus.

### 5.3 Pattern Recognition: Rhetorical Archetypes

The statistical patterns clearly delineate three rhetorical archetypes within the corpus.

**Archetype 1: Authentic Virtue**
This pattern is defined by a high positive CCI, high scores on multiple virtue dimensions, and correspondingly low scores on vice dimensions. John McCain's 2008 concession speech is the exemplar in this dataset (CCI = 0.757). His profile is dominated by Dignity (M=0.90), Truth (M=0.80), Justice (M=0.80), and Pragmatism (M=0.90), with negligible scores for vices. His rhetoric emphasizes unity and shared identity over division. As McCain stated, "Whatever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that" (Source: john_mccain_2008_concession_ff9b26f2.txt). Mitt Romney's speech on impeachment shows a similar pattern (CCI = 0.556), emphasizing an appeal to impartial justice and truth. He framed his decision as an obligation to a higher principle, stating, "As a senator-juror, I swore an oath before God to exercise impartial justice. I am profoundly religious. My faith is at the heart of who I am" (Source: mitt_romney_2020_impeachment_9ebec73f.txt).

**Archetype 2: Strategic Pathology**
This pattern is the inverse of Authentic Virtue, characterized by a strongly negative CCI and the salient use of vices. JD Vance (CCI = -0.496) and Steve King (CCI = -0.348) exemplify this archetype. Their discourse is high in Tribalism (M=0.80 for both), Resentment (M=0.90 for both), and Fear (M=0.60 for Vance, M=0.90 for King). Vance's speech constructs a narrative of threat from an out-group, a hallmark of high-Fear, high-Tribalism rhetoric. He claims, "The real threat to American democracy is that American voters keep on voting for less immigration and our politicians keep on rewarding us with more" (Source: jd_vance_2022_natcon_conference_516a3c9c.txt). Similarly, Steve King's speech uses fear-based appeals by linking immigrants to violent crime, stating that because of release policies, there are "135 dead Americans that would be alive today" (Source: steve_king_2017_house_floor_738780d9.txt). This archetype relies on division, grievance, and threat to mobilize support.

**Archetype 3: High-Tension/Contradictory**
This archetype, discussed in section 5.2, is the most complex. It is not defined by a simple dominance of virtue or vice, but by the simultaneous, salient expression of both. The speeches by Ocasio-Cortez, Sanders, and Lewis fall into this category. John Lewis's 1963 speech is a historically significant example. It scores high on Justice (M=0.90) in its demand for civil rights, but also equally high on Resentment (M=0.90), reflecting the deep anger over systemic oppression. This is evident when he says, "By and large, American politics is dominated by politicians who build their careers on immoral compromises and ally themselves with open forms of political, economic, and social exploitation" (Source: john_lewis_1963_march_on_washington_ab348df3.txt). The framework captures this righteous anger as a combination of a just cause fueled by resentment of injustice.

### 5.5 Framework Effectiveness Assessment

The CAF framework demonstrated considerable effectiveness in differentiating between speakers and identifying nuanced rhetorical strategies. Its multi-dimensional approach, combined with salience-weighting, provides a richer picture than a simple one-dimensional positive/negative scale. The CCI proved to be a robust summary metric for overall civic character.

However, the analysis also revealed a key area for methodological improvement. The case of John Lewis, with identical high raw scores (0.90) and high salience scores (0.90) for both Justice and Resentment, resulted in a calculated Justice Tension of 0.00. This is because the `abs(Virtue_Salience - Vice_Salience)` term became zero. This finding suggests that the current Tension Index formula is effective at identifying *strategic* contradiction where one value is emphasized over its de-emphasized counterpart, but it may fail to capture instances of *direct* contradiction where a speaker gives equal weight to opposing moral claims. This is a critical insight for future iterations of the framework.

Furthermore, a planned analysis of the discriminatory power of each dimension (`analyze_speaker_differentiation`) could not be completed due to a technical error in the execution. Qualitatively, however, the dimensions of Tribalism, Resentment, Dignity, and Justice appear to be the most powerful differentiators in this corpus, as they show the greatest variance across the identified archetypes.

## 6. Discussion

The results of this analysis carry several implications for the study of political communication. The clear identification of "Authentic Virtue" and "Strategic Pathology" archetypes provides a data-driven confirmation of rhetorical patterns commonly discussed in political science. The CAF offers a systematic, replicable method for classifying discourse that moves beyond subjective interpretation.

The most significant contribution of this analysis, however, is the nuanced portrait of high-tension rhetoric. The framework allows for a move beyond labeling speakers like Ocasio-Cortez or Sanders as simply "populist." Instead, it deconstructs their strategy, quantifying the precise blend of virtuous appeals (to justice, dignity) and pathological tactics (appeals to tribalism, resentment) they employ. The CCI then provides a summative judgment on the overall character of that blend. The difference between Ocasio-Cortez's near-neutral CCI and Sanders's negative CCI is instructive. It suggests that while both use a similar rhetorical toolkit, the specific weighting and emphasis of virtues versus vices can lead to substantially different overall effects on civic discourse. This finding suggests that future research could investigate the specific conditions under which audiences respond to these mixed moral appeals.

The methodological limitation identified in the Tension Index is also a valuable finding. It highlights the challenge of formally modeling complex human concepts like moral contradiction. A speaker who passionately advocates for justice while simultaneously expressing deep resentment for the perpetrators of injustice is not necessarily being strategically incoherent; they may be expressing a deeply coherent emotional and moral position. Future research could explore alternative formulations for the Tension Index, perhaps one that considers the absolute magnitude of co-occurring oppositional scores, regardless of salience differences, to better capture this type of direct, passionate contradiction.

Given the small sample size, these findings are preliminary. A crucial next step would be to apply the CAF to a much larger and more diverse corpus of political texts. This would allow for more robust statistical analysis, including testing the hypotheses generated here: for instance, that populist rhetoric is consistently characterized by high scores on the Tension Indices, or that the absence of Manipulation and Fantasy is a reliable marker of institutional, virtue-oriented discourse.

## 7. Conclusion

This computational analysis of eight political speeches using the Civic Analysis Framework (CAF) v10.0 successfully demonstrated the framework's capacity to produce nuanced and insightful evaluations of political discourse. The study identified distinct rhetorical archetypes—Authentic Virtue, Strategic Pathology, and High-Tension—and quantified their characteristics using the framework's novel derived metrics, particularly the Salience-Weighted Civic Character Index (CCI) and the Character Tension Indices.

The findings indicate that the CAF is not merely a tool for classifying speech as "good" or "bad," but a sophisticated instrument for dissecting the complex moral and strategic architecture of political language. It effectively revealed how speakers can simultaneously leverage appeals to both unifying virtues and divisive vices, a hallmark of contemporary populist communication. While highlighting the framework's strengths, the analysis also uncovered a key limitation in its measurement of tension, providing a clear direction for future methodological refinement. As a preliminary, exploratory study, this report validates the potential of the CAF as a powerful tool for computational social science and sets a clear agenda for future research into the character of civic discourse.

## 8. Evidence Citations

**alexandria_ocasio_cortez_2025_fighting_oligarchy_1121e4ae.txt**
- "If you are willing to fight for someone you don’t know, you are welcome here."
- "We need to come together and spend every day between now and election day working to educate our neighbors, and give Evans and Boebert the boot, and replace them with a brawling Democrat who will stand for Colorado."

**bernie_sanders_2025_fighting_oligarchy_261b893a.txt**
- "Abraham Lincoln talked about a government of the people, by the people, for the people. Well, Trump has a government of the billionaires, by the billionaires, and for the billionaires."

**cory_booker_2018_first_step_act_0c32812a.txt**
- "We were all caught in an inescapable network of mutuality, tied in a common garment. We cannot suffer the illusion of separation when we think this criminal justice system that is so punishing some is not hurting this country as a whole."

**jd_vance_2022_natcon_conference_516a3c9c.txt**
- "The real threat to American democracy is that American voters keep on voting for less immigration and our politicians keep on rewarding us with more."
- "The real threat to American democracy is that American voters keep on voting for less immigration and our politicians keep on rewarding us with more. That is the threat to American democracy."

**john_lewis_1963_march_on_washington_ab348df3.txt**
- "We are tired! We are tired of being beaten by policemen. We are tired of seeing our people locked up in jails over and over again."
- "By and large, American politics is dominated by politicians who build their careers on immoral compromises and ally themselves with open forms of political, economic, and social exploitation."

**john_mccain_2008_concession_ff9b26f2.txt**
- "Whatever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that."

**mitt_romney_2020_impeachment_9ebec73f.txt**
- "As a senator-juror, I swore an oath before God to exercise impartial justice. I am profoundly religious. My faith is at the heart of who I am. I take an oath before God as enormously consequential."

**steve_king_2017_house_floor_738780d9.txt**
- "And of those that they released, there have been at least 124 of them who have been charged with homicide for 135 murders. That's 135 dead Americans that would be alive today if the President didn't have the policy of releasing criminal, criminal aliens onto the streets."