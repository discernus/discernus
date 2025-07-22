---
# --- Discernus Configuration ---

# REQUIRED: A unique, machine-readable name for the experiment.
name: simple_shakespeare_analysis

# REQUIRED: A human-readable description of the experiment's purpose.
description: |
  Simple demonstration experiment analyzing Shakespeare's sonnet 18 for tone and main idea
  to validate basic system functionality.

# REQUIRED: A specific, falsifiable hypothesis to be tested.
hypothesis: |
  The sonnet will have a predominantly positive tone (defined as >70% positive words/phrases) 
  and its main idea will be a celebration of beauty.

framework_file: framework.md
corpus: corpus/
models:
  - "anthropic/claude-3-haiku-20240307"
runs_per_model: 1
workflow:
  - agent: AnalysisAgent
  
---

# Simple Experiment

This experiment analyzes Shakespeare's sonnet 18 ('Shall I compare thee to a summer's day?') for tone and thematic content using basic computational analysis.