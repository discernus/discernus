# CLI Experiment Definition & Execution Guide

## Overview

This guide explains how to define and run narrative gravity analysis experiments using the command-line interface. The system implements **clean separation of concerns** where three independent component types combine at runtime to create experimental configurations.

## Clean Component Architecture

### 🔧 **LLM Analysis Approach** (Prompt Templates)
Framework-agnostic prompt engineering optimized for specific LLM response patterns.

**Available Approaches:**
- `hierarchical_analysis v2.1.0` - Ranking, weighting, and evidence extraction
- `traditional_analysis v2.1.0` - Comprehensive dimensional scoring
- `civic_virtue_hierarchical v2.1.0` - (deprecated) Legacy conflated naming

### 🏗️ **Theoretical Framework** 
Pure theoretical definitions of narrative space including dipoles and conceptual relationships.

**Available Frameworks:**
- `civic_virtue v2.1.0` - Dignity/Truth/Justice dipoles with civic engagement focus
- `test_civic_virtue vv1.0` - Testing framework for validation

### ⚖️ **Mathematical Weighting** 
Mathematical algorithms for interpreting scores and generating meaningful visualizations.

**Available Methods:**
- `hierarchical_weighted v2.1.0` - Primary/secondary/tertiary importance (45%/35%/20%)
- `linear_traditional v2.1.0` - Equal weight averaging across all dimensions
- `test_winner_take_most vv1.0` - Testing methodology for validation

## Component Management

### List Available Components

```bash
# View all components
python src/narrative_gravity/cli/component_manager.py list

# View specific component type
python src/narrative_gravity/cli/component_manager.py list --type prompt
python src/narrative_gravity/cli/component_manager.py list --type framework
python src/narrative_gravity/cli/component_manager.py list --type weighting
```

### Component Details

```bash
# Get detailed information about a specific component
python src/narrative_gravity/cli/component_manager.py show prompt "hierarchical_analysis" "2.1.0"
python src/narrative_gravity/cli/component_manager.py show framework "civic_virtue" "2.1.0"
python src/narrative_gravity/cli/component_manager.py show weighting "hierarchical_weighted" "2.1.0"
```

## Experiment Definition

### What is an Experiment?

An experiment is a **systematic research configuration** that specifies:

1. **Research Question**: What hypothesis are you testing?
2. **LLM Analysis Approach**: How should the LLM analyze text? (hierarchical vs traditional)
3. **Theoretical Framework**: What conceptual space should be analyzed? (civic virtue, political spectrum)
4. **Mathematical Weighting**: How should scores be interpreted? (hierarchical vs linear)
5. **Target Texts**: What corpus should be analyzed?

### Experiment Creation Process

#### Step 1: Define Research Context
```bash
# Create experiment configuration file
cat > my_experiment_config.yaml << 'EOF'
experiment:
  name: "Lincoln_Speech_Civic_Virtue_Analysis"
  hypothesis: "Lincoln's Second Inaugural uses hierarchical civic virtue themes with Hope and Justice dominance"
  description: "Testing hierarchical vs traditional analysis approaches on foundational American political text"
  research_context: "Validation study comparing LLM analysis approaches for civic virtue framework"

components:
  llm_analysis_approach: "hierarchical_analysis v2.1.0"
  theoretical_framework: "civic_virtue v2.1.0" 
  mathematical_weighting: "hierarchical_weighted v2.1.0"

analysis:
  mode: "single_model"  # or "multi_model"
  selected_models: ["gpt-4o-mini"]
  target_texts: ["corpus/presidential_speeches/lincoln_1865_second_inaugural.txt"]

metadata:
  researcher: "user"
  tags: ["validation_study", "civic_virtue", "hierarchical_analysis"]
  research_notes: "Baseline validation for hierarchical analysis approach"
EOF
```

#### Step 2: Validate Component Compatibility
```bash
# Check if selected components work together
python src/narrative_gravity/cli/component_manager.py validate-compatibility \
    "hierarchical_analysis v2.1.0" \
    "civic_virtue v2.1.0" \
    "hierarchical_weighted v2.1.0"
```

#### Step 3: Create Experiment
```bash
# Create experiment in database
python src/narrative_gravity/cli/experiment_manager.py create \
    --config my_experiment_config.yaml \
    --validate-components
```

### Manual Experiment Creation

