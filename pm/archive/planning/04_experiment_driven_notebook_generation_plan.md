# Experiment-Driven Notebook Generation Plan

**Status**: Planning Phase  
**Priority**: High - Critical UX Fix  
**Owner**: Core Platform Team  
**Target**: Replace generic Stage 6 templates with experiment-specific analysis notebooks

## 🎯 Problem Statement

### Current System Issues
1. **Generic Universal Template**: One-size-fits-all approach ignores experiment specifications
2. **DCS-Centric Focus**: Emphasizes visualization over hypothesis validation
3. **Cognitive Overload**: Massive cells with complex chart generation code destroy researcher flow
4. **Missing Statistical Analysis**: No connection to experiment's research questions, thresholds, or success criteria
5. **Poor Research UX**: Researchers expecting "r > 0.85 correlation validation" get "territorial coverage metrics" instead

### Research Impact
- Researchers cannot validate their core hypotheses
- Academic success criteria (correlation thresholds, p-values) completely ignored
- Complex visualization code intimidates non-technical users
- Experiment specifications become meaningless - system doesn't use them

## 🏗️ Solution Architecture

### **Phase 1: Hypothesis-Driven Analysis Core** (Priority 1)
Replace generic templates with experiment specification parser that generates targeted hypothesis testing notebooks.

### **Phase 2: DCS Chart Integration** (Priority 2)  
Once statistical foundation works, integrate DCS charts that illuminate and support the analysis findings.

## 📋 Phase 1: Hypothesis-Driven Analysis Core

### **1.1 Experiment Specification Parser**

**Objective**: Extract testable hypotheses from experiment YAML specifications

**Implementation**: 
- Parse `research_question`, `target_correlation`, `success_threshold` fields
- Extract `statistical_analysis.primary_methods` and `validation_metrics`
- Identify model tiers from `models` configuration
- Map to hypothesis testing framework

**Input Example** (from flagship ensemble experiment):
```yaml
research_question: "RQ 1.2: Flagship Model Validation with Intelligent TPM Management"
target_correlation: 0.85
success_threshold: "r > 0.85 with manual coding scores + high inter-flagship-model agreement"

validation_metrics:
  primary_correlation:
    target: "r > 0.85 with BYU manual coding"
    significance: "p < 0.05"
  flagship_ensemble_agreement:
    target: "r > 0.75 inter-flagship-model agreement"
    significance: "p < 0.05"
```

**Output Structure**:
```python
{
    'h1_manual_validation': {
        'target': 0.85,
        'method': 'pearson_correlation',
        'success_criteria': 'r > 0.85, p < 0.05',
        'status': 'pending_manual_data'
    },
    'h2_inter_flagship_agreement': {
        'target': 0.75,
        'models': ['gpt-4o', 'claude-3-5-sonnet-20241022', 'mistral/mistral-large-latest'],
        'method': 'inter_model_correlation',
        'success_criteria': 'r > 0.75, p < 0.05'
    },
    'h3_flagship_vs_local': {
        'flagship_models': ['gpt-4o', 'claude-3-5-sonnet-20241022', 'mistral/mistral-large-latest'],
        'local_models': ['ollama/llama3.2', 'ollama/mistral'],
        'method': 'anova_between_tiers',
        'success_criteria': 'significant_difference'
    }
}
```

### **1.2 Hypothesis Cell Generator**

**Objective**: Generate targeted analysis cells for each hypothesis with specific statistical tests

**Key Features**:
- **Clear Success Criteria**: Each cell shows exact thresholds (r > 0.85, p < 0.05)
- **Pass/Fail Assessment**: Automatic evaluation against experiment specifications
- **Real Data Integration**: Uses actual results from `run_metadata.json`
- **Pending Data Handling**: Graceful handling when manual coding data not yet available

