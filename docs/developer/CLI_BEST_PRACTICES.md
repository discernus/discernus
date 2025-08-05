# Discernus CLI Best Practices

**Optimization tips, troubleshooting guide, and expert workflows for computational social science research.**

## Model Selection Best Practices

### Understanding Model Trade-offs

| Model | Speed | Cost | Quality | Use Case |
|-------|-------|------|---------|----------|
| `gemini-2.5-flash-lite` | ⚡ Fastest | 💰 Cheapest | ⭐⭐⭐ Good | Development, testing |
| `gemini-2.5-flash` | ⚡ Fast | 💰💰 Moderate | ⭐⭐⭐⭐ Very Good | Production analysis |
| `gemini-2.5-pro` | 🔄 Slower | 💰💰💰 Expensive | ⭐⭐⭐⭐⭐ Excellent | Final synthesis, publications |

### Recommended Model Strategies

#### Development Workflow
```yaml
# .discernus.dev.yaml
analysis_model: vertex_ai/gemini-2.5-flash-lite
synthesis_model: vertex_ai/gemini-2.5-flash-lite
dry_run: true          # Test without execution
verbose: true          # See what's happening
auto_commit: false     # Manual control
```

**Benefits:**
- 🚀 **Fast iteration** - Quick feedback cycles
- 💰 **Cost-effective** - Minimal expense during development
- 🔍 **Transparent** - Verbose output for debugging

#### Production Workflow
```yaml
# .discernus.prod.yaml
analysis_model: vertex_ai/gemini-2.5-flash
synthesis_model: vertex_ai/gemini-2.5-pro
ensemble_runs: 3       # Reliability through repetition
auto_commit: true      # Track all results
```

**Benefits:**
- ⚖️ **Balanced** - Good quality with reasonable cost
- 📊 **Reliable** - Multiple runs for consistency
- 📝 **Tracked** - Automatic provenance

#### Publication Workflow
```yaml
# .discernus.publication.yaml
analysis_model: vertex_ai/gemini-2.5-pro
synthesis_model: vertex_ai/gemini-2.5-pro
ensemble_runs: 5       # Maximum reliability
verbose: true          # Full documentation
auto_commit: true      # Complete provenance
```

**Benefits:**
- 🏆 **Highest quality** - Best possible results
- 📈 **Maximum reliability** - Multiple ensemble runs
- 📚 **Full documentation** - Complete audit trail

## Cost Optimization Strategies

### 1. Staged Analysis Approach

```bash
# Stage 1: Quick validation with cheapest model
discernus run --analysis-model vertex_ai/gemini-2.5-flash-lite --analysis-only

# Stage 2: If analysis looks good, run full pipeline
discernus continue --synthesis-model vertex_ai/gemini-2.5-pro
```

**Savings:** ~60% cost reduction by validating before expensive synthesis

### 2. Development vs Production Models

**Development** (cost-optimized):
```bash
export DISCERNUS_ANALYSIS_MODEL=vertex_ai/gemini-2.5-flash-lite
export DISCERNUS_SYNTHESIS_MODEL=vertex_ai/gemini-2.5-flash-lite
```

**Production** (quality-optimized):
```bash
export DISCERNUS_ANALYSIS_MODEL=vertex_ai/gemini-2.5-flash
export DISCERNUS_SYNTHESIS_MODEL=vertex_ai/gemini-2.5-pro
```

### 3. Smart Caching Strategy

```bash
# First run - full analysis
discernus run

# Subsequent runs - reuse cached analysis
discernus continue --synthesis-model vertex_ai/gemini-2.5-pro

# Different synthesis approach - no re-analysis cost
discernus continue --synthesis-model vertex_ai/gemini-2.5-flash
```

**Savings:** ~70% cost reduction on subsequent runs

### 4. Batch Processing

```bash
# Process multiple experiments efficiently
for experiment in experiments/*/; do
    echo "Processing: $experiment"
    discernus --quiet run "$experiment" --analysis-only
done

# Then run synthesis on successful analyses
for experiment in experiments/*/; do
    if [ -f "$experiment/runs/*/results/analysis.json" ]; then
        discernus --quiet continue "$experiment"
    fi
done
```

## Performance Optimization

### 1. Parallel Processing

```bash
# Process multiple experiments in parallel
parallel -j 4 'discernus --quiet run {} --analysis-only' ::: experiments/*/

# Follow up with synthesis
parallel -j 2 'discernus --quiet continue {}' ::: experiments/*/
```

### 2. Smart Validation

```bash
# Skip validation for trusted experiments
discernus run --skip-validation

# Use dry-run to validate without execution
discernus run --dry-run
```

### 3. Efficient Output Management

```bash
# Quiet mode for scripts
discernus --quiet run > experiment.log 2>&1

# No-color for log files
discernus --no-color run | tee experiment.log
```

## Workflow Best Practices

### 1. Research Project Setup

