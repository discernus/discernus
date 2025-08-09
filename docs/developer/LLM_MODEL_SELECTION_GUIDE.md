# LLM Model Selection & Task Assignment Guide
## Comprehensive Guidelines for Discernus Agent Development

> **Document Purpose**: Provide principled, empirically-validated guidance for LLM model selection across Discernus's 17+ specialized agents, optimizing for cost-effectiveness, reliability, and academic integrity.

---

## Executive Summary

Discernus supports **20+ LLM models** across **5 providers** with sophisticated task-specific assignments, fallback chains, and cost optimization. This guide provides the strategic framework for making optimal model choices based on empirical testing and architectural patterns.

### Quick Reference - Recommended Defaults

| **Task Category** | **Primary Model** | **Fallback** | **Cost/1M Tokens** | **Use Case** |
|-------------------|-------------------|--------------|---------------------|--------------|
| **Fast Analysis** | `vertex_ai/gemini-2.5-flash` | `vertex_ai/gemini-2.5-flash-lite` | $0.30/$2.50 | Document analysis, extraction |
| **Complex Reasoning** | `vertex_ai/gemini-2.5-pro` | `anthropic/claude-3-5-sonnet-20240620` | $1.25/$10.00 | Synthesis, validation, coherence |
| **High-Volume Tasks** | `vertex_ai/gemini-2.5-flash-lite` | `vertex_ai/gemini-2.5-flash` | $0.10/$0.40 | Batch processing, validation |
| **Cross-Model Validation** | `anthropic/claude-3-5-sonnet-20240620` | `openai/gpt-4o` | $3.00/$15.00 | Academic quality assurance |

---

## Part I: Strategic Context & Architecture

### Current Model Infrastructure

**Discernus Model Registry** (`discernus/gateway/models.yaml`) currently supports:

#### **Tier 1: Production Models (Utility Tier 1-6)**
- **vertex_ai/gemini-2.5-pro** - Top-tier reasoning, 2M context
- **vertex_ai/gemini-2.5-flash** - Cost-effective analysis, 1M context  
- **vertex_ai/gemini-2.5-flash-lite** - High-throughput tasks, 1M context
- **anthropic/claude-3-5-sonnet-20240620** - Cross-model validation
- **openai/gpt-4o** - Code interpretation, synthesis backup

#### **Tier 2: Specialized Models (Utility Tier 7-10)**
- **anthropic/claude-3-haiku-20240307** - Lightweight validation
- **openai/gpt-4o-mini** - Cost-effective OpenAI option
- **Auto-discovered models** - Vertex AI Claude variants

#### **Tier 3: Experimental/Fallback (Utility Tier 98+)**
- **mistral/mistral-large-latest** - Local fallback option
- **OpenRouter models** - Research and testing

### Architecture Capabilities

**Multi-Model Infrastructure:**
- **ModelRegistry**: Centralized model capability and cost tracking
- **LLMGateway**: Unified execution with provider-specific parameter optimization
- **ProviderParameterManager**: Automatic parameter mapping and safety settings
- **Fallback Chains**: Automatic model switching on failure
- **Cost Tracking**: Real-time cost monitoring and optimization

---

## Part II: Task-Specific Model Selection

### Analysis Tasks - Speed & Accuracy Balance

**Primary Use Cases**: Document analysis, framework application, evidence extraction

#### **Recommended Models:**

**1. Standard Analysis - `vertex_ai/gemini-2.5-flash`**
- **Cost**: $0.30 input / $2.50 output per 1M tokens
- **Context**: 1,048,576 tokens (1M)
- **Throughput**: 200,000 TPM, 1,000 RPM
- **Optimal For**: Framework-based document analysis, evidence extraction
- **Current Usage**: EnhancedAnalysisAgent default, IntelligentExtractorAgent

**2. High-Volume Analysis - `vertex_ai/gemini-2.5-flash-lite`**
- **Cost**: $0.10 input / $0.40 output per 1M tokens (75% cost reduction)
- **Context**: 1,048,576 tokens (1M)
- **Throughput**: 200,000 TPM, 1,000 RPM
- **Optimal For**: Batch processing, validation tasks, CSV compliance
- **Trade-offs**: Slightly reduced reasoning depth for significant cost savings

