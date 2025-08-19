# Fast Iteration Testing Methods

## Overview

This document outlines two critical testing methodologies that enable rapid development iteration without the cost and time overhead of full experiment runs:

1. **Mock Testing for Infrastructure** - Test code logic with simulated data
2. **Prompt Engineering Testing Harness** - Iterate on LLM prompts directly

## 1. Mock Testing for Infrastructure

### When to Use
- Testing data parsing, transformation, and validation logic
- Debugging file I/O, database queries, or API integrations
- Validating business logic without external dependencies
- Testing error handling and edge cases
- Infrastructure changes that don't require real LLM responses

### Benefits
- **Speed**: Instant feedback vs. 5+ minute experiment runs
- **Cost**: Zero API costs for infrastructure testing
- **Reliability**: Deterministic results for debugging
- **Isolation**: Test specific components without system complexity

### Implementation Pattern

```python
#!/usr/bin/env python3
"""
Mock test for [component_name] using simulated data.
No API calls needed - just tests the infrastructure logic.
"""

import json
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_component_logic():
    """Test the component logic with mocked data."""
    
    # 1. Create realistic mock data that matches expected structure
    mock_data = {
        "field1": "value1",
        "field2": "value2",
        # ... structure matching real data
    }
    
    # 2. Test each step of the logic
    print("🔬 Testing [component] logic with mocked data...")
    
    # Test 1: Data extraction
    result1 = extract_data(mock_data)
    print(f"✅ Step 1 result: {result1}")
    
    # Test 2: Data transformation
    result2 = transform_data(result1)
    print(f"✅ Step 2 result: {result2}")
    
    # Test 3: Validation
    result3 = validate_data(result2)
    print(f"✅ Step 3 result: {result3}")
    
    # 3. Verify final output structure
    if validate_output(result3):
        print("✅ All tests passed - logic is working")
    else:
        print("❌ Output validation failed")

if __name__ == "__main__":
    test_component_logic()
```

### Mock Data Best Practices
- **Realistic Structure**: Match the exact data format expected by the component
- **Edge Cases**: Include boundary conditions and error scenarios
- **Minimal Size**: Use small, focused datasets that test the logic
- **Documentation**: Clearly document what each mock represents

### Example: Data Extraction Testing
```python
# Mock the exact structure from EnhancedAnalysisAgent artifacts
mock_artifact_data = {
    "batch_id": "batch_123",
    "raw_analysis_response": """```
<<<DISCERNUS_ANALYSIS_JSON_v6>>>
{"document_analyses": [{"document_name": "test.txt", "dimensional_scores": {...}}]}
<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>
```"""
}
```

## 2. Prompt Engineering Testing Harness

### When to Use
- Iterating on LLM prompt design and structure
- Testing different prompt variations for optimal responses
- Debugging LLM response parsing and validation
- Optimizing prompt performance and cost
- Testing framework-specific prompt templates

### Benefits
- **Direct Control**: Test prompts without pipeline complexity
- **Rapid Iteration**: Quick feedback on prompt effectiveness
- **Cost Control**: Test with cheaper models (Flash Lite)
- **Focused Testing**: Isolate prompt issues from infrastructure problems

### Implementation Pattern

