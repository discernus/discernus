# Discernus Reboot: Development Handoff Context

## 📋 **Project Status Summary**

The Discernus Reboot is a **Question-Driven Development** platform for narrative gravity analysis. We follow a systematic approach where each development cycle answers a specific researcher question.

### ✅ **Completed Research Questions (1-4)**

**Question #1**: Single text analysis → **COMPLETE** (`/analyze` endpoint)
**Question #2**: Two-text comparison → **COMPLETE** (`/compare` endpoint)  
**Question #3**: Group comparison → **COMPLETE** (`/compare-groups-direct`, `/analyze-corpus` endpoints)
**Question #4**: Distance metrics → **COMPLETE** (integrated into all comparison endpoints)

### 🎯 **Current Challenge: Research Question #5**
> *"Do different flagship cloud LLMs produce statistically similar results for a substantive text?"*

This question requires building **Statistical Comparison Infrastructure** - see `04_statistical_comparison_infrastructure.md` for the complete plan.

## 🏗️ **Current System Architecture**

### **Solid Foundation (All Working)**
- **Database**: PostgreSQL with proper schema and migrations
- **API**: FastAPI with comprehensive endpoints
- **Background Processing**: Celery with Redis
- **Testing**: 100% pass rate (10/10 tests) with mocking
- **CI/CD**: GitHub Actions with multi-Python testing (3.11, 3.12, 3.13)
- **LLM Gateway**: Multi-provider support (OpenAI, Anthropic, Mistral, Google AI, Ollama)

### **Key Directories**
```
src/reboot/
├── api/main.py              # FastAPI endpoints
├── database/
│   ├── models.py           # SQLAlchemy models
│   ├── session.py          # DB session management
│   └── alembic/            # Database migrations
├── engine/
│   ├── signature_engine.py # Coordinate calculations
│   └── prompt_engine.py    # Prompt generation
├── gateway/
│   ├── llm_gateway.py      # LLM interface
│   └── reboot_litellm_client.py # Multi-provider client
├── reporting/
│   ├── report_builder.py   # HTML report generation
│   └── reboot_plotly_circular.py # Visualizations
└── tasks.py                # Celery background tasks
```

## 🔧 **Development Environment**

### **Local Setup**
```bash
# Python environment
python3 -m venv venv-py313
source venv-py313/bin/activate
pip install -r requirements.txt

# Database
# PostgreSQL running locally on port 5432
# Database: discernus_reboot

# Environment variables (.env file)
REBOOT_DATABASE_URL=postgresql://postgres:postgres@localhost:5432/discernus_reboot
REDIS_URL=redis://localhost:6379/0
SQL_DEBUG=false

# Services
# Redis: localhost:6379
# Celery worker: celery -A src.reboot.tasks worker --loglevel=info
# FastAPI server: uvicorn src.reboot.api.main:app --reload
```

### **Testing & CI**
```bash
# Run tests locally
python -m pytest tests/reboot/ -v

# Check CI status
python3 scripts/check_ci_status.py

# Database migrations
python3 scripts/run_reboot_migration.py
```

## 📊 **Current Database Schema**

### **Existing Tables**
```sql
-- Current schema (working but limited)
reboot_analysis_jobs (
    id UUID PRIMARY KEY,
    status VARCHAR(20),
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);

reboot_analysis_results (
    id SERIAL PRIMARY KEY,
    job_id UUID REFERENCES reboot_analysis_jobs(id),
    centroid_x FLOAT,
    centroid_y FLOAT,
    scores TEXT, -- JSON string
    created_at TIMESTAMP
);
```

**Problem**: Schema is too specific for single/dual analysis. Needs to be generalized for statistical comparisons.

## 🎯 **Next Steps: Statistical Comparison Infrastructure**

The complete plan is in `04_statistical_comparison_infrastructure.md`. Here's the priority order:

### **Phase 1: Generic Database Schema (CRITICAL)**
**Why First**: Everything else builds on this foundation
**Tasks**:
1. Design new generic schema (detailed in plan document)
2. Create Alembic migration
3. Migrate existing data
4. Update SQLAlchemy models

### **Phase 2: Statistical Method Registry**
**Core Methods Needed**:
- Geometric similarity (centroid distance)
- Dimensional correlation (score-based)
- Confidence intervals
- Significance testing

### **Phase 3: Generic Comparison API**
**New Endpoint**: `/compare-statistical`
**Handles**: Multi-model, multi-framework, multi-run, temporal comparisons

## 🧠 **Key Insights for Next Developer**

