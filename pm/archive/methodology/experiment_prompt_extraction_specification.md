# Experiment Prompt Extraction System Specification v1.0
# Automated Parser for Coordinate-Free Discourse Analysis Experiments
#
# PURPOSE: Define precise rules for extracting LLM prompts from experiment YAML files
# SCOPE: Zero-intelligence system that follows mechanical rules without interpretation
# OUTPUT: Structured prompt sequences ready for LLM API orchestration
#
# Date: 2025-07-02
# Version: 1.0
# Status: Complete specification for deterministic implementation

# ================================================================
# SYSTEM OVERVIEW
# ================================================================

## Core Function
Parse experiment YAML files and extract executable LLM prompts using purely mechanical rules.

## Design Constraints
- **Zero Intelligence**: No domain knowledge or interpretive capability
- **Deterministic**: Same input always produces identical output
- **Rule-Based**: Follows explicit parsing rules without decision-making
- **Validation**: Detects malformed experiments and reports specific errors

## Input/Output Contract
- **Input**: Valid experiment YAML file following coordinate-free experiment schema
- **Output**: Structured prompt execution plan with variable substitution map

# ================================================================
# YAML STRUCTURE PARSING RULES
# ================================================================

## Required Top-Level Elements
The parser MUST find these exact YAML paths or report missing element errors:

```yaml
experiment_name: [string]
framework_integration:
  analysis_protocol:
    [stage_definitions]
```

## Stage Definition Recognition Rules

### Rule 1: Stage Identification
- Search for keys matching pattern: `stage_[number]_[name]` or `stage_[number][suffix]`
- Valid stage patterns:
  - `stage_1_discovery`
  - `stage_2_anchor_assessment` 
  - `stage_3_competitive_analysis`
  - `stage_4_framework_fit`
- Extract stage number from key name for execution ordering

### Rule 2: Prompt Location Rules
For each identified stage, extract prompts using these exact paths:

**Single Prompt Stages:**
```yaml
stage_X_[name]:
  prompt: |
    [prompt_content]
```

**Multi-Prompt Stages:**
```yaml
stage_X_[name]:
  [anchor]_prompt: |
    [prompt_content]
```

**Extraction Algorithm:**
1. Check if `prompt` key exists → single prompt stage
2. Check for keys ending in `_prompt` → multi-prompt stage  
3. If neither found → report malformed stage error

### Rule 3: Contextual Content Assembly
For each prompt, assemble complete content by concatenating in this exact order:

1. **Stage Context** (if exists):
   - Path: `stage_X_[name].contextual_guidance`
   - Include if present, skip if absent

2. **Main Prompt Content**:
   - Path: `stage_X_[name].prompt` OR `stage_X_[name].[anchor]_prompt`
   - Required - report error if missing

3. **Output Format** (if exists):
   - Search for keys matching: `output_format`, `required_output_format`, `output_structure`
   - Include if present, skip if absent

**Assembly Rule:** Concatenate with double line breaks (`\n\n`) between sections.

# ================================================================
# VARIABLE EXTRACTION AND SUBSTITUTION
# ================================================================

## Variable Identification Rules

### Rule 1: Variable Pattern Recognition
- Variables marked with: `{variable_name}`
- Valid variable name pattern: `[a-zA-Z_][a-zA-Z0-9_]*`
- Extract all unique variables from each prompt

### Rule 2: Variable Type Classification

**Text Input Variables:**
- `{speech_text}` → requires external text input
- `{text}` → requires external text input

**Stage Result Variables:**
- `{discovery_results}` → output from stage_1_discovery
- `{populism_results}` → output from populism_prompt in stage_2_anchor_assessment
- `{pluralism_results}` → output from pluralism_prompt in stage_2_anchor_assessment  
- `{framework_results}` → combined output from stage_2 + stage_3
- `{[stage_name]_results}` → output from named stage

**Metadata Variables:**
- `{experiment_name}` → from top-level experiment_name field
- `{timestamp}` → system-generated execution timestamp

### Rule 3: Dependency Chain Construction
For each prompt, build dependency list:

1. Identify all variables in prompt
2. For each variable, determine source:
   - Text input: no dependency
   - Stage result: depends on source stage completion
   - Metadata: no dependency
3. Sort dependencies by stage execution order

# ================================================================
# EXECUTION SEQUENCE GENERATION
# ================================================================

## Stage Ordering Rules

### Rule 1: Numeric Ordering
- Extract stage number from stage key name
- Execute stages in ascending numeric order: 1, 2, 3, 4, etc.

