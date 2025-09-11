# Research Provenance Guide

**Understanding How Discernus Tracks Your Research**

## What is Provenance?

Provenance is the complete record of how your research was conducted - every step, every decision, every piece of data. Discernus automatically tracks everything to ensure your research is transparent, reproducible, and auditable.

## What Gets Tracked

### 📁 **Complete Experiment Records**
- **Input Materials**: Your experiment specification, framework, and corpus files
- **Analysis Results**: All scores, evidence, and statistical findings
- **Processing Logs**: Every LLM interaction, decision, and system event
- **Output Reports**: Final synthesis reports and all intermediate results

### 🔍 **Automatic Tracking**
- **File Changes**: Every modification to your experiment files
- **Model Usage**: Which AI models were used and when
- **Cost Tracking**: Exact costs for each analysis step
- **Error Logs**: Any issues encountered and how they were resolved

## How It Works

### 1. **Automatic Capture**
Discernus automatically captures everything as you run experiments:
```bash
discernus run projects/my_experiment
# All provenance data is automatically recorded
```

### 2. **Organized Storage**
Your experiment directory contains everything:
```
projects/my_experiment/
├── experiment.md          # Your research questions
├── framework.md           # Your analytical approach
├── corpus/               # Your text documents
├── runs/                 # All experiment runs
│   └── 20250101T120000Z/ # Timestamped run
│       ├── outputs/      # Results and reports
│       ├── logs/         # Complete execution logs
│       └── artifacts/    # All intermediate data
└── shared_cache/         # Reusable analysis results
```

### 3. **Git Integration**
All changes are automatically committed to Git with descriptive messages:
```bash
git log --oneline
# Shows: "Analysis completed for 15 documents using sentiment_binary_v1 framework"
```

## Why This Matters

### ✅ **For Researchers**
- **Reproducibility**: Anyone can recreate your exact analysis
- **Transparency**: Complete visibility into your methodology
- **Quality Control**: Easy to spot and fix issues
- **Publication Ready**: Full audit trail for peer review

### ✅ **For Collaborators**
- **Clear History**: See exactly what was done and when
- **Easy Onboarding**: New team members can understand the work
- **Version Control**: Track changes and improvements over time

### ✅ **For Reviewers**
- **Complete Evidence**: Every claim backed by data
- **Methodology Transparency**: Clear understanding of approach
- **Reproducibility**: Can verify results independently

## Key Features

### 🔒 **Content-Addressable Storage**
- Every file is stored by its content hash (SHA-256)
- Impossible to accidentally modify or lose data
- Automatic deduplication saves space

### 📊 **Comprehensive Logging**
- **Development Logs**: Technical details for debugging
- **Research Logs**: Academic-focused audit trail
- **Performance Logs**: Timing and cost tracking

### 🗂️ **Smart Organization**
- **Runs Directory**: Each experiment run gets its own timestamped folder
- **Shared Cache**: Reusable analysis results across runs
- **Artifacts**: All intermediate data preserved

## Best Practices

### 1. **Keep Experiment Files Clean**
- Use descriptive names for your framework and corpus files
- Include clear metadata in your experiment.md
- Document any manual decisions or assumptions

### 2. **Review Your Provenance**
- Check the logs if something seems wrong
- Use `discernus status` to see system health
- Look at the artifacts to understand what was generated

### 3. **Share Complete Experiments**
- Always share the entire experiment directory
- Include the Git history for full provenance
- Use `discernus archive` to create publication packages

## Troubleshooting

### **Missing Provenance Data**
```bash
# Check if logging is working
discernus status

# Look at recent logs
ls projects/my_experiment/runs/*/logs/
```

### **Corrupted Data**
```bash
# Discernus uses content hashes - corruption is automatically detected
# The system will warn you if any data is corrupted
```

### **Large File Sizes**
```bash
# Use shared cache to avoid duplicating analysis results
# Check what's in your shared_cache directory
ls projects/my_experiment/shared_cache/
```

## Advanced: Technical Details

For detailed technical information about the provenance system, see:
- **[Technical Documentation](../developer/architecture/PROVENANCE_SYSTEM.md)** - Complete system specification
- **[Developer Guide](../developer/README.md)** - For contributors and advanced users

---

**Remember**: Provenance is automatic - you don't need to do anything special. Just run your experiments normally, and Discernus handles all the tracking for you.
