# Micro Test Experiment

## Abstract
Complete pipeline validation with 4 documents, 2 dimensions, 2 derived metrics, and statistical analysis. Tests end-to-end integration including calculation agents and statistical synthesis with minimal computational cost.

## Research Questions
- How do sentiment categories differ in positive and negative sentiment scores?
- What are the patterns in net sentiment and sentiment magnitude across different sentiment categories?
- Are there significant differences between positive and negative sentiment groups in ANOVA analysis?

## Expected Outcomes
Statistical comparison of sentiment scores between positive and negative sentiment categories, including ANOVA analysis, descriptive statistics, and derived metric calculations.

## Data Grouping and Custom Variable Mapping

**Primary Analysis Variable**: sentiment_category (positive vs negative)
- Two groups: positive (n=2), negative (n=2)
- Both groups meet ANOVA requirements (n≥2)

**Statistical Analysis Requirements**:
- ANOVA comparison between sentiment categories
- Descriptive statistics for all dimensions and derived metrics
- Reliability analysis for measurement consistency

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
  framework: "sentiment_binary_v1.md"
  corpus: "corpus.md"

# 5.3: Hypotheses (Optional but Recommended)
hypotheses:
  - id: "H1"
    description: "Positive sentiment documents show significantly higher positive sentiment scores than negative sentiment documents"
    falsifiable: true
    mutually_exclusive: true
    collective_exhaustive: true
  - id: "H2"
    description: "Negative sentiment documents show significantly higher negative sentiment scores than positive sentiment documents"
    falsifiable: true
    mutually_exclusive: true
    collective_exhaustive: true
  - id: "H3"
    description: "There are significant differences between positive and negative sentiment groups in ANOVA analysis"
    falsifiable: true
    mutually_exclusive: true
    collective_exhaustive: true

# --- End of Machine-Readable Appendix ---
```
