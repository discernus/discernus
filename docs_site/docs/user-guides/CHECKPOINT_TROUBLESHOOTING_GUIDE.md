# Checkpoint System Troubleshooting Guide

*Understanding and resolving experiment checkpoint failures*

## Overview

The experiment orchestrator uses a **5-checkpoint validation system** to prevent expensive failures. Each checkpoint must pass before proceeding to the next phase.

## Checkpoint Flow

```
INITIALIZING → PRE_FLIGHT → API_CONNECTIVITY → COST_CONTROL → 
COMPONENT_REGISTRATION → ANALYSIS → QUALITY_VALIDATION → 
ENHANCED_PIPELINE → OUTPUT_VALIDATION → COMPLETED
```

## Common Checkpoint Failures

### 1. API Connectivity Validation

**Error**: `❌ API connectivity check failed`

**Common Causes**:
- Missing API keys in `.env` file
- Invalid API keys (expired/revoked)
- Network connectivity issues
- API service outages

**Solutions**:
```bash
# Check API keys are set
docker-compose exec app env | grep -E "(OPENAI|ANTHROPIC|MISTRAL)_API_KEY"

# Test connectivity manually
docker-compose exec app python3 -c "
from src.api_clients.direct_api_client import DirectAPIClient
client = DirectAPIClient()
print(client.test_connectivity())
"
```

### 2. Cost Control Validation

**Error**: `❌ Estimated cost $X.XX exceeds budget limit $Y.YY`

**Common Causes**:
- Large corpus size with expensive models
- High analysis matrix complexity
- Conservative budget limits

**Solutions**:
```bash
# Check current cost estimates
docker-compose exec app python3 scripts/utilities/estimate_experiment_cost.py

# Adjust budget in experiment definition
# OR reduce corpus size / model selection
```

### 3. Experiment Quality Validation

**Error**: `❌ Analysis success rate X% below minimum 30%`

**Common Causes**:
- Framework configuration issues
- Prompt template problems
- API rate limiting causing failures
- Corpus text quality issues

**Solutions**:
```bash
# Validate framework
docker-compose exec app python3 scripts/utilities/unified_framework_validator.py frameworks/your_framework.yaml

# Check recent analysis quality
docker-compose exec app python3 scripts/utilities/analyze_experiment_quality.py
```

### 4. Output Generation Validation

**Error**: `❌ Missing expected output files`

**Common Causes**:
- Enhanced pipeline generation failures
- Insufficient disk space
- Permission issues in output directories
- Template rendering errors

**Solutions**:
```bash
# Check disk space
docker-compose exec app df -h

# Validate output directory permissions
docker-compose exec app ls -la experiments/

# Test enhanced pipeline manually
docker-compose exec app python3 scripts/applications/enhanced_analysis_pipeline.py --test
```

### 5. Data Persistence Validation

**Error**: `❌ Run data not properly saved to database`

**Common Causes**:
- PostgreSQL connection issues
- Database schema problems
- Transaction rollback errors
- Insufficient database permissions

**Solutions**:
```bash
# Check database connectivity
docker-compose exec app python3 scripts/utilities/check_database.py

# Verify experiment data
docker-compose exec db psql -d discernus -U discernus -c "
SELECT id, state, created_at FROM experiments ORDER BY created_at DESC LIMIT 5;
SELECT experiment_id, COUNT(*) FROM runs GROUP BY experiment_id;
"
```

## Environment Validation

### Docker Environment Check

The orchestrator validates it's running in Docker:

**Error**: `❌ Not running in Docker environment`

**Solution**:
```bash
# Always use Docker for experiments
docker-compose up -d
docker-compose exec app python3 scripts/applications/comprehensive_experiment_orchestrator.py
```

### Database Environment Check

**Error**: `❌ Database not available for data persistence`

**Solution**:
```bash
# Ensure PostgreSQL container running
docker-compose up -d db

# Check connection
docker-compose exec app python3 -c "
from src.models.database import get_db_connection
conn = get_db_connection()
print('Database connected:', conn is not None)
"
```

## Debugging Techniques

### 1. Enable Detailed Logging

```bash
# Set debug logging level
export LOG_LEVEL=DEBUG
docker-compose exec app python3 scripts/applications/comprehensive_experiment_orchestrator.py
```

### 2. Manual Checkpoint Testing

```bash
# Test individual checkpoints
docker-compose exec app python3 -c "
from scripts.applications.comprehensive_experiment_orchestrator import ComprehensiveExperimentOrchestrator
orchestrator = ComprehensiveExperimentOrchestrator()
result = orchestrator._validate_api_connectivity()
print('API Connectivity:', result)
"
```

### 3. State Recovery

```bash
# Check experiment state
docker-compose exec db psql -d discernus -U discernus -c "
SELECT id, name, state, error_message FROM experiments 
WHERE state NOT IN ('COMPLETED', 'FAILED') 
ORDER BY updated_at DESC;
"
```

## Recovery Procedures

### Resume Failed Experiment

```bash
# Find failed experiment ID
docker-compose exec db psql -d discernus -U discernus -c "
SELECT id, name, state FROM experiments WHERE state = 'FAILED' ORDER BY updated_at DESC LIMIT 5;
"

# Resume from last checkpoint (if supported)
docker-compose exec app python3 scripts/applications/comprehensive_experiment_orchestrator.py --resume EXPERIMENT_ID
```

### Clean Failed Experiment

```bash
# Clean up failed experiment data
docker-compose exec app python3 scripts/utilities/cleanup_failed_experiment.py EXPERIMENT_ID
```

## Best Practices

### 1. Pre-Flight Checks
- Always run in Docker environment
- Verify API keys before starting
- Check available disk space
- Validate framework files

### 2. Cost Management  
- Review cost estimates before execution
- Use smaller test corpora for development
- Monitor API usage during experiments

### 3. Quality Assurance
- Validate frameworks before experiments  
- Test with small sample before full analysis
- Monitor QA confidence scores

## Getting Help

### 1. Check Logs
```bash
# View orchestrator logs
docker-compose logs app | grep -E "(ERROR|WARN|checkpoint)"
```

### 2. System Status
```bash
# Run system diagnostics
docker-compose exec app python3 scripts/utilities/system_diagnostics.py
```

### 3. Community Support
- Check project documentation: `docs_site/`
- Review existing issues: `product_management/BACKLOG.md`
- Create detailed issue reports with checkpoint error messages 