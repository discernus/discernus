# Documentation Cleanup Plan - June 2025

## Current Assessment

### ✅ **Keep Current (Active Documentation)**
- **PAPER_PUBLICATION_CHECKLIST.md** - Current paper preparation checklist
- **USER_STORIES.md** - Valuable for understanding user needs and future development
- **MODULAR_ARCHITECTURE.md** - Core technical documentation still relevant
- **STORAGE_ARCHITECTURE.md** - Important for understanding data organization

### 🗃️ **Archive (Historical Development Notes)**
- **PROJECT_CLEANUP_v2025.06.04.md** - Historical cleanup record
- **FRAMEWORK_INJECTION_FIX.md** - Completed fix from development
- **VISUALIZATION_FIXES.md** - Completed fixes from development
- **MODEL_NAME_FIX.md** - Completed fixes from development
- **PROMPT_AND_FILENAME_IMPROVEMENTS.md** - Completed improvements
- **UX_CLEANUP_OPTIONAL_TEXT.md** - Completed UX improvements  
- **CLI_JSON_FIXES.md** - Completed CLI fixes
- **IMPROVED_INTERFACE_NOTES.md** - Completed interface improvements
- **TEST_SAMPLE_JSON.md** - Development test notes
- **ROBUST_FRAMEWORK_NAMES.md** - Completed framework naming fixes

### 🔄 **Review/Update Needed**
- **DEVELOPMENT_ROADMAP.md** - May need updating based on current priorities
- **PROJECT_SNAPSHOT_v2.0.md** - May be historical or still relevant

## Recommended Actions

### 1. Create Archive Structure
```
docs/
├── archive/
│   ├── development_history/     # Historical development notes
│   └── completed_fixes/         # Completed fix documentation
├── development/                 # Current active development docs
└── examples/                   # User guides and examples
```

### 2. Move Historical Files
Move completed fix/cleanup documentation to `docs/archive/completed_fixes/`:
- PROJECT_CLEANUP_v2025.06.04.md
- FRAMEWORK_INJECTION_FIX.md
- VISUALIZATION_FIXES.md
- MODEL_NAME_FIX.md
- PROMPT_AND_FILENAME_IMPROVEMENTS.md
- UX_CLEANUP_OPTIONAL_TEXT.md
- CLI_JSON_FIXES.md
- IMPROVED_INTERFACE_NOTES.md
- TEST_SAMPLE_JSON.md
- ROBUST_FRAMEWORK_NAMES.md

### 3. Keep Active Documentation
Maintain in `docs/development/`:
- PAPER_PUBLICATION_CHECKLIST.md
- USER_STORIES.md
- MODULAR_ARCHITECTURE.md
- STORAGE_ARCHITECTURE.md
- DEVELOPMENT_ROADMAP.md (after review/update)

### 4. Create Missing Documentation
Consider creating:
- **FRAMEWORK_DEVELOPMENT_GUIDE.md** - How to create new frameworks
- **API_REFERENCE.md** - Technical API documentation
- **DEPLOYMENT_GUIDE.md** - How to deploy/distribute the software

## Config Folder Assessment

✅ **Config folder is correctly implemented**
- Uses symlinks to active framework: `config/dipoles.json -> ../frameworks/civic_virtue/dipoles.json`
- Enables clean framework switching via `framework_manager.py`
- No cleanup needed - this is proper modular architecture

## Benefits of Cleanup

1. **Clearer Documentation Structure** - Separate current docs from historical records
2. **Easier Navigation** - Users find relevant docs faster
3. **Reduced Clutter** - Development folder focuses on current needs
4. **Historical Preservation** - Important development history preserved but organized
5. **Better Onboarding** - New contributors see current documentation first

## Implementation Priority

**High Priority:** Archive completed fixes (reduces clutter significantly)
**Medium Priority:** Update DEVELOPMENT_ROADMAP.md 
**Low Priority:** Create new documentation files 