**H1 Example Output**:
```python
# H1: Manual Coding Validation
# Target: r > 0.85 with BYU manual coding

print("🎯 H1: Validating AI Analysis Against Manual Coding")
print("Success Criteria: r > 0.85, p < 0.05")
print("-" * 50)

# Extract AI-generated centroids (ready to run)
ai_centroids = extract_model_centroids(results_df, target_model='gpt-4o')

# Manual coding integration (pending data)
# manual_centroids = pd.read_csv('byu_manual_coding.csv')
# correlation, p_value = pearsonr(ai_centroids, manual_centroids)
# success = correlation > 0.85 and p_value < 0.05
# print(f"📊 Correlation: {correlation:.3f} (p = {p_value:.3f})")
# print(f"🎯 Result: {'✅ PASS' if success else '❌ FAIL'}")

print("⏳ Awaiting BYU manual coding data")
```

**H2 Example Output**:
```python
# H2: Inter-Flagship Model Agreement
# Target: r > 0.75 between flagship models

flagship_models = ['gpt-4o', 'claude-3-5-sonnet-20241022', 'mistral/mistral-large-latest']
print("🎯 H2: Flagship Model Agreement Analysis")

# Calculate inter-model correlations (works with current data)
correlations = {}
for model1, model2 in itertools.combinations(flagship_models, 2):
    corr, p_val = pearsonr(
        extract_model_centroids(results_df, model1),
        extract_model_centroids(results_df, model2)
    )
    correlations[f"{model1} vs {model2}"] = {'r': corr, 'p': p_val}

# Evaluate success
avg_correlation = np.mean([stats['r'] for stats in correlations.values()])
overall_success = avg_correlation > 0.75

print(f"🎯 Average Inter-Flagship Correlation: {avg_correlation:.3f}")
print(f"🎯 Overall Result: {'✅ PASS' if overall_success else '❌ FAIL'}")
```

### **1.3 Statistical Analysis Integration**

**Objective**: Connect generated analysis code to actual experiment results

**Data Pipeline**:
1. Load `run_metadata.json` with experiment results
2. Extract model centroids, coordinates, raw scores
3. Apply statistical tests specified in experiment YAML
4. Generate interpretations based on success thresholds

**Success Validation Logic**:
```python
def evaluate_experiment_success(results, experiment_spec):
    """Evaluate experiment against its own success criteria."""
    validation_results = {}
    
    for hypothesis_id, hypothesis in experiment_spec['hypotheses'].items():
        target = hypothesis['target']
        actual = calculate_actual_metric(results, hypothesis)
        success = actual > target
        
        validation_results[hypothesis_id] = {
            'target': target,
            'actual': actual,
            'success': success,
            'criteria': hypothesis['success_criteria']
        }
    
    return validation_results
```

### **1.4 Clean Notebook Structure**

**Objective**: Generate clean, focused notebooks that researchers can actually use

**Notebook Template Structure**:
```
Cell 1: Data Loading & Experiment Overview
Cell 2: H1 - Manual Coding Validation (r > 0.85 target)
Cell 3: H2 - Inter-Flagship Agreement (r > 0.75 target)  
Cell 4: H3 - Flagship vs Local Model Comparison
Cell 5: H4 - Cost-Effectiveness Analysis
Cell 6: Overall Experiment Success Assessment
Cell 7: Next Steps & Recommendations
```

**Key Principles**:
- **One hypothesis per cell** - Clear cognitive boundaries
- **Immediate feedback** - Pass/fail results visible immediately
- **No complex visualization code** - Focus on statistical validation
- **Actionable outcomes** - Clear guidance on experiment success/failure

## 📋 Phase 2: DCS Chart Integration

### **2.1 Pre-Generated Chart Assets**

**Objective**: Generate DCS charts during experiment execution, display as static assets in notebooks

**Implementation Strategy**:
```python
# During experiment execution (run_experiment.py)
def generate_dcs_visual_assets(experiment_results, output_dir):
    """Generate DCS charts as static assets during experiment execution."""
    
    # Framework overview chart
    plot_dcs_framework(framework_config, experiment_results).savefig(
        f"{output_dir}/dcs_framework_overview.png", dpi=300
    )
    
    # Model comparison chart
    plot_model_comparison(model_centroids).savefig(
        f"{output_dir}/model_comparison.svg"
    )
    
    # Competitive dynamics (if applicable)
    if has_competitive_relationships:
        plot_competitive_dynamics(signatures).save(
            f"{output_dir}/competitive_dynamics.html"
        )
```

