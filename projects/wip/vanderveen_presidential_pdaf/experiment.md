# Van der Veen Presidential Campaign Replication Study

## Abstract

This experiment analyzes populist discourse patterns in 2016 presidential campaign speeches using the PDAF v10.0 framework. We examine 56 speeches from 6 major candidates (Trump, Clinton, Sanders, Cruz, Rubio, Kasich) across four campaign phases to test specific hypotheses about populist rhetoric variation by candidate, party, and temporal context. The study validates PDAF's analytical capabilities by comparing results against established human coding benchmarks and tests theoretical predictions about populist discourse patterns in American electoral politics. Expected outcomes include identification of dimensional populism profiles for each candidate, strategic tension analysis revealing rhetorical sophistication, and temporal evolution patterns showing campaign adaptation strategies.

## Research Questions

1. **What patterns emerge in populist discourse across 2016 presidential candidates?** *(Open-ended pattern discovery)*
2. **Which PDAF dimensions show the most variation across candidates and why?** *(Dimensional exploration)*
3. **How do different campaign phases (primary vs. general) affect populist rhetoric intensity?** *(Context effects analysis)*
4. **What rhetorical strategies and linguistic patterns correlate with higher/lower populist scores?** *(Mechanism discovery)*
5. **Are there unexpected populist patterns, outliers, or strategic contradictions that warrant further investigation?** *(Anomaly detection)*
6. **How do strategic tension patterns reveal candidate positioning sophistication?** *(Strategic analysis)*

## Hypotheses

### Primary Hypothesis

**H₀**: μ_trump = μ_clinton = μ_sanders = μ_cruz = μ_rubio = μ_kasich (All candidates have equal Salience-Weighted Overall Populism Index scores)
**H₁**: At least one candidate differs significantly from the others in Salience-Weighted Overall Populism Index scores

**Test**: One-way ANOVA across 6 presidential candidates (Trump, Clinton, Sanders, Cruz, Rubio, Kasich)
**Threshold**: p < 0.05, F > F_critical

### Secondary Hypotheses

**H₂**: μ_trump > μ_clinton on Salience-Weighted Overall Populism Index (Trump scores significantly higher than Clinton)
**H₃**: μ_sanders > μ_clinton on Salience-Weighted Overall Populism Index (Sanders scores significantly higher than Clinton)
**H₄**: μ_trump > μ_rubio, μ_kasich on Salience-Weighted Overall Populism Index (Trump scores significantly higher than establishment Republicans)
**H₅**: μ_republican > μ_democratic on Nationalist Exclusion dimension (Republicans higher on nationalist populism)
**H₆**: μ_democratic > μ_republican on Economic Populist Appeals dimension (Democrats higher on economic populism)

### Temporal and Strategic Hypotheses

**H₇**: μ_general_election > μ_early_primary on Manichaean People-Elite Framing dimension (Intensification across campaign)
**H₈**: Populist Strategic Contradiction Index (PSCI) correlates negatively with `electoral_success` field values (ρ < -0.3, p < 0.05) using Spearman's rank correlation
**H₉**: Trump shows significantly higher variance in Salience-Weighted Overall Populism Index than other candidates (descriptive analysis)
**H₁₀**: At least 4 of the 9 PDAF dimensions show significant differences between `candidate_type: "outsider"` and `candidate_type: "establishment"` groups

### Statistical Testing Strategy

**Primary Candidate Analysis:**
- **Kruskal-Wallis Test**: Non-parametric alternative to ANOVA for comparing Salience-Weighted Overall Populism Index across 6 candidates (H₁)
- **Dunn's Post-hoc Tests**: Multiple comparison corrections for pairwise candidate comparisons (H₂-H₄)
- **Effect Size**: η² for Kruskal-Wallis, Cohen's d for pairwise comparisons

**Party and Group Comparisons:**
- **Mann-Whitney U Tests**: Non-parametric tests for party differences on Nationalist Exclusion and Economic Populist Appeals (H₅-H₆)
- **Mann-Whitney U Tests**: Outsider vs. establishment comparisons on all 9 PDAF dimensions (H₁₀)

**Temporal Analysis:**
- **Independent t-tests**: Compare early primary vs. general election phases on Manichaean People-Elite Framing (H₇)
- **Spearman's Rank Correlation**: Between campaign phase progression and populism intensity

