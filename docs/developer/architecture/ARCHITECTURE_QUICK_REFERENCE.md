# 📖 Architecture Quick Reference

## Core Philosophy: "Thick LLM + Thin Software = Epistemic Trust"

### Strategic Vision
Discernus exists to **dramatically advance understanding of human rhetoric using methods that are both rigorous and scalable**. We're building a domain-neutral platform that can analyze any rhetorical text with unprecedented precision.

### Design Principles
1. **Human Intelligence Amplifier**: Technology amplifies human judgment, never replaces it
2. **Framework-Agnostic**: Political science is our lead use case, not our only use case
3. **Epistemic Trust**: Transparency and adversarial review build trust in results
4. **Drupal-Style Ecosystem**: Tightly controlled core, open module ecosystem

---

## 🏗️ THIN Architecture Patterns

### ✅ THIN Pattern: Natural Language Flow
```python
# GOOD - Natural language communication
def analyze_text(text: str, framework: str) -> str:
    prompt = f"""
    Analyze this text using {framework}:
    {text}
    
    Provide your analysis in natural language with specific evidence.
    """
    response = llm_gateway.call(prompt)
    return response  # Pass through as natural language

# Next agent can read this directly
next_prompt = f"Previous analysis: {response}\n\nNow synthesize..."
```

### 🚫 THICK Anti-Pattern: JSON Parsing
```python
# BAD - Parsing structured data from LLM
def analyze_text(text: str, framework: str) -> dict:
    prompt = f"Analyze {text} and return JSON with scores..."
    response = llm_gateway.call(prompt)
    
    # This is THICK - software interpreting LLM intelligence
    data = json.loads(response)
    score = data.get('score', 0)
    return {'processed_score': score * 1.5}  # Software intelligence!
```

### ✅ THIN Pattern: Environment-Agnostic Python Execution
```python
# GOOD - Portable across environments
import sys
PYTHON_EXECUTABLE = sys.executable

AGENT_SCRIPTS = {
    'pre_test': [PYTHON_EXECUTABLE, 'agents/PreTestAgent/main.py'],
    'analyse_batch': [PYTHON_EXECUTABLE, 'agents/AnalyseBatchAgent/main.py'],
}

# Works in venv, conda, system Python, Windows, etc.
subprocess.run([PYTHON_EXECUTABLE, 'some_script.py'])
```

### 🚫 THICK Anti-Pattern: Hardcoded Environment Paths
```python
# BAD - Breaks in different environments
AGENT_SCRIPTS = {
    'pre_test': ['venv/bin/python3', 'agents/PreTestAgent/main.py'],  # macOS only
    'analyse_batch': ['python3', 'agents/AnalyseBatchAgent/main.py'], # System python
}

# BAD - Platform-specific paths
command = "venv/bin/python3 scripts/router.py"  # Won't work on Windows
command = "python3 scripts/test_runner.py"      # Wrong environment
```

**🎯 Architectural Principle**: Never hardcode environment-specific paths in business logic. Use `sys.executable` to automatically detect the current Python environment.

### ✅ THIN Pattern: Agent Registry Usage
```python
# GOOD - Dynamic agent discovery
def spawn_analysis_agent(framework: str, text: str):
    agent_def = agent_registry.get_agent('AnalysisAgent')
    prompt = get_expert_prompt(
        'analysis_expert',
        framework=framework,
        text=text
    )
    agent = create_agent_instance(agent_def)
    return agent.execute(prompt)
```

### 🚫 THICK Anti-Pattern: Hardcoded Agents
```python
# BAD - Hardcoded agent instantiation
def spawn_analysis_agent(framework: str, text: str):
    if framework == 'PDAF':
        agent = PDFAnalysisAgent()
    elif framework == 'CFF':
        agent = CFFAnalysisAgent()
    else:
        agent = GenericAnalysisAgent()
    return agent.analyze(text)
```

---

## 🔧 Core Infrastructure Components


### LLM Gateway (`discernus/gateway/llm_gateway.py`)
**Purpose**: Provider abstraction with parameter management
**Usage**: All LLM calls go through gateway

```python
# GOOD - Gateway with provider abstraction
response, metadata = llm_gateway.execute_call(
    model='anthropic/claude-3-5-sonnet-20240620',
    prompt=prompt
)

# BAD - Direct provider calls
import anthropic
client = anthropic.Anthropic()
response = client.messages.create(...)
```

### Project Chronolog (`discernus/core/project_chronolog.py`)
**Purpose**: Academic provenance and audit trail
**Usage**: Log all significant events for transparency

```python
# GOOD - Comprehensive logging
log_project_event(
    project_path, 
    "ANALYSIS_STARTED", 
    session_id, 
    {"model": model_name, "framework": framework}
)

# BAD - No logging or minimal logging
print(f"Starting analysis with {model_name}")
```

---

## 📊 Mathematical Operations: The Hybrid Pattern

