# Sentiment Binary Framework v1.0

## Abstract & Raison d'être

**What is this framework?**
A minimalist framework for measuring basic positive vs negative sentiment to validate pipeline functionality.

**What problem does it solve?**
Provides the simplest possible framework to test end-to-end integration of the Discernus analysis pipeline.

**Who is it for?**
Test suite developers and pipeline maintainers who need to validate system functionality with minimal computational cost.

## Theoretical Foundations

This framework is grounded in basic sentiment analysis theory, measuring the presence of positive and negative emotional language in text.

## Analytical Methodology

**Dimensions:**
- Positive Sentiment (0.0-1.0): Presence of positive language and optimistic expressions
- Negative Sentiment (0.0-1.0): Presence of negative language and pessimistic expressions

## Intended Application & Corpus Fit

**Target Corpus Description**: Short text documents with clear emotional content.

**Known Limitations**: Designed for testing purposes only, not for serious sentiment analysis.

---

```yaml
metadata:
  framework_name: "sentiment_binary_v1"
  framework_version: "1.0.0"
  author: "Test Suite"
  spec_version: "10.0"

analysis_variants:
  default:
    description: "Basic sentiment analysis"
    analysis_prompt: |
      You are analyzing text for sentiment. Score 0.0-1.0 for each dimension.

      POSITIVE SENTIMENT: Look for praise, optimism, success words, enthusiasm
      - 0.9-1.0: Dominant positive language throughout
      - 0.7-0.8: Strong positive presence
      - 0.4-0.6: Moderate positive elements
      - 0.1-0.3: Weak positive indicators
      - 0.0: No positive language

      NEGATIVE SENTIMENT: Look for criticism, pessimism, failure words, despair
      - 0.9-1.0: Dominant negative language throughout
      - 0.7-0.8: Strong negative presence
      - 0.4-0.6: Moderate negative elements
      - 0.1-0.3: Weak negative indicators
      - 0.0: No negative language

dimensions:
  - name: "positive_sentiment"
    description: "Positive language presence"
    markers:
      positive_examples:
        - "great"
        - "excellent"
        - "success"
        - "wonderful"
        - "fantastic"
      negative_examples:
        - "terrible"
        - "failure"
        - "awful"
        - "disastrous"
    scoring_calibration:
      high: "0.7-1.0: Strong positive presence"
      medium: "0.4-0.6: Moderate positive elements"
      low: "0.1-0.3: Weak positive indicators"
      absent: "0.0: No positive language"

  - name: "negative_sentiment"
    description: "Negative language presence"
    markers:
      positive_examples:
        - "bad"
        - "terrible"
        - "failure"
        - "awful"
        - "disastrous"
      negative_examples:
        - "good"
        - "excellent"
        - "wonderful"
        - "fantastic"
    scoring_calibration:
      high: "0.7-1.0: Strong negative presence"
      medium: "0.4-0.6: Moderate negative elements"
      low: "0.1-0.3: Weak negative indicators"
      absent: "0.0: No negative language"

derived_metrics: []

output_schema:
  type: object
  properties:
    dimensional_scores:
      type: object
      properties:
        positive_sentiment: {$ref: "#/definitions/score_object"}
        negative_sentiment: {$ref: "#/definitions/score_object"}
  required: ["dimensional_scores"]
  definitions:
    score_object:
      type: object
      properties:
        raw_score: {type: number, minimum: 0.0, maximum: 1.0}
        salience: {type: number, minimum: 0.0, maximum: 1.0}
        confidence: {type: number, minimum: 0.0, maximum: 1.0}
        evidence: {type: string}
      required: ["raw_score", "salience", "confidence", "evidence"]
```
