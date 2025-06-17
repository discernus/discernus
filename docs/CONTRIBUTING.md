# Contributing to Narrative Gravity Wells

Thank you for contributing to the Narrative Gravity Wells project! This guide ensures consistent development practices.

## 🏗️ Project Organization Standards

### Root Directory Philosophy
Keep the root directory **minimal and operational**:

#### ✅ **Allowed in Root**
- **Operational files**: `README.md`, `CHANGELOG.md`, `LICENSE`
- **Launch tools**: `launch.py`, `launch_streamlit.py`, `check_database.py`
- **Configuration**: `requirements.txt`, `env.example`, `alembic.ini`, `pytest.ini`
- **Build/deploy**: `.gitignore`, `setup.py`

#### ❌ **NEVER in Root**
- Analysis results → `analysis_results/`
- Test files → `tests/`
- Utility scripts → `scripts/`
- Documentation → `docs/`
- Temporary files → `tmp/YYYY_MM_DD/`

### Documentation Organization
- **`docs/architecture/`**: System architecture documentation
- **`docs/user-guides/`**: End-user documentation
- **`docs/development/`**: Developer documentation (this file)
- **`docs/api/`**: API documentation
- **Root level**: Only operational guides (`LAUNCH_GUIDE.md`)

## 🗄️ Database Architecture (CRITICAL)

### Primary Rule: PostgreSQL for Everything
- **PRIMARY DATABASE**: PostgreSQL for ALL application data
- **SQLite**: ONLY for unit testing (in-memory) and logging fallback
- **Never assume SQLite** for main application functionality

### Database Usage by Component
| Component | Database | Purpose |
|-----------|----------|---------|
| Main app | PostgreSQL | Application data |
| API server | PostgreSQL | REST API data |
| Celery workers | PostgreSQL | Background jobs |
| Unit tests | SQLite (`:memory:`) | Isolated testing |
| Logging fallback | SQLite (`logs/`) | When PostgreSQL unavailable |

### Quick Database Commands
```bash
# Check database status
python check_database.py

# Setup database
python launch.py --setup-db

# Manual connection test
python -c "from src.narrative_gravity.models.base import engine; engine.connect()"
```

## 🚀 Development Setup

### 1. Initial Setup
```bash
# Clone and setup
git clone [repository]
cd narrative_gravity_analysis

# Create environment
python -m venv venv
source venv/bin/activate  # or `venv\Scripts\activate` on Windows

# Install dependencies
pip install -r requirements.txt

# Setup database
python launch.py --setup-db
```

### 2. Launch Development Environment
```bash
# Full platform (recommended)
python launch.py

# Individual services
python launch.py --streamlit-only  # UI only
python launch.py --api-only         # API only
python launch.py --celery-only      # Background worker only
```

### 3. Verify Setup
```bash
# Check all services
python check_database.py

# Run tests
pytest
```

## 📦 Package Structure Guidelines

### Import Standards
```python
# ✅ Package imports (preferred)
from src.narrative_gravity.engine import NarrativeGravityWellsElliptical
from src.narrative_gravity.framework_manager import FrameworkManager

# ✅ Dual import pattern (for Streamlit compatibility)
try:
    from .module import Class  # Relative import
except ImportError:
    from src.package.module import Class  # Absolute fallback
```

### File Organization
```
src/narrative_gravity/
├── __init__.py
├── app.py              # Streamlit application
├── engine.py           # Core analysis engine
├── launcher.py         # Service launcher
├── framework_manager.py # Framework management
├── api/               # REST API
├── models/            # Database models
├── prompts/           # Prompt management
├── tasks/             # Background tasks
└── utils/             # Utilities
```

## 📝 Change Documentation

### Changelog Requirements
- **ALL significant changes** must be documented in `CHANGELOG.md`
- **NO separate summary files** - use the master changelog
- Follow semantic versioning: `[vX.Y.Z] - Description - YYYY-MM-DD`

