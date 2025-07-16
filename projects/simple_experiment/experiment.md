# Simple Experiment

This experiment will analyze the tone and main idea of Shakespeare's sonnet 18 ('Shall I compare thee to a summer's day?').

**Hypothesis**: The sonnet will have a predominantly positive tone (defined as >70% positive words/phrases) and its main idea will be a celebration of beauty.

```yaml
models:
  - "anthropic/claude-3-haiku-20240307"
num_runs: 1
statistical_plan:
  required_tests:
    - test_name: "tone_analysis"
      scope: "sentiment_analysis"
    - test_name: "main_idea_analysis"
      scope: "concept_extraction"
  validation_status: "complete"
``` 