```bash
# Create new research project
mkdir political-discourse-study
cd political-discourse-study

# Initialize configuration
discernus config init

# Edit configuration for project needs
cat > .discernus.yaml << EOF
# Political Discourse Study Configuration
analysis_model: vertex_ai/gemini-2.5-flash
synthesis_model: vertex_ai/gemini-2.5-pro
auto_commit: true
verbose: true
ensemble_runs: 3
EOF

# Set up experiment structure
mkdir -p corpus runs shared_cache
```

### 2. Iterative Development

```bash
# 1. Quick structure validation
discernus validate

# 2. Test analysis with cheap model
discernus run --analysis-model vertex_ai/gemini-2.5-flash-lite --analysis-only --dry-run

# 3. Run actual analysis if dry-run looks good
discernus run --analysis-model vertex_ai/gemini-2.5-flash-lite --analysis-only

# 4. If analysis is satisfactory, run full pipeline
discernus continue --synthesis-model vertex_ai/gemini-2.5-pro
```

### 3. Team Collaboration

```bash
# Create team configuration
cat > team-config.yaml << EOF
# Team Standards
analysis_model: vertex_ai/gemini-2.5-flash
synthesis_model: vertex_ai/gemini-2.5-pro
auto_commit: true
ensemble_runs: 3
verbose: false
EOF

# Team members use with personal overrides
DISCERNUS_VERBOSE=true discernus --config team-config.yaml run
```

### 4. CI/CD Integration

```yaml
# .github/workflows/research.yml
name: Research Pipeline
on: [push, pull_request]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Setup Discernus
        run: pip install discernus
      - name: Validate Experiments
        run: |
          for experiment in experiments/*/; do
            discernus --quiet validate "$experiment"
          done
        env:
          DISCERNUS_NO_COLOR: true
          DISCERNUS_QUIET: true

  test-analysis:
    runs-on: ubuntu-latest
    needs: validate
    steps:
      - uses: actions/checkout@v3
      - name: Test Analysis
        run: |
          discernus --quiet run --dry-run --analysis-only
        env:
          DISCERNUS_ANALYSIS_MODEL: vertex_ai/gemini-2.5-flash-lite
          DISCERNUS_NO_COLOR: true
          DISCERNUS_AUTO_COMMIT: false
```

## Error Handling and Debugging

### 1. Systematic Debugging Approach

```bash
# Step 1: Validate experiment structure
discernus validate
echo "Validation exit code: $?"

# Step 2: Test with dry-run
discernus run --dry-run --verbose
echo "Dry-run exit code: $?"

# Step 3: Run with verbose output
discernus --verbose run --analysis-only
echo "Analysis exit code: $?"

# Step 4: Check results and continue
discernus artifacts
discernus continue --verbose
echo "Synthesis exit code: $?"
```

### 2. Common Error Patterns

#### Exit Code 3 - Validation Failed

**Problem:**
```bash
$ discernus run
❌ Missing experiment.md in .
Error: Experiment structure validation failed
# Exit code: 3
```

**Solutions:**
```bash
# Check required files
ls -la experiment.md framework.md corpus/

# Create missing experiment.md
cat > experiment.md << EOF
# Experiment Definition
name: "My Research Experiment"
framework: "framework.md"
corpus: "corpus/"
EOF

# Skip validation if files are in non-standard locations
discernus run --skip-validation
```

#### Exit Code 5 - File Error

**Problem:**
```bash
$ discernus --config missing.yaml run
❌ Config file not found: missing.yaml
Error: Config file not found: missing.yaml
# Exit code: 5
```

**Solutions:**
```bash
# Check file exists and permissions
ls -la missing.yaml

# Use auto-discovery instead
discernus run

# Create config file
discernus config init missing.yaml
```

#### Exit Code 6 - Configuration Error

**Problem:**
```bash
$ discernus config validate
❌ Config validation failed: Invalid YAML syntax at line 5
Error: Config validation failed: Invalid YAML syntax
# Exit code: 6
```

**Solutions:**
```bash
# Check YAML syntax
yamllint .discernus.yaml

# Recreate config
discernus config init --force

# Validate specific sections
python -c "import yaml; yaml.safe_load(open('.discernus.yaml'))"
```

### 3. Performance Debugging

```bash
# Monitor resource usage
time discernus --verbose run --analysis-only

# Check cache efficiency
ls -la shared_cache/artifacts/
discernus artifacts

# Profile model performance
discernus run --analysis-model vertex_ai/gemini-2.5-flash-lite --verbose | grep "tokens\|cost"
```

## Security and Privacy Best Practices

### 1. Credential Management

```bash
# Use environment variables for credentials (not config files)
export GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json

# Never commit credentials to git
echo "*.json" >> .gitignore
echo ".env" >> .gitignore
```

### 2. Data Privacy

```bash
# Use hashed filenames for sensitive data
export DISCERNUS_HASH_FILENAMES=true

# Disable auto-commit for sensitive experiments
export DISCERNUS_AUTO_COMMIT=false
```

### 3. Audit Trail Management

```bash
# Enable comprehensive logging
export DISCERNUS_VERBOSE=true

# Regular provenance validation
scripts/validate_run_integrity.py runs/*/
```

## Advanced Workflows

### 1. Multi-Framework Analysis

