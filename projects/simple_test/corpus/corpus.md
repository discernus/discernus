# Democratic Discourse Corpus v7.1

## Overview
A comparative corpus examining social cohesion patterns in contrasting approaches to democratic discourse. This research-grade corpus contains two paradigmatic examples of American political communication: institutional gracious concession versus populist anti-establishment critique.

## Collection Methodology
Documents were selected from public domain sources representing distinct democratic discourse styles. Selection criteria prioritized rhetorical authenticity, temporal significance, and analytical contrast potential for social cohesion research.

## Ethical Considerations
All documents are public domain political speeches with no privacy concerns. Content represents legitimate democratic discourse and is used for academic research purposes examining social cohesion patterns.

## Corpus Description
This corpus contains two documents spanning institutional and populist approaches to American democratic discourse, selected to enable comparative analysis of social cohesion signatures across different rhetorical strategies.

## Support for Analytical Goals
The corpus structure supports comparative analysis through consistent metadata fields enabling statistical grouping by speaker, party, ideology, and temporal variables. Document selection ensures sufficient contrast for meaningful social cohesion pattern differentiation.

## File Manifest

```json
{
  "corpus_version": "v7.1",
  "file_manifest": [
    {
      "name": "john_mccain_2008_concession.txt",
      "document_type": "concession_speech",
      "party": "Republican",
      "year": 2008,
      "temporal_sequence": 1,
      "speaker": "John McCain",
      "ideology": "conservative",
      "discourse_style": "institutional",
      "event": "Presidential Concession Speech",
      "word_count": 1247,
      "source": "Public Domain"
    },
    {
      "name": "bernie_sanders_2025_fighting_oligarchy.txt",
      "document_type": "floor_speech", 
      "party": "Independent",
      "year": 2025,
      "temporal_sequence": 2,
      "speaker": "Bernie Sanders",
      "ideology": "progressive",
      "discourse_style": "populist",
      "event": "Senate Floor Speech on Economic Inequality",
      "word_count": 892,
      "source": "Public Domain"
    }
  ],
  "field_naming_standards": {
    "required_consistency": ["document_type", "party", "speaker", "year"],
    "prohibited_variations": {
      "speech_type": "document_type",
      "political_party": "party",
      "author": "speaker"
    }
  },
  "statistical_readiness": {
    "grouping_variables": ["party", "speaker", "document_type"],
    "temporal_variables": ["year", "temporal_sequence"]
  }
}
```

## Research Context

This corpus enables comparative analysis of social cohesion patterns in democratic discourse, featuring:

1. **Democratic Discourse Contrast**: Institutional (McCain) vs Populist (Sanders) approaches
2. **Temporal Span**: 2008-2025, capturing different eras of American political communication
3. **Rhetorical Diversity**: Gracious concession vs systemic critique discourse styles
4. **Social Cohesion Analysis**: Optimized for CFF v7.3 framework dimensions
5. **Statistical Reliability**: Consistent field naming enables robust comparative analysis

## Expected Social Cohesion Patterns

**McCain (Institutional)**: Higher cohesion indices (dignity, hope, amity, cohesive goals)
**Sanders (Populist)**: Higher fragmentative elements (tribal dominance, enmity) with strategic contradictions

## Analytical Capabilities

This corpus supports:
- **Comparative Analysis**: Statistical grouping by party, speaker, and discourse style
- **Temporal Analysis**: Chronological ordering via temporal_sequence field
- **Social Cohesion Research**: Framework-agnostic metadata supporting CFF v7.3 analysis
- **Democratic Resilience Studies**: Contrasting discourse types for impact assessment