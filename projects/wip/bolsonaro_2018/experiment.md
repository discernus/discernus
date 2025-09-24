# Bolsonaro 2018 Populist Discourse Analysis: Replication and Extension Study

## Abstract

This experiment replicates and extends Tamaki & Fuks (2019) analysis of populist discourse in Jair Bolsonaro's 2018 Brazilian presidential campaign speeches using the PDAF v10.0.2 framework. We analyze 13 speeches spanning from candidacy launch (July 22) through pre-second-round (October 27), testing the original study's finding of increasing populist intensity across the campaign while exploring dimensional patterns, strategic tensions, and the interplay between populist, patriotic, and nationalist discourses. The study validates PDAF's cross-cultural applicability by comparing results against Team Populism's holistic grading benchmarks and tests theoretical predictions about populist discourse evolution in Latin American electoral contexts. Expected outcomes include identification of Bolsonaro's unique dimensional populism profile, strategic tension analysis revealing rhetorical sophistication patterns, and temporal evolution mapping showing campaign adaptation strategies, particularly following the September 6 stabbing incident.

## Research Questions

### Replication Questions (from original study)
1. **To what extent is Jair Bolsonaro a populist politician based on his 2018 campaign speeches?** *(Core replication)*
2. **How does Bolsonaro's populist discourse evolve across the campaign timeline?** *(Temporal progression)*
3. **How do patriotic and nationalist elements interact with populist rhetoric in Bolsonaro's speeches?** *(Discourse interaction)*
4. **What is the relationship between electoral proximity and populist intensity?** *(Strategic intensification)*

### Extension Questions (beyond original study)
5. **Which PDAF dimensions are most salient in Bolsonaro's populist discourse and why?** *(Dimensional profiling)*
6. **How does the September 6 stabbing incident affect populist discourse patterns?** *(Crisis impact analysis)*
7. **What strategic tensions emerge between different populist dimensions across campaign phases?** *(Strategic contradiction analysis)*
8. **How do different audience types (business leaders vs. mass rallies) affect populist rhetoric deployment?** *(Audience adaptation)*
9. **What linguistic markers and rhetorical strategies correlate with higher/lower populist scores?** *(Mechanism discovery)*
10. **How does Bolsonaro's populist profile compare to other Latin American populists using PDAF metrics?** *(Comparative positioning)*

## Hypotheses

### Primary Hypotheses (Replicating Original Study)
**H₁**: Bolsonaro's Salience-Weighted Overall Populism Index will average ≥ 0.5 across all campaign speeches (confirming "somewhat populist" classification)
**H₂**: μ_late_campaign > μ_early_campaign on Salience-Weighted Overall Populism Index (populist intensification hypothesis)
**H₃**: Patriotic/nationalist framing will show negative correlation with people-centric populist dimensions (r < -0.3, p < 0.05)

### Secondary Hypotheses (Extending Original Study)
**H₄**: μ_post_stabbing > μ_pre_stabbing on Manichaean People-Elite Framing dimension (crisis amplification effect)
**H₅**: Anti-Pluralist Exclusion and Crisis-Restoration dimensions will show highest salience scores (> 0.7) across speeches
**H₆**: Business audience speeches will score lower on Economic Populist Appeals than mass rally speeches (audience moderation effect)
**H₇**: Populist Strategic Contradiction Index will be highest in October speeches (electoral pressure effect)
**H₈**: Elite Conspiracy dimension will show significant increase after stabbing incident (victimization narrative)

