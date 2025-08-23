# Prompt Engineering Harness

A flexible, configurable tool for testing specific LLM models with specific prompts without fallback mechanisms. Perfect for rapid iteration, prompt tuning, and model validation in the Discernus research pipeline.

## 🎯 Purpose

The Prompt Engineering Harness provides a controlled environment for:
- **Model Testing**: Validate specific models with known prompts
- **Prompt Iteration**: Rapidly test and refine prompts
- **Experiment Validation**: Test prompts with real experiment assets
- **Model Comparison**: Compare responses across different models
- **Development Workflow**: Integrate prompt testing into development cycles

## 🚀 Quick Start

### Basic Usage

```bash
# Test simple prompt with specific model
python3 scripts/prompt_engineering/harness.py --model "vertex_ai/gemini-2.5-pro" --prompt "What is 2+2?"

# Test with prompt from file
python3 scripts/prompt_engineering/harness.py --model "anthropic/claude-3-5-sonnet-20240620" --prompt-file "test_prompt.txt"

# Test with experiment assets
python3 scripts/prompt_engineering/harness.py --model "vertex_ai/gemini-2.5-pro" --experiment "projects/simple_test_cff" --corpus "speech1.txt"

# List available models
python3 scripts/prompt_engineering/harness.py --list-models
```

### Prerequisites

- Python 3.8+
- Discernus environment activated
- Valid API keys configured in `.env`
- Required dependencies installed

## 📚 Usage Examples

### 1. Simple Prompt Testing

Test a basic prompt with a specific model:

```bash
python3 scripts/prompt_engineering/harness.py \
  --model "vertex_ai/gemini-2.5-pro" \
  --prompt "Analyze the sentiment of this text: 'I love this new research tool!'"
```

### 2. File-Based Prompt Testing

Test a prompt stored in a file:

```bash
# Create test prompt file
echo "You are a political discourse analyst. Analyze the following text for populist rhetoric markers." > test_prompt.txt

# Test with file
python3 scripts/prompt_engineering/harness.py \
  --model "anthropic/claude-3-5-sonnet-20240620" \
  --prompt-file "test_prompt.txt"
```

### 3. Experiment Asset Testing

Test prompts with real experiment frameworks and corpus:

```bash
python3 scripts/prompt_engineering/harness.py \
  --model "vertex_ai/gemini-2.5-pro" \
  --experiment "projects/simple_test_cff" \
  --corpus "speech1.txt"
```

This loads:
- **Framework**: From `projects/simple_test_cff/framework.md`
- **Corpus**: From `projects/simple_test_cff/corpus/speech1.txt`
- **Creates**: A structured prompt combining both

### 4. Custom System Prompts

Override the default system prompt:

```bash
python3 scripts/prompt_engineering/harness.py \
  --model "vertex_ai/gemini-2.5-pro" \
  --prompt "Analyze this text for moral foundations." \
  --system-prompt "You are an expert in moral psychology and political discourse analysis."
```

## 🔧 Command Line Options

| Option | Short | Description | Required |
|--------|-------|-------------|----------|
| `--model` | `-m` | Model to test (from model registry) | Yes* |
| `--prompt` | `-p` | Direct prompt text to test | No** |
| `--prompt-file` | `-f` | Path to file containing prompt text | No** |
| `--experiment` | `-e` | Path to experiment directory | No** |
| `--corpus` | `-c` | Corpus file name (used with --experiment) | No** |
| `--system-prompt` | `-s` | Custom system prompt | No |
| `--list-models` | `-l` | List all available models in registry | No |

*Required unless using `--list-models`
**Must specify one of: `--prompt`, `--prompt-file`, or `--experiment` with `--corpus`

## 🏗️ Architecture

### Core Components

1. **Model Registry Integration**
   - Loads available models from `discernus.gateway.model_registry`
   - Validates model selection before execution
   - Provides model details and capabilities

2. **Prompt Sources**
   - **Direct**: Inline prompt text
   - **File**: Load from text file
   - **Experiment**: Combine framework + corpus

3. **Secure Execution**
   - Direct model calls without fallback mechanisms
   - Transparent error reporting
   - Usage tracking and cost monitoring

4. **Output Formatting**
   - Structured response display
   - Token usage statistics
   - Execution metadata

### Integration Points

- **Model Registry**: `discernus.gateway.model_registry.ModelRegistry`
- **LiteLLM**: Direct model calling via `litellm.completion`
- **Experiment Assets**: Framework and corpus loading
- **Environment**: `.env` file configuration

