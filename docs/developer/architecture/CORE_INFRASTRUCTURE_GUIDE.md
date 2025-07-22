# Core Infrastructure Guide
*Agent Registry, Model Registry, and LLM Gateway*

## Overview

Discernus core infrastructure implements a framework-agnostic, domain-neutral platform for computational text analysis. Every component is designed around three foundational commitments that ensure academic credibility and institutional trust.

## Three Foundational Commitments Integration

### Mathematical Reliability
Every infrastructure component supports the hybrid intelligence pattern: **LLM designs → secure code executes → LLM interprets**. This ensures computational accuracy while maintaining human-readable analysis.

### Cost Transparency  
All components provide upfront cost estimation, budget controls, and intelligent model selection to enable predictable institutional pricing.

### Complete Reproducibility
Every component maintains complete audit trails, decision documentation, and provenance chains that enable deterministic replication and academic defense.

## Agent Registry Architecture

### Dynamic Agent Discovery System
**Location**: `discernus/core/agent_registry.yaml`

The agent registry enables a modular ecosystem where new analytical capabilities can be registered and discovered without requiring core system modifications.

#### Agent Archetypes
```yaml
agents:
  - name: AnalysisAgent
    archetype: Role-Playing
    module: "discernus.orchestration.ensemble_orchestrator"
    execution_method: "_spawn_analysis_agents"
    description: "Primary workhorse agent that applies frameworks to documents"
    
  - name: StatisticalAnalysisAgent
    archetype: Tool-Using
    module: "discernus.agents.statistical_analysis_agent"
    execution_method: "calculate_statistics"
    description: "Performs secure statistical calculations on analysis results"
```

#### Input/Output Contracts
Each agent defines clear contracts for reproducibility:
```yaml
inputs:
  - framework_content: "The full text of the analytical framework"
  - text_content: "The content of the single document to be analyzed"
  - analysis_instructions: "Specific instructions for this analysis run"
outputs:
  - analysis_results: "Structured analysis with evidence and reasoning"
```

### Foundational Commitments Implementation

**Mathematical Reliability**: 
- `StatisticalAnalysisAgent` uses secure code execution for all calculations
- `StatisticalInterpretationAgent` translates mathematical results into natural language
- Clear separation between LLM reasoning and computational operations

**Cost Transparency**:
- `ExecutionPlannerAgent` provides upfront cost estimates based on corpus size and model selection
- `EnsembleConfigurationAgent` assesses model health and recommends cost-effective alternatives

**Complete Reproducibility**:
- Every agent logs inputs, outputs, and execution context
- Agent registry provides complete specification of capabilities and execution methods
- Prompt sources are centralized and versioned

## Model Registry and Intelligent Selection

### Unified Model Access
**Location**: `discernus/gateway/model_registry.py`

The model registry provides intelligent model selection with cost awareness and reliability guarantees.

#### Core Implementation Pattern
```python
class ModelRegistry:
    def __init__(self, config_path: Optional[str] = None):
        self.config_path = Path(config_path or Path(__file__).parent / 'models.yaml')
        self.models = self._load_models()
    
    def get_model_for_task(self, task_type: str) -> Optional[str]:
        # Filter models suitable for the task
        suitable_models = [
            name for name, details in self.models.items()
            if task_type in details.get('task_suitability', [])
        ]
        
        # Sort by utility tier (lower is better)
        sorted_models = sorted(suitable_models, 
                             key=lambda name: self.models[name].get('utility_tier', 99))
        
        return sorted_models[0]
```

#### Intelligent Fallback Chain
```python
def get_fallback_model(self, failed_model_name: str) -> Optional[str]:
    """Gets the next best model in the fallback chain"""
    failed_model_details = self.get_model_details(failed_model_name)
    current_tier = failed_model_details.get('utility_tier')
    
    # Find models with higher utility tier (lower priority)
    fallback_candidates = [
        name for name, details in self.models.items()
        if details.get('utility_tier', 99) > current_tier
    ]
    
    return sorted(fallback_candidates, 
                 key=lambda name: self.models[name].get('utility_tier', 99))[0]
```