### **1. Question-Driven Development Philosophy**
- Every feature serves a specific research question
- Build infrastructure that answers the **pattern**, not just the specific question
- Research Question #5 is part of a larger "statistical comparison" pattern

### **2. System Design Principles**
- **Modular**: Each component is isolated and testable
- **Generic**: Build for the pattern, not the specific use case
- **Persistent**: PostgreSQL for all data, no temporary files
- **Tested**: Every feature has comprehensive tests with mocking

### **3. Technical Architecture**
- **FastAPI**: Async endpoints with proper error handling
- **PostgreSQL**: Single source of truth for all data
- **Celery**: Background processing for long-running tasks
- **LiteLLM**: Multi-provider LLM access with consistent interface

### **4. Development Workflow**
1. **Plan First**: Document the approach before coding
2. **Test-Driven**: Write tests alongside implementation
3. **Incremental**: Each phase should be fully working before next
4. **CI Integration**: All changes go through GitHub Actions

## 🔍 **Critical Implementation Details**

### **Database Migration Strategy**
- Create new tables alongside existing ones
- Gradual migration with rollback capability
- Validate data integrity throughout process

### **Statistical Methods**
- Must be academically sound and peer-reviewable
- Implement confidence intervals and significance testing
- Configurable thresholds for similarity classification

### **API Design**
- Single endpoint handles all comparison types
- Flexible request/response schemas
- Proper error handling and validation

### **Testing Strategy**
- Mock all LLM calls for fast, free tests
- Test statistical calculations with known datasets
- Integration tests for full workflows

## 🚨 **Important Constraints & Considerations**

### **Performance**
- Multi-model comparisons can be expensive (multiple LLM calls)
- Implement async processing and result caching
- Consider rate limiting and cost management

### **Statistical Validity**
- Thresholds need empirical validation
- Methods must be academically defensible
- Clear documentation of what "statistically similar" means

### **Scalability**
- Infrastructure should support future comparison types
- Pluggable statistical methods
- Configuration-driven experiments

## 📚 **Key Files to Understand**

### **Must Read**
1. `src/reboot/pm/02_development_methodology.md` - Question-driven approach
2. `src/reboot/pm/03_mvp_plan.md` - Current system capabilities
3. `src/reboot/pm/04_statistical_comparison_infrastructure.md` - Next phase plan

### **Core Implementation**
1. `src/reboot/api/main.py` - Current endpoints
2. `src/reboot/database/models.py` - Database schema
3. `src/reboot/gateway/llm_gateway.py` - LLM interface
4. `src/reboot/engine/signature_engine.py` - Coordinate calculations

### **Testing & CI**
1. `tests/reboot/api/test_main.py` - Test suite
2. `.github/workflows/ci.yml` - CI/CD pipeline
3. `scripts/run_reboot_migration.py` - Database migration

## 💡 **Success Metrics**

### **Research Question #5 Success**
- [ ] System can compare 3+ LLMs on same text
- [ ] Statistical similarity determination with confidence levels
- [ ] Visual reports showing model agreement/disagreement
- [ ] Quantitative metrics (correlation, distance, significance)

### **Infrastructure Success**
- [ ] New comparison types can be added without core changes
- [ ] Statistical methods are pluggable and extensible
- [ ] Database schema supports any comparison pattern
- [ ] Single API endpoint handles all comparison types

### **Quality Assurance**
- [ ] All functionality covered by tests
- [ ] CI/CD validates statistical calculations
- [ ] Performance benchmarks for large comparisons
- [ ] Documentation for researchers and developers

## 🎯 **Recommended Starting Point**

**Start with Phase 1: Generic Database Schema**

1. Read the complete plan in `04_statistical_comparison_infrastructure.md`
2. Design the new schema based on the SQL provided
3. Create Alembic migration files
4. Test migration with existing data
5. Update SQLAlchemy models

This foundation enables everything else. The statistical methods and API can be developed in parallel once the schema is ready.

## 🤝 **Handoff Notes**

- **CI/CD is working**: All tests pass, GitHub Actions validates everything
- **Database is stable**: PostgreSQL with proper migrations
- **LLM Gateway is robust**: Supports multiple providers reliably
- **Documentation is current**: All plans and architecture docs are up-to-date
- **Testing is comprehensive**: 100% pass rate with proper mocking

The system is in excellent shape for implementing the Statistical Comparison Infrastructure. The foundation is solid, the plan is detailed, and the path forward is clear.

**Good luck building the future of narrative gravity analysis! 🚀** 