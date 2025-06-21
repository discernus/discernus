# CLI Quick Reference - Experiment Operations

## Component Management

### List Components
```bash
# All components
python src/narrative_gravity/cli/component_manager.py list

# By type
python src/narrative_gravity/cli/component_manager.py list --type prompt
python src/narrative_gravity/cli/component_manager.py list --type framework  
python src/narrative_gravity/cli/component_manager.py list --type weighting
```

### Component Info
```bash
# Get component IDs
python src/narrative_gravity/cli/component_manager.py show prompt "hierarchical_analysis" "2.1.0"
```

## Two-Phase Experiment Workflow

### **Phase 1: CLI Execution**

#### 1. Create Experiment
```bash
# Using config file (recommended)
python src/narrative_gravity/cli/experiment_manager.py create --config experiment_config.yaml

# Direct creation
python src/narrative_gravity/cli/experiment_manager.py create \
    --name "My_Experiment" \
    --hypothesis "Testing hypothesis" \
    --prompt-template-id "component_id" \
    --framework-id "component_id" \
    --weighting-id "component_id"
```

#### 2. Run Analysis
```bash
# Single text
python src/narrative_gravity/cli/run_analysis.py \
    --experiment-id 16 \
    --text-file "path/to/text.txt" \
    --model "gpt-4o-mini"

# Batch analysis
python src/narrative_gravity/cli/run_analysis.py \
    --experiment-id 16 \
    --text-dir "corpus/texts/" \
    --model "gpt-4o-mini"
```

### **Phase 2: Jupyter Analysis**

#### 3. Generate Jupyter Notebooks
```bash
python src/narrative_gravity/cli/generate_analysis_templates.py --experiment-id 16
```

#### 4. Interactive Analysis
```bash
cd analysis_results/experiment_16_analysis/
jupyter notebook enhanced_analysis.ipynb
```

#### 5. Export Results
```bash
python src/narrative_gravity/cli/export_academic_data.py --experiment-id 16 --format all
```

## Component Architecture

### Clean Separation of Concerns
1. **🔧 LLM Analysis Approach** (prompt templates) - HOW to analyze
2. **🏗️ Theoretical Framework** (frameworks) - WHAT to analyze  
3. **⚖️ Mathematical Weighting** (weighting methods) - HOW to interpret

### Available Components
- **LLM Approaches**: `hierarchical_analysis`, `traditional_analysis`
- **Frameworks**: `civic_virtue`, `test_civic_virtue`
- **Weighting**: `hierarchical_weighted`, `linear_traditional`

## Quick Setup

### Environment
```bash
source scripts/setup_dev_env.sh
python3 -c "from src.narrative_gravity.engine import NarrativeGravityWellsElliptical; print('✅ Ready')"
```

### Sample Experiment Config
```yaml
experiment:
  name: "Quick_Test"
  hypothesis: "Testing basic functionality"
components:
  llm_analysis_approach: "hierarchical_analysis v2.1.0"
  theoretical_framework: "civic_virtue v2.1.0"
  mathematical_weighting: "hierarchical_weighted v2.1.0"
analysis:
  mode: "single_model"
  selected_models: ["gpt-4o-mini"]
```

## Common Troubleshooting

### Database Issues
```bash
python check_database.py
```

### Component Not Found
```bash
python src/narrative_gravity/cli/component_manager.py list --type prompt
```

### Environment Issues
```bash
source scripts/setup_dev_env.sh
``` 