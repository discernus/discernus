# Coordinate-Free Experiment Definition Schema Specification v1.0
# YAML Schema for Coordinate-Free Discourse Analysis Experiments
#
# PURPOSE: Define exact YAML structure for experiments compatible with automated prompt extraction
# SCOPE: Complete schema specification enabling experiment authors to create parser-compatible definitions
# COMPATIBILITY: Designed to pair exactly with Experiment Prompt Extraction System Specification v1.0
#
# Date: 2025-07-02
# Version: 1.0
# Status: Complete schema for deterministic parsing

# ================================================================
# SCHEMA OVERVIEW
# ================================================================

## Purpose
Define the exact YAML structure that experiment authors must follow to ensure compatibility with the automated prompt extraction system.

## Design Principles
- **Explicit Structure**: Every required and optional field clearly specified
- **Parser Compatibility**: Exact one-to-one mapping with prompt extraction system expectations
- **Validation Ready**: Schema enables automated validation of experiment definitions
- **Extensible**: Forward-compatible design supports future enhancements

## Compliance Requirement
Experiment YAML files MUST conform to this schema to be processable by the automated prompt extraction system.

# ================================================================
# TOP-LEVEL SCHEMA STRUCTURE
# ================================================================

## Required Root Elements

```yaml
# REQUIRED: Experiment identification
experiment_name: string                    # Must be valid filename (no spaces/special chars)
version: string                           # Semantic version (e.g., "v1.0")
display_name: string                      # Human-readable experiment name

# REQUIRED: Experiment description  
description: |
  Multi-line string describing experiment purpose, methodology, and scope.
  Must be present but can be empty string.

# REQUIRED: Framework integration section
framework_integration:
  framework_source: string               # Reference to framework specification
  analysis_protocol:                     # REQUIRED: Contains all stage definitions
    [stage_definitions]                  # Must contain at least one valid stage

# OPTIONAL: Additional metadata
research_questions: [optional]           # Research questions and hypotheses
experimental_design: [optional]         # Design methodology and approach
measurement_framework: [optional]       # Measurement and analytics approach
```

## Schema Validation Rules

### String Field Requirements
- `experiment_name`: Must match pattern `^[a-zA-Z0-9_-]+$` (alphanumeric, underscore, hyphen only)
- `version`: Must match semantic version pattern `^v?\d+\.\d+(\.\d+)?$`
- `display_name`: Any non-empty string, max 200 characters

### Required vs Optional Fields
- **REQUIRED**: `experiment_name`, `version`, `display_name`, `description`, `framework_integration`
- **OPTIONAL**: All other top-level fields (research_questions, experimental_design, etc.)

# ================================================================
# FRAMEWORK INTEGRATION SCHEMA
# ================================================================

## Required Structure

```yaml
framework_integration:
  # REQUIRED: Framework reference
  framework_source: string               # Framework specification filename or identifier
  
  # REQUIRED: Analysis protocol containing stage definitions
  analysis_protocol:
    # REQUIRED: LLM configuration
    llm_model: string                     # Supported models: "GPT-4", "Claude-3.5 Sonnet", etc.
    prompt_strategy: string              # Analysis strategy description
    
    # REQUIRED: Stage definitions (at least one stage required)
    stage_1_[name]: [stage_definition]   # First stage (required)
    stage_2_[name]: [stage_definition]   # Additional stages (optional)
    stage_N_[name]: [stage_definition]   # Up to N stages supported
```

## Stage Naming Convention Rules

### Pattern Requirements
- Stage keys MUST match pattern: `stage_[number]_[name]`
- `[number]`: Integer starting from 1, sequential (1, 2, 3, 4, ...)
- `[name]`: Alphanumeric identifier (a-z, A-Z, 0-9, underscore only)
- Examples: `stage_1_discovery`, `stage_2_anchor_assessment`, `stage_3_competitive_analysis`

### Validation Rules
- Stage numbers must be sequential (no gaps: 1→2→3, not 1→3→4)
- Stage names must be unique within experiment
- Maximum 10 stages supported (stage_1 through stage_10)

# ================================================================
# STAGE DEFINITION SCHEMA
# ================================================================

## Single Prompt Stage Structure

```yaml
stage_X_[name]:
  # OPTIONAL: Stage description and context
  description: string                     # Human-readable stage description
  contextual_guidance: |                  # Optional context for LLM
    Multi-line string providing context for analysis.
    Automatically included in prompt assembly.
  
  # REQUIRED: Main prompt content
  prompt: |                              # Required main prompt text
    Complete prompt content including:
    - Role definition (recommended)
    - Task instructions
    - Variable placeholders: {variable_name}
    - Output format requirements
  
  # OPTIONAL: Output formatting
  output_format: |                       # Optional structured output format
    Specific output format requirements.
    Automatically appended to prompt.
  
  # OPTIONAL: Validation criteria
  output_validation: [string_array]      # Optional validation criteria list
```

