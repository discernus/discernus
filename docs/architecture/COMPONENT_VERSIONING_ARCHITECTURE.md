# Component Versioning System Guide

## Overview

The Component Versioning System implements systematic version control for the three core analysis components:

- **Prompt Templates**: Versioned prompt engineering with complete history
- **Framework Versions**: Evolution tracking of framework definitions  
- **Weighting Methodologies**: Mathematical approaches for narrative positioning

This system enables the validation-first research platform by providing:
- Complete provenance tracking for all analysis components
- Systematic development workflows with hypothesis tracking
- Component compatibility validation
- Reproducible research configurations

## Database Architecture

### Core Tables

#### `prompt_templates`
Stores versioned prompt templates with performance tracking:

```sql
CREATE TABLE prompt_templates (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    version VARCHAR(20) NOT NULL,
    template_content TEXT NOT NULL,
    template_type VARCHAR(20) DEFAULT 'standard',
    description TEXT,
    created_by INTEGER REFERENCES user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    parent_version_id VARCHAR(36) REFERENCES prompt_templates(id),
    usage_count INTEGER DEFAULT 0,
    success_rate FLOAT,
    average_cost FLOAT,
    validation_status VARCHAR(20) DEFAULT 'draft'
);
```

#### `framework_versions`
Tracks framework evolution with complete configuration:

```sql
CREATE TABLE framework_versions (
    id VARCHAR(36) PRIMARY KEY,
    framework_name VARCHAR(100) NOT NULL,
    version VARCHAR(20) NOT NULL,
    dipoles_json JSON NOT NULL,
    framework_json JSON NOT NULL,
    weights_json JSON NOT NULL,
    description TEXT,
    created_by INTEGER REFERENCES user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    parent_version_id VARCHAR(36) REFERENCES framework_versions(id),
    usage_count INTEGER DEFAULT 0,
    average_coherence FLOAT,
    framework_fit_average FLOAT,
    validation_status VARCHAR(20) DEFAULT 'draft'
);
```

#### `weighting_methodologies`
Mathematical algorithms for narrative positioning:

```sql
CREATE TABLE weighting_methodologies (
    id VARCHAR(36) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    version VARCHAR(20) NOT NULL,
    algorithm_description TEXT NOT NULL,
    mathematical_formula TEXT,
    algorithm_type VARCHAR(50) NOT NULL,
    parameters_json JSON NOT NULL,
    created_by INTEGER REFERENCES user(id),
    created_at TIMESTAMP DEFAULT NOW(),
    parent_version_id VARCHAR(36) REFERENCES weighting_methodologies(id),
    usage_count INTEGER DEFAULT 0,
    validation_status VARCHAR(20) DEFAULT 'draft'
);
```

#### `component_compatibility`
Compatibility matrix for component combinations:

```sql
CREATE TABLE component_compatibility (
    id VARCHAR(36) PRIMARY KEY,
    prompt_template_id VARCHAR(36) REFERENCES prompt_templates(id),
    framework_id VARCHAR(36) REFERENCES framework_versions(id),
    weighting_method_id VARCHAR(36) REFERENCES weighting_methodologies(id),
    compatibility_score FLOAT,
    validation_status VARCHAR(20) DEFAULT 'untested',
    test_run_count INTEGER DEFAULT 0,
    successful_runs INTEGER DEFAULT 0,
    validated_at TIMESTAMP,
    UNIQUE(prompt_template_id, framework_id, weighting_method_id)
);
```

#### `development_sessions`
Structured development workflow tracking:

```sql
CREATE TABLE development_sessions (
    id VARCHAR(36) PRIMARY KEY,
    session_name VARCHAR(255) NOT NULL,
    component_type VARCHAR(50) NOT NULL,
    component_name VARCHAR(100) NOT NULL,
    hypothesis TEXT,
    researcher INTEGER REFERENCES user(id),
    status VARCHAR(20) DEFAULT 'active',
    iteration_log JSON NOT NULL DEFAULT '[]',
    test_results JSON NOT NULL DEFAULT '{}',
    success_metrics JSON NOT NULL DEFAULT '{}',
    created_version_id VARCHAR(36),
    started_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP
);
```

### Foreign Key Integration

The `experiment` and `run` tables have been updated with foreign key references:

