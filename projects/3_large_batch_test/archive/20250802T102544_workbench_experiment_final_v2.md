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
  American political discourse has undergone a measurable transformation from
  pluralist-patriotic rhetoric to ethno-populist discourse, with party platforms
  serving as institutional amplifiers that codify more extreme rhetoric than
  individual candidates typically express in speeches.

research_questions:
  - "How has American presidential discourse evolved from 1992-2025?"
  - "When and why do populist and nationalist rhetoric decouple in presidential discourse?"
  - "Do party platforms exhibit different rhetorical characteristics than candidate speeches?"
  - "Which presidents/periods show independent populist vs. nationalist appeals?"

hypotheses:
  H1_Temporal_Shift: "Mean populism scores increased significantly after 2016 (pre-2016 < 0.4, post-2016 > 0.6)"
  H2_Partisan_Asymmetry: "Republican documents score ≥0.2 points higher than Democratic documents on both populism and nationalism axes"
  H3_Platform_Moderation: "Party platforms score 0.1-0.3 points lower on populism than candidate speeches from the same campaign season"
  H4_Decoupling_Events: "Identifiable periods/candidates show populism-nationalism decoupling with correlation r < 0.3, revealing strategic rhetorical independence"
  H5_Presidential_Consistency: "Individual presidents maintain consistent rhetorical signatures (within-president variance < 0.15)"
  H6_Document_Type_Profiles: "Each document type exhibits distinct populism profiles within presidential cycles (platforms, SOTU, inaugurals show statistically different means)"
  H7_Framework_Reliability: "v7.1 experimental framework achieves >90% successful score extraction with <$0.10 cost per run"
  H8_Change_Point_Detection: "Statistical change point analysis identifies a single primary inflection point for populist rhetoric emergence"

success_criteria:
  - "Achieve >90% successful score extraction from all 63 documents"
  - "Detect statistically significant change point with temporal shift (p < 0.05)"
  - "Confirm Republican-Democratic score differences ≥0.2 points on both axes"
  - "Validate platform moderation hypothesis with 0.1-0.3 point difference"
  - "Identify decoupling periods with populism-nationalism correlation r < 0.3"
  - "Maintain total experiment cost under $0.10 with Flash Lite"
  - "Complete full analysis pipeline in <10 minutes"
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