### Rule 2: Multi-Prompt Stage Handling
For stages with multiple prompts (e.g., populism_prompt + pluralism_prompt):
- Execute all prompts within stage in parallel (no defined order)
- Mark stage complete only when ALL prompts complete
- Dependent stages wait for complete stage completion

### Rule 3: Dependency Validation
Before generating execution plan:
1. Check that all variable dependencies can be resolved
2. Verify no circular dependencies exist
3. Report unresolvable dependency errors

## Execution Plan Structure

```json
{
  "experiment_metadata": {
    "experiment_name": "string",
    "total_stages": number,
    "total_prompts": number
  },
  "execution_sequence": [
    {
      "stage_id": "stage_1_discovery",
      "stage_number": 1,
      "execution_order": 1,
      "prompts": [
        {
          "prompt_id": "stage_1_discovery",
          "dependencies": ["speech_text"],
          "variables": ["speech_text"],
          "complete_prompt": "assembled prompt text with variables"
        }
      ]
    },
    {
      "stage_id": "stage_2_anchor_assessment", 
      "stage_number": 2,
      "execution_order": 2,
      "prompts": [
        {
          "prompt_id": "populism_prompt",
          "dependencies": ["speech_text"],
          "variables": ["speech_text"],
          "complete_prompt": "assembled prompt text"
        },
        {
          "prompt_id": "pluralism_prompt", 
          "dependencies": ["speech_text"],
          "variables": ["speech_text"],
          "complete_prompt": "assembled prompt text"
        }
      ]
    }
  ]
}
```

# ================================================================
# PROMPT ASSEMBLY ALGORITHMS
# ================================================================

## Algorithm 1: Single Prompt Assembly

```python
def assemble_single_prompt(stage_data):
    prompt_parts = []
    
    # Add contextual guidance if exists
    if 'contextual_guidance' in stage_data:
        prompt_parts.append(stage_data['contextual_guidance'])
    
    # Add main prompt (required)
    if 'prompt' not in stage_data:
        raise MalformedStageError("Missing required 'prompt' field")
    prompt_parts.append(stage_data['prompt'])
    
    # Add output format if exists
    for format_key in ['output_format', 'required_output_format', 'output_structure']:
        if format_key in stage_data:
            prompt_parts.append(stage_data[format_key])
            break
    
    return "\n\n".join(prompt_parts)
```

## Algorithm 2: Multi-Prompt Assembly

```python
def assemble_multi_prompts(stage_data):
    prompts = {}
    
    # Find all _prompt keys
    prompt_keys = [key for key in stage_data.keys() if key.endswith('_prompt')]
    
    if not prompt_keys:
        raise MalformedStageError("No prompt keys found in multi-prompt stage")
    
    for prompt_key in prompt_keys:
        prompt_parts = []
        
        # Add contextual guidance if exists
        if 'contextual_guidance' in stage_data:
            prompt_parts.append(stage_data['contextual_guidance'])
        
        # Add specific prompt
        prompt_parts.append(stage_data[prompt_key])
        
        # Add output format if exists
        for format_key in ['output_format', 'required_output_format', 'output_structure']:
            if format_key in stage_data:
                prompt_parts.append(stage_data[format_key])
                break
        
        prompts[prompt_key] = "\n\n".join(prompt_parts)
    
    return prompts
```

## Algorithm 3: Variable Extraction

```python
import re

def extract_variables(prompt_text):
    variable_pattern = r'\{([a-zA-Z_][a-zA-Z0-9_]*)\}'
    variables = re.findall(variable_pattern, prompt_text)
    return list(set(variables))  # Remove duplicates

def classify_variable(variable_name):
    if variable_name in ['speech_text', 'text']:
        return 'text_input'
    elif variable_name.endswith('_results'):
        return 'stage_result'
    elif variable_name in ['experiment_name', 'timestamp']:
        return 'metadata'
    else:
        return 'unknown'
```

# ================================================================
# ERROR HANDLING SPECIFICATION
# ================================================================

## Required Error Types

### Structural Errors
- **MissingExperimentName**: No `experiment_name` field found
- **MissingAnalysisProtocol**: No `framework_integration.analysis_protocol` found
- **NoStagesFound**: No valid stage definitions found
- **MalformedStageError**: Stage missing required prompt field

### Variable Errors  
- **UnresolvableDependency**: Variable cannot be resolved to any source
- **CircularDependency**: Variables create circular dependency chain
- **UnknownVariableType**: Variable doesn't match any known pattern

### Validation Errors
- **InvalidStageNumber**: Stage number not extractable from stage name
- **DuplicateStageNumber**: Multiple stages with same number
- **EmptyPrompt**: Prompt field exists but is empty

