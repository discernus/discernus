# Populist Discourse Analysis Framework (PDAF) Analysis Report

**Experiment**: simple_test_pdaf  
**Framework**: pdaf_v10.md  
**Corpus**: corpus.md (4 documents)  

---

## 1. Executive Summary

This report presents a computational analysis of political discourse from four American political figures, utilizing the Populist Discourse Analysis Framework (PDAF) v10.0.0. The analysis of speeches from John McCain, Steve King, Bernie Sanders, and Alexandria Ocasio-Cortez reveals a clear and quantifiable distinction between institutional and populist rhetoric. The preliminary findings from this pilot study (N=4) indicate that while populist actors share a common rhetorical core—characterized by Manichaean people-elite framing, crisis narratives, and accusations of systemic corruption—they diverge significantly along ideological lines. This divergence is most starkly captured by the framework's "Boundary Distinctions" dimensions.

The data suggests a fundamental schism in how different types of populists define "the people." The conservative populist discourse of Steve King is characterized by a high degree of `Nationalist Exclusion` (Raw Score = 0.90), defining the ingroup along national and cultural lines while exhibiting a complete absence of economic populist appeals. Conversely, the progressive populist discourse of Bernie Sanders and Alexandria Ocasio-Cortez is defined by maximal scores in `Economic Populist Appeals` (Raw Score = 1.00 for both), constructing the ingroup around economic class struggle while eschewing nationalist exclusion. John McCain's 2008 concession speech serves as a crucial control case, with negligible scores across all populist dimensions, thereby demonstrating the framework's discriminatory power.

Furthermore, the PDAF's novel "strategic tension" metrics provide a more nuanced understanding of populist strategy. For instance, the `Democratic-Authoritarian Tension` metric reveals how both King and Sanders balance claims of popular sovereignty with anti-pluralist rhetoric, a tension not present in Ocasio-Cortez's speech. The `Crisis-Elite Attribution Tension` is notably higher among progressive populists, suggesting a tighter strategic linkage between articulating a societal crisis and attributing it to elite malfeasance. These findings underscore the PDAF's capacity to move beyond binary classification, offering a multi-dimensional, data-driven methodology for dissecting the complex and often contradictory nature of populist communication.

## 2. Opening Framework: Key Insights

- **Populist vs. Institutional Discourse Is Quantifiably Distinct:** The analysis demonstrates the framework's effectiveness in differentiating populist from non-populist speech. The three populist speakers (King, Sanders, Ocasio-Cortez) registered high `Salience-Weighted Core Populism Index` scores (0.81, 0.76, and 0.79, respectively), while the institutional speaker (McCain) scored near-zero (0.10).

- **Ideological Divergence Occurs in Boundary Construction:** The most significant finding is the clear ideological split in how populists define the boundaries of "the people." Conservative populism (King) relies heavily on `Nationalist Exclusion` (Raw Score = 0.90), while progressive populism (Sanders, AOC) is defined by `Economic Populist Appeals` (Raw Score = 1.00). This creates a near-perfect inverse relationship within the `Boundary Distinctions` category.

- **A Shared Rhetorical Core Unites Populists:** Despite ideological differences, all analyzed populist speakers employ a similar core rhetorical toolkit. They consistently score high on `Manichaean People-Elite Framing` (Mean = 0.87), `Crisis-Restoration Narrative` (Mean = 0.77), and `Elite Conspiracy/Systemic Corruption` (Mean = 0.87), suggesting these are foundational elements of contemporary American populism.

- **Strategic Tensions Reveal Nuanced Rhetorical Strategies:** The PDAF's tension metrics highlight subtle differences in populist messaging. For example, both King and Sanders exhibit a `Democratic-Authoritarian Tension` score of 0.10, indicating a strategic balancing of popular sovereignty claims with anti-pluralist elements. In contrast, Ocasio-Cortez's speech avoids this specific tension by forgoing sovereignty claims, despite a high anti-pluralism score.

- **Progressive Populism Tightly Links Crisis and Conspiracy:** The progressive speakers (Sanders and Ocasio-Cortez) display the highest `Crisis-Elite Attribution Tension` (0.14 for both). This suggests their strategy involves a more deliberate and balanced fusion of describing a societal crisis and attributing it to a corrupt elite conspiracy, a linkage less pronounced in the conservative populist example.

