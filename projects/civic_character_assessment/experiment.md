---
name: "civic_character_assessment"
description: |
  This experiment evaluates civic virtue and character patterns in contemporary 
  American political discourse using the Character Assessment Framework v4.3 
  Tension Enhanced. The corpus includes the same diverse political speeches analyzed 
  in the moral foundations experiment, but focuses on civic character traits rather 
  than moral foundations. The framework's Moral Character Strategic Contradiction 
  Index (MC-SCI) will reveal whether political leaders demonstrate coherent civic 
  virtue or exhibit character contradictions in their public rhetoric.

hypothesis: |
  Political speakers will demonstrate measurably different civic character patterns, 
  with institutionalist speakers (Romney, McCain) showing higher Dignity and Truth 
  scores while populist speakers (Sanders, AOC, Vance) emphasize Justice and 
  Courage. The Moral Character Strategic Contradiction Index (MC-SCI) will reveal 
  systematic differences in character coherence, with experienced leaders showing 
  more coherent virtue patterns than newer political voices.

framework: "framework.md"
corpus_path: "corpus/"
models:
  - "vertex_ai/gemini-2.5-pro"
runs_per_model: 3
analysis_variant: "default"
---

# Civic Character Assessment Experiment

## Overview

This experiment evaluates civic virtue and character patterns in contemporary American political discourse using the Character Assessment Framework v4.3 Tension Enhanced, focusing on civic character traits rather than moral foundations.

## Research Question

How do civic virtues manifest in political discourse, and what patterns of character coherence or contradiction emerge across different speaker profiles and political contexts?

## Methodology

### Framework
**Character Assessment Framework v4.3 Tension Enhanced** provides:
- Civic virtue analysis (Dignity, Truth, Justice, Courage)
- Moral Character Strategic Contradiction Index (MC-SCI) for coherence measurement
- Character tension pattern analysis for rhetorical consistency assessment

### Corpus Composition
8 diverse political speeches representing:
- **Institutionalist Leaders**: Romney (impeachment), McCain (concession)
- **Populist Voices**: Sanders, AOC (economic policy), Vance (national conservatism)
- **Civil Rights Legacy**: Lewis (march on Washington)
- **Policy Advocates**: Booker (criminal justice reform)
- **Controversial Positions**: King (immigration stance)

### Expected Outcomes
1. **Character Profiling**: Quantified civic virtue patterns per speaker
2. **Coherence Analysis**: MC-SCI scores revealing character consistency patterns
3. **Speaker Typology**: Different character profiles across political roles
4. **Framework Testing**: Validation of character assessment methodology

## Significance

This experiment tests whether computational character assessment can reliably distinguish civic virtue patterns in political discourse, providing insights into how political leaders project character through rhetoric and establishing baseline performance for civic virtue analysis. 