# Deprecated Scripts

This directory contains scripts that are no longer part of the active Discernus pipeline but are preserved for reference and potential future use.

## Deprecated Scripts

### `multi_run_synthesis_experiment.py`
**Original Purpose**: Multi-run synthesis experiment execution with ensemble capabilities  
**Deprecation Date**: 2025-01-19  
**Reason for Deprecation**: 
- Not integrated into current v10.0 pipeline architecture
- Superseded by enhanced single-agent synthesis approach
- Complex orchestration patterns replaced by THIN architecture

**Original Features**:
- Multiple synthesis run execution
- Ensemble result aggregation  
- Prompt engineering harness functionality
- Model comparison capabilities
- Configurable experiment parameters

**File Size**: 9.7KB, 269 lines

## Deprecation Policy

Scripts in this directory are preserved because they:

1. **Contain Valuable Patterns**: May have useful code patterns or approaches
2. **Reference Implementation**: Serve as examples of previous architectural approaches  
3. **Research Continuity**: Maintain connection to prior research methodologies
4. **Potential Revival**: Could be adapted for future use cases

## ⚠️ Important Notes

- **DO NOT USE IN PRODUCTION**: These scripts are not maintained and may have outdated dependencies
- **NO SUPPORT**: Deprecated scripts are not supported or updated
- **COMPATIBILITY ISSUES**: May not work with current system architecture
- **REFERENCE ONLY**: Use only for understanding previous approaches or extracting useful patterns

## Migration Path

If you need functionality from deprecated scripts:

1. **Review Current Pipeline**: Check if equivalent functionality exists in v10.0 system
2. **Extract Patterns**: Identify useful code patterns that could be adapted
3. **Modernize Approach**: Implement using current THIN architecture principles
4. **Test Thoroughly**: Ensure compatibility with current system

## Alternative Solutions

Instead of using deprecated scripts, consider:

- **Current CLI**: Use `discernus run` for experiment execution
- **Enhanced Synthesis**: Leverage the v10.0 enhanced synthesis agent
- **Prompt Testing**: Use `tests/prompt_engineering_harness.py` for prompt development
- **Multi-Model Support**: Use current model selection and ensemble capabilities

## Historical Context

### Multi-Run Synthesis Evolution

The `multi_run_synthesis_experiment.py` script represented an earlier approach to:
- **Ensemble Methods**: Multiple model runs for consensus
- **Prompt Engineering**: Iterative prompt development and testing
- **Result Aggregation**: Combining outputs from multiple synthesis attempts

This approach was superseded by:
- **Enhanced Single-Agent Synthesis**: More sophisticated single-pass synthesis
- **THIN Architecture**: Simplified, more maintainable approach
- **Framework-Agnostic Design**: Better generalization across research frameworks

## Recovery Instructions

If you need to recover functionality from deprecated scripts:

1. **Analyze Requirements**: Determine what specific functionality is needed
2. **Check Current Capabilities**: Verify if current system provides equivalent features
3. **Consult Documentation**: Review current architecture documentation
4. **Implement Modern Version**: Create new implementation using current patterns
5. **Test Integration**: Ensure compatibility with current pipeline

## Maintenance Status

- **No Updates**: Deprecated scripts receive no updates or bug fixes
- **No Testing**: Not included in current test suites
- **No Documentation**: Documentation may be outdated or incomplete
- **Preservation Only**: Maintained solely for historical reference