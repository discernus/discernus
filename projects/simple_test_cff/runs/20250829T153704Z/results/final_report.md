# Cohesive Flourishing Framework Analysis Report

**Experiment**: simple_test
**Run ID**: N/A (Composite analysis from raw data)
**Date**: 2025-08-29
**Framework**: cff_v10.md
**Corpus**: corpus.md (4 documents)

**Analysis Model**: Gemini 2.5 Flash
**Synthesis Model**: Gemini 2.5 Pro

---

## 1. Executive Summary

This report presents a preliminary computational analysis of four paradigmatic American political speeches using the Cohesive Flourishing Framework (CFF) v10. The study aimed to measure the discourse's impact on social cohesion by analyzing rhetorical patterns across institutional and populist styles. The corpus included John McCain's 2008 concession speech (institutional), a 2017 House floor speech by Steve King (conservative populist), and 2025 policy statements from Bernie Sanders and Alexandria Ocasio-Cortez (progressive populist). Due to the pilot nature of this study (N=4), all findings should be considered indicative and exploratory, intended to generate hypotheses for future large-scale research.

The analysis reveals a stark divergence in the rhetorical construction of cohesion between institutional and populist discourse. John McCain's speech registered a strongly positive Full Cohesion Index of +0.773, characterized by high-salience appeals to `Amity`, `Hope`, and `Individual Dignity`. In sharp contrast, all three populist speeches produced negative cohesion scores, indicating fragmentative rhetoric. Steve King's speech was the most fragmentative (Full Cohesion Index: -0.823), driven by intense and salient appeals to `Tribal Dominance`, `Fear`, and `Enmity`. The progressive populist speeches from Sanders and Ocasio-Cortez were also fragmentative (Full Cohesion Index: -0.611 and -0.051, respectively), primarily through class-based `Tribal Dominance`, `Envy`, and `Enmity` directed at an "oligarchy."

A key finding, enabled by the CFF's novel methodology, is the identification of sophisticated, high-tension rhetoric. The speech by Alexandria Ocasio-Cortez, for example, simultaneously employed high-intensity, high-salience appeals to both cohesive dimensions (e.g., `Individual Dignity`, `Amity`) and fragmentative ones (e.g., `Enmity`, `Envy`). This strategy appears to build a highly cohesive in-group ("class solidarity") for the purpose of waging a fragmentative conflict against a defined out-group ("billionaires"), resulting in a near-neutral overall cohesion score. This demonstrates the framework's capacity to move beyond simple valence and capture the complex, often contradictory, nature of modern political communication.

## 2. Opening Framework: Key Insights

* **Institutional vs. Populist Rhetoric Show Opposing Effects on Cohesion:** The data indicates a clear divide. Institutional discourse (McCain) scored +0.773 on the Full Cohesion Index, actively promoting unity. All populist examples scored negatively (King: -0.823, Sanders: -0.611, AOC: -0.051), suggesting their rhetorical structure is fundamentally fragmentative.
* **Fragmentation Achieved Through Different Populist Strategies:** Conservative populism (King) primarily leveraged exclusionary identity and existential threat, with high scores for `Tribal Dominance` (0.9), `Fear` (0.9), and `Enmity` (0.9). Progressive populism (Sanders, AOC) achieved fragmentation through class-based tribalism and resentment, with high scores for `Envy` (0.8 in both) and `Enmity` (0.9 in both).
* **High-Tension Rhetoric Builds In-Group Cohesion for Out-Group Conflict:** Alexandria Ocasio-Cortez's speech exemplifies a complex strategy of simultaneous cohesion and fragmentation. It scored high on both `Amity` (0.9) and `Enmity` (0.9), and on both `Individual Dignity` (0.9) and `Tribal Dominance` (0.75). This suggests a rhetorical model that builds strong in-group bonds for the explicit purpose of confronting an out-group.
* **Salience-Weighting Reveals True Rhetorical Emphasis:** The distinction between intensity and salience proved critical. For instance, while Sanders' speech contained appeals to `Hope` (Intensity: 0.6), its low salience (0.4) compared to `Fear` (Salience: 0.8) meant that the overall emotional climate was correctly identified as negative. This confirms the value of weighting scores by rhetorical prominence.
* **Framework Construct Validity Appears Sound:** Across the corpus, dimensions intended to be cohesive (`Individual Dignity`, `Hope`, `Amity`, `Cohesive Goals`) were associated with positive cohesion scores, while fragmentative dimensions (`Tribal Dominance`, `Fear`, `Envy`, `Enmity`) were associated with negative scores. This alignment suggests the framework's theoretical constructs are behaving as expected.
* **Rhetorical Contradiction Is Not Always Incoherent:** The `Strategic Contradiction Index` was relatively low across all speeches, even for AOC's high-tension discourse (0.071). This suggests that speakers can strategically deploy opposing appeals without creating a message that feels incoherent, so long as the emphasis is managed, a nuance captured by the CFF's tension formula.

