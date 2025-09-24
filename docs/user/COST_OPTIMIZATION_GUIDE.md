# Discernus Cost Optimization Guide

**Comprehensive cost analysis and optimization strategies for Discernus experiments**

This guide provides detailed cost breakdowns, optimization strategies, and practical recommendations for managing experiment costs across different scales and use cases.

---

## Executive Summary

**Key Cost Insights:**
- **Analysis costs scale linearly** with document count (~$0.0015-0.0035 per document)
- **Orchestration costs are relatively fixed** (~$0.72-3.38 regardless of document count)
- **Small experiments (<20 docs)**: Orchestration costs dominate (60-80% of total)
- **Large experiments (>100 docs)**: Analysis costs dominate (70-85% of total)
- **Break-even point**: ~20-30 documents where analysis and orchestration costs are equal

**Model Architecture:**
- **Discernus supports only Gemini 2.5 series models** due to their optimal combination of low token costs, large context windows, and unlimited Dynamic Shared Quota (DSQ) service level
- **Academic researchers** can access additional cost savings through [Google Cloud for Researchers](https://cloud.google.com/edu/researchers?hl=en), including up to $5,000 in free credits and academic pricing discounts

---

## Cost Structure Overview

### Per-Document Analysis Cost

**Primary Model**: `vertex_ai/gemini-2.5-flash`
- **Input**: $0.30 per 1M tokens
- **Output**: $2.50 per 1M tokens

**Typical Per-Document Processing (4 analysis steps)**:
- **Score extraction**: `flash-lite` - 3,000-5,000 input, 300-600 output tokens (~$0.0003-0.0006)
- **Evidence extraction**: `flash-lite` - 3,000-5,000 input, 200-400 output tokens (~$0.0002-0.0004)
- **Composite analysis**: `flash` - 3,000-5,000 input, 500-800 output tokens (~$0.0020-0.0035)
- **Markup**: `flash-lite` - 3,000-5,000 input, 200-400 output tokens (~$0.0002-0.0004)
- **Cost per document**: **$0.0027 - $0.0049** (3 flash-lite + 1 flash calls)

**Analysis Cost Scaling**:
```
Small experiment (10 docs):  $0.027 - $0.049
Medium experiment (50 docs): $0.135 - $0.245  
Large experiment (100 docs): $0.270 - $0.490
```

### Post-Analysis Orchestration Cost

**Fixed costs regardless of document count**:

#### 1. Statistical Analysis
- **Model**: `vertex_ai/gemini-2.5-pro` ($1.25/$10.00 per 1M tokens)
- **Input**: 5,000-15,000 tokens (framework) + 2,000-5,000 tokens per document
- **Output**: 23,000-73,000 tokens (comprehensive statistical report)
- **Cost**: **$0.27 - $0.99**

#### 2. Evidence Curation
- **Planning**: $0.043-0.105 (strategic curation plan)
- **Execution**: $0.028-0.700 (1-3 iterations based on corpus size)
- **Total**: **$0.07 - $0.81**

#### 3. Synthesis
- **Stage 1**: $0.325-1.425 (data-driven analysis)
- **Stage 2**: $0.053-0.145 (evidence integration)
- **Total**: **$0.38 - $1.57**

**Total Orchestration Cost**: **$0.72 - $3.38**

---

## Complete Cost Estimates by Experiment Size

| **Experiment Size** | **Documents** | **Analysis Cost** | **Orchestration Cost** | **Total Cost** | **Cost per Document** |
|-------------------|---------------|-------------------|------------------------|----------------|----------------------|
| **Nano** (1-2 docs) | 1-2 | $0.003-0.010 | $0.72-3.38 | **$0.72-3.39** | $0.36-1.70 |
| **Micro** (3-8 docs) | 3-8 | $0.008-0.039 | $0.72-3.38 | **$0.73-3.42** | $0.09-0.43 |
| **Small** (9-20 docs) | 9-20 | $0.024-0.098 | $0.72-3.38 | **$0.74-3.48** | $0.04-0.17 |
| **Medium** (21-50 docs) | 21-50 | $0.057-0.245 | $0.72-3.38 | **$0.78-3.63** | $0.015-0.07 |
| **Large** (51-100 docs) | 51-100 | $0.138-0.490 | $0.72-3.38 | **$0.86-3.87** | $0.008-0.039 |

---

## Cost Optimization Strategies

### 1. Experiment Size Optimization

**For Small Experiments (<20 documents)**:
- **Use `--analysis-only` flag** to skip orchestration costs
- **Savings**: $0.72-3.38 (60-80% cost reduction)
- **Use case**: Quick analysis, testing, validation

**For Medium Experiments (20-50 documents)**:
- **Use `--statistical-prep` flag** to stop before synthesis
- **Savings**: $0.38-1.57 (synthesis costs)
- **Use case**: External statistical analysis, data export

**For Large Experiments (>100 documents)**:
- **Use cost-optimized models** for analysis phase
- **Consider `--resume-from-stats`** for iterative work
- **Use case**: Comprehensive research studies

### 2. Model Selection Optimization

**Available Models** (Gemini 2.5 series only):
- **`vertex_ai/gemini-2.5-flash-lite`**: $0.10/$0.40 per 1M tokens, 1M context, DSQ unlimited
- **`vertex_ai/gemini-2.5-flash`**: $0.30/$2.50 per 1M tokens, 1M context, DSQ unlimited  
- **`vertex_ai/gemini-2.5-pro`**: $1.25/$10.00 per 1M tokens, 2M context, DSQ unlimited

**High-Volume Analysis** (for >100 documents):
```bash
# Use flash-lite for analysis (75% cost reduction)
discernus run experiment --analysis-model vertex_ai/gemini-2.5-flash-lite
```
- **Per-document cost**: $0.0007-0.0014 (vs $0.0027-0.0049)
- **Total savings for 500 docs**: $1.00-1.75

**Quality vs Cost Trade-offs**:
- **Flash-lite**: 75% cost reduction, slight quality reduction
- **Flash**: Standard quality, balanced cost
- **Pro**: Highest quality, 4x cost for analysis

**Why Gemini 2.5 Series Only**:
- **Dynamic Shared Quota (DSQ)**: No rate limits, scales automatically
- **Large context windows**: 1M-2M tokens for complex experiments
- **Cost efficiency**: Best price/performance ratio for research workloads
- **Academic integration**: Seamless with Google Cloud for Researchers program

### 3. Resume Strategy Optimization

**Iterative Workflow**:
```bash
# Step 1: Initial analysis and statistical prep
discernus run experiment --statistical-prep

# Step 2: Resume for synthesis (when ready)
discernus run experiment --resume-from-stats
```
- **Benefits**: Spread costs over time, iterative refinement
- **Use case**: Long-term research projects, budget management

**Analysis-Only Workflow**:
```bash
# Quick analysis without synthesis
discernus run experiment --analysis-only

# Later: Resume for statistical analysis
discernus run experiment --resume-from-analysis
```

### 4. Framework Optimization

**Framework Complexity Impact**:
- **Simple frameworks**: Lower input tokens, faster processing
- **Complex frameworks**: Higher input tokens, more detailed analysis
- **Optimization**: Use simpler frameworks for cost-sensitive projects

**Framework Size Guidelines**:
- **<5,000 tokens**: Low complexity, minimal cost impact
- **5,000-15,000 tokens**: Medium complexity, moderate cost impact  
- **>15,000 tokens**: High complexity, significant cost impact

---

## Practical Cost Management

### Budget Planning

**For Small Projects (<$5 budget)**:
- **Recommended**: Nano/Micro experiments (1-8 documents)
- **Strategy**: Use `--analysis-only` for initial exploration
- **Expected cost**: $0.72-3.42 per experiment

**For Medium Projects ($5-50 budget)**:
- **Recommended**: Small/Medium experiments (9-50 documents)
- **Strategy**: Use `--statistical-prep` for data export
- **Expected cost**: $0.74-3.63 per experiment

**For Large Projects ($50+ budget)**:
- **Recommended**: Large experiments (50+ documents)
- **Strategy**: Use cost-optimized models, resume workflows
- **Expected cost**: $0.86-3.87 per experiment

**Academic Research Benefits**:
- **Google Cloud for Researchers**: Apply for up to $5,000 in free credits
- **Academic pricing**: Additional discounts on Google Cloud services
- **Training credits**: Up to 200 credits for Google Cloud Skills Boost
- **Community access**: Join Google Cloud Research Innovators program
- **Apply at**: [Google Cloud for Researchers](https://cloud.google.com/edu/researchers?hl=en)

### Cost Monitoring

**Real-time Cost Tracking**:
```bash
# Check experiment artifacts for cost breakdown
discernus artifacts experiment_path

# Monitor system status and model usage
discernus status
```

**Cost Estimation**:
- **Before running**: Use document count × $0.002 + $1.00 (orchestration estimate)
- **During analysis**: Monitor audit logs for real-time costs
- **After completion**: Review artifact metadata for detailed breakdown

### Optimization Checklist

**Before Running Experiments**:
- [ ] Choose appropriate experiment size for your budget
- [ ] Select cost-optimized models for large experiments
- [ ] Plan resume strategy for iterative work
- [ ] Consider `--analysis-only` for initial exploration

**During Experiment Execution**:
- [ ] Monitor progress and costs in real-time
- [ ] Use `--resume-from-*` flags for iterative work
- [ ] Stop early with `--statistical-prep` if synthesis not needed

**After Experiment Completion**:
- [ ] Review cost breakdown in artifacts
- [ ] Archive results to avoid re-processing
- [ ] Plan next iteration based on findings

---

## Advanced Cost Optimization

### Custom Model Selection

**For Analysis Phase**:
```bash
# Cost-optimized for large experiments
discernus run experiment --analysis-model vertex_ai/gemini-2.5-flash-lite

# Quality-optimized for small experiments  
discernus run experiment --analysis-model vertex_ai/gemini-2.5-pro
```

**For Synthesis Phase**:
```bash
# Standard synthesis
discernus run experiment --synthesis-model vertex_ai/gemini-2.5-pro

# Cost-optimized synthesis (slight quality reduction)
discernus run experiment --synthesis-model vertex_ai/gemini-2.5-flash
```

### Batch Processing

**For Multiple Small Experiments**:
- **Strategy**: Run analysis-only for all experiments first
- **Then**: Resume synthesis for selected experiments
- **Benefit**: Avoid orchestration costs for experiments you don't need synthesis for

**For Large Corpora**:
- **Strategy**: Split into smaller experiments with `--statistical-prep`
- **Then**: Use `--resume-from-stats` for synthesis of selected results
- **Benefit**: More granular control over synthesis costs

---

## Cost Examples from Real Experiments

### Documented Performance Benchmarks

**Nano Experiment (2 documents)**:
- **Time**: ~47 seconds
- **Cost**: ~$0.014
- **Use case**: Testing, validation

**Micro Experiment (4 documents)**:
- **Time**: ~2 minutes  
- **Cost**: ~$0.08
- **Use case**: Small studies, pilot research

**Medium Experiment (8 documents)**:
- **Time**: ~10 minutes
- **Cost**: ~$0.75
- **Use case**: Standard research studies

**Large Experiment (54 documents)**:
- **Time**: ~30 minutes
- **Cost**: ~$3.50
- **Use case**: Comprehensive studies

### Cost Scaling Examples

**500 Document Experiment**:
- **Analysis cost**: $1.35-2.45 (with flash-lite: $0.35-0.70)
- **Orchestration cost**: $0.72-3.38
- **Total cost**: $2.07-5.83 (with flash-lite: $1.07-4.08)
- **Cost per document**: $0.004-0.012

**1000 Document Experiment**:
- **Analysis cost**: $2.70-4.90 (with flash-lite: $0.70-1.40)
- **Orchestration cost**: $0.72-3.38
- **Total cost**: $3.42-8.28 (with flash-lite: $1.42-5.28)
- **Cost per document**: $0.003-0.008

---

## Conclusion

Discernus provides flexible cost optimization through:

1. **Experiment size planning** - Choose appropriate scale for your budget
2. **Model selection** - Balance quality vs cost based on experiment size
3. **Resume strategies** - Spread costs over time with iterative workflows
4. **Flag optimization** - Use `--analysis-only` and `--statistical-prep` to control costs

**Key Takeaway**: For small experiments, orchestration costs dominate, so use `--analysis-only` for initial exploration. For large experiments, analysis costs dominate, so use cost-optimized models and resume strategies.

**Recommended Starting Point**: Begin with `--analysis-only` experiments to explore your data, then use `--statistical-prep` for data export, and finally `--resume-from-stats` for synthesis only when you're ready for the final report.
