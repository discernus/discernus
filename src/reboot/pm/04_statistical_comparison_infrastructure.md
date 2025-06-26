# 04: Statistical Comparison Infrastructure Plan

## Executive Summary

This document outlines the infrastructure needed to transform the Discernus Reboot from a "single/dual analysis tool" into a "statistical comparison platform" that can answer Research Question #5 and all future questions following the multi-dimensional statistical comparison pattern.

## The Pattern Recognition

### Current Question #5
> *"Do different flagship cloud LLMs produce statistically similar results for a substantive text?"*

### Future Questions in This Pattern
- "Do local models produce statistically similar results to flagship cloud LLMs?"
- "Do LLMs produce statistically significant runs across multiple runs of the same experiment?"
- "What's the difference between framework A and framework B when analyzing the same text?"
- "How do results vary over time periods?"
- "How do different users' manual annotations compare to LLM results?"

### The Universal Pattern
**Multi-dimensional statistical comparison across different variables** - where we analyze the same content across different conditions (models, frameworks, runs, time, users) and determine statistical similarity/difference.

## Current System State (✅ Completed)

- **Solid Foundation**: PostgreSQL persistence, CI/CD pipeline, comprehensive test suite
- **LLM Gateway**: Multi-provider support (OpenAI, Anthropic, Mistral, Google AI, Ollama)
- **Core Functionality**: Single analysis, two-text comparison, group comparison, distance metrics
- **Visualization**: HTML report generation with circular plots
- **Statistical Foundation**: Coordinate calculation, distance metrics

## Infrastructure Requirements

### 1. Generic Database Schema (Phase 1)

**Problem**: Current schema is too specific to single/dual comparisons.

**Solution**: Generic analysis storage supporting any comparison type.

#### New Tables Design

```sql
-- Generic Analysis Jobs (replaces specific job types)
CREATE TABLE analysis_jobs (
    id UUID PRIMARY KEY,
    job_type VARCHAR(50), -- "single", "comparison", "multi_model", "multi_framework", "multi_run"
    configuration JSONB,  -- Flexible config for any job type
    status VARCHAR(20),
    created_at TIMESTAMP,
    completed_at TIMESTAMP
);

-- Generic Analysis Results (supports any analysis type)
CREATE TABLE analysis_results (
    id SERIAL PRIMARY KEY,
    job_id UUID REFERENCES analysis_jobs(id),
    
    -- Analysis Context (what was analyzed)
    text_content TEXT,
    text_identifier VARCHAR(255), -- For corpus analysis
    
    -- Analysis Configuration (how it was analyzed)
    model VARCHAR(100),
    framework VARCHAR(100),
    prompt_template VARCHAR(100),
    run_number INTEGER DEFAULT 1,
    
    -- Results (what we found)
    centroid_x FLOAT,
    centroid_y FLOAT,
    raw_scores JSONB,
    
    -- Metadata
    api_cost FLOAT,
    duration_seconds FLOAT,
    created_at TIMESTAMP
);

-- Statistical Comparisons (the new infrastructure)
CREATE TABLE statistical_comparisons (
    id UUID PRIMARY KEY,
    comparison_type VARCHAR(50), -- "multi_model", "multi_framework", "multi_run", "temporal"
    
    -- What's being compared
    source_job_ids UUID[], -- Array of job IDs being compared
    comparison_dimension VARCHAR(50), -- "model", "framework", "run_number", "time"
    
    -- Statistical Results
    similarity_metrics JSONB,
    significance_tests JSONB,
    confidence_intervals JSONB,
    
    -- Conclusions
    similarity_classification VARCHAR(50), -- "HIGHLY_SIMILAR", "DIFFERENT", etc.
    confidence_level FLOAT,
    
    created_at TIMESTAMP
);
```

#### Migration Strategy
1. Create new tables alongside existing ones
2. Migrate existing data to new generic format
3. Update application code to use new schema
4. Remove old tables after validation

### 2. Statistical Method Registry (Phase 2)

**Modular Statistical Analysis System**:

```python
class StatisticalMethodRegistry:
    """
    Registry of statistical comparison methods
    Allows adding new methods without changing core infrastructure
    """
    
    methods = {
        "geometric_similarity": GeometricSimilarityAnalyzer,
        "dimensional_correlation": DimensionalCorrelationAnalyzer, 
        "temporal_stability": TemporalStabilityAnalyzer,
        "framework_variance": FrameworkVarianceAnalyzer,
        "run_consistency": RunConsistencyAnalyzer
    }
    
    def analyze(self, method: str, data: List[AnalysisResult]) -> Dict:
        return self.methods[method].analyze(data)
```

#### Core Statistical Methods to Implement

**A. Geometric Similarity (Centroid-based)**:
- Euclidean distance between model centroids
- Mean distance, max distance, variance calculations
- Similarity scoring (inverse distance)

