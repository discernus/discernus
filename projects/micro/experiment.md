# Micro Test Experiment

## Abstract
Complete pipeline validation with 4 documents, 2 dimensions, 2 derived metrics, and statistical analysis. Tests end-to-end integration including calculation agents and statistical synthesis with minimal computational cost.

## Research Questions
- How do sentiment categories differ in positive and negative sentiment scores?
- What are the patterns in net sentiment and sentiment magnitude across different sentiment categories?
- What descriptive patterns emerge between positive and negative sentiment groups?

## Expected Outcomes
Descriptive analysis of sentiment scores between positive and negative sentiment categories, including descriptive statistics, derived metric calculations, and pattern identification.

## Reliability Filtering Parameters

**Testing Parameterized Filtering**: This experiment tests the new reliability filtering system with different threshold settings.

```yaml
reliability_filtering:
  salience_threshold: 0.2          # Lower threshold for testing (default: 0.3)
  confidence_threshold: 0.0        # No confidence filtering (default: 0.0)
  reliability_threshold: 0.15      # Lower reliability threshold (default: 0.25)
  reliability_calculation: "confidence_x_salience"  # Standard method
  framework_fit_required: false   # No framework fit requirement
  framework_fit_threshold: 0.3    # Default framework fit threshold

# Advanced filtering for testing
advanced_filtering:
  dimension_specific_thresholds:   # Per-dimension overrides for testing
    positive_sentiment: 0.1        # Very low threshold for positive sentiment
    negative_sentiment: 0.3        # Higher threshold for negative sentiment
  exclude_dimensions: []           # No exclusions
  include_dimensions: []           # No forced inclusions
```

## Data Grouping and Custom Variable Mapping

**Primary Analysis Variable**: sentiment_category (positive vs negative)
- Two groups: positive (n=2), negative (n=2)
- Sample size N=4 suitable for descriptive analysis and case study patterns

**Statistical Analysis Requirements**:
- Descriptive statistics for all dimensions and derived metrics
- Pattern analysis between sentiment categories
- Basic measurement consistency checks (reliability analysis not feasible with N=4)

---

```yaml
# --- Start of Machine-Readable Appendix ---

# 5.1: Metadata (Required)
metadata:
  experiment_name: "micro_test_experiment"
  author: "Test Suite"
  spec_version: "10.0"

# 5.2: Components (Required)
components:
  framework: "framework.md"
  corpus: "corpus.md"

# 5.3: Hypotheses (Optional but Recommended)
hypotheses:
  - id: "H1"
    description: "Positive sentiment documents show higher positive sentiment scores than negative sentiment documents"
    falsifiable: true
    mutually_exclusive: true
    collective_exhaustive: true
  - id: "H2"
    description: "Negative sentiment documents show higher negative sentiment scores than positive sentiment documents"
    falsifiable: true
    mutually_exclusive: true
    collective_exhaustive: true
  - id: "H3"
    description: "There are observable patterns between positive and negative sentiment groups in descriptive analysis"
    falsifiable: true
    mutually_exclusive: true
    collective_exhaustive: true

# --- End of Machine-Readable Appendix ---
```
