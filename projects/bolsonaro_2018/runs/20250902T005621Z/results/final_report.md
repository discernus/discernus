# Populist Discourse Analysis Framework Analysis Report

**Experiment**: bolsonaro_2018
**Run ID**: Not Available
**Date**: 2025-09-02
**Framework**: pdaf_v10_0_2.md
**Corpus**: corpus.md (13 documents)
**Analysis Model**: vertex_ai/gemini-2.5-flash
**Synthesis Model**: vertex_ai/gemini-2.5-pro

---
## 1. Executive Summary

This report presents a computational analysis of 13 speeches from Jair Bolsonaro's 2018 Brazilian presidential campaign, utilizing the Populist Discourse Analysis Framework (PDAF) v10.0.2. The analysis challenges the common narrative of a simple, linear intensification of populist rhetoric over the course of the campaign. Instead, the findings reveal a consistently high level of multi-dimensional populism present from the very outset. The mean Salience-Weighted Overall Populism Index across the corpus was a remarkably high 0.82, indicating that populist framing was a core, rather than an emergent, feature of the campaign's communication strategy.

The study identifies a sophisticated pattern of rhetorical modulation rather than uniform escalation. While core populist themes—such as `Manichaean People-Elite Framing` (M=0.87), `Crisis-Restoration Narrative` (M=0.84), and `Authenticity vs. Political Class` (M=0.84)—remained intensely and saliently stable, other dimensions demonstrated significant variance contingent on campaign events. Specifically, `Anti-Pluralist Exclusion` and `Economic Populist Appeals` were strategically de-emphasized at critical junctures, such as immediately before the first-round vote. The September 6th assassination attempt served as a key rhetorical catalyst, precipitating a marked increase in `Elite Conspiracy/Systemic Corruption` narratives (mean raw score increased from 0.70 pre-stabbing to 0.76 post-stabbing), framing the attack as proof of a corrupt system aligned against him.

Furthermore, the analysis of strategic contradictions reveals a complex rhetorical balancing act. The highest level of contradictory messaging, as measured by the Populist Strategic Contradiction Index (PSCI), occurred not during mass rallies but in a speech to business leaders (PSCI = 0.18). This suggests a deliberate strategy of simultaneously deploying and differentially emphasizing conflicting populist messages to build a broad but ideologically diverse coalition. These findings underscore the utility of the PDAF's multi-dimensional, salience-weighted approach in moving beyond binary classifications to uncover the nuanced, dynamic, and strategically coherent nature of contemporary populist discourse.

## 2. Opening Framework: Key Insights

*   **Populism as a Baseline, Not a Crescendo**: Contrary to the hypothesis of populist intensification, Jair Bolsonaro's discourse began with and maintained an exceptionally high level of populism. The mean Salience-Weighted Overall Populism Index was 0.82, with the first speech scoring 0.85. This suggests his populist platform was a foundational, not an adaptive, strategy.
*   **The Assassination Attempt as a Conspiracy Catalyst**: The September 6th stabbing incident did not uniformly amplify all populist themes. While `Manichaean People-Elite Framing` remained stable, `Elite Conspiracy/Systemic Corruption` scores rose significantly in its aftermath (mean raw score +0.06). Bolsonaro leveraged the attack to substantiate claims of a corrupt system actively working against him, as seen in his post-stabbing speech where he claimed, "The PT discovered the path to power. The electronic vote" (Source: 2018-09-16_Post-Stabbing_Speech.txt).
*   **Strategic Modulation of Exclusionary Rhetoric**: The analysis revealed significant variance across campaign stages for `Anti-Pluralist Exclusion` (ANOVA, p=0.033) and `Economic Populist Appeals` (ANOVA, p=0.014). Both themes were notably suppressed in the speech immediately preceding the first-round vote, indicating a tactical moderation of more divisive messages to consolidate a broader electoral base at a critical moment.
*   **Maximum Contradiction Aimed at Elites**: The highest Populist Strategic Contradiction Index (PSCI = 0.18) was recorded in the speech to business leaders on September 6th. This was driven by a high tension between appeals to popular sovereignty and anti-pluralism, and between constructing internal unity and emphasizing external threats. This finding suggests a sophisticated strategy of deploying contradictory messages with differential emphasis to appeal to elite audiences without alienating the populist base.
*   **A Stable Core of Populist Rhetoric**: The bedrock of Bolsonaro's populism consisted of three consistently high-scoring and highly salient dimensions: `Manichaean People-Elite Framing` (Mean Raw=0.87, Mean Salience=0.85), `Crisis-Restoration Narrative` (Mean Raw=0.84, Mean Salience=0.84), and `Authenticity vs. Political Class` (Mean Raw=0.84, Mean Salience=0.81). This stable triad formed the unwavering narrative engine of his campaign.

