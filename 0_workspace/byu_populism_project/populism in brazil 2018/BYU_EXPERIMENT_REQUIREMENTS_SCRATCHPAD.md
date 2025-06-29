# BYU Experiment Requirements Scratchpad

**Project**: Tamaki & Fuks Competitive Populism Framework Validation  
**Framework**: `tamaki_fuks_competitive_populism_v3.2.yaml`  
**Created**: January 2025  
**Purpose**: Experimental design requirements for validating computational populism analysis

## Overview

This document outlines the experimental requirements for validating our Tamaki & Fuks competitive populism framework against the original BYU Team Populism methodology. Each experiment has a specific purpose and core falsifiable hypothesis that makes it unique.

**Core Research Question**: Can computational analysis using Framework Specification v3.2 replicate and extend the insights from manual human coding of Brazilian populist discourse?

---

## Experiment 1: Tamaki & Fuks Methodology Replication

**Purpose**: Validate our framework against the original BYU Team Populism manual coding results  
**Core Falsifiable Question**: Can our computational analysis achieve r > 0.80 correlation with manual human coding of Bolsonaro's populism scores?

**Hypothesis**: 
- H1: Computational analysis will correlate r > 0.80 with manual coding
- H0: Computational analysis will show r ≤ 0.80 correlation (random/inadequate)

**Key Variables**:
- Independent: Speech text (12 Bolsonaro speeches, July-October 2018)
- Dependent: Populism score (0-2 scale following Tamaki & Fuks methodology)
- Control: Original manual coding scores as ground truth

