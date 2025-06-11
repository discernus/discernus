# Multi-LLM Testing Guide for Narrative Gravity Analysis

You're ready to test with **ChatGPT, Claude, and Mistral**! Here's your complete testing workflow.

## 🚀 Quick Start (5 minutes)

### Step 1: Generate Your Prompt
```bash
# Generate interactive prompt for civic virtue framework
python generate_prompt.py --framework civic_virtue --mode interactive

# Generate other frameworks
python generate_prompt.py --framework political_spectrum --mode api
python generate_prompt.py --framework moral_rhetorical_posture --mode api
```

### Step 2: Test with LLMs
1. **Copy the generated prompt**
2. **Go to your preferred LLM:**
   - ChatGPT: https://chat.openai.com
   - Claude: https://claude.ai
   - Mistral: https://chat.mistral.ai
3. **Paste the prompt + your text**
4. **Copy the JSON response**

### Step 3: Visualize Results
```bash
# Launch your visualization app
python launch_app.py
# OR
streamlit run narrative_gravity_app.py
```
Then paste the JSON into the app for instant visualization!

## 📊 Testing Framework Comparison

### Test the Same Text Across All Models

**Sample Text (Trump's 2025 SOTU):**
```
We must unite as Americans to build a stronger, more just society where every person has the opportunity to succeed through hard work and determination.
```

**Testing Matrix:**

| Framework | ChatGPT | Claude | Mistral |
|-----------|---------|--------|---------|
| Civic Virtue | ✅ Test | ✅ Test | ✅ Test |
| Political Spectrum | ✅ Test | ✅ Test | ✅ Test |
| Moral Rhetorical Posture | ✅ Test | ✅ Test | ✅ Test |

## 🔧 Available Frameworks

### 1. **Civic Virtue Framework** (Most Advanced)
- **Focus**: Moral analysis of political discourse
- **Wells**: Dignity/Tribalism, Truth/Manipulation, Justice/Resentment, Hope/Fantasy, Pragmatism/Fear
- **Best for**: Political speeches, policy arguments, civic discourse

### 2. **Political Spectrum Framework**
- **Focus**: Left-right political positioning
- **Wells**: Traditional political dimensions
- **Best for**: Partisan analysis, ideological positioning

### 3. **Moral Rhetorical Posture Framework**
- **Focus**: Communication style and approach
- **Wells**: Rhetorical strategies and moral appeals
- **Best for**: Communication analysis, rhetorical assessment

## 📝 Sample Test Prompts

### For ChatGPT:
```
[Paste your generated prompt here]

Please analyze this text: "We must unite as Americans to build a stronger, more just society where every person has the opportunity to succeed through hard work and determination."
```

### For Claude:
```
[Paste your generated prompt here]

Text to analyze: "We must unite as Americans to build a stronger, more just society where every person has the opportunity to succeed through hard work and determination."
```

### For Mistral:
```
[Paste your generated prompt here]

Analyze: "We must unite as Americans to build a stronger, more just society where every person has the opportunity to succeed through hard work and determination."
```

## 🎯 What to Look For

### Expected JSON Format:
```json
{
  "title": "Analysis Title",
  "model_name": "ChatGPT",
  "model_version": "GPT-4", 
  "framework": "civic_virtue",
  "scores": {
    "Dignity": 0.8,
    "Tribalism": 0.2,
    "Truth": 0.7,
    "Manipulation": 0.1,
    "Justice": 0.6,
    "Resentment": 0.3,
    "Hope": 0.8,
    "Fantasy": 0.2,
    "Pragmatism": 0.7,
    "Fear": 0.1
  },
  "analysis": "This text demonstrates strong alignment with integrative civic values..."
}
```

### Key Comparisons to Track:
1. **Score Consistency**: Do models give similar scores for the same text?
2. **Reasoning Quality**: Which model provides best analysis explanations?
3. **Framework Sensitivity**: How do scores change across frameworks?
4. **Bias Detection**: Any systematic biases in model responses?

## 🔄 Automated Testing (Advanced)

If you want to automate testing (requires API keys):

### 1. Set up API credentials:
```bash
# Add to your .env file:
OPENAI_API_KEY=your_openai_key
ANTHROPIC_API_KEY=your_anthropic_key
MISTRAL_API_KEY=your_mistral_key
```

### 2. Use the multi-LLM tester:
```bash
# Quick comparison test
python test_multi_llm.py --quick --framework civic_virtue

# Full comprehensive test
python test_multi_llm.py --framework civic_virtue
```

## 📈 Results Analysis

### Visualization Options:
1. **Streamlit App**: Interactive plots and comparisons
2. **Direct Visualization**: 
   ```python
   from narrative_gravity_elliptical import NarrativeGravityWellsElliptical
   analyzer = NarrativeGravityWellsElliptical()
   output_path = analyzer.create_visualization(your_json_data)
   ```

### Comparison Metrics:
- **Inter-model agreement**: How consistent are scores across models?
- **Framework sensitivity**: How much do scores vary by framework?
- **Reasoning quality**: Which model provides most insightful analysis?

## 🚨 Troubleshooting

### Common Issues:
1. **JSON Format Errors**: Make sure LLM returns valid JSON
2. **Score Scale Issues**: Ensure scores are 0.0-1.0, not 1-10
3. **Missing Fields**: Check all required fields are present

### Quick Fixes:
```bash
# Test your setup
python test_huggingface_setup.py

# Validate framework configs
python framework_manager.py summary

# Check prompt generation
python generate_prompt.py --framework civic_virtue --mode interactive
```

## 📚 Sample Texts for Testing

### Political Speeches:
- Trump's 2025 SOTU (already in `reference_texts/`)
- Obama speeches
- Biden speeches

### Policy Arguments:
- Healthcare reform proposals
- Climate change statements
- Economic policy announcements

### Persuasive Content:
- Editorial articles
- Campaign materials
- Social media posts

## 🎉 Ready to Test!

You now have everything needed to test your Narrative Gravity Maps with ChatGPT, Claude, and Mistral:

1. ✅ **Working infrastructure**
2. ✅ **Generated prompts** 
3. ✅ **Visualization system**
4. ✅ **Testing frameworks**
5. ✅ **Sample texts**

**Start testing and compare how different LLMs analyze the same content!** 🚀 