### Changelog Format
```markdown
## [v2.1.2] - Brief Description - 2025-06-09

### ✨ New Features
- Feature descriptions

### 🔧 Fixes & Improvements
- Bug fixes and improvements

### 🏗️ Infrastructure
- Infrastructure changes
```

## 🧪 Testing Standards

### Test Organization
- **Unit tests**: `tests/unit/` - Use in-memory SQLite
- **Integration tests**: `tests/integration/` - Can use PostgreSQL
- **Utilities**: `tests/utilities/` - Testing utilities

### Database in Tests
```python
# ✅ Unit test fixture
@pytest.fixture
def test_engine():
    return create_engine("sqlite:///:memory:")

# ✅ Integration test - uses actual PostgreSQL
def test_api_integration():
    # Uses configured PostgreSQL database
```

### Running Tests
```bash
# All tests
pytest

# Specific categories
pytest tests/unit/
pytest tests/integration/

# With coverage
pytest --cov=src
```

## 🔧 File Movement Protocol

When reorganizing files:

1. **Find all references**: `grep -r "filename" .`
2. **Update imports**: All Python files using the moved module
3. **Update documentation**: All markdown files referencing the file
4. **Update configs**: `alembic/env.py`, test files, etc.
5. **Test imports**: Ensure everything still works
6. **Document**: Add to `CHANGELOG.md`

## 🎯 Quality Checklist

Before submitting changes:

- [ ] **Database**: Using PostgreSQL for application data
- [ ] **Organization**: Files in correct directories
- [ ] **References**: All file references updated after moves
- [ ] **Documentation**: Changes added to `CHANGELOG.md`
- [ ] **Imports**: All import statements work correctly
- [ ] **Tests**: All tests pass
- [ ] **Documentation**: All doc references accurate

## 🚨 Common Issues

### "Database not accessible"
1. Check PostgreSQL is running: `brew services start postgresql`
2. Verify connection: `python check_database.py`
3. Setup database: `python launch.py --setup-db`

### Import Errors After File Moves
1. Check all Python files: `grep -r "old_module_name" src/`
2. Update alembic config: `alembic/env.py`
3. Update test files: `tests/`

### Service Startup Issues
1. Check ports aren't in use: `lsof -i :8501` or `lsof -i :8000`
2. Use individual service flags: `python launch.py --streamlit-only`
3. Check launch guide: `LAUNCH_GUIDE.md`

## 📊 Text Data Organization

### Corpus Structure
All text data is centralized under `corpus/` for better organization:

```
corpus/
├── golden_set/              # Curated, analysis-ready datasets
│   └── presidential_speeches/
│       ├── txt/            # Standardized text files
│       ├── csv/            # Structured data
│       └── md/             # Markdown versions
├── raw_sources/            # Original source materials
│   ├── recent_us_presidents/
│   ├── synthetic_narratives/
│   └── other_texts/
└── processing_scripts/     # Transform raw → golden
    ├── proper_paragraph_segmentation.py
    └── fix_*.py
```

### Examples Directory
Working demonstrations and tutorials are provided in `examples/`:

```
examples/
├── corpus_generation_demo.py    # Complete demo of generation tools
├── sample_speech.md             # Example markdown with frontmatter
├── sample_documents.csv         # Example CSV data
├── constitution_excerpt.txt     # Plain text example
├── from_*.jsonl                 # Generated JSONL outputs
├── combined_corpus.jsonl        # Multi-source combination
└── generated_schema.json        # Auto-generated schema
```

**Purpose**: Developer onboarding, user training, tool testing, format validation

### Data Processing Workflow
1. **Raw sources**: Original texts stored in `corpus/raw_sources/`
2. **Processing**: Scripts in `corpus/processing_scripts/` standardize format
3. **Golden sets**: Analysis-ready data in `corpus/golden_set/`
4. **Examples**: Working demonstrations in `examples/` for tool training

### Adding New Text Data
- **Raw materials**: Place in `corpus/raw_sources/[category]/`
- **Processing scripts**: Add to `corpus/processing_scripts/`
- **Curated output**: Generate into `corpus/golden_set/[category]/`
- **Examples**: Update `examples/` when adding new data formats

