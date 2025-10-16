# Vanderveen Presidential PDAF Experiment - Statistical Power Enhancement Tasks

**Current Status**: 56 speeches total, significant power limitations for minor candidates
**Goal**: Upgrade statistical power to enable robust analysis across all candidates

## Current Sample Sizes
- **Donald Trump**: 21 speeches (Tier 2 - moderately powered)
- **Hillary Clinton**: 21 speeches (Tier 2 - moderately powered)  
- **Bernie Sanders**: 5 speeches (Tier 3 - exploratory)
- **Marco Rubio**: 4 speeches (Tier 3 - exploratory)
- **Ted Cruz**: 3 speeches (Tier 3 - exploratory)
- **John Kasich**: 2 speeches (Tier 3 - exploratory)

---

## 🎯 TIER 1: Minimum Viable Analysis (N≥10 per group)
**Target**: Enable meaningful ANOVA across all 6 candidates
**Timeline**: 2-3 weeks
**Total Additional Speeches**: 26

### Collection Tasks
- [ ] **Sanders Collection** (5→10 speeches)
  - [ ] Identify 5 additional Sanders speeches from primary season
  - [ ] Focus on: Iowa caucus period, Super Tuesday states, late primary rallies
  - [ ] Sources: Campaign websites, C-SPAN archives, local news coverage
  - [ ] Priority dates: February-March 2016

- [ ] **Rubio Collection** (4→10 speeches)  
  - [ ] Identify 6 additional Rubio speeches from primary season
  - [ ] Focus on: Florida campaign events, establishment endorsements, debate prep rallies
  - [ ] Sources: Florida media archives, campaign event transcripts
  - [ ] Priority dates: January-March 2016

- [ ] **Cruz Collection** (3→10 speeches)
  - [ ] Identify 7 additional Cruz speeches from primary season
  - [ ] Focus on: Iowa caucus events, evangelical rallies, conservative conferences
  - [ ] Sources: Conservative media archives, religious conference transcripts
  - [ ] Priority dates: January-February 2016

- [ ] **Kasich Collection** (2→10 speeches)
  - [ ] Identify 8 additional Kasich speeches from primary season
  - [ ] Focus on: New Hampshire events, moderate Republican gatherings, policy speeches
  - [ ] Sources: New Hampshire media, moderate Republican organization archives
  - [ ] Priority dates: January-March 2016

### Technical Tasks
- [ ] **Corpus Integration**
  - [ ] Add new speeches to corpus manifest with proper metadata
  - [ ] Update document counts and candidate distributions
  - [ ] Validate YAML syntax and structure
  - [ ] Update experiment.md statistical parameters

- [ ] **Quality Assurance**
  - [ ] Verify speech authenticity and completeness
  - [ ] Check word counts and transcript quality
  - [ ] Ensure consistent metadata across all new documents
  - [ ] Run corpus validation tests

### Expected Outcomes
- ✅ Meaningful 6-group ANOVA possible
- ✅ Can detect medium-to-large effect sizes (d ≥ 0.8)
- ✅ Reliable descriptive statistics and patterns
- ✅ All candidates move to Tier 2 or higher

---

## 🎯 TIER 2: Reliable Analysis (N≥15 per group)
**Target**: Enable reliable post-hoc testing and effect size estimation
**Timeline**: 4-6 weeks (after Tier 1 completion)
**Total Additional Speeches**: 20 (46 total from baseline)

### Collection Tasks
- [ ] **Sanders Collection** (10→15 speeches)
  - [ ] Identify 5 additional Sanders speeches
  - [ ] Focus on: Convention period, general election surrogate speeches
  - [ ] Sources: DNC archives, progressive organization events
  - [ ] Priority dates: July-November 2016

- [ ] **Rubio Collection** (10→15 speeches)
  - [ ] Identify 5 additional Rubio speeches
  - [ ] Focus on: Senate campaign events, establishment endorsements
  - [ ] Sources: Florida Senate race archives, Republican organization events
  - [ ] Priority dates: Throughout 2016

- [ ] **Cruz Collection** (10→15 speeches)
  - [ ] Identify 5 additional Cruz speeches
  - [ ] Focus on: Conservative conferences, policy speeches, endorsements
  - [ ] Sources: Conservative think tank archives, policy conference transcripts
  - [ ] Priority dates: Throughout 2016

- [ ] **Kasich Collection** (10→15 speeches)
  - [ ] Identify 5 additional Kasich speeches
  - [ ] Focus on: Policy speeches, moderate Republican events, endorsements
  - [ ] Sources: Moderate Republican organization archives, policy conference transcripts
  - [ ] Priority dates: Throughout 2016

