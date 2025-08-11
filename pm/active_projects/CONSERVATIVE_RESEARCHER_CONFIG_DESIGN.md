# Conservative Researcher Configuration Design
*Durable Statistical Preparation Preferences*

---

## User Experience Problem

**Conservative researchers** who prefer external statistical analysis should be able to:
- Set their preference once and never think about it again
- Never feel "nagged" to use Discernus synthesis
- Have a clear, professional workflow that respects their methodological choices
- Easily collaborate with colleagues who have different preferences

---

## Solution: Enhanced Configuration System

### New Configuration Options

#### Statistical Preparation Mode Setting
```yaml
# .discernus.yaml
# Conservative researcher permanent configuration

# Execution Mode (NEW)
default_execution_mode: statistical_preparation  # Options: complete, statistical_preparation, analysis_only

# Synthesis Preferences (NEW)
synthesis:
  default_enabled: false
  show_synthesis_suggestions: false
  allow_resume_to_synthesis: true

# Existing options work as before
analysis_model: vertex_ai/gemini-2.5-flash-lite
auto_commit: true
skip_validation: false
```

#### Environment Variable Support
```bash
# Durable environment setup
export DISCERNUS_DEFAULT_EXECUTION_MODE=statistical_preparation
export DISCERNUS_SYNTHESIS_DEFAULT_ENABLED=false
export DISCERNUS_SYNTHESIS_SHOW_SUGGESTIONS=false
```

### CLI Behavior Changes

#### Default Command Behavior
```bash
# Conservative researcher configuration active
discernus run
# → Automatically runs statistical preparation (no --statistical-prep needed)
# → No synthesis suggestions or prompts
# → Clean, focused researcher workflow

# Traditional researcher (default configuration)
discernus run  
# → Runs complete pipeline as before
# → No behavior change for existing users
```

#### Override Capabilities
```bash
# Conservative researcher can still access full pipeline when needed
discernus run --complete-pipeline

# Or resume from statistical prep
discernus run --resume-from-stats

# Traditional researcher can try statistical prep
discernus run --statistical-prep
```

### User-Friendly Setup Commands

#### Configuration Wizard
```bash
# Interactive setup for research workflow preferences
discernus config setup

# Output:
# 🔬 Discernus Research Workflow Setup
# 
# How do you prefer to conduct statistical analysis?
# 
# 1. Complete Pipeline (recommended for new users)
#    → Discernus handles analysis, statistics, and interpretation
# 
# 2. Statistical Preparation (recommended for experienced statisticians)  
#    → Discernus handles text analysis, you handle statistics in R/Python/STATA
#
# 3. Analysis Only (minimal processing)
#    → Discernus extracts scores, you handle everything else
#
# Choice [1-3]: 2
#
# ✅ Configuration saved to .discernus.yaml
# ✅ You'll always get analysis-ready CSV datasets by default
# ✅ Run 'discernus run' to start - no additional flags needed
```

#### Pre-configured Profiles
```bash
# Quick profile setup
discernus config profile conservative-researcher
# → Sets statistical_preparation mode, disables synthesis suggestions

discernus config profile complete-pipeline  
# → Traditional full pipeline (default behavior)

discernus config profile minimal-processing
# → Analysis-only mode for maximum researcher control
```

#### Workspace-Specific Setup
```bash
# Set up current project for statistical preparation workflow
discernus config init --profile conservative-researcher

# Set up for traditional complete pipeline
discernus config init --profile complete-pipeline
```

### Enhanced User Messaging

#### Conservative Researcher Experience
```bash
# No synthesis suggestions, clean focus on data preparation
$ discernus run

🔬 Discernus Statistical Preparation Mode
📊 Processing 1,247 documents with Civic Character Framework...
✅ Analysis complete: 1,247/1,247 documents processed
✅ Derived metrics calculated using framework formulas
✅ Statistical preparation package ready: results/statistical_package/

📁 Your analysis-ready dataset:
   • discernus_data.csv - Raw scores + derived metrics + evidence
   • variable_codebook.csv - Column definitions
   • import_scripts/ - R, Python, STATA helpers

🚀 Next: Load data into your preferred statistical software
💡 Tip: See README.txt in statistical_package/ for usage examples

Total cost: $2.47 USD | Processing time: 3.2 minutes
```

#### Traditional Researcher Experience (Unchanged)
```bash
# Existing behavior preserved
$ discernus run

🔬 Discernus Complete Research Pipeline
📊 Processing 1,247 documents with Civic Character Framework...
✅ Analysis complete: 1,247/1,247 documents processed
✅ Statistical analysis complete: ANOVA, correlations, reliability
✅ Synthesis complete: Academic report generated

📁 Complete research package ready: results/
   • final_report.md - Complete academic analysis
   • scores.csv, evidence.csv, statistics.csv
   
Total cost: $8.94 USD | Processing time: 12.7 minutes
```

### Configuration File Templates

#### Conservative Researcher Template
```yaml
# .discernus.yaml - Conservative Researcher Profile
# 
# This configuration optimizes Discernus for researchers who prefer
# to handle their own statistical analysis and interpretation.

# Execution Mode
default_execution_mode: statistical_preparation

# Model Configuration (cost-optimized for text processing)
analysis_model: vertex_ai/gemini-2.5-flash-lite
validation_model: vertex_ai/gemini-2.5-flash-lite

# Synthesis Settings
synthesis:
  default_enabled: false
  show_suggestions: false
  allow_resume: true

# Workflow Settings
auto_commit: true
skip_validation: false
verbose: false

# Output Preferences
statistical_package:
  include_full_evidence: true
  include_import_scripts: true
  format_for_tools: [r, python, stata]
```

