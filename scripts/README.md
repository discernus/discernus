# Operational Scripts

This directory contains startup and utility scripts for the Narrative Gravity Analysis system.

## 🚀 **Startup Scripts**

### **`run_api.py`** - FastAPI Server
```bash
python scripts/run_api.py
```
- **Purpose**: Starts the FastAPI web server for REST API access
- **Port**: http://localhost:8000
- **Documentation**: http://localhost:8000/api/docs
- **Features**: Auto-reload on code changes, development logging

### **`run_celery.py`** - Task Worker
```bash
python scripts/run_celery.py
```
- **Purpose**: Starts Celery worker for background task processing
- **Queues**: `analysis`, `celery` (default)
- **Features**: macOS-compatible pool settings, development logging

## 🛠️ **Utility Scripts**

### **`setup_database.py`** - Database Setup
```bash
python scripts/setup_database.py
```
- **Purpose**: Initial database setup and validation
- **Functions**: 
  - Creates PostgreSQL database if needed
  - Tests database connectivity
  - Sets up environment file from template
  - Provides migration guidance

## 🔄 **Usage Workflows**

### **Development Startup**
```bash
# 1. Setup database (first time only)
python scripts/setup_database.py

# 2. Run database migrations
alembic upgrade head

# 3. Start API server (Terminal 1)
python scripts/run_api.py

# 4. Start Celery worker (Terminal 2)  
python scripts/run_celery.py
```

### **Production Deployment**
```bash
# Database setup
python scripts/setup_database.py
alembic upgrade head

# Use production WSGI server instead of run_api.py
# Use production task queue manager instead of run_celery.py
```

## 📋 **Requirements**

### **Database Setup**
- PostgreSQL installed and running
- Database credentials in `.env` file
- Python database drivers: `psycopg2-binary`

### **API Server**
- FastAPI and dependencies
- Uvicorn ASGI server
- Source modules in `src/` directory

### **Celery Worker**
- Redis server running (for task queue)
- Celery and dependencies
- Access to analysis modules

## 🔧 **Configuration**

All scripts use project-relative imports and should be run from the project root:

```bash
# Correct - from project root
python scripts/run_api.py

# Incorrect - from scripts directory
cd scripts && python run_api.py  # Will fail
```

## 🚨 **Troubleshooting**

### **Database Issues**
```bash
# Check PostgreSQL is running
brew services list | grep postgresql

# Start PostgreSQL if needed
brew services start postgresql

# Create database manually if setup fails
createdb narrative_gravity
```

### **Import Errors**
```bash
# Ensure you're in project root
pwd  # Should show .../narrative_gravity_analysis

# Check Python path includes src/
python -c "import sys; print('src' in ' '.join(sys.path))"
```

### **Port Conflicts**
- **API Server**: Change port in `run_api.py` if 8000 is busy
- **Redis**: Default port 6379 must be available for Celery
- **PostgreSQL**: Default port 5432 must be available

---

*Scripts moved from root directory for better organization*  
*All functionality preserved with cleaner project structure* 