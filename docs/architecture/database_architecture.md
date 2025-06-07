# Database-First Architecture for Narrative Gravity Analysis

## Overview

The Narrative Gravity Analysis system now uses a **database-first architecture** designed specifically for academic research workflows and enterprise business intelligence tools. This addresses the critical need for comprehensive data logging and analysis capabilities.

## Key Improvements

### ✅ **What We Fixed**
- **Scattered JSON files** → **Single source of truth in database**
- **Limited SQLite** → **Enterprise PostgreSQL with SQLite fallback**
- **Missing raw responses** → **Complete LLM corpus capture**
- **Academic incompatibility** → **Native export to SPSS, R, Parquet**
- **No BI integration** → **Direct Looker/Tableau connectivity**

## Database Schema

### Core Tables

#### `jobs` - Multi-run Analysis Jobs
```sql
CREATE TABLE jobs (
    job_id TEXT PRIMARY KEY,
    speaker TEXT NOT NULL,
    speech_type TEXT NOT NULL,
    text_length INTEGER NOT NULL,
    framework TEXT NOT NULL,
    model_name TEXT NOT NULL,
    total_runs INTEGER NOT NULL,
    successful_runs INTEGER NOT NULL,
    total_cost DECIMAL(10,4) NOT NULL,
    total_duration_seconds DECIMAL(8,2) NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    mean_scores JSONB NOT NULL,  -- Average well scores
    variance_stats JSONB NOT NULL,  -- Variance analysis
    threshold_category TEXT NOT NULL  -- perfect/near_perfect/minimal/normal
);
```

#### `runs` - Individual LLM Analyses
```sql
CREATE TABLE runs (
    run_id TEXT PRIMARY KEY,
    job_id TEXT NOT NULL REFERENCES jobs(job_id),
    run_number INTEGER NOT NULL,
    well_scores JSONB NOT NULL,  -- All well scores
    narrative_position JSONB NOT NULL,  -- x,y coordinates
    analysis_text TEXT NOT NULL,  -- Processed analysis
    model_name TEXT NOT NULL,
    framework TEXT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cost DECIMAL(8,4) NOT NULL,
    duration_seconds DECIMAL(6,2) NOT NULL,
    success BOOLEAN NOT NULL,
    error_message TEXT,
    -- ENHANCED CORPUS CAPTURE
    raw_prompt TEXT,  -- Complete prompt sent to LLM
    raw_response TEXT,  -- Full unprocessed LLM response
    input_text TEXT,  -- Source text being analyzed
    model_parameters JSONB,  -- Temperature, max_tokens, etc.
    api_metadata JSONB  -- Request/response metadata
);
```

#### `variance_stats` - Academic Variance Analysis
```sql
CREATE TABLE variance_stats (
    id SERIAL PRIMARY KEY,
    job_id TEXT NOT NULL REFERENCES jobs(job_id),
    well_name TEXT NOT NULL,
    mean_score DECIMAL(6,4) NOT NULL,
    std_deviation DECIMAL(6,4) NOT NULL,
    variance DECIMAL(8,6) NOT NULL,
    score_category TEXT NOT NULL,  -- low/medium/high
    well_type TEXT NOT NULL  -- integrative/disintegrative
);
```

## Academic Export Capabilities

### Supported Formats

#### **CSV** - Universal compatibility
```python
# Export all data to CSV
files = logger.export_for_academics(export_format="csv")
# Creates: runs.csv, jobs.csv, variance.csv
```

#### **SPSS** - Statistical analysis (.sav files)
```python
# Export with proper variable labels
files = logger.export_for_academics(export_format="spss")
# Creates: narrative_gravity_TIMESTAMP.sav
```

#### **R** - Advanced statistics
```python
# Export with auto-generated analysis script
files = logger.export_for_academics(export_format="r")
# Creates: data.csv + analysis_script.R
```

#### **Parquet** - Data lakes & big data
```python
# Compressed columnar format for analytics
files = logger.export_for_academics(export_format="parquet")
# Creates: narrative_gravity_corpus_TIMESTAMP.parquet
```

### Sample Academic Workflow

```python
from src.utils.statistical_logger import StatisticalLogger

# Initialize with PostgreSQL preference
logger = StatisticalLogger(prefer_postgresql=True)

# Export all formats for comprehensive analysis
exports = logger.export_for_academics(
    export_format="all",
    output_dir="exports/research_2025/",
    include_raw_responses=True  # Full corpus
)

# Query specific subsets
claude_responses = logger.get_full_response_corpus(filters={
    'model_name': 'claude-3-5-sonnet-20241022',
    'speaker': 'Trump'
})

# Get corpus statistics
stats = logger.get_corpus_stats()
print(f"Total cost: ${stats['total_cost']:.4f}")
```

