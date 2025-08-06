# Score Validation Quick Reference

**THIN Academic Validation in <5 Minutes**

## Basic Usage

```bash
# Validate any score
discernus validate-score <experiment> <document> <score_name> --score-value <value>

# Example
discernus validate-score projects/simple_test "speech.txt" "dignity_score" --score-value 0.65
```

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--score-value` | Numerical score to validate | **Required** |
| `--confidence` | Confidence level (0.0-1.0) | `0.8` |
| `--model` | LLM model for validation | Auto-detected |
| `--output` | Save report to file | Console output |
| `--framework` | Framework name | Auto-detected |

## Validation Report

```
# Score Validation Report
Document: speech.txt
Score: dignity_score = 0.65 (confidence: 0.8)
Framework: cff_v7.3
Validation Time: 3.3 seconds

## Score Grounding
- Evidence Found: True
- Primary Evidence: "key supporting text"
- Grounding Strength: strong

## Evidence Quality
- Relevance: high
- Specificity: high  
- Quality Score: 0.90

## Academic Validation
- Methodology Sound: True
- Transparency Adequate: True
- Peer Review Ready: True
- Validation Confidence: 0.85

## Recommendations
- List of specific improvements
```

## Model Consistency

**Auto-Detection**: Tool automatically detects analysis model
**Consistency Check**: Validates model match for academic integrity
**Override**: Use `--model` to specify different model

## Common Use Cases

### Peer Review
```bash
# Reviewer validates computational claims
discernus validate-score projects/study "document.txt" "score" --score-value 0.75
```

### Research Development  
```bash
# Test scoring methodology
discernus validate-score projects/test "sample.txt" "test_score" --score-value 0.6
```

### Quality Assurance
```bash
# Save validation report
discernus validate-score projects/study "doc.txt" "score" --score-value 0.75 --output report.md
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| `Model mismatch` | Use `--model` to match analysis model |
| `Analysis artifact not found` | Ensure experiment has been run |
| `Framework version mismatch` | Update to compatible framework version |

## Performance

- **Target**: <5 minutes
- **Typical**: 3-4 seconds
- **Cost**: $0.001-0.005 per validation (Flash Lite)

## THIN Architecture

- **LLM Intelligence**: Delegates validation to LLM
- **Framework Agnostic**: Works with any research framework  
- **Durable Infrastructure**: Simple, maintainable code
- **Cost Effective**: Uses appropriate models

---

**Quick Start**: `discernus validate-score projects/simple_test "doc.txt" "score" --score-value 0.75` 