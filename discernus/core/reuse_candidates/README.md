# Reuse Candidates

This directory contains core components that are potentially valuable but require restoration and integration effort to be useful in the current pipeline.

## Reuse Candidates

### Mathematical & Statistical Tools
- **math_toolkit.py** - Comprehensive statistical toolkit (75KB, 1613 lines)
  - **Value**: Tested, reliable mathematical functions
  - **Current Status**: Used by deprecated agents but not current pipeline
  - **Restoration Effort**: Medium - needs integration with current pipeline

- **statistical_formatter.py** - Statistical result formatting (14KB, 303 lines)
  - **Value**: Professional statistical output formatting
  - **Current Status**: Used by math_toolkit but not current pipeline
  - **Restoration Effort**: Low - simple integration

### Enhanced Synthesis
- **unified_synthesis_agent.py** - Unified synthesis approach (12KB, 288 lines)
  - **Value**: Could enhance current synthesis capabilities
  - **Current Status**: Imported by experiment_orchestrator but not actively used
  - **Restoration Effort**: Medium - needs testing and integration

- **enhanced_synthesis_prompt.yaml** - Enhanced synthesis prompts (8.7KB, 200 lines)
  - **Value**: Could improve synthesis quality
  - **Current Status**: Not actively used in current pipeline
  - **Restoration Effort**: Low - simple integration

### Notebook Generation
- **componentized_notebook_generation.py** - Componentized approach (7.9KB, 179 lines)
  - **Value**: Token-limit compliant notebook generation
  - **Current Status**: Used by notebook_generation_orchestrator but not fully utilized
  - **Restoration Effort**: Medium - needs full integration

- **universal_notebook_template.py** - Universal template system (6.7KB, 170 lines)
  - **Value**: Standardized notebook templates
  - **Current Status**: Used by notebook generation components
  - **Restoration Effort**: Low - already partially integrated

### Research Tools
- **discernuslibrarian.py** - Literature research system (71KB, 1515 lines)
  - **Value**: Academic literature discovery and validation
  - **Current Status**: Standalone research tool, not integrated into pipeline
  - **Restoration Effort**: High - major integration effort needed

## Integration Priority

### High Priority (Low Effort, High Value)
1. **statistical_formatter.py** - Simple integration, immediate value
2. **enhanced_synthesis_prompt.yaml** - Simple integration, synthesis improvement

### Medium Priority (Medium Effort, Good Value)
3. **math_toolkit.py** - Statistical function library integration
4. **unified_synthesis_agent.py** - Synthesis enhancement
5. **componentized_notebook_generation.py** - Notebook generation improvement

### Lower Priority (High Effort, High Value)
6. **discernuslibrarian.py** - Major research capability addition

## Restoration Process

1. **Assessment**: Review component for current compatibility
2. **Testing**: Create tests to verify functionality
3. **Integration**: Modify imports and dependencies
4. **Validation**: Ensure no regression in current pipeline
5. **Documentation**: Update usage documentation

## Current Pipeline Compatibility

These components are **NOT** currently integrated and require work before use. They represent potential enhancements rather than current capabilities.