- **Distinct Speaker Archetypes Emerge:** The analysis reveals unique rhetorical profiles. Alexandria Ocasio-Cortez's discourse is uniquely characterized by high scores in `Authenticity vs. Political Class` (0.90) and `Homogeneous People Construction` (0.80), suggesting a strategy focused on building an inclusive, authentic movement identity. Steve King's profile is dominated by nationalism, while Bernie Sanders' centers on a potent combination of core populism and intense economic critique.

## 4. Methodology

### Framework Description and Analytical Approach

This analysis employs the Populist Discourse Analysis Framework (PDAF) v10.0.0, a computational tool designed to measure the core components of populist communication. The framework moves beyond simple binary classification by operationalizing nine distinct dimensions of populist rhetoric, each measured for its presence (raw score) and its prominence (salience score).

The PDAF's innovation lies in its derived metrics. It calculates four **Salience-Weighted Indices** (`Core Populism`, `Populism Mechanisms`, `Boundary Distinctions`, `Overall Populism`) that provide a more robust measure of populist intensity by weighting raw scores by their salience. Crucially, it also introduces three **Strategic Tension Indices**:
1.  **Democratic-Authoritarian Tension:** Measures the contradiction between claims of popular sovereignty and anti-pluralist, exclusionary rhetoric.
2.  **Internal-External Focus Tension:** Measures the balance between constructing an internal "homogeneous people" and defining it against an external "other" via nationalist exclusion.
3.  **Crisis-Elite Attribution Tension:** Measures the strategic linkage between narratives of crisis and attributions of elite conspiracy.

The analytical approach is primarily descriptive and comparative, leveraging the quantitative scores produced by the framework to identify patterns, compare speaker profiles, and assess the framework's utility. Given the small sample size (N=4), this study is considered a pilot analysis, and its findings are preliminary and suggestive rather than generalizable.

### Data Structure and Corpus Description

The analysis was conducted on the **Democratic Discourse Corpus**, comprising four speeches from American political figures spanning 2008-2025:
-   **John McCain (Republican, 2008):** 2008 Presidential Concession Speech (classified as `institutional`).
-   **Steve King (Republican, 2017):** 2017 House Floor Speech (classified as `populist_conservative`).
-   **Bernie Sanders (Independent, 2025):** "Fighting Oligarchy" Speech (classified as `populist_progressive`).
-   **Alexandria Ocasio-Cortez (Democratic, 2025):** "Fighting Oligarchy" Speech (classified as `populist_progressive`).

The dataset for each document includes raw scores (0-1), salience scores (0-1), and confidence scores for each of the nine PDAF dimensions.

### Statistical Methods and Analytical Constraints

The analysis relies on the descriptive statistics and derived metrics provided in the `Complete Research Data`. The primary method involves comparing the mean scores of individual speakers and ideological groups across the framework's dimensions and derived indices.

A notable constraint was identified in the provided automated statistical output. Several functions failed to correctly parse speaker identities or ideological categories, and data inconsistencies (e.g., a column name typo for `homogeneous_people_construction`) resulted in `NaN` (Not a Number) values for some derived metrics in the automated summary tables. To ensure analytical rigor, this report is based on a manual aggregation and recalculation of speaker profiles directly from the document-level data provided in the `calculate_derived_metrics` output, which was complete and well-formed. This approach circumvents the errors in the higher-level summary functions and allows for a more accurate and detailed analysis. All claims are based on this manually verified data.

## 5. Comprehensive Results

The analysis reveals starkly different rhetorical profiles among the four speakers, highlighting the PDAF's ability to capture both the shared core and ideological variations of populist discourse.

### 5.1 Descriptive Statistics: Speaker Profiles

The mean scores for each speaker across the nine primary dimensions and key derived indices are presented below. These profiles form the basis of the comparative analysis. John McCain's speech serves as the institutional baseline, against which the three populist speakers are compared.

**Table 1: Mean Raw Scores by Speaker**

| Dimension                                    | McCain | King  | Sanders | AOC   |
| -------------------------------------------- | ------ | ----- | ------- | ----- |
| Manichaean People-Elite Framing              | 0.00   | 0.80  | 0.90    | 0.90  |
| Crisis-Restoration Narrative                 | 0.10   | 0.90  | 0.70    | 0.70  |
| Popular Sovereignty Claims                   | 0.00   | 0.80  | 0.80    | 0.00  |
| Anti-Pluralist Exclusion                     | 0.00   | 0.20  | 0.20    | 0.70  |
| Elite Conspiracy/Systemic Corruption         | 0.00   | 0.80  | 0.90    | 0.90  |
| Authenticity vs. Political Class             | 0.00   | 0.00  | 0.00    | 0.90  |
| Homogeneous People Construction              | 0.00   | 0.10  | 0.70    | 0.80  |
| Nationalist Exclusion                        | 0.10   | 0.90  | 0.00    | 0.00  |
| Economic Populist Appeals                    | 0.00   | 0.00  | 1.00    | 1.00  |