**Success Criteria**:
- Correlation coefficient r > 0.80 with manual scores
- Average score accuracy: 0.50 ±0.02 (matching Bolsonaro's 0.5 baseline)
- Temporal progression match: 0.5→0.9 pattern recognition
- Statistical significance: p < 0.05

---

## Experiment 2: Context Effects Analysis

**Purpose**: Quantify the difference between isolated speaker analysis vs. full rally context  
**Core Falsifiable Question**: Does analyzing Bolsonaro's isolated utterances produce significantly different populism scores than analyzing full rally context?

**Hypothesis**:
- H1: Isolated speaker analysis will show higher populism scores than contextualized analysis
- H0: No significant difference between isolated and contextualized analysis

**Key Variables**:
- Independent: Analysis mode (isolated vs. contextualized)
- Dependent: Populism score difference
- Control: Same speech corpus analyzed both ways

**Success Criteria**:
- Measurable effect size (Cohen's d > 0.3)
- Statistical significance (p < 0.05)
- Directional consistency across speeches
- Theoretical explanation for observed differences

**Methodological Innovation**: This addresses the video vs. transcript gap that BYU acknowledged but couldn't control for.

---

## Experiment 3: Corpus Isolation A/B Test

**Purpose**: Compare manually pre-isolated Bolsonaro corpus vs. LLM-guided isolation instructions  
**Core Falsifiable Question**: Does pre-isolating Bolsonaro utterances produce different results than instructing the LLM to focus only on Bolsonaro's words?

**Hypothesis**:
- H1: Pre-isolated corpus will show more consistent results with lower variance
- H0: No significant difference between pre-isolation and LLM-guided isolation

**Experimental Design**:
- **Condition A**: Manually cleaned corpus with only Bolsonaro's direct quotes
- **Condition B**: Full rally transcripts with LLM instructions to isolate Bolsonaro
- **Condition C**: Full rally transcripts with no isolation instructions (control)

**Key Variables**:
- Independent: Corpus preparation method
- Dependent: Populism score accuracy and variance
- Control: Same speeches processed different ways

**Success Criteria**:
- Variance comparison between conditions
- Accuracy difference vs. ground truth
- Processing consistency (reliability across runs)
- Cost-benefit analysis of manual vs. automated isolation

---

## Experiment 4: Language Effects Validation

**Purpose**: Test the impact of Portuguese vs. English vs. mixed language cues on analysis accuracy  
**Core Falsifiable Question**: Does using Portuguese-only language cues produce more accurate results than English or mixed-language frameworks?

**Hypothesis**:
- H1: Portuguese-only framework will achieve highest correlation with manual coding
- H0: No significant difference between language cue approaches

**Experimental Design**:
- **Framework A**: Portuguese-only cues (current `tamaki_fuks_competitive_populism_v3.2.yaml`)
- **Framework B**: English-only cues (translated equivalents)
- **Framework C**: Mixed Portuguese/English cues
- **Framework D**: Language-agnostic approach (minimal cues)

**Key Variables**:
- Independent: Language cue strategy
- Dependent: Correlation with manual coding
- Control: Same corpus, different framework versions

**Success Criteria**:
- Correlation coefficient comparison
- Cultural authenticity assessment
- Methodological credibility evaluation
- LLM language understanding validation

---

## Experiment 5: Competitive Ideology Dynamics

**Purpose**: Validate the Tamaki & Fuks insight that patriotism and nationalism compete with populism  
**Core Falsifiable Question**: Do speeches with higher patriotism/nationalism scores show systematically lower populism scores?

**Hypothesis**:
- H1: Populism scores will be negatively correlated with patriotism and nationalism scores
- H0: No systematic relationship between ideological categories

**Key Variables**:
- Independent: Patriotism and nationalism anchor scores
- Dependent: Populism anchor scores
- Control: Same speeches analyzed for all three anchors

**Success Criteria**:
- Negative correlation between populism and competing ideologies
- Statistical significance of competitive relationships
- Replication of Tamaki & Fuks qualitative observation quantitatively
- Theoretical validation of "crowding out" mechanism

**Novel Contribution**: First quantitative measurement of competitive ideology dynamics in political discourse.

---

## Experiment 6: Temporal Evolution Analysis

**Purpose**: Track changes in Bolsonaro's populist rhetoric across the 2018 campaign timeline  
**Core Falsifiable Question**: Can computational analysis detect the same temporal progression that manual coders observed (0.5→0.9 increase)?

**Hypothesis**:
- H1: Populism scores will show systematic increase from July to October 2018
- H0: No systematic temporal pattern in populism scores

**Key Variables**:
- Independent: Speech date (temporal sequence)
- Dependent: Populism score evolution
- Control: Chronological ordering of same corpus

**Success Criteria**:
- Temporal progression pattern match (0.5→0.9)
- October 7 turning point detection
- Statistical significance of trend
- Correlation with electoral timeline events

**Theoretical Significance**: Validates computational detection of campaign strategy evolution.

---

## Experiment 7: Cross-LLM Reliability Assessment

**Purpose**: Test consistency of populism analysis across different LLM systems  
**Core Falsifiable Question**: Do different LLM systems (GPT-4, Claude, Gemini) produce consistent populism scores using the same framework?

**Hypothesis**:
- H1: Inter-LLM reliability will exceed r > 0.70 (acceptable reliability threshold)
- H0: Inter-LLM reliability will be r ≤ 0.70 (inadequate consistency)

**Experimental Design**:
- **System A**: GPT-4 with Tamaki & Fuks framework
- **System B**: Claude with Tamaki & Fuks framework  
- **System C**: Gemini with Tamaki & Fuks framework
- **System D**: Local model (for comparison)

**Key Variables**:
- Independent: LLM system
- Dependent: Populism score consistency
- Control: Identical framework and corpus across systems

**Success Criteria**:
- Inter-rater reliability coefficient > 0.70
- Systematic vs. random error analysis
- Cost-performance optimization
- Framework robustness validation

---

## Experiment 8: Framework Specification v3.2 Compliance

**Purpose**: Validate that our framework properly implements Framework Specification v3.2 anchor-set architecture  
**Core Falsifiable Question**: Does the anchor-set implementation produce theoretically consistent results compared to axis-based approaches?

**Hypothesis**:
- H1: Anchor-set framework will show better theoretical consistency than axis-based alternatives
- H0: No significant difference between architectural approaches

**Experimental Design**:
- **Architecture A**: Pure anchor-set (current implementation)
- **Architecture B**: Axis-based populism-pluralism framework
- **Architecture C**: Hybrid axes + anchors approach

**Key Variables**:
- Independent: Framework architecture
- Dependent: Theoretical consistency and interpretability
- Control: Same corpus across architectural variants

**Success Criteria**:
- Theoretical coherence assessment
- Interpretability evaluation
- Framework Specification compliance
- Academic credibility validation

---

## Experiment 9: Scalability Performance Analysis

**Purpose**: Test framework performance and accuracy at scale using Global Populism Database  
**Core Falsifiable Question**: Does analysis quality degrade significantly when scaling from 12 speeches to 100+ speeches?

**Hypothesis**:
- H1: Framework will maintain correlation r > 0.70 with manual coding at scale
- H0: Framework performance will degrade significantly at scale

**Key Variables**:
- Independent: Corpus size (12, 50, 100, 200+ speeches)
- Dependent: Accuracy maintenance and processing consistency
- Control: Subset validation against manual coding

**Success Criteria**:
- Accuracy maintenance across scale
- Processing time optimization
- Quality control validation
- Cost-effectiveness analysis

---

## Experiment 10: Novel Insights Discovery

**Purpose**: Identify patterns or insights not detectable through manual coding alone  
**Core Falsifiable Question**: Can computational analysis reveal systematic patterns in populist discourse that were not identified in the original BYU study?

**Hypothesis**:
- H1: Computational analysis will identify at least 2 novel patterns not reported in Tamaki & Fuks
- H0: Computational analysis will only replicate previously known patterns

**Exploration Areas**:
- Linguistic complexity patterns in populist vs. non-populist segments
- Temporal micro-evolution within individual speeches
- Audience response correlation with populist intensity
- Syntactic pattern analysis
- Competitive ideology transition patterns

**Success Criteria**:
- Novel pattern identification
- Academic significance assessment
- Theoretical contribution evaluation
- Methodological innovation validation

---

## Experimental Timeline & Dependencies

### Phase 1: Foundation Experiments (Weeks 1-2)
- **Experiment 1**: Tamaki & Fuks Methodology Replication (prerequisite for all others)
- **Experiment 2**: Context Effects Analysis
- **Experiment 3**: Corpus Isolation A/B Test

### Phase 2: Methodological Validation (Weeks 3-4)  
- **Experiment 4**: Language Effects Validation
- **Experiment 5**: Competitive Ideology Dynamics
- **Experiment 7**: Cross-LLM Reliability Assessment

### Phase 3: Advanced Analysis (Weeks 5-6)
- **Experiment 6**: Temporal Evolution Analysis
- **Experiment 8**: Framework Specification v3.2 Compliance
- **Experiment 10**: Novel Insights Discovery

### Phase 4: Scale Testing (Week 7)
- **Experiment 9**: Scalability Performance Analysis

---

## Success Metrics & Validation Framework

### Minimum Viable Validation (Gates 1-2)
- **Gate 1**: Experiment 1 achieves r > 0.70 correlation
- **Gate 2**: Experiment 5 demonstrates competitive ideology dynamics

### Academic Credibility Validation (Gates 3-4)
- **Gate 3**: Experiments 2-4 show systematic, interpretable patterns
- **Gate 4**: Experiment 7 demonstrates cross-LLM reliability

### Strategic Partnership Validation (Gate 5)
- **Gate 5**: Experiments 6, 8-10 provide novel academic insights

### Quality Assurance
- Statistical significance testing for all quantitative hypotheses
- Effect size reporting (Cohen's d) for practical significance
- Confidence intervals for all correlation coefficients
- Multiple comparison corrections where appropriate
- Systematic error pattern analysis vs. random noise

---

## Resource Requirements

### Technical Infrastructure
- Multiple LLM API access (GPT-4, Claude, Gemini)
- Computational resources for large-scale analysis
- Statistical analysis software (R/Python)
- Data storage for corpus and results

### Human Resources
- Experiment design and execution
- Statistical analysis and interpretation
- Framework development and testing
- Documentation and academic writing

### Data Requirements
- Original Tamaki & Fuks manual coding results
- Complete Bolsonaro speech corpus (transcripts)
- Temporal metadata for campaign timeline analysis
- Global Populism Database access (for scaling experiments)

---

## Risk Mitigation

### Experimental Risks
- **Low correlation with manual coding**: Honest assessment of limitations, hybrid validation approach
- **Cross-LLM inconsistency**: Framework robustness improvements, ensemble methods
- **Scale degradation**: Quality control mechanisms, statistical validation protocols
- **No novel insights**: Focus on methodological replication and validation

### Academic Risks
- **Methodological criticism**: Complete experimental transparency, peer review engagement
- **Reproducibility concerns**: Open framework specifications, detailed methodology documentation
- **"Black box" concerns**: Interpretable analysis methods, step-by-step validation

### Strategic Risks
- **Partnership delays**: Modular deliverables, incremental value demonstration
- **Technology limitations**: Realistic scope management, honest capability documentation
- **Academic alignment**: Continuous feedback integration, collaborative development

---

**Next Steps**: 
1. Prioritize Phase 1 experiments for immediate execution
2. Establish statistical analysis protocols
3. Prepare experimental infrastructure
4. Begin with Experiment 1 (Tamaki & Fuks replication) as foundation

**Cross-Reference**: See `BYU_STRATEGIC_ENGAGEMENT_PLAN.md` for partnership strategy and `BYU_METHODOLOGICAL_VALIDATION_PROTOCOL.md` for technical implementation details. 