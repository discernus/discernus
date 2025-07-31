---
name: "political_moral_analysis"
description: |
  This experiment validates the Moral Foundations Theory v4.2 Tension Enhanced 
  framework using a diverse corpus of American political speeches. The corpus 
  includes 8 speeches from different ideological positions, historical periods 
  (1963-2022), and contexts (electoral, legislative, policy advocacy). While 
  this heterogeneous design limits causal inference about ideology, it provides 
  a robust test of the framework's analytical capabilities across varied 
  political discourse contexts.

hypothesis: |
  This diverse political corpus will demonstrate measurable variation in moral 
  foundation emphasis patterns across speakers and contexts, with the Moral 
  Strategic Contradiction Index (MSCI) revealing different patterns of moral 
  rhetorical coherence. While temporal and contextual factors limit 
  generalizability, this experiment will validate the framework's capacity to 
  detect and quantify moral foundation patterns in political discourse.

framework: "framework.md"
corpus_path: "corpus/"
models:
  - "vertex_ai/gemini-2.5-pro"
runs_per_model: 3
analysis_variant: "default"
---

# Political Moral Analysis Experiment

## Overview

This experiment validates the Moral Foundations Theory v4.2 Tension Enhanced framework using a diverse corpus of American political speeches spanning 60 years of political discourse.

## Research Question

Can computational moral analysis reliably detect and quantify moral foundation patterns across diverse political contexts, speakers, and historical periods?

## Methodology

### Framework
**Moral Foundations Theory v4.2 Tension Enhanced** provides:
- Six moral foundation pairs (Care/Harm, Fairness/Cheating, Loyalty/Betrayal, Authority/Subversion, Sanctity/Degradation, Liberty/Oppression)
- Moral Strategic Contradiction Index (MSCI) for measuring rhetorical contradictions
- Salience-enhanced analysis capturing rhetorical emphasis patterns

### Corpus Composition
8 diverse political speeches representing:
- **Ideological Spectrum**: Progressive (Sanders, AOC) to Conservative (Romney, McCain, King)
- **Historical Range**: 1963 (Lewis) to 2022 (Vance)
- **Contextual Variety**: Electoral, legislative, policy advocacy, civil rights

### Expected Outcomes
1. **Validation**: Framework successfully processes diverse political discourse
2. **Variation**: Measurable differences in moral foundation emphasis patterns
3. **Coherence Analysis**: MSCI reveals different patterns of moral rhetorical consistency
4. **Framework Testing**: Robust assessment of analytical capabilities across contexts

## Significance

This experiment tests whether computational moral analysis can provide reliable, quantifiable insights into moral reasoning patterns in political discourse, establishing baseline performance for the enhanced framework. 