## 4. Methodology

### Framework Description and Analytical Approach

This analysis employed the Cohesive Flourishing Framework (CFF) v10, a computational tool designed to assess the impact of political discourse on social cohesion. The CFF's core innovation is its independent scoring of ten dimensions organized into five opposing pairs: Identity (Tribal Dominance vs. Individual Dignity), Emotional Climate (Fear vs. Hope), Success Orientation (Envy vs. Compersion), Relational Climate (Enmity vs. Amity), and Goal Orientation (Fragmentative vs. Cohesive Goals).

For each dimension, the analysis captured both **intensity** (a 0.0-1.0 score of its strength) and **salience** (a 0.0-1.0 score of its rhetorical prominence). This dual-track approach allows for a more nuanced understanding of rhetorical strategy. From these base scores, several derived metrics were calculated:

* **Tension Indices:** Quantify the degree of strategic contradiction when opposing appeals are used with imbalanced emphasis.
* **Strategic Contradiction Index:** An average of all tension indices, measuring overall rhetorical coherence.
* **Salience-Weighted Cohesion Indices:** Three indices (Descriptive, Motivational, Full) that measure social cohesion on a scale from -1.0 (fragmentative) to +1.0 (cohesive), giving greater weight to themes the speaker emphasizes most. This report focuses on the **Full Cohesion Index** as the most comprehensive measure.

### Data Structure and Corpus Description

The corpus consists of four key American political speeches selected to represent different rhetorical styles:

* **`john_mccain_2008_concession.txt`**: An example of institutional discourse focused on democratic norms.
* **`steve_king_2017_house_floor.txt`**: An example of conservative populist discourse.
* **`bernie_sanders_2025_fighting_oligarchy.txt`**: An example of progressive populist discourse.
* **`alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`**: An example of progressive populist discourse with complex rhetorical layering.

Raw analytical data was provided, which included intensity and salience scores for each of the ten CFF dimensions for all four documents. Derived metrics were calculated from this raw data according to the formulas specified in the CFF v10 documentation.

### Statistical Methods and Analytical Constraints

Given the small sample size (N=4), this study is descriptive and exploratory. Inferential statistics like t-tests, while planned, were not appropriate due to insufficient statistical power (e.g., comparing one institutional speech to three populist ones). The primary analytical method involved the calculation of derived CFF metrics and a comparative analysis of these scores across the documents.

**Limitations:**

* **Sample Size:** With only four documents, the findings cannot be generalized. They are preliminary and serve to demonstrate the framework's analytical potential and generate hypotheses.
* **Data Inconsistencies:** Minor inconsistencies were present in the raw analysis output (e.g., `compassion` used for `compersion`, `enity` for `enmity`). These were resolved by mapping the provided data to the correct CFF dimensions as defined in the framework specification. All claims are made with this operationalization in mind.
* **Single Coder:** The analysis relies on a single set of scores from a computational agent. Future research would require inter-rater reliability checks with multiple human or AI coders.

## 5. Comprehensive Results

### 5.1 Descriptive Statistics

