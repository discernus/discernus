# Deprecation Note - June 19, 2025

## Files Deprecated

### `.ai_assistant_rules.md`
**Reason**: Redundant with comprehensive master document
**Replacement**: `ai_assistant_compliance_rules.md` (root directory)
**Date Deprecated**: June 19, 2025

## Background

The project had three overlapping AI assistant rule files:
1. `.cursorrules` - Cursor IDE integration (KEPT)
2. `.ai_assistant_rules.md` - General rules (DEPRECATED)
3. `ai_assistant_compliance_rules.md` - Comprehensive master (KEPT)

## Resolution

- **KEPT**: `.cursorrules` - Serves specific Cursor IDE integration purpose
- **KEPT**: `ai_assistant_compliance_rules.md` - Comprehensive master document (202 lines)
- **DEPRECATED**: `.ai_assistant_rules.md` - Redundant with master document

The `.cursorrules` file has been updated to reference the master document as the authoritative source.

## Migration

Any references to `.ai_assistant_rules.md` should be updated to reference `ai_assistant_compliance_rules.md` instead. 