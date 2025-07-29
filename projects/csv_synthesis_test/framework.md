# Rhetorical Analysis Framework

This framework analyzes rhetorical patterns in political speeches.

## Dimensions

### Virtues
- unity (0-1): Emphasis on bringing people together
- hope (0-1): Positive vision for the future
- truth (0-1): Factual accuracy and honesty
- justice (0-1): Fairness and equality

### Vices
- division (0-1): Us vs them rhetoric
- fear (0-1): Emphasis on threats and dangers
- deception (0-1): Misleading or false statements
- injustice (0-1): Unfairness and inequality

## Analysis Instructions

For each document:
1. Identify key themes and rhetorical devices
2. Score each dimension on a scale of 0.0-1.0
3. Provide evidence quotes for each dimension
4. Calculate composite scores

## Output Contract

```json
{
  "dimension_groups": {
    "virtues": ["unity", "hope", "truth", "justice"],
    "vices": ["division", "fear", "deception", "injustice"]
  },
  "scoring": {
    "scale": {
      "min": 0.0,
      "max": 1.0,
      "step": 0.1
    }
  },
  "evidence": {
    "required_per_dimension": 1,
    "max_per_dimension": 3
  }
}
``` 