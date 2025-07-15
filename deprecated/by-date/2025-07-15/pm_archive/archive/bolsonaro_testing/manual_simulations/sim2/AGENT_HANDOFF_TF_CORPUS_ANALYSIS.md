# AGENT HANDOFF DOCUMENTATION: T&F Corpus Analysis

## Mission Overview

You are tasked with executing a **systematic coordinate-free populism analysis** across the complete Tamaki & Fuks (2019) corpus of 9 Bolsonaro campaign speeches. This analysis will validate our coordinate-free analytical framework against Eduardo Tamaki's manual populism scores and demonstrate the framework's effectiveness across temporal patterns in political discourse.

## Strategic Context

### What We've Built
- **Coordinate-Free Framework**: Alternative to mathematical coordinate reduction that preserves multidimensional analytical detail
- **Sequential Analysis Protocol**: Discovery → Framework Application → Competitive Analysis → Framework Fit Assessment
- **Proven Methodology**: Successfully tested on single speech (sim1), now scaling to full corpus

### Why This Matters
- **Framework Validation**: Tests whether coordinate-free approach works across diverse political texts
- **Temporal Analysis**: Examines how populist discourse evolves over campaign timeline (Aug → Oct 2018)
- **Academic Rigor**: Compares AI analysis with expert human scoring (Eduardo Tamaki's benchmark)
- **Methodological Innovation**: Demonstrates LLM-enabled analysis without brittle software constraints

## Corpus Information

### Source Materials
**9 Tamaki & Fuks Benchmark Speeches** with Eduardo's manual scores:
1. `23 de Agosto - Araçatuba (1).m4a.txt` (Score: 0.6)
2. `31 de Agosto - Porto Velho (RO).m4a.txt` (Score: 0.0) 
3. `6 de Setembro - Associaçao Comercial e Empresarial Juiz de Fora.m4a.txt` (Score: 0.3)
4. `16 de Setembro - Apos Atentado.m4a.txt` (Score: 0.3)
5. `30 de Setembro - Av. Paulista (2).m4a.txt` (Score: 0.4)
6. `6 de Outubro - 1 dia antes das eleiçoes.m4a.txt` (Score: 0.3)
7. `16 October 2018 Speech right after the first round of elections.txt` (Score: 0.7)
8. `22 de Outubro - Av. Paulista.m4a.txt` (Score: 0.9)
9. `27 de Outubro - Ultima Live antes do 2o turno.m4a.txt` (Score: 0.9)

### Expected Pattern
Eduardo identified **temporal escalation**: Early speeches (Aug-Sep) show low populism (0.0-0.4), later speeches (Oct) show high populism (0.7-0.9). Your analysis should detect this progression.

## Setup Instructions

### Step 1: Create sim2 Directory Structure
```
0_workspace/rethink/new_specs/sim2/
├── corpus/                          # T&F speech files
├── prompts/                         # Copied prompt templates  
├── results/                         # Analysis outputs
│   ├── speech_01_aragacuba/
│   ├── speech_02_porto_velho/
│   ├── [...]/
│   └── speech_09_ultima_live/
└── CORPUS_ANALYSIS_SUMMARY.md       # Final synthesis
```

### Step 2: Copy Required Files
**From sim1 to sim2/prompts/:**
- `stage_1_discovery.txt`
- `stage_2_populism_prompt.txt`  
- `stage_2_pluralism_prompt.txt`
- `stage_3_competitive_analysis.txt`
- `stage_4_framework_fit.txt`

**From T&F corpus to sim2/corpus/:**
Copy all 9 speech files from:
`0_workspace/byu_populism_project/populism in brazil 2018/speeches-zip/rev-transcripts/`

### Step 3: Verify File Integrity
Ensure each speech file contains:
- Timestamped Portuguese transcript
- Complete speech content (not truncated)
- Readable format for analysis

## Execution Protocol

### CRITICAL: Sequential Processing Required
Execute stages 1-4 for EACH speech before moving to next speech. Do NOT parallelize across speeches - complete one speech fully, then proceed to next.

### For Each Speech (1-9):

#### Stage 1: Discovery Analysis
1. **Input**: Complete speech transcript
2. **Prompt**: `stage_1_discovery.txt` with `{speech_text}` substituted
3. **Output**: `speech_XX_stage1_discovery.md`
4. **Focus**: Identify emergent themes without framework bias

#### Stage 2A: Populism Assessment  
1. **Input**: Complete speech transcript
2. **Prompt**: `stage_2_populism_prompt.txt` with `{speech_text}` substituted
3. **Output**: `speech_XX_stage2a_populism.md`
4. **Focus**: Systematic populism evaluation with Brazilian context

#### Stage 2B: Pluralism Assessment
1. **Input**: Complete speech transcript  
2. **Prompt**: `stage_2_pluralism_prompt.txt` with `{speech_text}` substituted
3. **Output**: `speech_XX_stage2b_pluralism.md`
4. **Focus**: Systematic pluralism evaluation

#### Stage 3: Competitive Analysis
1. **Input**: Stage 2A + 2B results
2. **Prompt**: `stage_3_competitive_analysis.txt` with results substituted
3. **Output**: `speech_XX_stage3_competitive.md`
4. **Focus**: Archetype identification, competitive dynamics

#### Stage 4: Framework Fit Assessment
1. **Input**: All previous stage results
2. **Prompt**: `stage_4_framework_fit.txt` with results substituted  
3. **Output**: `speech_XX_stage4_framework_fit.md`
4. **Focus**: Framework appropriateness validation

### File Naming Convention
```
speech_01_aracatuba_stage1_discovery.md
speech_01_aracatuba_stage2a_populism.md
speech_01_aracatuba_stage2b_pluralism.md
speech_01_aracatuba_stage3_competitive.md
speech_01_aracatuba_stage4_framework_fit.md
```

## Quality Standards

### Analytical Rigor
- **Portuguese Competency**: Maintain original quotes with English translations
- **Brazilian Context**: Demonstrate understanding of 2018 political climate, Operation Car Wash, military references
- **Evidence-Based**: Support every assessment with direct textual quotes
- **Confidence Calibration**: Honest uncertainty acknowledgment

### Cultural Context Requirements
- **Anti-Corruption Context**: Operation Car Wash influence on political discourse
- **Military References**: 1964-1985 dictatorship historical context
- **Religious Elements**: Evangelical political influence
- **Regional Dynamics**: Northeast/South political tensions
- **Economic Context**: 2016-2018 economic crisis impact

### Methodological Adherence
- **Sequential Execution**: Complete all stages for one speech before proceeding
- **Prompt Fidelity**: Follow prompt instructions exactly without deviation
- **Variable Substitution**: Accurate replacement of template variables
- **Output Format**: Structured markdown following specified formats

## Expected Outcomes by Speech

### Low Populism Speeches (Scores 0.0-0.4)
**Porto Velho (0.0)**: Should show minimal populist themes, focus on policy/administration
**Early Campaign (0.3-0.4)**: Mixed themes with weak populist elements

### Medium Populism Speeches (Score 0.7)  
**Post-First Round (0.7)**: Strong populist themes but missing key elements

### High Populism Speeches (Score 0.9)
**Late Campaign (0.9)**: Comprehensive populist themes, clear archetype patterns

### Temporal Pattern Validation
Your analysis should reveal **progressive populist intensification** from August to October, matching Eduardo's observed pattern.

## Success Criteria

### Framework Validation
- [ ] **High Framework Fit**: Most speeches show >80% coverage by populism/pluralism framework
- [ ] **Appropriate Confidence**: High confidence for clear cases, medium for ambiguous
- [ ] **Cultural Competency**: Brazilian context demonstrated throughout
- [ ] **Temporal Progression**: Analysis captures escalation pattern

### Analytical Quality
- [ ] **Evidence-Based**: Every assessment supported by textual quotes
- [ ] **Archetype Identification**: Clear classification of competitive patterns  
- [ ] **Comparative Insight**: Differences between speeches analytically explained
- [ ] **Framework Appropriateness**: Accurate assessment of when framework fits vs. doesn't

### Methodological Validation
- [ ] **Coordinate-Free Success**: Rich analysis without mathematical constraints
- [ ] **Discovery Effectiveness**: Stage 1 captures themes Stage 2+ might miss
- [ ] **Sequential Value**: Each stage builds meaningfully on previous stages
- [ ] **Scalability**: Methodology works across diverse speech types

## Warning Flags

### Analysis Quality Issues
- **Generic Assessments**: Analysis could apply to any political speech
- **Framework Forcing**: Artificially finding populism/pluralism where it doesn't exist
- **Cultural Blindness**: Missing Brazilian-specific context and markers
- **Confidence Miscalibration**: False certainty on ambiguous content

### Methodological Problems  
- **Stage Dependencies**: Later stages don't build on earlier analysis
- **Template Failure**: Prompts don't generate expected analytical structure
- **Evidence Weakness**: Assessments not supported by specific textual quotes
- **Pattern Mismatch**: Temporal progression doesn't align with Eduardo's pattern

## Final Deliverable: Corpus Analysis Summary

After completing all 9 speeches, create `CORPUS_ANALYSIS_SUMMARY.md` containing:

### Cross-Speech Pattern Analysis
- **Temporal Progression**: How populism evolves August → October
- **Archetype Distribution**: Frequency of different competitive patterns
- **Framework Performance**: Which speeches show high vs. low framework fit
- **Brazilian Context Validation**: How well analysis captures cultural specificity

### Methodological Assessment
- **Coordinate-Free Validation**: Does approach preserve analytical detail?
- **Sequential Protocol Effectiveness**: Value added by each analytical stage
- **Scalability Evidence**: Framework performance across diverse speech types
- **Comparison with Eduardo**: How AI analysis aligns with expert human assessment

### Research Insights
- **Populist Communication Evolution**: Insights into campaign discourse strategy
- **Framework Refinement**: Suggestions for improving coordinate-free approach
- **Brazilian Innovation**: Contributions to populism analysis methodology
- **Academic Validation**: Rigor demonstration for peer review

## Research Significance

This analysis will:
1. **Validate Coordinate-Free Framework**: Test across real political corpus
2. **Demonstrate LLM Analytical Capability**: Show AI can match expert human analysis
3. **Advance Populism Research**: Provide new insights into Brazilian political discourse
4. **Pioneer Methodology**: Model for future LLM-enabled discourse analysis

---

**Execute this analysis with systematic rigor. You are testing both the framework's analytical power and the viability of LLM-enabled discourse analysis methodology. Success here validates a new paradigm for computational social science research.** 