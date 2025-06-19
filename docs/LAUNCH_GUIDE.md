# Narrative Gravity Wells - Backend Services Launch Guide

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

# 2. Use CLI tools for research
python scripts/framework_sync.py status
python scripts/intelligent_ingest.py /path/to/corpus/
python scripts/export_academic_data.py --study-name my_research

# 3. Access API documentation
# Open http://localhost:8000/api/docs
```

## Troubleshooting

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

# Fix the narrative gravity reference
sed -i 's/Narrative Gravity Analysis/Discernus Framework Analysis/g' docs/product_management/20250617_enhanced_analysis_pipeline_specification.md 

cp docs/product_management/DAILY_TODO_2025_06_18.md docs/product_management/DAILY_TODO_2025_06_19.md
# Update date and reset task completion status 

mv docs/product_management/software_platform_restructuring_plan_option4.md docs/product_management/strategy/archived/ 

mkdir -p docs/product_management/strategy/archived/daily_todos/
mv docs/product_management/*TODO*2025_06_17*.md docs/product_management/strategy/archived/daily_todos/
mv docs/product_management/*todo*2025_06_17*.md docs/product_management/strategy/archived/daily_todos/ 

docs/product_management/
├── README.md                                    ← Updated ✅
├── CURRENT_ITERATION_DISCERNUS_MVP.md          ← Keep ✅
├── DAILY_TODO_2025_06_19.md                    ← Create new
├── BACKLOG.md                                   ← Update terminology
├── discernus_mvp_user_journeys.md              ← Keep ✅
├── mvp_single_framework_plan.md                ← Keep ✅
├── TECHNICAL_ARCHITECTURE_PLAN.md              ← Create (consolidate from specs)
│
├── strategy/
│   ├── archived/
│   │   ├── daily_todos/                        ← Archive old TODOs
│   │   └── software_platform_restructuring_plan_option4.md ← Archive
│   └── [current strategy docs]
├── futures/                                     ← Keep existing
└── visualization_references/                   ← Keep existing 