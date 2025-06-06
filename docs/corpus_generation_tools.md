# Corpus Generation Tools Documentation

This document describes the automated tooling for generating JSON Schema skeletons and creating JSONL corpus files from various source formats.

## Overview

The corpus generation tooling consists of two main components:

1. **Schema Generator** (`src/cli/schema_generator.py`) - Generates JSON Schema skeletons from example records
2. **JSONL Generator** (`src/cli/jsonl_generator.py`) - Converts various source formats to JSONL corpus files

These tools ensure all narratives conform to the core+extension schema and provide automated validation and normalization.

## Schema Generator

### Purpose
- Generate JSON Schema skeletons from existing JSONL records
- Detect data types, formats, and enum values automatically
- Validate records against existing schemas
- Support schema evolution and migration

### Usage

```bash
# Generate schema from JSONL file
python src/cli/schema_generator.py \
  --input sample_data.jsonl \
  --output generated_schema.json \
  --title "My Schema" \
  --description "Schema for my dataset"

# Validate records against existing schema
python src/cli/schema_generator.py \
  --input data.jsonl \
  --validate-against schemas/core_schema_v1.0.0.json \
  --show-errors
```

### Features

#### Automatic Type Detection
- **Strings**: Detects formats (date-time, URI, email)
- **Numbers**: Sets appropriate min/max constraints
- **Enums**: Identifies limited value sets (≤5 unique values from 3+ examples)
- **Objects**: Recursively analyzes nested properties
- **Arrays**: Analyzes item types and structures

#### Smart Required Field Detection
- Fields present in ≥80% of records are marked as required
- Handles optional fields with null values appropriately

#### Format Detection
- Date/time patterns: `2024-01-15T14:30:00Z`
- URLs: `https://example.com`
- Email addresses: `user@domain.com`

### Command Line Options

| Option | Description |
|--------|-------------|
| `--input`, `-i` | Input JSONL file with example records |
| `--output`, `-o` | Output JSON schema file |
| `--title` | Schema title |
| `--description` | Schema description |
| `--schema-id` | Schema $id URL |
| `--version` | Schema version (default: 1.0.0) |
| `--validate-against` | Validate input records against existing schema |
| `--show-errors` | Show detailed validation errors |

## JSONL Generator

### Purpose
- Convert various source formats to JSONL corpus files
- Apply different chunking strategies (fixed, sectional, semantic)
- Validate output against core schema
- Handle metadata extraction and normalization

### Supported Input Formats

#### 1. Markdown Files (.md, .markdown)
Supports YAML frontmatter for metadata:

```markdown
---
text_id: "speech_001"
title: "Important Speech"
document_type: "speech"
author: "Jane Doe"
date: "2024-01-15T14:30:00Z"
publication: "Conference 2024"
document_metadata:
  venue: "Washington DC"
  duration_minutes: 45
---

# Speech Content

The main content of the speech goes here...
```

#### 2. CSV Files (.csv)
Must contain a text content column and optional metadata columns:

```csv
text_id,title,document_type,author,date,content
doc_001,Article Title,article,John Smith,2024-01-01T00:00:00Z,"Article content here..."
```

#### 3. Plain Text Files (.txt, .text)
Raw text with metadata provided via command line:

```bash
python src/cli/jsonl_generator.py \
  --input document.txt \
  --metadata '{"author": "Author Name", "document_type": "speech"}'
```

### Chunking Strategies

#### Fixed Chunking
- Splits text into fixed-size chunks with configurable overlap
- Tries to break at word boundaries
- Best for: Uniform processing requirements

```bash
--chunk-type fixed --chunk-size 1000 --chunk-overlap 100
```

#### Sectional Chunking
- Splits by semantic sections (headers, paragraphs, numbered sections)
- Preserves natural document structure
- Best for: Structured documents with clear sections

```bash
--chunk-type sectional
```

#### Semantic Chunking
- Breaks at sentence and paragraph boundaries
- Respects maximum chunk size while maintaining coherence
- Best for: Natural language processing tasks

```bash
--chunk-type semantic --chunk-size 1500
```

### Usage Examples

```bash
# Convert markdown files with sectional chunking
python src/cli/jsonl_generator.py \
  --input documents/*.md \
  --output corpus.jsonl \
  --chunk-type sectional \
  --schema schemas/core_schema_v1.0.0.json

# Convert CSV with specific text column
python src/cli/jsonl_generator.py \
  --input data.csv \
  --output corpus.jsonl \
  --format csv \
  --csv-text-column article_text \
  --chunk-type fixed \
  --chunk-size 800

# Convert plain text with metadata override
python src/cli/jsonl_generator.py \
  --input transcript.txt \
  --output corpus.jsonl \
  --format text \
  --metadata '{"author": "Speaker Name", "document_type": "speech"}' \
  --chunk-type semantic

# Validate existing JSONL file
python src/cli/jsonl_generator.py \
  --input existing_corpus.jsonl \
  --validate-only \
  --schema schemas/core_schema_v1.0.0.json
```

### Command Line Options