### Model Configuration Structure
**Location**: `discernus/gateway/models.yaml`

```yaml
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
    last_updated: "2025-01-15"
```

### Foundational Commitments Implementation

**Mathematical Reliability**:
- Consistent model access ensures reproducible computational workflows
- Model health checking prevents calculation failures
- Fallback chains maintain computational continuity

**Cost Transparency**:
- Complete cost data per model (input/output token pricing)
- Utility tier system for cost-aware selection
- Optimal batch size recommendations for cost efficiency
- Upfront cost estimation for any task/model combination

**Complete Reproducibility**:
- Complete model configuration logging
- Version tracking with `last_updated` timestamps
- Provider and performance tier documentation
- Deterministic model selection based on task requirements

## LLM Gateway Routing

### Provider Abstraction Layer
**Location**: `discernus/gateway/llm_gateway.py`

The LLM Gateway provides unified access to multiple providers while maintaining complete transparency and reliability.

#### Core Execution Pattern
```python
class LLMGateway:
    def execute_call(self, model: str, prompt: str, system_prompt: str = "You are a helpful assistant.", 
                    max_retries: int = 3, **kwargs) -> Tuple[str, Dict[str, Any]]:
        """Executes LLM call with intelligent fallback and complete logging"""
        
        current_model = model
        attempts = 0
        
        while attempts < max_retries:
            attempts += 1
            
            try:
                # Clean parameters based on provider requirements
                clean_params = self.parameter_manager.get_clean_parameters(current_model, kwargs)
                
                response = litellm.completion(
                    model=current_model, 
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": prompt}
                    ], 
                    stream=False, 
                    **clean_params
                )
                
                # Extract and log usage data
                usage_data = self._extract_usage_data(response)
                
                return content, {
                    "success": True, 
                    "model": current_model, 
                    "usage": usage_data, 
                    "attempts": attempts
                }
                
            except Exception as e:
                fallback_model = self.model_registry.get_fallback_model(current_model)
                if fallback_model:
                    current_model = fallback_model
                else:
                    return "", {"success": False, "error": str(e), "model": current_model}
```

#### Health Checking System
```python
async def check_model_health(self, model_name: str) -> Dict[str, Any]:
    """Checks model health with complete diagnostic information"""
    try:
        messages = [{"role": "user", "content": "Hello, model!"}]
        clean_params = self.parameter_manager.get_clean_parameters(model_name, {})
        litellm.completion(model=model_name, messages=messages, stream=False, **clean_params)
        
        return {'is_healthy': True, 'message': 'Model is responsive.'}
    except Exception as e:
        return {'is_healthy': False, 'message': f'Health check failed: {str(e)}'}
```

### Foundational Commitments Implementation

**Mathematical Reliability**:
- Consistent parameter cleaning ensures reproducible model behavior
- Health checking prevents calculation failures
- Automatic retry with fallback maintains computational reliability

**Cost Transparency**:
- Complete usage tracking (prompt_tokens, completion_tokens, total_tokens)
- Cost calculation based on model registry pricing
- Fallback cost implications clearly documented
- Upfront cost estimation before execution

**Complete Reproducibility**:
- Complete request/response logging
- Parameter cleaning and provider-specific handling documented
- Retry attempts and fallback decisions logged
- Model selection rationale captured for audit

## Centralized Prompt Management

### THIN Compliance System
**Location**: `discernus/core/agent_roles.py`

Centralized prompt management ensures consistency and prevents hardcoded intelligence in orchestrator code.

#### Expert Agent Prompts
```python
EXPERT_AGENT_PROMPTS = {
    'corpus_detective_agent': """You are a corpus_detective_agent, specializing in systematic analysis of user-provided text corpora.

RESEARCH QUESTION: {research_question}

SOURCE TEXTS:
{source_texts}

The moderator_llm has requested your corpus analysis expertise:

MODERATOR REQUEST: {expert_request}

Your Task:
Analyze the provided corpus systematically and help the user understand what they have...
""",
    
    'knowledgenaut_agent': """You are a knowledgenaut_agent, a specialized research agent with expertise in academic literature discovery and framework interrogation.

RESEARCH QUESTION: {research_question}

The research infrastructure will automatically:
- Execute literature searches based on your research question
- Validate paper quality and detect systematic biases
- Synthesize findings with confidence levels
- Provide adversarial critique for quality control
- Generate comprehensive research reports
"""
}
```

