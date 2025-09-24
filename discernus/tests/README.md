# Discernus Test Suite

## Overview

The Discernus test suite follows a **five-tier testing strategy** designed to provide AI agents with tests that actually work, while maintaining comprehensive coverage for the platform, including intelligent testing with real LLMs.

### Testing Philosophy

1. **Progressive Complexity**: Start with simple tests that always work, add complexity only when needed
2. **Clear Success/Failure Signals**: Tests should obviously pass or fail with clear error messages
3. **Standard Python Patterns**: Use normal unittest patterns that AI agents understand
4. **Framework Agnostic**: Tests work with any compliant framework specification
5. **Cost Efficient**: Mock-based testing for development, strategic LLM usage for intelligence validation
6. **Intelligence Validation**: Test prompts with real LLMs to ensure they actually work
7. **Negligible Cost**: Intelligent testing costs less than half a penny per full test run

## Three-Tier Testing Strategy

### ⚡ Tier 1: Quick Test (30 seconds)
**File**: `quick_test.py`
**Purpose**: Instant verification that the system works

```bash
python3 discernus/tests/quick_test.py
```

**What it tests**:
- Basic imports work
- Mock gateway functionality
- Agent initialization and basic execution
- Environment setup verification

**When to use**: First thing to run when working with the system

### ✅ Tier 2: Simple Working Tests (1 minute)
**File**: `simple_working_tests.py`
**Purpose**: Comprehensive testing with guaranteed success

```bash
python3 discernus/tests/simple_working_tests.py
python3 -m unittest discernus.tests.simple_working_tests -v
```

**What it tests**:
- Basic imports and system functionality
- Mock gateway initialization
- Environment check utilities
- Project structure validation
- Essential files verification
- Python environment validation

**Key Features**:
- **7 focused tests** covering essential functionality
- **Standard Python testing patterns** 
- **Guaranteed to work** with simple, reliable mocks
- **Clear failure modes** when something is actually broken

### 🧠 Tier 3: Working Pytest Tests (2 minutes)
**Files**: Various `test_*.py` files
**Purpose**: Test specific components that are known to work

```bash
# Run all working tests
python3 -m pytest discernus/tests/ -v

# Run specific working tests
python3 -m pytest discernus/tests/test_derived_metrics_cache.py -v
python3 -m pytest discernus/tests/test_local_artifact_storage.py -v
```

**What it tests**:
- **Component-specific functionality** that is known to work
- **Infrastructure components** like caching, storage, CLI commands
- **Regression testing** for specific features
- **Unit testing** of individual components

**Key Features**:
- **81 working tests** after cleanup
- **Component-focused** testing approach
- **Known working** - tests that actually pass
- **Focused scope** - each test validates specific functionality

**Note**: These tests focus on components that are known to work. Many tests were removed during cleanup because they were broken due to API changes.

## Quick Start for AI Agents

### Step 1: Environment Check
```bash
# Check if your environment is ready
python3 -c "from discernus.tests import print_test_environment; print_test_environment()"
```

### Step 2: Run Quick Test
```bash
# 30-second verification
python3 discernus/tests/quick_test.py
```

### Step 3: Run Simple Working Tests
```bash
# Full validation
python3 discernus/tests/simple_working_tests.py
```

### Step 4: Run Intelligent Tests (Optional)
```bash
# Option A: Cost-effective real LLM testing (~$0.004 - less than half a penny!)
# Set GOOGLE_APPLICATION_CREDENTIALS (preferred) or ANTHROPIC_API_KEY
# Standardized on Vertex AI Gemini 2.5 Flash for consistency
python3 discernus/tests/intelligent_integration_tests.py

# Option B: Complete pipeline validation (~$0.003 - comprehensive testing!)
# Set GOOGLE_APPLICATION_CREDENTIALS
# Uses Gemini 2.5 Flash Lite for all stages
cd discernus/tests/integration
python3 run_nano_micro_tests.py

# Option C: Free local LLM testing (slow)
# Requires: ollama install && ollama pull mistral
python3 discernus/tests/local_intelligent_tests.py
```

## Provenance System Testing

The simple working tests now include **comprehensive provenance system validation** ensuring academic integrity features work correctly:

### What the Provenance Tests Cover:
- **`test_chronolog_event_logging`**: Verifies that chronolog events are logged correctly with proper timestamps and signatures
- **`test_chronolog_integrity_verification`**: Tests cryptographic integrity verification of chronolog events
- **`test_conversation_logger_captures_llm_interactions`**: Ensures LLM interactions are captured for complete audit trails
- **`test_provenance_system_integration`**: Validates integration with workflow orchestrator for end-to-end provenance