## 4. Methodology

### 4.1 Framework Description
This analysis employed the Populist Discourse Analysis Framework (PDAF) v10.0.2, a computational tool designed to quantify the components of populist political communication. The PDAF evaluates texts across nine core dimensions organized into three theoretical categories:
1.  **Primary Populist Core Anchors**: `Manichaean People-Elite Framing`, `Crisis-Restoration Temporal Narrative`, `Popular Sovereignty Claims`, `Anti-Pluralist Exclusion`.
2.  **Populist Mechanism Anchors**: `Elite Conspiracy/Systemic Corruption`, `Authenticity vs. Political Class`, `Homogeneous People Construction`.
3.  **Boundary Distinction Anchors**: `Nationalist Exclusion`, `Economic Populist Appeals`.

A key innovation of the PDAF is its use of salience-weighting, which measures not only the intensity of a theme (raw_score, 0.0-1.0) but also its rhetorical prominence within the text (salience, 0.0-1.0). This allows for the calculation of Salience-Weighted Indices that reflect the strategic emphasis of the discourse. The framework also calculates a Populist Strategic Contradiction Index (PSCI) to quantify the use of contradictory messaging.

### 4.2 Corpus and Data Structure
The corpus consists of 13 speeches delivered by Jair Bolsonaro between July 22, 2018, and October 27, 2018. The documents were selected to represent key moments in the campaign, including the official launch, mass rallies, a speech to business leaders, and communications following the September 6th assassination attempt. Each document was analyzed by the `vertex_ai/gemini-2.5-flash` model, which produced scores for each of the nine dimensions, along with supporting textual evidence.

### 4.3 Statistical Methods
The analysis relied on descriptive and inferential statistics generated from the model's output. Key methods included:
*   **Descriptive Statistics**: Calculation of mean, median, and standard deviation for all raw and salience scores to identify central tendencies and variability.
*   **Salience-Weighted Indices**: Calculation of overall, core, mechanism, and boundary indices to assess the emphasized components of the populist message.
*   **Strategic Tension Analysis**: Calculation of the Populist Strategic Contradiction Index (PSCI) to measure rhetorical incoherence or strategic ambiguity.
*   **Hypothesis Testing**: A series of pre-defined hypotheses were evaluated using the statistical results. This included comparisons of means between campaign phases (e.g., pre- vs. post-stabbing) and analysis of variance (ANOVA) to detect significant differences in dimensional scores across campaign stages.
*   **Reliability Analysis**: Cronbach's alpha was calculated for the Primary Populist Core Anchors to assess their internal consistency as a measure of a single underlying construct.

### 4.4 Limitations
This study's findings should be considered in light of several limitations. The sample size of 13 documents is small, which limits the statistical power of some tests and means the findings are preliminary and indicative rather than definitive. The automated statistical analysis did not produce a correlation matrix, rendering hypotheses H₃ and H₁₃ untestable. Some statistical tests (e.g., t-tests on single-document campaign stages) were not possible due to insufficient data points. The analysis is confined to the textual content of formal speeches and does not capture other modes of communication or audience reception.

## 5. Comprehensive Results

### 5.1 Hypothesis Evaluation

This section evaluates the 14 hypotheses outlined in the experiment configuration.

**H₁ (Overall Populism ≥ 0.5): CONFIRMED.**
The mean Salience-Weighted Overall Populism Index across all speeches was 0.82, substantially exceeding the 0.5 threshold for a "somewhat populist" classification. The lowest score recorded for any speech was 0.75, confirming that Bolsonaro's discourse was consistently and intensely populist throughout the campaign.

