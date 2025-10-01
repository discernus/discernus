# DO NOT DELETE - CRITICAL SYSTEM SPECIFICATIONS

**⚠️ CRITICAL SYSTEM FILES - DO NOT DELETE OR MODIFY ⚠️**

This document explains why the specification files in `docs/specifications/` are **CRITICAL SYSTEM COMPONENTS** that must never be deleted, moved, or significantly modified without careful consideration of system impact.

## Why These Files Are Critical

The Discernus validation system **directly references and loads** these specification files at runtime to validate experiments. These are not just documentation - they are **active system components** that the validation agents use to determine whether experiments are valid and executable.

## System Dependencies

### 1. Validation Agent Dependencies

The following agents **directly load and reference** these specification files:

- **V2ValidationAgent** (`discernus/agents/validation_agent/v2_validation_agent.py`)
- **V2ValidationAgent** (consolidated validation agent)

Both agents use the `_load_specification_references()` method to dynamically load:
- `CORPUS_SPECIFICATION.md`
- `EXPERIMENT_SPECIFICATION.md` 
- `FRAMEWORK_SPECIFICATION.md`

### 2. Runtime Loading Process

The validation system follows this process:

1. **Dynamic Discovery**: Agents search for `docs/specifications/` directory starting from their location
2. **File Loading**: Each specification file is loaded into memory as reference material
3. **Validation Logic**: The loaded specifications are used to validate experiment components
4. **Error Reporting**: Validation failures reference specific sections of these specifications

### 3. Critical System Functions

These specifications serve as:

- **Validation Standards**: Define what constitutes valid experiments, frameworks, and corpora
- **Reference Documentation**: Provide the authoritative source for validation rules
- **Error Context**: Help users understand why validation failed and how to fix issues
- **System Integration**: Enable the orchestrator to validate experiments before execution

## File Locations and Purpose

| File | Purpose | Used By |
|------|---------|---------|
| `CORPUS_SPECIFICATION.md` | Defines valid corpus structure and metadata requirements | V2ValidationAgent |
| `EXPERIMENT_SPECIFICATION.md` | Defines valid experiment structure and configuration | V2ValidationAgent |
| `FRAMEWORK_SPECIFICATION.md` | Defines valid framework structure and analytical requirements | V2ValidationAgent |

## Impact of Deletion/Modification

### If These Files Are Deleted:
- **System Failure**: Validation agents will crash when trying to load specifications
- **Experiment Blocking**: No experiments can be validated or executed
- **User Experience**: Complete system breakdown with cryptic error messages

### If These Files Are Modified:
- **Validation Changes**: Changes to specification content will immediately affect validation behavior
- **Breaking Changes**: Modifications to required fields or structure can break existing experiments
- **Version Incompatibility**: Changes to specification versions can cause system incompatibilities

## Safe Modification Guidelines

### ✅ Safe Changes:
- **Documentation Updates**: Clarifying language, examples, or explanations
- **Version Bumps**: Updating version numbers in headers
- **New Optional Sections**: Adding new optional requirements
- **Bug Fixes**: Correcting errors in existing specifications

### ❌ Dangerous Changes:
- **Removing Required Fields**: Will break validation logic
- **Changing File Names**: Will break the loading mechanism
- **Moving Files**: Will break the discovery mechanism
- **Structural Changes**: Modifying YAML structure or required sections
- **Breaking Version Changes**: Incompatible changes to specification versions

## System Architecture Context

These specifications are part of the **THIN architecture** principle:

- **Durable Infrastructure**: Specifications serve as stable, long-term system components
- **Agent Agnostic**: Multiple agents reference the same specifications
- **Version Controlled**: Specifications are versioned and tracked in Git
- **Runtime Integration**: Active system components, not just documentation

## Maintenance Protocol

### Before Making Changes:
1. **Test Impact**: Run validation tests to ensure changes don't break existing functionality
2. **Version Control**: Ensure changes are properly versioned and documented
3. **Backward Compatibility**: Consider impact on existing experiments
4. **System Testing**: Verify that all validation agents still work correctly

### Emergency Recovery:
If these files are accidentally deleted or corrupted:
1. **Git Recovery**: Use `git checkout` to restore from version control
2. **System Restart**: Restart any running validation processes
3. **Validation Test**: Run a test experiment to verify system functionality

## Conclusion

These specification files are **CRITICAL SYSTEM COMPONENTS** that enable the Discernus validation system to function. They are not just documentation - they are active system dependencies that must be preserved and maintained with extreme care.

**Remember**: The validation system depends on these files being present, accessible, and properly formatted. Any changes must be made with full understanding of their system impact.

---

*This document was created to prevent accidental deletion or modification of critical system specification files that are actively referenced by the Discernus validation system.*