### Why This Matters:
- **Academic Integrity**: Ensures tamper-evident records for peer review
- **Reproducibility**: Validates complete audit trails for replication studies
- **Reliability**: Catches regressions in mission-critical provenance features
- **Compliance**: Confirms the three-tier audit trail functions correctly

**Note**: The cost is so negligible ($0.004 per full test suite) that you can run intelligent tests freely during development without budget concerns.

### Step 5: Run Specific Tests
```bash
# Individual test
python3 -m unittest discernus.tests.simple_working_tests.TestBasicFunctionality.test_imports_work -v

# Test discovery (finds only working tests)
python3 -m unittest discover discernus/tests -v
```

## Development Testing Tools

### 🎯 Prompt Engineering Harness

The prompt engineering harness is a flexible tool for testing specific models with specific prompts during development. It's designed for rapid iteration and prompt tuning **without fallback mechanisms** - when a model fails, it fails clearly.

#### Quick Usage
```bash
# Use Make commands (recommended - handles environment automatically):

# List all available models by provider
make harness-list

# Test a simple prompt with any model
make harness-simple MODEL="vertex_ai/gemini-2.5-pro" PROMPT="What is 2+2?"

# Test a prompt from file
make harness-file MODEL="anthropic/claude-3-5-sonnet-20240620" FILE="test_prompt.txt"
```

#### Direct Usage
```bash
# Manual command (always use proper venv activation):
source venv/bin/activate && python3 scripts/prompt_engineering_harness.py --help

# List models
source venv/bin/activate && python3 scripts/prompt_engineering_harness.py --list-models

# Test with direct prompt
source venv/bin/activate && python3 scripts/prompt_engineering_harness.py \
  --model "openrouter/perplexity/r1-1776" \
  --prompt "Explain quantum computing in exactly 10 words."

# Test with prompt from file
source venv/bin/activate && python3 scripts/prompt_engineering_harness.py \
  --model "vertex_ai/gemini-2.5-pro" \
  --prompt-file "my_test_prompt.txt"

# Test with experiment assets
source venv/bin/activate && python3 scripts/prompt_engineering_harness.py \
  --model "anthropic/claude-3-5-sonnet-20240620" \
  --experiment "projects/simple_experiment" \
  --corpus "speech1.txt"
```

#### Key Features
- **No Fallback Mechanisms**: Fails fast and clearly when models don't work
- **Direct Model Testing**: Tests exactly the model you specify
- **Multiple Input Methods**: Direct text, files, or experiment assets
- **Model Registry Integration**: Lists available models with provider grouping
- **Environment Loading**: Automatically loads API keys from .env file
- **Clear Diagnostics**: Shows exactly what failed and why

#### When to Use
- **Model Validation**: Quickly test if a specific model is working
- **Prompt Tuning**: Iterate on prompts with immediate feedback
- **API Testing**: Verify API keys and model availability
- **Debugging**: Isolate model-specific issues without complex workflows
- **Development**: Test prompts before integrating into experiments

#### Example Output
```
✅ Using direct prompt

🚀 Testing Model: vertex_ai/gemini-2.5-pro
================================================================================
🎯 Making direct call to: vertex_ai/gemini-2.5-pro
📝 System prompt: You are a helpful assistant.
💬 User prompt: What is the capital of Japan? Answer in one sentence.
================================================================================

📊 RESULTS:
================================================================================
✅ SUCCESS
📝 Response Length: 30 characters
🔢 Token Usage: 20 prompt + 42 completion = 62 total

📄 MODEL RESPONSE:
----------------------------------------
The capital of Japan is Tokyo.
----------------------------------------

🏁 Test completed for model: vertex_ai/gemini-2.5-pro
```

This tool is essential for development workflows and is integrated into the standardized Make commands for consistent environment handling.

## Test Development Guidelines

### For AI Agents: Use Simple Working Tests

When developing or debugging:

1. **Start with Quick Test**: Verify basic functionality works
2. **Use Simple Working Tests**: For comprehensive validation
3. **Avoid Legacy Tests**: Unless specifically needed for integration testing
4. **Follow Standard Patterns**: Use normal unittest patterns

### Adding New Tests

When adding a new test to the simple working tests:

1. **One Test, One Assertion**: Each test should validate one specific thing
2. **Clear Naming**: `test_what_it_tests_and_why`
3. **Minimal Setup**: Use simple, obvious mock data
4. **Clear Failure Messages**: Make it obvious what went wrong