Analysis of the four documents reveals wide variance across the CFF dimensions, indicating the framework's ability to discriminate between different rhetorical styles. The institutional speech by McCain is a clear outlier on cohesive dimensions, while the populist speeches cluster at the opposite end of the spectrum.

**Table 1: Mean and Standard Deviation of CFF Dimension Scores (Intensity) Across Corpus (N=4)**

| Dimension                          | Mean (M) | Std. Dev. (SD) |
| :--------------------------------- | :------: | :------------: |
| **Fragmentative Dimensions** |          |                |
| Tribal Dominance                   |   0.66   |      0.38      |
| Fear                               |   0.65   |      0.38      |
| Envy                               |   0.40   |      0.43      |
| Enmity                             |   0.70   |      0.37      |
| Fragmentative Goals                |   0.41   |      0.46      |
| **Cohesive Dimensions**      |          |                |
| Individual Dignity                 |   0.48   |      0.40      |
| Hope                               |   0.58   |      0.34      |
| Compersion                         |   0.35   |      0.42      |
| Amity                              |   0.48   |      0.49      |
| Cohesive Goals                     |   0.51   |      0.45      |

The high standard deviations for most dimensions confirm the significant rhetorical differences within this small, diverse corpus. `Enmity` (M=0.70) and `Tribal Dominance` (M=0.66) were the most prevalent fragmentative themes overall, while `Hope` (M=0.58) was the most prevalent cohesive theme.

### 5.2 Advanced Metric Analysis

The derived CFF metrics provide a clearer picture of the strategic intent and potential impact of each speech. The Full Cohesion Index, in particular, starkly differentiates the institutional from the populist styles.

**Table 2: Calculated Derived Metrics by Document**

| Document     | Speaker | Style         | Strategic Contradiction Index | Full Cohesion Index |
| :----------- | :------ | :------------ | :---------------------------: | :-----------------: |
| McCain 2008  | McCain  | institutional |             0.038             |  **+0.773**  |
| King 2017    | King    | populist_c    |             0.032             |  **-0.823**  |
| Sanders 2025 | Sanders | populist_p    |             0.124             |  **-0.611**  |
| AOC 2025     | AOC     | populist_p    |             0.071             |  **-0.051**  |

John McCain's speech is an archetype of cohesive discourse, combining a very high cohesion score with very low strategic contradiction. This indicates a clear, consistent message aimed at unity. As McCain stated, the goal was to "find ways to come together, to find the necessary compromises to bridge our differences" (Source: `john_mccain_2008_concession.txt`). His rhetoric actively downplayed fear—"do not despair of our present difficulties"—while emphasizing universal opportunity: "America offers opportunities to all who have the industry and will to seize it" (Source: `john_mccain_2008_concession.txt`).

Conversely, Steve King's speech is an archetype of fragmentative discourse. Its extremely low cohesion score (-0.823) and low contradiction index (0.032) signify a clear, consistent message aimed at division. This was achieved by constructing an existential threat from an out-group. As King stated: "it's another life loss to an, an illegal criminal alien who was unlawfully present in America... costing in the end thousands of lives in America" (Source: `steve_king_2017_house_floor.txt`). This rhetoric is built on high-salience `Fear` (0.9), `Enmity` (0.9), and `Tribal Dominance` (0.9).

### 5.3 Correlation and Interaction Analysis

While a formal correlation matrix could not be computed, observational analysis reveals strong relationships between dimensions that align with the CFF's theoretical design.

**Fragmentative Clustering:** High scores on `Tribal Dominance`, `Fear`, `Envy`, and `Enmity` consistently appear together in the populist speeches and are associated with highly negative Full Cohesion Index scores. For example, Sanders' speech combines high `Tribal Dominance` (0.9) and `Enmity` (0.9) with high `Envy` (0.8). This is evidenced by his rhetoric defining a tribal out-group ("oligarchs") and expressing resentment towards their success: "The rich want to get richer and they don't care who they step on" (Source: `bernie_sanders_2025_fighting_oligarchy.txt`).

