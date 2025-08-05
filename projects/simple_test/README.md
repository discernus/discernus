# Simple Test Experiment

This is a minimal validation test for the Discernus v7.1 architecture using the Character Assessment Framework v7.3.

## Configuration

This experiment is configured to use **Gemini 2.5 Flash Lite** for both analysis and synthesis to enable:
- **Fast execution** (~47 seconds vs ~3+ minutes)
- **Low cost** (~$0.014 USD vs ~$0.27 USD)
- **Rapid iteration** for testing and development

The configuration is set in `.discernus.yaml`:
```yaml
analysis_model: vertex_ai/gemini-2.5-flash-lite
synthesis_model: vertex_ai/gemini-2.5-flash-lite
```

## Usage

### From within the experiment directory:
```bash
cd projects/simple_test
discernus run .
```

### From project root:
```bash
# Note: This will use global config (Pro for synthesis)
discernus run projects/simple_test

# To use the local Flash Lite config:
cd projects/simple_test && discernus run .
```

## Expected Results

- **Character Differentiation**: Measurable differences between McCain (institutional) and Sanders (populist) discourse
- **MC-SCI Validation**: Coherence metrics reflecting different discourse styles  
- **Architecture Testing**: Successful v7.1 JSON synthesis pipeline execution
- **Cost Efficiency**: ~$0.014 USD per run with Flash Lite models