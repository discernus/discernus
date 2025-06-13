# Civic Virtue Framework - First Real Experiment Specification
*Generated: June 13, 2025*
*Planned Execution: June 14, 2025*

## **🎯 Experiment Overview**

### **Primary Objective**
Conduct the first comprehensive validation of the Civic Virtue Framework using a strategically selected set of presidential speeches to establish baseline performance metrics and validate the framework's ability to distinguish between different rhetorical approaches to civic engagement.

### **Research Hypothesis**
**H1**: The Civic Virtue Framework will demonstrate systematic differences in civic rhetoric patterns between:
- **Presidential contexts**: Inaugural addresses vs State of the Union speeches
- **Political approaches**: Different presidents' rhetorical strategies for civic engagement
- **Historical periods**: Speeches across different political climates

**H2**: The framework will achieve high reliability (CV ≤ 0.20) across multiple runs, demonstrating readiness for academic research applications.

## **📋 Experimental Design**

### **Framework Specification**
- **Framework**: `civic_virtue` (v2025.06.04)
- **Analysis Dimensions**: 10 wells across virtue-problem dipole
  - **Integrative Wells**: Dignity (primary), Truth (secondary), Justice (secondary), Hope (tertiary), Pragmatism (tertiary)
  - **Disintegrative Wells**: Tribalism (primary), Resentment (secondary), Manipulation (secondary), Fear (tertiary), Fantasy (tertiary)

### **Text Selection Strategy**

**Primary Analysis Set** (8 speeches, balanced design):

1. **Presidential Inaugural Addresses** (Civic Vision Focus):
   - `golden_obama_inaugural_01.txt` - Obama 2009 Inaugural
   - `golden_trump_inaugural_01.txt` - Trump 2017 Inaugural  
   - `golden_biden_inaugural_01.txt` - Biden 2021 Inaugural
   - `golden_bush_inaugural_01.txt` - Bush 2001 Inaugural

2. **State of the Union Addresses** (Policy Implementation Focus):
   - `golden_obama_sotu_01.txt` - Obama SOTU
   - `golden_trump_sotu_01.txt` - Trump SOTU
   - `golden_biden_sotu_01.txt` - Biden SOTU  
   - `golden_bush_sotu_01.txt` - Bush SOTU

**Text Characteristics**:
- **Size Range**: 9.3KB - 46KB (varied complexity)
- **Contexts**: 4 different presidents across 2 distinct speech types
- **Time Span**: 2001-2021 (20-year period)
- **Political Diversity**: Republican and Democratic approaches

### **Technical Specifications**

**LLM Configuration**:
- **Primary Model**: `gpt-4.1-mini` (cost-effective, high performance)
- **Temperature**: 0.1 (consistency-focused)
- **Max Tokens**: 4000 (sufficient for civic virtue analysis)

**Reliability Protocol**:
- **Runs per Text**: 3 runs for reliability validation
- **Total Planned Runs**: 24 runs (8 texts × 3 runs each)
- **Success Criteria**: CV ≤ 0.20 for each text
- **Quality Assurance**: 6-layer QA system validation on all results

**Prompt Template**:
- **Version**: `hierarchical_v2.1` (latest validated template)
- **Framework Integration**: Full civic_virtue well specifications
- **Output Format**: Structured JSON with justifications

## **💰 Cost Estimation**

### **Cost Analysis**
Based on existing experiment data and 2025 pricing:

**Per-Run Cost Estimation**:
- **Model**: GPT-4.1-mini ($0.00015/1K input, $0.0006/1K output)
- **Average Input**: ~3,000 tokens (speech + prompt)
- **Average Output**: ~800 tokens (structured analysis)
- **Estimated Cost per Run**: ~$0.0009 input + $0.0005 output = **$0.0014 per run**

**Total Experiment Cost**:
- **24 runs × $0.0014** = **~$0.034 total**
- **Safety Buffer (50%)**: **~$0.051 maximum**

**Comparison to Historical Data**:
- Recent experiments: $0.034-0.055 per run (GPT-4 legacy pricing)
- This experiment: $0.0014 per run (GPT-4.1-mini efficiency)
- **Cost Reduction**: ~96% improvement with new model

### **Resource Requirements**
- **Estimated Duration**: ~10 minutes total (24 runs × 15s avg + processing)
- **Database Storage**: Minimal impact (~24 new run records)
- **API Rate Limits**: Well within OpenAI limits for GPT-4.1-mini

## **📊 Success Metrics**

### **Primary Success Metrics**