**Table 2: Key Derived Metric Scores by Speaker**

| Derived Metric                               | McCain | King  | Sanders | AOC   |
| -------------------------------------------- | ------ | ----- | ------- | ----- |
| Salience-Weighted Core Populism Index        | 0.10   | 0.81  | 0.76    | 0.79  |
| Salience-Weighted Boundary Distinctions Index| 0.10   | 0.90  | 1.00    | 1.00  |
| Democratic-Authoritarian Tension             | 0.00   | 0.10  | 0.10    | 0.00  |
| Crisis-Elite Attribution Tension             | 0.00   | 0.00  | 0.14    | 0.14  |

### 5.2 Advanced Metric Analysis: Unpacking Strategy

The derived metrics provide deeper insights into the strategic construction of each message.

**Salience-Weighted Indices:** The `Salience-Weighted Core Populism Index` confirms that King (0.81), Sanders (0.76), and AOC (0.79) all employ a strong populist core, while McCain (0.10) does not. The power of the framework is most evident in the `Salience-Weighted Boundary Distinctions Index`. Here, the ideological divergence is unmistakable. King's score of 0.90 is driven entirely by `Nationalist Exclusion`, while Sanders' and AOC's scores of 1.00 are driven entirely by `Economic Populist Appeals`. This metric effectively quantifies the "thin-centered" nature of populism, showing how the core ideology is "filled" by distinct, and mutually exclusive, host ideologies.

**Strategic Tension Analysis:** The tension metrics reveal the subtle balancing acts within each speech.
-   **Democratic-Authoritarian Tension:** Both Steve King and Bernie Sanders register a tension score of 0.10. This indicates that their rhetoric combines strong claims to represent the will of the people (`Popular Sovereignty Claims` raw scores of 0.80 for both) with exclusionary, anti-pluralist language (`Anti-Pluralist Exclusion` raw scores of 0.20 for both). As Sanders stated, "The American people are outraged... and the American people are saying loud and clear, 'We will not accept an oligarchic form of society'" (Source: bernie_sanders_2025_fighting_oligarchy.txt), a clear sovereignty claim. This is balanced against exclusionary undertones. King's speech pairs similar sovereignty claims with explicit exclusion of "criminal aliens" (Source: steve_king_2017_house_floor.txt). Interestingly, Alexandria Ocasio-Cortez avoids this tension (score = 0.00) not by being less anti-pluralist (her score of 0.70 is the highest in the sample), but by completely avoiding popular sovereignty claims. This suggests a different strategic choice: to focus on defining the enemy rather than claiming to embody the popular will.

-   **Crisis-Elite Attribution Tension:** The progressive populists, Sanders and Ocasio-Cortez, exhibit the highest tension score here (0.14). This reflects a highly coordinated message that pairs a salient `Crisis-Restoration Narrative` (raw scores of 0.70) with an equally salient `Elite Conspiracy` narrative (raw scores of 0.90). Ocasio-Cortez exemplifies this fusion: "We are witnessing an oligarchy in America. And that is when those with the most economic, political, and technological power destroy the public good to enrich themselves while millions of Americans pay the price" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt). This quote simultaneously invokes a crisis ("destroy the public good") and attributes it to a conspiratorial elite ("oligarchy... enrich themselves"). King, by contrast, has zero tension here, as his crisis narrative is not matched in salience by a conspiracy narrative.

### 5.4 Pattern Recognition and Theoretical Insights

#### The Populist/Institutional Divide

The data provides a clear quantitative baseline for non-populist, institutional discourse. John McCain's speech is virtually devoid of populist markers, with near-zero scores across all core dimensions. His language, as captured in the quote, "The American people have spoken, and they have spoken clearly" (Source: john_mccain_2008_concession.txt), acknowledges popular sovereignty in a procedural, democratic context, starkly contrasting with the populist co-optation of the term. This validates the framework's ability to discriminate between rhetorical modes.

#### The Shared Core of Populist Rhetoric