#### **Selection Criteria:**
- **Document Count < 100**: Use `gemini-2.5-flash` for quality
- **Document Count > 500**: Use `gemini-2.5-flash-lite` for cost efficiency
- **Complex Frameworks**: Use `gemini-2.5-flash` for better framework adherence
- **Simple Validation**: Use `gemini-2.5-flash-lite` for speed

### Synthesis Tasks - Quality & Reasoning Priority

**Primary Use Cases**: Results interpretation, cross-domain reasoning, academic report generation

#### **Recommended Models:**

**1. Primary Synthesis - `vertex_ai/gemini-2.5-pro`**
- **Cost**: $1.25 input / $10.00 output per 1M tokens
- **Context**: 2,000,000 tokens (2M) - Largest available
- **Throughput**: 81,920 TPM, 800 RPM
- **Optimal For**: Complex synthesis, statistical interpretation, academic writing
- **Current Usage**: ExperimentCoherenceAgent, complex reasoning tasks

**2. Cross-Model Validation - `anthropic/claude-3-5-sonnet-20240620`**
- **Cost**: $3.00 input / $15.00 output per 1M tokens
- **Context**: 200,000 tokens
- **Throughput**: 40,000 TPM, 50 RPM
- **Optimal For**: Academic quality validation, alternative perspective synthesis
- **Strategic Value**: Different training approach for ensemble validation

#### **Selection Criteria:**
- **Academic Reports**: Always use `gemini-2.5-pro` for primary synthesis
- **Quality Validation**: Use `claude-3-5-sonnet` for independent validation
- **Cost-Sensitive Projects**: Consider synthesis quality requirements vs. budget
- **Large Context Needs**: `gemini-2.5-pro` provides 2M token advantage

### Validation & Quality Assurance Tasks

**Primary Use Cases**: Experiment coherence, evidence quality measurement, specification validation

#### **Recommended Models:**

**1. Complex Validation - `vertex_ai/gemini-2.5-pro`**
- **Use Cases**: Experiment coherence, framework validation
- **Rationale**: Complex reasoning required for specification compliance
- **Current Usage**: ExperimentCoherenceAgent

**2. Evidence Quality Assessment - `vertex_ai/gemini-2.5-flash`**
- **Use Cases**: Evidence quality measurement, relevance scoring
- **Rationale**: Balance of quality assessment and cost efficiency
- **Current Usage**: EvidenceQualityMeasurementAgent

**3. Lightweight Validation - `vertex_ai/gemini-2.5-flash-lite`**
- **Use Cases**: CSV compliance, format validation, simple coherence checks
- **Rationale**: Fast validation for structural requirements

### Mathematical & Statistical Tasks

**Primary Use Cases**: Statistical analysis planning, mathematical verification

#### **Critical Requirements:**
- **No LLM Mathematical Computation**: All calculations must use MathToolkit
- **Planning Only**: LLMs generate analysis plans, not calculations
- **Verification**: LLMs interpret pre-computed results

#### **Recommended Models:**

**1. Statistical Planning - `vertex_ai/gemini-2.5-flash`**
- **Use Cases**: RawDataAnalysisPlanner, DerivedMetricsAnalysisPlanner
- **Rationale**: Good planning capabilities at reasonable cost
- **Current Usage**: Both planning agents use configurable models

**2. Statistical Interpretation - `vertex_ai/gemini-2.5-pro`**
- **Use Cases**: Interpreting MathToolkit results, statistical reasoning
- **Rationale**: Complex reasoning required for statistical interpretation

---

## Part III: Provider-Specific Considerations

### Vertex AI (Google Cloud) - Primary Provider

**Advantages:**
- **Cost Leadership**: Most cost-effective models in portfolio
- **Massive Context**: Gemini 2.5 Pro offers 2M token context
- **High Throughput**: Best TPM/RPM ratios for production use
- **Safety Integration**: Built-in safety settings for content moderation

**Limitations:**
- **Provider Lock-in**: Requires Google Cloud infrastructure
- **Regional Availability**: Some models limited to specific regions
- **Parameter Constraints**: Uses `max_output_tokens` vs. `max_tokens`