```sql
-- Added to experiment table
ALTER TABLE experiment ADD COLUMN prompt_template_version_id VARCHAR(36) REFERENCES prompt_templates(id);
ALTER TABLE experiment ADD COLUMN framework_version_id VARCHAR(36) REFERENCES framework_versions(id);
ALTER TABLE experiment ADD COLUMN weighting_method_version_id VARCHAR(36) REFERENCES weighting_methodologies(id);

-- Added to run table  
ALTER TABLE run ADD COLUMN prompt_template_version_id VARCHAR(36) REFERENCES prompt_templates(id);
ALTER TABLE run ADD COLUMN framework_version_id VARCHAR(36) REFERENCES framework_versions(id);
ALTER TABLE run ADD COLUMN weighting_method_version_id VARCHAR(36) REFERENCES weighting_methodologies(id);
```

## CLI Management Tool

### Installation

The component manager CLI is available at:
```bash
python src/narrative_gravity/cli/component_manager.py
```

### Commands

#### List Components
```bash
# List all components
python src/narrative_gravity/cli/component_manager.py list

# List specific component type
python src/narrative_gravity/cli/component_manager.py list --type prompt
python src/narrative_gravity/cli/component_manager.py list --type framework
python src/narrative_gravity/cli/component_manager.py list --type weighting
```

#### Create Prompt Template
```bash
python src/narrative_gravity/cli/component_manager.py create-prompt \
    "civic_virtue_enhanced" \
    "2.2.0" \
    "templates/civic_virtue_enhanced.txt" \
    --description "Enhanced civic virtue template with better reasoning"
```

#### Create Framework Version
```bash
python src/narrative_gravity/cli/component_manager.py create-framework \
    "civic_virtue" \
    "2.2.0" \
    "frameworks/civic_virtue/config_v2_2_0.json" \
    --description "Updated dipole weights based on validation study"
```

#### Create Weighting Methodology
```bash
python src/narrative_gravity/cli/component_manager.py create-weighting \
    "exponential_decay" \
    "1.0.0" \
    "exponential" \
    "Exponential decay weighting for narrative prominence" \
    --formula "weight = exp(-decay_rate * rank)" \
    --parameters '{"decay_rate": 0.5, "min_weight": 0.1}'
```

#### Export Components
```bash
# Export for sharing or backup
python src/narrative_gravity/cli/component_manager.py export \
    framework "civic_virtue" "2.1.0" "civic_virtue_v2_1_0.json"
```

## Development Workflows

### Systematic Component Development

1. **Start Development Session**
   ```python
   session = DevelopmentSession(
       session_name="improve_civic_virtue_coherence",
       component_type="framework",
       component_name="civic_virtue",
       hypothesis="Adjusting dipole weights will improve coherence scores",
       base_version="2.1.0",
       target_version="2.2.0"
   )
   ```

2. **Iterate and Test**
   - Create component variations using Claude/GPT-4
   - Test with validation datasets
   - Track performance metrics
   - Document iteration decisions

3. **Validate Component Combinations**
   ```bash
   python src/narrative_gravity/cli/component_manager.py validate-compatibility \
       "<prompt_id>" "<framework_id>" "<weighting_id>"
   ```

4. **Performance Tracking**
   - Usage counts automatically updated
   - Success rates calculated from run results
   - Average costs tracked for optimization

### Best Practices

#### Version Naming
- **Semantic versioning**: `MAJOR.MINOR.PATCH`
- **Major**: Breaking changes or complete rewrites
- **Minor**: New features or significant improvements
- **Patch**: Bug fixes or minor adjustments

#### Component Design
- **Prompt Templates**: Include clear instructions and examples
- **Frameworks**: Maintain mathematical rigor in dipole definitions
- **Weighting**: Document mathematical foundations and assumptions

#### Validation Process
1. **Unit Testing**: Individual component functionality
2. **Integration Testing**: Component combination compatibility  
3. **Validation Studies**: Performance against known datasets
4. **Academic Review**: Theoretical soundness verification

## Migration Status

### Completed
✅ Database schema implemented with foreign keys  
✅ Component versioning tables populated  
✅ All experiments (16) migrated to component references  
✅ All runs (26) migrated to component references  
✅ CLI management tool created  
✅ Foreign key constraints enforced  

## Clean Component Architecture 

### 🎯 **UPDATED: Clean Separation of Concerns**

The system now implements **clean architectural separation** where each component type has distinct responsibilities and independent lifecycles:

