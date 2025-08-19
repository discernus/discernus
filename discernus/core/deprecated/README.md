# Deprecated Core Components

This directory contains core components that are no longer used in the current pipeline.

## Deprecated Components

### Utilities
- **thin_output_extraction.py** - Output extraction utilities (used by deprecated agents)
- **parsing_utils.py** - Parsing utilities (used by deprecated agents)  
- **thin_validation.py** - THIN validation utilities (self-referential, unused)

### Infrastructure
- **infrastructure_telemetry.py** - Complex telemetry system (over-engineered, unused)
- **llm_code_sanitizer.py** - Code sanitization (only used in tests)
- **notebook_executor.py** - Notebook execution (only used by notebook_generation_orchestrator)
- **report_generator.py** - Report generation (used by deprecated agents)
- **artifact_browser.py** - Artifact browsing (only used in tests)
- **evidence_confidence_calibrator.py** - Evidence calibration (used by deprecated agents)

### Templates & Specifications
- **notebook_templates/** - Jinja2 templates (not used in current pipeline)
- **v8_specifications.py** - V8 specification handling (only used by notebook_generation_orchestrator)

## Status

❌ **NOT INTEGRATED** - These components are not part of the current active pipeline and should not be used in production.

## Note

These components are preserved for reference but should not be used. They may contain outdated patterns or dependencies that conflict with current architecture.
