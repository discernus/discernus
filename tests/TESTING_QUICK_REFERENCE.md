# Testing Quick Reference

## 🚀 **Fast Testing Commands**

### **Run All Tests (Recommended)**
```bash
# All unit tests (fast, isolated)
python -m pytest tests/unit/ -v

# Integration tests not requiring API server (medium speed)
DATABASE_URL="sqlite:///test.db" python -m pytest tests/integration/test_api.py tests/integration/test_streamlit_integration.py tests/integration/test_cli_tools.py tests/integration/test_corpus_tools.py -v
```

### **Individual Test Categories**

**Unit Tests (Always use SQLite)**
```bash
python -m pytest tests/unit/test_crud.py -v
python -m pytest tests/unit/test_api_services.py -v  
python -m pytest tests/unit/test_analysis_tasks.py -v
python -m pytest tests/unit/test_celery_app.py -v
```

**Integration Tests - No Server Required**
```bash
# API/Schema validation
DATABASE_URL="sqlite:///test.db" python -m pytest tests/integration/test_api.py -v

# Streamlit app tests (includes fixed launch_app.py help mode)
python -m pytest tests/integration/test_streamlit_integration.py -v

# CLI tools tests
python -m pytest tests/integration/test_cli_tools.py -v

# Corpus tools tests
python -m pytest tests/integration/test_corpus_tools.py -v
```

**Integration Tests - Require Live API Server**
```bash
# Terminal 1: Start API server
python scripts/run_api.py

# Terminal 2: Run server-dependent tests
python -m pytest tests/integration/test_auth_system.py -v
python -m pytest tests/integration/final_ingestion_test.py -v
python -m pytest tests/integration/test_job_processing.py -v
```

## 📊 **Current Test Status**

- ✅ **Unit Tests**: 100% passing with SQLite
- ✅ **Integration (No Server)**: 17/20 passing 
- ⚠️ **Integration (With Server)**: Requires live API + PostgreSQL

## 🔧 **Database Configuration**

| Test Type | Default DB | Alternative |
|-----------|------------|-------------|
| Unit Tests | SQLite (in-memory) | N/A |
| Integration Tests | SQLite (file) | PostgreSQL |
| Full System Tests | PostgreSQL | N/A |

## 🐛 **Common Issues & Solutions**

**Import Errors**
```bash
# Add project root to Python path
export PYTHONPATH=/Users/jeffwhatcott/narrative_gravity_analysis:$PYTHONPATH
```

**Database Connection Errors**
```bash
# Use SQLite for testing
DATABASE_URL="sqlite:///test.db" python -m pytest tests/integration/ -v
```

**API Server Not Running**
```bash
# Check if server is running
curl http://localhost:8000/api/health

# Start server if needed
python scripts/run_api.py
```

## 🎯 **Test Development Guidelines**

1. **Unit Tests**: Always use in-memory SQLite
2. **Integration Tests**: Default to SQLite, add PostgreSQL option
3. **New Tests**: Follow existing patterns in `tests/unit/` and `tests/integration/`
4. **Assertions**: Use `assert` statements, not `return` statements
5. **Fixtures**: Use pytest fixtures for database setup

---
*Updated: January 2025 - Testing Strategy v2.1* 