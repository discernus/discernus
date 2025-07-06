# Discernus Extension Guide for Academics

## **🎯 Overview: Add Your Favorite Tools Without Forking**

This guide shows you how to extend Discernus with your favorite libraries, tools, and expert agents without forking the entire codebase. The extension system follows THIN principles: **simple configuration files** enable complex capabilities.

---

## **🚀 Quick Start: 5-Minute Extension**

### **Step 1: Create Extension Template**
```python
from discernus.core.capability_registry import create_extension

# Create template for your domain
extension_file = create_extension("psycholinguistics", "Psychological text analysis tools")
print(f"Created: {extension_file}")
```

### **Step 2: Edit Your Extension**
Open `extensions/psycholinguistics.yaml` and customize:

```yaml
name: psycholinguistics
description: Psychological text analysis tools
version: 1.0.0
author: Dr. Academic Researcher

# Add your favorite libraries
libraries:
  - spacy
  - transformers
  - psychoanalyzer

# Define your expert agent
agents:
  psycholinguistics_expert:
    description: Expert in psychological text analysis
    prompt: |
      You are a psycholinguistics_expert specializing in psychological aspects of language.
      
      RESEARCH QUESTION: {research_question}
      SOURCE TEXTS: {source_texts}
      EXPERT REQUEST: {expert_request}
      
      Your Task:
      Analyze the psychological dimensions of language use.
      You have access to spaCy, transformers, and psychoanalyzer libraries.
      
      Write Python code in ```python blocks for analysis.

# Custom environment setup
environments:
  name: psycholinguistics_env
  imports:
    - import spacy
    - from transformers import pipeline
  setup_code: |
    # Initialize your tools
    nlp = spacy.load("en_core_web_sm")
    emotion_analyzer = pipeline("text-classification", model="j-hartmann/emotion-english-distilroberta-base")
```

### **Step 3: Use Your Extension**
```python
# Your new expert agent is now available
moderator_request = "REQUEST TO psycholinguistics_expert: Analyze emotional patterns in the text"
```

**That's it!** Your extension is automatically loaded and available system-wide.

---

## **📚 Extension Types**

### **🔧 Type 1: Add New Libraries**

**Use Case**: You want to use spaCy, transformers, or domain-specific libraries.

```yaml
name: nlp_advanced
libraries:
  - spacy
  - transformers
  - nltk.parse
  - gensim
  - scikit-learn
```

**Security**: Libraries are automatically whitelisted for secure code execution.

---

### **🤖 Type 2: Add Expert Agents**

**Use Case**: You want specialized agents for your research domain.

```yaml
name: discourse_analysis
agents:
  discourse_expert:
    description: Critical discourse analysis specialist
    prompt: |
      You are a discourse_expert specializing in critical discourse analysis (CDA).
      
      RESEARCH QUESTION: {research_question}
      SOURCE TEXTS: {source_texts}
      EXPERT REQUEST: {expert_request}
      
      Your Expertise:
      - Power relations in discourse
      - Ideological analysis of text
      - Social construction through language
      - Fairclough's three-dimensional framework
      
      Provide systematic CDA analysis addressing the moderator's request.
  
  conversation_analyst:
    description: Conversation analysis specialist
    prompt: |
      You are a conversation_analyst expert in ethnomethodological conversation analysis.
      
      Apply CA methods:
      - Turn-taking organization
      - Sequence organization  
      - Repair mechanisms
      - Preference organization
      
      Focus on micro-level interactional patterns.
```

---

### **🛠️ Type 3: Custom Environments**

**Use Case**: You need specialized initialization, configuration, or mock fallbacks.

```yaml
name: sentiment_analysis_suite
environments:
  name: sentiment_env
  description: Comprehensive sentiment analysis environment
  
  imports:
    - from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    - from textblob import TextBlob
    - import spacy
    
  setup_code: |
    # Initialize sentiment analyzers
    vader = SentimentIntensityAnalyzer()
    nlp = spacy.load("en_core_web_sm")
    
    # Custom sentiment function
    def multi_sentiment_analysis(text):
        vader_scores = vader.polarity_scores(text)
        textblob_scores = TextBlob(text).sentiment
        
        return {
            "vader": vader_scores,
            "textblob": {"polarity": textblob_scores.polarity, "subjectivity": textblob_scores.subjectivity}
        }
  
  mock_fallbacks:
    spacy: |
      class MockSpacy:
          def load(self, model):
              return self
          def __call__(self, text):
              return {"tokens": text.split()}
      spacy = MockSpacy()
