# Complete Brazilian Political Speech Analysis Instructions
## Coordinate-Free Discourse Analysis Protocol
### Date: 2025-01-01

---

## **MISSION & METHODOLOGY**

### Core Mission
Conduct systematic discourse analysis of Brazilian political speeches from the 2018 presidential election using a coordinate-free analytical framework. Your goal is thorough, unbiased analysis without any external expectations or target outcomes.

### Critical Methodological Principles

**What You HAVE Access To:**
- Clean speech transcripts (8 speeches available)
- Analysis prompt templates for each stage
- Brazilian political context information
- Coordinate-free analytical framework specification

**What You DO NOT Have Access To:**
- Any external validation data or target scores
- Previous analysis results or expectations
- Information about experimental design or validation goals
- Any predetermined outcomes or scoring expectations

**Analytical Integrity Requirements:**
- **No Contamination**: You have no target knowledge to influence your analysis
- **Genuine Assessment**: Provide your honest analytical evaluation
- **Evidence-Based**: Support all claims with specific textual evidence
- **Systematic**: Apply the same analytical rigor to all speeches
- **Unbiased**: Let themes emerge naturally without forcing predetermined patterns

---

## **CORPUS & CONTEXT**

### Available Speeches (Clean Transcripts)
**Primary Analysis Corpus** (start with these 3):
- `speech_01_aracatuba.txt` - August 23: Campaign rally speech (65 lines)
- `speech_02_porto_velho.txt` - August 31: Campaign rally speech (356 lines)
- `speech_03_juiz_de_fora.txt` - September 6: Business association address (323 lines)

**Extended Corpus** (available for expansion):
- `speech_04_apos_atentado.txt` - September 16: After assassination attempt (788 lines)
- `speech_05_dia_antes_eleicoes.txt` - October 6: One day before elections (116 lines)
- `speech_06_first_round_victory.txt` - October 16: After first round victory (125 lines)
- `speech_07_ultima_live_2o_turno.txt` - October 27: Final live before second round (212 lines)
- `speech_08_paulista_avenue.txt` - October 22: Paulista Avenue rally (272 lines)

### Brazilian Political Context (2018)
Consider the following environmental factors:
- Operation Car Wash anti-corruption investigations
- Economic crisis and political polarization
- Military dictatorship historical references (1964-1985)
- Evangelical political influence growth
- Regional political dynamics and tensions

---

## **ANALYTICAL FRAMEWORK**

### 4-Stage Sequential Analysis Protocol
Execute stages 1-4 for each speech in order. Complete all stages for one speech before proceeding to the next.

**Stage 1: Discovery Analysis**
- Identify 3-5 main themes in each speech
- Focus on emergent patterns without predefined categories
- Use `clean_prompts/stage_1_discovery_clean.txt`
- Support all findings with textual evidence

**Stage 2A: Populism Assessment**
- Evaluate presence and characteristics of populist themes
- Use systematic assessment criteria (presence, salience, intensity, consistency)
- Apply `clean_prompts/stage_2a_populism_clean.txt`
- Maintain Brazilian cultural context awareness

**Stage 2B: Pluralism Assessment**
- Evaluate presence and characteristics of pluralist themes
- Apply same systematic criteria as populism assessment
- Use `clean_prompts/stage_2b_pluralism_clean.txt`
- Assess independently from populism findings

**Stage 3: Competitive Analysis**
- Analyze how populist and pluralist themes interact
- Identify patterns of opposition, coexistence, or dominance
- Apply `clean_prompts/stage_3_competitive_clean.txt`
- Determine coherency patterns and strategic messaging

**Stage 4: Framework Fit Assessment**
- Evaluate how well populism/pluralism framework captures the speech
- Assess coverage percentage, relevance, and explanatory power
- Use `clean_prompts/stage_4_framework_fit.txt`
- Identify themes beyond framework scope
- Provide honest assessment of analytical limitations

---

## **EXECUTION PROTOCOL**