## Multi-Prompt Stage Structure

```yaml
stage_X_[name]:
  # OPTIONAL: Stage description and context
  description: string                     # Human-readable stage description
  contextual_guidance: |                  # Optional shared context for all prompts
    Multi-line string providing context.
    Automatically included in ALL prompt assemblies.
  
  # REQUIRED: Multiple prompt definitions (at least one ending in '_prompt')
  [anchor1]_prompt: |                    # First prompt (e.g., populism_prompt)
    Complete prompt content for first anchor analysis.
    
  [anchor2]_prompt: |                    # Second prompt (e.g., pluralism_prompt)  
    Complete prompt content for second anchor analysis.
    
  [anchorN]_prompt: |                    # Additional prompts as needed
    Complete prompt content for additional analyses.
  
  # OPTIONAL: Shared output formatting
  output_format: |                       # Optional format applied to all prompts
    Shared output format requirements.
```

## Variable Placeholder Rules

### Supported Variable Patterns
Variables in prompts must follow exact pattern: `{variable_name}`

### Variable Type Classification

**Text Input Variables:**
- `{speech_text}` - Primary text input for analysis
- `{text}` - Alternative text input identifier
- `{document}` - Document input identifier
- `{corpus_item}` - Corpus item identifier

**Stage Result Variables:**
- `{discovery_results}` - Output from stage_1_discovery
- `{[stage_name]_results}` - Output from named stage
- `{[anchor]_results}` - Output from specific anchor prompt (e.g., {populism_results})
- `{framework_results}` - Combined results from framework analysis stages

**Metadata Variables:**
- `{experiment_name}` - Experiment name from top-level field
- `{timestamp}` - System-generated execution timestamp
- `{stage_number}` - Current stage number
- `{total_stages}` - Total number of stages in experiment

### Variable Naming Rules
- Variable names must match pattern: `^[a-zA-Z_][a-zA-Z0-9_]*$`
- Variable names are case-sensitive
- Reserved variables cannot be redefined
- Unknown variables will cause parsing errors

# ================================================================
# STAGE TYPE SPECIFICATIONS
# ================================================================

## Discovery Stage (Typically stage_1_discovery)

```yaml
stage_1_discovery:
  description: "Open-ended analysis without framework bias"
  
  contextual_guidance: |
    Optional context about analytical approach and domain background.
    
  prompt: |
    You are an expert [domain] analyst...
    
    Analyze this [domain] text without using predefined categories.
    
    TEXT: {speech_text}
    
    Questions:
    1. What are the main themes?
    2. How does this text approach [key_concept]?
    3. What values are emphasized?
    
    REQUIRED OUTPUT FORMAT:
    - Number responses 1-N
    - Support with [EVIDENCE: "quote"] tags
    
  output_validation:
    - "Themes are specific and evidence-based"
    - "Analysis approach clearly characterized"
```

## Anchor Assessment Stage (Typically stage_2_[name])

```yaml
stage_2_anchor_assessment:
  description: "Independent evaluation of conceptual anchors"
  
  contextual_guidance: |
    Context about anchor definitions and assessment criteria.
    
  [anchor1]_prompt: |
    You are a [domain] expert specializing in [anchor1] theory...
    
    Based on this text, assess [anchor1] themes:
    
    TEXT: {speech_text}
    
    [Anchor1] Assessment:
    1. PRESENCE: Are [anchor1] themes present? (Yes/No/Unclear)
    2. SALIENCE: How central? (High/Medium/Low/None)
    3. EVIDENCE: What language supports assessment?
    4. INTENSITY: How strongly emphasized? (Strong/Moderate/Weak/None)
    5. CONSISTENCY: Consistently applied? (Consistent/Mixed/Inconsistent)
    6. CONFIDENCE: Assessment confidence? (High/Medium/Low)
    
  [anchor2]_prompt: |
    [Similar structure for second anchor]
    
  output_format: |
    REQUIRED OUTPUT FORMAT:
    1. [PRESENCE]: Yes/No/Unclear
    2. [SALIENCE]: High/Medium/Low/None with justification
    [etc.]
```

## Competitive Analysis Stage (Typically stage_3_competitive_analysis)