### Technical Tasks
- [ ] **Advanced Statistical Analysis**
  - [ ] Implement Dunn's post-hoc tests for all pairwise comparisons
  - [ ] Calculate robust effect sizes (Cohen's d, η²) for all comparisons
  - [ ] Generate confidence intervals for all statistical estimates
  - [ ] Update statistical analysis functions with enhanced power

- [ ] **Report Enhancement**
  - [ ] Update final report with reliable statistical conclusions
  - [ ] Add comprehensive post-hoc analysis section
  - [ ] Include effect size interpretations and practical significance
  - [ ] Enhance methodology section with power analysis

### Expected Outcomes
- ✅ Reliable post-hoc testing (Dunn's tests)
- ✅ Better effect size estimates
- ✅ Can detect medium effect sizes (d ≥ 0.6)
- ✅ Publication-ready statistical methodology

---

## 🎯 TIER 3: Robust Analysis (N≥20 per group)
**Target**: Enable robust statistical conclusions and smaller effect detection
**Timeline**: 6-8 weeks (after Tier 2 completion)
**Total Additional Speeches**: 20 (66 total from baseline)

### Collection Tasks
- [ ] **Trump Collection** (21→30 speeches)
  - [ ] Identify 9 additional Trump speeches
  - [ ] Focus on: Early primary events, policy speeches, business events
  - [ ] Sources: Business conference archives, early campaign events
  - [ ] Priority dates: 2015-early 2016

- [ ] **Clinton Collection** (21→30 speeches)
  - [ ] Identify 9 additional Clinton speeches
  - [ ] Focus on: Early primary events, policy speeches, women's events
  - [ ] Sources: Women's organization archives, early campaign events
  - [ ] Priority dates: 2015-early 2016

- [ ] **Sanders Collection** (15→20 speeches)
  - [ ] Identify 5 additional Sanders speeches
  - [ ] Focus on: Early campaign events, policy speeches, progressive conferences
  - [ ] Sources: Progressive organization archives, early campaign events
  - [ ] Priority dates: 2015-early 2016

- [ ] **Rubio Collection** (15→20 speeches)
  - [ ] Identify 5 additional Rubio speeches
  - [ ] Focus on: Early campaign events, policy speeches, Hispanic outreach
  - [ ] Sources: Hispanic organization archives, early campaign events
  - [ ] Priority dates: 2015-early 2016

- [ ] **Cruz Collection** (15→20 speeches)
  - [ ] Identify 5 additional Cruz speeches
  - [ ] Focus on: Early campaign events, policy speeches, conservative conferences
  - [ ] Sources: Conservative organization archives, early campaign events
  - [ ] Priority dates: 2015-early 2016

- [ ] **Kasich Collection** (15→20 speeches)
  - [ ] Identify 5 additional Kasich speeches
  - [ ] Focus on: Early campaign events, policy speeches, moderate conferences
  - [ ] Sources: Moderate organization archives, early campaign events
  - [ ] Priority dates: 2015-early 2016

### Technical Tasks
- [ ] **Advanced Statistical Modeling**
  - [ ] Implement mixed-effects models for temporal analysis
  - [ ] Add interaction effect analysis (candidate × phase × dimension)
  - [ ] Implement robust statistical tests (bootstrap confidence intervals)
  - [ ] Add sensitivity analysis for outlier effects

- [ ] **Publication Preparation**
  - [ ] Generate publication-ready statistical tables
  - [ ] Create comprehensive methodology appendix
  - [ ] Prepare replication materials and code
  - [ ] Draft academic paper with robust statistical foundation

### Expected Outcomes
- ✅ Robust statistical conclusions
- ✅ Can detect smaller effect sizes (d ≥ 0.5)
- ✅ Publication-ready statistical power
- ✅ Comprehensive temporal and interaction analysis

---

## 📋 General Collection Guidelines

### Quality Standards
- [ ] **Transcript Quality**: Full, accurate transcripts (not summaries)
- [ ] **Word Count**: Minimum 500 words per speech
- [ ] **Authenticity**: Verified original speeches, not paraphrased content
- [ ] **Metadata**: Complete campaign phase, date, location, and context

### Source Prioritization
1. **Primary Sources**: Official campaign transcripts, C-SPAN archives
2. **Secondary Sources**: Major news outlets, academic archives
3. **Tertiary Sources**: Local media, organization archives (with verification)

### Technical Integration
- [ ] **Corpus Manifest**: Update YAML with all new documents
- [ ] **Experiment Configuration**: Update statistical parameters
- [ ] **Validation**: Run full experiment validation after each tier
- [ ] **Testing**: Execute statistical analysis to verify improvements

### Progress Tracking
- [ ] **Collection Log**: Track speeches collected by candidate and source
- [ ] **Quality Metrics**: Monitor transcript quality and completeness
- [ ] **Statistical Validation**: Test power improvements after each batch
- [ ] **Timeline Management**: Adjust collection strategy based on progress

---

## 🎯 Success Metrics

### Tier 1 Success (N≥10)
- All candidates have ≥10 speeches
- ANOVA across 6 groups is statistically meaningful
- Can detect large effect sizes (d ≥ 0.8)

### Tier 2 Success (N≥15)  
- All candidates have ≥15 speeches
- Post-hoc testing is reliable
- Can detect medium effect sizes (d ≥ 0.6)

### Tier 3 Success (N≥20)
- All candidates have ≥20 speeches
- Robust statistical conclusions possible
- Can detect smaller effect sizes (d ≥ 0.5)
- Publication-ready statistical power

---

**Last Updated**: 2025-09-03
**Next Review**: After Tier 1 completion
