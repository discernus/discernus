Executive Summary

Objective: Assess whether the Civic Analysis Framework (CAF) v7.3 can (1) differentiate speakers using 10 civic character dimensions, (2) reveal distinct character signatures across five virtues and five vices, and (3) demonstrate meaningful variation in character coherence (via indices derived from CAF formulas). Using only the attached framework specifications and the provided evidence, we analyze eight political speeches and report statistical and qualitative findings.

Key Findings:
- The pipeline successfully computed all derived metrics with 100% success (statistical_results.csv: task_01_calculate_derived_metrics.success = True), producing valid tensions, indices, and no missing data (task_02_validate_calculated_metrics: total_missing = 0).
- Descriptive statistics show substantial variance across dimensions (e.g., justice_score SD = 0.217; resentment_score SD = 0.237; hope_score SD = 0.238), supporting the potential to differentiate speakers.
- Individual civic character indices (unweighted) ranged from 0.420 to 0.805; salience-weighted indices ranged from 0.418 to 0.808, indicating wide dispersion in overall civic character profiles.
- Hypothesis H1 (speaker differentiation) is supported descriptively but limited inferentially: the ANOVA result logged as NaN with p ≥ 0.05 for civic_character_index (task_06_character_coherence_analysis_H3), suggesting no confirmed statistical difference on that single composite metric, though dimension-level ANOVAs are not reported.
- Hypothesis H2 (character signatures) is supported: distinct virtue/vice configurations are observable across speakers in scores.csv and evidence quotes.
- Hypothesis H3 (coherence variation) is partially supported via dispersion in civic_character_index (SD ≈ 0.122 unweighted; ≈ 0.123 salience-weighted), but no valid ANOVA statistic was produced in the log for coherence; still, the spread indicates meaningful variation.
- Fit assessment: CAF v7.3 explains variance in the corpus reasonably well at the descriptive level: multiple dimensions show wide ranges and nontrivial standard deviations; derived indices distribute sensibly. Inferential fit is constrained by limited sample size (n = 8) and at least one incomplete ANOVA result.

Framework Explanation and Purpose

Framework: Civic Analysis Framework (CAF) v7.3 (caf_v7.3.md)
Purpose: Provide a systematic, virtue-ethics–aligned assessment of the civic character of political discourse by modeling tensions between five civic virtues (dignity, truth, justice, hope, pragmatism) and five pathological counterparts (tribalism, manipulation, resentment, fear, fantasy). CAF defines:
- Dimensions and semantic markers for each virtue/vice
- A sequential analysis methodology
- Salience weighting to reflect contextual centrality
- Tension metrics for each axis and composite indices:
  - Tension scores per axis (e.g., truth-manipulation tension)
  - Civic Character Index (CCI)
  - Salience-Weighted CCI
  - Virtue and Pathology indices

CAF emphasizes evidence-based scoring with explicit quotes, numerical scores (0.0–1.0), salience, and confidence, enabling inter-rater reliability and construct validity checks.

Corpus Evaluated

Eight speeches spanning eras and ideological positions (experiment.md, methodology/corpus list; scores.csv document_id):
- John Lewis (1963) – March on Washington speech: john_lewis_1963_march_on_washington.txt
- John McCain (2008) – Concession speech: john_mccain_2008_concession.txt
- Mitt Romney (2020) – Impeachment speech: mitt_romney_2020_impeachment.txt
- Cory Booker (2018) – First Step Act speech: cory_booker_2018_first_step_act.txt
- Bernie Sanders (2025) – Fighting oligarchy: bernie_sanders_2025_fighting_oligarchy.txt
- Alexandria Ocasio-Cortez (2025) – Fighting oligarchy: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt
- JD Vance (2022) – NatCon conference: jd_vance_2022_natcon_conference.txt
- Steve King (2017) – House floor remarks: steve_king_2017_house_floor.txt

The dataset includes:
- Evidence quotations per dimension (evidence.csv)
- Structured scores with salience and confidence (scores.csv)
- Derived metrics and validation outputs (statistical_results.csv)

Methodology Overview

