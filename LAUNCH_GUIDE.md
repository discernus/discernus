# Narrative Gravity Wells - Launch Guide

## Quick Start

### Launch Everything (Recommended)
```bash
python launch.py
```
This starts:
- 🗄️ Database setup (if needed)
- 🌐 API Server at http://localhost:8000
- 📚 API Documentation at http://localhost:8000/api/docs
- 🔄 Celery Worker for background processing
- 🖥️ Streamlit UI at http://localhost:8501

### Launch Individual Services

#### Just the UI (No Database Required)
```bash
python launch.py --streamlit-only --no-db-check
```

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
- **8501**: Streamlit UI (Main Interface)
- **8000**: FastAPI Server (REST API)
- **5432**: PostgreSQL Database (Default)
- **6379**: Redis (Celery Backend, if used)

### Service Dependencies
- **Streamlit**: Can run standalone
- **API Server**: Requires database
- **Celery Worker**: Requires database and API
- **Full Platform**: All services working together

## Troubleshooting

### Port Already in Use
```bash
python launch.py --port 8502  # Use different port
```

### Database Connection Issues
```bash
python launch.py --setup-db   # Initialize database
```

### Missing Dependencies
```bash
pip install -r requirements.txt
```

### Legacy Access (Backward Compatibility)
```bash
python launch_streamlit.py    # Simple Streamlit-only launcher
```

## Development Workflow

1. **First Time Setup**:
   ```bash
   python launch.py --setup-db
   ```

2. **Daily Development**:
   ```bash
   python launch.py --streamlit-only  # UI development
   # OR
   python launch.py                   # Full stack development
   ```

3. **API Development**:
   ```bash
   python launch.py --api-only
   ```

4. **Background Task Development**:
   ```bash
   python launch.py --celery-only
   ``` 