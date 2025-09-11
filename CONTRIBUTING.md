# Contributing to Discernus Development Tools

Thank you for your interest in contributing to the Discernus development tools! This collection provides utilities, testing harnesses, and productivity tools for computational social science research.

## 🎯 Project Overview

The Discernus tools repository contains utilities organized into categories:

- **Auditing Tools** - Quality assurance and compliance checking
- **Compliance Tools** - Standards and regulatory compliance
- **Framework Tools** - Framework development and validation
- **Prompt Engineering** - LLM optimization and testing
- **Testing Harnesses** - Specialized testing utilities
- **IDE Integration** - Development workflow tools

## 🚀 Getting Started

### Development Environment

```bash
# Clone the repository
git clone https://github.com/discernus/tools.git
cd tools

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests to verify setup
pytest tests/
```

### Project Structure

```
tools/
├── scripts/                # Main tool collection
│   ├── auditing/          # Quality assurance
│   ├── compliance_tools/  # Standards compliance
│   ├── cursor_tools/      # IDE integration
│   ├── framework_researcher/  # Framework development
│   ├── framework_validation/  # Framework quality
│   └── prompt_engineering/    # LLM optimization
├── tests/                 # Test suite
├── docs/                  # Documentation
├── examples/              # Usage examples
└── templates/             # Reusable templates
```

## 🛠️ Development Guidelines

### Code Quality Standards

- **Python 3.8+** compatibility required
- **Clear documentation** for all tools
- **Comprehensive testing** for new functionality
- **Cross-platform compatibility** (Windows, macOS, Linux)
- **Minimal dependencies** to reduce maintenance burden

### Tool Design Principles

1. **Single Responsibility** - Each tool does one thing well
2. **Composability** - Tools work together in workflows
3. **Configurability** - Flexible configuration options
4. **Reliability** - Robust error handling and recovery
5. **Performance** - Efficient resource usage

## 🔧 Tool Categories

### 1. Auditing Tools

**Purpose**: Quality assurance and compliance checking

**Current Tools**:
- Dependency license auditing
- Code quality assessment
- Research provenance validation
- Performance monitoring

**Contribution Opportunities**:
- Security vulnerability scanning
- Academic integrity checking
- Automated quality reporting
- Integration with CI/CD systems

**Example Tool Structure**:
```python
#!/usr/bin/env python3
"""
Tool Name: Brief description

Usage:
    python tool_name.py [options] [arguments]

Examples:
    python tool_name.py --input file.txt --output report.html
"""

import argparse
import logging
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Tool description")
    parser.add_argument("input", help="Input file or directory")
    parser.add_argument("--output", help="Output file")
    parser.add_argument("--verbose", action="store_true", help="Verbose output")
    
    args = parser.parse_args()
    
    # Tool implementation
    result = process_input(args.input)
    
    if args.output:
        save_result(result, args.output)
    else:
        print_result(result)

if __name__ == "__main__":
    main()
```

### 2. Framework Research Tools

**Purpose**: Framework development and validation support

**Current Tools**:
- Framework synthesis and documentation
- Research methodology validation
- Academic literature integration
- Statistical validation support

**Contribution Opportunities**:
- Enhanced natural language generation
- Integration with academic databases
- Automated citation management
- Multi-format documentation export

### 3. Prompt Engineering Tools

**Purpose**: LLM optimization and testing

**Current Tools**:
- Systematic prompt testing harness
- Response quality analysis
- A/B testing for prompt variants
- Performance optimization tools

**Contribution Opportunities**:
- Advanced prompt optimization algorithms
- Multi-model testing support
- Cost optimization tools
- Prompt template libraries

## 📋 Contribution Process

### 1. Planning Phase

1. **Check existing tools** for similar functionality
2. **Create GitHub issue** describing the proposed tool
3. **Discuss design approach** with maintainers
4. **Get approval** before starting development

### 2. Development Phase

1. **Create feature branch** from `main`
2. **Follow naming conventions** for tools and files
3. **Implement with comprehensive error handling**
4. **Add configuration options** for flexibility
5. **Include usage examples** and documentation

### 3. Testing Phase

1. **Write unit tests** for core functionality
2. **Add integration tests** for tool workflows
3. **Test cross-platform compatibility**
4. **Validate with real-world data**
5. **Performance testing** for resource usage

### 4. Documentation Phase

1. **Write clear docstrings** for all functions
2. **Create usage examples** with sample data
3. **Update main README** with tool description
4. **Add tool-specific documentation** if complex

### 5. Review Phase

1. **Create pull request** with detailed description
2. **Address review feedback** promptly
3. **Ensure all tests pass** in CI
4. **Update documentation** based on feedback

## 🧪 Testing Guidelines

### Test Structure

```
tests/
├── auditing/              # Auditing tool tests
├── compliance_tools/      # Compliance tool tests
├── framework_researcher/  # Framework tool tests
├── prompt_engineering/    # Prompt tool tests
├── integration/           # Cross-tool integration tests
├── fixtures/              # Test data and fixtures
└── utils/                 # Test utilities
```

### Test Requirements

#### Unit Tests
- Test individual tool functions
- Mock external dependencies
- Cover error conditions
- Fast execution (< 1 second per test)

