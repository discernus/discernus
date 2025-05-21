# Model Comparison Analysis - Jefferson's First Inaugural Address

## 1. Tabular Comparison

### Reasoning LLMs

| Metric | Claude 3.7 Sonnet Thinking | Perplexity R1 1776 | OpenAI o4-mini |
|--------|---------------------------|-------------------|----------------|
| MPS | 0.9 | 0.9 | 0.9 |
| DPS | 0.4 | 0.4 | 0.3 |
| COM | (0.0, 0.6) | (0.0, 0.6) | (0.0, 0.3) |
| Top 3 Wells | Hope (0.9), Dignity (0.8), Justice (0.8) | Hope (0.9), Dignity (0.8), Justice/Pragmatism (0.8) | Dignity (1.0), Justice (1.0), Hope (0.9) |
| Bottom 3 Wells | All negative wells (0.1) | Manipulation/Resentment (0.0), others (0.1) | All negative wells (0.1) |

### Standard LLMs

| Metric | Perplexity Sonar | Claude 3.7 Sonnet | GPT-4.1 | Gemini 2.5 Pro | Grok 3 Beta | Le Chat |
|--------|-----------------|------------------|---------|----------------|------------|----------|
| MPS | 0.9 | 0.9 | 0.87 | 0.9 | 0.9 | 0.8 |
| DPS | 0.4 | 0.4 | 0.44 | 0.4 | 0.9 | 0.2 |
| COM | (0.0, 0.3) | (0.0, 2.6) | (0.0, 0.6) | (0.0, 0.3) | (0.0, 0.5) | (0.5, 0.5) |
| Top 3 Wells | Various (0.7-0.9) | Justice (0.85) | Various | Similar to Perplexity | Truth/Pragmatism (0.9) | Dignity (0.9), Truth/Hope (0.8) |
| Bottom 3 Wells | All negative low | All negative low | All negative low | All negative low | Higher DPS (0.9) | All negative (0.1) |

## 2. Initial Observations

### Reasoning LLMs Consensus
- Consistent MPS of 0.9 across all three
- Similar DPS (0.3-0.4 range)
- Strong agreement on Hope and Dignity as top wells
- Uniform treatment of negative wells
- COM positioning shows remarkable consistency in x=0

### Standard LLMs Variations
- More variance in metrics, especially DPS (0.2-0.9)
- COM positions show greater variation
- Le Chat shows unique lateral COM displacement
- Grok 3 Beta shows notably higher DPS
- Claude 3.7 Sonnet shows extreme vertical COM displacement

### Key Differences Between Groups
1. Reasoning LLMs show more consistency in:
   - Metric scores
   - Well rankings
   - COM positioning
   - Treatment of negative dimensions

2. Standard LLMs show more variation in:
   - DPS scores
   - COM positioning
   - Interpretation of positive dimensions

## 3. Areas for Deeper Analysis

1. Why do reasoning LLMs show such consistency in their analysis?
2. What accounts for the significant DPS variation in standard LLMs?
3. Why does Le Chat show unique lateral COM displacement?
4. What factors contribute to Grok 3 Beta's high DPS?
5. Is Claude 3.7 Sonnet's extreme COM displacement meaningful?

*Note: This is an initial analysis. Further investigation of specific patterns and potential causative factors will follow.* 