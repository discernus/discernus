# BYU Populism Prototype: Strategic Plan

## Context & Strategic Rationale

### Role-Play Validation Approach
We conducted an extensive role-play exercise where we simulated Kirk Hawkins (BYU Political Science, Director of Team Populism) receiving a collaboration proposal for the Discernus platform. This approach allowed us to:

- **Validate product-market fit** from an authentic academic researcher perspective
- **Identify specific pain points** in current political discourse analysis workflows
- **Understand quality standards** and methodological requirements
- **Discover collaboration pathways** and potential partnership structures
- **Clarify value propositions** that resonate with academic research needs

### Key Strategic Insights
The role-play revealed that our populism/pluralism framework aligns remarkably well with active academic research. Kirk Hawkins literally runs the [Global Populism Database](https://populism.byu.edu/publications) and has published extensively on measuring populist discourse - meaning this addresses a real, current pain point rather than a theoretical need.

**Strategic Advantages Identified**:
- **Scaling opportunity**: They manually code thousands of speeches - computational assistance could be transformative
- **Methodological innovation**: Geometric visualizations and contradiction detection offer novel analytical capabilities
- **Reproducibility crisis**: Academic demand for transparent, reproducible analysis workflows
- **Global network**: Team Populism spans 30+ countries, providing scale potential
- **Student researcher pipeline**: 15-20 graduate students who could adopt our tools

**Critical Success Factors**:
- Must meet academic quality standards (not just "good enough")
- Requires methodological transparency and reproducibility
- Needs integration with existing workflows (Stata, manual coding)
- Must handle multilingual analysis (Portuguese, Spanish, English)
- Should provide pedagogical value for graduate students

### Strategic Rationale
Rather than building a general-purpose SaaS platform, we're pursuing **strategic academic partnerships** as our go-to-market approach. This allows us to:

1. **Validate methodology** against established academic standards
2. **Build credibility** through peer-reviewed research collaboration
3. **Understand user needs** deeply before scaling
4. **Establish moat** through domain expertise and research relationships
5. **Create network effects** through academic collaboration networks

## Crucial Open Questions

Our plan must definitively answer these fundamental questions to validate this strategic direction:

### Technical Viability Questions
- **Q1**: Can our framework detect populist discourse patterns with accuracy comparable to manual human coding?
- **Q2**: Does our approach work effectively for Portuguese political discourse, including specific terminology like 'povo' versus 'elite'?
- **Q3**: Can we generate visualizations that feel "Jupyter native" rather than "wacky bolt-ons" to academic users?
- **Q4**: Is our temporal analysis capability sufficient to track rhetorical changes over campaign timelines?
- **Q5**: Can we achieve reliable transcription quality from video sources for Portuguese political speeches?
- **Q6**: Does our framework handle domain-specific Brazilian political discourse (not just general Portuguese)?

### Market Validation Questions  
- **Q7**: Do our analytical outputs provide insights that researchers cannot easily obtain through existing methods?
- **Q8**: Is there genuine demand for computational approaches to supplement manual coding workflows?
- **Q9**: Would graduate students actually adopt Jupyter notebook-based analytical tools?
- **Q10**: Can our approach scale beyond individual researchers to research networks?
- **Q11**: Can we provide baseline validation against speeches already hand-coded by academic teams?
- **Q12**: Can we enable meaningful comparisons across candidates within the same election cycle?

### Business Model Questions
- **Q13**: Can we address "black box" concerns while maintaining competitive advantage?
- **Q14**: What licensing approach builds trust while preserving future revenue potential?
- **Q15**: How do we reassure collaborators we won't "rugpull" them after they invest resources?
- **Q16**: Is there a path from academic partnerships to sustainable monetization?
- **Q17**: Can we differentiate sufficiently from existing text analysis tools?
- **Q18**: Do we provide enough value to justify resource investment from research partners?

### Partnership Viability Questions
- **Q19**: Are we bringing genuine value to academic collaborations, or just asking for favors?
- **Q20**: Can we meet the methodological rigor standards required for academic publication?
- **Q21**: Can we reach the "expensive manual human rater happy place equivalent" quality standard?
- **Q22**: Is there alignment between our development roadmap and research community needs?
- **Q23**: Can we build lasting partnerships rather than one-off collaborations?

### Success Validation Framework
**If we can answer YES to 17+ of these 23 questions after executing our plan, we have validated this strategic direction.**

**Critical Success Threshold**: Must answer YES to ALL Technical Viability questions (Q1-Q6) and at least 3 of 6 Market Validation questions (Q7-Q12) to proceed.

**Additional Key Questions** that must be addressed:
- **Q3** (Jupyter native visualizations): Critical for user adoption
- **Q15** (rugpull concerns): Essential for building trust  
- **Q21** (quality standard equivalence): Make-or-break for academic credibility

### Jupyter Native Heuristics
To objectively measure the subjective "Jupyter native" feel (Q3), we will evaluate our prototype notebook against the following heuristics. A "native" experience means the user feels empowered and the tool feels like a natural extension of their existing workflow, not a foreign element.

- **1. Data Fluidity**: Can a user easily get data *out* of our visualizations and into a standard Pandas DataFrame with a single, intuitive command? The notebook should not be a data dead-end.
- **2. Standard Library Integration**: Are visualizations built on common, well-documented libraries like Matplotlib, Seaborn, or Plotly? Avoids forcing users to learn a bespoke, proprietary visualization API.
- **3. Pedagogical Clarity**: Is the notebook well-documented with Markdown cells that explain the *why* behind the analysis, not just the *what* of the code? Does it guide the user through a narrative?
- **4. Self-Containment & Reproducibility**: Can a user `Run All Cells` from top to bottom without errors? Are dependencies clearly defined and results reproducible?
- **5. Modularity & Hackability**: Are the visualization functions modular enough that a user could reasonably copy a function and tweak it for their own purposes? The notebook should empower, not constrain.

### Pivot Hypotheses & Alternative Value Propositions
A "No-Go" decision on the primary validation path is not a failure, but a data point. Based on the outcome of our pilot, we have the following pre-defined pivots and alternative value propositions:

- **Pivot Hypothesis: From Validation to Exploration.**
  - **Trigger**: If we cannot consistently match the results of manual human coding (fail Q1/Q21).
  - **Pivot**: Re-frame the tool's primary value from *validating existing theories* to *enabling exploratory analysis*. The tool's purpose would be to rapidly scan large corpora to find novel patterns, generate new hypotheses, and identify interesting areas for deep manual review. This changes the user from a "validator" to an "explorer."

- **Alternative Value Prop: The Productivity Multiplier (Human-in-the-Loop).**
  - **Trigger**: Could be a primary offering or a fallback if full automation is too difficult.
  - **Value Prop**: Instead of replacing the human rater, we augment them. The platform would perform a first-pass analysis, flag ambiguous or highly populist/pluralist sections, and present them to a researcher in an efficient UI for final judgment. This shifts the value from "automated results" to "radically faster human coding." This directly addresses the labor-intensive nature of their current workflow.

### Critical Implementation Concerns Identified
Based on our conversation analysis, several specific concerns emerged that require focused attention:

**Jupyter Visualization Integration**: "I personally am not a Jupyter notebook user, so I have some trepidation about it... I just want to make sure our visualization engine ends up feeling 'jupyter native' not some wacky bolt on that gets in the way."

**Licensing/Black Box Concerns**: "If they like the prototype, they are going to immediately ask about licensing and 'black box' concerns before committing real resources."

**Quality Standard Reality Check**: "Whether we feel like we will ever be able to provide him enough quality data that he can get to his expensive manual human rater happy place equivalent... If we can't get to the moon ever, there is no sense building rockets."

**Domain-Specific Language Processing**: Specific concern about Brazilian Portuguese political terminology like 'povo' versus 'elite' and other culturally-specific populist language patterns.

**Academic Validation Requirements**: Need for baseline validation against speeches already hand-coded by academic teams, temporal pattern detection, and cross-candidate comparison capabilities.

## Executive Summary

This document outlines our strategic approach to developing a prototype analysis of Brazilian populist discourse for potential collaboration with Kirk Hawkins and the BYU Team Populism project. The goal is to validate our Discernus platform's capability to provide academic-grade analysis of political discourse while building a foundation for future research partnerships.

## Strategic Objectives

### Primary Goal
Demonstrate that Discernus can provide meaningful, reproducible analysis of populist discourse that meets academic research standards and complements existing manual coding methodologies.

### Secondary Goals
- Validate our populism/pluralism framework against established academic work
- Build trust with academic researchers through transparency and methodological rigor
- Establish a pathway for future research partnerships
- Develop Jupyter notebook-native visualization capabilities

## Background Context

**Research Partner**: Kirk Hawkins, BYU Political Science, Director of Team Populism
- Runs the Global Populism Database (66 countries, 2000-2018)
- Published extensively on measuring populist discourse
- Uses manual coding with graduate student teams
- Published specific analysis of Bolsonaro's 2018 campaign rhetoric

**Value Proposition for Partnership**:
- Scale manual coding work through computational analysis
- Provide novel geometric visualizations of ideological positioning
- Enable reproducible research workflows through Jupyter notebooks
- Detect rhetorical contradictions and temporal patterns

## Strategic Plan

### 1. Quality Bar Analysis (Critical First Step)
**Goal**: Understand if we can ever reach Kirk's "expensive manual human rater happy place"

**Actions**:
- Deep read the Bolsonaro 2018 paper (`populism-in-brazils-2018-general-elections-pdf.pdf`)
- Identify specific metrics they used (populism scores, temporal patterns, etc.)
- Map their manual coding categories to our framework capabilities
- Assess gap between our current capabilities and their quality standards

**Success Criteria**: Clear understanding of whether our approach can achieve academic-grade results

**Risk**: If we can't bridge the quality gap, there's no point building the technical infrastructure

### 2. Corpus Ingestion Workflow
**Goal**: Reliable transcription pipeline for Portuguese political discourse

**Options Analysis**:
- **YouTube extraction**: Leverage existing infrastructure, but quality concerns
- **Eleven Labs API**: Higher quality, but cost and Portuguese capability questions  
- **Manual transcription**: Guaranteed quality, but not scalable
- **Hybrid approach**: YouTube + human verification for quality subset

**Recommended Approach**: 
- Phase 1: Manual transcription of 10-15 key speeches for proof-of-concept
- Phase 2: Build automated pipeline based on results

**Success Criteria**: Clean, accurate transcripts of representative Bolsonaro campaign speeches

### 3. Framework Enhancement 
**Goal**: Upgrade `populism_pluralism_v1.0.yaml` to full experiment specification

**Technical Requirements**:
- Multilingual capability (Portuguese political terminology)
- Temporal analysis (tracking populism intensity over campaign timeline)
- Validation metrics (comparison with manual coding)
- Contradiction detection (mixed populist/pluralist rhetoric)
- Framework Specification v3.1 compliance

**Success Criteria**: Framework that can analyze Portuguese political discourse with comparable categories to manual coding rubrics

### 4. Jupyter Integration Strategy
**Goal**: Native-feeling visualizations that don't feel "bolted-on"

**Approach**:
- Use matplotlib/seaborn for static visualizations
- Plotly for interactive elements (but keep it simple)
- Custom visualization functions that generate standard notebook objects
- Clear markdown explanations between code cells
- Exportable results (CSV, images) for Stata integration

**Success Criteria**: Jupyter notebook that political science graduate students can understand and use

### 5. Licensing/IP Strategy
**Goal**: Build trust while preserving future monetization path

**Principles**:
- **Open methodology**: Publish framework specifications, make algorithms transparent
- **Data sovereignty**: Researchers own their data, we provide analysis tools
- **Academic licensing**: Free/low-cost for academic research, commercial rates for consulting
- **No vendor lock-in**: Results exportable, frameworks portable

**Communication Strategy**: Address licensing concerns proactively in initial prototype presentation

## Implementation Timeline

### Phase 1: Analysis & Planning (Days 1-2)
1. **Deep read Bolsonaro paper** - understand specific findings and methodology
2. **Corpus assessment** - evaluate available speeches, select representative sample
3. **Framework gap analysis** - identify needed enhancements for Portuguese analysis
4. **Quality benchmarking** - define success criteria against paper findings

### Phase 2: Technical Implementation (Days 3-5)
1. **Manual transcription** of 10-15 key speeches (representative campaign timeline)
2. **Framework enhancement** for Portuguese political discourse
3. **Jupyter notebook template** development
4. **Visualization prototype** development

### Phase 3: Pilot Analysis (Days 6-7)
1. **Run analysis** on transcribed speeches
2. **Generate visualizations** and statistical comparisons
3. **Compare results** to paper findings
4. **Document methodology** and results

### Phase 4: Evaluation & Decision (Day 8)
1. **Quality assessment** - do our results validate against manual coding?
2. **Gap analysis** - what would it take to reach academic standards?
3. **Go/No-Go decision** on pursuing partnership

## Success Criteria & Decision Points

### Go/No-Go Decision Point (End of Phase 3)
**Must Answer These Questions**:
- Can our approach detect the patterns Hawkins found manually?
- Are our visualizations meaningful to political scientists?
- Is the quality gap bridgeable with reasonable effort?
- Do we provide novel insights beyond manual coding?

**Go Criteria** (need 3 of 4):
- ✅ Detect major populism trends identified in paper
- ✅ Generate interpretable visualizations
- ✅ Quality gap appears bridgeable
- ✅ Provide novel analytical insights

**No-Go Criteria** (any 1 triggers):
- ❌ Fundamental disconnect between our analysis and manual coding results
- ❌ Quality gap requires complete methodology overhaul
- ❌ Technical complexity exceeds available resources
- ❌ No clear value proposition over existing methods

## Risk Assessment

### High Risk
- **Portuguese language processing**: Our framework may not handle Brazilian political terminology effectively
- **Quality standards**: Academic standards may be higher than our current capabilities
- **Data availability**: Video transcription quality may be insufficient

### Medium Risk
- **Jupyter integration**: Visualization approach may feel foreign to academic workflows
- **Temporal analysis**: Campaign timeline analysis may require methodological adjustments

### Low Risk
- **Framework adaptation**: Core populism/pluralism concepts should translate
- **Collaboration interest**: Based on role-play, genuine interest exists

## Resource Requirements

### Technical Resources
- Access to Eleven Labs API or similar transcription service
- Development time for framework enhancement
- Jupyter notebook development environment

### Research Resources
- Time for deep analysis of existing academic work
- Manual transcription capacity (10-15 speeches)
- Domain expertise consultation (Portuguese political discourse)

### Success Dependencies
- Quality transcription of source material
- Accurate mapping of academic coding categories to our framework
- Effective visualization of results in academic context

## Next Steps

1. **Immediate**: Begin deep read of Bolsonaro paper to understand methodology and findings
2. **Day 1**: Complete gap analysis between their approach and our capabilities  
3. **Day 2**: Select representative speech sample and begin transcription
4. **Day 3**: Begin framework enhancement for Portuguese analysis
5. **Decision Point**: End of week - Go/No-Go based on pilot results

## Success Metrics

### Quantitative
- Correlation between our populism scores and their manual coding
- Temporal trend alignment with paper findings
- Processing accuracy for Portuguese political terminology

### Qualitative  
- Interpretability of visualizations to political science audience
- Methodological transparency and reproducibility
- Novel insights beyond existing analysis

---

**Document Created**: January 2025  
**Project**: Discernus x BYU Team Populism Collaboration  
**Status**: Planning Phase 