**Cohesive Clustering:** In McCain's speech, high scores on `Individual Dignity` (0.8), `Hope` (0.9), `Compersion` (0.9), and `Amity` (0.9) cluster together, producing the high positive cohesion score. This is reflected in his call for goodwill towards his opponent: "I had the honor of calling Senator Barack Obama to congratulate him... on being elected the next president of the country that we both love" (Source: `john_mccain_2008_concession.txt`). This statement registers as high `Compersion` (celebrating another's success) and `Amity`.

### 5.4 Pattern Recognition and Theoretical Insights

The most revealing pattern is the high-tension rhetoric identified in Alexandria Ocasio-Cortez's speech. The CFF's ability to score opposing dimensions independently is crucial here. Her speech scored high on both `Amity` (0.9) and `Enmity` (0.9), and on `Cohesive Goals` (0.85) and `Fragmentative Goals` (0.85).

This is not a contradiction but a sophisticated strategy: building in-group cohesion for out-group conflict. The `Amity` and `Cohesive Goals` are directed inward, toward the movement. As she stated: "Because in this house, we stand together... if we stand together, it is the only way that we can win" (Source: `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`). This call for "class solidarity" is a `Cohesive Goal` for the in-group.

Simultaneously, the `Enmity` and `Fragmentative Goals` are directed outward, at the "oligarchy." She identifies an enemy—"The same billionaires are taking a wrecking ball to our country"—and attributes fragmentative goals to them: "they derive their power from dividing working people apart" (Source: `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`). This dual strategy, which results in a near-zero cohesion score, would be missed by simpler analytical models that force a choice between "cooperative" or "conflictual." The CFF reveals it as a coherent strategy of targeted cohesion and targeted fragmentation.

### 5.5 Framework Effectiveness Assessment

Based on this pilot analysis, the CFF demonstrates significant discriminatory power. It clearly distinguished between the four speeches and produced metrics that align with a qualitative reading of the texts. The framework-corpus fit appears strong; the persuasive, strategic nature of the political speeches is well-suited to the CFF's dimensional structure.

The salience-weighted indices proved particularly effective. They correctly identified the dominant rhetorical thrust of each speech, preventing less-emphasized themes from distorting the overall cohesion measurement. The framework's ability to quantify high-tension rhetoric, as seen in the AOC analysis, represents a significant methodological insight, suggesting that much of modern populist appeal may lie in this blend of in-group love and out-group hate, a concept well-grounded in Social Identity Theory.

## 6. Discussion

The preliminary findings from this analysis suggest a profound rhetorical divide between traditional institutional politics and contemporary populism. The institutional model, as exemplified by McCain, appears normatively committed to post-conflict unification, using rhetoric that elevates shared identity (`Individual Dignity`) and forward-looking `Hope`. In contrast, both conservative and progressive populism appear to operate from a conflict-based model where social and political progress is contingent on the defeat of a defined enemy, whether cultural (King) or economic (Sanders, AOC).

The archetypes that emerge are the **Institutional Unifier** and the **Populist Combatant**. The Unifier's goal is system stability and bridging divides. The Combatant's goal is system disruption and the vanquishing of an oppressor. The CFF data suggests these are not merely differences in policy but fundamental differences in the perceived nature and purpose of political communication itself.

The most theoretically significant finding is the complex rhetorical structure of AOC's speech. It suggests a hybrid model that combines the universalist language of dignity and inclusion with the particularist language of class-based tribalism and enmity. This may represent an evolution in populist rhetoric, attempting to build a broader, more diverse coalition by appealing to universal values (`Individual Dignity`) while simultaneously sharpening the attack on a specific out-group (`Enmity`, `Envy`). The near-zero `Full Cohesion Index` (-0.051) for this speech is telling: it is a rhetoric perfectly balanced between building and breaking, uniting a specific "us" to fight a specific "them."

Future research should apply this framework to a much larger corpus of political texts to validate these preliminary archetypes. Investigating the temporal evolution from the institutional style of 2008 to the populist styles of 2017-2025 would be a particularly fruitful avenue. Furthermore, exploring audience reception to these different rhetorical packages could connect the CFF's discourse analysis to real-world behavioral outcomes.

