# THIN Architecture Reference
*LLM Intelligence + Minimal Software*

## Core Philosophy

**"Thick LLM + Thin Software = Epistemic Trust"**

THIN architecture maximizes LLM intelligence while minimizing software parsing and logic. This creates transparent, auditable systems where humans can understand and trust the analytical process.

## THIN Patterns (DO THIS)

### 1. Natural Language Flow Between Components

**Principle**: LLMs communicate through natural language, not complex data structures.

**✅ THIN Implementation**:
```python
# discernus/core/agent_roles.py
EXPERT_AGENT_PROMPTS = {
    'corpus_detective_agent': """You are a corpus_detective_agent, specializing in systematic analysis of user-provided text corpora.

RESEARCH QUESTION: {research_question}

SOURCE TEXTS:
{source_texts}

The moderator_llm has requested your corpus analysis expertise:

MODERATOR REQUEST: {expert_request}

Your Task:
Analyze the provided corpus systematically and help the user understand what they have...
"""
}

def get_expert_prompt(expert_type: str, **kwargs) -> str:
    """Get expert prompt with dynamic parameter substitution"""
    template = EXPERT_AGENT_PROMPTS.get(expert_type, EXPERT_AGENT_PROMPTS['generic_expert'])
    return template.format(**kwargs)
```

**Why This Works**:
- LLMs receive clear, natural language instructions
- No complex JSON parsing required
- Human-readable prompt templates
- Easy to modify and extend

### 2. Secure Code Execution for Mathematical Operations

**Principle**: LLMs design calculations, secure code executes them, LLMs interpret results.

**✅ THIN Implementation**:
```python
# discernus/core/secure_code_executor.py
def process_llm_code_request(conversation_id: str, speaker: str, response: str) -> str:
    """Enhanced code execution with complete transparency"""
    
    # Extract code blocks from natural language response
    code_blocks = re.findall(r'```python\n(.*?)\n```', response, re.DOTALL)
    if not code_blocks:
        return response  # No code to execute
    
    executor = SecureCodeExecutor(enable_data_science=True)
    enhanced_response = response
    
    for i, code in enumerate(code_blocks):
        # LLM designed the calculation, now execute it securely
        result = executor.execute_code(code)
        
        # Add transparent results back to natural language response
        enhanced_response += f"\n\n**🔐 Secure Code Execution Result:**\n```\n{result['output']}\n```"
        enhanced_response += f"\n*Execution time: {result['execution_time']:.3f}s*"
    
    return enhanced_response
```

**Mathematical Reliability Pattern**:
1. **LLM Design Phase**: LLM writes calculation logic in natural language with code
2. **Secure Execution Phase**: Infrastructure executes code with security and resource limits
3. **LLM Interpretation Phase**: LLM receives results and interprets them in natural language

### 3. Centralized Intelligence in Dedicated Files

**Principle**: All LLM prompts and intelligence centralized, not scattered in orchestrator code.