**Strategic Analysis:**
- **Spearman's Rank Correlation**: Between Populist Strategic Contradiction Index and electoral success (H₈) - appropriate for ordinal data
- **Kendall's Tau**: Alternative rank correlation for robustness

**Descriptive and Exploratory Analysis:**
- **Effect Size**: Cohen's d for all comparisons, η² for Kruskal-Wallis
- **Reliability**: Cronbach's alpha for each dimension across candidates
- **Descriptive Statistics**: Mean, median, IQR for all dimensions by candidate/group
- **Visualization**: Box plots, violin plots, and heatmaps for pattern identification

## Expected Outcomes

This experiment will produce empirical findings on populist discourse differences across candidates, party effects, temporal evolution, and strategic sophistication. The analysis will include non-parametric tests (Kruskal-Wallis, Mann-Whitney U), rank correlations (Spearman's, Kendall's), effect size measurement, candidate comparison, and comprehensive descriptive analysis with visualizations.

## Data Grouping and Custom Variable Mapping

### Corpus Metadata Integration

All statistical grouping uses metadata fields directly from the corpus manifest:

- **Primary Field**: `candidate_short` - Pre-assigned in corpus manifest for each document
- **Secondary Fields**: `party`, `campaign_phase`, `speech_type` - All from corpus manifest metadata
- **Data Integrity**: No filename parsing or speaker name mapping required

### Statistical Grouping Structure

The corpus contains the following candidate groups:

- **Trump** (n=21): Republican nominee, outsider candidate
- **Clinton** (n=21): Democratic nominee, establishment candidate
- **Sanders** (n=5): Democratic primary challenger, progressive populist
- **Cruz** (n=3): Republican primary challenger, conservative populist
- **Rubio** (n=4): Republican establishment candidate
- **Kasich** (n=2): Republican moderate, treated as baseline reference

### Custom Analytical Groupings (Direct Corpus Fields)

**Candidate Type Groups** (using `candidate_type` field from corpus manifest):

- **"outsider"**: Trump (n=22), Sanders (n=5) - Anti-establishment positioning
- **"establishment"**: Clinton (n=21), Rubio (n=4), Kasich (n=2) - Institutional experience
- **"challenger"**: Cruz (n=3) - Establishment challenger with populist appeals

**Electoral Success Groups** (using `electoral_success` field from corpus manifest):

- **Score 3**: Trump (n=22), Clinton (n=21) - General election nominees
- **Score 2**: Sanders (n=5), Cruz (n=3) - Significant primary performance
- **Score 1**: Rubio (n=4), Kasich (n=2) - Early primary exit

**Note**: All grouping variables (`candidate_type`, `electoral_success`) are explicitly defined in the corpus manifest metadata for every document, ensuring coherence validation compliance.

### Statistical Analysis Parameters

- **Primary Analysis Variable**: `candidate_short` (directly from corpus manifest)
- **ANOVA Groups**: 6 candidates with varying n (Trump=21, Clinton=21, Sanders=5, Cruz=3, Rubio=4, Kasich=2)
- **Party Comparison**: Republican (n=30) vs. Democratic (n=26) speeches
- **Temporal Groups**: 4 campaign phases with speeches distributed across all candidates
- **Compliance**: Follows Experiment Specification v10.0 corpus metadata linkage requirements

This approach ensures all statistical agents use the same, unambiguous grouping data directly from the corpus manifest.

## Significance

This experiment represents the first comprehensive PDAF analysis of 2016 presidential campaign populist discourse across all major candidates. The candidate comparison analysis will produce empirical findings on:

1. **Candidate effects**: Whether different candidates show distinct populist discourse patterns
2. **Party differences**: Whether Republican and Democratic candidates differ systematically on specific populist dimensions
3. **Temporal evolution**: Whether populist rhetoric intensifies across campaign phases
4. **Strategic sophistication**: Whether rhetorical consistency correlates with electoral success
5. **Framework validation**: Whether PDAF provides meaningful discrimination across candidates and contexts

The diverse candidate sample (57 speeches) and comprehensive dimensional analysis (9 PDAF dimensions) provide robust data for candidate comparison while testing PDAF's ability to detect meaningful differences in populist discourse patterns across different campaign contexts and candidate types.

```yaml
# --- Start of Machine-Readable Appendix ---

# Metadata (Required)
metadata:
  experiment_name: "vanderveen_presidential_pdaf_replication"
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
