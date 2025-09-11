# Discernus Performance Guide

**Timing, costs, and resource requirements for different experiment sizes**

This guide provides performance expectations and cost estimates to help you plan your research projects effectively.

## Experiment Size Categories

Discernus experiments are categorized by document count and expected processing time:

| Category | Documents | Expected Time | Cost Range | Use Case |
|----------|-----------|---------------|------------|----------|
| **Nano** | 1-2 | < 1 minute | $0.01-0.02 | Testing, validation |
| **Micro** | 3-8 | 1-3 minutes | $0.05-0.15 | Small studies, pilots |
| **Small** | 9-20 | 3-8 minutes | $0.20-0.50 | Focused research |
| **Medium** | 21-50 | 8-15 minutes | $0.50-1.50 | Standard research |
| **Large** | 51-100 | 15-45 minutes | $1.50-5.00 | Comprehensive studies |

## Performance Benchmarks

### Nano Experiments (1-2 documents)

**Example**: `nano_test_experiment`
- **Documents**: 2
- **Time**: ~47 seconds
- **Cost**: ~$0.014
- **Memory**: < 100MB
- **Use Case**: Testing, validation, learning

### Micro Experiments (3-8 documents)

**Example**: `micro_test_experiment`
- **Documents**: 4
- **Time**: ~2 minutes
- **Cost**: ~$0.08
- **Memory**: < 200MB
- **Use Case**: Small studies, pilot research

### Small Experiments (9-20 documents)

**Example**: `business_ethics_experiment`
- **Documents**: 4-8
- **Time**: ~5 minutes
- **Cost**: ~$0.25
- **Memory**: < 500MB
- **Use Case**: Focused research projects

### Medium Experiments (21-50 documents)

**Example**: `1a_caf_civic_character`
- **Documents**: 8
- **Time**: ~10 minutes
- **Cost**: ~$0.75
- **Memory**: < 1GB
- **Use Case**: Standard research studies

### Large Experiments (51-100 documents)

**Example**: `1b_chf_constitutional_health`
- **Documents**: 54
- **Time**: ~30 minutes
- **Cost**: ~$3.50
- **Memory**: < 2GB
- **Use Case**: Comprehensive studies

## Cost Breakdown

### Cost Per Document

| Model | Cost per Document | Analysis | Synthesis |
|-------|------------------|----------|-----------|
| **Flash Lite** | $0.001-0.003 | Fast | Fast |
| **Flash** | $0.005-0.010 | Fast | Good |
| **Pro** | $0.015-0.030 | Slower | Excellent |

### Cost Optimization Strategies

**Development Workflow**:
```bash
# Use Flash Lite for development
export DISCERNUS_ANALYSIS_MODEL=vertex_ai/gemini-2.5-flash-lite
export DISCERNUS_SYNTHESIS_MODEL=vertex_ai/gemini-2.5-flash-lite
```

**Production Workflow**:
```bash
# Use balanced models for production
export DISCERNUS_ANALYSIS_MODEL=vertex_ai/gemini-2.5-flash
export DISCERNUS_SYNTHESIS_MODEL=vertex_ai/gemini-2.5-pro
```

## Resource Requirements

### System Requirements

**Minimum**:
- **RAM**: 4GB
- **Disk**: 1GB free space
- **CPU**: 2 cores
- **Network**: Stable internet connection

**Recommended**:
- **RAM**: 8GB
- **Disk**: 5GB free space
- **CPU**: 4 cores
- **Network**: High-speed internet

### Memory Usage by Experiment Size

| Size | Peak Memory | Typical Usage |
|------|-------------|---------------|
| Nano | 100MB | 50MB |
| Micro | 200MB | 100MB |
| Small | 500MB | 250MB |
| Medium | 1GB | 500MB |
| Large | 2GB | 1GB |

## Performance Optimization

### Model Selection

**For Speed**:
- Use `vertex_ai/gemini-2.5-flash-lite` for analysis
- Use `vertex_ai/gemini-2.5-flash` for synthesis

