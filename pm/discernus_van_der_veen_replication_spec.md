# Discernus van der Veen Replication Specification: LLM-Based Populist Classification System
## Technical Specification & Implementation Plan

### Executive Summary

This document outlines the specification for a Discernus-based system that replicated the van der Veen 2024 paper to validate the "Thick LLM + Thin Software" paradigm for academic research through populist discourse classification. The MVP will directly replicate and extend the van der Veen et al. (2024) study using LLM ensembles instead of fine-tuned BERT, testing six core hypotheses about LLM-based research approaches.

**Core Innovation**: LLM disagreement detection and adversarial review instead of traditional ensemble averaging, providing unprecedented transparency and uncertainty quantification for academic research.

---

## 1. Technical Architecture

### 1.1 Core Design Philosophy
- **Thick LLM**: Complex reasoning handled by language models
- **Thin Software**: Minimal orchestration layer focused on data flow and persistence
- **Disagreement as Signal**: Surface model disagreement rather than suppress it
- **Academic-First**: Optimize for research workflows and transparency

### 1.2 Technology Stack
```yaml
Core Framework:
  - Language: Python 3.9+
  - LLM Interface: TinyLLM (unified API across providers)
  - Data Processing: pandas, numpy
  - Export Formats: CSV, JSON (R/Stata compatible)

LLM Providers:
  - Primary: OpenAI GPT-4
  - Secondary: Anthropic Claude-3-Sonnet
  - Tertiary: Google Gemini-Pro

Dependencies:
  - tinyllm: Multi-provider LLM interface
  - pandas: Data manipulation and export
  - jupyter: Interactive development environment
  - python-dotenv: Environment variable management
```

### 1.3 System Architecture
```python
# Single-file MVP architecture
class DiscernusMVP:
    def __init__(self):
        self.llm = TinyLLM()
        self.models = ['gpt-4', 'claude-3-sonnet', 'gemini-pro']
        self.disagreement_cases = []
        self.audit_trail = []
    
    # Core methods:
    # - classify_sentence() -> multi-model classification
    # - detect_disagreement() -> identify contested cases
    # - adversarial_review() -> LLM-based adjudication
    # - export_results() -> academic-friendly outputs
```

---

## 2. Implementation Plan

### 2.1 Two-Week Development Timeline

**Week 1: Core Infrastructure**
- Days 1-2: TinyLLM integration, prompt engineering, basic ensemble logic
- Days 3-4: Disagreement detection, adversarial review implementation
- Day 5: CSV export, audit trail, basic cost tracking

**Week 2: Validation & Testing**
- Days 6-7: Load van der Veen dataset, run validation comparisons
- Days 8-9: Refine prompts based on accuracy results, optimize performance
- Day 10: Final testing, documentation, demo preparation

### 2.2 Core Components

#### 2.2.1 Ensemble Classification Pipeline
```python
def classify_sentence(self, sentence: str) -> dict:
    """
    Send sentence to all three LLMs using standardized prompt
    Returns structured results with confidence scores
    """
    classifications = {}
    for model in self.models:
        response = self.llm.complete(
            model=model,
            prompt=self.build_populist_prompt(sentence),
            temperature=0.1,
            max_tokens=200
        )
        classifications[model] = self.parse_json_response(response)
    
    return self.analyze_consensus(sentence, classifications)
```

#### 2.2.2 Disagreement Detection Logic
```python
def detect_disagreement(self, classifications: dict) -> dict:
    """
    Three-tier disagreement classification:
    - CONSENSUS: All models agree
    - MAJORITY: 2-1 split with minority report
    - CONTESTED: Complete disagreement requiring review
    """
    classes = [c['classification'] for c in classifications.values()]
    
    if len(set(classes)) == 1:
        return {'status': 'CONSENSUS', 'requires_review': False}
    elif len(set(classes)) == 2:
        return {'status': 'MAJORITY', 'requires_review': True}
    else:
        return {'status': 'CONTESTED', 'requires_review': True}
```

#### 2.2.3 Adversarial Review System
```python
def adversarial_review(self, sentence: str, disagreement_data: dict) -> dict:
    """
    Specialized LLM analyzes why models disagree
    Provides meta-analysis of classification difficulty
    """
    adversarial_prompt = f"""
    Analyze disagreement between populist classifiers:
    
    SENTENCE: "{sentence}"
    DISAGREEMENT: {format_disagreement(disagreement_data)}
    
    Determine:
    1. Why models disagree
    2. Most compelling classification
    3. Whether case is genuinely ambiguous
    
    Return JSON with analysis and recommendation.
    """
    
    return self.llm.complete(model='gpt-4', prompt=adversarial_prompt)
```