| Option | Description |
|--------|-------------|
| `--input`, `-i` | Input files (supports wildcards) |
| `--output`, `-o` | Output JSONL file |
| `--format` | Input format: auto, csv, markdown, text |
| `--schema` | JSON schema file for validation |
| `--chunk-type` | Chunking strategy: fixed, sectional, semantic |
| `--chunk-size` | Chunk size in characters (fixed/semantic) |
| `--chunk-overlap` | Chunk overlap in characters (fixed only) |
| `--csv-text-column` | CSV column containing text content |
| `--metadata` | JSON string with metadata overrides |
| `--validate-only` | Only validate against schema, don't generate |

## Output Format

All generated JSONL files conform to the core schema structure:

```json
{
  "document": {
    "text_id": "unique_identifier",
    "title": "Document Title",
    "document_type": "speech",
    "author": "Author Name",
    "date": "2024-01-15T14:30:00Z",
    "schema_version": "1.0.0",
    "document_metadata": {}
  },
  "chunk_id": 0,
  "total_chunks": 3,
  "chunk_type": "sectional",
  "chunk_size": 1245,
  "document_position": 0.0,
  "word_count": 186,
  "unique_words": 142,
  "word_density": 0.76,
  "chunk_content": "The actual text content of this chunk...",
  "framework_data": {}
}
```

## Chunk Metadata Calculation

### Word Counts
- **word_count**: Total words in chunk (split by whitespace)
- **unique_words**: Unique words (case-insensitive)
- **word_density**: Ratio of unique to total words (lexical diversity)

### Positioning
- **document_position**: Normalized position (0.0-1.0) of chunk start in document
- **chunk_id**: Zero-based index within document
- **total_chunks**: Total number of chunks in document

### Size Information
- **chunk_size**: Actual character count of chunk content
- **chunk_overlap**: Characters overlapping with previous chunk (fixed chunking only)

## Integration with API

Generated JSONL files can be directly uploaded to the corpus ingestion API:

```bash
# Upload generated corpus
curl -X POST "http://localhost:8000/api/corpora/upload" \
  -F "file=@examples/combined_corpus.jsonl" \
  -F "corpus_name=my_corpus"
```

## Schema Evolution

### Creating Extension Schemas

1. Generate base schema from existing data:
```bash
python src/cli/schema_generator.py \
  --input framework_data.jsonl \
  --output schemas/framework_extension_v1.0.0.json \
  --title "Framework Extension Schema"
```

2. Manually refine the generated schema:
   - Add detailed descriptions
   - Adjust required fields
   - Set appropriate constraints
   - Add examples

3. Update the schema registry in `schemas/README.md`

### Migration Scripts

When schemas evolve, create migration scripts in `schemas/migrations/`:

```python
# schemas/migrations/migrate_v1_to_v2.py
def migrate_record(record):
    """Migrate a record from v1.0.0 to v2.0.0"""
    # Add migration logic here
    record['document']['schema_version'] = '2.0.0'
    return record
```

## Best Practices

### Source Data Preparation
1. **Clean your data** before ingestion
2. **Standardize metadata** fields across sources
3. **Use consistent date formats** (ISO 8601)
4. **Validate URLs** and other format-specific fields

### Chunking Strategy Selection
- **Fixed chunking**: When you need consistent chunk sizes for modeling
- **Sectional chunking**: For documents with clear structural divisions
- **Semantic chunking**: For natural language analysis where context matters

### Schema Design
1. **Start with generated schemas** then refine manually
2. **Use descriptive field names** and documentation
3. **Be conservative with required fields** - allow flexibility
4. **Version your schemas** and maintain migration paths

### Validation Workflow
1. Generate JSONL from sources
2. Validate against schema
3. Fix any validation errors
4. Upload to API for ingestion

## Troubleshooting

### Common Issues

#### "Text column not found in CSV"
Ensure your CSV has the expected text column name, or specify it with `--csv-text-column`.

#### "Invalid JSON metadata"
Check that your `--metadata` argument is valid JSON with proper escaping.

#### "Schema validation errors"
Review the error messages and ensure your source data matches the expected schema format.

#### "Empty chunks generated"
Your chunking strategy may be too aggressive. Try:
- Increasing chunk size for fixed chunking
- Using semantic chunking for better boundary detection
- Checking source data for unusual formatting

### Debug Mode

Add verbose output to see what's happening:

```bash
python -v src/cli/jsonl_generator.py [options]
```

### Testing

Run the demonstration script to verify everything works:

```bash
python examples/corpus_generation_demo.py
```

## Dependencies

Ensure you have these packages installed:

```txt
jsonschema>=4.0.0
PyYAML>=6.0.0
```

Install with:
```bash
pip install -r requirements.txt
```

## Contributing

When extending the tooling:

1. **Add new input formats** by extending the `SourceParser` class
2. **Add new chunking strategies** by extending the `TextChunker` class
3. **Add new validation rules** in the schema generator
4. **Update documentation** for any new features
5. **Add test cases** for new functionality

See `examples/corpus_generation_demo.py` for usage patterns and testing approaches. 