## 📊 Research Data Exports

### Export Organization
Academic and research data exports are organized under `exports/`:

```
exports/
└── academic_formats/           # Research-ready data exports
    ├── *.R                    # Pre-written R analysis scripts
    ├── *.csv                  # Data formatted for statistical tools
    ├── *.parquet              # Compressed columnar data format
    └── *_YYYYMMDD_HHMMSS.*    # Timestamped for version tracking
```

### Export Purpose
- **Academic Collaboration**: Enable researchers to use preferred tools (R, Python, Stata)
- **External Validation**: Support independent replication of analysis
- **Publication Support**: Provide publication-ready datasets
- **Reproducible Research**: Include complete data with analysis code

### Export Standards
- **Timestamped**: All exports include precise creation timestamps
- **Self-contained**: Include both data and analysis scripts
- **Multi-format**: Support various academic analysis tools
- **Documented**: Scripts include clear analysis procedures

## 🚀 Release Process

### Automated Releases
Use the standardized release script for all releases:

```bash
# Test release process safely
python scripts/release.py --dry-run patch --message "Test release"

# Actual releases
python scripts/release.py patch --message "Bug fixes and improvements"
python scripts/release.py minor --message "New features added"
python scripts/release.py major --message "Breaking changes"
```

### Release Requirements
- **100% test pass rate**: All tests must pass before release
- **Clean repository**: No uncommitted changes
- **Documentation current**: All docs up to date
- **File hygiene**: Proper project organization

### What the Release Script Does
1. **Pre-release checks**: Git status, file hygiene, tests, documentation
2. **Version management**: Semantic versioning, CHANGELOG updates
3. **Git operations**: Commits, tags, pushes automatically
4. **Release summary**: Generated success report

For detailed information, see `docs/development/RELEASE_PROCESS.md`.

## 📚 Key Documentation

- **Architecture**: `docs/architecture/database_architecture.md`
- **Launch Guide**: `LAUNCH_GUIDE.md`
- **Release Process**: `docs/development/RELEASE_PROCESS.md`
- **Project Structure**: `PROJECT_STRUCTURE.md`
- **Changelog**: `CHANGELOG.md`

## 🤝 Code Review Guidelines

### Focus Areas
1. **Database usage**: Ensure PostgreSQL for app data
2. **File organization**: Proper directory placement
3. **Import paths**: Correct package imports
4. **Documentation**: Changes documented in changelog
5. **Error handling**: User-friendly error messages with doc references

### Review Checklist
- [ ] Follows project organization philosophy
- [ ] Database architecture respected
- [ ] All references updated for moved files
- [ ] Changes documented in changelog
- [ ] Tests pass
- [ ] Error messages reference appropriate documentation

## 🗂️ Temporary File Management

### Standard Pattern
When creating temporary files during development or analysis:

```bash
# ✅ Correct temporary file organization
tmp/
├── 2025_06_09/
│   ├── prompt_experiments/
│   ├── model_testing/
│   └── visualization_tests/
├── 2025_06_10/
│   └── scoring_validation/
└── 2025_06_11/
    └── framework_comparison/
```

### Best Practices
- **Date format**: `YYYY_MM_DD` for chronological sorting
- **Descriptive names**: Use clear experiment/task names
- **Isolated experiments**: Each temporary effort gets its own subfolder
- **Auto-cleanup**: Directories older than 30 days can be safely removed

### Git Ignore
The `tmp/` directory should be git-ignored to prevent accidental commits:
```gitignore
# Temporary files and experiments
tmp/
```

### Common Use Cases
- **Prompt experiments**: `tmp/2025_06_09/prompt_v3_testing/`
- **Model comparisons**: `tmp/2025_06_09/gpt4_vs_claude/`
- **Visualization tests**: `tmp/2025_06_09/ellipse_rendering/`
- **Data preprocessing**: `tmp/2025_06_09/corpus_cleaning/`

This ensures consistent, professional development across all contributors! 