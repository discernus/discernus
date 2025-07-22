# Van der Veen 2019 Replication - Micro Experiment

## Experiment Configuration

```yaml
name: "Van der Veen 2019 Populist Language Classification - PDAF v1.3 Replication (Micro)"
description: "Micro-scale replication of Van der Veen 2019 populist discourse classification using enhanced tension-aware populist analysis framework"
framework_file: "framework.md"
corpus: "corpus"

# Research Context
research_question: "Can PDAF v1.3 tension-enhanced analysis replicate and extend Van der Veen 2019 findings on populist language patterns in 2016 presidential candidates?"
hypothesis: "PDAF v1.3 will identify populist patterns consistent with Van der Veen findings while revealing strategic tension patterns not captured in original analysis"

# Original Study Reference
original_paper: "projects/vanderveen/paper_source_materials/Classifying_populist_language_in_American_presiden.rtf"
replication_type: "methodological_extension" # Using different but related framework

# Experiment Workflow
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

# Expected Corpus Analysis
corpus_composition:
  republican_speeches: 3  # Trump (2), Cruz (1)
  democratic_speeches: 2  # Sanders (2) 
  party_platforms: 2     # Republican + Democratic 2016
  total_documents: 7
  
  populist_expectations:
    trump_speeches: "high_populist_intensity_with_strategic_tensions"
    sanders_speeches: "moderate_to_high_populist_intensity_different_patterns"
    cruz_speech: "moderate_populist_intensity_ideological_variant"
    party_platforms: "lower_populist_intensity_institutional_language"

# Replication Parameters
comparison_focus:
  - "Populist vs non-populist classification accuracy vs Van der Veen"
  - "Cross-candidate populist pattern differences"
  - "Cross-party populist strategic coherence analysis"
  - "NEW: Strategic tension patterns not available in original study"
  
validation_approach:
  - "Qualitative comparison with Van der Veen populist classifications"
  - "Cross-ideological populist pattern analysis"
  - "Strategic coherence assessment using PDAF v1.3 tension mathematics"
  
# Enhancement Beyond Original Study
tension_analysis_additions:
  - "Democratic-Authoritarian populist tension quantification"
  - "Internal-External focus populist strategic patterns" 
  - "Crisis-Elite attribution tension measurement"
  - "Populist Strategic Contradiction Index (PSCI) assessment"
  - "Cross-candidate strategic coherence comparison"

# Success Criteria
replication_success_metrics:
  basic_replication: "PDAF classifications align with Van der Veen populist/non-populist findings"
  methodological_extension: "Tension analysis reveals strategic patterns invisible to original method"
  research_contribution: "Provides deeper insight into populist strategic communication architecture"
  
analytical_depth:
  - "Quantitative populist intensity scoring for each document"
  - "Strategic tension pattern identification and measurement" 
  - "Cross-candidate populist strategic coherence comparison"
  - "Party platform vs candidate speech populist pattern analysis"

# Academic Standards
provenance_requirements:
  - "Complete methodology documentation for replication"
  - "Comparison tables with Van der Veen original classifications"
  - "Statistical analysis of populist pattern differences"
  - "Methodological enhancement documentation"
  
output_requirements:
  - "Academic-quality replication report"
  - "Van der Veen comparison analysis"
  - "PDAF v1.3 tension analysis findings"
  - "Methodological enhancement assessment"
```

## Expected Research Contribution

### Replication Value
- **Methodological validation** of populist discourse computational analysis
- **Cross-framework comparison** between Van der Veen approach and PDAF v1.3
- **2016 election populist discourse systematic documentation**

### Extension Value  
- **Strategic tension quantification** unavailable in original study
- **Cross-ideological populist coherence analysis** using tension mathematics
- **Enhanced populist strategic communication understanding**

### Academic Impact
- **Reproducible computational populist analysis**
- **Framework enhancement documentation** 
- **Methodological contribution to populist studies**

---

## Corpus Asset Summary

**Republican Assets (3 documents)**:
- `us.2016.Trump.Announcement.6-16.docx` - Key populist moment
- `us.2016.Trump.7-21.docx` - Mid-campaign populist messaging
- `us.2016.Cruz.Announcement.3-23.docx` - Alternative Republican populist variant

**Democratic Assets (2 documents)**:
- `us.2016.Sanders.Announcement.5-26.docx` - Key left-populist moment  
- `us.2016.Sanders.3-15.docx` - Mid-campaign populist messaging

**Institutional Assets (2 documents)**:
- `us.2016.RepublicanPartyPlatform.pdf` - Official institutional language
- `us.2016.DemocraticPartyPlatform.pdf` - Official institutional language

**Total**: 7 balanced documents enabling systematic populist pattern analysis with institutional comparison.

---

**Research Question Focus**: Can enhanced tension-aware populist analysis replicate and extend academic findings while revealing strategic patterns invisible to original methodology? 