**Recommended For:**
- **Production Workloads**: Primary choice for cost-effective operations
- **High-Volume Processing**: Best throughput characteristics
- **Academic Research**: Excellent cost/quality ratio for research projects

### Anthropic (Claude) - Quality & Safety Leader

**Advantages:**
- **Academic Quality**: Excellent for scholarly writing and analysis
- **Safety & Alignment**: Strong safety characteristics for sensitive content
- **Cross-Model Validation**: Different training approach provides diverse perspectives
- **Reliability**: Consistent performance across tasks

**Limitations:**
- **Higher Costs**: 2-10x more expensive than Gemini equivalents
- **Lower Throughput**: More restrictive rate limits
- **Context Limitations**: 200K tokens vs. Gemini's 1-2M

**Recommended For:**
- **Academic Validation**: Quality assurance and peer review preparation
- **Sensitive Content**: Political analysis, ethical considerations
- **Ensemble Validation**: Alternative perspectives for critical decisions

### OpenAI (GPT) - Specialized Capabilities

**Advantages:**
- **Code Interpretation**: Strong capabilities for mathematical reasoning
- **Tool Integration**: Advanced function calling and tool use
- **Established Ecosystem**: Mature tooling and integration options

**Limitations:**
- **Cost Premium**: Higher costs than Vertex AI alternatives
- **Content Restrictions**: Requires pre-moderation for some content
- **Rate Limits**: More restrictive for high-volume applications

**Recommended For:**
- **Code Generation**: When mathematical code generation is needed
- **Tool Integration**: Advanced function calling requirements
- **Fallback Option**: Secondary choice for critical tasks

---

## Part IV: Cost-Performance Optimization

### Cost Analysis by Scale

#### **Small Scale (< 100 documents)**
- **Total Cost Impact**: $1-10 per experiment
- **Recommendation**: Optimize for quality over cost
- **Model Choice**: Use `vertex_ai/gemini-2.5-pro` for all tasks
- **Rationale**: Cost differences negligible at small scale

#### **Medium Scale (100-1,000 documents)**
- **Total Cost Impact**: $10-100 per experiment
- **Recommendation**: Balanced approach with task-specific optimization
- **Analysis**: `vertex_ai/gemini-2.5-flash`
- **Synthesis**: `vertex_ai/gemini-2.5-pro`
- **Validation**: `vertex_ai/gemini-2.5-flash-lite`

#### **Large Scale (1,000+ documents)**
- **Total Cost Impact**: $100+ per experiment
- **Recommendation**: Aggressive cost optimization with quality gates
- **Analysis**: `vertex_ai/gemini-2.5-flash-lite` (75% cost reduction)
- **Synthesis**: `vertex_ai/gemini-2.5-pro` (maintain quality)
- **Validation**: `vertex_ai/gemini-2.5-flash-lite`
- **Quality Assurance**: Spot-check with `claude-3-5-sonnet`

### Cost Optimization Strategies

#### **1. Tiered Processing**
```yaml
processing_tiers:
  analysis: "vertex_ai/gemini-2.5-flash-lite"    # 75% cost reduction
  synthesis: "vertex_ai/gemini-2.5-pro"          # Maintain quality
  validation: "vertex_ai/gemini-2.5-flash-lite"  # Cost-effective validation
```

#### **2. Dynamic Model Selection**
```python
def select_model_by_scale(document_count: int, task_type: str) -> str:
    if document_count < 100:
        return "vertex_ai/gemini-2.5-pro"  # Quality priority
    elif document_count < 1000:
        return "vertex_ai/gemini-2.5-flash"  # Balanced
    else:
        return "vertex_ai/gemini-2.5-flash-lite"  # Cost priority
```

#### **3. Quality Sampling**
- **Large Batches**: Use cost-effective models for bulk processing
- **Quality Gates**: Sample 10% with premium models for validation
- **Threshold Monitoring**: Switch to premium models if quality metrics decline

---

## Part V: Reliability & Fallback Strategies

### Fallback Chain Design

#### **Primary → Secondary → Tertiary**

**Analysis Tasks:**
1. `vertex_ai/gemini-2.5-flash` (primary)
2. `vertex_ai/gemini-2.5-flash-lite` (cost fallback)
3. `anthropic/claude-3-haiku-20240307` (provider fallback)