```bash
# Analyze same corpus with different frameworks
for framework in frameworks/*.md; do
    framework_name=$(basename "$framework" .md)
    mkdir -p "experiments/$framework_name"
    cp experiment.md corpus/ "experiments/$framework_name/"
    cp "$framework" "experiments/$framework_name/framework.md"
    
    discernus --quiet run "experiments/$framework_name"
done
```

### 2. Ensemble Analysis

```bash
# Run multiple ensemble runs with different models
discernus run --ensemble-runs 3 --analysis-model vertex_ai/gemini-2.5-flash
discernus run --ensemble-runs 3 --analysis-model vertex_ai/gemini-2.5-pro

# Compare results
python scripts/compare_ensemble_results.py runs/*/
```

### 3. Batch Corpus Processing

```bash
# Process large corpus in batches
split -l 100 large_corpus.txt corpus_batch_
for batch in corpus_batch_*; do
    mkdir -p "experiments/batch_$(basename $batch)"
    mv "$batch" "experiments/batch_$(basename $batch)/corpus/"
    cp experiment.md framework.md "experiments/batch_$(basename $batch)/"
    
    discernus --quiet run "experiments/batch_$(basename $batch)" &
done
wait  # Wait for all background jobs
```

### 4. Quality Assurance Pipeline

```bash
#!/bin/bash
# research-qa-pipeline.sh

set -e  # Exit on any error

experiment_dir="$1"
if [ -z "$experiment_dir" ]; then
    echo "Usage: $0 <experiment_directory>"
    exit 2
fi

echo "🔍 Quality Assurance Pipeline for: $experiment_dir"

# Stage 1: Validation
echo "Stage 1: Validation"
discernus --quiet validate "$experiment_dir"
echo "✅ Validation passed"

# Stage 2: Test Analysis
echo "Stage 2: Test Analysis"
discernus --quiet run "$experiment_dir" --analysis-only --analysis-model vertex_ai/gemini-2.5-flash-lite
echo "✅ Test analysis completed"

# Stage 3: Production Analysis
echo "Stage 3: Production Analysis"
discernus --quiet continue "$experiment_dir" --synthesis-model vertex_ai/gemini-2.5-pro
echo "✅ Production synthesis completed"

# Stage 4: Integrity Check
echo "Stage 4: Integrity Check"
python scripts/validate_run_integrity.py "$experiment_dir/runs/"*
echo "✅ Integrity check passed"

echo "🎉 Quality assurance pipeline completed successfully"
```

## Monitoring and Maintenance

### 1. Cost Monitoring

```bash
# Track costs across experiments
grep -r "total_cost" experiments/*/runs/*/manifest.json | \
    awk '{sum += $2} END {print "Total cost: $" sum}'

# Monitor token usage
grep -r "total_tokens" experiments/*/runs/*/manifest.json | \
    awk '{sum += $2} END {print "Total tokens: " sum}'
```

### 2. Performance Monitoring

```bash
# Track execution times
grep -r "end_time\|start_time" experiments/*/runs/*/manifest.json | \
    python scripts/calculate_execution_times.py

# Monitor cache hit rates
ls shared_cache/artifacts/ | wc -l
find experiments/*/runs/ -name "*.json" | wc -l
```

### 3. Health Checks

```bash
# Daily health check script
#!/bin/bash
echo "🏥 Discernus Health Check - $(date)"

# Check system status
discernus status

# Validate configurations
for config in .discernus.yaml team-config.yaml; do
    if [ -f "$config" ]; then
        discernus config validate "$config"
    fi
done

# Check disk space
df -h shared_cache/

# Check recent runs
find experiments/*/runs/ -name "manifest.json" -mtime -1 | \
    xargs grep -l '"status": "completed"' | wc -l | \
    xargs echo "Successful runs in last 24h:"

echo "✅ Health check completed"
```

## Troubleshooting Checklist

### Quick Diagnostic Commands

```bash
# System health
discernus status

# Configuration status
discernus --verbose config show

# Experiment validation
discernus validate

# File permissions
ls -la experiment.md framework.md corpus/

# Cache status
ls -la shared_cache/artifacts/ | head -10

# Recent runs
ls -la runs/ | tail -5

# Environment variables
env | grep DISCERNUS_ | sort
```

### Common Solutions

| Problem | Quick Fix | Command |
|---------|-----------|---------|
| Missing experiment.md | Create template | `echo "name: test" > experiment.md` |
| Invalid config | Recreate | `discernus config init --force` |
| Permission denied | Fix permissions | `chmod 644 .discernus.yaml` |
| Cache corruption | Clear cache | `rm -rf shared_cache/artifacts/*` |
| Git conflicts | Reset | `git reset --hard HEAD` |
| High costs | Use cheaper models | `export DISCERNUS_ANALYSIS_MODEL=vertex_ai/gemini-2.5-flash-lite` |

---

*For command reference, see [CLI_COMMAND_REFERENCE.md](CLI_COMMAND_REFERENCE.md). For configuration details, see [CLI_CONFIGURATION_GUIDE.md](CLI_CONFIGURATION_GUIDE.md).*