- Scoring: Each speech was scored along 10 dimensions with salience and confidence, extracted “via gasket” (scores.csv). Evidence quotes are linked to each document, dimension, and score (evidence.csv).
- Derived Metrics: CAF v7.3 formulas computed five axis tensions, Civic Character Index, Salience-Weighted CCI, Virtue Index, and Pathology Index (statistical_results.csv, task_01_calculate_derived_metrics.calculated_metrics).
- Validation: Missing-data and range checks passed (task_02), with sensible variance in scores and indices (task_03 descriptive stats).
- Inferential Analyses: One ANOVA result is logged for civic_character_index with NaN statistic and p ≥ 0.05 (task_06). No other dimension-level ANOVA outputs are present.

Quantitative Results

From statistical_results.csv task_01 (derived metrics), the per-speech results are:

Dignity-Tribalism Tension:
- [0.575, 0.625, 0.725, 0.600, 0.650, 0.850, 0.600, 0.550]
Range 0.55–0.85; mean ≈ 0.647

Truth-Manipulation Tension:
- [0.400, 0.575, 0.725, 0.650, 0.550, 0.750, 0.550, 0.250]
Range 0.25–0.75; mean ≈ 0.556

Justice-Resentment Tension:
- [0.650, 0.575, 0.825, 0.550, 0.650, 0.750, 0.725, 0.450]
Range 0.45–0.825; mean ≈ 0.647

Hope-Fear Tension:
- [0.650, 0.550, 0.825, 0.775, 0.600, 0.850, 0.675, 0.350]
Range 0.35–0.85; mean ≈ 0.659

Pragmatism-Fantasy Tension:
- [0.525, 0.775, 0.825, 0.650, 0.550, 0.825, 0.675, 0.500]
Range 0.50–0.825; mean ≈ 0.666

Indices:
- Virtue Index: [0.55, 0.70, 0.77, 0.52, 0.60, 0.74, 0.50, 0.34] (range 0.34–0.77; mean 0.59)
- Pathology Index: [0.43, 0.46, 0.20, 0.23, 0.40, 0.13, 0.21, 0.50] (range 0.13–0.50; mean 0.32)
- Civic Character Index (CCI): [0.560, 0.620, 0.785, 0.645, 0.600, 0.805, 0.645, 0.420]
- Salience-Weighted CCI: [0.567, 0.625, 0.786, 0.661, 0.610, 0.808, 0.647, 0.418]

Descriptive statistics (task_03):
- CCI mean 0.635, SD 0.122; SW-CCI mean 0.640, SD 0.123.
- Dimension SDs indicate meaningful variance: justice_score SD 0.217; resentment_score SD 0.237; hope_score SD 0.238; truth_score SD 0.179; manipulation_score SD 0.179; pragmatism_score SD 0.213.

Speaker-Level Profiles and Evidence Support

Below are succinct character signatures using scores.csv values and evidence.csv quotes with references. Quotes are included to substantiate dimension scoring, with explicit document references.

1) Alexandria Ocasio-Cortez (alexandria_ocasio_cortez_2025_fighting_oligarchy.txt)
- Signature: Elevated dignity (0.80) and justice (0.75) with moderate manipulation (0.60) and notable tribalism (0.65). CCI ≈ 0.560; SW-CCI ≈ 0.567.
- Evidence:
  - Dignity: “Our lives deserve dignity and our work deserves respect.” (evidence.csv; document_id: alexandria_ocasio_cortez_2025_fighting_oligarchy.txt)
  - Tribalism: “They specialize in getting us to turn on one another…” (same doc)
  - Justice: “...choosing and voting for Democrats... who know how to stand for the working class.” (same doc)
  - Manipulation: “They throw out every label and judgment... to keep us distracted...” (same doc)
  - Hope: “...I want to tell you that you do. You do.” (same doc)

2) Bernie Sanders (bernie_sanders_2025_fighting_oligarchy.txt)
- Signature: Strong justice (0.80), high pragmatism (0.75), lower pathology (pathology index 0.46 with manipulation 0.55, tribalism 0.60, resentment 0.65). CCI ≈ 0.620; SW-CCI ≈ 0.625.
- Evidence:
  - Truth: “...despite a huge increase in worker productivity over the last 52 years... real ... wages ... lower...” (evidence.csv; document_id: bernie_sanders_2025_fighting_oligarchy.txt)
  - Justice: “They are prepared to destroy Social Security, Medicare...” (same doc)
  - Manipulation marker present (emotional trigger framing): “...the worst and most dangerous addiction we have is the greed of the oligarchs.” (same doc)
  - Hope: “If we stand together... we can create the kind of nation that we deserve.” (same doc)

