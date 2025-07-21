# PM Frameworks Migration Notice - January 20, 2025

## Complete PM Workspace Archived

**Date**: January 20, 2025  
**Reason**: Framework library migration completed, PM workspace superseded  
**Current Location**: `frameworks/` directory (repository root)

## What Was Moved

The entire `pm/frameworks/` workspace has been moved to:
`deprecated/by-date/2025-01-20/pm_frameworks_migration_workspace/`

### Contents Archived
- **Migration Tools**: framework_migrator.py, run_migration.py, run_auto_migration.py
- **Migration Documentation**: MIGRATION_PLAN.md, MIGRATION_COMPLETION_REPORT.md  
- **v4.0 Migrated Frameworks**: All frameworks converted to v4.0 format
- **Historical v3.2 YAML**: 3_2_spec_frameworks/ directory
- **Legacy CFF Versions**: Multiple CFF evolution iterations
- **Development Artifacts**: Experimental and work-in-progress files

## Migration Completed (July 2025)

### What Was Accomplished
- ✅ **9 frameworks migrated** from v3.2 YAML to v4.0 Markdown format
- ✅ **Production directory structure** created in `frameworks/`
- ✅ **Framework organization** by reference/seed/community categories
- ✅ **Quality standardization** with v4.0 specification compliance

### Current Framework Locations
- **Reference/Core**: `frameworks/reference/core/` (ECF, CAF, CHF)
- **Reference/Flagship**: `frameworks/reference/flagship/` (CFF v4.2)  
- **Seed Frameworks**: `frameworks/seed/` organized by domain (political, ethics, communication, temporal)
- **Community**: `frameworks/community/` (ready for contributions)

## Retrospective Documentation

The migration effort has been documented in GitHub issues:
- **[Epic #80](https://github.com/discernus/discernus/issues/80)**: Framework Library Modernization retrospective
- **[Issues #81-85](https://github.com/discernus/discernus/issues/81)**: Detailed migration documentation

## For Current Work

**Use the main `frameworks/` directory for all framework-related work.**

The PM workspace served its purpose as a development environment for the major framework library modernization effort. All production frameworks now reside in the properly organized `frameworks/` directory.