```bash
# Direct experiment creation with component IDs
python src/narrative_gravity/cli/experiment_manager.py create \
    --name "Direct_Experiment_Test" \
    --hypothesis "Testing direct CLI experiment creation" \
    --prompt-template-id "db1a7436-54e2-4b13-a03e-25d91ad723c7" \
    --framework-id "059aa4c8-4b50-4c3e-8b4f-123456789abc" \
    --weighting-id "7bbd4ebb-a1b2-4c3d-8e9f-123456789def" \
    --analysis-mode "single_model" \
    --models "gpt-4o-mini"
```

## Experiment Execution

### Single Text Analysis

```bash
# Analyze single text with existing experiment
python src/narrative_gravity/cli/run_analysis.py \
    --experiment-id 16 \
    --text-file "corpus/presidential_speeches/lincoln_1865_second_inaugural.txt" \
    --model "gpt-4o-mini"
```

### Batch Analysis

```bash
# Analyze multiple texts
python src/narrative_gravity/cli/run_analysis.py \
    --experiment-id 16 \
    --text-dir "corpus/presidential_speeches/" \
    --model "gpt-4o-mini" \
    --parallel 3
```

### Multi-Model Analysis

```bash
# Compare across multiple LLMs
python src/narrative_gravity/cli/run_analysis.py \
    --experiment-id 16 \
    --text-file "corpus/presidential_speeches/lincoln_1865_second_inaugural.txt" \
    --models "gpt-4o-mini,claude-3-haiku,gemini-pro" \
    --compare-models
```

## Experiment Management

### List Experiments

```bash
# View all experiments
python src/narrative_gravity/cli/experiment_manager.py list

# View experiments by status
python src/narrative_gravity/cli/experiment_manager.py list --status completed
python src/narrative_gravity/cli/experiment_manager.py list --status running

# View experiments by researcher
python src/narrative_gravity/cli/experiment_manager.py list --researcher user
```

### Experiment Details

```bash
# Get detailed experiment information
python src/narrative_gravity/cli/experiment_manager.py show 16

# View experiment results
python src/narrative_gravity/cli/experiment_manager.py results 16

# Export experiment data
python src/narrative_gravity/cli/experiment_manager.py export 16 --format json
```

## Component Development Workflow

### Creating New Components

#### New LLM Analysis Approach
```bash
# Start development session
python src/narrative_gravity/cli/start_dev_session.py \
    --component-type prompt_template \
    --name "evidence_based_analysis" \
    --hypothesis "Evidence-focused prompts will improve justification quality"

# Create new prompt template
python src/narrative_gravity/cli/component_manager.py create-prompt \
    "evidence_based_analysis" \
    "1.0.0" \
    "templates/evidence_based_prompt.txt" \
    --description "Framework-agnostic evidence-based analysis with citation requirements"
```

#### New Theoretical Framework
```bash
# Create framework from configuration
python src/narrative_gravity/cli/component_manager.py create-framework \
    "moral_foundations" \
    "1.0.0" \
    "frameworks/moral_foundations/config.json" \
    --description "Haidt's moral foundations framework implementation"
```

#### New Mathematical Weighting
```bash
# Create weighting methodology
python src/narrative_gravity/cli/component_manager.py create-weighting \
    "attention_focused" \
    "1.0.0" \
    "exponential" \
    "Dynamic weighting based on salience detection" \
    --formula "weight = exp(salience_score * attention_factor)" \
    --parameters '{"attention_factor": 2.0, "min_weight": 0.1}'
```

## Quality Assurance

### Component Validation

```bash
# Validate component quality
python src/narrative_gravity/cli/validate_component.py \
    --component-type prompt_template \
    --name "hierarchical_analysis" \
    --version "2.1.0"

# Check component compatibility matrix
python src/narrative_gravity/cli/component_manager.py compatibility-matrix
```

### Experiment Validation

```bash
# Validate experiment configuration
python src/narrative_gravity/cli/experiment_manager.py validate 16

# Check experiment reproducibility
python src/narrative_gravity/cli/experiment_manager.py reproduce 16 \
    --text-file "corpus/presidential_speeches/lincoln_1865_second_inaugural.txt"
```

## Post-Experiment Analysis

### Jupyter Notebook Generation

After experiment execution, interactive Jupyter notebooks are automatically generated for rich analysis:

```bash
# Generate enhanced analysis notebook for specific experiment
python src/narrative_gravity/cli/generate_analysis_templates.py \
    --experiment-id 16 \
    --template-type jupyter \
    --output-dir "analysis_results/experiment_16_analysis/"

# Generate comprehensive analysis with all experiments
python src/narrative_gravity/cli/generate_analysis_templates.py \
    --date-range "2025-06-01,2025-06-30" \
    --template-type jupyter \
    --include-visualization \
    --output-dir "analysis_results/june_2025_comprehensive/"
```