3) Cory Booker (cory_booker_2018_first_step_act.txt)
- Signature: High justice (0.85) and hope (0.80), strong pragmatism (0.75), low pathology (0.20). Highest overall coherence among top tier: CCI ≈ 0.785; SW-CCI ≈ 0.786.
- Evidence:
  - Justice/policy: “...end the use of juvenile solitary confinement...” and “...ensure incarcerated women have access to free sanitary products...” (evidence.csv; document_id: cory_booker_2018_first_step_act.txt)
  - Truth: “...federal prison population has exploded by eight hundred percent...” (same doc)
  - Hope: “...bipartisan compromise bill... ways to make this system more fair.” (same doc)
  - Pragmatism: “This legislation is a product of compromise... just one step in the right direction...” (same doc)

4) JD Vance (jd_vance_2022_natcon_conference.txt)
- Signature: Moderate dignity (0.70) and hope (0.70), mid tribalism (0.50) and manipulation (0.30), pragmatism moderate (0.40). CCI ≈ 0.645; SW-CCI ≈ 0.661.
- Evidence:
  - Dignity/party progress framing: “...we're starting to win the debate within our own party.” (evidence.csv; document_id: jd_vance_2022_natcon_conference.txt)
  - Tribalism/immigration framing: “...thanks to Joe Biden's open border policies...” (same doc)
  - Hope/leadership: “...the leader of the Republican party is a guy who actually plans to put American citizens first...” (same doc)
  - Pragmatism/industrial policy critique: “We should also not let the Chineses make all of our stuff...” (same doc)

5) John Lewis (john_lewis_1963_march_on_washington.txt)
- Signature: Strong justice (0.80) with significant hope (0.70) and moderate resentment (0.50). CCI ≈ 0.600; SW-CCI ≈ 0.610.
- Evidence:
  - Justice: “We must have legislation that will protect the Mississippi sharecropper...” (evidence.csv; document_id: john_lewis_1963_march_on_washington.txt)
  - Justice: “We need a bill to ensure the equality of a maid who earns five dollars a week...” (same doc)
  - Hope: “We want our freedom and we want it now!” (same doc)
  - Resentment/grievance: “We are tired!... of being beaten by policemen.” (same doc)

6) John McCain (john_mccain_2008_concession.txt)
- Signature: Highest composite civic character among all eight (CCI ≈ 0.805; SW-CCI ≈ 0.808), with high dignity (0.85), hope (0.80), pragmatism (0.75), minimal vices (pathology index ≈ 0.13).
- Evidence:
  - Dignity/respect for mandate: “The American people have spoken, and they have spoken clearly.” (evidence.csv; document_id: john_mccain_2008_concession.txt)
  - Truth/acknowledgment of opponent: “Senator Obama has achieved a great thing...” (same doc)
  - Hope/aspirational unity: “Let there be no reason now for any American to fail to cherish their citizenship...” (same doc)
  - Pragmatism/compromise: “...find the necessary compromises to bridge our differences...” (same doc)

7) Mitt Romney (mitt_romney_2020_impeachment.txt)
- Signature: Process-centered justice (0.55) and truth (0.45), moderate pragmatism (0.50), low dignity score (0.40) relative to peers; mid-pathology index (0.21). CCI ≈ 0.645; SW-CCI ≈ 0.647.
- Evidence:
  - Justice/oath: “As a senator-juror, I swore an oath before God to exercise impartial justice.” (evidence.csv; document_id: mitt_romney_2020_impeachment.txt)
  - Truth/seriousness: “The allegations... are very serious.” (same doc)
  - Hope/future accountability: “...I will tell my children... that I did my duty...” (same doc)
  - Pragmatism/process: “The verdict is ours to render under our Constitution.” (same doc)