```python
#!/usr/bin/env python3
"""
Prompt engineering test harness for [agent_name].
Test LLM responses directly without full pipeline execution.
"""

import json
import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent.parent))

from discernus.gateway.llm_gateway import LLMGateway
from discernus.core.config import Config

def test_prompt_variations():
    """Test different prompt variations with the LLM."""
    
    # 1. Initialize LLM gateway with test configuration
    config = Config()
    gateway = LLMGateway(config)
    
    # 2. Load the prompt template
    prompt_template = load_prompt_template("path/to/prompt.yaml")
    
    # 3. Test different prompt variations
    test_cases = [
        {
            "name": "Baseline prompt",
            "prompt": prompt_template,
            "expected": "structured JSON response"
        },
        {
            "name": "Enhanced clarity prompt", 
            "prompt": prompt_template.replace("analyze", "carefully analyze"),
            "expected": "more detailed analysis"
        }
        # ... more variations
    ]
    
    # 4. Execute each test case
    for test_case in test_cases:
        print(f"\n🧪 Testing: {test_case['name']}")
        
        try:
            response = gateway.chat.completions.create(
                model="vertex_ai/gemini-2.5-flash-lite",  # Use cheaper model for testing
                messages=[{"role": "user", "content": test_case['prompt']}],
                max_tokens=1000
            )
            
            # 5. Validate response quality
            quality_score = validate_response_quality(response.content, test_case['expected'])
            print(f"✅ Quality score: {quality_score}/10")
            
            # 6. Test response parsing
            parsed = parse_response(response.content)
            if parsed:
                print(f"✅ Parsing successful: {len(parsed)} items")
            else:
                print(f"❌ Parsing failed")
                
        except Exception as e:
            print(f"❌ Test failed: {e}")

def validate_response_quality(response, expected):
    """Rate response quality on a scale of 1-10."""
    score = 0
    
    # Check for expected content
    if expected.lower() in response.lower():
        score += 3
    
    # Check for structured format
    if "{" in response and "}" in response:
        score += 2
    
    # Check for completeness
    if len(response) > 100:
        score += 2
    
    # Check for clarity
    if "error" not in response.lower() and "sorry" not in response.lower():
        score += 3
    
    return min(score, 10)

if __name__ == "__main__":
    test_prompt_variations()
```

### Prompt Testing Best Practices
- **Use Cheaper Models**: Flash Lite for iteration, Pro for final validation
- **Test Variations**: Try different phrasings, structures, and examples
- **Validate Output**: Check both content quality and parsing success
- **Document Results**: Keep track of what works and what doesn't
- **Iterate Quickly**: Make small changes and test immediately

## 3. When to Use Each Method

### Use Mock Testing When:
- [x] Debugging data extraction bugs
- [x] Testing file I/O operations
- [x] Validating business logic
- [x] Testing error handling
- [x] Infrastructure changes
- [x] Unit testing components

### Use Prompt Engineering Harness When:
- [x] LLM responses are inconsistent
- [x] Prompt templates need optimization
- [x] Testing different prompt variations
- [x] Debugging parsing failures
- [x] Cost optimization
- [x] Framework-specific prompt testing

### Use Full Experiment Runs When:
- [x] End-to-end integration testing
- [x] Performance benchmarking
- [x] Production validation
- [x] User acceptance testing
- [x] Final quality assurance

## 4. Implementation Checklist

### Mock Testing Setup
- [ ] Create test script in project root
- [ ] Import necessary modules
- [ ] Create realistic mock data
- [ ] Test each step of the logic
- [ ] Validate final output
- [ ] Document test results

### Prompt Engineering Setup
- [ ] Initialize LLM gateway
- [ ] Load prompt templates
- [ ] Define test cases
- [ ] Execute with cheaper models
- [ ] Validate response quality
- [ ] Test response parsing

## 5. Cost and Time Comparison

| Method | Time | Cost | Use Case |
|--------|------|------|----------|
| Mock Testing | Seconds | $0 | Infrastructure logic |
| Prompt Harness | Minutes | $0.01-0.05 | LLM prompt iteration |
| Full Experiment | 5-15 minutes | $0.10-0.50 | Integration testing |

## 6. Example Workflow

1. **Identify Issue**: Data extraction returning empty results
2. **Mock Test**: Create test with simulated data to validate logic
3. **Fix Logic**: Correct the data extraction method
4. **Mock Validation**: Verify fix works with test data
5. **Prompt Test** (if needed): Test LLM response parsing
6. **Full Validation**: Run one experiment to confirm end-to-end success

## 7. Memory Commitments

This document commits to memory the following testing principles:

1. **Always use mocks first** for infrastructure and logic testing
2. **Use prompt engineering harness** for LLM response iteration
3. **Reserve full experiments** for integration and final validation
4. **Test fast, iterate fast, fix fast**
5. **Minimize API costs during development**
6. **Isolate problems before running expensive operations**

## 8. Related Documentation

- [CLI Best Practices](../CLI_BEST_PRACTICES.md)
- [Troubleshooting Guide](../troubleshooting/TROUBLESHOOTING_GUIDE.md)
- [Development Workflows](../workflows/DEVELOPMENT_WORKFLOW.md)