### Launch Jupyter Analysis

```bash
# Navigate to generated analysis directory
cd analysis_results/experiment_16_analysis/

# Launch Jupyter server
jupyter notebook enhanced_analysis.ipynb

# Or launch Jupyter Lab for advanced features
jupyter lab enhanced_analysis.ipynb
```

### Interactive Analysis Features

The generated Jupyter notebooks include:
- **📊 Interactive Visualizations**: Plotly-based elliptical plots with zoom, pan, hover
- **📈 Statistical Analysis**: Comprehensive metrics and statistical tests
- **🔍 Data Exploration**: Interactive widgets for filtering and comparison
- **📝 Publication-Ready Output**: LaTeX-formatted tables and high-DPI figures
- **🔄 Reproducible Analysis**: Complete code with explanations and methodology

## Academic Export

### Individual Experiment Export

```bash
# Export experiment for publication
python src/narrative_gravity/cli/export_academic_data.py \
    --experiment-id 16 \
    --format all \
    --output-dir "exports/academic_formats/lincoln_analysis_2025_06_11/"
```

### Comprehensive Research Export

```bash
# Export all experiments from date range
python src/narrative_gravity/cli/export_academic_data.py \
    --date-range "2025-06-01,2025-06-30" \
    --frameworks "civic_virtue" \
    --include-development-sessions \
    --format all \
    --output-dir "exports/academic_formats/june_2025_validation_study/"
```

## Troubleshooting

### Common Issues

#### Component Not Found
```bash
# Error: Component not found
# Solution: List available components
python src/narrative_gravity/cli/component_manager.py list --type prompt

# Find correct component ID
python src/narrative_gravity/cli/component_manager.py show prompt "hierarchical_analysis" "2.1.0"
```

#### Compatibility Issues
```bash
# Error: Components not compatible
# Solution: Check compatibility matrix
python src/narrative_gravity/cli/component_manager.py validate-compatibility \
    "prompt_id" "framework_id" "weighting_id"
```

#### Database Connection Issues
```bash
# Check database status
python check_database.py

# Verify component tables
python src/narrative_gravity/cli/component_manager.py list
```

### Environment Setup

```bash
# Ensure development environment is set up
source scripts/setup_dev_env.sh

# Verify imports work
python3 -c "from src.narrative_gravity.engine import NarrativeGravityWellsElliptical; print('✅ Imports working!')"
```

## Best Practices

### Experiment Design
1. **Clear Hypothesis**: Always specify what you're testing
2. **Component Rationale**: Document why you chose specific components
3. **Validation Focus**: Use clean architecture for systematic comparison
4. **Documentation**: Tag experiments for later analysis

### Component Development
1. **Independent Lifecycles**: Develop each component type separately
2. **Clear Naming**: Use descriptive, framework-agnostic names
3. **Version Control**: Use semantic versioning for all components
4. **Quality Gates**: Validate components before production use

### Research Workflow
1. **Validation First**: Test components before large studies
2. **Systematic Comparison**: Use component matrix for method validation
3. **Academic Standards**: Export data in publication-ready formats
4. **Reproducibility**: Document complete experimental provenance

## Integration with Academic Pipeline

The CLI experiment system integrates seamlessly with the academic publication workflow using a **two-phase approach**:

### **Phase 1: CLI Experiment Execution** (Systematic & Reproducible)
1. **Component Development** → Systematic iteration with hypothesis tracking
2. **Experimental Design** → Clean architecture supporting method validation  
3. **Data Collection** → CLI batch processing with complete provenance
4. **Database Storage** → All results stored with component version tracking

### **Phase 2: Interactive Jupyter Analysis** (Rich & Exploratory)
5. **Jupyter Generation** → Automated creation of analysis-ready notebooks
6. **Interactive Exploration** → Rich visualizations, statistical analysis, data widgets
7. **Academic Export** → Publication-ready data in multiple formats (CSV, R, Stata, Jupyter)
8. **Human Validation** → Interactive comparison protocols for validation studies

### **Benefits of Two-Phase Approach**

- **Reproducibility**: CLI ensures consistent, scriptable experiment execution
- **Exploration**: Jupyter enables rich interactive analysis and hypothesis generation
- **Academic Standards**: Both phases support publication-quality research workflows
- **Validation Focus**: Clean separation enables systematic comparison studies
- **Flexibility**: Researchers can iterate on analysis without re-running expensive LLM calls

This workflow supports the validation-first research platform approach, enabling systematic development and rigorous academic validation of narrative analysis methodologies. 