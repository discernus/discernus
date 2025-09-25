# Discernus Installation Guide

**Quick setup guide for Discernus with Vertex AI Gemini integration.**

## Prerequisites

- **Python 3.13+** (required for system compatibility)
- **Git** for version control
- **Google Cloud Account** with Vertex AI enabled
- **Google Cloud CLI** installed and configured

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/discernus/discernus.git
cd discernus
```

### 2. Install Dependencies

#### Option A: Using Makefile (Recommended)
```bash
# Install dependencies using the project Makefile
make install
```

#### Option B: Manual Installation
```bash
# Install dependencies to user directory
pip install --user -r requirements.txt
```

### 3. Configure Environment Variables

```bash
# Copy environment template
cp env.template .env

# Edit .env with your configuration
nano .env  # or your preferred editor
```

### 4. Configure Google Cloud & Vertex AI

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

# Test with available experiment
discernus run projects/0mm --skip-validation
```

## Configuration

### Environment Variables

Configure your environment using the `.env` file:

```bash
# Copy environment template
cp env.template .env

# Edit with your configuration
nano .env
```

Example `.env` configuration:
```bash
# Google Cloud Configuration
GOOGLE_CLOUD_PROJECT=your-project-id
GOOGLE_APPLICATION_CREDENTIALS=path/to/your/service-account-key.json

# Optional: Override default models
DISCERNUS_DEFAULT_MODEL=vertex_ai/gemini-2.5-flash
DISCERNUS_VERIFICATION_MODEL=vertex_ai/gemini-2.5-pro

# Optional: Debug settings
DISCERNUS_DEBUG=false
DISCERNUS_LOG_LEVEL=INFO
```

## Quick Start

### Run Your First Experiment

```bash
# Navigate to an experiment directory
cd projects/0mm

# Run the experiment
discernus run .

# Or run from anywhere
discernus run projects/0mm
```

### Available Commands

```bash
# Run complete experiment
discernus run [path]

# Run specific phases
discernus run [path] --from analysis --to statistical

# Validate experiment structure
discernus validate [path]

# Show experiment artifacts
discernus artifacts [path]

# Show system status
discernus status

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

- **CLI Reference**: `docs/user/CLI_REFERENCE.md`
- **User Guide**: `docs/user/USER_GUIDE.md`
- **Quick Start Guide**: `docs/user/QUICK_START_GUIDE.md`

## Next Steps

1. **Read the CLI Reference** for essential commands
2. **Explore example experiments** in the `projects/` directory
3. **Create your first experiment** using the framework templates
4. **Check system status** with `discernus status`

---

**Need more help?** Check the [CLI Reference](CLI_REFERENCE.md) or [User Guide](USER_GUIDE.md).