**B. Dimensional Correlation (Score-based)**:
- Pearson correlation across individual framework dimensions
- Cross-model agreement per dimension
- Statistical significance testing

**C. Confidence Intervals**:
- 95% confidence intervals for each condition's position
- Overlap analysis between conditions
- Statistical significance determination

**D. Classification Thresholds**:
```python
SIMILARITY_THRESHOLDS = {
    "geometric": {
        "highly_similar": 0.1,      # Centroids within 0.1 units
        "moderately_similar": 0.3,  # Centroids within 0.3 units  
        "dissimilar": 0.5           # Centroids > 0.5 units apart
    },
    "dimensional": {
        "high_correlation": 0.8,    # r > 0.8 across dimensions
        "moderate_correlation": 0.6, # r > 0.6 across dimensions
        "low_correlation": 0.4      # r < 0.4 across dimensions
    },
    "overall_agreement": {
        "statistically_similar": 0.7,    # Combined score > 0.7
        "moderately_similar": 0.5,       # Combined score 0.5-0.7
        "statistically_different": 0.3   # Combined score < 0.3
    }
}
```

### 3. Generic Comparison API (Phase 3)

**Single endpoint that handles all comparison patterns**:

```python
@app.post("/compare-statistical")
async def compare_statistical(request: StatisticalComparisonRequest):
    """
    Generic statistical comparison endpoint
    Handles: multi-model, multi-framework, multi-run, temporal, etc.
    """
    pass

class StatisticalComparisonRequest(BaseModel):
    comparison_type: str  # "multi_model", "multi_framework", "multi_run"
    
    # For multi-model: same text, different models
    text: Optional[str] = None
    models: Optional[List[str]] = None
    
    # For multi-framework: same text, different frameworks  
    frameworks: Optional[List[str]] = None
    
    # For multi-run: same text+model, multiple runs
    runs_per_condition: Optional[int] = None
    
    # For temporal: same conditions, different time periods
    time_periods: Optional[List[str]] = None
    
    # Generic configuration
    experiment_file_path: str = "experiments/reboot_mft_experiment.yaml"
    statistical_methods: List[str] = ["geometric", "dimensional", "correlation"]

class StatisticalComparisonResponse(BaseModel):
    job_id: str
    comparison_type: str
    similarity_classification: str  # "HIGHLY_SIMILAR", "MODERATELY_SIMILAR", "DIFFERENT"
    confidence_level: float
    
    # Detailed results
    condition_results: List[ConditionResult]  # Individual results per condition
    statistical_metrics: Dict[str, Any]
    significance_tests: Dict[str, Any]
    
    # Visualization
    report_url: str
```

### 4. Configuration-Driven Experiments (Phase 4)

**YAML templates for each comparison type**:

```yaml
# experiments/multi_model_comparison_template.yaml
name: "Multi-Model Statistical Comparison Template"
description: "Template for comparing any set of models statistically"

comparison:
  type: "multi_model"  # "multi_framework", "multi_run", "temporal"
  dimension: "model"   # What varies between conditions
  
  statistical_methods:
    - "geometric_similarity"
    - "dimensional_correlation" 
    - "significance_testing"
  
  thresholds:
    highly_similar: 0.8
    moderately_similar: 0.6
    statistically_different: 0.4

conditions:
  # Template that can be filled programmatically
  text: "${TEXT_TO_ANALYZE}"
  models: "${MODELS_TO_COMPARE}" 
  runs_per_model: 3
  
framework: "moral_foundations_theory"
prompt_template: "moral_foundations_analysis"
```

### 5. Visualization Infrastructure (Phase 5)

**Generic Multi-Dimensional Visualization**:

```python
class ComparisonVisualizer:
    """
    Generates visualizations for any type of statistical comparison
    """
    
    def generate_comparison_report(
        self,
        comparison_result: ComparisonResult,
        visualization_type: str = "auto"  # "overlay", "matrix", "temporal", "variance"
    ) -> str:
        """
        Auto-detects the best visualization based on comparison type
        """
        pass
```

**Visualization Types by Comparison**:
- **Multi-Model**: Overlay plot with different colors per model + confidence ellipses
- **Multi-Framework**: Matrix plot showing same text across different frameworks
- **Multi-Run**: Scatter plot showing consistency with error bars
- **Temporal**: Line plot showing changes over time
- **Multi-User**: Comparison matrix between human and LLM annotations

## System Architecture

