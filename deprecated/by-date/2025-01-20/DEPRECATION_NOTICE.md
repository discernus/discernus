# Deprecation Notice - January 20, 2025

## MECE Trinity Nomenclature Deprecated

**Date**: January 20, 2025  
**Reason**: Terminology standardization for framework library release

### What Was Deprecated
- **Old Terminology**: "MECE Trinity + X" architecture
- **Old Location**: `pm/frameworks/mece_trinity/` (moved here from PM workspace)

### Current Terminology
- **New Terminology**: "Core Modules + Flagship" architecture
- **Current Location**: `frameworks/reference/`
  - **Core Modules** (Universal): ECF v1.0, CAF v4.1, CHF v1.0
  - **Flagship Module** (Comprehensive): CFF v4.2

### Files Moved
- `mece_trinity_deprecated_pm_workspace/` - Complete PM workspace content
- Contains older versions of frameworks and deprecated documentation
- All content superseded by current `frameworks/reference/` directory

### Migration Actions Taken
- Updated GitHub issues #67-79 to use correct terminology
- Current framework files remain canonical in `frameworks/reference/`
- No code changes needed (no Python code referenced MECE Trinity)

This deprecation ensures consistent terminology across the framework library for the upcoming release.