8) Steve King (steve_king_2017_house_floor.txt)
- Signature: Lower civic character overall (CCI ≈ 0.420; SW-CCI ≈ 0.418) with higher manipulation (0.70), resentment (0.60), tribalism (0.50), and lower hope (0.10).
- Evidence:
  - Tribalism/framing judiciary: “...a lame duck President who has made appointments... who seem to believe that the Constitution means what they want it to mean...” (evidence.csv; document_id: steve_king_2017_house_floor.txt)
  - Manipulation/judicial intent: “A Supreme Court writing law.” (same doc)
  - Resentment/immigration grievance: “...thousands of Americans that are dead at the hands of the criminal aliens...” (same doc)
  - Fear: “This is an infuriating topic... keep the families of these victims in their prayers...” (same doc)

Direct Evaluation of Hypotheses

H1: The 10 CAF dimensions will show statistically significant differences between speakers.
- Evidence for/against:
  - Descriptive variance is strong across many dimensions (task_03): e.g., resentment_score SD = 0.237 with min 0.10 to max 0.65; justice_score SD = 0.217; hope_score SD = 0.238; truth_score SD = 0.179; manipulation_score SD = 0.179.
  - Derived tensions and indices disperse meaningfully (e.g., SW-CCI min 0.418 to max 0.808).
  - However, inferential testing is incomplete: task_06 (one-way ANOVA for civic_character_index) reports NaN statistic and p ≥ 0.05. No ANOVAs for the individual 10 dimensions are reported in the logs provided.
- Conclusion: Partially supported descriptively; not confirmed inferentially on the composite metric in the provided results. Additional dimension-level ANOVAs would be necessary to validate H1 statistically.

H2: Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices.
- Evidence:
  - Clear signature differentiation in scores and quotes:
    - McCain: High dignity, hope, pragmatism; minimal vices; unifying concession statements (john_mccain_2008_concession.txt).
    - Booker: High justice and pragmatism with concrete policy steps; bipartisan, incremental framing (cory_booker_2018_first_step_act.txt).
    - King: Elevated manipulation/resentment/tribalism; fear-oriented framing (steve_king_2017_house_floor.txt).
    - AOC and Sanders: Justice-forward with populist framing, some tribal/manipulative elements, hope appeals (respective 2025 speeches).
    - Romney: Duty/process/justice-centric with measured hope; lower dignity score in this scoring set but strong process language (mitt_romney_2020_impeachment.txt).
    - Lewis: Rights-protection urgency; justice and hope with grievance statements reflecting 1963 context (john_lewis_1963_march_on_washington.txt).
    - Vance: Party identity cues, immigration-centric tribal framing, industrial policy critique, progress/hope inside the movement (jd_vance_2022_natcon_conference.txt).
- Conclusion: Supported. Distinct signatures are evident across multiple dimensions and substantiated by document-specific quotations.

H3: MC-SCI scores will vary meaningfully between speakers, indicating different levels of character coherence.
- Note: MC-SCI is referenced in experiment.md (CAF v7.1/MC-SCI), but the provided calculations are CAF v7.3 tensions and indices. The outputs include civic_character_index and salience-weighted CCI, but no explicit MC-SCI column is present in scores.csv/statistical_results.csv. Nonetheless, coherence can be proxied by CCI/SW-CCI dispersion.
- Evidence:
  - CCI ranges from 0.420 (King) to 0.805 (McCain); SW-CCI from 0.418 to 0.808; SD ≈ 0.122–0.123. This indicates meaningful variation in composite coherence-like indices across speeches.
  - task_06 lists an ANOVA for civic_character_index with NaN statistic and p ≥ 0.05, preventing an inferential claim on group differences for coherence.
- Conclusion: Partially supported. There is clear variation in coherence-like indices across speakers, but the statistical test recorded does not establish significance. If MC-SCI is distinct from CCI, it was not output here; thus, we infer coherence variation descriptively.

Qualitative Insights: High vs. Low Coherence Profiles

- Highest composite coherence: John McCain (SW-CCI ≈ 0.808). Characterized by strong dignity, truthfulness in acknowledging the opponent, constructive hope, and explicit calls for pragmatic compromise. Quotes include:
  - “The American people have spoken, and they have spoken clearly.” (john_mccain_2008_concession.txt)
  - “...offer[ing] our next president our good will and earnest effort to find ways to come together...” (same doc)
  These align with high tension scores across identity, truth, hope, and pragmatism axes.

