---
name: "populist_rhetoric_study"
description: |
  This experiment analyzes populist communication strategies and rhetorical coherence 
  across Donald Trump's presidential speeches using the Cohesive Flourishing Framework 
  v4.4 Tension Enhanced. The corpus includes Trump's 2017 Inaugural Address, his 2017 address to a joint 
  session of Congress, State of the Union addresses (2018-2020), and his 2025 
  address to a joint session of Congress, 
  providing comprehensive coverage of presidential populist rhetoric patterns. The framework's Strategic Contradiction 
  Index (SCI) will reveal the coherence and tension patterns in populist 
  communication strategies.

hypothesis: |
  Trump's presidential rhetoric will demonstrate measurably distinct populist 
  communication patterns characterized by high tension scores between opposing 
  dimensions (Unifying vs Divisive, Individual vs Collective), elevated Strategic 
  Contradiction Index (SCI) scores indicating strategic overreach, and consistent 
  salience patterns emphasizing crisis/threat rhetoric over flourishing/opportunity 
  themes across the presidential tenure.

framework: "framework.md"
corpus_path: "corpus/"
models:
  - "vertex_ai/gemini-2.5-pro"
runs_per_model: 3
analysis_variant: "default"
---

# Populist Rhetoric Study

## Overview

This experiment analyzes the rhetorical strategies and strategic coherence in Donald Trump's presidential speeches using the Cohesive Flourishing Framework v4.4 Tension Enhanced, focusing on populist communication patterns.

## Research Question

How do populist communication strategies manifest in presidential rhetoric, and what patterns of strategic coherence or contradiction emerge across different speech contexts?

## Methodology

### Framework
**Cohesive Flourishing Framework v4.4 Tension Enhanced** provides:
- Multi-dimensional rhetorical analysis (Unifying/Divisive, Individual/Collective, Crisis/Opportunity)
- Strategic Contradiction Index (SCI) for measuring tension and coherence
- Salience-weighted analysis for strategic priority identification

### Corpus Composition
6 Trump presidential speeches spanning his presidency:
- **2017 Inaugural Address**: Foundational presidential rhetoric
- **2017 Joint Session Address**: Early presidential policy vision
- **State of the Union (2018-2020)**: Annual presidential communications
- **2025 Joint Session Address**: Recent presidential communication

### Expected Outcomes
1. **Populist Pattern Identification**: Quantified populist communication characteristics
2. **Strategic Coherence Analysis**: SCI scores revealing tension patterns
3. **Temporal Evolution**: Changes in rhetorical strategies over time
4. **Framework Validation**: Testing CFF's capacity for populist discourse analysis

## Significance

This experiment provides systematic analysis of populist presidential rhetoric, offering insights into strategic communication patterns and testing the framework's analytical capabilities for political discourse characterized by populist elements. 