## 7. Conclusion

This computational analysis, though limited in scope, successfully demonstrates the utility of the Cohesive Flourishing Framework v10 for dissecting the complex rhetorical strategies of modern political discourse. The framework's novel design, particularly its independent scoring of opposing dimensions and its use of salience-weighting, allowed for the identification of patterns that simpler models would miss.

The analysis provides preliminary, data-driven evidence for a stark rhetorical divergence between institutional and populist communication. While institutional discourse aims to foster broad social cohesion, populist discourse—regardless of ideological orientation—appears structurally fragmentative, predicated on conflict with a defined out-group. The study further reveals the sophisticated nature of some populist rhetoric, which can strategically blend cohesive and fragmentative appeals to build solidarity within a movement for the purpose of external conflict. These indicative findings warrant further investigation with larger datasets to explore the dynamics of social cohesion and fragmentation in contemporary democracy.

## 8. Evidence Citations

### `john_mccain_2008_concession.txt`

* **On Amity & Cohesive Goals:** "I urge all Americans - I urge all Americans who supported me to join me in not just congratulating him, but offering our next president our good will and earnest effort to find ways to come together, to find the necessary compromises to bridge our differences"
* **On Hope & Cohesive Goals:** "to find ways to come together, to find the necessary compromises to bridge our differences and help restore our prosperity, defend our security in a dangerous world, and leave our children and grandchildren a stronger, better country than we inherited."
* **On Individual Dignity:** "America offers opportunities to all who have the industry and will to seize it."
* **On Countering Fear:** "do not despair of our present difficulties"
* **On Compersion & Amity:** "I had the honor of calling Senator Barack Obama to congratulate him - please - to congratulate him on being elected the next president of the country that we both love."

### `steve_king_2017_house_floor.txt`

* **On Fear & Enmity:** "Well, Mr. Speaker, it was another day in, in the life of America and Americans. It's another life loss to an, an illegal criminal alien who was unlawfully present in America, who had no business to be here... This happens every day in this country... it's costing in the end thousands of lives in America."
* **On Tribal Dominance & Fragmentative Goals:** "We have a Constitution to preserve, protect, defend, and support and defend. And so our obligation then is to say, 'Mr. President, you're lame duck. Let's stick with the tradition...'"
* **On Fear & Existential Threat:** "And it would kick the breath out of your gut to hear that if you're a constitutionalist... thinking, 'What am I going to do tomorrow? Lord, wake me up with an idea on how to, how to preserve our Constitution,' if the Supreme Court of the United States believes that they can write law."

### `bernie_sanders_2025_fighting_oligarchy.txt`

* **On Tribal Dominance (Class-based):** "The American people are outraged at what's going on, and the American people are saying loud and clear, \"We will not accept an oligarchic form of society... all so that they could give over a trillion dollars in tax breaks to the wealthiest 1%.\""
* **On Envy & Enmity:** "The rich want to get richer and they don't care who they step on."
* **On Fear:** "They are prepared to destroy Social Security, Medicaid, Medicare, the Veterans Administration in order to make themselves even richer."
* **On Fragmentative Goals:** "That is what a rigged economy is about, and that is what we are going to change."

### `alexandria_ocasio_cortez_2025_fighting_oligarchy.txt`

* **On Amity & Cohesive Goals (In-group):** "Because in this house, we stand together, we know that, that it's our only choice because we know that without exception, if we stand together, it is the only way that we can win."
* **On Enmity (Out-group):** "The same billionaires are taking a wrecking ball to our country and they derive their power from dividing working people apart."
* **On Individual Dignity (Universal Appeal):** "If you are willing to fight for someone you don't know, you are welcome here... no matter who you voted for in the past. No matter if you know all the right words to say, no matter your race, religion, gender identity, or status"
* **On Envy:** "These kinds of spoils aren't earned really. They aren't working for these billions. They're stealing them. They're stealing them from you and you and me."
* **On Cohesive Goals (Movement-specific):** "This movement is not about partisan labels or purity tests, but about class solidarity."
