# Experiment: Non-Blind Comparative Analysis of Populist Discourse Patterns Across Ideological Boundaries
## A PDAF v1.0 Bias Effects Study Using Revealed Speaker Identities

**Date**: July 12, 2025  
**Framework**: Populist Discourse Analysis Framework (PDAF) v1.0  
**Analysis Type**: Non-blind comparative cross-ideological populist discourse analysis  
**Comparison Study**: Bias effects measurement vs. blind analysis condition
**Expected Duration**: 45-60 minutes computational analysis

---

## Research Question

**Primary Question**: How do political speeches from different ideological orientations (conservative dignity, progressive dignity, conservative tribalism, progressive tribalism) differ in their populist discourse patterns as measured by the PDAF v1.0 framework's nine-anchor architecture when analyzed with revealed speaker identities?

**Bias Effects Question**: Do LLM-based political discourse analyses produce different PDAF scores when speaker identities are revealed versus anonymized, and what does this reveal about bias effects in computational social science?

**Secondary Questions**:
1. Does the PDAF v1.0 calibration system effectively distinguish between populist discourse patterns and adjacent concepts (nationalism, economic appeals) when speaker identities are known?
2. Can PDAF's boundary distinction tests separate "principled critique" from "raw populist negativity" in edge cases without the protection of blinding?
3. How do the nine anchors perform across different ideological contexts while maintaining cross-ideological validity when analyst bias is possible?

---

## Literature Context

### Theoretical Foundation

**Populist Discourse Theory**: Recent scholarship identifies populism as a distinct political communication style characterized by people-elite moral dichotomies, crisis-restoration narratives, and anti-pluralist exclusion (Mudde, 2004; Laclau, 2005). PDAF v1.0 operationalizes these theoretical insights into measurable dimensions with empirical calibration.

**Cross-Ideological Populism**: Research demonstrates that populist discourse patterns appear across ideological boundaries, with left-populist and right-populist variants sharing core structural elements while differing in boundary conditions (Rooduijn & Pauwels, 2011; Kriesi, 2014). PDAF's calibration system enables ideologically neutral measurement.

**Boundary Distinction Challenges**: A critical challenge in populist discourse analysis is distinguishing core populist patterns from adjacent concepts like nationalism and economic redistributive appeals (Albertazzi et al., 2018; Bonikowski, 2017). PDAF's boundary anchors and calibration packets address this methodological gap.

### Research Gap

**Calibration System Validation**: While existing populist measurement frameworks exist, few incorporate empirical calibration systems that prevent ideological bias and ensure cross-contextual validity. PDAF v1.0's extreme composite reference texts provide a methodological innovation requiring validation.

**Edge Case Handling**: Previous frameworks struggle with edge cases like "principled critique" vs "raw negativity" where critical language may serve dignity-aligned rather than populist mobilization. PDAF's calibration system claims to address this limitation.

**Computational Optimization**: Most populist analysis relies on manual coding rather than computational approaches. PDAF v1.0's optimization for LLM-based analysis represents a significant methodological advance requiring empirical testing.

---

## Hypotheses

### Primary Hypothesis

**H1**: Political speeches categorized as "tribal-oriented" (both conservative and progressive) will demonstrate significantly higher PDAF Layer 2 PDI scores than speeches categorized as "dignity-oriented" (both conservative and progressive).

**Rationale**: Tribal-oriented rhetoric emphasizes people-elite moral dichotomies, crisis narratives, and anti-pluralist exclusion that align with populist discourse patterns. Dignity-oriented rhetoric emphasizes universal principles and institutional respect that score lower on populist measures.

**Operationalization**: 
- Tribal speeches: conservative_tribalism and progressive_tribalism categories
- Dignity speeches: conservative_dignity and progressive_dignity categories  
- PDAF Layer 2 PDI: Democratic engagement motivation score (0.0-2.0 scale)
- Significance threshold: p < 0.05 for mean difference between tribal and dignity groups

### Secondary Hypotheses

**H2**: The PDAF boundary distinction anchors (Nationalist Exclusion, Economic Redistributive) will show clear ideological differentiation: conservative tribalism will score higher on Nationalist Exclusion, progressive tribalism will score higher on Economic Redistributive Appeals.