### Step 1: Setup Results Directory Structure
Create the following directory structure:
```
sim3/
├── results/
│   ├── speech_01_aracatuba/
│   ├── speech_02_porto_velho/
│   └── speech_03_juiz_de_fora/
```

### Step 2: Begin with Araçatuba Speech (Complete All Stages)
1. **Stage 1**: Use `clean_corpus/speech_01_aracatuba.txt` + `clean_prompts/stage_1_discovery_clean.txt`
   - Save as: `results/speech_01_aracatuba/speech_01_aracatuba_stage1_discovery.md`

2. **Stage 2A**: Use same speech + `clean_prompts/stage_2a_populism_clean.txt`
   - Save as: `results/speech_01_aracatuba/speech_01_aracatuba_stage2a_populism.md`

3. **Stage 2B**: Use same speech + `clean_prompts/stage_2b_pluralism_clean.txt`
   - Save as: `results/speech_01_aracatuba/speech_01_aracatuba_stage2b_pluralism.md`

4. **Stage 3**: Use same speech + `clean_prompts/stage_3_competitive_clean.txt`
   - Save as: `results/speech_01_aracatuba/speech_01_aracatuba_stage3_competitive.md`

5. **Stage 4**: Use same speech + `clean_prompts/stage_4_framework_fit.txt`
   - Save as: `results/speech_01_aracatuba/speech_01_aracatuba_stage4_framework_fit.md`

### Step 3: Continue Sequential Analysis
Repeat complete 4-stage analysis for:
- `speech_02_porto_velho.txt` (save in `results/speech_02_porto_velho/`)
- `speech_03_juiz_de_fora.txt` (save in `results/speech_03_juiz_de_fora/`)

### Step 4: Optional Expansion
If additional validation desired, continue with speeches 4-8 following the same protocol.

---

## **QUALITY STANDARDS & DELIVERABLES**

### Quality Requirements
**Analytical Rigor:**
- Support assessments with direct Portuguese quotes + English translations
- Apply Brazilian cultural context appropriately
- Follow prompt instructions exactly
- Provide honest confidence assessments

**Output Format:**
- Structured markdown format in designated results folders
- Evidence-based conclusions with specific textual support
- Cultural competency demonstrated
- Sequential stage dependencies maintained

### Expected Deliverables
**Minimum Delivery** (3 speeches):
- 15 stage analysis files (5 stages × 3 speeches)
- Organized results directory structure
- Systematic discourse analysis across corpus
- Evidence-based thematic identification
- Framework appropriateness assessment

**Extended Delivery** (8 speeches):
- 40 stage analysis files (5 stages × 8 speeches)
- Comprehensive temporal analysis across campaign period
- Robust framework validation through diverse contexts

### File Naming Convention
```
results/speech_XX_name/
├── speech_XX_name_stage1_discovery.md
├── speech_XX_name_stage2a_populism.md
├── speech_XX_name_stage2b_pluralism.md
├── speech_XX_name_stage3_competitive.md
└── speech_XX_name_stage4_framework_fit.md
```

---

## **WORKFLOW INTEGRITY**

### Execution Sequence
1. **Begin with Speech 1** (Araçatuba) - complete all 5 stages
2. **Proceed sequentially** through speeches 2-3 (minimum) or 2-8 (extended)
3. **Maintain analytical independence** - don't let earlier analyses bias later ones
4. **Focus on individual speech characteristics** rather than comparative patterns
5. **Complete all analyses** before any validation or external comparison

### Success Criteria
Your analysis will be successful when you have provided:
- Thorough, evidence-based assessment of each speech
- Honest evaluation of populist and pluralist characteristics
- Systematic application of analytical framework
- Clear identification of framework limitations and coverage gaps
- High-quality insights into Brazilian political discourse patterns

**Remember**: This is genuine analytical work, not a test with predetermined correct answers. Your independent assessment is the goal.

---

**BEGIN: Create results directory structure, then start analysis with speech_01_aracatuba.txt using stage_1_discovery_clean.txt** 