### ✅ THIN Pattern: LLM Design + Secure Execution
```python
# GOOD - LLM designs, code executes, LLM interprets
class StatisticalAnalysisAgent:
    def calculate_statistics(self, analysis_results):
        # LLM INTELLIGENCE: Design statistical approach
        calculation_design = await self.llm_gateway.call(
            "Design Python code for Cronbach's alpha calculation...",
            "statistical_designer"
        )
        
        # SECURE CODE EXECUTION: Perform calculations
        execution_result = await self.code_executor.execute_code(
            calculation_design, analysis_results
        )
        
        # LLM INTELLIGENCE: Interpret results
        interpretation = await self.llm_gateway.call(
            f"Interpret these statistical results: {execution_result}",
            "statistical_interpreter"
        )
        
        return interpretation
```

### 🚫 THICK Anti-Pattern: Software Math
```python
# BAD - Mathematical operations in software
def calculate_statistics(self, analysis_results):
    scores = [r['score'] for r in analysis_results]
    mean_score = sum(scores) / len(scores)  # Software intelligence!
    std_dev = statistics.stdev(scores)      # Software intelligence!
    return {'mean': mean_score, 'std': std_dev}
```

---

## 🎯 Domain-Neutral Design Patterns

### ✅ THIN Pattern: Framework-Agnostic Core
```python
# GOOD - Works for any framework
class FrameworkAnalyzer:
    def analyze_with_framework(self, framework_spec: str, text: str):
        prompt = f"""
        You are an expert analyst applying this framework:
        {framework_spec}
        
        Analyze this text systematically:
        {text}
        
        Provide thorough analysis with specific evidence.
        """
        return self.llm_gateway.call(prompt)
```

### 🚫 THICK Anti-Pattern: Framework-Specific Logic
```python
# BAD - Hardcoded framework assumptions
class FrameworkAnalyzer:
    def analyze_with_framework(self, framework_name: str, text: str):
        if framework_name == 'PDAF':
            return self.analyze_populist_discourse(text)
        elif framework_name == 'CFF':
            return self.analyze_cohesive_flourishing(text)
        else:
            raise ValueError(f"Unknown framework: {framework_name}")
```

---

## 🚨 Common Pitfalls and Solutions

### Pitfall 1: "Helper Functions" for LLM Responses
```python
# SUBTLE THICK - Looks innocent but is parsing in disguise
def extract_confidence_score(llm_response: str) -> float:
    # This is still parsing!
    match = re.search(r'confidence:\s*(\d+)', llm_response)
    return float(match.group(1)) if match else 0.0

# THIN SOLUTION - Let LLM provide what you need
def get_confidence_assessment(llm_response: str) -> str:
    prompt = f"""
    Based on this analysis: {llm_response}
    
    How confident should we be in this assessment? 
    Explain your reasoning.
    """
    return llm_gateway.call(prompt)
```

### Pitfall 2: Complex Orchestrator Logic
```python
# THICK - Orchestrator making decisions
def orchestrate_analysis(texts, framework):
    if len(texts) > 10:
        strategy = 'batch_processing'
    elif framework == 'complex':
        strategy = 'ensemble_analysis'
    else:
        strategy = 'simple_analysis'
    
    return execute_strategy(strategy, texts, framework)

# THIN SOLUTION - LLM makes decisions
def orchestrate_analysis(texts, framework):
    decision_prompt = f"""
    I need to analyze {len(texts)} texts using {framework}.
    What's the best approach? Consider:
    - Corpus size and complexity
    - Framework requirements
    - Resource constraints
    
    Recommend a strategy and explain your reasoning.
    """
    strategy = llm_gateway.call(decision_prompt)
    return execute_llm_strategy(strategy, texts, framework)
```

---

## 🎯 Success Metrics

### Technical Success
- **Registry Usage**: All agents and models discovered via registry
- **Natural Language**: No JSON parsing from LLM responses
- **Secure Math**: All calculations via SecureCodeExecutor
- **Complete Logging**: Full audit trail for academic transparency

### User Experience Success
- **Conversational Feel**: Researchers feel like they're collaborating
- **Transparent Process**: Users can see what's happening
- **Human Agency**: Researchers maintain control and oversight
- **Professional Results**: Output ready for academic use

### Ecosystem Success
- **Framework Agnostic**: Works with any systematic analysis framework
- **Domain Neutral**: Supports political science, corporate communications, etc.
- **Extensible**: Easy to add new capabilities via modules
- **Maintainable**: Minimal code that's easy to understand and modify

---

## 🔗 Next Steps

- **Need more detail?** See `AGENT_DESIGN_PRINCIPLES.md`
- **Strategic context?** See `DISCERNUS_STRATEGIC_VISION.md`
- **Implementation help?** See `CORE_INFRASTRUCTURE.md`
- **Quick compliance check?** See `THIN_COMPLIANCE_CHECKLIST.md`

---

*Remember: When in doubt, choose the approach that amplifies human intelligence rather than replacing it. The best THIN architecture feels like collaborating with a brilliant research assistant.* 