# Enhanced Analysis Agent - Show Your Work Architecture

## Current Active Components

This directory contains the **Show Your Work Architecture** implementation for the Enhanced Analysis Agent, which uses structured output via multi-tool calling instead of text parsing.

### Primary Implementation
- **`agent_multi_tool.py`** - Main multi-tool agent implementation with 3-tool calling approach
- **`prompt_multi_tool.txt`** - Multi-tool prompt template with explicit step-by-step instructions

### Alternative Implementations
- **`agent_tool_calling.py`** - Single-tool calling implementation (fallback/alternative)
- **`prompt_tool_calling.txt`** - Single-tool prompt template
- **`prompt_tool_calling_simple.txt`** - Simplified single-tool prompt
- **`prompt_tool_calling_ultra_simple.txt`** - Ultra-simple single-tool prompt

## Architecture Principles

### Multi-Tool Calling Approach
The primary implementation uses **3 focused tools** that work together:

1. **`record_analysis_scores`** - Dimensional scores with confidence and salience
2. **`record_evidence_quotes`** - Evidence quotes and reasoning for each dimension  
3. **`record_computational_work`** - Derived metrics calculations and code execution

### Key Features
- **Structured Output**: No text parsing - uses platform-guaranteed structured responses
- **Explicit Instructions**: Step-by-step prompting that forces Gemini to call all 3 tools
- **Full PDAF Support**: Handles all 9 PDAF dimensions with proper schema
- **Large Document Processing**: Successfully processes 70k+ character documents
- **Complex Framework Support**: Handles 50k+ character framework specifications

## Deprecated Components

The `archive_deprecated/` directory contains files from the old THIN v2.0 architecture:
- Old orchestrator-based components
- Text parsing implementations
- Legacy prompt templates
- Deprecated caching and processing components

These are preserved for reference but are no longer used in the current architecture.

## Usage

```python
from discernus.agents.EnhancedAnalysisAgent.agent_multi_tool import EnhancedAnalysisAgentMultiTool

# Initialize the multi-tool agent
agent = EnhancedAnalysisAgentMultiTool(security, audit, storage, llm_gateway, model='vertex_ai/gemini-2.5-pro')

# Analyze document with framework
result = agent.analyze_document(document_content, framework_content, document_id)
```

## Status

✅ **Fully Operational** - Successfully tested with:
- Full Trump speech (74,665 characters)
- Complete PDAF framework (53,643 characters)  
- All 9 PDAF dimensions properly scored
- All 3 tools called reliably
- Complex derived metrics calculations