### Temporal Evolution Hypotheses
**H₉**: Linear trend analysis will show significant positive slope for overall populism from July to October (β > 0, p < 0.05)
**H₁₀**: Variance in populist scores will increase in final campaign month (Levene's test, October vs. earlier months)
**H₁₁**: At least 5 of 9 PDAF dimensions will show significant differences between campaign_stage groups (ANOVA)

### Dimensional Pattern Hypotheses
**H₁₂**: Core populist dimensions (People-Elite, Crisis-Restoration, Popular Sovereignty, Anti-Pluralist) will show higher internal consistency (Cronbach's α > 0.8) than auxiliary dimensions
**H₁₃**: Nationalist Exclusion will correlate positively with Anti-Pluralist Exclusion (r > 0.5, p < 0.05)
**H₁₄**: Economic Populist Appeals will show lowest salience in business/policy speeches (< 0.3)

### Statistical Testing Strategy
- **Trend Analysis**: Linear regression on temporal progression of Salience-Weighted Overall Populism Index
- **Phase Comparison**: Paired t-tests comparing early vs. late campaign, pre vs. post-stabbing
- **Dimensional Analysis**: ANOVA across 9 PDAF dimensions, post-hoc Tukey HSD
- **Audience Effects**: Independent t-tests between audience types on relevant dimensions
- **Correlation Analysis**: Pearson correlations between dimensions and with temporal/contextual variables
- **Reliability Testing**: Cronbach's alpha for dimensional consistency
- **Effect Sizes**: Cohen's d for all significant comparisons, η² for ANOVA effects
- **Strategic Tension**: Calculate Populist Strategic Contradiction Index for each speech

## Expected Outcomes

This experiment will produce empirical validation of the original study's findings while providing deeper dimensional analysis through PDAF's comprehensive framework. Expected outcomes include:

1. **Replication Confirmation**: Validation of 0.5 average populist score and temporal intensification pattern
2. **Dimensional Profile**: Identification of Bolsonaro's unique populist signature across 9 dimensions
3. **Crisis Impact**: Quantification of stabbing incident's effect on populist discourse deployment
4. **Strategic Evolution**: Mapping of rhetorical adaptation strategies across campaign phases
5. **Audience Calibration**: Evidence of strategic discourse modulation based on audience type
6. **Comparative Positioning**: Contextualization within Latin American populist discourse patterns

## Data Grouping and Custom Variable Mapping

### Corpus Metadata Integration
All statistical grouping uses metadata fields directly from the corpus manifest:
- **Primary Temporal Field**: `campaign_stage` - Pre-assigned for temporal analysis
- **Crisis Marker**: `political_phase` - Includes "post_assassination" marker
- **Audience Type**: `audience` - Categorizes target audience for each speech
- **Speech Type**: `speech_type` - Distinguishes campaign speeches from policy/personal statements

### Statistical Grouping Structure

**Campaign Stage Groups** (using `campaign_stage` field):
- **"early_campaign"**: July 22 speech (n=1, baseline reference)
- **"mid_campaign"**: August 23-31, September 6 speeches (n=4)
- **"campaign_interruption"**: September 16 post-stabbing (n=1, special case)
- **"late_campaign"**: September 30 speech (n=1)
- **"final_campaign"**: October 6 speech (n=1)
- **"election_day"**: October 7 morning speech (n=1)
- **"post_first_round"**: October 7 evening, October 16 speeches (n=2)
- **"pre_second_round"**: October 22, 27 speeches (n=2)

**Pre/Post Stabbing Groups** (derived from date field):
- **"pre_stabbing"**: Speeches before September 6, 2018 (n=4)
- **"post_stabbing"**: Speeches from September 16 onward (n=9)

**Audience Type Groups** (using `audience` field):
- **"mass_public"**: Mass rallies and public events (n=5)
- **"business_leaders"**: Business association speech (n=1, baseline)
- **"online_supporters"**: Facebook live broadcasts (n=3)
- **"national_audience"**: Broad national appeals (n=4)

**Electoral Proximity Groups** (derived from date field):
- **"distant"**: July-August speeches, >30 days before election (n=3)
- **"approaching"**: September speeches, 7-30 days before (n=3)
- **"imminent"**: October 1-6 speeches, <7 days before first round (n=1)
- **"inter_round"**: October 7-21, between rounds (n=3)
- **"final_push"**: October 22-27, before second round (n=2)

### Statistical Analysis Parameters
- **Primary Analysis Variable**: `campaign_stage` with 8 distinct phases
- **Secondary Variables**: `audience`, `political_phase`, `speech_type`
- **Temporal Variable**: Date field for trend analysis
- **Crisis Marker**: September 6, 2018 as inflection point
- **Compliance**: All variables directly from corpus manifest per v10.0 specification

## Significance

This experiment represents the first PDAF v10.0.2 analysis of Brazilian populist discourse, providing both validation of existing scholarship and new insights through dimensional analysis. The study's significance includes:

1. **Methodological Bridge**: Connecting Team Populism's holistic grading with PDAF's dimensional framework
2. **Latin American Context**: Testing PDAF's applicability to Brazilian Portuguese political discourse
3. **Crisis Response Analysis**: Unique natural experiment via stabbing incident's impact on populist rhetoric
4. **Temporal Granularity**: Dense sampling across campaign timeline reveals strategic evolution
5. **Theoretical Contribution**: Evidence on populism-patriotism-nationalism interaction in non-Western contexts
6. **Comparative Baseline**: Establishing Brazilian populist discourse patterns for cross-national comparison

The comprehensive dimensional analysis (9 PDAF dimensions × 13 speeches) combined with rich contextual metadata enables sophisticated hypothesis testing while maintaining replication fidelity to the original study's core findings.

```yaml
# --- Start of Machine-Readable Appendix ---

# Metadata (Required)
metadata:
  experiment_name: "bolsonaro_2018_populist_discourse_analysis"
  author: "Discernus Project"
  spec_version: "10.0"

# Components (Required)
components:
  # The filename of the v10.0 Framework file.
  # Must be in the same directory as this experiment.md.
  framework: "pdaf_v10_0_2.md"

  # The filename of the v8.0 compliant Corpus manifest file.
  # Must be in the same directory as this experiment.md.
  corpus: "corpus.md"

# --- End of Machine-Readable Appendix ---
```

