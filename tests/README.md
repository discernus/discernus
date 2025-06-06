# Test Suite Documentation

## 📁 Test Organization

The test suite is organized into clear categories for different types of testing:

```
tests/
├── integration/          # Integration tests for full system workflows
├── unit/                 # Unit tests for individual components  
├── utilities/            # Utility scripts and validation tools
├── test_data/            # Test data files and sample corpora
├── test_results/         # Test output and validation results
└── README.md            # This documentation
```

## 🧪 Test Categories

### **Integration Tests** (`integration/`)

Full system integration tests that verify end-to-end workflows:

- **`test_auth_system.py`** - Authentication and JWT token system validation
- **`test_api.py`** - FastAPI endpoints and request/response validation  
- **`test_corpus_tools.py`** - Corpus ingestion and processing workflows
- **`test_ingestion.py`** - Text ingestion and database storage validation
- **`test_job_processing.py`** - Celery task queue and job processing
- **`final_ingestion_test.py`** - Comprehensive ingestion system validation

### **Unit Tests** (`unit/`)

Individual component tests:

- **`test_cli_tools.py`** - Framework manager and CLI tool tests
- **`test_streamlit_app.py`** - Streamlit interface component tests

### **Utility Scripts** (`utilities/`)

Development and validation utilities:

- **`run_epic_validation.py`** - Epic 1 validation suite (Task Queue, HuggingFace, Retry Logic, Golden Set)
- **`align_formats.py`** - CSV format alignment and validation utility
- **`check_corpus5.py`** - Quick corpus validation check
- **`check_docs.py`** - Documentation completeness validation
- **`quick_test.py`** - Fast system health check

## 📊 Test Data

### **Sample Datasets** (`test_data/`)
- **`sample_corpus.jsonl`** - Original sample corpus for testing
- **`sample_corpus_v2.jsonl`** - Updated sample corpus format

### **Test Results** (`test_results/`)
- Contains output from Epic validation runs
- Stores integration test results for analysis
- Performance benchmark data

## 🚀 Running Tests

### **Database Configuration for Tests**

Integration tests use **SQLite** by default for faster, isolated testing:

```bash
# SQLite (recommended for testing)
DATABASE_URL="sqlite:///test.db" python -m pytest tests/integration/ -v

# PostgreSQL (for production-like testing)
DATABASE_URL="postgresql://user:pass@localhost:5432/test_db" python -m pytest tests/integration/ -v
```

### **Quick System Check**
```bash
# Fast health check
python tests/utilities/quick_test.py

# Documentation validation
python tests/utilities/check_docs.py
```

### **Epic Validation Suite**
```bash
# Complete Epic 1 validation (4 test categories)
python tests/utilities/run_epic_validation.py
```

### **Integration Tests**

**Option 1: Using SQLite (Recommended)**
```bash
# All integration tests with SQLite
DATABASE_URL="sqlite:///test.db" python -m pytest tests/integration/ -v

# Individual tests with SQLite
DATABASE_URL="sqlite:///test.db" python -m pytest tests/integration/test_api.py -v
DATABASE_URL="sqlite:///test.db" python -m pytest tests/integration/test_streamlit_integration.py -v
DATABASE_URL="sqlite:///test.db" python -m pytest tests/integration/test_cli_tools.py -v
```

**Option 2: Tests Not Requiring Database**
```bash
# API import/schema tests (no database needed)
python -m pytest tests/integration/test_api.py -v
python -m pytest tests/integration/test_streamlit_integration.py -v
python -m pytest tests/integration/test_corpus_tools.py -v
```

**Option 3: Tests Requiring Live API Server**
```bash
# Start API server first (in another terminal)
python scripts/run_api.py

# Then run tests requiring live API
python tests/integration/test_auth_system.py
python tests/integration/final_ingestion_test.py
python tests/integration/test_job_processing.py
```

### **Unit Tests**
```bash
# Run unit tests with pytest (use SQLite by default)
python -m pytest tests/unit/ -v

# Individual unit test files
python -m pytest tests/unit/test_crud.py -v
python -m pytest tests/unit/test_api_services.py -v
python -m pytest tests/unit/test_analysis_tasks.py -v
```

### **Utility Tools**
```bash
# Format alignment
python tests/utilities/align_formats.py

# Corpus validation
python tests/utilities/check_corpus5.py
```

## ✅ Test Status

### **Epic 1 Validation** ✅ (4/4 Success)
- ✅ **Task Queue Processing**: Celery + Redis operational
- ✅ **HuggingFace Integration**: All 3 frameworks loaded
- ✅ **Retry Logic**: Error handling validated
- ✅ **Golden Set Testing**: 17 presidential speeches validated

### **Integration Test Coverage** ✅ (30/31 passing - 97%)
- ✅ **API Import/Schema Tests**: FastAPI components validated (3/3)
- ✅ **Streamlit Integration**: App startup and CLI tools (5/6)
- ✅ **CLI Tools**: Framework management (9/9) 
- ✅ **Corpus Tools**: Schema and JSONL generation (2/2)
- ✅ **Authentication System**: Live API testing (7/7)
- ✅ **Job Processing**: Task queue integration (1/1)
- ✅ **Ingestion Workflow**: JSONL processing (2/2)
- ✅ **Full End-to-End**: Complete workflow validation (1/1)

### **Unit Test Coverage** ✅ (151/151 passing - 100%)
- ✅ **Database Operations**: CRUD operations with SQLite (19/19)
- ✅ **API Services**: Text ingestion and processing (9/9)
- ✅ **Task Processing**: Celery task logic with mocking (3/3)
- ✅ **Authentication**: JWT and security utilities (6/6)
- ✅ **Framework Management**: CLI and prompt generation (12/12)
- ✅ **Data Processing**: Sanitization, logging, costs (102/102)

### **Database Testing Strategy** 🔄
- **Unit Tests**: Use in-memory SQLite for fast isolation
- **Integration Tests**: SQLite by default, PostgreSQL optional
- **Full System Tests**: Require PostgreSQL + live API server

## �� Test Maintenance

### **Adding New Tests**
1. **Integration Tests**: Add to `integration/` for full workflow tests
2. **Unit Tests**: Add to `unit/` for component-specific tests  
3. **Utilities**: Add to `utilities/` for development tools

### **Test Data Management**
- Place sample data in `test_data/`
- Store results in `test_results/`
- Use descriptive naming conventions

### **Running Full Test Suite**
```bash
# Epic validation (comprehensive)
python tests/utilities/run_epic_validation.py

# Quick health check
python tests/utilities/quick_test.py

# Integration tests (all)
for test in tests/integration/*.py; do python "$test"; done
```

---

## 📈 Test Philosophy

Our testing approach prioritizes:

1. **End-to-End Validation**: Epic tests verify complete workflows
2. **Component Isolation**: Unit tests verify individual functions
3. **Real-World Data**: Golden set provides realistic validation
4. **Performance Monitoring**: Tests track system performance
5. **Academic Rigor**: Validation meets research standards

---

*Last Updated: January 2025*  
*Test Suite Version: v1.1 (Post-Cleanup)* 