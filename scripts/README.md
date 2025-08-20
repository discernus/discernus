# Discernus Scripts Directory

This directory contains utility scripts and tools for Discernus development, testing, and maintenance. Scripts are organized into logical subdirectories for better maintainability.

## 📁 Directory Structure

```
scripts/
├── auditing/                   # Experiment and run integrity validation
├── compliance_tools/           # THIN architecture compliance checking
├── corpus_tools/               # Corpus extraction and processing utilities
├── cursor_tools/               # Development environment and safety tools
├── deprecated/                 # Legacy scripts (preserved for reference)
├── framework_validation/       # Framework validation and quality assurance
└── prompt_engineering_harness.py  # Standalone prompt testing tool
```

## 🔧 Tool Categories

### Framework Validation
**Location**: `scripts/framework_validation/`
**Purpose**: Validates frameworks against the current Discernus framework specification using LLM analysis.

**Key Features**:
- Automated validation against v10.0 specification
- Clear, actionable feedback on blocking issues and quality problems
- LLM-powered analysis with Gemini 2.5 Pro
- Fast iteration without setting up full experiments

**Usage**:
```bash
# Validate a framework (recommended)
make validate-framework FRAMEWORK=projects/my_framework.md

# Direct usage
python3 scripts/framework_validation/framework_validator.py my_framework.md
```

**Documentation**: See `scripts/framework_validation/README.md` for complete usage guide.

### Auditing & Integrity
**Location**: `scripts/auditing/`
**Purpose**: Validate experiment runs and ensure research integrity through provenance checking.

**Key Tools**:
- `validate_run_integrity.py` - Comprehensive integrity validation of research runs
- Content-addressed hash verification
- Provenance chain validation
- Git integration checking

**Usage**:
```bash
# Validate a research run
python3 scripts/auditing/validate_run_integrity.py projects/simple_test/runs/20250804T175152Z
```

### Compliance Tools
**Location**: `scripts/compliance_tools/`
**Purpose**: Ensure THIN architecture compliance and code quality standards.

**Key Tools**:
- `thin_compliance_check.py` - Comprehensive THIN architecture compliance checking
- `thin_compliance_audit.py` - Detailed compliance auditing with recommendations
- `install_git_hooks.sh` - Git hooks for automated compliance checking

**Usage**:
```bash
# Check THIN compliance
python3 scripts/compliance_tools/thin_compliance_check.py

# Run compliance audit
python3 scripts/compliance_tools/thin_compliance_audit.py
```

### Corpus Tools
**Location**: `scripts/corpus_tools/`
**Purpose**: Extract, process, and manage corpus data from various sources.

**Key Tools**:
- `youtube_transcript_extractor.py` - Extract transcripts from YouTube videos
- `enhanced_transcript_extractor.py` - Advanced transcript extraction with metadata
- `stealth_transcript_scraper.py` - Robust transcript extraction with fallbacks
- `download_github_corpora.py` - Download corpus data from GitHub repositories

**Usage**:
```bash
# Extract YouTube transcript
python3 scripts/corpus_tools/youtube_transcript_extractor.py VIDEO_URL

# Download GitHub corpus
python3 scripts/corpus_tools/download_github_corpora.py
```

**Documentation**: See `scripts/corpus_tools/YOUTUBE_EXTRACTION_GUIDE.md` for detailed extraction guide.

### Development Tools
**Location**: `scripts/cursor_tools/`
**Purpose**: Development environment setup, safety, and maintenance utilities.

**Key Tools**:
- `check_environment.py` - Verify development environment setup
- `safe_python.sh` - Safe Python execution wrapper for agents
- `prevent_nested_repos.py` - Prevent nested Git repository issues
- `python_wrapper.py` - Python execution wrapper with safety features

**Usage**:
```bash
# Check environment
make check
# or
python3 scripts/cursor_tools/check_environment.py

# Use safe Python wrapper
./scripts/cursor_tools/safe_python.sh -m discernus.cli run experiment
```

### Prompt Engineering
**Location**: `scripts/prompt_engineering_harness.py`
**Purpose**: Test and iterate on LLM prompts for framework development.

**Key Features**:
- Test prompts against different models
- Compare model responses
- Iterate on prompt design
- Support for file-based prompts

**Usage**:
```bash
# List available models
make harness-list

# Test a simple prompt
make harness-simple MODEL="vertex_ai/gemini-2.5-flash" PROMPT="Test prompt"

# Test from file
make harness-file MODEL="vertex_ai/gemini-2.5-pro" FILE="my_prompt.txt"
```

## 🚀 Quick Start

### For Framework Developers
1. **Validate your framework**: `make validate-framework FRAMEWORK=my_framework.md`
2. **Check environment**: `make check`
3. **Test prompts**: `make harness-file MODEL=vertex_ai/gemini-2.5-flash FILE=my_prompt.txt`

### For System Developers
1. **Check compliance**: `python3 scripts/compliance_tools/thin_compliance_check.py`
2. **Validate runs**: `python3 scripts/auditing/validate_run_integrity.py path/to/run`
3. **Environment setup**: `python3 scripts/cursor_tools/check_environment.py`

### For Corpus Managers
1. **Extract transcripts**: `python3 scripts/corpus_tools/youtube_transcript_extractor.py URL`
2. **Download corpora**: `python3 scripts/corpus_tools/download_github_corpora.py`
3. **Process data**: See individual tool documentation

## 📋 Makefile Integration

Most tools are integrated into the main Makefile for easy access:

```bash
# Framework validation
make validate-framework FRAMEWORK=path/to/framework.md

# Environment checking
make check

# Prompt testing
make harness-list
make harness-simple MODEL=model PROMPT=prompt
make harness-file MODEL=model FILE=file

# Experiment execution (uses safe wrappers)
make run-safe EXPERIMENT=path/to/experiment
make continue-safe EXPERIMENT=path/to/experiment
make debug-safe EXPERIMENT=path/to/experiment
```

## 🔧 Development Guidelines

### Adding New Scripts
1. **Choose appropriate subdirectory** based on script purpose
2. **Follow naming conventions** (snake_case, descriptive names)
3. **Include docstrings** and help text
4. **Add to Makefile** if appropriate for common use
5. **Update this README** with new tool documentation

### Script Organization Principles
- **Single responsibility**: Each script has a clear, focused purpose
- **Logical grouping**: Related scripts are in the same subdirectory
- **Documentation**: Each subdirectory has its own README
- **Makefile integration**: Common operations are accessible via make commands
- **Safety first**: Use safe wrappers and validation where appropriate

### Deprecated Scripts
Scripts that are no longer actively used but preserved for reference are moved to `scripts/deprecated/`. These should not be used in new development but may contain useful patterns or historical context.

## 📚 Related Documentation

- [CLI Best Practices](../docs/developer/CLI_BEST_PRACTICES.md)
- [THIN Architecture Compliance](../docs/developer/THIN_COMPLIANCE.md)
- [Framework Development Guide](../docs/developer/FRAMEWORK_DEVELOPMENT.md)
- [Corpus Management Guide](../docs/developer/CORPUS_MANAGEMENT.md)

## 🤝 Contributing

When adding new scripts or tools:

1. **Follow the organization structure** - put scripts in appropriate subdirectories
2. **Document thoroughly** - include help text, docstrings, and README updates
3. **Test comprehensively** - ensure scripts work in different environments
4. **Consider Makefile integration** - add common operations to the Makefile
5. **Maintain consistency** - follow existing patterns and conventions

The scripts directory is designed to be a comprehensive toolkit for Discernus development, testing, and maintenance. Keep it organized, documented, and accessible.