Across the ideological divide, the three populist speakers build their arguments on a common foundation.
-   **Manichaean People-Elite Framing (Mean Raw Score = 0.87):** All three present politics as a moral struggle. This is vividly illustrated by Ocasio-Cortez's claim that "The same billionaires are taking a wrecking ball to our country and they derive their power from dividing working people apart" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt), which constructs a virtuous "working people" against destructive "billionaires."
-   **Elite Conspiracy/Systemic Corruption (Mean Raw Score = 0.87):** The elite are not just misguided; they are corrupt and conspiratorial. Ocasio-Cortez accuses a political opponent of having "handed the keys to Elon Musk and is selling off our country for parts to the wealthiest people in the world for a kickback" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt). This narrative of a self-serving, colluding elite is a cornerstone of the populist appeal.
-   **Crisis-Restoration Narrative (Mean Raw Score = 0.77):** Populist rhetoric is animated by a sense of urgency and decline. Steve King frames this as a constitutional crisis, arguing that "we have a Constitution that's got to be restored" (Source: steve_king_2017_house_floor.txt). This temporal narrative—a virtuous past, a corrupt present, and a promised restoration—is a powerful mobilizing tool shared by all three populists.

#### The Great Divergence: Nationalist vs. Economic Boundaries

The most powerful insight from this analysis is the ideological chasm in how populists construct their ingroup. The `Boundary Distinctions` dimensions act as a near-perfect classifier for conservative versus progressive populism in this sample.
-   **Conservative Populism & Nationalist Exclusion:** Steve King's discourse is defined by a high score on `Nationalist Exclusion` (0.90) and a zero on `Economic Populist Appeals`. His rhetoric focuses on threats from outside the national community. He states, "This President has... released over 30,000 criminals, criminal aliens onto the streets of America" (Source: steve_king_2017_house_floor.txt). This defines the threat in national and legal-status terms, constructing "the people" as law-abiding citizens threatened by foreign elements.
-   **Progressive Populism & Economic Appeals:** In stark contrast, Bernie Sanders and Alexandria Ocasio-Cortez score a perfect 1.00 on `Economic Populist Appeals` and zero on `Nationalist Exclusion`. Their construction of "the people" is rooted in economic class. As Sanders declares, "We will not accept the richest guy in the world... giv[ing] over a trillion dollars in tax breaks to the wealthiest 1%" (Source: bernie_sanders_2025_fighting_oligarchy.txt). Here, "the people" are the 99% exploited by the "wealthiest 1%." The enemy is an internal economic class, not an external national threat.

### 5.5 Framework Effectiveness Assessment

Based on this pilot analysis, the PDAF v10.0.0 demonstrates significant promise and effectiveness.
-   **Discriminatory Power:** The framework successfully and decisively separated the institutional speech from the three populist speeches. Furthermore, it effectively discriminated between conservative and progressive variants of populism, primarily through the `Boundary Distinctions` dimensions.
-   **Framework-Corpus Fit:** The framework's dimensions mapped well onto the content of the speeches. The high scores on core dimensions for the populist speakers, contrasted with low scores for the institutional speaker, indicate a strong fit. The fact that `Nationalist Exclusion` and `Economic Populist Appeals` acted as such clear ideological markers suggests these dimensions are well-calibrated for the contemporary American political context.
-   **Methodological Insights:** The inclusion of salience-weighting and strategic tension metrics represents a significant methodological advance. Salience-weighting prevents a simple checklist approach, giving more prominence to the themes a speaker emphasizes. The tension metrics, in particular, move the analysis from a static measurement of features to a dynamic assessment of rhetorical strategy, revealing the complex and sometimes contradictory logic of populist communication.

## 6. Discussion

The preliminary findings of this analysis have several important theoretical and practical implications. The results lend strong support to theories that conceptualize populism as a "thin-centered ideology"—a core set of ideas (the virtuous people vs. the corrupt elite) that can be attached to various "thick" host ideologies like nationalism or socialism. This analysis provides a quantitative demonstration of that process: the PDAF's `Core Populism` dimensions represent the "thin" ideology, while the `Boundary Distinctions` dimensions represent the "thick" ideological content that "fills" it.

