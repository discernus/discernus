# PDAF v10.0 Execution Guide

## 🎯 Overview
This guide provides step-by-step instructions for executing the Trump Populism Evolution Study using the PDAF v10.0 framework.

## 📋 Prerequisites
- **Framework**: PDAF v10.0 configured and available
- **Corpus**: 109 curated documents in `/corpus/analysis_ready/`
- **Models**: Gemini 2.0 Flash (analysis) and Pro (synthesis) available
- **Environment**: Discernus CLI configured and functional

## 🚀 Execution Workflow

### **Phase 1: Campaign Rhetoric Analysis (2015-2016)**
```bash
# Execute analysis for campaign phase
discernus run experiment \
  --framework pdaf_v10 \
  --corpus /corpus/analysis_ready/01_campaign_2015_2016 \
  --model gemini-2.0-flash-exp \
  --output /runs/campaign_2015_2016_results \
  --config /runs/experiment_templates/pdaf_v10_execution.yaml
```

**Expected Output:**
- Individual document PDAF v10.0 analyses
- Phase-level aggregation of populist dimensions
- Key themes and rhetorical patterns identification

### **Phase 2: Presidential Governance Analysis (2017-2020)**
```bash
# Execute analysis for presidential phase
discernus run experiment \
  --framework pdaf_v10 \
  --corpus /corpus/analysis_ready/02_presidential_2017_2020 \
  --model gemini-2.0-flash-exp \
  --output /runs/presidential_2017_2020_results \
  --config /runs/experiment_templates/pdaf_v10_execution.yaml
```

**Focus Areas:**
- Governance rhetoric evolution
- Policy implementation communication
- Institutional vs. populist positioning

### **Phase 3: Post-Presidential Evolution (2021-2023)**
```bash
# Execute analysis for post-presidency phase
discernus run experiment \
  --framework pdaf_v10 \
  --corpus /corpus/analysis_ready/03_post_presidency_2021_2023 \
  --model gemini-2.0-flash-exp \
  --output /runs/post_presidency_2021_2023_results \
  --config /runs/experiment_templates/pdaf_v10_execution.yaml
```

**Critical Analysis:**
- January 6 speech analysis
- Political comeback messaging
- Rally vs. governance rhetoric comparison

### **Phase 4: Current Campaign Analysis (2024-2025)**
```bash
# Execute analysis for 2024 campaign phase
discernus run experiment \
  --framework pdaf_v10 \
  --corpus /corpus/analysis_ready/04_2024_campaign \
  --model gemini-2.0-flash-exp \
  --output /runs/campaign_2024_results \
  --config /runs/experiment_templates/pdaf_v10_execution.yaml
```

**Evolution Tracking:**
- Campaign strategy adaptation
- Policy platform development
- Messaging consistency analysis

### **Phase 5: Baseline Comparison (1988-2000)**
```bash
# Execute analysis for baseline phase
discernus run experiment \
  --framework pdaf_v10 \
  --corpus /corpus/analysis_ready/05_baseline_1988_2000 \
  --model gemini-2.0-flash-exp \
  --output /runs/baseline_1988_2000_results \
  --config /runs/experiment_templates/pdaf_v10_execution.yaml
```

**Longitudinal Foundation:**
- Pre-populist positioning
- Early political rhetoric patterns
- Baseline populist indicators

## 🔬 Synthesis Phase

### **Longitudinal Synthesis Execution**
```bash
# Execute comprehensive synthesis
discernus run synthesis \
  --framework pdaf_v10 \
  --inputs /runs/*_results \
  --model gemini-2.0-pro-exp \
  --output /runs/final_synthesis_report \
  --config /runs/experiment_templates/pdaf_v10_execution.yaml
```

**Synthesis Objectives:**
1. **Evolution Patterns**: Track populist dimension changes across phases
2. **Contextual Analysis**: Compare rhetoric across political roles
3. **Strategic Consistency**: Identify core vs. adaptive messaging
4. **Effectiveness Assessment**: Evaluate rhetorical evolution success

## 📊 Expected Results Structure

```
runs/
├── campaign_2015_2016_results/
│   ├── individual_analyses/
│   ├── phase_summary.json
│   └── key_findings.md
├── presidential_2017_2020_results/
│   ├── governance_rhetoric_analysis.json
│   └── institutional_positioning.md
├── post_presidency_2021_2023_results/
│   ├── comeback_messaging.json
│   └── rally_vs_governance_comparison.md
├── campaign_2024_results/
│   ├── platform_evolution.json
│   └── strategic_adaptation.md
├── baseline_1988_2000_results/
│   ├── early_positioning.json
│   └── populist_foundations.md
└── final_synthesis_report/
    ├── executive_summary.md
    ├── evolution_timeline.json
    ├── key_insights.md
    └── research_implications.pdf
```

## ⚠️ Troubleshooting

### **Common Issues**

#### **Model Availability**
- **Issue**: Gemini Pro model unavailable
- **Solution**: Use Flash model for synthesis phase
- **Impact**: Reduced depth but maintains analytical quality

#### **Rate Limiting**
- **Issue**: API rate limits exceeded
- **Solution**: Implement progressive execution with delays
- **Command**: Add `--delay 30` parameter

#### **Document Processing Errors**
- **Issue**: Individual documents fail processing
- **Solution**: Check document formatting and metadata
- **Recovery**: Skip problematic documents and note in logs

#### **Memory/Resource Constraints**
- **Issue**: Large corpus causes memory issues
- **Solution**: Process phases sequentially
- **Optimization**: Use batch processing for large phases

### **Quality Validation**

#### **Pre-Execution Checks**
```bash
# Validate corpus integrity
discernus validate corpus /corpus/analysis_ready/

# Check framework configuration
discernus validate framework pdaf_v10

# Verify model availability
discernus health check --models gemini-2.0-flash-exp,gemini-2.0-pro-exp
```

#### **Post-Execution Validation**
```bash
# Validate results consistency
discernus validate results /runs/*_results/

# Check synthesis coherence
discernus validate synthesis /runs/final_synthesis_report/
```

## 📈 Performance Optimization

### **Execution Strategies**
1. **Sequential Processing**: Run phases one at a time for stability
2. **Batch Optimization**: Group similar documents for efficient processing
3. **Progressive Validation**: Validate each phase before proceeding
4. **Resource Monitoring**: Track memory and API usage throughout

### **Cost Management**
- **Expected Cost**: $50-150 for complete execution
- **Optimization**: Use Flash for analysis phases, Pro only for synthesis
- **Monitoring**: Track token usage per phase

## 🎯 Success Criteria

### **Technical Success**
- ✅ All 5 phases execute without critical errors
- ✅ Synthesis phase completes successfully
- ✅ Results maintain analytical consistency
- ✅ Metadata and provenance preserved

### **Research Success**
- ✅ Clear populist evolution patterns identified
- ✅ Longitudinal trends documented
- ✅ Contextual rhetorical adaptations analyzed
- ✅ Research implications articulated

---

**Ready for Execution**: All infrastructure prepared
**Estimated Runtime**: 20-30 hours total
**Quality Assurance**: Comprehensive validation pipeline implemented
