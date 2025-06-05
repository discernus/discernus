# JSON Schema Repository for Narrative Gravity Analysis

This directory contains versioned JSON Schema files for the universal narrative corpus format and framework-specific extensions.

## Schema Versioning Policy

We use **Semantic Versioning (SemVer)** for all schema files:
- **Major version** (x.0.0): Breaking changes that require data migration
- **Minor version** (x.y.0): Backward-compatible additions of new fields
- **Patch version** (x.y.z): Documentation or validation rule clarifications

## File Naming Convention

All schema files include the version in the filename:
- `core_schema_v1.0.0.json` - Universal core document+chunk schema
- `cv_extension_v1.0.0.json` - Civic Virtue framework extension
- `mrp_extension_v1.0.0.json` - Moral-Rhetorical Posture framework extension  
- `ps_extension_v1.0.0.json` - Political Spectrum framework extension

## Schema Structure

Each schema file contains:
- `$schema`: JSON Schema draft version (2020-12)
- `$id`: Unique identifier URL for the schema version
- `title`: Human-readable schema name
- `description`: Schema purpose and usage
- `type`: Root object type
- `properties`: Field definitions with validation rules
- `required`: Array of mandatory fields

## Usage in Data

All JSONL records must include a `schema_version` field that references the schema version:

```json
{
  "schema_version": "1.0.0",
  "text_id": "example_001",
  // ... other fields
}
```

## Migration Scripts

When schema versions are updated, migration scripts are provided in the `migrations/` subdirectory:
- `migrate_1.0.0_to_1.1.0.py` - Python migration script
- `migrate_1.0.0_to_1.1.0.jq` - jq command-line migration

## Framework Extension Guidelines

Framework-specific extensions:
1. **Must not** modify core schema fields
2. **Should** add fields to `framework_data` object in chunks
3. **Must** provide backward compatibility for older versions
4. **Should** follow additive-only changes when possible

## Validation Workflow

1. **Ingestion**: Validate against core schema + active framework extensions
2. **Migration Check**: Detect `schema_version` mismatches 
3. **Auto-upgrade**: Run migration scripts if configured
4. **Storage**: Store original version info with migrated data

## Schema Registry

| Schema | Current Version | Status | Notes |
|--------|----------------|---------|-------|
| Core | 1.0.0 | Stable | Universal document+chunk format |
| Civic Virtue | 1.0.0 | Stable | Dignity, Truth, Hope, etc. wells |
| Moral-Rhetorical Posture | 1.0.0 | Draft | Dipole marker framework |
| Political Spectrum | 1.0.0 | Draft | Ideological lexicon mapping |

## Git Tags

Each schema release is tagged in Git:
```bash
git tag v1.0.0
git push --tags
```

Schema URLs resolve to tagged versions:
```
https://your-repo.github.io/schemas/core_schema_v1.0.0.json
``` 