# Developer Tools

This directory contains specialized utilities for Discernus development, testing, and troubleshooting.

## Tools

### `verify_model_health.py`
**Purpose**: Model health verification utility for developers  
**Functionality**: 
- Performs health checks on all models in the Model Registry
- Tests API connectivity and configuration
- Provides detailed status reporting with Rich console output
- Handles Vertex AI safety settings and provider-specific configurations

**Usage**: `python3 -m discernus.dev_tools.verify_model_health`

**Features**:
- Concurrent model testing for efficiency
- Provider-specific error handling (Vertex AI, etc.)
- Rich console output with tables and color coding
- Low-cost API calls for testing
- Comprehensive error reporting

**Dependencies**:
- `asyncio` - Async execution
- `litellm` - LLM API abstraction
- `rich` - Console formatting
- `yaml` - Configuration parsing
- Model registry from `discernus/gateway/models.yaml`

## Integration Status

❌ **NOT INTEGRATED** - This tool is currently standalone and not integrated into:
- Main CLI commands
- Makefile targets
- Automated workflows
- Current pipeline

## Relationship to Current System

**Similar Functionality Exists**:
- `discernus/gateway/llm_gateway.py` has built-in `check_model_health()` methods
- `discernus/core/provenance_visualizer.py` has health check visualization capabilities
- Main CLI has provenance health checking features

**Key Differences**:
- **Dev Tool**: Standalone utility for comprehensive model registry testing
- **Built-in**: Integrated health checks within the gateway system
- **Scope**: Dev tool tests ALL models, built-in checks individual models

## Assessment

### **Value**: 🟡 **MEDIUM**
- **Pros**: Comprehensive model testing, developer-friendly output, standalone utility
- **Cons**: Duplicates functionality available in the gateway system

### **Maintenance Status**: 🟢 **WELL-MAINTAINED**
- Clean, well-documented code
- Proper error handling and async implementation
- Rich console output for developer experience

## Current Usage Pattern

The tool appears to be designed for:
1. **Pre-flight checks** before running experiments
2. **Troubleshooting** API key and configuration issues
3. **Development** and testing of model configurations
4. **Documentation** of model availability and status

## Future Considerations

This tool represents a decision point for the Discernus architecture:

1. **Integration Option**: Move functionality into main CLI as `discernus health` command
2. **Organization Option**: Move to `scripts/developer_tools/` for better discoverability
3. **Enhancement Option**: Integrate comprehensive testing into gateway health checks
4. **Deprecation Option**: Remove standalone tool if built-in functionality is sufficient

## Development Workflow

**Current Use Cases**:
- Verify all models are accessible before running experiments
- Debug API configuration issues
- Test new model additions to the registry
- Validate provider settings and API keys

**Integration Opportunities**:
- Pre-experiment validation pipeline
- Automated health monitoring
- CI/CD pipeline integration
- Developer onboarding and setup verification

## Technical Implementation

**Architecture**: Async-first design with concurrent model testing
**Error Handling**: Comprehensive exception capture and reporting
**Output**: Rich console formatting with tables and color coding
**Configuration**: Reads from centralized model registry
**Safety**: Low-cost API calls with provider-specific optimizations

## Maintenance Notes

- **Last Updated**: 2025-01-19
- **Code Quality**: High - follows project coding standards
- **Dependencies**: Minimal external dependencies
- **Testing**: Manual testing only - no automated test coverage
- **Documentation**: Self-documenting with clear usage examples