```

---

## **🎯 Real-World Examples**

### **Example 1: Computational Linguistics Extension**

```yaml
name: computational_linguistics
description: Advanced NLP and linguistic analysis tools
author: Linguistics Department

libraries:
  - spacy
  - nltk.parse
  - nltk.corpus
  - stanfordcorenlp
  - allennlp

agents:
  syntax_expert:
    prompt: |
      You are a syntax_expert specializing in computational syntactic analysis.
      
      Your capabilities:
      - Dependency parsing with spaCy
      - Constituency parsing with Stanford CoreNLP  
      - Syntactic complexity metrics
      - Cross-linguistic syntactic analysis
      
      Provide rigorous syntactic analysis with computational validation.
  
  phonetics_expert:
    prompt: |
      You are a phonetics_expert specializing in computational phonetic analysis.
      
      Focus on:
      - Phonetic transcription and analysis
      - Prosodic features and stress patterns
      - Acoustic analysis where applicable
      - Cross-linguistic phonetic patterns

environments:
  name: linguistics_env
  imports:
    - import spacy
    - import nltk
    - from nltk.parse import stanford
  setup_code: |
    # Load linguistic models
    nlp_en = spacy.load("en_core_web_lg")
    nlp_es = spacy.load("es_core_news_lg")
    
    # Initialize parsers
    constituency_parser = stanford.StanfordParser(
        path_to_jar="stanford-parser.jar",
        path_to_models_jar="stanford-parser-models.jar"
    )
```

### **Example 2: Social Science Extension**

```yaml
name: social_science_toolkit
description: Social science research methods and tools

libraries:
  - pandas
  - scipy.stats
  - networkx
  - geopandas
  - socialsim

agents:
  network_analyst:
    prompt: |
      You are a network_analyst expert in social network analysis.
      
      Your capabilities:
      - Social network metrics (centrality, clustering, etc.)
      - Community detection algorithms
      - Network visualization and interpretation
      - Temporal network analysis
      
      Use NetworkX for rigorous network analysis.
  
  survey_methodologist:
    prompt: |
      You are a survey_methodologist expert in survey research and sampling.
      
      Focus on:
      - Survey design and validation
      - Sampling methodology and bias
      - Response rate analysis
      - Measurement error assessment

environments:
  name: social_science_env
  setup_code: |
    import networkx as nx
    import pandas as pd
    import scipy.stats as stats
    
    # Custom social science functions
    def calculate_network_metrics(graph):
        return {
            "density": nx.density(graph),
            "clustering": nx.average_clustering(graph),
            "centrality": nx.degree_centrality(graph)
        }
```

---

## **⚙️ Advanced Configuration**

### **Conditional Loading**
```yaml
libraries:
  - name: spacy
    required: true
    fallback: "Basic tokenization only"
  - name: transformers  
    required: false
    condition: "gpu_available"
```

### **Version Constraints**
```yaml
libraries:
  - spacy>=3.4.0
  - transformers>=4.20.0
  - torch>=1.12.0
```

### **Custom Validation**
```yaml
validation:
  check_gpu: |
    import torch
    if not torch.cuda.is_available():
        raise EnvironmentError("GPU required for transformers")
  
  check_models: |
    import spacy
    try:
        spacy.load("en_core_web_lg")
    except OSError:
        raise EnvironmentError("Please install: python -m spacy download en_core_web_lg")