1. **Reliability Achievement**:
   - **Target**: CV ≤ 0.20 for ≥75% of texts (6 of 8 texts)
   - **Stretch Goal**: CV ≤ 0.15 for ≥50% of texts

2. **Framework Discrimination**:
   - **Inaugural vs SOTU**: Significant differences in at least 3 civic virtue dimensions
   - **Cross-Presidential**: Detectable patterns reflecting different civic approaches

3. **Quality Assurance Validation**:
   - **High Confidence**: ≥70% of analyses achieve HIGH QA confidence
   - **Anomaly Detection**: <10% of analyses flagged for anomalies

### **Secondary Success Metrics**

4. **Technical Performance**:
   - **Success Rate**: 100% successful API calls
   - **Processing Time**: ≤20 seconds average per run
   - **Cost Efficiency**: Actual costs within 25% of estimates

5. **Framework Validation**:
   - **Theoretical Coherence**: Results align with expected civic virtue patterns
   - **Practical Utility**: Clear differentiation between rhetorical approaches

## **📋 Experimental Protocol**

### **Execution Sequence**

**Phase 1: Pre-Execution Validation** (5 minutes)
1. ✅ Verify civic_virtue framework configuration
2. ✅ Confirm 8 target texts accessible
3. ✅ Test GPT-4.1-mini API connectivity
4. ✅ Initialize QA system for validation

**Phase 2: Systematic Analysis** (15 minutes)
1. **Inaugural Address Analysis** (4 texts × 3 runs = 12 runs)
   - Execute 3 runs per inaugural speech
   - Real-time reliability monitoring
   - QA validation per run

2. **State of the Union Analysis** (4 texts × 3 runs = 12 runs)
   - Execute 3 runs per SOTU speech
   - Cross-validate with inaugural patterns
   - Comparative analysis preparation

**Phase 3: Quality Validation** (10 minutes)
1. **Reliability Assessment**: Calculate CV for each text
2. **QA System Analysis**: Run 6-layer validation
3. **Anomaly Detection**: Flag any unusual patterns
4. **Success Criteria Evaluation**: Assess against defined metrics

**Phase 4: Results Documentation** (10 minutes)
1. **Experiment Summary**: Generate comprehensive results
2. **Academic Export**: Prepare QA-enhanced dataset
3. **Visualization Generation**: Create civic virtue visualizations
4. **Next Steps Planning**: Define follow-up experiments

### **Quality Controls**

**Real-Time Monitoring**:
- API response validation after each call
- Immediate CV calculation after 3rd run per text
- QA confidence scoring for early anomaly detection

**Error Handling**:
- API failure: Retry with exponential backoff
- Parsing failure: Flag for manual review
- High CV detection: Option for additional runs

**Data Integrity**:
- Complete provenance tracking for all runs
- Backup of raw responses for reanalysis
- Version control for all configuration files

## **🔬 Expected Outcomes**

### **Anticipated Results**

**Rhetorical Pattern Differentiation**:
- **Inaugural Addresses**: Higher Dignity, Hope, Justice scores (aspirational civic vision)
- **State of the Union**: Higher Pragmatism scores, more nuanced problem acknowledgment
- **Cross-Presidential**: Distinctive civic virtue signatures per president

**Framework Performance**:
- **Reliability**: CV ≤ 0.20 for most texts (established framework maturity)
- **Discrimination**: Clear differentiation between speech types and presidential approaches
- **QA Validation**: High confidence scores demonstrating analysis quality

### **Potential Challenges**

**Technical Risks**:
- API rate limiting (mitigation: GPT-4.1-mini has high limits)
- Parsing inconsistencies (mitigation: proven prompt templates)
- Cost overruns (mitigation: conservative estimates with buffer)

**Analytical Risks**:
- Low reliability on complex texts (mitigation: additional runs if needed)
- QA system false positives (mitigation: manual review process)
- Framework misapplication (mitigation: theoretical validation)

## **📈 Next Steps Planning**

### **Immediate Follow-Up** (June 15-16)
1. **Results Analysis**: Comprehensive statistical analysis of patterns
2. **Academic Integration**: Generate QA-enhanced Jupyter notebook
3. **Framework Refinement**: Identify any needed adjustments
4. **Documentation**: Complete experiment report with findings

### **Extended Research Program** (June 17-20)
1. **Cross-Framework Validation**: Compare with political_spectrum framework
2. **Temporal Analysis**: Expand to additional presidential speeches
3. **Publication Preparation**: Academic paper draft with methodology
4. **Replication Package**: Complete academic replication materials

---

**This experiment represents the first comprehensive validation of the Civic Virtue Framework with real-world political discourse, establishing baseline performance for future academic applications.** 