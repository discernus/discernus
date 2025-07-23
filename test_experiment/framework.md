# Simple Sentiment Analysis Framework v1.0

## Overview
This framework analyzes text sentiment and thematic content.

## Dimensions

### Sentiment Score
- Scale: 1-5 (1=Very Negative, 5=Very Positive)
- Measures overall emotional tone of the text

### Urgency Level  
- Scale: 1-5 (1=No Urgency, 5=Highly Urgent)
- Assesses the perceived urgency of issues discussed

### Complexity Score
- Scale: 1-5 (1=Simple, 5=Very Complex)
- Evaluates the complexity of topics and language

## Output Format
Return analysis as JSON:
```json
{
  "sentiment_score": 3,
  "urgency_level": 4,
  "complexity_score": 3
}
``` 