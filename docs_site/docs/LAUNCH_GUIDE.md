# Discernus - Backend Services Launch Guide

## Quick Start

### Launch All Backend Services (Recommended)
```bash
python launch.py
```
This starts:
- 🗄️ Database connectivity check
- 🌐 API Server at http://localhost:8000
- 📚 API Documentation at http://localhost:8000/api/docs
- 🔄 Celery Worker for background processing

**Note**: Frontend interfaces have been archived. Focus is on backend research pipeline.

### Launch Individual Services

#### Just the API Server
```bash
python launch.py --api-only
```

#### Just Background Processing
```bash
python launch.py --celery-only
```

### Database Setup

#### Check Database Status
```bash
python check_database.py
```

#### Initial Database Setup (PostgreSQL)
```bash
python launch.py --setup-db
```

#### Database Type Clarification
- **PostgreSQL**: Primary database for all application data
- **SQLite**: Only used for testing and logging fallback
- See `docs/architecture/database_architecture.md` for complete details

## Service Architecture

### Port Allocation
- **8000**: FastAPI Server (REST API + Documentation)
- **5432**: PostgreSQL Database (Default)
- **6379**: Redis (Celery Backend, if used)

### Service Dependencies
- **API Server**: Requires PostgreSQL database
- **Celery Worker**: Requires database for task management
- **Research Pipeline**: All backend services working together

## Research Workflow Integration

### Academic Analysis Pipeline
```bash
# 1. Launch backend services
python launch.py

# 2. Use CLI tools for research (requires PYTHONPATH)
PYTHONPATH=src python scripts/framework_sync.py status
PYTHONPATH=src python scripts/intelligent_ingest.py /path/to/corpus/
PYTHONPATH=src python scripts/export_academic_data.py --study-name my_research

# 3. Production experiment execution (validated workflow)
PYTHONPATH=src python3 scripts/production/comprehensive_experiment_orchestrator.py \
    research_workspaces/my_workspace/experiments/my_study.yaml --force-reregister

# 4. Access API documentation
# Open http://localhost:8000/api/docs
```

## Troubleshooting

### Import Path Issues (Common)
**Problem:** `No module named 'src'` or `No module named 'scripts'` errors

**Solution:**
```bash
# Set PYTHONPATH for all operations
export PYTHONPATH=src
# Or use inline for specific commands
PYTHONPATH=src python scripts/some_script.py
```

**Background:** Import path technical debt affects multiple CLI tools and orchestrator components.

### Production Experiment Execution
**Validated Working Command:**
```bash
PYTHONPATH=src python3 scripts/production/comprehensive_experiment_orchestrator.py \
    research_workspaces/your_workspace/experiments/experiment.yaml --force-reregister
```

**Current Status:**
- ✅ Framework integration and orchestrator infrastructure working
- ✅ YAML unified architecture eliminates configuration mismatches  
- ⚠️ Enhanced analysis pipeline blocked by import path issues

### Port Already in Use
```bash
python launch.py --port 8002  # Use different port for API
```

### Database Connection Issues
```bash
python launch.py --setup-db   # Initialize database
python check_database.py     # Verify connection
```

### Missing Dependencies
```bash
pip install -r requirements.txt
source scripts/setup_dev_env.sh  # Setup development environment
```

### API Health Check
```bash
curl http://localhost:8000/health  # Check API status
```

## Development Workflow

1. **First Time Setup**:
   ```bash
   python launch.py --setup-db
   source scripts/setup_dev_env.sh
   ```

2. **Daily Research Development**:
   ```bash
   python launch.py                   # Full backend stack
   # Use CLI tools and API for research operations
   ```

3. **API Development**:
   ```bash
   python launch.py --api-only        # Just API server
   ```

4. **Background Task Development**:
   ```bash
   python launch.py --celery-only     # Just worker processes
   ```

## Archived Components

**Frontend interfaces have been moved to `archive/deprecated_interfaces/`:**
- Streamlit interface → `archive/streamlit_legacy/`
- React frontend → `archive/deprecated_interfaces/react_frontend/`  
- Chainlit chat → `archive/deprecated_interfaces/chainlit_interface/`

**Focus**: Core research pipeline completion before interface development.

## Production Research Workflow Status

### ✅ Validated Working Components (June 20, 2025)
- **Framework Integration:** YAML unified architecture eliminates configuration mismatches
- **Experiment Orchestrator:** Core infrastructure and transaction management working
- **LLM Connections:** OpenAI, Anthropic, Google AI operational
- **Asset Management:** Content-addressable storage with integrity verification
- **Intelligent Output Routing:** Research workspace experiments co-located with results

### ⚠️ Pending Technical Debt
- **Enhanced Analysis Pipeline:** Import path issues prevent completion
- **CLI Tools:** Most require `PYTHONPATH=src` for proper operation
- **Statistical Analysis:** Blocked by `scripts.` import path technical debt

### 🎯 Recommended Production Usage
```bash
# Current validated workflow for experiment execution
PYTHONPATH=src python3 scripts/production/comprehensive_experiment_orchestrator.py \
    research_workspaces/your_workspace/experiments/your_study.yaml --force-reregister
```

This validates framework architecture and orchestrator infrastructure while providing graceful degradation when enhanced analysis components have import issues. 