## Business Intelligence Integration

### Looker Connectivity
```yaml
connection: narrative_gravity_pg
host: localhost
database: narrative_gravity
schema: public
tables:
  - jobs
  - runs  
  - variance_stats
  - performance_metrics
```

### Key Dimensions & Measures
- **Dimensions**: speaker, model_name, framework, timestamp
- **Measures**: total_cost, success_rate, variance, duration  
- **Advanced**: JSONB queries on well_scores and parameters

### Sample Looker SQL
```sql
SELECT 
    speaker,
    model_name,
    AVG(total_cost) as avg_cost,
    AVG(successful_runs::float / total_runs) as success_rate,
    COUNT(*) as job_count
FROM jobs 
WHERE timestamp >= '2025-01-01'
GROUP BY speaker, model_name
ORDER BY success_rate DESC;
```

## Database Configuration

### PostgreSQL (Preferred)
```python
pg_config = {
    'host': 'localhost',
    'port': '5432', 
    'database': 'narrative_gravity',
    'user': 'postgres',
    'password': 'your_password'
}
logger = StatisticalLogger(pg_config=pg_config)
```

### Environment Variables
```bash
export DB_HOST=localhost
export DB_PORT=5432
export DB_NAME=narrative_gravity
export DB_USER=postgres
export DB_PASSWORD=your_password
```

### SQLite Fallback
If PostgreSQL is unavailable, the system automatically falls back to SQLite with reduced functionality.

## Migration from JSON Files

The system now eliminates scattered JSON output files:

### Before (Problematic)
```
model_output/
├── job_12345.json
├── job_67890.json
└── analysis_results/
    ├── dashboard_data.json
    └── variance_stats.json
```

### After (Clean)
```
PostgreSQL Database
├── Complete run data
├── Job metadata  
├── Variance statistics
└── Performance metrics
     ↓
All visualizations pull from DB
```

## Performance Optimizations

### Indexes for Analytics
```sql
CREATE INDEX idx_runs_job_id ON runs(job_id);
CREATE INDEX idx_runs_model_name ON runs(model_name);
CREATE INDEX idx_runs_timestamp ON runs(timestamp);
CREATE INDEX idx_jobs_speaker ON jobs(speaker);
CREATE INDEX idx_jobs_model_name ON jobs(model_name);
```

### JSONB Efficiency
- Well scores stored as JSONB for efficient querying
- Model parameters indexed for parameter analysis
- Native JSON operations in PostgreSQL

## Dependencies

### Required Python Packages
```txt
psycopg2-binary==2.9.9    # PostgreSQL driver
pandas==2.2.3             # DataFrame operations
pyreadstat==1.3.0         # SPSS/Stata support
fastparquet==2025.1.0     # Parquet support
scipy==1.15.1             # Scientific computing
scikit-learn==1.7.0       # Machine learning
```

## Usage Examples

### Initialize Logger
```python
from src.utils.statistical_logger import StatisticalLogger

# Auto-detect best database
logger = StatisticalLogger()

# Force PostgreSQL
logger = StatisticalLogger(prefer_postgresql=True)
```

### Export for Academics
```python
# All formats
exports = logger.export_for_academics(export_format="all")

# SPSS only
spss_file = logger.export_for_academics(export_format="spss")

# Include raw responses for corpus linguistics
full_corpus = logger.export_for_academics(
    export_format="csv",
    include_raw_responses=True
)
```

### Query Corpus
```python
# All Claude responses
claude_data = logger.get_full_response_corpus(filters={
    'model_name': 'claude-3-5-sonnet-20241022'
})

# High-cost analyses
expensive = logger.get_full_response_corpus(filters={
    'min_cost': 0.01
})

# Date range
recent = logger.get_full_response_corpus(filters={
    'date_range': ('2025-01-01', '2025-12-31')
})
```

## Benefits

### For Academics
- ✅ **Direct SPSS/R/Stata compatibility**
- ✅ **Complete raw response corpus**
- ✅ **Proper variable labels and metadata**
- ✅ **Auto-generated analysis scripts**

### For Enterprise
- ✅ **Looker/Tableau connectivity**
- ✅ **Data lake integration (Parquet)**
- ✅ **Scalable PostgreSQL backend**
- ✅ **Real-time dashboard capability**

### For Researchers
- ✅ **Single source of truth**
- ✅ **No more scattered JSON files**
- ✅ **Full LLM interaction history**
- ✅ **Advanced query capabilities**

This architecture transforms the Narrative Gravity system from a file-based tool into an enterprise-grade research platform suitable for academic publication and commercial deployment. 