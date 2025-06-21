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

## Framework Data Structure

The `framework_data` field in each chunk supports a three-stage data population model:

### 1. Ingestion Metadata (Populated at Upload Time)
- **Pre-analysis tags**: Human-assigned framework relevance markers
- **Content categorization**: Language complexity, content type, context
- **Domain-specific metadata**: Historical context, author affiliation, etc.

### 2. Preprocessing Markers (Populated During Ingestion)
- **Language markers**: Pre-identified phrases relevant to framework analysis
- **Lexical indicators**: Framework-specific vocabulary patterns
- **Structural markers**: Content organization relevant to analysis

### 3. Analysis Results (Populated During Processing)
- **Well scores**: Individual framework dimension scores (0.0-1.0)
- **Narrative positioning**: Calculated position on framework coordinate system
- **Framework metrics**: Framework-specific calculated measures
- **Confidence scores**: Analysis reliability and confidence indicators

## Validation Workflow

### Current Approach: Framework-Agnostic Ingestion + Runtime Selection

1. **Ingestion**: Validate against core schema only (universal compatibility)
2. **Job Creation**: Select frameworks at runtime for cross-framework analysis
3. **Processing**: Any framework can analyze any corpus
4. **Results Storage**: Framework-specific results stored in `framework_data.analysis_results`
5. **Migration Check**: Detect `schema_version` mismatches 
6. **Auto-upgrade**: Run migration scripts if configured

## Schema Registry

| Schema | Current Version | Status | Notes |
|--------|----------------|---------|-------|
| Core | 1.0.0 | Stable | Universal document+chunk format |
| Civic Virtue Extension | 1.0.0 | Stable | Dignity, Truth, Hope, etc. wells - framework_data structure |
| Political Spectrum Extension | 1.0.0 | Stable | Liberal, Conservative, Libertarian, Authoritarian - framework_data structure |
| Moral-Rhetorical Posture Extension | 1.0.0 | Stable | Restorative, Retributive, etc. postures - framework_data structure |

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