**H3**: The PDAF calibration system will successfully identify and properly score "principled critique" cases as lower on populist measures despite critical language, without prior knowledge of which speeches represent such cases.

**H4**: Core populist anchors (Manichaean Framing, Crisis-Restoration, Popular Sovereignty, Anti-Pluralist) will show consistent patterns across ideological boundaries, validating cross-ideological measurement validity.

### Alternative Hypotheses

**H_alt1**: Ideological orientation (conservative vs. progressive) will be a stronger predictor of boundary anchor scores than dignity/tribal orientation, indicating ideological confounding.

**H_alt2**: The calibration system will fail to distinguish principled critique from populist negativity, reproducing the edge case issues identified in previous frameworks.

**H_alt3**: Individual speakers will show more consistency in discourse patterns than categorical assignments, suggesting personality factors dominate over rhetorical strategy categorization.

---

## Dataset Specification

### Corpus Description

**Source**: Identified corpus from political discourse collection (for bias effects study)
**Total Texts**: 8 speeches across diverse political contexts  
**Selection Period**: American political discourse spanning 1960s-2020s
**Language**: English
**Token Range**: 5,200-26,000 tokens per speech
**Corpus Location**: `corpus/` (speeches with revealed speaker identities)
**Calibration Assets**: `pdaf_assets/` (framework calibration materials)

**THIN Asset Discovery Protocol**:
- Agents access only this isolated experiment folder
- Framework specification and calibration materials discoverable through folder exploration
- Corpus filenames reveal speaker identities and speech contexts
- Non-blind analysis for bias effects measurement vs. blind condition

### Sample Distribution

**Identified Corpus** (8 speeches):
- John McCain: 2008 Presidential Election Concession Speech (~6,600 tokens)
- Mitt Romney: 2020 Senate Impeachment Vote Speech (~7,000 tokens)
- Cory Booker: 2018 First Step Act Criminal Justice Reform Speech (~20,600 tokens)
- John Lewis: 1963 March on Washington Civil Rights Speech (~4,700 tokens)
- J.D. Vance: 2022 National Conservative Conference Presentation (~17,000 tokens)
- Steve King: 2017 House Floor Immigration Speech (~26,200 tokens)
- Bernie Sanders: 2025 Economic Inequality Fighting Oligarchy Speech (~4,800 tokens)
- Alexandria Ocasio-Cortez: 2025 Economic Inequality Fighting Oligarchy Speech (~6,400 tokens)

**Non-Blind Methodology**:
- Speaker identities revealed to test bias effects in LLM analysis
- Research categories disclosed through speaker identification
- Direct comparison with blind analysis condition results
- Bias effects measurement for computational social science methodology

### Critical Test Cases

**Edge Case Analysis**: The corpus includes speeches that previous frameworks misclassified due to critical language serving different purposes than populist mobilization. This provides a direct test of PDAF's calibration system effectiveness without revealing which specific speeches serve as edge cases.

**Cross-Ideological Validation**: The corpus spans multiple decades and political contexts, enabling validation of PDAF's claim to ideological neutrality across different rhetorical approaches.

**Boundary Distinction Testing**: The corpus includes speeches that should test PDAF's boundary anchor precision for distinguishing populist patterns from nationalist and economic patterns, without revealing which speeches represent which patterns.

---

## Framework Alignment

### Framework Suitability

**PDAF v1.0 Appropriateness**: The framework is specifically designed for populist discourse analysis with validated linguistic markers and empirical calibration. The nine-anchor architecture directly addresses the theoretical distinctions central to populist communication research.

**Calibration System Integration**: PDAF's extreme composite reference texts provide empirical anchoring that previous frameworks lacked. The calibration packets enable precise measurement across ideological boundaries.

**Computational Optimization**: PDAF v1.0 includes enhanced linguistic markers optimized for LLM-based analysis, making it suitable for computational rhetoric analysis.

### Variable Mapping

**Independent Variables**:
- **Ideological Orientation**: Conservative vs. Progressive (categorical)
- **Rhetorical Strategy**: Dignity vs. Tribal (categorical)
- **Speaker Identity**: Individual politicians (categorical, for random effects)
- **Temporal Context**: Year of speech (continuous, 1963-2025)