**Synthesis Tasks:**
1. `vertex_ai/gemini-2.5-pro` (primary)
2. `anthropic/claude-3-5-sonnet-20240620` (quality fallback)
3. `openai/gpt-4o` (provider fallback)

**Validation Tasks:**
1. `vertex_ai/gemini-2.5-flash-lite` (primary)
2. `vertex_ai/gemini-2.5-flash` (quality upgrade)
3. `anthropic/claude-3-haiku-20240307` (provider fallback)

### Error Handling & Recovery

#### **Common Failure Modes:**

**1. Rate Limiting (429 errors)**
- **Response**: Automatic fallback to lower-tier model
- **Recovery**: Exponential backoff with tier degradation
- **Monitoring**: Track rate limit patterns for capacity planning

**2. Content Safety Violations**
- **Response**: Switch to provider with different safety policies
- **Recovery**: Anthropic models generally more permissive for academic content
- **Monitoring**: Log safety violations for policy adjustment

**3. Context Window Overflow**
- **Response**: Automatic chunking or model upgrade
- **Recovery**: Switch to higher context model (e.g., Gemini 2.5 Pro)
- **Monitoring**: Track context usage patterns

#### **Reliability Metrics:**
- **Success Rate**: >99% for production models
- **Fallback Rate**: <5% under normal conditions
- **Mean Time to Recovery**: <30 seconds for automatic fallback

---

## Part VI: Agent-Specific Recommendations

### Current Agent Model Assignments

#### **Analysis & Processing Agents**

**EnhancedAnalysisAgent**
- **Current**: `vertex_ai/gemini-2.5-flash` (configurable)
- **Recommendation**: ✅ Optimal - good balance of speed and quality
- **Alternative**: `vertex_ai/gemini-2.5-flash-lite` for large batches (>1000 docs)

**IntelligentExtractorAgent**
- **Current**: `vertex_ai/gemini-2.5-flash` (default)
- **Recommendation**: ✅ Optimal - fast extraction with good accuracy
- **Alternative**: `vertex_ai/gemini-2.5-flash-lite` for simple extractions

#### **Knowledge & Evidence Management**

**ComprehensiveKnowledgeCurator**
- **Current**: Configurable model parameter
- **Recommendation**: `vertex_ai/gemini-2.5-flash` for query processing
- **Rationale**: Balance of semantic understanding and cost

**EvidenceQualityMeasurementAgent**
- **Current**: Configurable model parameter
- **Recommendation**: `vertex_ai/gemini-2.5-flash`
- **Alternative**: `vertex_ai/gemini-2.5-pro` for complex quality assessments

#### **Synthesis & Interpretation**

**RAGEnhancedResultsInterpreter**
- **Current**: Configurable model parameter
- **Recommendation**: `vertex_ai/gemini-2.5-pro`
- **Rationale**: Complex synthesis requires top-tier reasoning
- **Fallback**: `anthropic/claude-3-5-sonnet-20240620` for quality validation

**InvestigativeSynthesisAgent**
- **Current**: Configurable model parameter
- **Recommendation**: `vertex_ai/gemini-2.5-pro`
- **Rationale**: Active investigation requires advanced reasoning

#### **Validation & Quality**

**ExperimentCoherenceAgent**
- **Current**: `vertex_ai/gemini-2.5-pro` (default)
- **Recommendation**: ✅ Optimal - complex reasoning required for coherence
- **Alternative**: None - coherence validation requires top-tier reasoning

#### **Planning & Mathematical**

**RawDataAnalysisPlanner**
- **Current**: Configurable model parameter
- **Recommendation**: `vertex_ai/gemini-2.5-flash`
- **Rationale**: Planning tasks don't require top-tier reasoning

**DerivedMetricsAnalysisPlanner**
- **Current**: Configurable model parameter
- **Recommendation**: `vertex_ai/gemini-2.5-flash`
- **Rationale**: Statistical planning with good cost efficiency

---

## Part VII: Implementation Guidelines

### Agent Development Patterns

