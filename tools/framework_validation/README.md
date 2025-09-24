# Framework Validator CLI Tool

A dedicated tool for validating Discernus frameworks against the current framework specification. Uses Gemini 2.5 Pro to assess framework coherence, compliance, and quality.

## 🎯 Raison d'Être

**Why This Tool Exists**: Framework validation is the critical first step in the research pipeline. Without proper validation, researchers waste time and resources on experiments with flawed frameworks. This tool provides **fast, reliable structural validation** that catches issues before they propagate through the system.

**The Problem It Solves**: Manual framework review is slow, inconsistent, and error-prone. Researchers need a tool that can quickly assess framework compliance, identify blocking issues, and provide actionable feedback for improvement.

**The Solution**: Automated LLM-powered validation that understands the framework specification, identifies structural and quality issues, and provides clear, actionable recommendations for framework improvement.

- **Automated validation** against the current framework specification
- **Clear, actionable feedback** on blocking issues, quality problems, and suggestions
- **LLM-powered analysis** that understands context and provides intelligent recommendations
- **Fast iteration** without setting up full experiments

## 🚀 Usage

### Basic Validation
```bash
# Validate a framework file
python3 scripts/framework_validation/framework_validator.py projects/pdaf_iteration/pdaf_v9.md

# Use Makefile shortcut (recommended)
make validate-framework FRAMEWORK=projects/pdaf_iteration/pdaf_v9.md
```

### Advanced Options
```bash
# Use a different model (e.g., Flash for faster validation)
python3 scripts/framework_validation/framework_validator.py --model vertex_ai/gemini-2.5-flash my_framework.md

# Verbose output for debugging
python3 scripts/framework_validation/framework_validator.py --verbose my_framework.md

# Get help
python3 scripts/framework_validation/framework_validator.py --help
```

## 📋 What Gets Validated

### 1. **Structural Compliance**
- Required sections (Abstract, Theoretical Foundations, Analytical Methodology)
- Machine-readable appendix with proper YAML formatting
- Essential framework components (dimensions, analysis variants, output schema)

### 2. **Content Quality**
- Theoretical grounding and academic citations
- Clear dimension definitions and examples
- Proper scoring calibration and disambiguation rules

### 3. **Machine-Readable Appendix**
- YAML syntax validation
- Required fields and proper structure
- Formula syntax and mathematical validity
- Output schema compliance

### 4. **Agent Integration**
- Analysis prompt design and clarity
- Sequential analysis variants for complex frameworks
- Proper separation of domain expertise from technical instructions

## 🚨 Issue Classification

### 🚫 **BLOCKING ISSUES** (Priority: "BLOCKING")
- **Impact**: Framework will not pass validation or execute successfully
- **Examples**: Missing required sections, malformed YAML, critical theoretical gaps
- **Action**: Must fix before proceeding

### ⚠️ **QUALITY ISSUES** (Priority: "QUALITY")  
- **Impact**: Framework may function but with reduced reliability or clarity
- **Examples**: Incomplete content, weak theoretical grounding, ambiguous definitions
- **Action**: Should address for better results

### 💡 **SUGGESTIONS** (Priority: "SUGGESTION")
- **Impact**: Framework works but could be improved
- **Examples**: Content enhancements, better examples, performance optimizations
- **Action**: Consider for framework improvement

## 🔧 Technical Details

### LLM Model
- **Default**: `vertex_ai/gemini-2.5-pro` (high-quality validation)
- **Alternative**: `vertex_ai/gemini-2.5-flash` (faster, lower cost)
- **Temperature**: 0.1 (consistent validation results)
- **Max Tokens**: 8000 (handles complex frameworks)

### Validation Process
1. **Load Framework**: Reads and parses the framework file
2. **Load Specification**: Loads current framework specification from `docs/specifications/`
3. **Create Prompt**: Generates comprehensive validation prompt
4. **LLM Analysis**: Uses Gemini to analyze framework against specification
5. **Parse Response**: Extracts structured validation results
6. **Display Results**: Shows categorized issues and suggestions

### Error Handling
- **File Not Found**: Clear error message with path resolution
- **LLM Errors**: Graceful fallback with error details
- **JSON Parsing**: Intelligent parsing with fallback extraction
- **Truncated Responses**: Handles long responses gracefully

## 📁 File Structure