**✅ THIN Implementation**:
```python
# discernus/core/agent_roles.py - Centralized prompt management
EXPERT_AGENT_PROMPTS = {
    'knowledgenaut_agent': """You are a knowledgenaut_agent, a specialized research agent with expertise in academic literature discovery and framework interrogation.

RESEARCH QUESTION: {research_question}

The research infrastructure will automatically:
- Execute literature searches based on your research question
- Validate paper quality and detect systematic biases
- Synthesize findings with confidence levels
- Provide adversarial critique for quality control
- Generate comprehensive research reports
""",
    
    'data_science_expert': """You are a data_science_expert, specializing in:
- Statistical analysis and hypothesis testing
- Machine learning and computational methods
- Data visualization and pattern recognition
- Quantitative research methodology

Write Python code in ```python blocks for analysis. Be rigorous about statistical significance and methodology.
"""
}
```

**Why This Works**:
- All prompts in one place for easy modification
- Orchestrator code stays minimal
- New experts can be added without code changes
- Version control tracks prompt evolution

### 4. Configuration-Driven Extension System

**Principle**: New capabilities added through configuration, not code modification.

**✅ THIN Implementation**:
```yaml
# discernus/core/agent_registry.yaml
agents:
  - name: StatisticalAnalysisAgent
    archetype: Tool-Using
    module: "discernus.agents.statistical_analysis_agent"
    class: "StatisticalAnalysisAgent"
    execution_method: "calculate_statistics"
    description: "Performs secure statistical calculations on analysis results"
    inputs:
      - analysis_results: "Raw analysis results from ensemble"
      - session_results_path: "Path to results directory"
    outputs:
      - stats_file_path: "Path to JSON file with statistical results"
```

**Model Registry Configuration**:
```yaml
# discernus/gateway/models.yaml
models:
  anthropic/claude-3-5-sonnet-20240620:
    provider: "anthropic"
    performance_tier: "top-tier"
    context_window: 200000
    costs:
      input_per_million_tokens: 3.00
      output_per_million_tokens: 15.00
    utility_tier: 1
    task_suitability: [synthesis, coordination, planning]
    optimal_batch_size: 8
```

### 5. Infrastructure-Only Software Components

**Principle**: Software handles routing, storage, and security - not intelligence.

**✅ THIN Implementation**:
```python
# discernus/gateway/llm_gateway.py
class LLMGateway:
    """Pure execution gateway - no intelligence, just routing"""
    
    def execute_call(self, model: str, prompt: str, system_prompt: str = "You are a helpful assistant.", 
                    max_retries: int = 3, **kwargs) -> Tuple[str, Dict[str, Any]]:
        """Executes LLM call with intelligent fallback and complete logging"""
        
        current_model = model
        attempts = 0
        
        while attempts < max_retries:
            attempts += 1
            
            try:
                # Clean parameters (infrastructure)
                clean_params = self.parameter_manager.get_clean_parameters(current_model, kwargs)
                
                # Execute call (infrastructure)
                response = litellm.completion(
                    model=current_model, 
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ], 
                    stream=False, 
                    **clean_params
                )
                
                # Extract usage data (infrastructure)
                usage_data = self._extract_usage_data(response)
                
                return content, {
                    "success": True, 
                    "model": current_model, 
                    "usage": usage_data, 
                    "attempts": attempts
                }
                
            except Exception as e:
                # Fallback logic (infrastructure)
                fallback_model = self.model_registry.get_fallback_model(current_model)
                if fallback_model:
                    current_model = fallback_model
                else:
                    return "", {"success": False, "error": str(e)}
```

**What This Component Does (Infrastructure)**:
- Routes requests to appropriate models
- Handles failures and retries
- Tracks usage and costs
- Manages provider-specific parameters

**What This Component Does NOT Do (Intelligence)**:
- Interpret LLM responses
- Make decisions about analysis
- Parse complex data structures
- Contain domain-specific logic

### 6. Complete Audit Trail for Reproducibility

**Principle**: Every decision logged for academic defense, not just final results.

**✅ THIN Implementation**:
```python
# discernus/core/project_chronolog.py
class ProjectChronolog:
    def log_event(self, event_type: str, session_id: str, data: Dict[str, Any]) -> str:
        """Log any project event with automatic timestamping and signing"""
        event = ChronologEvent(
            timestamp=datetime.utcnow().isoformat() + "Z",
            event=event_type,
            session_id=session_id,
            project=self.project_name,
            data=data
        )
        
        # Generate cryptographic signature for integrity
        event.signature = self._sign_event(event)
        
        # Append to chronolog with complete transparency
        self._append_event(event)
        
        # Automatically commit to Git for academic integrity
        self._commit_chronolog_event(event)
        
        return event.event_id
```

**Complete Reproducibility Features**:
- Cryptographic signatures for tamper evidence
- Git integration for version control
- Session-specific chronologs for replication
- Complete decision trail from start to finish

## THICK Anti-Patterns (AVOID THESE)

### 1. Complex JSON Parsing from LLM Responses

**❌ THICK Anti-Pattern**:
```python
# BAD: Software parsing complex LLM responses
def parse_analysis_results(llm_response: str) -> Dict[str, Any]:
    """THICK: Complex parsing logic that breaks easily"""
    try:
        json_match = re.search(r'```json\n(.*?)\n```', llm_response, re.DOTALL)
        if json_match:
            parsed_data = json.loads(json_match.group(1))
            
            # THICK: Software intelligence interpreting LLM output
            if 'score' in parsed_data:
                if parsed_data['score'] > 7.0:
                    parsed_data['category'] = 'high'
                elif parsed_data['score'] > 4.0:
                    parsed_data['category'] = 'medium'
                else:
                    parsed_data['category'] = 'low'
            
            return parsed_data
    except json.JSONDecodeError:
        # THICK: Complex error handling for parsing
        return {'error': 'Failed to parse LLM response'}
```

**Why This is THICK**:
- Software contains intelligence to interpret LLM responses
- Brittle parsing that breaks with format changes
- Complex error handling for parsing failures
- Software making analytical decisions (score categorization)

**✅ THIN Alternative**:
```python
# GOOD: Natural language processing
def process_analysis_response(llm_response: str) -> str:
    """THIN: Just save the response, let LLMs handle intelligence"""
    
    # Execute any code blocks if present
    enhanced_response = process_llm_code_request(conversation_id, speaker, llm_response)
    
    # Save to chronolog for complete reproducibility
    chronolog.log_event("ANALYSIS_COMPLETED", session_id, {
        'original_response': llm_response,
        'enhanced_response': enhanced_response,
        'timestamp': datetime.utcnow().isoformat()
    })
    
    return enhanced_response
```

### 2. Hardcoded Prompts in Orchestrator Code

**❌ THICK Anti-Pattern**:
```python
# BAD: Hardcoded prompts scattered throughout orchestrator
class ThickOrchestrator:
    def spawn_analysis_agent(self, framework: str, text: str):
        # THICK: Hardcoded prompt in orchestrator
        prompt = f"""You are an expert analyst. Analyze the following text using this framework:
        
        Framework: {framework}
        Text: {text}
        
        Provide a score from 1-10 and explain your reasoning.
        Return your response in JSON format with 'score' and 'reasoning' fields.
        """
        
        # THICK: Orchestrator contains analytical intelligence
        response = self.llm_gateway.execute_call("gpt-4", prompt)
        
        # THICK: Complex parsing logic
        return self._parse_analysis_response(response)
```

**Why This is THICK**:
- Prompts scattered throughout codebase
- Hard to modify or version control prompts
- Orchestrator contains analytical intelligence
- Tightly coupled to response format

**✅ THIN Alternative**:
```python
# GOOD: Centralized prompt management
class ThinOrchestrator:
    def spawn_analysis_agent(self, framework: str, text: str):
        # THIN: Get prompt from centralized location
        prompt = get_expert_prompt('analysis_agent', 
                                 framework=framework, 
                                 text=text)
        
        # THIN: Orchestrator just routes requests
        response = self.llm_gateway.execute_call("gpt-4", prompt)
        
        # THIN: No parsing, just return natural language
        return response
```

### 3. Mathematical Operations in Software

**❌ THICK Anti-Pattern**:
```python
# BAD: Software doing mathematical analysis
class ThickStatisticalAnalyzer:
    def calculate_framework_statistics(self, scores: List[float]) -> Dict[str, float]:
        """THICK: Software contains mathematical intelligence"""
        
        # THICK: Software calculating statistics
        mean_score = sum(scores) / len(scores)
        variance = sum((x - mean_score) ** 2 for x in scores) / len(scores)
        std_dev = variance ** 0.5
        
        # THICK: Software making analytical decisions
        if std_dev > 2.0:
            reliability = "low"
        elif std_dev > 1.0:
            reliability = "medium"
        else:
            reliability = "high"
        
        # THICK: Software interpreting results
        interpretation = self._interpret_statistical_significance(mean_score, std_dev)
        
        return {
            'mean': mean_score,
            'std_dev': std_dev,
            'reliability': reliability,
            'interpretation': interpretation
        }
```

**Why This is THICK**:
- Software contains mathematical intelligence
- Hardcoded thresholds for decision making
- Software interpreting statistical significance
- Opaque calculations that can't be audited

**✅ THIN Alternative**:
```python
# GOOD: LLM designs, secure code executes, LLM interprets
class ThinStatisticalAnalyzer:
    def calculate_framework_statistics(self, scores: List[float]) -> str:
        """THIN: LLM intelligence + secure code execution"""
        
        # THIN: LLM designs the statistical analysis
        analysis_prompt = get_expert_prompt('statistical_analysis_agent',
                                          scores=scores,
                                          task="Calculate descriptive statistics and assess reliability")
        
        # THIN: LLM returns analysis with code blocks
        llm_response = self.llm_gateway.execute_call("gpt-4", analysis_prompt)
        
        # THIN: Secure code execution handles mathematics
        enhanced_response = process_llm_code_request(self.session_id, 'statistical_agent', llm_response)
        
        # THIN: Return natural language analysis
        return enhanced_response
```

### 4. Monolithic Architecture with Tight Coupling

**❌ THICK Anti-Pattern**:
```python
# BAD: Monolithic class with multiple responsibilities
class ThickAnalysisEngine:
    def __init__(self):
        self.model_configs = self._load_hardcoded_models()
        self.prompt_templates = self._load_hardcoded_prompts()
        self.statistical_thresholds = self._load_hardcoded_thresholds()
    
    def run_complete_analysis(self, framework: str, corpus: List[str]):
        """THICK: Monolithic method with multiple responsibilities"""
        
        # THICK: Hardcoded model selection logic
        model = self._select_model_by_hardcoded_rules(framework)
        
        # THICK: Hardcoded prompt construction
        prompt = self._construct_analysis_prompt(framework, corpus)
        
        # THICK: Direct LLM calls with hardcoded parameters
        results = []
        for text in corpus:
            response = self._call_llm_directly(model, prompt, text)
            parsed_result = self._parse_with_complex_logic(response)
            results.append(parsed_result)
        
        # THICK: Software statistical analysis
        stats = self._calculate_statistics_in_software(results)
        
        # THICK: Software interpretation
        interpretation = self._interpret_results_in_software(stats)
        
        return {
            'results': results,
            'statistics': stats,
            'interpretation': interpretation
        }
```

**Why This is THICK**:
- Single class with multiple responsibilities
- Hardcoded configurations and logic
- Direct LLM calls without abstraction
- Complex parsing and interpretation logic

**✅ THIN Alternative**:
```python
# GOOD: Modular architecture with clear separation
class ThinAnalysisOrchestrator:
    def __init__(self):
        # THIN: Dependency injection of infrastructure components
        self.model_registry = get_model_registry()
        self.llm_gateway = LLMGateway(self.model_registry)
        self.chronolog = get_project_chronolog(self.project_path)
    
    def run_complete_analysis(self, framework: str, corpus: List[str]):
        """THIN: Orchestrator just coordinates, doesn't contain intelligence"""
        
        # THIN: Model registry handles intelligent selection
        model = self.model_registry.get_model_for_task('analysis')
        
        # THIN: Centralized prompt management
        prompt = get_expert_prompt('analysis_agent', framework=framework)
        
        # THIN: LLM gateway handles execution
        results = []
        for text in corpus:
            response = self.llm_gateway.execute_call(model, prompt.format(text=text))
            # THIN: No parsing, just save natural language
            results.append(response)
        
        # THIN: Statistical analysis by specialized agent
        stats_prompt = get_expert_prompt('statistical_analysis_agent', 
                                       results=results)
        stats_response = self.llm_gateway.execute_call(model, stats_prompt)
        
        # THIN: Secure code execution for calculations
        enhanced_stats = process_llm_code_request(self.session_id, 'stats_agent', stats_response)
        
        # THIN: Complete audit trail
        self.chronolog.log_event("ANALYSIS_COMPLETED", self.session_id, {
            'framework': framework,
            'corpus_size': len(corpus),
            'model_used': model,
            'results_count': len(results)
        })
        
        return enhanced_stats