#### Dynamic Prompt Generation
```python
def get_expert_prompt(expert_type: str, **kwargs) -> str:
    """Get expert prompt with dynamic parameter substitution"""
    template = EXPERT_AGENT_PROMPTS.get(expert_type, EXPERT_AGENT_PROMPTS['generic_expert'])
    return template.format(**kwargs)
```

### Foundational Commitments Implementation

**Mathematical Reliability**:
- Consistent prompt formatting ensures reproducible LLM behavior
- Expert specialization prevents calculation errors through domain expertise
- Clear separation between prompts and execution logic

**Cost Transparency**:
- Centralized prompts enable accurate token count estimation
- Expert templates optimize for efficiency while maintaining quality
- Prompt versioning supports cost impact analysis

**Complete Reproducibility**:
- All prompts centrally managed and versioned
- Dynamic parameter substitution logged
- Expert selection rationale documented
- Prompt evolution tracked for academic consistency

## Chronolog and Provenance System

### Complete Reproducibility Implementation
**Location**: `discernus/core/project_chronolog.py`

The chronolog system is the primary mechanism for achieving zero mystery in analytical processes.

#### Project-Level Audit Trail
```python
class ProjectChronolog:
    def __init__(self, project_path: str, signing_key: Optional[str] = None):
        self.project_path = Path(project_path)
        self.chronolog_file = self.project_path / f"PROJECT_CHRONOLOG_{self.project_name}.jsonl"
        
        # Cryptographic signing for tamper evidence
        self.signing_key = signing_key or os.getenv('CHRONOLOG_SIGNING_KEY', 'default_dev_key')
        
        # Git integration for reliable persistence
        self.git_repo = git.Repo(self.project_path, search_parent_directories=True)
```

#### Event Integrity and Verification
```python
def _sign_event(self, event: ChronologEvent) -> str:
    """Generate cryptographic signature for event integrity"""
    canonical_data = {
        'timestamp': event.timestamp,
        'event': event.event, 
        'session_id': event.session_id,
        'project': event.project,
        'event_id': event.event_id,
        'data': event.data
    }
    
    canonical_json = json.dumps(canonical_data, sort_keys=True, separators=(',', ':'))
    signature = hmac.new(
        self.signing_key.encode('utf-8'),
        canonical_json.encode('utf-8'),
        hashlib.sha256
    ).hexdigest()
    
    return signature
```

#### Academic Integrity Features
```python
def create_run_chronolog(self, session_id: str, results_directory: str) -> Dict[str, Any]:
    """Create run-specific chronolog for academic integrity"""
    # Filter project chronolog for this session
    session_events = []
    with open(self.chronolog_file, 'r', encoding='utf-8') as f:
        for line in f:
            event_dict = json.loads(line.strip())
            if event_dict.get('session_id') == session_id:
                session_events.append(event_dict)
    
    # Create run-specific chronolog file
    run_chronolog_file = Path(results_directory) / f"RUN_CHRONOLOG_{session_id}.jsonl"
    with open(run_chronolog_file, 'w', encoding='utf-8') as f:
        for event_dict in session_events:
            f.write(json.dumps(event_dict, separators=(',', ':')) + '\n')
    
    return {
        'status': 'run_chronolog_created',
        'session_events': len(session_events),
        'run_chronolog_file': str(run_chronolog_file)
    }
```

### Foundational Commitments Implementation

**Mathematical Reliability**:
- All mathematical operations logged with complete context
- Secure code execution events captured with input/output
- Calculation rationale preserved for verification

**Cost Transparency**:
- Complete cost tracking for every LLM call
- Model selection decisions logged with cost implications
- Budget utilization captured throughout project lifecycle

**Complete Reproducibility**:
- Cryptographic integrity for all events
- Git integration for tamper-evident persistence
- Session-specific chronologs for academic replication
- Complete decision trail from initialization to completion

