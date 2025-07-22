---
# Van der Veen 2019 Replication - Micro Experiment

name: "Van der Veen 2019 Populist Language Classification - PDAF v1.3 Replication (Micro)"
description: |
  Micro-scale replication of Van der Veen 2019 populist discourse classification using enhanced 
  tension-aware populist analysis framework. Tests whether PDAF v1.3 can replicate academic 
  findings while revealing strategic patterns invisible to original methodology.

hypothesis: |
  PDAF v1.3 will identify populist patterns consistent with Van der Veen findings while revealing 
  strategic tension patterns not captured in original analysis. Specifically: (1) Trump speeches 
  will show high populist intensity with strategic tensions, (2) Sanders speeches will show 
  moderate-to-high populist intensity with different patterns, (3) Party platforms will show 
  lower populist intensity with institutional language patterns.

framework_file: framework.md
corpus: corpus/

workflow:
  - agent: "DataExtractionAgent"
    model: "vertex_ai/gemini-2.5-pro"
    description: "Extract text from DOCX files and prepare for populist analysis"
    
  - agent: "AnalysisAgent"
    model: "vertex_ai/gemini-2.5-pro"
    runs: 1
    description: "Apply PDAF v1.3 tension-enhanced populist analysis to each text"
    analysis_focus: "populist_discourse_patterns_with_tension"
    
  - agent: "CalculationAgent"
    model: "vertex_ai/gemini-2.5-flash"
    description: "Calculate populist intensity indices, tension scores, and strategic coherence metrics"
    
  - agent: "SynthesisAgent"
    model: "vertex_ai/gemini-2.5-pro"
    runs: 1
    description: "Synthesize findings in relation to Van der Veen original results and assess replication success"

# Research Context
research_question: "Can PDAF v1.3 tension-enhanced analysis replicate and extend Van der Veen 2019 findings on populist language patterns in 2016 presidential candidates?"
original_paper: "projects/vanderveen/paper_source_materials/Classifying_populist_language_in_American_presiden.rtf"
replication_type: "methodological_extension"

# Corpus Information  
corpus_composition:
  republican_speeches: 3  # Trump (2), Cruz (1)
  democratic_speeches: 2  # Sanders (2) 
  party_platforms: 2     # Republican + Democratic 2016
  total_documents: 7

# Success Criteria
success_metrics:
  basic_replication: "PDAF classifications align with Van der Veen populist/non-populist findings"
  methodological_extension: "Tension analysis reveals strategic patterns invisible to original method"
  research_contribution: "Provides deeper insight into populist strategic communication architecture"

---

## Van der Veen 2019 Replication Experiment

### Original Study Context

**Paper**: Van der Veen 2019 - "Classifying populist language in American presidential politics"  
**Focus**: Computational classification of populist language in 2016 presidential candidate speeches  
**Method**: Van der Veen classification approach

### Methodological Enhancement

**Enhanced Method**: PDAF v1.3 Tension Enhanced provides:
- **Strategic tension quantification** (Democratic-Authoritarian, Internal-External, Crisis-Elite)
- **Populist Strategic Contradiction Index (PSCI)** measurement
- **Cross-ideological coherence analysis** across Republican/Democratic populist patterns
- **Salience-weighted analysis** for strategic priority identification

### Balanced Micro Corpus (7 documents)

**Republican Assets (3)**:
- `us.2016.Trump.Announcement.6-16.docx` - Trump announcement speech (key populist moment)
- `us.2016.Trump.7-21.docx` - Trump mid-campaign speech (RNC period)
- `us.2016.Cruz.Announcement.3-23.docx` - Cruz announcement (alternative Republican populist variant)

**Democratic Assets (2)**:  
- `us.2016.Sanders.Announcement.5-26.docx` - Sanders announcement (key left-populist moment)
- `us.2016.Sanders.3-15.docx` - Sanders mid-campaign speech

**Institutional Comparison (2)**:
- `us.2016.RepublicanPartyPlatform.pdf` - Official Republican institutional language
- `us.2016.DemocraticPartyPlatform.pdf` - Official Democratic institutional language

### Research Questions

#### Primary Replication Question
Can PDAF v1.3 tension-enhanced analysis replicate Van der Veen 2019 populist classification findings?

#### Methodological Extension Questions
1. What strategic tension patterns emerge in 2016 populist discourse?
2. How do Republican vs Democratic populist strategies differ in coherence? 
3. Do candidate speeches vs party platforms show different populist strategic patterns?
4. What populist insights are revealed through tension analysis unavailable to original method?

### Expected Findings

**Trump speeches**: High populist intensity with strategic tensions (Democratic-Authoritarian conflicts)  
**Sanders speeches**: Moderate-to-high populist intensity with different strategic patterns  
**Cruz speech**: Moderate populist intensity with ideological variant patterns  
**Party platforms**: Lower populist intensity with institutional language patterns

### Academic Value

**Replication Contribution**:
- Methodological validation of computational populist analysis
- Cross-framework comparison between approaches
- Reproducible analysis of 2016 populist discourse

**Extension Contribution**:
- Strategic tension mathematics applied to populist studies
- Cross-ideological coherence analysis using quantitative methods
- Enhanced populist communication theory through computational analysis 