- Lowest composite coherence: Steve King (SW-CCI ≈ 0.418). Characterized by elevated tribalism, manipulation, resentment, and fear.
  - “A Supreme Court writing law.” (steve_king_2017_house_floor.txt)
  - “...thousands of Americans that are dead at the hands of the criminal aliens...” (same doc)
  The rhetoric centralizes grievance and threat, lowering tensions and indices.

Framework Validation and Reliability

- Technical execution: Successful derived metrics computation for all eight speeches (task_01 success = True), zero missing data (task_02).
- Range and variance: All core dimensions show plausible ranges (task_02 range_check) and variation (task_03), avoiding clustering at 0.5 and supporting construct sensitivity.
- Evidence anchoring: Each dimension in evidence.csv includes at least one supporting quotation tied to a document_id and reasoning label (e.g., “policy_proposal,” “emotional_triggers,” “fact_based_argument”).
- Salience weighting: SW-CCI tracks CCI closely but refines rankings where salience differs (e.g., JD Vance’s SW-CCI exceeds his unweighted CCI), indicating value added by salience modeling.

Quantitative Assessment of Framework Fit to the Corpus

- Variance explained (descriptive): CAF v7.3 produces wide, interpretable dispersion across all axes and indices, matching expectations for heterogeneous political discourse. Standard deviations are nontrivial (e.g., hope_score SD 0.238; justice_score SD 0.217; CCI SD 0.122), indicating that the framework captures meaningful variance.
- Coherence of derived measures: Tension formulas yield sensible ranges and rank-orderings consistent with the qualitative content of speeches (e.g., McCain > Booker > Vance ≈ Romney > Lewis ≈ Sanders ≈ AOC > King on CCI/SW-CCI).
- Inferential constraints: The only logged ANOVA (on CCI) returned NaN and p ≥ 0.05, so formal variance-explanation claims cannot be made from inferential outputs provided. With n = 8, statistical power is limited; dimension-level ANOVAs are not present in the logs.
- Overall fit judgment: Reasonably good descriptive fit. CAF v7.3 explains variance across this corpus in a face-valid and quantitatively differentiated manner. Strict statistical confirmation of between-speaker differences is inconclusive given the provided ANOVA result.

Statistical Methodology and Results (As Provided)

- Derived metrics: Computed per CAF formulas for all eight speeches; success rate 1.0 (task_01).
- Metric validation: Missing-data check and range-check passed (task_02).
- Descriptive statistics: Reported for all primary scores and indices (task_03).
- ANOVA: One entry for coherence proxy (civic_character_index) shows F_statistic = NaN, p_value = NaN with interpretation “p ≥ 0.05” (task_06), indicating no evidence of significant group differences based on that specific run/result.

Limitations

- Sample size: n = 8 is small for robust inferential testing; power is likely insufficient.
- Missing inferential breadth: Only one ANOVA entry (for CCI) is provided; dimension-level ANOVAs and effect sizes are not present in the results.
- MC-SCI availability: Although the experiment design references MC-SCI, the outputs do not include an explicit MC-SCI variable; coherence is assessed via CCI/SW-CCI proxies.
- Temporal and ideological heterogeneity: The corpus spans decades and diverse political contexts, which can complicate direct statistical comparisons without additional controls.

Recommendations for Future Work

- Run ANOVAs (or mixed models) per dimension to test H1 comprehensively; report p-values and effect sizes (η²).
- Ensure MC-SCI is computed and logged explicitly if it is the designated coherence metric.
- Increase sample size per speaker or across more speeches to improve power and enable within-speaker variance estimates.
- Conduct salience-weighted hypothesis tests to evaluate whether weighting alters between-speaker differentiation.

Conclusion

