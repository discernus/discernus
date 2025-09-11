# Discernus Alpha Release Notes

**Version 2.0.0 - Alpha Release**

*Released: January 2025*

## Overview

Discernus Alpha is the first public release of our computational social science research platform. This release provides core functionality for text analysis, statistical processing, and research synthesis with full provenance tracking.

## Key Features

### Core Platform
- **THIN Architecture**: Minimal software with maximum LLM intelligence
- **Multi-Model Support**: Google Gemini 2.5 series (Flash, Pro, Flash Lite)
- **Complete Provenance**: Full audit trail for all research activities
- **Cost Transparency**: Upfront cost estimation and real-time tracking
- **Academic Standards**: Publication-ready outputs with verification

### Analysis Capabilities
- **Dimensional Scoring**: Framework-based text analysis
- **Statistical Processing**: Automated ANOVA, correlations, effect sizes
- **Evidence Retrieval**: RAG-powered evidence collection
- **Multi-Document Processing**: 1-100 documents per experiment
- **Caching System**: Reuse analysis results for efficiency

### Research Workflow
- **Experiment Management**: Structured experiment definitions
- **Framework System**: Reusable analytical approaches
- **Corpus Processing**: Text collection and preparation
- **Synthesis Reports**: Automated research synthesis
- **Archive Creation**: Publication-ready research packages

## Getting Started

### Quick Start
```bash
# 1. Install and verify
make check

# 2. Run your first experiment (5 minutes)
cd projects/nano_test_experiment
discernus run .

# 3. Explore results
open runs/*/results/final_report.md
```

### Essential Commands
```bash
discernus run [path]           # Run complete experiment
discernus list                 # List available experiments
discernus status               # Check system status
discernus --help               # Get help
```

## Performance Expectations

### Experiment Sizes
- **Nano** (1-2 docs): < 1 minute, ~$0.01
- **Micro** (3-8 docs): 1-3 minutes, ~$0.05-0.15
- **Small** (9-20 docs): 3-8 minutes, ~$0.20-0.50
- **Medium** (21-50 docs): 8-15 minutes, ~$0.50-1.50
- **Large** (51-100 docs): 15-45 minutes, ~$1.50-5.00

### Model Options
- **Flash Lite**: Fastest, cheapest, good quality
- **Flash**: Balanced speed and quality
- **Pro**: Highest quality, slower, more expensive

## Known Limitations

### Alpha Limitations
- **Maximum Documents**: 100 per experiment
- **Maximum Document Size**: 50,000 characters
- **Framework Dimensions**: 20 per framework
- **Corpus Size**: 500MB total per experiment

### Performance Limits
- **Memory Usage**: 2GB peak for large experiments
- **Processing Time**: 60-minute timeout
- **Cost**: No built-in budget limits (monitor manually)

### Platform Limitations
- **LLM Providers**: Google Gemini only (alpha)
- **Operating Systems**: macOS, Linux (Windows untested)
- **Python Version**: 3.13.5+ required

## Breaking Changes

### From Previous Versions
- **CLI Interface**: New `discernus` command replaces old `make` commands
- **Configuration**: YAML-based config files replace JSON
- **Framework Format**: v10 specification required
- **Experiment Structure**: New experiment.md format

### Migration Guide
```bash
# Old way (deprecated)
make run EXPERIMENT=projects/experiment

# New way (alpha)
discernus run projects/experiment
```

## Workarounds

### Common Issues

**High Costs**:
```bash
# Use cheaper models
export DISCERNUS_ANALYSIS_MODEL=vertex_ai/gemini-2.5-flash-lite
export DISCERNUS_SYNTHESIS_MODEL=vertex_ai/gemini-2.5-flash-lite
```

**Memory Issues**:
```bash
# Use analysis-only mode
discernus run projects/experiment --analysis-only
```

**Slow Performance**:
```bash
# Use faster models
discernus run --analysis-model vertex_ai/gemini-2.5-flash-lite
```

**Large Corpora**:
```bash
# Split into smaller experiments
split -l 20 large_corpus.txt corpus_batch_
for batch in corpus_batch_*; do
    mkdir "experiments/batch_$(basename $batch)"
    mv "$batch" "experiments/batch_$(basename $batch)/corpus/"
    discernus run "experiments/batch_$(basename $batch)"
done
```

## Alpha-Specific Considerations

### Research Use
- **Validation Required**: All results should be validated independently
- **Reproducibility**: Use provided archives for replication
- **Cost Management**: Monitor API costs carefully
- **Data Privacy**: Be aware of data sent to LLM providers

### Development Use
- **API Limits**: Respect rate limits and quotas
- **Error Handling**: System may fail on edge cases
- **Documentation**: Some features may be undocumented
- **Support**: Community support only (no commercial support)

### Production Use
- **Not Recommended**: Alpha release not suitable for production
- **Data Loss Risk**: No guarantees on data persistence
- **Breaking Changes**: Future versions may break compatibility
- **Performance**: Not optimized for high-volume usage

## What's Next

### Planned Features (Beta)
- **Multi-Provider Support**: OpenAI, Anthropic, local models
- **Advanced Analytics**: More statistical methods
- **Collaboration Tools**: Team workflows and sharing
- **API Interface**: REST API for integration
- **Cloud Deployment**: Managed hosting options

### Community Contributions
- **Framework Library**: Community-contributed frameworks
- **Corpus Collections**: Shared text collections
- **Extensions**: Plugin system for custom functionality
- **Documentation**: Community-maintained guides

## Support and Resources

### Documentation
- **[Quick Start Guide](QUICK_START_GUIDE.md)** - 5-minute tutorial
- **[Installation Guide](INSTALLATION_GUIDE.md)** - Complete setup
- **[CLI Reference](CLI_REFERENCE.md)** - All commands
- **[Performance Guide](PERFORMANCE_GUIDE.md)** - Timing and costs
- **[Troubleshooting](TROUBLESHOOTING_GUIDE.md)** - Common issues

### Community
- **GitHub Issues**: Bug reports and feature requests
- **Discussions**: Community support and questions
- **Contributing**: How to contribute to the project
- **Examples**: Sample experiments and frameworks

### Getting Help
1. Check the [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md)
2. Search [GitHub Issues](https://github.com/discernus/discernus/issues)
3. Ask questions in [Discussions](https://github.com/discernus/discernus/discussions)
4. Review [Examples](../projects/) for inspiration

## Changelog

### Version 2.0.0 (Alpha)
- Initial alpha release
- Core analysis and synthesis functionality
- Multi-model support (Gemini 2.5 series)
- Complete provenance tracking
- Cost transparency and estimation
- Academic-grade output formatting
- Archive creation for publication
- Comprehensive documentation

---

**Thank you for trying Discernus Alpha!** We're excited to see what research you'll create with our platform.