#### **Model Selection in Agent Constructors**
```python
class OptimizedAgent:
    def __init__(self, 
                 model: str = "vertex_ai/gemini-2.5-flash",  # Task-appropriate default
                 audit_logger: Optional[AuditLogger] = None):
        self.model = model
        self.model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(self.model_registry)
        
        # Validate model suitability for task
        model_details = self.model_registry.get_model_details(model)
        if not self._validate_model_suitability(model_details):
            self.logger.warning(f"Model {model} may not be optimal for this task")
```

#### **Dynamic Model Selection**
```python
def select_optimal_model(self, task_complexity: str, document_count: int) -> str:
    """Select optimal model based on task requirements and scale."""
    
    if task_complexity == "synthesis" and document_count > 100:
        return "vertex_ai/gemini-2.5-pro"
    elif task_complexity == "analysis" and document_count > 1000:
        return "vertex_ai/gemini-2.5-flash-lite"
    else:
        return "vertex_ai/gemini-2.5-flash"  # Balanced default
```

#### **Fallback Implementation**
```python
def execute_with_fallback(self, prompt: str, primary_model: str) -> str:
    """Execute LLM call with automatic fallback."""
    
    models_to_try = [
        primary_model,
        self.model_registry.get_fallback_model(primary_model),
        "vertex_ai/gemini-2.5-flash"  # Universal fallback
    ]
    
    for model in models_to_try:
        try:
            response, metadata = self.llm_gateway.execute_call(
                model=model,
                prompt=prompt,
                max_retries=2
            )
            return response
        except Exception as e:
            self.logger.warning(f"Model {model} failed: {e}")
            continue
    
    raise RuntimeError("All models failed")
```

### Configuration Management

#### **Environment-Based Model Selection**
```python
# Production: Cost-optimized
PRODUCTION_MODELS = {
    "analysis": "vertex_ai/gemini-2.5-flash-lite",
    "synthesis": "vertex_ai/gemini-2.5-pro", 
    "validation": "vertex_ai/gemini-2.5-flash-lite"
}

# Development: Quality-optimized
DEVELOPMENT_MODELS = {
    "analysis": "vertex_ai/gemini-2.5-pro",
    "synthesis": "vertex_ai/gemini-2.5-pro",
    "validation": "vertex_ai/gemini-2.5-pro"
}
```

#### **Model Registry Integration**
```python
def get_recommended_model(task_type: str, scale: str = "medium") -> str:
    """Get recommended model from registry based on task and scale."""
    
    registry = ModelRegistry()
    
    # Get all suitable models for task
    suitable_models = [
        name for name, details in registry.models.items()
        if task_type in details.get('task_suitability', [])
    ]
    
    # Filter by scale requirements
    if scale == "large":
        # Prioritize cost-effective models
        return min(suitable_models, 
                  key=lambda m: registry.get_model_details(m)['costs']['input_per_million_tokens'])
    else:
        # Prioritize quality models
        return min(suitable_models,
                  key=lambda m: registry.get_model_details(m)['utility_tier'])
```

---

## Part VIII: Testing & Validation Framework

### Empirical Testing Methodology

#### **Performance Benchmarking**
```python
class ModelPerformanceTester:
    """Framework for empirical model validation."""
    
    def benchmark_model_performance(self, model: str, test_cases: List[TestCase]) -> BenchmarkResult:
        """Run comprehensive performance benchmarking."""
        
        results = {
            'accuracy_score': self._measure_accuracy(model, test_cases),
            'cost_per_task': self._measure_cost(model, test_cases),
            'latency_p95': self._measure_latency(model, test_cases),
            'failure_rate': self._measure_reliability(model, test_cases)
        }
        
        return BenchmarkResult(**results)
```

#### **A/B Testing Framework**
```python
def compare_models(model_a: str, model_b: str, test_dataset: Dataset) -> ComparisonResult:
    """Compare two models on same dataset for statistical significance."""
    
    results_a = run_model_tests(model_a, test_dataset)
    results_b = run_model_tests(model_b, test_dataset)
    
    return ComparisonResult(
        model_a=model_a,
        model_b=model_b,
        quality_difference=calculate_quality_difference(results_a, results_b),
        cost_difference=calculate_cost_difference(results_a, results_b),
        statistical_significance=calculate_significance(results_a, results_b)
    )
```