Using only the supplied assets, CAF v7.3 demonstrates strong descriptive sensitivity to differences in civic character across eight political speeches, yielding distinct character signatures supported by document-specific quotations. Composite civic character indices vary widely (SW-CCI 0.418–0.808), aligning with qualitative expectations. While descriptive evidence supports H1–H3 in spirit, inferential confirmation is limited by the provided ANOVA result (NaN; p ≥ 0.05 for CCI) and the absence of dimension-level tests and explicit MC-SCI outputs. Overall, CAF v7.3 appears to be a good descriptive fit for this corpus, explaining variance in a coherent, interpretable manner; formal statistical confirmation of speaker differentiation awaits additional tests.

Appendix: Selected Evidence Quotations and References

- Alexandria Ocasio-Cortez:
  - “Our lives deserve dignity and our work deserves respect.” (evidence.csv; alexandria_ocasio_cortez_2025_fighting_oligarchy.txt)
  - “They specialize in getting us to turn on one another...” (same doc)
  - “...voting for Democrats... who know how to stand for the working class.” (same doc)
  - “They throw out every label and judgment... to keep us distracted...” (same doc)
  - “...I want to tell you that you do. You do.” (same doc)

- Bernie Sanders:
  - “...despite a huge increase in worker productivity... real ... wages today are lower...” (evidence.csv; bernie_sanders_2025_fighting_oligarchy.txt)
  - “They are prepared to destroy Social Security, Medicare...” (same doc)
  - “...the worst and most dangerous addiction... is the greed of the oligarchs.” (same doc)
  - “If we stand together... we can create the kind of nation that we deserve.” (same doc)

- Cory Booker:
  - “...end the use of juvenile solitary confinement...” (evidence.csv; cory_booker_2018_first_step_act.txt)
  - “...ensure incarcerated women have access to free sanitary products...” (same doc)
  - “...federal prison population has exploded by eight hundred percent...” (same doc)
  - “This legislation is a product of compromise... just one step in the right direction...” (same doc)

- JD Vance:
  - “...thanks to Joe Biden's open border policies...” (evidence.csv; jd_vance_2022_natcon_conference.txt)
  - “...places... with the highest immigration rates are the places with the highest home prices.” (same doc)
  - “...the leader of the Republican party is a guy who actually plans to put American citizens first...” (same doc)
  - “We should also not let the Chineses make all of our stuff.” (same doc)

- John Lewis:
  - “We must have legislation that will protect the Mississippi sharecropper...” (evidence.csv; john_lewis_1963_march_on_washington.txt)
  - “We need a bill to ensure the equality of a maid...” (same doc)
  - “We want our freedom and we want it now!” (same doc)
  - “We are tired!... of being beaten by policemen.” (same doc)

- John McCain:
  - “The American people have spoken, and they have spoken clearly.” (evidence.csv; john_mccain_2008_concession.txt)
  - “Senator Obama has achieved a great thing...” (same doc)
  - “Let there be no reason now for any American to fail to cherish their citizenship...” (same doc)
  - “...find the necessary compromises to bridge our differences...” (same doc)

- Mitt Romney:
  - “As a senator-juror, I swore an oath before God to exercise impartial justice.” (evidence.csv; mitt_romney_2020_impeachment.txt)
  - “The allegations... are very serious.” (same doc)
  - “...I will tell my children and their children that I did my duty...” (same doc)
  - “The verdict is ours to render under our Constitution.” (same doc)

- Steve King:
  - “...lame duck President... appointments to the Supreme Court... the Constitution means what they want it to mean...” (evidence.csv; steve_king_2017_house_floor.txt)
  - “A Supreme Court writing law.” (same doc)
  - “...thousands of Americans that are dead at the hands of the criminal aliens...” (same doc)
  - “...keep the families of these victims in their prayers...” (same doc)

Sources
[1] caf_v7.3.md https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7692671/565a8618-4ddb-459c-8b26-015da8ef2134/caf_v7.3.md
[2] evidence.csv https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7692671/82753191-f2ed-46e8-9b74-f6409fa298fe/evidence.csv
[3] experiment.md https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7692671/312d3185-43d7-4039-ad2a-70af0deb0b33/experiment.md
[4] scores.csv https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7692671/77a2f18f-d940-457a-a150-ff78f239a51d/scores.csv
[5] statistical_results.csv https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/7692671/502b0b2e-1c07-4e7c-9828-4f56392b56c3/statistical_results.csv