**H₂ (μ_late_campaign > μ_early_campaign): FALSIFIED.**
The populist intensification hypothesis was not supported. A pairwise comparison of the Salience-Weighted Overall Populism Index for the designated 'early_campaign' speech (0.85) and 'late_campaign' speech (0.84) showed a negligible decrease. The broader temporal trend analysis also indicated a slight, though not statistically significant, decreasing trend over the entire campaign.

**H₃ (Patriotic/nationalist framing vs. people-centric populist dimensions correlation < -0.3): INDETERMINATE.**
The statistical analysis did not generate a correlation matrix, making it impossible to test the relationship between `Nationalist Exclusion` and the core populist dimensions.

**H₄ (μ_post_stabbing > μ_pre_stabbing on Manichaean People-Elite Framing): FALSIFIED.**
The mean raw score for `Manichaean People-Elite Framing` was identical in the pre-stabbing and post-stabbing periods (M = 0.875 for both). The assassination attempt did not appear to amplify this specific dimension of his populism, which was already at a near-maximum level. As Bolsonaro stated in his first speech, "In the barracks you have companionship, patriotism, discipline, hierarchy, love for the homeland. In politics, no. [...] Thank you again, Geraldo Alckmin [laughter], for having united the scum of Brazilian politics [applause]" (Source: 2018-07-22_PSL_Conference_Candidacy_Launch.txt), establishing this high baseline early on.

**H₅ (Anti-Pluralist Exclusion and Crisis-Restoration salience > 0.7): CONFIRMED.**
Both dimensions demonstrated high rhetorical salience. The mean salience for `Anti-Pluralist Exclusion` was 0.79, and the mean salience for `Crisis-Restoration Narrative` was 0.84. This confirms these two themes were central pillars of his messaging.

**H₆ (Business audience speeches score lower on Economic Populist Appeals): FALSIFIED.**
The speech to business leaders on September 6th scored 0.7 for `Economic Populist Appeals`, which was *higher* than the corpus-wide mean of 0.62 and higher than scores from mass public rallies. In this speech, he framed his policy as liberating producers, stating, "What does Brazil need? It needs someone, then, to take the State off the back of those who produce" (Source: 2018-09-06_Juiz_de_Fora_Business_Association.txt).

**H₇ (Populist Strategic Contradiction Index highest in October): FALSIFIED.**
The highest PSCI score (0.18) was recorded on September 6th in the speech to business leaders, not in October. This suggests that the need to balance contradictory messages was greatest when addressing an elite, rather than a mass, audience.

**H₈ (Elite Conspiracy dimension increase after stabbing): CONFIRMED.**
The mean raw score for `Elite Conspiracy/Systemic Corruption` increased from 0.70 in the pre-stabbing period to 0.76 in the post-stabbing period. The speech immediately following the attack scored a 0.9 on this dimension, featuring claims that "The PT discovered the path to power. The electronic vote," and that the potential for electoral fraud was "concrete" (Source: 2018-09-16_Post-Stabbing_Speech.txt).

**H₉ (Linear trend shows positive slope for overall populism): FALSIFIED.**
The temporal trend analysis indicated a slight decreasing, not increasing, trend in the overall populism index over the campaign.

**H₁₀ (Variance in populist scores increases in final campaign month): FALSIFIED.**
The Levene's test for equality of variances was not significant, indicating that the variability of populist scores did not increase in October compared to earlier months.

**H₁₁ (At least 5 of 9 PDAF dimensions show significant differences between campaign_stage groups): FALSIFIED.**
ANOVA testing revealed that only two dimensions, `Anti-Pluralist Exclusion` (p=0.033) and `Economic Populist Appeals` (p=0.014), showed statistically significant variance across the defined campaign stages. The core populist message remained largely stable.