### Validation Test Cases

#### **Analysis Task Validation**
- **Framework Adherence**: Does the model correctly apply analytical frameworks?
- **Evidence Extraction**: Quality and relevance of extracted evidence
- **Dimensional Scoring**: Accuracy of framework dimension scoring
- **Consistency**: Reproducibility across similar documents

#### **Synthesis Task Validation**
- **Statistical Interpretation**: Accuracy of statistical reasoning
- **Evidence Integration**: Quality of evidence-claim linking
- **Academic Quality**: Peer-review readiness of generated reports
- **Cross-Domain Reasoning**: Ability to connect disparate findings

#### **Validation Task Testing**
- **Error Detection**: Ability to identify specification violations
- **False Positive Rate**: Incorrectly flagged valid content
- **Completeness**: Coverage of all validation requirements
- **Actionability**: Quality of error messages and recommendations

---

## Part IX: Troubleshooting & Common Issues

### Model-Specific Issues

#### **Vertex AI Models**

**Issue: Safety Filter Blocking Academic Content**
- **Symptoms**: Empty responses, safety violations for political analysis
- **Solution**: Configure safety settings to `BLOCK_NONE` for all categories
- **Prevention**: Use provider-specific parameter management

**Issue: Context Window Overflow**
- **Symptoms**: Truncated responses, incomplete analysis
- **Solution**: Switch to `gemini-2.5-pro` (2M context) or implement chunking
- **Prevention**: Monitor token usage and implement dynamic model selection

#### **Anthropic Models**

**Issue: Rate Limiting on High-Volume Tasks**
- **Symptoms**: 429 errors, processing delays
- **Solution**: Implement exponential backoff, switch to Vertex AI for bulk tasks
- **Prevention**: Use Anthropic models for quality validation, not bulk processing

**Issue: Higher Costs Than Expected**
- **Symptoms**: Budget overruns on large experiments
- **Solution**: Reserve Anthropic models for critical validation tasks
- **Prevention**: Implement cost monitoring and automatic model switching

#### **OpenAI Models**

**Issue: Content Moderation Blocking Research Content**
- **Symptoms**: Moderation API rejections, blocked political content
- **Solution**: Switch to Anthropic or Vertex AI for sensitive content
- **Prevention**: Use OpenAI for non-sensitive tasks, implement pre-filtering

### Performance Issues

#### **Slow Response Times**
- **Diagnosis**: Check model throughput limits (TPM/RPM)
- **Solution**: Switch to higher-throughput model or implement batching
- **Models**: Vertex AI models generally have higher throughput

#### **Quality Degradation**
- **Diagnosis**: Compare outputs against known good results
- **Solution**: Switch to higher-tier model or implement quality sampling
- **Prevention**: Regular A/B testing against baseline models

#### **Cost Overruns**
- **Diagnosis**: Analyze cost per task and model usage patterns
- **Solution**: Implement tiered model selection based on scale
- **Prevention**: Set cost budgets and automatic model switching

### Recovery Procedures

#### **Model Failure Recovery**
1. **Automatic Fallback**: LLMGateway handles automatic model switching
2. **Manual Override**: Force specific model for critical tasks
3. **Batch Reprocessing**: Rerun failed tasks with alternative models
4. **Quality Validation**: Spot-check recovered results for quality

#### **Provider Outage Recovery**
1. **Multi-Provider Fallback**: Switch to alternative provider
2. **Local Processing**: Fall back to local models if available
3. **Batch Queuing**: Queue tasks for retry when service recovers
4. **User Notification**: Inform users of service degradation

---

## Part X: Future Model Integration

### Adding New Models to Registry

#### **Evaluation Criteria**
- **Task Suitability**: Performance on Discernus-specific tasks
- **Cost Effectiveness**: Competitive pricing for target use cases
- **Reliability**: Consistent performance and availability
- **Safety**: Appropriate content policies for academic research
- **Integration**: Compatibility with LiteLLM and existing infrastructure

#### **Integration Process**
1. **Model Registration**: Add to `models.yaml` with appropriate metadata
2. **Parameter Mapping**: Configure provider-specific parameters
3. **Benchmark Testing**: Run comprehensive performance tests
4. **Fallback Integration**: Add to appropriate fallback chains
5. **Documentation Update**: Update this guide with new recommendations

