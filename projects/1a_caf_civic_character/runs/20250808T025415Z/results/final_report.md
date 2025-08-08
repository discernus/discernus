# Speaker Character Pattern Analysis
Framework: Civic Analysis Framework (CAF) v7.3
Run ID: [PLACEHOLDER]
Date: [PLACEHOLDER]

## Executive Summary

This experiment evaluated speaker differentiation and character patterns using the CAF framework across a corpus of political speeches. Key findings suggest potential speaker-specific character signatures, though statistical validation was limited by sample constraints. The framework demonstrated utility in identifying distinct virtue-vice patterns, particularly in justice and dignity dimensions. Primary limitations include small sample sizes and potential temporal bias across different speech eras.

## Collaborator Section

### H1: Speaker Differentiation
**Hypothesis**: The 10 CAF dimensions will show statistically significant differences between speakers
**Testability**: Not testable due to insufficient samples per speaker for ANOVA

Evidence suggests dimensional variation between speakers, particularly in truth and hope dimensions. For example, Cory Booker demonstrates high truth scores: "We know there is no deeper proclivity to commit crimes among people of color, but there is a much deeper bias in the way that our drug laws have been and are being applied" [1]. This contrasts with hope-focused rhetoric: "Like people, our nation has demonstrated the capacity to change" [2].

### H2: Character Signatures
**Hypothesis**: Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices
**Testability**: Partially testable through pattern analysis, though statistical significance testing is limited

Evidence indicates distinct character patterns. Booker emphasizes justice: "We profess - we actually swear an oath to the flag - that we are a nation of liberty and justice for all" [3]. AOC demonstrates high dignity scores: "If you are willing to fight for working people regardless of who they are, how they identify, or where they come from, you are welcome here" [4].

### H3: MC-SCI Coherence
**Hypothesis**: MC-SCI scores will vary meaningfully between speakers, indicating different levels of character coherence
**Testability**: Not testable due to insufficient samples for statistical comparison

Limited evidence suggests variation in character coherence. Compare Booker's measured truth claims [5] with Sanders' more dramatic fantasy-oriented rhetoric: "They live in another planet. They own mansions all over the world" [6].

## Evidence References

[1] cory_booker_2018_first_step_act.txt, dimension: truth, confidence: 0.9
[2] cory_booker_2018_first_step_act.txt, dimension: hope, confidence: 0.9
[3] cory_booker_2018_first_step_act.txt, dimension: justice, confidence: 0.95
[4] alexandria_ocasio_cortez_2025_fighting_oligarchy.txt, dimension: dignity, confidence: 0.9
[5] cory_booker_2018_first_step_act.txt, dimension: truth, confidence: 0.9
[6] bernie_sanders_2025_fighting_oligarchy.txt, dimension: fantasy, confidence: 0.7

## Technical Transparency

Limitations:
- Insufficient samples per speaker for ANOVA testing
- Temporal variation between speeches (2018-2025) may confound speaker differences
- Single evaluations per document limit reliability assessment
- Uneven representation across speakers

Models:
- Analysis: vertex_ai/gemini-2.5-pro
- Synthesis: vertex_ai/gemini-2.5-pro

Cost Summary: [PLACEHOLDER]

---

## Research Transparency: Computational Cost Analysis

### Cost Summary
**Total Cost**: $0.7788 USD  
**Total Tokens**: 235,272  
**Run Timestamp**: 20250808T025415Z  

### Cost Breakdown by Operation
- **Individual Document Analysis**: $0.6475 USD (198,360 tokens, 4 calls, $0.1619 avg/call)
- **Raw Data Analysis Planning**: $0.0636 USD (17,634 tokens, 1 calls, $0.0636 avg/call)
- **Derived Metrics Analysis Planning**: $0.0676 USD (19,278 tokens, 1 calls, $0.0676 avg/call)

### Cost Breakdown by Model
- **anthropic/claude-3-5-sonnet-20241022**: $0.7788 USD (235,272 tokens, 6 calls)

### Cost Breakdown by Agent
- **EnhancedAnalysisAgent**: $0.6475 USD (198,360 tokens, 4 calls)
- **RawDataAnalysisPlanner**: $0.0636 USD (17,634 tokens, 1 calls)
- **DerivedMetricsAnalysisPlanner**: $0.0676 USD (19,278 tokens, 1 calls)

### Methodology Note
This research was conducted using the Discernus computational research platform, ensuring complete transparency in computational costs. All LLM interactions are logged with exact token counts and costs for reproducibility and academic integrity.

**Cost Calculation**: Based on provider pricing at time of execution  
**Token Counting**: Exact tokens reported by LLM providers  
**Audit Trail**: Complete logs available in experiment run directory  