```

---

## **🔒 Security & Best Practices**

### **✅ Do's**
- **Use established libraries** from PyPI
- **Provide mock fallbacks** for optional dependencies
- **Test your extensions** before sharing
- **Document your requirements** clearly
- **Follow semantic versioning**

### **❌ Don'ts**
- **Don't bypass security** (no file system access, network calls)
- **Don't hardcode paths** (use relative paths only)
- **Don't include credentials** in extension files
- **Don't override core functionality**

### **Security Notes**
- Extensions run in the **same secure sandbox** as core code
- **No network access** or file system writes allowed
- **Resource limits** still apply (memory, CPU time)
- **All code execution logged** for reproducibility

---

## **🧪 Testing Extensions**

### **Validation Tool**
```python
from discernus.core.capability_registry import CapabilityRegistry

# Validate your extension
registry = CapabilityRegistry()
issues = registry.validate_extension("extensions/your_extension.yaml")

if issues:
    print("Issues found:")
    for issue in issues:
        print(f"  - {issue}")
else:
    print("✅ Extension is valid!")
```

### **Test Your Agent**
```python
from discernus.core.llm_roles import get_expert_prompt

# Test your expert agent prompt
prompt = get_expert_prompt(
    expert_name="your_expert",
    research_question="Test question",
    source_texts="Test text",
    expert_request="Test request"
)

print(prompt)  # Verify formatting works correctly
```

---

## **📦 Sharing Extensions**

### **Package Structure**
```
my_extension/
├── extension.yaml          # Main extension file
├── README.md              # Usage instructions
├── requirements.txt       # Python dependencies
├── examples/              # Example usage
│   └── demo.py
└── tests/                 # Validation tests
    └── test_extension.py
```

### **Best Practices**
1. **Include comprehensive README** with installation instructions
2. **Provide working examples** that others can run
3. **List all dependencies** with version constraints
4. **Include test cases** to verify functionality
5. **Use semantic versioning** for updates

---

## **🚀 Migration from Fork-Based Approach**

### **Before (Fork-Required)**
```python
# Had to fork repo and modify core files
class MySpecializedAgent:
    def __init__(self):
        # Custom initialization
        pass
    
    def analyze(self, text):
        # Custom analysis logic
        pass
```

### **After (Extension-Based)**
```yaml
# Simple YAML configuration
agents:
  my_specialized_agent:
    prompt: |
      You have access to specialized analysis tools.
      Write Python code in ```python blocks to use them.
      
environments:
  setup_code: |
    # Your custom initialization here
    def specialized_analysis(text):
        # Custom analysis logic
        return results
```

**Benefits:**
- ✅ **No fork required** - easy updates
- ✅ **Automatic integration** - works immediately  
- ✅ **Secure execution** - same safety guarantees
- ✅ **Easy sharing** - simple YAML file
- ✅ **Version compatibility** - stays current with updates

---

## **🆘 Troubleshooting**

### **Common Issues**

**1. "Library not found" errors**
```bash
# Install missing dependencies
pip install your-library-name

# Or add to your extension's mock fallbacks
mock_fallbacks:
  your_library: |
    class MockLibrary:
        def analyze(self, text):
            return "Mock analysis - library not available"
    your_library = MockLibrary()
```

**2. "Extension not loading"**
- Check YAML syntax with online validator
- Ensure file is in `extensions/` directory
- Verify file extension is `.yaml` or `.yml`
- Check console for error messages

**3. "Agent not found"**
- Restart Python session to reload extensions
- Verify agent name matches exactly (case-sensitive)
- Check that extension file is valid YAML

**4. "Import errors in secure execution"**
- Add library to extension's `libraries` list
- Libraries must be installed (`pip install`)
- Some libraries may need special initialization

### **Getting Help**

1. **Validate your extension** first using the validation tool
2. **Check the examples** in this guide for reference patterns
3. **Test with simple cases** before complex setups
4. **Use mock fallbacks** for libraries that might not be available
5. **Check console logs** for detailed error messages

---

## **🔮 Future Extensibility Features**

The extension system is designed for growth:

- **Plugin marketplaces** for sharing extensions
- **Dependency resolution** for complex requirements
- **Hot reloading** for development workflows
- **Extension versioning** and compatibility checking
- **GUI extension builders** for non-programmers

---

**Happy extending! 🎉**

*With the Discernus extension system, your favorite academic tools are just a YAML file away.* 