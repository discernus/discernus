# Registry

**Module:** `src.corpus.registry`
**File:** `/Volumes/dev/discernus/src/corpus/registry.py`
**Package:** `corpus`

Corpus Registry - Enhanced corpus management with stable identifiers.

Provides:
- Stable URIs for corpus and document identification  
- Database integration while preserving file workflow
- FAIR data principles compliance
- Academic citation support

## Dependencies

- `dataclasses`
- `datetime`
- `hashlib`
- `json`
- `os`
- `pathlib`
- `sqlalchemy`
- `src.utils.database`
- `typing`
- `urllib.parse`

## Table of Contents

### Classes
- [CorpusDocument](#corpusdocument)
- [CorpusRegistry](#corpusregistry)

## Classes

### CorpusDocument

Enhanced document representation with stable identifiers.

---

### CorpusRegistry

Enhanced corpus registry with stable identifiers and FAIR data compliance.

Provides:
- Stable URI generation for citations
- Database integration with file system preservation
- Content integrity validation
- Academic metadata standards

#### Methods

##### `__init__`
```python
__init__(self, base_uri: str)
```

##### `generate_text_id`
```python
generate_text_id(self, author: str, title: str, date: datetime, doc_type: str) -> str
```

Generate semantic text identifier for stable referencing.

Format: {author_last}_{type}_{year}[_{sequence}]
Example: lincoln_inaugural_1865, obama_sotu_2009_01

##### `generate_uri`
```python
generate_uri(self, text_id: str) -> str
```

Generate stable URI for document citation (FUTURE: not yet implemented).

##### `calculate_content_hash`
```python
calculate_content_hash(self, file_path: Path) -> str
```

Calculate SHA-256 hash of file content for integrity checking.

##### `register_document`
```python
register_document(self, file_path: Union[Any], title: str, author: str, date: datetime, document_type: str, **metadata) -> [CorpusDocument](src/corpus/registry.md#corpusdocument)
```

Register a document in the corpus with stable identifiers.

Args:
    file_path: Path to source file
    title: Document title
    author: Document author
    date: Document date
    document_type: Type of document (inaugural, sotu, speech, etc.)
    **metadata: Additional metadata fields
    
Returns:
    CorpusDocument with stable identifiers and metadata

##### `register_corpus_directory`
```python
register_corpus_directory(self, directory: Union[Any], corpus_name: str, metadata_file: Optional[str]) -> List[[CorpusDocument](src/corpus/registry.md#corpusdocument)]
```

Register all documents in a directory as a corpus.

Args:
    directory: Directory containing corpus files
    corpus_name: Name for the corpus
    metadata_file: Optional CSV/JSON file with document metadata
    
Returns:
    List of registered CorpusDocument objects

##### `get_document_by_text_id`
```python
get_document_by_text_id(self, text_id: str) -> Optional[[CorpusDocument](src/corpus/registry.md#corpusdocument)]
```

Retrieve document by text_id.

##### `get_document_by_uri`
```python
get_document_by_uri(self, uri: str) -> Optional[[CorpusDocument](src/corpus/registry.md#corpusdocument)]
```

Retrieve document by URI.

##### `list_documents`
```python
list_documents(self, corpus_name: Optional[str]) -> List[[CorpusDocument](src/corpus/registry.md#corpusdocument)]
```

List all registered documents, optionally filtered by corpus.

##### `validate_integrity`
```python
validate_integrity(self) -> Dict[Any]
```

Validate corpus integrity - check files exist and hashes match.

Returns:
    Dictionary with 'valid', 'missing_files', 'hash_mismatches', 'errors'

##### `_text_id_exists`
```python
_text_id_exists(self, text_id: str) -> bool
```

Check if text_id already exists in database.

##### `_save_to_database`
```python
_save_to_database(self, doc: [CorpusDocument](src/corpus/registry.md#corpusdocument)) -> None
```

Save document to database.

##### `_create_corpus_record`
```python
_create_corpus_record(self, name: str, record_count: int) -> int
```

Create corpus record in database.

##### `_parse_filename_metadata`
```python
_parse_filename_metadata(self, filename: str) -> Dict
```

Parse basic metadata from filename patterns like 'golden_author_type_seq.txt'.

##### `_load_metadata_file`
```python
_load_metadata_file(self, metadata_path: Path) -> Dict
```

Load document metadata from CSV or JSON file.

##### `_row_to_document`
```python
_row_to_document(self, row) -> [CorpusDocument](src/corpus/registry.md#corpusdocument)
```

Convert database row to CorpusDocument object.

---

*Generated on 2025-06-21 18:56:11*