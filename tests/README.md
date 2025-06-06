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
```bash
# Individual integration tests
python tests/integration/test_auth_system.py
python tests/integration/test_api.py
python tests/integration/test_corpus_tools.py

# Comprehensive ingestion test
python tests/integration/final_ingestion_test.py
```

### **Unit Tests**
```bash
# Run unit tests with pytest
cd tests/unit
python -m pytest test_cli_tools.py -v
python -m pytest test_streamlit_app.py -v
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

### **Integration Test Coverage** ✅
- ✅ **Authentication System**: JWT tokens working
- ✅ **API Endpoints**: FastAPI responses validated
- ✅ **Corpus Processing**: Text ingestion operational
- ✅ **Job Processing**: Task queue functional
- ✅ **Database Operations**: PostgreSQL validated

### **Unit Test Coverage** ✅  
- ✅ **CLI Tools**: Framework manager functional
- ✅ **Streamlit Components**: Web interface operational

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