**Notebook Integration**:
```python
# Cell 8: DCS Framework Visualization (simple display)
from IPython.display import Image, display

print("📊 DCS Framework Analysis")
print("Supporting visualization for statistical findings above")
display(Image("dcs_framework_overview.png"))
print("✅ Coordinate system validation complete")
```

### **2.2 Chart-Analysis Integration**

**Objective**: Use DCS charts to illuminate and support statistical findings

**Integration Strategy**:
- **Post-hypothesis validation**: Charts appear after statistical tests
- **Finding-specific charts**: Different charts based on hypothesis results
- **Contextual narratives**: Chart descriptions reference statistical outcomes

**Example Integration**:
```python
# Cell 9: Visual Support for H2 Findings
if h2_flagship_agreement_passed:
    print("📊 H2 shows strong flagship agreement (r = 0.82) ✅")
    print("DCS visualization confirms model clustering:")
    display(Image("flagship_clustering.png"))
else:
    print("📊 H2 shows weak flagship agreement (r = 0.45) ❌") 
    print("DCS visualization reveals model divergence:")
    display(Image("model_divergence.png"))
```

## 🚀 Implementation Timeline

### **Week 1-2: Phase 1 Foundation**
- Build experiment specification parser
- Create hypothesis cell generator templates
- Test with flagship ensemble experiment
- Validate statistical analysis accuracy

### **Week 3: Phase 1 Completion** 
- Integrate with existing notebook generation system
- Test across multiple experiment types
- Refine based on researcher feedback
- Document new notebook structure

### **Week 4: Phase 2 Planning**
- Design DCS chart pre-generation system
- Plan integration with statistical findings
- Create chart-hypothesis linking strategy

### **Week 5-6: Phase 2 Implementation**
- Build chart pre-generation during experiment execution
- Integrate charts as supporting assets in notebooks
- Test complete workflow end-to-end

## 📊 Success Metrics

### **Phase 1 Success Criteria**
- [ ] Notebooks generate hypothesis-specific statistical analysis
- [ ] Success/failure assessment based on experiment specifications
- [ ] Clean, readable cells without complex visualization code
- [ ] Researchers can validate their core research questions

### **Phase 2 Success Criteria**  
- [ ] DCS charts enhance rather than overwhelm statistical analysis
- [ ] Charts generated reliably during experiment execution
- [ ] Visual assets support and illuminate hypothesis findings
- [ ] Complete researcher workflow from data collection to publication assets

## 🔧 Technical Architecture

### **New Components**
```
discernus/
├── notebook_generation/
│   ├── experiment_parser.py          # Parse experiment specs
│   ├── hypothesis_generator.py       # Generate hypothesis cells
│   ├── statistical_templates.py     # Statistical analysis templates
│   └── notebook_assembler.py        # Assemble final notebook
├── chart_generation/
│   ├── dcs_asset_generator.py       # Pre-generate DCS charts
│   └── chart_integrator.py         # Integrate charts in notebooks
```

### **Integration Points**
- **Experiment Runner**: Add chart generation after analysis completion
- **Stage 6 Setup**: Replace universal template with experiment-driven generation
- **Notebook Templates**: New hypothesis-focused template library

## 🎯 Expected Outcomes

### **For Researchers**
- **Actionable Analysis**: Can validate core research hypotheses immediately
- **Clear Success Criteria**: Know if experiment succeeded or failed
- **Clean Workflow**: Focus on findings, not debugging visualization code
- **Publication Ready**: Statistical validation ready for academic papers

### **For Discernus Platform**
- **Research-Focused Value**: Platform serves actual research needs
- **Professional Presentation**: Clean notebooks showcase platform sophistication  
- **Academic Credibility**: Proper statistical validation supports academic adoption
- **Unique DCS Value**: Charts enhance rather than overwhelm core analysis

This plan transforms Stage 6 from a generic visualization showcase into a **research validation engine** that serves actual academic workflow needs while preserving Discernus's unique DCS value proposition. 