```

## Implementation Guidelines

### For Human Developers

1. **Start with Natural Language**: Design LLM interactions first, then build minimal infrastructure around them
2. **Centralize Intelligence**: Put all prompts in `agent_roles.py`, all configurations in YAML files
3. **Use Secure Code Execution**: Never put mathematical operations in software - use the hybrid intelligence pattern
4. **Log Everything**: Use the chronolog system for complete reproducibility
5. **Avoid Parsing**: If you're parsing JSON from LLMs, you're probably doing it wrong

### For AI Agents

1. **Check for Parsing**: If your solution involves parsing LLM responses, reconsider the approach
2. **Use Existing Infrastructure**: Leverage model registry, LLM gateway, and chronolog systems
3. **Centralize Prompts**: Add new prompts to `agent_roles.py`, not inline in orchestrator code
4. **Follow Configuration Patterns**: Use YAML configuration for new agents and models
5. **Document Decisions**: Log rationale for architectural choices in chronolog

### Testing THIN Compliance

#### Quick Compliance Check
Ask yourself:
- [ ] Are LLMs doing the thinking, and software just providing infrastructure?
- [ ] Would a human researcher understand what's happening at each step?
- [ ] Can the system be audited for academic reproducibility?
- [ ] Are costs predictable and transparent?
- [ ] Can calculations be independently verified?

#### Red Flags (THICK Patterns)
- Complex JSON parsing from LLM responses
- Mathematical operations in software
- Hardcoded prompts in orchestrator code
- Decision-making logic in infrastructure components
- Opaque "black box" components

#### Green Flags (THIN Patterns)
- Natural language communication between components
- Centralized prompt management
- Secure code execution for calculations
- Configuration-driven extensibility
- Complete audit trails

## Migration from THICK to THIN

### Step 1: Identify THICK Components
Look for:
- Complex parsing logic
- Mathematical operations in software
- Hardcoded prompts
- Decision-making in infrastructure

### Step 2: Extract Intelligence
Move intelligence to:
- `agent_roles.py` for prompts
- LLM agents for analysis
- Secure code execution for calculations

### Step 3: Simplify Infrastructure
Replace complex logic with:
- Model registry for selection
- LLM gateway for execution
- Chronolog for logging
- Natural language communication

### Step 4: Validate Compliance
Test against:
- Three foundational commitments
- THIN compliance checklist
- Academic reproducibility requirements

## Benefits of THIN Architecture

### Academic Credibility
- **Transparent processes**: Every decision can be audited
- **Reproducible results**: Complete chronolog enables replication
- **Defensible methods**: Natural language makes processes understandable

### Cost Predictability
- **Upfront estimation**: Model registry provides accurate cost projections
- **Budget controls**: Infrastructure prevents cost overruns
- **Efficient execution**: Optimized for academic and institutional budgets

### Extensibility
- **Configuration-driven**: New capabilities added without code changes
- **Modular design**: Components can be independently updated
- **Domain-neutral**: Platform works across disciplines

### Reliability
- **Secure execution**: Mathematical operations protected from errors
- **Fallback systems**: Automatic recovery from failures
- **Complete logging**: Every operation tracked for debugging

**Remember**: THIN architecture isn't about using fewer tools - it's about putting intelligence in the right place (LLMs) and keeping software focused on infrastructure. This creates systems that are transparent, auditable, and trustworthy for academic and institutional use. 