## Secure Code Execution

### Mathematical Reliability Implementation
**Location**: `discernus/core/secure_code_executor.py`

The secure code executor implements the hybrid intelligence pattern essential for mathematical reliability.

#### Security-First Architecture
```python
class SecureCodeExecutor:
    def __init__(self, timeout_seconds: int = 30, memory_limit_mb: int = 256, 
                 enable_data_science: bool = True):
        self.timeout_seconds = timeout_seconds
        self.memory_limit_bytes = memory_limit_mb * 1024 * 1024
        self.security_checker = CodeSecurityChecker()
    
    def execute_code(self, code: str, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """Execute code safely with full logging and resource limits"""
        
        # Security check first
        is_safe, violations = self.security_checker.check_code_safety(code)
        if not is_safe:
            return {
                'success': False,
                'error': f"Security violations: {', '.join(violations)}",
                'security_violations': violations
            }
        
        # Execute with resource limits and complete logging
        return self._execute_in_sandbox(code)
```

#### AST-Based Security Analysis
```python
class CodeSecurityChecker:
    def check_code_safety(self, code: str) -> Tuple[bool, List[str]]:
        """Analyze code using AST for security violations"""
        try:
            tree = ast.parse(code)
            self.visit_node(tree)
        except SyntaxError as e:
            self.violations.append(f"Syntax error: {e}")
            return False, self.violations
        
        return len(self.violations) == 0, self.violations
```

#### Calculation Transparency
```python
def process_llm_code_request(conversation_id: str, speaker: str, response: str) -> str:
    """Enhanced code execution with complete transparency"""
    
    code_blocks = re.findall(r'```python\n(.*?)\n```', response, re.DOTALL)
    if not code_blocks:
        return response
    
    executor = SecureCodeExecutor(enable_data_science=True)
    enhanced_response = response
    
    for i, code in enumerate(code_blocks):
        result = executor.execute_code(code)
        
        # Log execution for experiment provenance
        execution_entry = {
            'conversation_id': conversation_id,
            'speaker': speaker,
            'code_block_index': i,
            'code': code,
            'timestamp': time.time(),
            'result': result
        }
        
        # Add transparent results to response
        enhanced_response += f"\n\n**🔐 Secure Code Execution Result:**\n```\n{result['output']}\n```"
        enhanced_response += f"\n*Execution time: {result['execution_time']:.3f}s*"
    
    return enhanced_response
```

### Foundational Commitments Implementation

**Mathematical Reliability**:
- Hybrid intelligence pattern: LLM designs → secure code executes → LLM interprets
- AST-based security prevents malicious code execution
- Resource limits ensure computational stability
- Complete separation of reasoning and calculation

**Cost Transparency**:
- Execution time tracking for cost analysis
- Resource utilization monitoring
- Security overhead clearly documented
- Performance metrics for budget planning

**Complete Reproducibility**:
- Complete code execution logging
- Security analysis results preserved
- Resource usage tracking
- Execution environment documentation
- Calculation audit trail for academic defense

## Integration Patterns

### Cross-Component Workflow
All infrastructure components work together to support the three foundational commitments:

1. **Model Registry** provides cost-aware model selection
2. **LLM Gateway** executes with complete usage tracking
3. **Secure Code Executor** handles mathematical operations
4. **Chronolog System** captures complete decision trail
5. **Agent Registry** provides reproducible capability discovery

### Academic Adoption Support
The infrastructure enables institutional adoption through:
- **Predictable costs** via model registry and gateway tracking
- **Reproducible results** via chronolog and secure execution
- **Transparent methods** via centralized prompt management
- **Reliable computation** via secure code execution

### Extension and Customization
The infrastructure supports the Drupal-style ecosystem through:
- **YAML-based configuration** for new agents and models
- **Centralized prompt management** for consistent behavior
- **Secure execution environment** for custom calculations
- **Complete audit trail** for regulatory compliance

This infrastructure creates the foundation for domain-neutral computational text analysis that amplifies human intelligence while maintaining the rigor, transparency, and reliability required for academic and institutional adoption. 