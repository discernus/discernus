---
version: "7.0"
name: presidential_populism_emergence_study_enhanced
description: |
  Enhanced longitudinal analysis of American political discourse (1992-2025) using
  the Political Discourse Analysis Framework v7.1 with explicit schema mapping and enhanced gasket
  architecture. This experiment validates the v7.1 framework's ability to detect
  precise temporal shifts, partisan asymmetries, and institutional vs. individual
  rhetorical differences through quantifiable hypotheses.
  
  Key innovations:
  - Political Discourse Analysis Framework v7.1 with enhanced linguistic markers
  - Explicit schema mapping for improved data extraction
  - Comprehensive platform coverage (63 documents including 17 party platforms)
  - Document processing standards v7.0 compliance (all PDFs converted to text)
  - Quantifiable hypotheses with specific numerical thresholds
  - Party platform vs. candidate rhetoric comparison with measurable differences

hypothesis: |
  American political discourse has undergone measurable temporal evolution in
  populist rhetoric intensity, with party platforms serving as institutional
  amplifiers that exhibit more extreme populist rhetoric than individual
  candidate speeches, while maintaining distinct strategic deployment of
  populist and nationalist rhetorical dimensions.

research_questions:
  - "How has American presidential discourse evolved from 1992-2025?"
  - "When and why do populist and nationalist rhetoric decouple in presidential discourse?"
  - "Do party platforms exhibit different rhetorical characteristics than candidate speeches?"
  - "Do Democratic presidents adapt their rhetoric in response to high-populist Republican predecessors or successors?"
  - "Which presidents/periods show independent populist vs. nationalist appeals?"

hypotheses:
  H1_Temporal_Evolution: "American presidential discourse shows measurable temporal shifts in populist rhetoric intensity, with at least one statistically significant change point detectable through correlation and trend analysis"
  H2_Partisan_Asymmetry: "Republican documents score significantly higher than Democratic documents on both populism and nationalism dimensions (≥0.2 point difference, p < 0.05)"
  H3_Platform_Amplification: "Party platforms exhibit more extreme populist rhetoric than individual candidate speeches from the same campaign season (platforms score 0.1-0.3 points higher on populism)"
  H4_Strategic_Decoupling: "Specific presidents or periods demonstrate strategic rhetorical independence where populism and nationalism scores show weak correlation (r < 0.3), indicating tactical message differentiation"
  H5_Presidential_Signatures: "Individual presidents maintain consistent rhetorical signatures across different speech contexts (within-president variance < 0.15 on both populism and nationalism)"
  H6_Institutional_Moderation: "Institutional documents (SOTU, joint sessions) exhibit more moderate rhetoric than campaign-oriented documents (inaugurals, platforms) within the same presidential cycle"
  H7_Rhetorical_Adaptation: "Democratic presidents exhibit elevated populist rhetoric when preceded or followed by high-populist Republican administrations, showing measurable adaptation to the prevailing rhetorical environment (≥0.15 point increase above Democratic baseline)"
  H8_Dimensional_Independence: "Populism and nationalism represent analytically distinct rhetorical strategies, with overall corpus correlation r < 0.7, allowing independent strategic deployment"

success_criteria:
  - "Achieve >90% successful score extraction from all 72 documents"
  - "Detect temporal evolution patterns with statistical significance (p < 0.05)"
  - "Confirm Republican-Democratic score differences ≥0.2 points on both dimensions"
  - "Validate platform amplification hypothesis with 0.1-0.3 point higher scores"
  - "Identify strategic decoupling instances with populism-nationalism correlation r < 0.3"
  - "Demonstrate presidential signature consistency (within-president variance < 0.15)"
  - "Confirm institutional vs. campaign document moderation patterns"
  - "Detect rhetorical adaptation patterns (Democrats showing ≥0.15 point increase when adjacent to high-populist Republicans)"
  - "Establish dimensional independence with overall correlation r < 0.7"
  - "Generate publication-ready statistical results with confidence intervals"

model:
  analysis: "vertex_ai/gemini-2.5-flash-lite"
  synthesis: "vertex_ai/gemini-2.5-flash-lite"

framework: "framework.md"
corpus_path: "corpus/"

document_processing_standards:
  max_file_size: "500KB"
  preferred_format: "txt"
  required_metadata: ["document_id", "title", "author", "date", "document_type", "party", "year"]
  content_quality:
    min_characters: 1000
    min_paragraphs: 3
    encoding: "UTF-8"
  validation_checks:
    - "File size within model limits"
    - "Content quality meets minimum standards"
    - "Metadata completeness for all documents"
    - "Corpus manifest accuracy"

metadata_enhancements:
  party_platforms:
    comparison_group: "candidate_speeches"
    hypothesis: "Platforms will be less populist/nationalist than candidates"
    analysis_dimensions:
      - "populism_pluralism_score"
      - "nationalism_patriotism_score"
      - "populist_intensity_index"
      - "democratic_institutionalism_index"
  document_types:
    speech_types: ["inaugural", "state_of_union", "joint_session"]
    platform_types: ["party_platform", "resolution"]
    comparison_analysis: "institutional_vs_individual_rhetoric"

corpus_validation:
  pre_analysis_checks:
    - "Verify all documents under size limits"
    - "Validate metadata completeness"
    - "Check corpus manifest accuracy"
    - "Test document encoding and quality"
  error_handling:
    oversized_files: "reject_with_clear_error"
    missing_metadata: "warn_with_defaults"
    encoding_issues: "auto_convert_to_utf8"
    empty_content: "reject_with_explanation"

expected_outcomes:
  statistical_analysis:
    - "Temporal trend analysis with change point detection"
    - "Partisan difference testing with ANOVA"
    - "Document type comparison (platforms vs. speeches)"
    - "Correlation analysis between populism and nationalism"
  cost_efficiency:
    target_cost: "$0.05-0.10"
    target_success_rate: "95%+"
    target_processing_time: "<5 minutes"
  quality_metrics:
    - "Framework score extraction success rate"
    - "Statistical analysis completion rate"
    - "Evidence curation quality"
    - "Results interpretation coherence"
--- 