## Error Reporting Format

```json
{
  "parse_success": false,
  "error_type": "MalformedStageError",
  "error_message": "Stage 'stage_2_anchor_assessment' missing required 'populism_prompt' field",
  "error_location": "framework_integration.analysis_protocol.stage_2_anchor_assessment",
  "suggestions": [
    "Add populism_prompt field with prompt content",
    "Check YAML indentation and structure"
  ]
}
```

# ================================================================
# IMPLEMENTATION REQUIREMENTS
# ================================================================

## Core Functions Required

### 1. YAML Parser Interface
```python
def parse_experiment_yaml(file_path: str) -> ExperimentParseResult:
    """
    Parse experiment YAML file and extract prompt execution plan.
    
    Returns:
        ExperimentParseResult with success/error and execution plan
    """
```

### 2. Prompt Assembly Interface  
```python
def assemble_prompts(parsed_experiment: dict) -> ExecutionPlan:
    """
    Assemble complete prompts with dependency chains.
    
    Returns:
        ExecutionPlan ready for orchestration system
    """
```

### 3. Validation Interface
```python
def validate_experiment_structure(experiment_data: dict) -> ValidationResult:
    """
    Validate experiment structure and variable dependencies.
    
    Returns:
        ValidationResult with pass/fail and specific errors
    """
```

## Configuration Requirements

### File Path Conventions
- Input: `[experiment_name].yaml`
- Output: `[experiment_name]_execution_plan.json`
- Errors: `[experiment_name]_parse_errors.json`

### Variable Substitution Markers
- Input variables: `{variable_name}`
- Preserved variables: Variables not marked for substitution pass through unchanged
- Invalid variables: Report as UnknownVariableType error

# ================================================================
# TESTING SPECIFICATION
# ================================================================

## Required Test Cases

### Valid Input Tests
1. **Single Stage Experiment**: Stage with single prompt, no variables
2. **Multi-Stage Sequential**: Stages with dependencies (1→2→3→4)
3. **Multi-Prompt Stage**: Stage with multiple parallel prompts
4. **Complex Dependencies**: Multiple variable types and cross-stage dependencies

### Error Condition Tests
1. **Missing Fields**: Each required field missing individually
2. **Malformed YAML**: Invalid YAML syntax and structure errors
3. **Variable Errors**: Unresolvable and circular dependencies
4. **Empty Content**: Empty prompts and missing content

### Edge Case Tests
1. **Large Experiments**: Many stages and complex dependency chains
2. **Unicode Content**: Non-ASCII characters in prompts and variables
3. **Special Characters**: Variables and prompts with edge-case characters

## Test Data Requirements
- Valid experiment YAML files for each test case
- Expected output JSON files for validation
- Error case YAML files with known error conditions

# ================================================================
# INTEGRATION SPECIFICATION
# ================================================================

## Orchestration System Interface

### Input Contract
The parser outputs JSON execution plans that orchestration systems can consume:

```json
{
  "experiment_name": "coordinate_free_populism_validation",
  "execution_sequence": [...],
  "variable_substitution_map": {
    "speech_text": "external_input_required",
    "discovery_results": "stage_1_output",
    "populism_results": "stage_2_populism_output"
  }
}
```

### Output Contract  
Orchestration systems provide variable values:

```json
{
  "speech_text": "actual speech content...",
  "discovery_results": "output from stage 1...",
  "populism_results": "output from populism analysis..."
}
```

### API Contract
```python
# Orchestration system calls parser
execution_plan = parse_experiment_yaml("experiment.yaml")

# Orchestration system executes prompts
for stage in execution_plan.stages:
    for prompt in stage.prompts:
        # Substitute variables
        final_prompt = substitute_variables(prompt.complete_prompt, variable_values)
        
        # Call LLM API
        result = llm_api.call(final_prompt)
        
        # Store result for dependent stages
        variable_values[prompt.result_variable] = result
```

# ================================================================
# VERSION CONTROL AND COMPATIBILITY
# ================================================================

## Experiment Schema Versioning
- Support schema version detection from YAML files
- Maintain backward compatibility for previous versions
- Clear upgrade paths for experiment specifications

## Parser Version Management
- Parser version must be logged in execution plans
- Reproducible parsing across different parser versions
- Clear compatibility matrix for schema/parser combinations

---

**This specification enables completely automated prompt extraction from experiment definitions without requiring domain expertise or interpretive intelligence. Any competent developer can implement this system and produce identical results given the same experiment YAML input.** 