#### 🔧 **Prompt Templates** (LLM Optimization Layer)
Framework-agnostic prompt engineering focused purely on LLM performance optimization.

**Naming Convention**: `{analysis_approach}_{version}`
- `hierarchical_analysis v2.1.0` - Ranking, weighting, and evidence extraction
- `traditional_analysis v2.1.0` - Comprehensive dimensional scoring  
- `evidence_based_analysis v1.0` - Evidence + justification workflows

**Key Principle**: Prompt templates are optimized for LLM response quality and are **completely independent** of theoretical frameworks.

#### 🏗️ **Framework Versions** (Theoretical Constructs Layer)  
Pure theoretical definitions of narrative space including dipoles and conceptual relationships.

**Naming Convention**: `{theoretical_framework}_{version}`  
- `civic_virtue v2.1.0` - Dignity/Truth/Justice dipoles with civic engagement focus
- `moral_foundations v1.0` - Haidt's moral foundations framework
- `political_spectrum v1.0` - Traditional left/right political positioning

**Key Principle**: Frameworks evolve based on theoretical development, completely separate from prompt engineering.

#### ⚖️ **Weighting Methodologies** (Mathematical Interpretation Layer)
Mathematical algorithms for interpreting scores and generating meaningful visualizations.

**Naming Convention**: `{mathematical_approach}_{version}`
- `hierarchical_weighted v2.1.0` - Primary/secondary/tertiary importance (45%/35%/20%)
- `linear_traditional v2.1.0` - Equal weight averaging across all dimensions
- `attention_focused v1.0` - Dynamic weighting based on salience detection

**Key Principle**: Weighting methodologies evolve based on visualization effectiveness and analytical requirements.

### Current Component Inventory
- **Prompt Templates**: 4 versions (CLEAN ARCHITECTURE ✅)
  - `hierarchical_analysis v2.1.0` (production - framework agnostic)
  - `traditional_analysis v2.1.0` (production - framework agnostic)
  - `civic_virtue_hierarchical v2.1.0` (deprecated - conflated naming)
  - `test_hierarchical vv1.0` (testing)

- **Framework Versions**: 2 versions (PROPERLY NAMED ✅)
  - `civic_virtue v2.1.0` (production)
  - `test_civic_virtue vv1.0` (testing)

- **Weighting Methodologies**: 3 versions (PROPERLY NAMED ✅)
  - `hierarchical_weighted v2.1.0` (production)
  - `linear_traditional v2.1.0` (production)
  - `test_winner_take_most vv1.0` (testing)

**Migration Status**: ✅ All 16 experiments successfully migrated to clean architecture

## Integration with Research Platform

### Experiment Creation
New experiments automatically reference specific component versions:

```python
experiment = Experiment(
    name="Lincoln Speech Analysis",
    prompt_template_version_id="<uuid>",
    framework_version_id="<uuid>",
    weighting_method_version_id="<uuid>"
)
```

### Provenance Tracking
Complete component lineage tracked in run records:

```python
run = Run(
    experiment_id=experiment.id,
    prompt_template_version_id=experiment.prompt_template_version_id,
    framework_version_id=experiment.framework_version_id,
    weighting_method_version_id=experiment.weighting_method_version_id,
    component_provenance={
        "prompt_version": "civic_virtue_hierarchical v2.1.0",
        "framework_version": "civic_virtue v2.1.0", 
        "weighting_version": "hierarchical_weighted v2.1.0"
    }
)
```

### Academic Export
Component versions included in academic data exports for reproducibility:

```json
{
  "analysis_metadata": {
    "prompt_template": {
      "name": "civic_virtue_hierarchical",
      "version": "2.1.0",
      "id": "uuid-here"
    },
    "framework": {
      "name": "civic_virtue", 
      "version": "2.1.0",
      "id": "uuid-here"
    },
    "weighting_methodology": {
      "name": "hierarchical_weighted",
      "version": "2.1.0", 
      "id": "uuid-here"
    }
  }
}
```

## Next Steps

1. **CLI Orchestration Tools**: Batch analysis management
2. **Validation Testing**: Systematic component testing framework
3. **Performance Monitoring**: Real-time component performance tracking
4. **Academic Integration**: Enhanced export capabilities for publications

This component versioning system provides the foundation for systematic, reproducible research with complete provenance tracking and validation capabilities. 