**Dependent Variables**:
- **Nine Anchor Scores**: Individual anchor measurements (0.0-2.0 each)
- **Layer 1 PDI**: Basic populist communication (0.0-2.0)
- **Layer 2 PDI**: Democratic engagement motivation (0.0-2.0)
- **Layer 3 PDI**: Democratic system health (0.0-2.0)
- **Confidence Ratings**: Certainty assessments for each measurement (0.0-1.0)

**Control Variables**:
- **Speech Length**: Word count (continuous)
- **Speech Context**: Formal setting, audience type (categorical)
- **Calibration Alignment**: Deviation from reference text patterns (continuous)

### Framework Innovation Testing

**Calibration System Validation**: Primary focus on testing whether extreme composite reference texts provide accurate measurement anchoring across ideological boundaries.

**Boundary Distinction Precision**: Testing whether boundary anchors (Nationalist Exclusion, Economic Redistributive) successfully separate populist core from adjacent concepts.

**Edge Case Handling**: Specific validation of "principled critique" vs "raw negativity" distinction using speeches identified through calibration system analysis rather than pre-specified cases.

---

## Analysis Plan

### Primary Analysis

**Analytical Approach**: Comparative analysis using PDAF v1.0 framework with calibration system validation and boundary distinction testing.

**Step 1: Individual Anchor Analysis**
- Apply PDAF v1.0 to each speech with full nine-anchor measurement
- Document calibration packet alignment for each anchor score
- Validate boundary distinction performance across ideological contexts
- Generate confidence ratings based on calibration reference matching

**Step 2: Composite PDI Calculation**
- Calculate Layer 1, 2, and 3 PDI scores using validated mathematical formulas
- Test PDI discrimination between dignity and tribal categories
- Validate competitive dynamics calculations if applicable
- Generate interpretive categories (High/Moderate/Neutral/Low populist)

**Step 3: Calibration System Validation**
- Test cross-ideological validity: do left-populist and right-populist speeches score similarly on core anchors?
- Validate boundary distinction: do nationalist and economic patterns separate properly?
- Edge case analysis: do principled critique cases score appropriately low on populist measures?

**Step 4: Comparative Framework Analysis**
- Compare PDAF results to theoretical predictions
- Identify systematic patterns across ideological boundaries
- Document calibration system performance and limitations
- Generate framework validation insights

### Statistical Methods

**Descriptive Statistics**:
- Mean, median, standard deviation for all nine anchors and three PDI layers
- Calibration alignment scores and confidence rating distributions
- Cross-ideological pattern visualization
- Boundary distinction performance metrics

**Inferential Statistics**:
- Independent samples t-tests for dignity vs. tribal comparisons
- ANOVA for ideological orientation effects
- Correlation analysis between anchors and PDI layers
- Chi-square tests for categorical prediction accuracy

**Calibration Validation**:
- Calibration packet alignment scoring
- Cross-ideological validity coefficients
- Boundary distinction precision metrics
- Edge case handling accuracy assessment

### Quality Controls

**Calibration Alignment Verification**:
- Each anchor score validated against calibration packet examples
- Cross-ideological pattern consistency checking
- Boundary distinction validation across all boundary anchors
- Competitive dynamics accuracy assessment

**Methodological Transparency**:
- Complete documentation of calibration reference matching
- Evidence preservation with calibration packet citations
- Uncertainty quantification for all measurements
- Alternative interpretation consideration for edge cases

---

## Expected Outcomes

### Primary Predictions

**Quantitative Predictions**:
- Tribal speeches: Mean Layer 2 PDI > 1.2 (moderate-high populist)
- Dignity speeches: Mean Layer 2 PDI < 0.8 (low-moderate populist)
- Boundary anchor differentiation: Conservative tribalism higher on Nationalist Exclusion, Progressive tribalism higher on Economic Redistributive
- Edge case handling: Speeches with principled critique patterns scoring < 1.0 on core populist anchors despite critical language

**Qualitative Predictions**:
- Calibration system will demonstrate clear ideological neutrality
- Boundary distinction will successfully separate populist from adjacent concepts
- Core populist anchors will show consistent patterns across ideological boundaries
- Edge cases will be handled appropriately through calibration reference matching

### Significance Thresholds