**H₁₂ (Core populist dimensions have higher internal consistency, Cronbach's α > 0.8): FALSIFIED.**
The Cronbach's alpha for the four core populist dimensions was 0.77. While this indicates acceptable internal consistency, it falls short of the hypothesized 0.8 threshold.

**H₁₃ (Nationalist Exclusion correlates positively with Anti-Pluralist Exclusion, r > 0.5): INDETERMINATE.**
This hypothesis could not be tested due to the absence of a correlation matrix in the statistical output.

**H₁₄ (Economic Populist Appeals salience lowest in business/policy speeches, < 0.3): FALSIFIED.**
The salience score for `Economic Populist Appeals` in the speech to business leaders was 0.7, far exceeding the < 0.3 threshold.

### 5.2 Descriptive Statistics

The analysis reveals a discourse saturated with populist rhetoric across multiple dimensions. The core tenets of populism were not only present but were the most intense and salient features of the campaign.

**Table 1: Descriptive Statistics for PDAF Dimensions (Raw Scores & Salience)**

| Dimension                                | Mean Raw Score (SD) | Mean Salience (SD) |
| ---------------------------------------- | ------------------- | ------------------ |
| **Core Anchors**                         |                     |                    |
| Manichaean People-Elite Framing          | 0.87 (0.05)         | 0.85 (0.05)        |
| Crisis-Restoration Narrative             | 0.84 (0.12)         | 0.84 (0.09)        |
| Anti-Pluralist Exclusion                 | 0.82 (0.17)         | 0.79 (0.18)        |
| Popular Sovereignty Claims               | 0.73 (0.10)         | 0.70 (0.11)        |
| **Mechanism Anchors**                    |                     |                    |
| Authenticity vs. Political Class         | 0.84 (0.07)         | 0.81 (0.07)        |
| Homogeneous People Construction          | 0.83 (0.09)         | 0.82 (0.10)        |
| Elite Conspiracy/Systemic Corruption     | 0.74 (0.15)         | 0.70 (0.13)        |
| **Boundary Anchors**                     |                     |                    |
| Nationalist Exclusion                    | 0.73 (0.17)         | 0.70 (0.17)        |
| Economic Populist Appeals                | 0.62 (0.17)         | 0.56 (0.19)        |

The data shows that `Manichaean People-Elite Framing`, `Crisis-Restoration Narrative`, `Authenticity vs. Political Class`, and `Homogeneous People Construction` were the most consistently high-scoring dimensions. Bolsonaro consistently framed the political landscape as a moral battle, stating in his final address, "The other side is the return of the past, it is corruption, it is lies, it is contempt for the family" (Source: 2018-10-27_Pre-Second-Round_Live.txt).

In contrast, `Economic Populist Appeals` had the lowest mean raw score (M=0.62) and the highest variability (SD=0.17), suggesting it was a more tactical and less central component of his message. `Anti-Pluralist Exclusion` also showed high variability, with a minimum score of 0.3 contrasting with a maximum of 1.0, indicating strategic modulation of this theme.

### 5.3 Advanced Metric Analysis

#### Salience-Weighted Indices
The salience-weighted indices confirm that the populist message was not merely present but was the central focus of the discourse. The **Salience-Weighted Overall Populism Index** had a mean of 0.82. The **Salience-Weighted Core Populism Index** (M=0.85) and **Salience-Weighted Populism Mechanisms Index** (M=0.82) were particularly high, indicating that the foundational elements of populism (the people vs. elite struggle) and the mechanisms for mobilizing support (authenticity, conspiracy) were the most emphasized parts of his rhetoric. The **Salience-Weighted Boundary Distinctions Index** was lower (M=0.73), reflecting the more tactical use of nationalist and economic appeals.

#### Populist Strategic Contradiction Index (PSCI)
The PSCI provides insight into Bolsonaro's rhetorical sophistication. The highest PSCI score (0.18) occurred in the September 6th speech to business leaders. This was driven by high tension between `Popular Sovereignty Claims` and `Anti-Pluralist Exclusion` (Democratic-Authoritarian Tension = 0.18) and between `Homogeneous People Construction` and `Nationalist Exclusion` (Internal-External Focus Tension = 0.21). In this single speech, he appealed to the "people" via referenda—"Let's respect the referendum... which gave us the right to buy weapons and ammunition"—while also delegitimizing opponents—"We can't continue with this porridge duo that I don't like, PT, PSDB" (Source: 2018-09-06_Juiz_de_Fora_Business_Association.txt). This suggests a calculated strategy to project both democratic legitimacy and strongman resolve to a skeptical elite audience.

### 5.4 Interaction and Reliability Analysis

While a full correlation analysis was not possible, the ANOVA results reveal significant interaction effects between specific populist dimensions and the campaign timeline. The statistically significant variance in `Anti-Pluralist Exclusion` (p=0.033) and `Economic Populist Appeals` (p=0.014) across campaign stages demonstrates that these were the primary dimensions Bolsonaro modulated for strategic effect. For instance, the raw score for `Anti-Pluralist Exclusion` dropped from a high of 1.0 in the late-October rally, where he proclaimed of his opponents, "Either they go abroad, or they go to jail!" (Source: 2018-10-22_Avenida_Paulista_Speech.txt), to just 0.3 in the speech on the eve of the first-round vote, indicating a tactical softening of tone.

The reliability analysis for the four Primary Populist Core Anchors yielded a Cronbach's alpha of 0.77. This value suggests that these four dimensions measure a related, underlying construct of "core populism" with acceptable internal consistency, lending construct validity to this central component of the PDAF framework.

### 5.5 Pattern Recognition and Theoretical Insights

The analysis reveals a clear pattern: a stable, intensely populist core surrounded by more flexible, tactical rhetorical modules. The core message, consistent across the campaign, was one of a virtuous, unified Brazilian people (`Homogeneous People Construction`) led by an authentic outsider (`Authenticity vs. Political Class`) in a Manichaean struggle against a corrupt political establishment (`Manichaean People-Elite Framing`) to restore the nation from a state of profound crisis (`Crisis-Restoration Narrative`). This is perfectly encapsulated in his statement: "This movement comes from the root, from the soul of the suffering people who want and will have change" (Source: 2018-09-30_Avenida_Paulista_Speech.txt).

The tactical modules—`Anti-Pluralist Exclusion`, `Nationalist Exclusion`, and `Economic Populist Appeals`—were deployed with greater variability. The suppression of anti-pluralist and economic populist themes just before the first-round vote, followed by their re-intensification, points to a sophisticated understanding of electoral timing. The spike in `Elite Conspiracy` rhetoric post-stabbing is a classic example of a populist leader instrumentalizing a crisis to validate their worldview, portraying personal victimhood as an attack on the people's movement itself.

## 6. Discussion

The findings of this analysis offer significant theoretical and methodological implications. Theoretically, they challenge the simple "intensification" model of populist campaign rhetoric. For Bolsonaro in 2018, populism was not a tool to be gradually dialed up; it was the fundamental operating system of his campaign from day one. The strategic modulation occurred at the level of specific dimensions, not the overall populist posture. This suggests that mature populist campaigns may operate from a high baseline, focusing on tactical adjustments rather than broad escalation.

The high PSCI score in the speech to business leaders is particularly revealing. It suggests that strategic contradiction is not a communicative failure but a feature, potentially used to build a "strange bedfellows" coalition of anti-establishment voters and pro-market elites. By simultaneously invoking popular will and anti-pluralist resolve, Bolsonaro could project both democratic legitimacy and authoritarian capacity, appealing to different segments of his audience with different, and even contradictory, messages.

Methodologically, this study demonstrates the value of the PDAF's granular, salience-weighted approach. A simple binary or single-score populist measurement would have confirmed that Bolsonaro is a populist but missed the crucial dynamics of strategic modulation, the specific impact of the assassination attempt, and the sophisticated use of rhetorical contradiction. The framework's ability to distinguish between intensity and salience, and to quantify tensions, provides a far richer and more accurate picture of how populist discourse functions in practice.

## 7. Conclusion

This computational analysis of Jair Bolsonaro's 2018 campaign discourse provides a nuanced, data-driven portrait of a sophisticated and multi-faceted populist communicator. The research confirms that his campaign was intensely populist from its inception, anchored by a stable core of Manichaean, crisis-driven, and anti-establishment rhetoric. The primary narrative is not one of simple intensification, but of strategic modulation, where specific themes like anti-pluralism and economic appeals were calibrated in response to campaign events and audiences.

The study validates the utility of the PDAF v10.0.2 framework, particularly its novel metrics for salience and strategic tension, in uncovering complex rhetorical strategies that simpler models would miss. The findings suggest that future research on populism should move beyond measuring *if* a leader is populist to analyzing *how* they are populist, focusing on the dynamic interplay of different rhetorical dimensions over time. While limited by its sample size, this analysis provides a robust and replicable foundation for understanding the specific brand of populism that reshaped Brazilian politics.

## 8. Evidence Citations

**Source: 2018-07-22_PSL_Conference_Candidacy_Launch.txt**
*   `Manichaean People-Elite Framing`: "No quartel você tem companheirismo, patriotismo, disciplina, hierarquia, amor à pátria. Na política, não. [...] Mais uma vez, obrigado, Geraldo Alckmin [risadas], por ter unido a escória da política brasileira [aplausos]."
*   `Crisis-Restoration Narrative`: "É o destino dessa grande nação chamada Brasil. [...] algo bateu em mim. Algo calou na minha alma: a reeleição da senhora Dilma Rousseff [uivos]. Terrorista! [...] Nós temos que salvar a nossa juventude para salvarmos o Brasil [gritos de apoio]."
*   `Anti-Pluralist Exclusion`: "Meus irmãos da Marinha, do Exército e da Aeronáutica, vocês serão reconhecidos no meu governo. [...] porque vocês são o último obstáculo para o socialismo. [...] Nós não aceitamos o comunismo."

**Source: 2018-08-23_Aracatuba_Speech_Part_2.txt**
*   `Anti-Pluralist Exclusion`: "Essa bandidagem vai morrer porque não liberaremos recursos da união para eles."
*   `Homogeneous People Construction`: "Somos um só país, uma só pátria, uma só nação, um só coração verde e amarelo."

**Source: 2018-09-06_Juiz_de_Fora_Business_Association.txt**
*   `Economic Populist Appeals`: "O que o Brasil precisa? Precisa de alguém então, que tire o Estado do cangote de quem produz."
*   `Anti-Pluralist Exclusion`: "Não podemos continuar com essa dupla de mingau que eu não gosto, PT, PSDB."
*   `Popular Sovereignty Claims`: "Vamos respeitar o referendo do M5, que nos deu o direito à compra de armas e munições."

**Source: 2018-09-16_Post-Stabbing_Speech.txt**
*   `Elite Conspiracy/Systemic Corruption`: "O PT descobriu o caminho para o poder. O voto eletrônico. [...] Quem aparelhava o TSE, com todo o respeito que eu tenho aos senhores ministros, que não têm conhecimento de informática. [...] Essa possibilidade de fraude no segundo turno, talvez até no primeiro, é concreta."

**Source: 2018-09-30_Avenida_Paulista_Speech.txt**
*   `Authenticity vs. Political Class`: "Esse movimento vem da raiz, vem da alma do povo sofrido que quer e terá a mudança."

**Source: 2018-10-07_Post-First-Round_Speech.txt**
*   `Crisis-Restoration Narrative`: "Mergulhar num país, numa mais profunda crise ética, moral e economica, nunca vista. O nosso país, realmente, esta a beira do caos. Nao podemos dar mais um passo a esquerda. O nosso passo agora, é pro centro-direita."
*   `Elite Conspiracy/Systemic Corruption`: "Eles tem dinheiro, tem um poder economico enorme. Eles tem tambem parte da midia favoravel aos seus propositos."

**Source: 2018-10-22_Avenida_Paulista_Speech.txt**
*   `Anti-Pluralist Exclusion`: "Ou vão pra fora, ou vão pra cadeia!"
*   `Crisis-Restoration Narrative`: "Será uma limpeza nunca vista na história do Brasil."

**Source: 2018-10-27_Pre-Second-Round_Live.txt**
*   `Manichaean People-Elite Framing`: "O outro lado é a volta do passado, é a corrupção, é a mentira, é o desprezo à família, é uma aproximação das ditaduras, entre tantas outra-- tantas outras coisas, todo mundo já sabe aqui que não é o caso, a gente tocar nesse assunto."
*   `Elite Conspiracy/Systemic Corruption`: "O que está em jogo é a perpetuação dessa máquina podre que nós temos aí, que vive da corrupção, pra tirar de vocês o atendimento médico, a educação, a segurança. É uma máquina podre que sobrevive, se retroalimenta da desgraça, da corrupção. O que está em jogo é a corrupção."