#### Integration Tests
- Test complete tool workflows
- Use realistic test data
- Verify tool interactions
- Moderate execution time (< 10 seconds)

#### Performance Tests
- Measure resource usage
- Test with large datasets
- Verify scalability
- Document performance characteristics

### Test Data Management

```python
# Use fixtures for test data
@pytest.fixture
def sample_framework():
    return Path("tests/fixtures/sample_framework.md")

@pytest.fixture
def test_config():
    return {
        "input_format": "markdown",
        "output_format": "html",
        "validation_level": "strict"
    }

def test_tool_functionality(sample_framework, test_config):
    result = process_framework(sample_framework, test_config)
    assert result.is_valid
    assert len(result.warnings) == 0
```

## 📚 Documentation Standards

### Tool Documentation

Each tool should include:

1. **Header docstring** with purpose and usage
2. **Command-line help** with clear descriptions
3. **Configuration options** with examples
4. **Error messages** that guide users to solutions
5. **Examples** with real-world use cases

### README Updates

When adding new tools:

1. **Add to tool category** in main README
2. **Include brief description** and primary use case
3. **Provide usage example** with sample command
4. **Link to detailed documentation** if available

### Code Documentation

```python
def validate_framework_structure(framework_path: Path, spec_version: str = "v10") -> ValidationResult:
    """Validate framework against specification requirements.
    
    This function checks framework files for compliance with Discernus
    framework specifications, including required sections, formatting,
    and academic standards.
    
    Args:
        framework_path: Path to the framework markdown file
        spec_version: Specification version to validate against (default: "v10")
        
    Returns:
        ValidationResult containing:
            - is_valid: Boolean indicating overall validation status
            - errors: List of critical validation failures
            - warnings: List of non-critical issues
            - suggestions: List of improvement recommendations
            
    Raises:
        FileNotFoundError: If framework file doesn't exist
        ValidationError: If framework format is severely malformed
        
    Example:
        >>> result = validate_framework_structure(Path("pdaf_v10.md"))
        >>> if result.is_valid:
        ...     print("Framework is valid!")
        >>> else:
        ...     print(f"Validation failed: {result.errors}")
    """
```

## 🔒 Security Guidelines

### Input Validation

- **Sanitize file paths** to prevent directory traversal
- **Validate configuration** to prevent code injection
- **Limit resource usage** to prevent DoS attacks
- **Handle sensitive data** appropriately

### Dependency Management

- **Minimal dependencies** to reduce attack surface
- **Pin versions** in requirements files
- **Regular security updates** for dependencies
- **Vulnerability scanning** in CI pipeline

### Error Handling

```python
def safe_file_operation(file_path: Path) -> Optional[str]:
    """Safely read file with proper error handling."""
    try:
        # Validate path is within allowed directories
        resolved_path = file_path.resolve()
        if not is_safe_path(resolved_path):
            raise SecurityError(f"Path outside allowed directories: {resolved_path}")
            
        # Read file with size limits
        if resolved_path.stat().st_size > MAX_FILE_SIZE:
            raise FileSizeError(f"File too large: {resolved_path}")
            
        return resolved_path.read_text(encoding='utf-8')
        
    except (OSError, UnicodeDecodeError) as e:
        logging.error(f"Failed to read file {file_path}: {e}")
        return None
    except SecurityError as e:
        logging.warning(f"Security violation: {e}")
        return None
```

## 🎯 Tool Quality Checklist

### Before Submitting

- [ ] **Functionality** - Tool works as intended
- [ ] **Error handling** - Graceful failure modes
- [ ] **Documentation** - Clear usage instructions
- [ ] **Testing** - Comprehensive test coverage
- [ ] **Performance** - Acceptable resource usage
- [ ] **Cross-platform** - Works on major platforms
- [ ] **Configuration** - Flexible options
- [ ] **Integration** - Works with existing tools

### Code Review Checklist

- [ ] **Code quality** - Clean, readable implementation
- [ ] **Security** - No obvious vulnerabilities
- [ ] **Dependencies** - Justified and minimal
- [ ] **Backward compatibility** - Doesn't break existing workflows
- [ ] **Documentation** - Complete and accurate
- [ ] **Tests** - Adequate coverage and quality

## 📞 Getting Help

### Communication Channels

1. **GitHub Issues** - Bug reports and feature requests
2. **GitHub Discussions** - General questions and ideas
3. **Email** - tools@discernus.ai for direct contact
4. **Documentation** - Check existing tool docs first

### Common Questions

**Q: How do I add a new tool category?**
A: Create a new directory under `scripts/` and update the main README.

**Q: What's the difference between auditing and compliance tools?**
A: Auditing tools check quality, compliance tools verify standards adherence.

**Q: How do I test tools that require external services?**
A: Use mocking for unit tests, integration tests for real service validation.

**Q: Can I contribute tools in other languages?**
A: Python is preferred, but shell scripts and other languages are acceptable for specific use cases.

## 📄 License

By contributing to Discernus Tools, you agree that your contributions will be licensed under the MIT License.

This permissive licensing enables:
- Maximum adoption across research communities
- Integration with proprietary development tools
- Flexibility for diverse research environments
- Compatibility with various licensing requirements

---

Thank you for helping improve computational social science research tools!