### 2.3 Data Processing Pipeline

#### 2.3.1 Input Data (van der Veen et al. 2024)
- **Governor speeches**: 288 speeches from 73 terms (2012-2020)
- **Presidential speeches**: 45 speeches from 2016 campaign
- **Validation data**: 26 speeches from recent governors (2018-2022)
- **Human coding**: Sentence-level populist/pluralist/neutral classifications

#### 2.3.2 Processing Workflow
```python
def process_speech(self, speech_text: str) -> pd.DataFrame:
    """
    1. Split speech into sentences
    2. Classify each sentence with ensemble
    3. Detect disagreement and apply adversarial review
    4. Generate audit trail with full provenance
    5. Export results in academic formats
    """
    sentences = self.split_sentences(speech_text)
    results = []
    
    for sentence in sentences:
        result = self.classify_sentence(sentence)
        if result['disagreement_flag']:
            result['adversarial_review'] = self.adversarial_review(sentence, result)
        results.append(result)
    
    return pd.DataFrame(results)
```

---

## 3. Testable Hypotheses

### 3.1 Core Hypotheses with Success Criteria

#### H1: Performance Parity
**Claim**: LLM ensembles match fine-tuned BERT performance
**Success Criteria**: 
- Governors: ≥84% accuracy vs. human coding
- Presidential: ≥89% accuracy vs. human coding
**Falsification**: <75% accuracy on either dataset

#### H2: Disagreement Value
**Claim**: LLM disagreement correlates with genuine ambiguity
**Success Criteria**: 
- Disagreement cases show >0.3 correlation with human uncertainty
- Disagreement rate 10-20% (meaningful but not excessive)
**Falsification**: Random disagreement with no correlation to human uncertainty

#### H3: Transparency Advantage
**Claim**: LLM reasoning superior to black-box ML
**Success Criteria**: 
- 100% decision traceability
- >70% explanation consistency
- >80% researcher comprehension
**Falsification**: Inconsistent or uninformative explanations

#### H4: Speed Advantage
**Claim**: 10x faster than traditional approaches
**Success Criteria**: 
- Complete analysis in <1 day vs. weeks for traditional ML
- >10x speedup factor
**Falsification**: <3x speedup over traditional approaches

#### H5: Cost Effectiveness
**Claim**: Academic budgets can sustain LLM research
**Success Criteria**: 
- <$5 per speech analysis
- <$500 total for full corpus
**Falsification**: >$1,000 for typical academic corpus

#### H6: Adversarial Review Effectiveness
**Claim**: LLM-based review improves ensemble accuracy
**Success Criteria**: 
- >5% accuracy improvement on contested cases
- Consistent adversarial review quality
**Falsification**: No improvement or degraded accuracy

### 3.2 Meta-Hypothesis: Paradigm Validation
**Claim**: "Thick LLM + Thin Software" superior for academic research
**Success Criteria**: ≥3 of 4 core hypotheses validated + researcher adoption intent
**Falsification**: Traditional ML approaches remain superior

---

## 4. Implementation Details

### 4.1 Prompt Engineering
```python
POPULIST_CLASSIFICATION_PROMPT = """
Classify this sentence as POPULIST, PLURALIST, or NEUTRAL.

POPULIST: Politics as moral struggle between virtuous "people" and corrupt "elite"
- Example: "The corrupt establishment has betrayed hardworking Americans"

PLURALIST: Democratic cooperation, checks and balances, inclusion
- Example: "We must work together across party lines to find solutions"

NEUTRAL: Neither populist nor pluralist framing
- Example: "The budget allocates $50 million for infrastructure"

Sentence: "{sentence}"

Respond with JSON:
{{"classification": "POPULIST|PLURALIST|NEUTRAL", "confidence": 0.0-1.0, "reasoning": "brief explanation"}}
"""
```

### 4.2 Output Formats

#### 4.2.1 Main Results CSV
```csv
sentence_id,sentence,final_classification,consensus_level,disagreement_flag,confidence_avg,adjudication_method,minority_report
1,"The elites have betrayed us",POPULIST,unanimous,False,0.89,consensus,
2,"We must work together",PLURALIST,majority,True,0.72,majority_rule,"Gemini classified as NEUTRAL"
```

#### 4.2.2 Disagreement Analysis CSV
```csv
sentence_id,sentence,gpt4_class,claude_class,gemini_class,disagreement_type,adversarial_recommendation,resolution_method
2,"We must work together",PLURALIST,PLURALIST,NEUTRAL,majority_split,PLURALIST,adversarial_review
```