```yaml
stage_3_competitive_analysis:
  description: "Analysis of anchor relationships and competitive dynamics"
  
  prompt: |
    You are a strategic communication analyst...
    
    Analyze how [anchor1] and [anchor2] themes interact:
    
    [ANCHOR1] ASSESSMENT: {anchor1_results}
    [ANCHOR2] ASSESSMENT: {anchor2_results}
    
    Competitive Analysis:
    1. OPPOSITION: Do themes directly compete?
    2. COEXISTENCE: Areas where themes coexist?
    3. DOMINANCE: Which theme dominates and where?
    4. COHERENCY PATTERN: Which pattern describes this text?
       - Focused [anchor1]: High [anchor1], low [anchor2]
       - Focused [anchor2]: High [anchor2], low [anchor1]
       - [Domain] tension: Moderate both with tension
       - Strategic ambiguity: Mixed signals for different audiences
       - Incoherent mixture: Contradictory themes
    5. STRATEGIC ASSESSMENT: What rhetorical strategy?
    
  output_format: |
    1. [OPPOSITION]: Areas of tension with examples
    2. [COEXISTENCE]: Areas of compatibility
    3. [DOMINANCE]: Dominant theme and contexts
    4. [COHERENCY PATTERN]: Select pattern with justification
    5. [STRATEGIC ASSESSMENT]: Primary strategy with reasoning
```

## Framework Fit Assessment Stage (Typically stage_4_framework_fit)

```yaml
stage_4_framework_fit:
  description: "Assessment of framework appropriateness and limitations"
  
  prompt: |
    You are a methodology expert in discourse analysis frameworks...
    
    Assess how well the [framework] captures this text:
    
    DISCOVERY RESULTS: {discovery_results}
    FRAMEWORK RESULTS: {framework_results}
    
    Framework Fit Assessment:
    1. COVERAGE: Percentage of important content captured? (0-100%)
    2. GAPS: Important themes not captured?
    3. RELEVANCE: Framework relevance? (Excellent/Good/Fair/Poor)
    4. ALIGNMENT: Discovery themes align with framework? (Strong/Moderate/Weak/No)
    5. EXPLANATORY POWER: Framework explains patterns? (High/Medium/Low)
    6. CONFIDENCE: Confidence in applicability? (High/Medium/Low)
    
    If coverage <70% or relevance Fair/Poor:
    7. RECOMMENDATIONS: Alternative frameworks or modifications
    
  output_format: |
    1. [COVERAGE]: X% with explanation if <70%
    2. [GAPS]: Uncaptured themes with significance
    3. [RELEVANCE]: Rating with justification
    4. [ALIGNMENT]: Level with explanation
    5. [EXPLANATORY POWER]: Level with reasoning
    6. [CONFIDENCE]: Level with rationale
    7. [RECOMMENDATIONS]: If applicable
```

# ================================================================
# OPTIONAL SCHEMA EXTENSIONS
# ================================================================

## Research Questions Section (Optional)

```yaml
research_questions:
  primary: string                         # Primary research question
  secondary: [string_array]               # List of secondary questions
  
falsifiable_hypotheses:
  [hypothesis_id]:                        # Unique hypothesis identifier
    hypothesis: string                    # Hypothesis statement
    operationalization: string           # How hypothesis will be tested
    measurement: string                   # Measurement approach
    falsification_criteria: string       # What would prove hypothesis wrong
```

## Experimental Design Section (Optional)

```yaml
experimental_design:
  design_type: string                     # Type of experimental design
  corpus_selection:                       # Corpus selection criteria
    primary_corpus: string
    selection_criteria: [string_array]
    corpus_size: string
  comparative_framework:                  # Comparison frameworks
    coordinate_free: string
    coordinate_based: string
  analysis_workflow:                      # Analysis workflow steps
    [step_id]: string
```

## Measurement Framework Section (Optional)

```yaml
measurement_framework:
  quantitative_elements:                  # Quantitative measurement approaches
    [metric_id]:
      metric: string
      calculation: string
      comparison: string
  qualitative_elements:                   # Qualitative analysis approaches
    [element_id]:
      metric: string
      categories: [string_array]
      analysis: string
```

# ================================================================
# VALIDATION SCHEMA
# ================================================================

## Required Field Validation

### Top-Level Required Fields
```yaml
# These fields MUST be present and non-empty
experiment_name: [required, string, pattern: ^[a-zA-Z0-9_-]+$]
version: [required, string, pattern: ^v?\d+\.\d+(\.\d+)?$]
display_name: [required, string, max_length: 200]
description: [required, string]
framework_integration: [required, object]
```

### Framework Integration Required Fields
```yaml
framework_integration:
  framework_source: [required, string]
  analysis_protocol: [required, object]
    llm_model: [required, string]
    prompt_strategy: [required, string]
    [at_least_one_stage]: [required]
```