The analysis also allows for the identification of distinct populist archetypes within this small sample:
1.  **The Institutionalist (McCain):** Characterized by an absence of populist rhetoric, adherence to procedural norms, and unifying, rather than polarizing, language.
2.  **The Nationalist Populist (King):** Combines the core populist antagonism with a boundary of nationhood and cultural purity, directing hostility towards external or "alien" threats.
3.  **The Economic Populist (Sanders):** Fuses core populism with a class-based boundary, directing hostility towards an internal economic oligarchy.
4.  **The Authentic-Intersectional Populist (AOC):** Builds on the economic populist model but adds a strong emphasis on personal authenticity and the construction of a broad, inclusive coalition of "working people." Her high score on `Homogeneous People Construction` (0.80) is particularly revealing. While the term can imply ethnic homogeneity, the supporting evidence—"If you are willing to fight for working people regardless of who they are, how they identify, or where they come from, you are welcome here" (Source: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt)—suggests she is constructing a new, *ideologically* homogeneous "people" based on shared struggle, a key feature of progressive movement-building.

The strategic tension metrics suggest that populist communication is a calculated endeavor. The differing tension profiles between speakers indicate that there is not one single "populist playbook" but rather a set of rhetorical tools that can be combined in different ways to navigate specific strategic dilemmas, such as balancing democratic legitimacy with the need to mobilize a base through exclusionary tactics.

### Limitations and Future Directions

The primary limitation of this study is its extremely small sample size (N=4). The findings, while clear and compelling within this sample, cannot be generalized to all populist or institutional discourse. They should be considered preliminary hypotheses that require validation on a much larger and more diverse corpus of political texts.

Future research should expand the corpus to include a wider range of speakers, ideologies, political systems, and time periods. This would allow for a more robust testing of the archetypes identified here. Researchers may wish to explore how strategic tension patterns evolve over a politician's career or in response to specific political events. Finally, integrating the PDAF with audience reception data could provide a crucial link between rhetorical strategy and political impact, exploring whether audiences perceive and respond to the strategic tensions this framework identifies.

## 7. Conclusion

This computational analysis, though limited in scope, successfully demonstrates the analytical power of the Populist Discourse Analysis Framework v10.0.0. By moving beyond simple labels, the PDAF provides a nuanced, multi-dimensional, and quantitative method for dissecting political language. The framework not only validates the core theoretical tenets of populism studies but also enriches them by revealing the precise rhetorical mechanisms of ideological divergence.

The key contribution of this analysis is the data-driven confirmation of a fundamental split in American populism: a shared antipathy towards "the elite" that is channeled into two distinct, mutually exclusive definitions of "the people"—one nationalist, the other economic. The framework's novel metrics for salience and strategic tension offer a promising new direction for the computational analysis of political communication, enabling researchers to decode not just *what* is being said, but *how* it is being strategically constructed. These preliminary findings warrant a broader application of the PDAF to further map the complex landscape of contemporary political discourse.

## 8. Evidence Citations

**alexandria_ocasio_cortez_2025_fighting_oligarchy.txt**
- "We are witnessing an oligarchy in America. And that is when those with the most economic, political, and technological power destroy the public good to enrich themselves while millions of Americans pay the price."
- "The same billionaires are taking a wrecking ball to our country and they derive their power from dividing working people apart."
- "It’s shorthand for the right wing’s entire political agenda and a certain ugly kind of politics, a politics that involves lying to and screwing over working and middle class Americans so that they can steal from our healthcare, Social Security, and veterans’ benefits to pay for tax cuts for the wealthiest and bailouts for their crypto billionaire friends."
- "He’s handed the keys to Elon Musk and is selling off our country for parts to the wealthiest people in the world for a kickback. And in exchange, those billionaires and oligarchs will back his campaigns and bankroll those of his allies. They scratch his back and he scratches theirs."
- "If you are willing to fight for working people regardless of who they are, how they identify, or where they come from, you are welcome here."
- "But I will say this, those leaders on either side of the aisle who are willing to put their fellow Americans down, so that they can get ahead or feel better about themselves, those folks may best find a home somewhere else."

**bernie_sanders_2025_fighting_oligarchy.txt**
- "The American people are outraged at what’s going on, and the American people are saying loud and clear, “We will not accept an oligarchic form of society."
- "We will not accept the richest guy in the world running all over Washington, making cuts to the Social Security Administration, cuts to the Veterans Administration, almost destroying the Department of Education, all so that they could give over a trillion dollars in tax breaks to the wealthiest 1%."

**john_mccain_2008_concession.txt**
- "The American people have spoken, and they have spoken clearly."

**steve_king_2017_house_floor.txt**
- "...because we have a Constitution that's got to be restored. And instead of being restored, it would be destroyed by another presidential appointment."
- "This President has, has released, his administration has released over 30,000 criminals, criminal aliens onto the streets of America. And of those that they released, there have been at least 124 of them who have been charged with homicide for 135 murders."