#### 4.2.3 Audit Trail JSON
```json
{
  "sentence_id": 1,
  "timestamp": "2024-01-15T10:30:00Z",
  "model_responses": {
    "gpt-4": {"classification": "POPULIST", "confidence": 0.9},
    "claude-3": {"classification": "POPULIST", "confidence": 0.85}
  },
  "cost_breakdown": {"total": 0.003, "per_model": 0.001},
  "processing_time_ms": 1250
}
```

---

## 5. Validation Strategy

### 5.1 Direct Replication
- Use exact same speeches from van der Veen et al. (2024)
- Compare LLM ensemble results to paper's BERT performance
- Validate against human-coded sentence classifications

### 5.2 Error Analysis
- Identify systematic patterns in LLM failures
- Analyze disagreement cases for theoretical insights
- Compare error types between LLM and traditional approaches

### 5.3 Academic Workflow Integration
- Export formats compatible with R, Stata, Python
- Documentation suitable for academic peer review
- Reproducibility package with complete code and data

---

## 6. Risk Mitigation

### 6.1 Technical Risks
- **API failures**: TinyLLM provides built-in retry logic
- **Cost overruns**: Real-time cost tracking with budget alerts
- **Rate limiting**: Automatic throttling across providers
- **Quality degradation**: Adversarial review and human oversight

### 6.2 Academic Risks
- **Reproducibility**: Complete audit trail and version control
- **Validity**: Direct comparison with established benchmarks
- **Bias**: Multi-provider ensemble reduces single-model bias
- **Transparency**: Full explanation and reasoning capture

---

## 7. Success Metrics

### 7.1 Quantitative Metrics
- **Accuracy**: ≥84% on governor speeches, ≥89% on presidential
- **Speed**: <1 day for full corpus analysis
- **Cost**: <$500 for complete van der Veen dataset
- **Disagreement**: 10-20% meaningful disagreement rate

### 7.2 Qualitative Metrics
- **Researcher comprehension**: >80% find explanations clear
- **Adoption intent**: >70% would use for future research
- **Transparency**: 100% traceable decision paths
- **Academic acceptance**: Suitable for peer review publication

---

## 8. Next Steps

### 8.1 Immediate Actions (Week 1)
1. Set up development environment with TinyLLM
2. Implement basic ensemble classification
3. Load and preprocess van der Veen dataset
4. Develop disagreement detection logic

### 8.2 Validation Phase (Week 2)
1. Run full corpus through LLM ensemble
2. Compare results to paper's benchmarks
3. Analyze disagreement patterns and adversarial review effectiveness
4. Generate academic-ready output formats

### 8.3 Documentation and Dissemination
1. Create comprehensive documentation
2. Prepare reproducibility package
3. Draft academic paper describing methodology
4. Present results to research community

---

## 9. Conclusion

This MVP represents a crucial test of the "Thick LLM + Thin Software" paradigm for academic research. By directly replicating and extending established computational social science research, we can definitively validate or falsify claims about LLM-based research approaches.

The system's emphasis on disagreement detection and adversarial review offers a fundamentally different approach to ensemble methods—one that surfaces uncertainty rather than suppressing it. This transparency could prove revolutionary for academic research, where understanding the boundaries of classificatory certainty is as important as the classifications themselves.

**If validated, this approach could democratize sophisticated computational analysis for researchers without deep technical backgrounds. If falsified, it provides crucial negative results about the current limitations of LLM-based academic research.**

The MVP's two-week timeline and direct comparison to published benchmarks make it an efficient, low-risk way to test these fundamental questions about the future of computational social science.

---

## Appendices

### Appendix A: Technical Dependencies
```python
# requirements.txt
tinyllm>=0.1.0
pandas>=2.0.0
numpy>=1.24.0
jupyter>=1.0.0
python-dotenv>=1.0.0
```

### Appendix B: Sample Code Structure
```
discernus_mvp/
├── discernus_mvp.py          # Main implementation
├── config.py                 # Configuration settings
├── prompts.py                # Prompt templates
├── data/                     # Input datasets
├── results/                  # Output files
└── notebooks/                # Analysis notebooks
```

### Appendix C: Budget Estimate
- **Development time**: 80 hours @ $100/hour = $8,000
- **API costs**: ~$200 for full dataset analysis
- **Total MVP cost**: ~$8,200
- **Cost per hypothesis tested**: ~$1,400
- **Potential impact**: Validation of new research paradigm