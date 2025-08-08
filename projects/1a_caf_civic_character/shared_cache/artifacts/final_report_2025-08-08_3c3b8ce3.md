# Speaker Character Pattern Analysis
Framework: Civic Analysis Framework (CAF) v7.3
Run ID: [Placeholder]
Date: [Placeholder]

## Executive Summary
This experiment evaluated speaker differentiation and character patterns using the CAF framework across a corpus of political speeches. While the statistical power was limited by sample size constraints, qualitative evidence suggests distinct character signatures between speakers, particularly in dimensions of dignity, justice, and truth. The analysis revealed meaningful variation in civic character coherence, though formal hypothesis testing was constrained by the available data.

## Collaborator Section

### H1: Speaker Differentiation
**Hypothesis**: The 10 CAF dimensions will show statistically significant differences between speakers
**Testability**: Not testable due to insufficient sample size for ANOVA

While statistical testing was not possible, qualitative evidence shows contrasting patterns. For example, McCain demonstrated high dignity: "Whatever our differences, we are fellow Americans, and please believe me when I say no association has ever meant more to me than that" [1]. Booker emphasized hope: "Like people, our nation has demonstrated the capacity to change. We as a nation have demonstrated the capacity to improve" [2].

### H2: Character Signatures
**Hypothesis**: Each speaker will exhibit a unique character signature across the 5 virtues and 5 vices
**Testability**: Partially testable through pattern analysis

Evidence suggests distinct character profiles, particularly in justice framing. Booker emphasized systemic reform: "We profess - we actually swear an oath to the flag - that we are a nation of liberty and justice for all. But our criminal justice system violates those values" [3]. Romney focused on personal duty: "As a senator-juror, I swore an oath before God to exercise impartial justice" [4]. McCain emphasized dignity and unity: "Whatever our differences, we are fellow Americans" [5].

### H3: MC-SCI Coherence Patterns
**Hypothesis**: MC-SCI scores will vary meaningfully between speakers, indicating different levels of character coherence
**Testability**: Testable through pattern analysis

Character coherence varied notably between speakers. Romney demonstrated integrated truth-seeking: "The House managers presented evidence supporting their case... I sought to hear testimony from John Bolton" [6]. In contrast, King showed lower coherence: "I can read this Constitution and understand what it means" [7]. McCain maintained consistency through compromise-oriented pragmatism: "I pledge to him tonight to do all in my power to help him lead us through the many challenges we face" [8].

## Evidence References
[1] john_mccain_2008_concession.txt, dignity, 0.95
[2] cory_booker_2018_first_step_act.txt, hope, 0.90
[3] cory_booker_2018_first_step_act.txt, justice, 0.95
[4] mitt_romney_2020_impeachment.txt, justice, 0.95
[5] john_mccain_2008_concession.txt, dignity, 0.95
[6] mitt_romney_2020_impeachment.txt, truth, 0.90
[7] steve_king_2017_house_floor.txt, truth, 0.85
[8] john_mccain_2008_concession.txt, pragmatism, 0.85

## Technical Transparency

Limitations:
- Insufficient sample size for ANOVA testing of H1
- Single-rater analysis without inter-rater reliability validation
- Temporal variation in corpus (1963-2025) may introduce era effects
- Uneven distribution of speech contexts and types

Models:
- vertex_ai/gemini-2.5-pro

Cost Summary:
[Not provided in input data]

---

## Research Transparency: Computational Cost Analysis

### Cost Summary
**Total Cost**: $0.7633 USD  
**Total Tokens**: 230,248  
**Run Timestamp**: 20250808T030048Z  

### Cost Breakdown by Operation
- **Individual Document Analysis**: $0.6318 USD (193,314 tokens, 4 calls, $0.1579 avg/call)
- **Raw Data Analysis Planning**: $0.0637 USD (17,637 tokens, 1 calls, $0.0637 avg/call)
- **Derived Metrics Analysis Planning**: $0.0679 USD (19,297 tokens, 1 calls, $0.0679 avg/call)

### Cost Breakdown by Model
- **anthropic/claude-3-5-sonnet-20241022**: $0.7633 USD (230,248 tokens, 6 calls)

### Cost Breakdown by Agent
- **EnhancedAnalysisAgent**: $0.6318 USD (193,314 tokens, 4 calls)
- **RawDataAnalysisPlanner**: $0.0637 USD (17,637 tokens, 1 calls)
- **DerivedMetricsAnalysisPlanner**: $0.0679 USD (19,297 tokens, 1 calls)

### Methodology Note
This research was conducted using the Discernus computational research platform, ensuring complete transparency in computational costs. All LLM interactions are logged with exact token counts and costs for reproducibility and academic integrity.

**Cost Calculation**: Based on provider pricing at time of execution  
**Token Counting**: Exact tokens reported by LLM providers  
**Audit Trail**: Complete logs available in experiment run directory  
