# Discernus Quick Start Guide

**Run your first experiment in 5 minutes**

This guide will get you up and running with Discernus using the nano experiment, which takes about 8-12 minutes and costs approximately $0.50-1.00.

## Prerequisites

- Python 3.13.5+ installed
- Google Cloud account with Vertex AI enabled
- Discernus installed (see [Installation Guide](INSTALLATION_GUIDE.md))

## Step 1: Verify Installation (1 minute)

```bash
# Check system status
make check

# Should show: ✅ System ready
```

## Step 2: Run Nano Experiment (8-12 minutes)

```bash
# Navigate to the test experiment
cd projects/nano

# Run the experiment
discernus run .

# Expected output:
# ✅ Validation completed (~1 minute)
# ✅ Analysis completed (2 documents, ~4-5 minutes)
# ✅ Statistical analysis completed (~1 minute)
# ✅ Evidence curation completed (~1 minute)
# ✅ Synthesis completed (~3 minutes)
# 💰 Total cost: ~$0.50-1.00
```

## Step 3: Verify Results (1 minute)

```bash
# Check the results directory
ls runs/*/artifacts/

# You should see:
# - final_synthesis_report_*.md (main results)
# - statistical_analysis_*.json (statistical results)
# - curated_evidence_*.json (supporting evidence)
# - score_extraction_*.json (dimensional scores)
# - marked_up_document_*.md (documents with evidence highlights)
# - artifact_registry.json (complete provenance registry)
```

## Step 4: Review Results (1 minute)

```bash
# Open the final report
open runs/*/artifacts/final_synthesis_report_*.md

# Or view in terminal
cat runs/*/artifacts/final_synthesis_report_*.md

# Check the run documentation
cat runs/*/README.md
```

## What Just Happened?

The nano experiment analyzed 2 documents using a sentiment framework:

- **Document 1**: Positive sentiment test text
- **Document 2**: Negative sentiment test text
- **Framework**: Binary sentiment analysis (positive/negative scores)
- **Output**: Dimensional scores, statistical analysis, evidence curation, and synthesis report

## Next Steps

### Run More Experiments

```bash
# List available experiments
discernus list

# Try a slightly larger experiment
cd ../micro
discernus run .
```

### Learn More

- **[Installation Guide](INSTALLATION_GUIDE.md)** - Complete setup instructions
- **[CLI Reference](CLI_REFERENCE.md)** - All available commands
- **[User Guide](USER_GUIDE.md)** - Comprehensive user documentation
- **[Alpha Model Strategy](ALPHA_MODEL_STRATEGY.md)** - Performance expectations and model information

## Troubleshooting

### Common Issues

**"Command not found: discernus"**

```bash
# Make sure you're in the project directory
cd /path/to/discernus
# Or install globally
pip install -e .
```

**"Authentication failed"**

```bash
# Re-authenticate with Google Cloud
gcloud auth application-default login
```

**"Vertex AI API not enabled"**

```bash
# Enable the API
gcloud services enable aiplatform.googleapis.com
```

### Getting Help

- Check the [User Guide](USER_GUIDE.md) for comprehensive documentation
- Review the [CLI Reference](CLI_REFERENCE.md) for command options
- See [Alpha Model Strategy](ALPHA_MODEL_STRATEGY.md) for performance expectations

---

**Ready for more?** Try the [micro experiment](../projects/micro/) or explore the [CLI Reference](CLI_REFERENCE.md) for advanced features.