**For Quality**:
- Use `vertex_ai/gemini-2.5-flash` for analysis
- Use `vertex_ai/gemini-2.5-pro` for synthesis

**For Cost**:
- Use `vertex_ai/gemini-2.5-flash-lite` for both phases

### Caching Strategy

**First Run**: Full analysis and synthesis
**Subsequent Runs**: Reuse cached analysis, only re-run synthesis

```bash
# First run - full cost
discernus run projects/experiment

# Subsequent runs - synthesis only
discernus continue projects/experiment
```

### Batch Processing

**Parallel Processing**:
```bash
# Process multiple experiments in parallel
parallel -j 2 'discernus run {}' ::: projects/experiment1 projects/experiment2
```

**Sequential Processing**:
```bash
# Process experiments one at a time
for exp in projects/*/; do
    discernus run "$exp"
done
```

## Known Limitations

### Current Limits

- **Maximum Documents**: 100 per experiment (alpha limit)
- **Maximum Document Size**: 50,000 characters
- **Maximum Framework Dimensions**: 20 per framework
- **Maximum Corpus Size**: 500MB total

### Breaking Points

- **Memory**: Experiments > 50 documents may require 8GB+ RAM
- **Time**: Large experiments may timeout after 60 minutes
- **Cost**: Very large experiments may exceed $10 per run

### Workarounds

**For Large Corpora**:
```bash
# Split large corpus into smaller experiments
split -l 20 large_corpus.txt corpus_batch_
for batch in corpus_batch_*; do
    mkdir "experiments/batch_$(basename $batch)"
    mv "$batch" "experiments/batch_$(basename $batch)/corpus/"
    discernus run "experiments/batch_$(basename $batch)"
done
```

**For Memory Issues**:
```bash
# Use analysis-only mode to reduce memory usage
discernus run projects/experiment --analysis-only
```

## Monitoring Performance

### Real-time Monitoring

```bash
# Run with verbose output to see timing
discernus --verbose run projects/experiment

# Monitor resource usage
top -p $(pgrep -f discernus)
```

### Performance Logs

```bash
# Check execution times
grep "execution_time" projects/experiment/runs/*/manifest.json

# Check memory usage
grep "memory_usage" projects/experiment/runs/*/manifest.json

# Check costs
grep "total_cost" projects/experiment/runs/*/manifest.json
```

## Troubleshooting Performance Issues

### Slow Performance

**Check Model Selection**:
```bash
# Use faster models
discernus run --analysis-model vertex_ai/gemini-2.5-flash-lite
```

**Check System Resources**:
```bash
# Monitor memory usage
free -h
# Monitor disk space
df -h
```

### High Costs

**Use Cheaper Models**:
```bash
# Use Flash Lite for both phases
export DISCERNUS_ANALYSIS_MODEL=vertex_ai/gemini-2.5-flash-lite
export DISCERNUS_SYNTHESIS_MODEL=vertex_ai/gemini-2.5-flash-lite
```

**Use Caching**:
```bash
# Reuse cached analysis
discernus continue projects/experiment
```

### Memory Issues

**Reduce Experiment Size**:
```bash
# Split large experiments
# Use analysis-only mode
discernus run projects/experiment --analysis-only
```

**Check System Resources**:
```bash
# Monitor memory usage
htop
# Check available memory
free -h
```

## Performance Best Practices

1. **Start Small**: Begin with nano/micro experiments
2. **Use Caching**: Leverage cached analysis for iterations
3. **Monitor Resources**: Watch memory and disk usage
4. **Optimize Models**: Choose appropriate models for your needs
5. **Plan Costs**: Estimate costs before running large experiments
6. **Test First**: Validate with small experiments before scaling up

---

**Need Help?** Check the [Troubleshooting Guide](TROUBLESHOOTING_GUIDE.md) or [CLI Reference](CLI_REFERENCE.md) for more detailed guidance.