**Statistical Significance**: p < 0.05 for primary hypothesis testing
**Effect Size**: Cohen's d > 0.5 for meaningful differences
**Calibration Alignment**: > 0.7 correlation with reference text patterns
**Boundary Precision**: > 80% accuracy in distinguishing populist from adjacent concepts

### Framework Validation Criteria

**Cross-Ideological Validity**: Core populist anchors show similar patterns across left-populist and right-populist speeches
**Boundary Distinction**: Nationalist and Economic anchors clearly separate ideological variants
**Edge Case Handling**: Principled critique cases score appropriately low on populist measures
**Calibration Stability**: Consistent reference text alignment across all speech categories

---

## Methodological Innovation Testing

### Calibration System Evaluation

**Extreme Composite Reference Validation**:
- Test whether calibration packets provide accurate measurement anchoring
- Evaluate cross-ideological validity of reference text patterns
- Assess boundary disambiguation effectiveness
- Validate competitive dynamics integration

**Computational Optimization Assessment**:
- Test LLM-based analysis accuracy compared to manual coding
- Evaluate linguistic marker effectiveness in computational contexts
- Assess calibration system integration with automated analysis
- Validate confidence rating accuracy

### Boundary Distinction Precision

**Populist vs. Nationalist Separation**:
- Test whether Nationalist Exclusion anchor captures cultural exclusion without conflating with core populist patterns
- Validate that populist core anchors remain ideologically neutral
- Assess boundary clarity in mixed cases

**Populist vs. Economic Separation**:
- Test whether Economic Redistributive anchor captures class-based appeals without conflating with populist anti-elitism
- Validate that economic populism scores appropriately on both populist core and economic boundary anchors
- Assess boundary precision in left-populist contexts

### Edge Case Handling

**Principled Critique vs. Raw Negativity**:
- Test whether speeches with critical language toward specific targets score appropriately based on underlying purpose
- Validate that calibration system distinguishes principled institutional critique from populist anti-elitism
- Assess framework performance on speeches where critical language serves constitutional or justice-oriented purposes

**Dignity-Aligned Critical Language**:
- Test whether calibration system recognizes critical language serving universal dignity principles
- Validate that moral critique based on constitutional principles scores differently from populist moral dichotomies
- Assess framework's ability to handle complex rhetorical strategies

---

## Ethical Considerations

### Research Ethics

**Ideological Neutrality**: This study tests populist discourse patterns without endorsing any political position. All ideological orientations are treated as legitimate objects of academic inquiry with equal analytical rigor.

**Calibration System Bias Prevention**: The extreme composite reference texts are designed to prevent ideological bias through cross-ideological validation. The study will assess whether this goal is achieved.

**Methodological Transparency**: Complete documentation of calibration system performance, boundary distinction accuracy, and edge case handling ensures replicability and prevents selective reporting.

### Implications Assessment

**Framework Validation Impact**: Results will influence future populist discourse research and potentially affect how scholars understand populist communication patterns across ideological boundaries.

**Calibration System Evaluation**: The study will determine whether PDAF's calibration approach represents a methodological advance or requires refinement for accurate populist measurement.

**Computational Analysis Advancement**: Findings will contribute to the development of computational approaches to political discourse analysis with potential applications in media monitoring and democratic health assessment.

---

## Conclusion

This experiment provides a comprehensive test of PDAF v1.0's key innovations: nine-anchor populist architecture, extreme composite reference calibration, and boundary distinction precision. By analyzing speeches across ideological boundaries with particular attention to edge cases, the study addresses both theoretical questions about populist discourse and practical questions about computational measurement accuracy.

**Key Contributions**:
1. **Calibration System Validation**: First systematic test of extreme composite reference texts for populist measurement
2. **Boundary Distinction Assessment**: Comprehensive evaluation of populist vs. nationalist vs. economic pattern separation
3. **Edge Case Handling**: Specific testing of principled critique vs. raw negativity distinction
4. **Cross-Ideological Validity**: Empirical validation of ideologically neutral populist measurement
5. **Computational Optimization**: Testing of LLM-based analysis with calibration system integration

**Expected Impact**: Results will advance populist discourse analysis methodology while providing practical tools for computational political analysis. The study will determine whether PDAF v1.0 represents a significant methodological advance or requires further refinement for accurate populist measurement across ideological boundaries. 