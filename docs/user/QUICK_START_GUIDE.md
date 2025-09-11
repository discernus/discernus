# Discernus Quick Start Guide

**Run your first experiment in 5 minutes**

This guide will get you up and running with Discernus using the nano_test_experiment, which takes about 47 seconds and costs approximately $0.014.

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

## Step 2: Run Nano Test Experiment (2 minutes)

```bash
# Navigate to the test experiment
cd projects/nano_test_experiment

# Run the experiment
discernus run .

# Expected output:
# ✅ Analysis completed (2 documents, ~30 seconds)
# ✅ Synthesis completed (~17 seconds)
# 💰 Total cost: ~$0.014
```

## Step 3: Verify Results (1 minute)

```bash
# Check the results directory
ls runs/*/results/

# You should see:
# - final_report.md (main results)
# - analysis.json (raw scores)
# - evidence.csv (supporting quotes)
# - scores.csv (dimensional scores)
```

## Step 4: Review Results (1 minute)

```bash
# Open the final report
open runs/*/results/final_report.md

# Or view in terminal
cat runs/*/results/final_report.md
```

## What Just Happened?

The nano_test_experiment analyzed 2 short documents using a simple sentiment framework:

- **Document 1**: Positive sentiment test text
- **Document 2**: Negative sentiment test text
- **Framework**: Binary sentiment analysis (positive/negative scores)
- **Output**: Dimensional scores, evidence, and synthesis report

## Next Steps

### Run More Experiments

```bash
# List available experiments
discernus list

# Try a slightly larger experiment
cd ../micro_test_experiment
discernus run .
```

### Learn More

- **[Installation Guide](INSTALLATION_GUIDE.md)** - Complete setup instructions
- **[CLI Reference](CLI_REFERENCE.md)** - All available commands
- **[Performance Guide](PERFORMANCE_GUIDE.md)** - Timing and cost expectations
- **[Troubleshooting](TROUBLESHOOTING_GUIDE.md)** - Common issues and solutions

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

- Check the [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md) for detailed solutions
- Review the [CLI Reference](CLI_REFERENCE.md) for command options
- See [Performance Guide](PERFORMANCE_GUIDE.md) for timing expectations

---

**Ready for more?** Try the [micro_test_experiment](../projects/micro_test_experiment/) or explore the [CLI Reference](CLI_REFERENCE.md) for advanced features.
