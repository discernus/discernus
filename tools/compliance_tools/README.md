# Compliance Tools

This directory contains tools for checking and auditing THIN architecture compliance across the Discernus codebase.

## Tools

### `thin_compliance_audit.py`
**Purpose**: Comprehensive THIN architecture compliance auditing  
**Usage**: `python3 scripts/compliance_tools/thin_compliance_audit.py`  
**Features**:
- Externalized YAML prompt validation
- Detection of inline prompt patterns
- Parsing logic analysis
- Agent architecture pattern checking
- Redundant/obsolete agent identification
- Severity-based violation reporting

**Compliance Checks**:
- ❌ **Inline Prompts**: Detects f-strings, triple-quoted prompts with variables
- ❌ **Excessive Parsing**: Identifies JSON parsing, regex usage, complex string manipulation
- ❌ **Missing YAML**: Flags agents without externalized prompt.yaml files
- ❌ **Architecture Violations**: Complex logic that should be delegated to LLMs

### `thin_compliance_check.py`
**Purpose**: Detailed compliance checking with specific rule validation  
**Usage**: `python3 scripts/compliance_tools/thin_compliance_check.py`  
**Features**:
- Rule-based compliance validation
- Detailed violation reporting
- Integration with development workflows
- Automated compliance scoring

### `install_git_hooks.sh`
**Purpose**: Install Git pre-commit hooks for THIN compliance  
**Usage**: `./scripts/compliance_tools/install_git_hooks.sh`  
**Features**:
- Pre-commit THIN architecture validation
- Prevents non-compliant code from being committed
- Lightweight checks on staged files only
- Automatic hook installation and configuration

## THIN Architecture Principles

The tools in this directory enforce adherence to THIN (Thoughtful, Human-centric, Intelligent, Natural) architecture:

1. **Externalized Prompts**: All LLM prompts must be in YAML files
2. **Minimal Parsing**: Avoid complex string manipulation and parsing logic
3. **LLM Intelligence**: Delegate complex logic to LLMs rather than code
4. **Clean Architecture**: Simple, maintainable agent patterns

## Integration Status

❌ **NOT INTEGRATED** - These tools are currently standalone and not integrated into the main Discernus pipeline. They are provided for:
- Development workflow enhancement
- Code quality maintenance
- Architecture compliance validation
- Manual auditing processes

## Use Cases

1. **Development**: Pre-commit hooks prevent THIN violations
2. **Code Review**: Audit tools help identify compliance issues
3. **Refactoring**: Compliance reports guide architecture improvements
4. **Quality Assurance**: Regular compliance checks maintain code quality

## Output Examples

```
🔍 THIN Architecture Compliance Audit
=====================================

✅ COMPLIANT AGENTS (10/12 = 83%)
❌ VIOLATIONS FOUND:
  - evidence_retriever_agent: Has prompt.yaml (OK)
  - csv_export_agent: Inline prompt patterns (MEDIUM)

📊 COMPLIANCE SCORE: 83%
```

## Dependencies

- Standard Python libraries
- Git (for hook installation)
- Access to Discernus agent directories
- No external dependencies required