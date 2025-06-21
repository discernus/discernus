# Intelligent Ingestion

**Module:** `src.corpus.intelligent_ingestion`
**File:** `/Volumes/dev/discernus/src/corpus/intelligent_ingestion.py`
**Package:** `corpus`

Intelligent Corpus Ingestion Service

Automatically extracts metadata from messy text files with confidence scoring.

## Dependencies

- `dataclasses`
- `datetime`
- `hashlib`
- `json`
- `openai`
- `os`
- `pathlib`
- `re`
- `registry`
- `shutil`
- `time`
- `typing`

## Table of Contents

### Classes
- [ExtractedMetadata](#extractedmetadata)
- [MetadataExtractor](#metadataextractor)
- [IntelligentIngestionService](#intelligentingestionservice)

## Classes

### ExtractedMetadata

Container for extracted metadata with confidence scoring

#### Methods

##### `__post_init__`
```python
__post_init__(self)
```

---

### MetadataExtractor

LLM-powered metadata extraction with confidence scoring

#### Methods

##### `__init__`
```python
__init__(self, api_key: Optional[str], content_limit: int)
```

##### `extract_metadata`
```python
extract_metadata(self, text_content: str, filename: str) -> [ExtractedMetadata](src/corpus/intelligent_ingestion.md#extractedmetadata)
```

Extract metadata from text content using LLM with retry logic

##### `_build_extraction_prompt`
```python
_build_extraction_prompt(self, text_content: str, filename: str) -> str
```

Build the prompt for metadata extraction with smart truncation

##### `_calculate_confidence`
```python
_calculate_confidence(self, metadata: [ExtractedMetadata](src/corpus/intelligent_ingestion.md#extractedmetadata), text_content: str) -> float
```

Calculate confidence score based on completeness and validation

##### `_is_valid_date`
```python
_is_valid_date(self, date_str: str) -> bool
```

Check if date string is valid

##### `_extract_title_fallback`
```python
_extract_title_fallback(self, text_content: str, filename: str) -> str
```

Fallback title extraction if LLM fails

---

### IntelligentIngestionService

Main service for intelligent corpus ingestion

#### Methods

##### `__init__`
```python
__init__(self, corpus_registry: [CorpusRegistry](src/corpus/registry.md#corpusregistry), confidence_threshold: float, content_limit: int)
```

##### `ingest_directory`
```python
ingest_directory(self, directory_path: str, output_dir: str) -> Dict[Any]
```

Ingest all text files from a directory

##### `_update_processed_manifest`
```python
_update_processed_manifest(self, text_id: str, file_path: Path, content_hash: str, metadata: [ExtractedMetadata](src/corpus/intelligent_ingestion.md#extractedmetadata)) -> None
```

Update the global manifest of processed files.

##### `check_already_processed`
```python
check_already_processed(self, content_hash: str) -> Optional[str]
```

Check if content has already been processed by hash.

##### `_process_file`
```python
_process_file(self, file_path: Path, output_dir: Path) -> Dict[Any]
```

Process a single file with organized storage for successful results.

##### `_generate_text_id`
```python
_generate_text_id(self, metadata: [ExtractedMetadata](src/corpus/intelligent_ingestion.md#extractedmetadata)) -> str
```

Generate semantic text ID from metadata

##### `_organize_processed_file`
```python
_organize_processed_file(self, file_path: Path, text_id: str, content_hash: str, metadata: [ExtractedMetadata](src/corpus/intelligent_ingestion.md#extractedmetadata)) -> Path
```

Move successfully processed file to content-addressable storage.

Args:
    file_path: Original file path
    text_id: Generated text ID (e.g., lincoln_inaugural_1865)  
    content_hash: SHA-256 hash of content
    metadata: Extracted metadata
    
Returns:
    Path to new stable location

---

*Generated on 2025-06-21 18:56:11*