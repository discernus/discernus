# Sentiment Binary Framework v1.0

## Abstract & Raison d'être

**What is this framework?**
A minimalist framework for measuring basic positive vs negative sentiment with derived metrics to validate complete pipeline functionality including statistical analysis.

**What problem does it solve?**
Provides a framework that triggers derived metrics calculation and statistical analysis while maintaining minimal computational cost.

**Who is it for?**
Test suite developers and pipeline maintainers who need to validate the complete pipeline including calculation agents and statistical synthesis.

## Theoretical & Empirical Foundations

This framework is grounded in basic sentiment analysis theory, measuring the presence of positive and negative emotional language in text with derived balance metrics.

**Key Citations:**
- Pang, B., & Lee, L. (2008). Opinion mining and sentiment analysis. Foundations and Trends in Information Retrieval, 2(1-2), 1-135. This foundational work established the theoretical basis for computational sentiment analysis.
- Liu, B. (2012). Sentiment analysis and opinion mining. Synthesis Lectures on Human Language Technologies, 5(1), 1-167. Provides comprehensive theoretical foundations for sentiment analysis methodologies.

## Analytical Methodology

**Dimensions:**
- Positive Sentiment (0.0-1.0): Presence of positive language and optimistic expressions
- Negative Sentiment (0.0-1.0): Presence of negative language and pessimistic expressions

**Derived Metrics:**
- Net Sentiment: Balance between positive and negative sentiment (positive - negative)
- Sentiment Magnitude: Average emotional intensity (positive + negative) / 2

## Intended Application & Corpus Fit

**Target Corpus Description**: Short text documents with clear emotional content, organized by sentiment categories for statistical comparison.

**Known Limitations**: Designed for testing purposes only, not for serious sentiment analysis.

---

```yaml
metadata:
  framework_name: "sentiment_with_derived_metrics_v1"
  framework_version: "1.0.0"
  author: "Test Suite"
  spec_version: "10.0"

analysis_variants:
  default:
    description: "Basic sentiment analysis with derived metrics"
    analysis_prompt: |
      You are analyzing text for sentiment. Score 0.0-1.0 for each dimension.

      POSITIVE SENTIMENT: Look for praise, optimism, success words, enthusiasm
      - 0.9-1.0: Dominant positive language throughout
      - 0.7-0.8: Strong positive elements present
      - 0.4-0.6: Balanced or mixed sentiment
      - 0.1-0.3: Some positive elements but mostly neutral/negative
      - 0.0: No positive sentiment detected

      NEGATIVE SENTIMENT: Look for criticism, pessimism, failure words, disappointment
      - 0.9-1.0: Dominant negative language throughout
      - 0.7-0.8: Strong negative elements present
      - 0.4-0.6: Balanced or mixed sentiment
      - 0.1-0.3: Some negative elements but mostly neutral/positive
      - 0.0: No negative sentiment detected

    dimensions:
      - name: "positive_sentiment"
        definition: "Presence of positive language and optimistic expressions"
        min_score: 0.0
        max_score: 1.0
        scoring_guide: |
          0.0: No positive sentiment detected
          0.25: Minimal positive elements
          0.5: Moderate positive sentiment
          0.75: Strong positive sentiment
          1.0: Dominant positive language throughout
      - name: "negative_sentiment"
        definition: "Presence of negative language and pessimistic expressions"
        min_score: 0.0
        max_score: 1.0
        scoring_guide: |
          0.0: No negative sentiment detected
          0.25: Minimal negative elements
          0.5: Moderate negative sentiment
          0.75: Strong negative sentiment
          1.0: Dominant negative language throughout

    derived_metrics:
      - name: "net_sentiment"
        description: "Balance between positive and negative sentiment"
        calculation: "positive_sentiment - negative_sentiment"
        interpretation: |
          > 0: Net positive sentiment
          = 0: Balanced sentiment
          < 0: Net negative sentiment
      - name: "sentiment_magnitude"
        description: "Average emotional intensity"
        calculation: "(positive_sentiment + negative_sentiment) / 2"
        interpretation: |
          > 0.5: High emotional intensity
          0.25-0.5: Moderate emotional intensity
          < 0.25: Low emotional intensity

    analysis_notes: |
      This is a test framework for pipeline validation. Use only for testing purposes.
      The dimensions are intentionally simple to test the complete pipeline.

output_schema:
  type: object
  required:
    - dimensional_scores
    - evidence
    - marked_up_document
  properties:
    dimensional_scores:
      type: object
      required:
        - positive_sentiment
        - negative_sentiment
      properties:
        positive_sentiment:
          $ref: "#/definitions/score_object"
        negative_sentiment:
          $ref: "#/definitions/score_object"
    evidence:
      type: array
      items:
        type: object
        required:
          - dimension
          - quote_text
          - confidence
        properties:
          dimension:
            type: string
          quote_text:
            type: string
          confidence:
            type: number
            minimum: 0.0
            maximum: 1.0
    marked_up_document:
      type: string

definitions:
  score_object:
    type: object
    required:
      - raw_score
      - salience
      - confidence
    properties:
      raw_score:
        type: number
        minimum: 0.0
        maximum: 1.0
      salience:
        type: number
        minimum: 0.0
        maximum: 1.0
      confidence:
        type: number
        minimum: 0.0
        maximum: 1.0
```