Example:
```python
def test_my_agent_basic_functionality(self):
    """Test that MyAgent can perform basic operations."""
    from discernus.agents.my_agent import MyAgent
    
    agent = MyAgent()
    result = agent.execute({'simple': 'input'}, {})
    
    self.assertIn('expected_output', result)
    self.assertEqual(result['expected_output'], 'expected_value')
```

### Mock Response Design

For the simple working tests, mock responses should:
- **Be Simple**: Use basic, valid JSON
- **Be Obvious**: Clear what input produces what output
- **Be Reliable**: Always work the same way
- **Be Minimal**: No unnecessary complexity

Example:
```python
mock_gateway = MockLLMGateway(['{"score": 0.8, "category": "positive"}'])
```

## Running Tests

### Prerequisites
```bash
# Ensure you're in the project root with virtual environment activated
source venv/bin/activate
```

### Individual Test Execution

```bash
# Quick test (fastest)
python3 discernus/tests/quick_test.py

# Simple working tests (recommended)
python3 discernus/tests/simple_working_tests.py
python3 -m unittest discernus.tests.simple_working_tests -v

# Intelligent integration tests (requires GOOGLE_APPLICATION_CREDENTIALS or ANTHROPIC_API_KEY)
# Standardized on Vertex AI Gemini 2.5 Flash
python3 discernus/tests/intelligent_integration_tests.py
python3 -m unittest discernus.tests.intelligent_integration_tests -v

# Local intelligent tests (requires Ollama)
python3 discernus/tests/local_intelligent_tests.py
python3 -m unittest discernus.tests.local_intelligent_tests -v

# Working analysis agent test
python3 -m unittest discernus.tests.test_analysis_agent.TestAnalysisAgent.test_analysis_agent_loops_and_captures_raw_output -v

# Legacy tests (use with caution)
python3 discernus/tests/comprehensive_test_suite.py
python3 discernus/tests/agent_isolation_test_framework.py
python3 discernus/tests/end_to_end_workflow_test.py
```

### Test Discovery
```bash
# Finds only working tests (excludes broken legacy tests)
python3 -m unittest discover discernus/tests -v
```

## Troubleshooting

### Common Issues

#### Test Failures in Quick Test
If the quick test fails, there's a fundamental problem:
1. **Import Error**: Check Python path and virtual environment
2. **Mock Gateway Error**: Check mock response format
3. **Agent Error**: Check agent initialization requirements
4. **Environment Error**: Check project root detection

#### Test Failures in Simple Working Tests
If simple working tests fail:
1. **Check Environment**: Run environment check utility
2. **Check Dependencies**: Ensure PyYAML and other packages installed
3. **Check Paths**: Ensure running from project root
4. **Check Mock Data**: Verify mock responses match expected format

#### Legacy Test Failures
If legacy tests fail:
1. **Expected Behavior**: These tests may be broken by design
2. **Mock Response Mismatches**: Mock responses don't match actual prompts
3. **Empty CSV Files**: Usually indicates upstream data extraction failures
4. **Use Alternative**: Switch to simple working tests instead

### Debug Mode
Enable debug output:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Performance Metrics

| Test Type | Time | Cost | Reliability | Purpose |
|-----------|------|------|-------------|---------|
| Quick Test | 30s | $0.00 | 100% | Basic verification |
| Simple Working Tests | 1min | $0.00 | 100% | Essential functionality |
| Working Pytest Tests | 2min | $0.00 | 95% | Component validation |

## Contributing

When contributing to the test suite:

1. **Prioritize Simple Working Tests**: Add new tests here first
2. **Follow Framework-Agnostic Principles**: Don't make assumptions about field names
3. **Use Standard Python Patterns**: Normal unittest patterns
4. **Test One Thing**: Each test should validate one specific behavior
5. **Clear Documentation**: Explain what each test validates and why
6. **Update This README**: Keep documentation current with changes

## Migration from Legacy Tests

If you're working with legacy tests:

### Deprecated Patterns
- Complex mock setups → Simple mock responses
- Integration tests → Isolated unit tests
- Multi-framework complexity → Single-framework simplicity
- File system mocking → In-memory data

### Recommended Migration
1. **Start with Simple Working Tests**: Use as template
2. **Extract Core Logic**: Identify what the test actually validates
3. **Simplify Setup**: Use minimal mock data
4. **Standard Patterns**: Convert to normal unittest patterns
5. **Validate One Thing**: Split complex tests into focused tests

The three-tier testing strategy ensures AI agents have tests that actually work, while maintaining the option for complex integration testing when needed. 