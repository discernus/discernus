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

## Five-Tier Testing Strategy

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

### ✅ Tier 2: Simple Working Tests (3 minutes)
**File**: `simple_working_tests.py`
**Purpose**: Comprehensive testing with guaranteed success

```bash
python3 discernus/tests/simple_working_tests.py
python3 -m unittest discernus.tests.simple_working_tests -v
```

**What it tests**:
- All core imports and agent initialization
- Mock gateway with queue-based responses
- Basic agent workflows (calculation, data extraction)
- Environment check utilities
- Individual test isolation

**Key Features**:
- **8 comprehensive tests** covering all major components
- **Standard Python testing patterns** 
- **Guaranteed to work** with simple, reliable mocks
- **Clear failure modes** when something is actually broken

### 🧠 Tier 3: Intelligent Integration Tests (5 minutes, ~$0.004)
**File**: `intelligent_integration_tests.py`
**Purpose**: Test prompts with real LLMs using cost-effective models

```bash
# Requires API keys (GOOGLE_APPLICATION_CREDENTIALS preferred, or ANTHROPIC_API_KEY)
# Standardized on Vertex AI Gemini 2.5 Flash for consistency
python3 discernus/tests/intelligent_integration_tests.py
python3 -m unittest discernus.tests.intelligent_integration_tests -v
```

**What it tests**:
- **Prompt intelligence validation** with real LLMs
- **Framework-agnostic behavior** with actual LLM responses
- **Error handling** with real LLM unpredictability
- **Calculation integration** with real numeric data
- **Cost-effective validation** using standardized Gemini 2.5 Flash ($0.35/$1.05)

**Key Features**:
- **Standardized on Gemini 2.5 Flash** for consistency and better rate limits
- Tests **actual prompt effectiveness** with real LLM intelligence
- Validates **framework-agnostic architecture** with real responses
- Maintains **cost efficiency** (less than half a penny per test run)
- Detects **prompt/response mismatches** that mocks miss
- **Better performance**: 163,840 TPM rate limits vs 25,000 TPM

**Cost Breakdown**:
- **Per test method**: ~$0.0007 (less than 1/10th of a penny)
- **Full test suite**: ~$0.004 (less than half a penny)
- **100 test runs**: ~$0.35 (7% of a coffee)
- **Daily development** (10 runs): ~$0.035 (0.7% of a coffee)
- **Practical impact**: Cost is negligible - run freely during development!

### 🏠 Tier 4: Local Intelligent Tests (15 minutes, FREE)
**File**: `local_intelligent_tests.py`
**Purpose**: Test prompts with local Ollama models (slow but free)

```bash
# Requires: ollama install && ollama pull mistral
python3 discernus/tests/local_intelligent_tests.py
python3 -m unittest discernus.tests.local_intelligent_tests -v
```

**What it tests**:
- **Local LLM integration** with Ollama models
- **Prompt validation** without API costs
- **Framework-agnostic behavior** with local intelligence
- **Performance characteristics** of local models
- **Resource usage patterns** for development

**Key Features**:
- **100% FREE** - no API costs ever
- **SLOW** - 30-60 seconds per test
- **Perfect for development** without budget constraints
- **Deterministic** with temperature=0
- **CI/CD friendly** for cost-conscious environments

### ⚠️ Tier 5: Legacy Complex Tests (May Be Broken)
**Files**: `comprehensive_test_suite.py`, `agent_isolation_test_framework.py`, `end_to_end_workflow_test.py`
**Purpose**: Advanced integration testing (use with caution)

```bash
# These tests may fail due to complex mock setups:
python3 discernus/tests/comprehensive_test_suite.py
python3 discernus/tests/agent_isolation_test_framework.py
python3 discernus/tests/end_to_end_workflow_test.py
```

**What they test**:
- Complex multi-framework scenarios
- Full workflow integration
- Advanced agent isolation
- CSV generation and validation

**Warning**: These tests have complex mock setups and may fail due to:
- Mock response mismatches
- Empty CSV file errors
- Integration test brittleness
- Over-engineered complexity

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

# Option B: Free local LLM testing (slow)
# Requires: ollama install && ollama pull mistral
python3 discernus/tests/local_intelligent_tests.py
```

**Note**: The cost is so negligible ($0.004 per full test suite) that you can run intelligent tests freely during development without budget concerns.

### Step 5: Run Specific Tests
```bash
# Individual test
python3 -m unittest discernus.tests.simple_working_tests.TestBasicFunctionality.test_imports_work -v

# Test discovery (finds only working tests)
python3 -m unittest discover discernus/tests -v
```

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
| Simple Working Tests | 3min | $0.00 | 100% | Comprehensive validation |
| Intelligent Integration Tests | 5min | ~$0.004 | 95% | Prompt intelligence validation |
| Local Intelligent Tests | 15min | $0.00 | 90% | Free intelligent validation |
| Legacy Tests | 10min | $0.00 | ~20% | Advanced integration |

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