## 📊 Output and Results

### Success Response

```
✅ SUCCESS
📝 Response Length: 1,247 characters
🔢 Token Usage: 156 prompt + 1,091 completion = 1,247 total

📄 MODEL RESPONSE:
----------------------------------------
[Model response content]
----------------------------------------
```

### Error Response

```
❌ FAILED
💥 Error: Model 'invalid-model' not found in registry

This is intentional - no fallback mechanism to hide the problem.
```

### Model Listing

```
📋 Available Models (12):
============================================================

🔧 ANTHROPIC:
  - anthropic/claude-3-5-sonnet-20240620 (tier: premium, perf: high)
  - anthropic/claude-3-haiku-20240307 (tier: standard, perf: medium)

🔧 VERTEX_AI:
  - vertex_ai/gemini-2.5-pro (tier: premium, perf: high)
  - vertex_ai/gemini-2.5-flash (tier: standard, perf: medium)
```

## 🎯 Best Practices

### 1. Prompt Design

- **Be Specific**: Clear, unambiguous instructions
- **Include Examples**: Show expected output format
- **Set Constraints**: Define response length and style
- **Test Iteratively**: Small changes, measure impact

### 2. Model Selection

- **Match Task Complexity**: Use appropriate model tier
- **Consider Cost**: Balance performance vs. expense
- **Test Consistency**: Use same model for comparisons
- **Validate Capabilities**: Ensure model supports required features

### 3. Experiment Integration

- **Use Real Assets**: Test with actual frameworks and corpus
- **Maintain Context**: Keep prompts aligned with experiment goals
- **Document Changes**: Track prompt evolution
- **Version Control**: Include prompts in experiment documentation

### 4. Development Workflow

- **Start Simple**: Basic prompts before complex ones
- **Test Early**: Validate prompts before full experiments
- **Iterate Rapidly**: Use harness for quick feedback
- **Document Results**: Keep successful prompt patterns

## 🔍 Troubleshooting

### Common Issues

1. **Model Not Found**
   ```
   ❌ Model 'invalid-model' not found in registry
   ```
   - **Solution**: Use `--list-models` to see available options
   - **Check**: Model registry configuration and API keys

2. **API Errors**
   ```
   ❌ DIRECT CALL FAILED: [API Error Details]
   ```
   - **Solution**: Verify API keys and rate limits
   - **Check**: Network connectivity and service status

3. **File Not Found**
   ```
   ❌ Failed to load experiment assets: [File Error]
   ```
   - **Solution**: Verify file paths and permissions
   - **Check**: Experiment directory structure

4. **Prompt Validation**
   ```
   ❌ Must specify either --prompt, --prompt-file, or --experiment with --corpus
   ```
   - **Solution**: Provide exactly one prompt source
   - **Check**: Command line argument combinations

### Debug Mode

For detailed debugging, add logging:

```bash
export DISCERNUS_LOG_LEVEL=DEBUG
python3 scripts/prompt_engineering/harness.py [options]
```

## 🚧 Development

### Adding New Features

1. **Extend CLI Options**: Add new argument parsers
2. **Enhance Prompt Sources**: Support additional input formats
3. **Improve Output**: Add new result formats and statistics
4. **Integration**: Connect with additional Discernus components

### Testing

```bash
# Test basic functionality
python3 scripts/prompt_engineering/harness.py --list-models

# Test with minimal prompt
python3 scripts/prompt_engineering/harness.py --model "vertex_ai/gemini-2.5-flash" --prompt "Hello"

# Test error handling
python3 scripts/prompt_engineering/harness.py --model "invalid-model" --prompt "test"
```

## 📝 Examples Directory

The `examples/` directory contains sample prompts and test cases:

- **Basic Prompts**: Simple, focused prompts for testing
- **Experiment Templates**: Framework-specific prompt patterns
- **Test Cases**: Validated prompts for common tasks
- **Documentation**: Prompt design guidelines and examples

## 🔗 Related Documentation

- [Discernus CLI Guide](../README.md)
- [Model Registry Documentation](../../discernus/gateway/README.md)
- [Experiment Specification](../../docs/specifications/EXPERIMENT_SPECIFICATION.md)
- [Framework Specification](../../docs/specifications/FRAMEWORK_SPECIFICATION.md)

## 📞 Support

For issues or questions:
1. Check this README and examples
2. Review command line help: `--help`
3. Check Discernus system status
4. Review experiment and framework specifications

---

**Note**: This harness is designed for development and testing. For production experiments, use the full Discernus CLI with proper experiment configuration.