#### Complete Pipeline Template (Default)
```yaml
# .discernus.yaml - Complete Pipeline Profile (Default)
#
# This configuration uses Discernus for complete research pipeline
# including statistical analysis and academic interpretation.

# Execution Mode  
default_execution_mode: complete

# Model Configuration (quality-optimized)
analysis_model: vertex_ai/gemini-2.5-flash-lite
synthesis_model: vertex_ai/gemini-2.5-pro
validation_model: vertex_ai/gemini-2.5-pro

# Synthesis Settings
synthesis:
  default_enabled: true
  statistical_analysis: true
  academic_interpretation: true

# Workflow Settings
auto_commit: true
skip_validation: false
verbose: false
```

### Implementation in CLI

#### Enhanced CLI Options
```python
# discernus/cli.py modifications

@click.option('--complete-pipeline', is_flag=True, 
              help='Force complete pipeline (overrides statistical prep default)')
@click.option('--statistical-prep', is_flag=True,
              help='Force statistical preparation mode (overrides complete default)')
@click.option('--respect-config', is_flag=True, default=True,
              help='Use configuration file execution mode (default: true)')
def run(ctx, experiment_path, complete_pipeline, statistical_prep, respect_config, ...):
    
    # Load configuration
    config = ctx.obj['config']
    
    # Determine execution mode
    if complete_pipeline:
        execution_mode = "complete"
    elif statistical_prep:
        execution_mode = "statistical_preparation"  
    elif respect_config and config.default_execution_mode:
        execution_mode = config.default_execution_mode
    else:
        execution_mode = "complete"  # Default behavior
    
    # Execute with appropriate mode
    if execution_mode == "statistical_preparation":
        result = orchestrator.run_experiment(statistical_prep_only=True, ...)
    else:
        result = orchestrator.run_experiment(...)
```

#### Configuration Management Commands
```python
@cli.group()
def config():
    """Manage Discernus configuration and research workflow preferences."""
    pass

@config.command()
@click.option('--profile', type=click.Choice(['conservative-researcher', 'complete-pipeline', 'minimal-processing']))
def setup(profile):
    """Interactive setup for research workflow preferences."""
    if profile:
        _apply_profile(profile)
    else:
        _interactive_workflow_setup()

@config.command()
@click.argument('profile_name', type=click.Choice(['conservative-researcher', 'complete-pipeline', 'minimal-processing']))
def profile(profile_name):
    """Apply a pre-configured research workflow profile."""
    _apply_profile(profile_name)

@config.command()
def show():
    """Show current configuration and execution mode."""
    config = load_config()
    _display_config_summary(config)
```

### Documentation Updates

#### New User Onboarding
```markdown
# Getting Started with Discernus

## Choose Your Research Workflow

Discernus supports different research workflows depending on your statistical analysis preferences:

### 🎯 Statistical Preparation Mode (Recommended for experienced statisticians)
**Best for**: Researchers who prefer R, Python, STATA for statistical analysis

**Setup**: `discernus config profile conservative-researcher`

**Workflow**: 
1. Discernus processes your texts and applies analytical frameworks
2. You receive analysis-ready CSV datasets with complete provenance
3. You perform statistical analysis using your preferred tools
4. You write conclusions and interpretation

### 🔬 Complete Pipeline Mode (Recommended for new users)
**Best for**: Researchers who want end-to-end analysis

**Setup**: `discernus config profile complete-pipeline` (default)

**Workflow**:
1. Discernus processes texts, performs statistics, and generates reports
2. You receive complete academic reports with interpretations
3. You review, refine, and publish results
```

#### Conservative Researcher Guide
```markdown
# Conservative Researcher Workflow Guide

## One-Time Setup
```bash
# Set your permanent preference
discernus config profile conservative-researcher

# Verify setup
discernus config show
```

## Daily Workflow
```bash
# Simple, consistent command - no flags needed
discernus run

# Your data is always ready in: results/statistical_package/
```

## Collaboration with Full-Pipeline Colleagues
```bash
# Share your statistical prep results
git add results/statistical_package/
git commit -m "Statistical prep complete - ready for analysis"

# Colleague can continue to synthesis if desired
discernus run --resume-from-stats
```

### Benefits of This Approach

#### For Conservative Researchers
- **Set once, forget forever**: No need to remember flags or feel nagged
- **Professional workflow**: Clean, focused on their expertise
- **Collaboration friendly**: Easy handoff between text processing and statistical analysis
- **Cost optimized**: Only pay for text processing, not statistical analysis they'll redo

#### For Discernus
- **Broader adoption**: Appeals to methodologically conservative researchers
- **Clear value proposition**: Excellence in text processing, respect for statistical expertise
- **Reduced support burden**: Clear workflow boundaries reduce confusion
- **User retention**: Satisfied users become advocates

#### For Mixed Teams
- **Workflow flexibility**: Team members can use different modes
- **Skill specialization**: Text processing specialists vs. statistical analysts
- **Quality control**: Multiple checkpoints in the research process
- **Academic standards**: Meets diverse institutional requirements

---

*Document Version: 1.0*  
*Date: August 2025*  
*Status: User Experience Design Complete*