### Stage Definition Required Fields
```yaml
stage_X_[name]:
  # For single prompt stages:
  prompt: [required, string, min_length: 10]
  
  # For multi-prompt stages:
  [at_least_one_prompt_ending_in_prompt]: [required, string, min_length: 10]
```

## Optional Field Validation

### Optional Fields with Validation Rules
```yaml
contextual_guidance: [optional, string]
output_format: [optional, string]
output_validation: [optional, array_of_strings]
description: [optional, string]
```

## Cross-Field Validation Rules

### Stage Number Validation
- Stage numbers must be sequential starting from 1
- No duplicate stage numbers allowed
- Maximum 10 stages supported

### Variable Reference Validation
- All variables in prompts must be resolvable
- No circular dependencies allowed
- Stage result variables must reference existing stages

### Prompt Content Validation
- Prompts must be non-empty strings
- Variable placeholders must follow {variable_name} pattern
- Role definitions recommended but not required

# ================================================================
# SCHEMA COMPLIANCE EXAMPLES
# ================================================================

## Minimal Valid Experiment

```yaml
experiment_name: minimal_experiment
version: v1.0
display_name: Minimal Valid Experiment
description: Basic experiment with single stage

framework_integration:
  framework_source: basic_framework.yaml
  analysis_protocol:
    llm_model: GPT-4
    prompt_strategy: Single stage analysis
    
    stage_1_discovery:
      prompt: |
        You are an expert analyst.
        
        Analyze this text: {speech_text}
        
        What are the main themes?
```

## Complex Valid Experiment

```yaml
experiment_name: complex_populism_analysis
version: v1.2
display_name: Complex Populism Analysis Validation Study
description: |
  Multi-stage coordinate-free populism analysis with framework fit assessment.

framework_integration:
  framework_source: populism_pluralism_coordinate_free_v1.0.yaml
  analysis_protocol:
    llm_model: Claude-3.5 Sonnet
    prompt_strategy: Sequential stage processing with validation checks
    
    stage_1_discovery:
      contextual_guidance: |
        You are analyzing Brazilian political discourse from 2018 election.
      prompt: |
        You are an expert discourse analyst...
        Analyze this text: {speech_text}
        Questions: [1-5]
      output_format: |
        Number responses 1-5 with evidence tags.
    
    stage_2_anchor_assessment:
      populism_prompt: |
        You are a populism expert...
        Assess populist themes in: {speech_text}
        [6-point assessment structure]
      pluralism_prompt: |
        You are a pluralism expert...
        Assess pluralist themes in: {speech_text}
        [6-point assessment structure]
    
    stage_3_competitive_analysis:
      prompt: |
        You are a strategic communication analyst...
        Analyze interaction: {populism_results} + {pluralism_results}
        [5-point competitive analysis]
    
    stage_4_framework_fit:
      prompt: |
        You are a methodology expert...
        Assess framework fit: {discovery_results} + {framework_results}
        [7-point fit assessment with recommendations]

research_questions:
  primary: Does coordinate-free analysis provide superior capabilities?
  secondary: 
    - Does discovery-first approach reduce bias?
    - Does framework fit assessment enable adaptive selection?
```

# ================================================================
# ERROR PREVENTION GUIDELINES
# ================================================================

## Common Schema Violations to Avoid

### Stage Definition Errors
- ❌ Missing stage numbers: `discovery:` instead of `stage_1_discovery:`
- ❌ Non-sequential stages: `stage_1`, `stage_3` (missing stage_2)
- ❌ Invalid stage names: `stage_1_discovery!` (special characters)
- ❌ Missing prompt content: Empty prompt fields

### Variable Errors
- ❌ Invalid variable syntax: `$variable` instead of `{variable}`
- ❌ Unresolvable variables: `{unknown_results}` with no source stage
- ❌ Circular dependencies: Stage A depends on Stage B which depends on Stage A

### Structure Errors
- ❌ Missing required fields: No `experiment_name` or `framework_integration`
- ❌ Invalid YAML syntax: Incorrect indentation or malformed structure
- ❌ Empty required sections: Present but empty `analysis_protocol`

## Schema Validation Tools

### Recommended Validation Approach
1. **YAML Syntax Validation**: Ensure valid YAML structure
2. **Schema Validation**: Validate against this specification
3. **Cross-Reference Validation**: Check variable dependencies and stage references
4. **Content Validation**: Ensure non-empty required content

### Implementation Recommendations
- Use JSON Schema or similar for automated validation
- Implement custom validation for cross-field dependencies
- Provide specific error messages with suggested corrections
- Include example corrections for common validation failures

---

**This schema specification provides the exact contract that experiment authors must follow to ensure compatibility with the automated prompt extraction system. Together with the Prompt Extraction System Specification, these form a complete API contract for deterministic experiment processing.** 