# Prompt Engineering Examples

This directory contains example prompts and test cases for the Prompt Engineering Harness.

## 📝 Available Examples

### Basic Analysis Prompts

- **`basic_analysis.txt`** - General political discourse analysis
  - Main arguments, rhetorical devices, emotional appeals
  - Target audience and political orientation
  - Structured analysis format

### Specialized Analysis Prompts

- **`moral_foundations.txt`** - Moral Foundations Theory analysis
  - Care/Harm, Fairness/Cheating, Loyalty/Betrayal
  - Authority/Subversion, Sanctity/Degradation
  - Intensity ratings and strategic implications

- **`populist_rhetoric.txt`** - Populist discourse analysis
  - Anti-elite language, people vs. elite framing
  - Crisis rhetoric, simplification, emotional appeals
  - Left-wing vs. right-wing populism identification

## 🧪 Using Examples

### Test with Direct Prompt

```bash
python3 scripts/prompt_engineering/harness.py \
  --model "vertex_ai/gemini-2.5-pro" \
  --prompt-file "scripts/prompt_engineering/examples/basic_analysis.txt"
```

### Test with Experiment Assets

```bash
python3 scripts/prompt_engineering/harness.py \
  --model "vertex_ai/gemini-2.5-pro" \
  --experiment "projects/simple_test_cff" \
  --corpus "speech1.txt"
```

## 🎯 Creating New Examples

### Template Structure

1. **Clear Role Definition**: "You are a [specialist/expert] in [domain]"
2. **Specific Analysis Tasks**: Numbered or bulleted requirements
3. **Output Format**: Specify desired response structure
4. **Evidence Requirements**: Ask for specific examples from text

### Example Template

```text
You are a [DOMAIN] specialist. Analyze the following text for:

**Analysis Areas:**
1. [Area 1]: [Description]
2. [Area 2]: [Description]
3. [Area 3]: [Description]

**Requirements:**
- [Specific requirement 1]
- [Specific requirement 2]
- [Output format specification]

Provide evidence from the text to support your analysis.
```

## 🔗 Integration with Experiments

These examples can be adapted for:
- **Framework-specific prompts** in experiment configurations
- **Agent prompt templates** for specialized analysis
- **Validation prompts** for testing model capabilities
- **Training prompts** for prompt engineering development

## 📚 Best Practices

1. **Be Specific**: Clear, unambiguous instructions
2. **Include Examples**: Show expected output format
3. **Set Constraints**: Define response length and style
4. **Test Iteratively**: Small changes, measure impact
5. **Document Evolution**: Track prompt improvements over time

---

**Note**: These examples are starting points. Adapt and refine them based on your specific research needs and model performance.
