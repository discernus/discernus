# Discernus Installation Guide

**Quick setup guide for Discernus with Vertex AI Gemini integration.**

## Prerequisites

- **Python 3.13.5+** with virtual environment support
- **Git** for version control
- **Google Cloud Account** with Vertex AI enabled
- **Google Cloud CLI** installed and configured

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/discernus/discernus.git
cd discernus
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure Google Cloud & Vertex AI

#### Install Google Cloud CLI
```bash
# macOS (using Homebrew)
brew install google-cloud-sdk

# Or download from: https://cloud.google.com/sdk/docs/install
```

#### Authenticate with Google Cloud
```bash
# Login to Google Cloud
gcloud auth login

# Set your project (replace with your project ID)
gcloud config set project YOUR_PROJECT_ID

# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com

# Verify authentication
gcloud auth application-default login
```

### 4. Verify Installation

```bash
# Run system check
make check

# Test with simple experiment
discernus run projects/nano_test_experiment --skip-validation
```

## Configuration

### Basic Configuration

Create a `.discernus.yaml` file in your project directory:

```yaml
# Basic Discernus Configuration
analysis_model: vertex_ai/gemini-2.5-flash
synthesis_model: vertex_ai/gemini-2.5-pro
auto_commit: true
verbose: false
```

### Environment Variables

You can also use environment variables:

```bash
export DISCERNUS_ANALYSIS_MODEL=vertex_ai/gemini-2.5-flash
export DISCERNUS_SYNTHESIS_MODEL=vertex_ai/gemini-2.5-pro
export DISCERNUS_AUTO_COMMIT=true
```

## Quick Start

### Run Your First Experiment

```bash
# Navigate to an experiment directory
cd projects/nano_test_experiment

# Run the experiment
discernus run .

# Or run from anywhere
discernus run projects/nano_test_experiment
```

### Available Commands

```bash
# Run complete experiment
discernus run [path]

# Resume from cached analysis
discernus resume [path]

# Validate a specific score
discernus validate-score [path] [document] [score] --score-value [value]

# Show system status
discernus status

# Show configuration
discernus config show

# Get help
discernus --help
```

## Troubleshooting

### Common Issues

**1. Authentication Errors**
```bash
# Re-authenticate with Google Cloud
gcloud auth application-default login
```

**2. Vertex AI API Not Enabled**
```bash
# Enable Vertex AI API
gcloud services enable aiplatform.googleapis.com
```

**3. Python Version Issues**
```bash
# Check Python version
python3 --version

# Should be 3.13.5 or higher
```

**4. Import Errors**
```bash
# Reinstall dependencies
pip install -r requirements.txt --force-reinstall
```

### Getting Help

- **CLI Reference**: `docs/developer/CLI_QUICK_REFERENCE.md`
- **Configuration Guide**: `docs/developer/CLI_CONFIGURATION_GUIDE.md`
- **Best Practices**: `docs/developer/CLI_BEST_PRACTICES.md`

## Next Steps

1. **Read the CLI Quick Reference** for essential commands
2. **Explore example experiments** in the `projects/` directory
3. **Create your first experiment** using the framework templates
4. **Join the community** for support and updates

---

**Need more help?** Check the [CLI Quick Reference](CLI_QUICK_REFERENCE.md) or [Best Practices Guide](CLI_BEST_PRACTICES.md).
