# Discernus User Guide

**Welcome to Discernus - Computational Social Science Research Platform**

Discernus is a THIN architecture platform that combines minimal software with maximum LLM intelligence to enable rigorous, reproducible computational social science research.

## 🚀 Quick Start

**Run your first experiment in 5 minutes:**

```bash
# 1. Verify installation
make check

# 2. Run nano test experiment
cd projects/nano_test_experiment
discernus run .

# 3. View results
open runs/*/results/final_report.md
```

**[→ Complete Quick Start Guide](QUICK_START_GUIDE.md)**

## 📚 User Documentation

### Getting Started
- **[Quick Start Guide](QUICK_START_GUIDE.md)** - 5-minute tutorial with nano_test_experiment
- **[Installation Guide](INSTALLATION_GUIDE.md)** - Complete setup instructions
- **[Release Notes](RELEASE_NOTES.md)** - Alpha features and limitations

### Using Discernus
- **[CLI Reference](CLI_REFERENCE.md)** - All commands and options
- **[Performance Guide](PERFORMANCE_GUIDE.md)** - Timing, costs, and resource requirements
- **[Provenance Guide](PROVENANCE_GUIDE.md)** - How research tracking works
- **[Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md)** - Common issues and solutions

## 🎯 What is Discernus?

Discernus enables researchers to:

- **Bring Your Own Framework**: Use any analytical framework - no hardcoded restrictions
- **Analyze Text**: Apply your frameworks to document collections
- **Generate Statistics**: Automated statistical analysis and reporting
- **Synthesize Research**: AI-powered research synthesis with evidence
- **Track Provenance**: Complete audit trail for reproducibility
- **Manage Costs**: Transparent pricing and budget controls

## 🏗️ How It Works

### THIN Architecture
- **Minimal Software**: Simple orchestration and caching
- **LLM Intelligence**: Analysis, reasoning, and synthesis
- **Natural Language Flow**: LLM-to-LLM communication
- **Academic Standards**: Publication-ready outputs

### Research Workflow
1. **Define Experiment**: Create experiment.md with research questions
2. **Create Framework**: Write your own analytical framework (any .md file)
3. **Prepare Corpus**: Add text documents to analyze
4. **Run Analysis**: Execute dimensional scoring and statistics
5. **Synthesize Results**: Generate research report with evidence
6. **Archive Research**: Create publication-ready packages

## 📊 Experiment Sizes

| Size | Documents | Time | Cost | Use Case |
|------|-----------|------|------|----------|
| **Nano** | 1-2 | < 1 min | ~$0.01 | Testing, learning |
| **Micro** | 3-8 | 1-3 min | ~$0.05-0.15 | Small studies |
| **Small** | 9-20 | 3-8 min | ~$0.20-0.50 | Focused research |
| **Medium** | 21-50 | 8-15 min | ~$0.50-1.50 | Standard studies |
| **Large** | 51-100 | 15-45 min | ~$1.50-5.00 | Comprehensive research |

## 🛠️ Essential Commands

```bash
# Run complete experiment
discernus run projects/experiment

# List available experiments
discernus list

# Check system status
discernus status

# Get help
discernus --help
```

## 💡 Example Experiments

### Available in `projects/` directory:

- **`nano_test_experiment`** - 2 documents, sentiment analysis (47 seconds)
- **`micro_test_experiment`** - 4 documents, sentiment analysis (2 minutes)
- **`business_ethics_experiment`** - Business ethics framework
- **`1a_caf_civic_character`** - Civic character analysis
- **`1b_chf_constitutional_health`** - Constitutional health framework
- **`2a_populist_rhetoric_study`** - Populist discourse analysis

## 🔧 Configuration

### Basic Configuration
Create `.discernus.yaml` in your project:

```yaml
analysis_model: vertex_ai/gemini-2.5-flash
synthesis_model: vertex_ai/gemini-2.5-pro
auto_commit: true
verbose: false
```

### Model Selection
- **Flash Lite**: Fastest, cheapest, good quality
- **Flash**: Balanced speed and quality  
- **Pro**: Highest quality, slower, more expensive

## 💰 Cost Management

### Cost Optimization
```bash
# Development (cheap)
export DISCERNUS_ANALYSIS_MODEL=vertex_ai/gemini-2.5-flash-lite
export DISCERNUS_SYNTHESIS_MODEL=vertex_ai/gemini-2.5-flash-lite

# Production (balanced)
export DISCERNUS_ANALYSIS_MODEL=vertex_ai/gemini-2.5-flash
export DISCERNUS_SYNTHESIS_MODEL=vertex_ai/gemini-2.5-pro
```

### Cost Estimation
- **Per Document**: $0.001-0.030 depending on model
- **Analysis Phase**: 70% of total cost
- **Synthesis Phase**: 30% of total cost

## 🚨 Troubleshooting

### Common Issues

**Authentication Errors**:
```bash
gcloud auth application-default login
```

**High Costs**:
```bash
# Use cheaper models
export DISCERNUS_ANALYSIS_MODEL=vertex_ai/gemini-2.5-flash-lite
```

**Memory Issues**:
```bash
# Use analysis-only mode
discernus run projects/experiment --analysis-only
```

**[→ Complete Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md)**

## 📖 Learn More

### Documentation Structure
- **User Docs** (`docs/user/`) - This directory, user-focused
- **Developer Docs** (`docs/developer/`) - Technical implementation
- **Architecture** (`docs/architecture/`) - System design
- **Specifications** (`docs/specifications/`) - Technical specs

### Key Concepts
- **THIN Architecture**: Minimal software, maximum LLM intelligence
- **Provenance**: Complete audit trail for reproducibility
- **Frameworks**: Reusable analytical approaches
- **Corpus**: Collection of documents to analyze
- **Experiments**: Research projects with defined questions

## 🤝 Getting Help

1. **Check Documentation**: Start with the guides above
2. **Search Issues**: Look for similar problems on GitHub
3. **Ask Questions**: Use GitHub Discussions for help
4. **Report Bugs**: Create GitHub Issues for problems
5. **Contribute**: Help improve the platform

## 🎉 Ready to Start?

1. **[Run Quick Start](QUICK_START_GUIDE.md)** - 5-minute tutorial
2. **[Explore Examples](../projects/)** - Try different experiments
3. **[Read CLI Reference](CLI_REFERENCE.md)** - Learn all commands
4. **[Check Performance Guide](PERFORMANCE_GUIDE.md)** - Understand costs and timing

---

**Welcome to Discernus!** We're excited to see what research you'll create.