```
scripts/
├── framework_validation/
│   ├── framework_validator.py      # Main validation tool
│   └── README.md                   # This documentation
├── framework_researcher/
│   ├── enhanced_framework_validator.py  # Enhanced validation with research synthesis
│   └── README.md                         # Enhanced validator documentation
└── ...
```

## 🔗 Related Tools

### Enhanced Framework Validator
The **enhanced framework validator** (`scripts/framework_researcher/enhanced_framework_validator.py`) builds upon this canonical validator by adding:

- **Academic validation** using LLM-based assessment
- **Research directions generation** for priority research questions
- **DiscernusLibrarian integration** for systematic literature reviews
- **Research synthesis** combining findings into actionable recommendations
- **Organized output structure** with framework-specific directories

**When to use which tool:**
- **This validator**: Quick structural compliance checks during development
- **Enhanced validator**: Comprehensive validation with academic grounding and research synthesis

## 🎯 Best Practices

### For Framework Developers
1. **Run validation early** in the development process
2. **Address blocking issues first** before quality improvements
3. **Use the suggestions** to enhance framework clarity and robustness
4. **Test with different models** if you encounter issues

### For Framework Reviewers
1. **Use this tool** to quickly assess framework quality
2. **Focus on blocking issues** in code reviews
3. **Reference the suggestions** for improvement recommendations
4. **Validate fixes** by running the tool again

## 🔍 Example Output

```
🔍 Validating framework: /Volumes/code/discernus/projects/pdaf_iteration/pdaf_v9.md

📋 Framework Validation Results
Framework: populist_discourse_analysis_framework
Version: 10.0.0
Status: ❌ FAILED

🚨 Issues Found (5):

🚫 BLOCKING ISSUES (2):
  1. Machine-Readable Appendix: Analysis Variants: The `analysis_variants.default.analysis_prompt` 
     instructs the agent to 'Embed your numerical assessments naturally within the analysis'...

⚠️  QUALITY ISSUES (3):
  1. Agent Integration & Analysis Variants: The `default` analysis variant attempts to evaluate 
     all nine dimensions in a single LLM call...

💡 Additional Suggestions:
  • The implementation of `markers` with `positive_examples`, `negative_examples`, and 
    `boundary_cases` for each dimension is excellent...

❌ Framework has BLOCKING issues and will not pass validation.
Fix these issues before proceeding with experiments.
```

## 🚀 Integration

### Makefile Integration
```makefile
validate-framework:  ## Validate a framework against current specification
	@if [ -z "$(FRAMEWORK)" ]; then echo "❌ Usage: make validate-framework FRAMEWORK=path/to/framework.md"; exit 1; fi
	@echo "🔍 Validating framework: $(FRAMEWORK)"
	@python3 scripts/framework_validation/framework_validator.py $(FRAMEWORK)
```

### CI/CD Integration
```yaml
# Example GitHub Actions step
- name: Validate Framework
  run: |
    python3 scripts/framework_validation/framework_validator.py ${{ github.event.inputs.framework_path }}
```

## 🔧 Troubleshooting

### Common Issues

#### "Framework file not found"
- **Cause**: Incorrect path or working directory
- **Fix**: Use relative path from project root or absolute path

#### "LLM response could not be parsed"
- **Cause**: LLM response format issues or truncation
- **Fix**: Check response length, try different model, or review framework complexity

#### "Validation failed due to parsing error"
- **Cause**: Framework content issues or LLM errors
- **Fix**: Check framework file format, try with --verbose flag

### Performance Tips
- **Use Flash model** for faster validation during development
- **Use Pro model** for final validation before submission
- **Run validation locally** to avoid API rate limits
- **Fix blocking issues first** to get faster feedback cycles

## 📚 Related Documentation

- [Framework Specification (v10.0)](../docs/specifications/FRAMEWORK_SPECIFICATION.md)
- [CLI Best Practices](../docs/developer/CLI_BEST_PRACTICES.md)
- [Framework Development Guide](../docs/developer/FRAMEWORK_DEVELOPMENT.md)

## 🤝 Contributing

To improve the framework validator:

1. **Report issues** with specific examples
2. **Suggest enhancements** for validation logic
3. **Contribute tests** for edge cases
4. **Improve documentation** and examples

The tool is designed to be extensible and can be enhanced to support additional validation rules or integration with other tools.