```mermaid
graph TD
    subgraph "API Layer"
        A[/compare-statistical] --> B{Comparison Type Router}
    end
    
    subgraph "Comparison Engine"
        B --> C[Multi-Model Analyzer]
        B --> D[Multi-Framework Analyzer] 
        B --> E[Multi-Run Analyzer]
        B --> F[Temporal Analyzer]
    end
    
    subgraph "Statistical Infrastructure"
        C & D & E & F --> G[Statistical Method Registry]
        G --> H[Geometric Similarity]
        G --> I[Dimensional Correlation]
        G --> J[Significance Testing]
        G --> K[Confidence Intervals]
    end
    
    subgraph "Data Layer"
        H & I & J & K --> L[(Generic Analysis Results)]
        L --> M[(Statistical Comparisons)]
    end
    
    subgraph "Visualization"
        M --> N[Comparison Visualizer]
        N --> O[Multi-Model Overlay]
        N --> P[Framework Matrix]
        N --> Q[Temporal Trends]
        N --> R[Variance Analysis]
    end
```

## Implementation Phases

### Phase 1: Generic Database Schema (Week 1)
**Priority**: CRITICAL - Foundation for everything else
**Tasks**:
1. Design new generic schema
2. Create Alembic migration
3. Implement SQLAlchemy models
4. Create migration script from existing data
5. Update database session handling

**Deliverables**:
- New database schema deployed
- Existing data migrated
- Models updated in `src/reboot/database/models.py`

### Phase 2: Statistical Method Registry (Week 2)
**Priority**: HIGH - Core analytical capability
**Tasks**:
1. Create `StatisticalMethodRegistry` class
2. Implement geometric similarity analyzer
3. Implement dimensional correlation analyzer
4. Add significance testing framework
5. Create threshold configuration system

**Deliverables**:
- `src/reboot/analysis/statistical_methods.py`
- Unit tests for all statistical methods
- Configuration system for thresholds

### Phase 3: Generic Comparison API (Week 3)
**Priority**: HIGH - User-facing functionality
**Tasks**:
1. Create `/compare-statistical` endpoint
2. Implement request/response models
3. Add comparison type routing
4. Integrate statistical method registry
5. Add error handling and validation

**Deliverables**:
- New API endpoint in `src/reboot/api/main.py`
- Request/response schemas
- Integration tests

### Phase 4: Configuration-Driven Experiments (Week 4)
**Priority**: MEDIUM - Flexibility and scalability
**Tasks**:
1. Create YAML template system
2. Implement template variable substitution
3. Add experiment configuration validation
4. Create standard templates for each comparison type
5. Add programmatic experiment generation

**Deliverables**:
- Template system in `src/reboot/experiments/`
- Standard templates for all comparison types
- Configuration validation

### Phase 5: Visualization Infrastructure (Week 5)
**Priority**: MEDIUM - User experience
**Tasks**:
1. Extend existing report builder
2. Create comparison-specific visualizations
3. Add auto-detection of visualization type
4. Implement statistical summary tables
5. Add interactive elements

**Deliverables**:
- Enhanced `src/reboot/reporting/comparison_visualizer.py`
- New visualization templates
- Interactive statistical reports

## Success Criteria

### Research Question #5 Answered
- System can compare multiple LLMs on the same text
- Statistical similarity determination with confidence levels
- Visual reports showing model agreement/disagreement
- Quantitative metrics for model comparison

### Infrastructure Scalability
- New comparison types can be added without core changes
- Statistical methods are pluggable and extensible
- Database schema supports any comparison pattern
- API handles any comparison type through single endpoint

### Quality Assurance
- All new functionality covered by tests
- CI/CD pipeline validates statistical calculations
- Performance benchmarks for large comparisons
- Documentation for researchers and developers

## Risk Mitigation

### Technical Risks
- **Database Migration Complexity**: Implement gradual migration with rollback capability
- **Statistical Method Accuracy**: Validate against known datasets and academic literature
- **Performance with Large Comparisons**: Implement async processing and result caching

### Research Risks
- **Threshold Validation**: Test thresholds with domain experts and adjust based on empirical results
- **Statistical Significance**: Ensure methods are academically sound and peer-reviewable
- **Interpretation Accuracy**: Provide clear documentation of what "statistically similar" means

## Future Extensions

This infrastructure enables future research questions:
- **Multi-User Comparison**: Compare human annotations vs LLM results
- **Temporal Analysis**: Track how model results change over time
- **Cross-Domain Analysis**: Compare results across different text domains
- **Meta-Analysis**: Statistical comparison of comparison results
- **Quality Assessment**: Determine which models are most reliable for specific tasks

## Next Steps for Implementation

1. **Start with Phase 1**: Database schema is the foundation - everything builds on this
2. **Parallel Development**: Statistical methods can be developed alongside API work
3. **Incremental Testing**: Each phase should be fully tested before moving to next
4. **Documentation**: Maintain comprehensive documentation for future developers
5. **Validation**: Test with real research questions throughout development

This infrastructure transforms the Discernus Reboot from a specific analysis tool into a general statistical comparison platform that can answer any research question following the multi-dimensional comparison pattern. 