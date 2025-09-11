# Discernus Librarian Tools

Framework management and validation utilities for the Discernus platform.

## 🎯 Purpose

The librarian tools provide framework management capabilities:

- **Framework validation** - Automated quality checks and compliance testing
- **Framework curation** - Tools for organizing and maintaining framework collections
- **Research synthesis** - Automated generation of framework documentation and reports
- **Quality assurance** - Inter-rater reliability testing and validation workflows

## 🛠️ Tools

### `validate_framework.py`
Comprehensive framework validation tool:

```bash
# Basic validation
python scripts/librarian/validate_framework.py framework.md

# Detailed validation with reports
python scripts/librarian/validate_framework.py framework.md --detailed --output validation_report.md

# Batch validation
python scripts/librarian/validate_framework.py frameworks/*.md --summary
```

### `synthesize_framework.py`
Automated framework documentation generator:

```bash
# Generate framework overview
python scripts/librarian/synthesize_framework.py framework.md --type overview

# Create validation report
python scripts/librarian/synthesize_framework.py framework.md --type validation --data reliability_data.json

# Generate usage guide
python scripts/librarian/synthesize_framework.py framework.md --type guide
```

### `curate_frameworks.py`
Framework collection management:

```bash
# Organize frameworks by category
python scripts/librarian/curate_frameworks.py frameworks/ --by-category --output organized/

# Update framework metadata
python scripts/librarian/curate_frameworks.py frameworks/ --update-metadata

# Generate collection index
python scripts/librarian/curate_frameworks.py frameworks/ --index --output index.md
```

## 📊 Validation Levels

- **Level 1**: Specification compliance
- **Level 2**: Academic quality
- **Level 3**: Measurement quality  
- **Level 4**: Production readiness

## 🔗 Dependencies and Integration

### Required Dependencies
- **Discernus Core Platform** - Required for LLM gateway access
- **Python 3.8+** - Runtime environment
- **Standard libraries** - requests, json, xml.etree.ElementTree

### Installation
```bash
# Install Discernus platform first
pip install discernus

# Then use librarian tools
python scripts/librarian/validate_framework.py framework.md
```

### Integration Points
These tools integrate with:
- **Discernus Core Platform** - Framework validation before experiments
- **Framework Repository** - Automated quality assurance  
- **Research Workflow** - Documentation generation and synthesis

## 📄 License

Licensed under GPL v3 (same as parent tools repository) to ensure tools remain free and open source.