# Root Documentation Archive - July 15, 2025

## What Was Archived

**From**: Root directory (/)  
**To**: deprecated/by-date/2025-07-15/root_docs/  
**Reason**: Obsolete documentation cleanup during project reorganization

## Archived Files

### `PARSING_SOLUTION_SUMMARY.md`
- **What**: Documents centralized parsing logic solution
- **Why Archived**: Describes THICK patterns that violate THIN architecture principles
- **Superseded By**: THIN architecture patterns in `docs/THIN_ARCHITECTURE_REFERENCE.md`

### `FIX_SUMMARY.md`
- **What**: Claude 3.5 Sonnet model registry fixes
- **Why Archived**: Temporary fix documentation, likely obsolete
- **Superseded By**: Current model registry automation in `scripts/`

### `VERTEX_AI_CLAUDE_STATUS_REPORT.md`
- **What**: Temporary status report on Vertex AI integration
- **Why Archived**: Temporary status report no longer needed
- **Superseded By**: Current model availability is handled automatically

### `MODEL_AVAILABILITY_REPORT.md`
- **What**: Model availability information
- **Why Archived**: Likely outdated information
- **Superseded By**: Dynamic model registry in `discernus/gateway/models.yaml`

### `QUICK_START.md`
- **What**: SOAR-specific quick start guide (55 lines)
- **Why Archived**: Used SOAR terminology and redundant with comprehensive guide
- **Superseded By**: `docs/QUICK_START_GUIDE.md` (313 lines, comprehensive)

## Migration Notes

All essential concepts from these files have been absorbed into the current documentation system:

- **THIN Architecture**: `docs/THIN_ARCHITECTURE_REFERENCE.md`
- **Quick Start**: `docs/QUICK_START_GUIDE.md`
- **Model Management**: `discernus/gateway/model_registry.py`
- **CLI Usage**: `discernus_cli.py --help`

## Recovery

If any content from these files is needed:
1. Check if the concept has been absorbed into current documentation
2. Use this archive location for historical reference
3. Consider whether patterns should be updated to current THIN standards

**Archive Date**: July 15, 2025  
**Project Phase**: General cleanup and PM reorganization