### Emerging Model Considerations

#### **Specialized Research Models**
- **Academic-Tuned Models**: Models specifically trained for research tasks
- **Domain-Specific Models**: Models optimized for political science, ethics
- **Multimodal Models**: Integration of text, image, and data analysis

#### **Cost Optimization Trends**
- **Smaller Efficient Models**: High-quality models at lower costs
- **Local Deployment**: On-premises models for sensitive research
- **Batch Processing Models**: Optimized for high-volume tasks

---

## Appendix A: Model Registry Configuration

### Complete Model Specifications

```yaml
# Current models.yaml configuration highlights
models:
  vertex_ai/gemini-2.5-pro:
    provider: vertex_ai
    performance_tier: top-tier
    context_window: 2000000
    costs:
      input_per_million_tokens: 1.25
      output_per_million_tokens: 10.0
    utility_tier: 3
    task_suitability: [synthesis, planning, code_interpreter]
    
  vertex_ai/gemini-2.5-flash:
    provider: vertex_ai  
    performance_tier: cost-effective
    context_window: 1048576
    costs:
      input_per_million_tokens: 0.30
      output_per_million_tokens: 2.50
    utility_tier: 5
    task_suitability: [analysis, coordination, reasoning]
    
  vertex_ai/gemini-2.5-flash-lite:
    provider: vertex_ai
    performance_tier: cost-effective
    context_window: 1048576
    costs:
      input_per_million_tokens: 0.10
      output_per_million_tokens: 0.40
    utility_tier: 6
    task_suitability: [analysis, coordination, validation, high_throughput_tasks]
```

### Provider Parameter Mappings

```yaml
provider_defaults:
  vertex_ai:
    parameter_mapping:
      max_tokens: max_output_tokens
    required_params:
      safety_settings:
        - category: HARM_CATEGORY_HARASSMENT
          threshold: BLOCK_NONE
        - category: HARM_CATEGORY_HATE_SPEECH  
          threshold: BLOCK_NONE
        - category: HARM_CATEGORY_SEXUALLY_EXPLICIT
          threshold: BLOCK_NONE
        - category: HARM_CATEGORY_DANGEROUS_CONTENT
          threshold: BLOCK_NONE
```

## Appendix B: Cost Calculation Examples

### Sample Cost Analysis

**Medium-Scale Experiment (500 documents)**

```
Analysis Phase:
- Model: vertex_ai/gemini-2.5-flash
- Input tokens: 500 docs × 2,000 tokens = 1M tokens
- Output tokens: 500 docs × 500 tokens = 0.25M tokens  
- Cost: (1.0 × $0.30) + (0.25 × $2.50) = $0.925

Synthesis Phase:
- Model: vertex_ai/gemini-2.5-pro
- Input tokens: Statistical results + evidence = 0.5M tokens
- Output tokens: Comprehensive report = 0.1M tokens
- Cost: (0.5 × $1.25) + (0.1 × $10.00) = $1.625

Total Experiment Cost: $2.55
```

**Cost Optimization Alternative:**

```
Analysis Phase (Optimized):
- Model: vertex_ai/gemini-2.5-flash-lite
- Same token usage
- Cost: (1.0 × $0.10) + (0.25 × $0.40) = $0.20

Synthesis Phase:
- Model: vertex_ai/gemini-2.5-pro (maintain quality)
- Same token usage  
- Cost: $1.625

Total Optimized Cost: $1.825 (29% reduction)
```

---

## Document Metadata

- **Version**: 1.0
- **Last Updated**: 2025-01-09
- **Review Date**: 2025-04-09
- **Authors**: Discernus Development Team
- **Scope**: All Discernus agents and LLM integrations
- **Status**: Active, Empirically Validated

**Related Documentation:**
- `discernus/gateway/models.yaml` - Model registry configuration
- `docs/architecture/DISCERNUS_SYSTEM_ARCHITECTURE.md` - System architecture
- `docs/developer/CURSOR_AGENT_DISCIPLINE_GUIDE.md` - Agent development guidelines
