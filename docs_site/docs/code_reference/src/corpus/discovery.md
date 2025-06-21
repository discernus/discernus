# Discovery

**Module:** `src.corpus.discovery`
**File:** `/Users/jeffwhatcott/Library/Mobile Documents/com~apple~CloudDocs/Coding Projects/discernus/src/corpus/discovery.py`
**Package:** `corpus`

Corpus Discovery - Search and exploration tools for corpus navigation.

Provides:
- Semantic and text-based search across corpus
- Faceted browsing by metadata fields
- Document similarity and clustering
- Corpus statistics and analytics

## Dependencies

- `collections`
- `csv`
- `dataclasses`
- `datetime`
- `json`
- `pathlib`
- `re`
- `registry`
- `time`
- `typing`

## Table of Contents

### Classes
- [SearchResult](#searchresult)
- [SearchResults](#searchresults)
- [CorpusStatistics](#corpusstatistics)
- [CorpusDiscovery](#corpusdiscovery)

## Classes

### SearchResult

Single search result with relevance scoring.

#### Methods

##### `__str__`
```python
__str__(self) -> str
```

---

### SearchResults

Collection of search results with metadata.

#### Methods

##### `__len__`
```python
__len__(self) -> int
```

##### `__iter__`
```python
__iter__(self)
```

##### `top`
```python
top(self, n: int) -> List[[SearchResult](src/corpus/discovery.md#searchresult)]
```

Get top N results by relevance.

##### `summary`
```python
summary(self) -> str
```

Generate search results summary.

---

### CorpusStatistics

Comprehensive corpus statistics.

#### Methods

##### `summary`
```python
summary(self) -> str
```

Generate statistics summary.

---

### CorpusDiscovery

Comprehensive corpus discovery and exploration tools.

Provides:
- Full-text and metadata search
- Faceted browsing and filtering
- Document similarity analysis
- Corpus statistics and analytics

#### Methods

##### `__init__`
```python
__init__(self, registry: Optional[[CorpusRegistry](src/corpus/registry.md#corpusregistry)])
```

##### `search`
```python
search(self, query: str, fields: Optional[List[str]], filters: Optional[Dict[Any]], limit: int, include_content: bool) -> [SearchResults](src/corpus/discovery.md#searchresults)
```

Search corpus documents with text and metadata filtering.

Args:
    query: Search query string
    fields: Fields to search in (default: all text fields)
    filters: Additional filters {field: value} or {field: [values]}
    limit: Maximum number of results
    include_content: Whether to search file content (slower)
    
Returns:
    SearchResults with ranked matches

##### `browse_by_facet`
```python
browse_by_facet(self, facet_field: str, facet_value: Optional[str]) -> Union[Any]
```

Browse corpus by faceted metadata.

Args:
    facet_field: Field to facet by (author, document_type, year, etc.)
    facet_value: Optional specific value to filter by
    
Returns:
    If facet_value is None: Dictionary of {value: count}
    If facet_value is provided: List of matching documents

##### `find_similar_documents`
```python
find_similar_documents(self, text_id: str, limit: int) -> List[Tuple[Any]]
```

Find documents similar to the given document.

Args:
    text_id: Text ID of reference document
    limit: Maximum number of similar documents
    
Returns:
    List of (document, similarity_score) tuples

##### `get_corpus_statistics`
```python
get_corpus_statistics(self, corpus_name: Optional[str]) -> [CorpusStatistics](src/corpus/discovery.md#corpusstatistics)
```

Generate comprehensive corpus statistics.

Args:
    corpus_name: Optional corpus name to filter by
    
Returns:
    CorpusStatistics with comprehensive metrics

##### `get_timeline`
```python
get_timeline(self, corpus_name: Optional[str], group_by: str) -> Dict[Any]
```

Get corpus timeline grouped by time period.

Args:
    corpus_name: Optional corpus name to filter by
    group_by: Time grouping ('year', 'decade', 'month')
    
Returns:
    Dictionary mapping time periods to document lists

##### `export_catalog`
```python
export_catalog(self, output_path: Path, format: str, corpus_name: Optional[str]) -> Path
```

Export corpus catalog in various formats.

Args:
    output_path: Path for output file
    format: Export format ('csv', 'json', 'tsv')
    corpus_name: Optional corpus name to filter by
    
Returns:
    Path to created file

##### `_get_documents`
```python
_get_documents(self) -> List[[CorpusDocument](src/corpus/registry.md#corpusdocument)]
```

Get cached documents or load from registry.

##### `_apply_filters`
```python
_apply_filters(self, documents: List[[CorpusDocument](src/corpus/registry.md#corpusdocument)], filters: Dict[Any]) -> List[[CorpusDocument](src/corpus/registry.md#corpusdocument)]
```

Apply metadata filters to document list.

##### `_calculate_relevance`
```python
_calculate_relevance(self, doc: [CorpusDocument](src/corpus/registry.md#corpusdocument), query: str, fields: List[str], include_content: bool) -> float
```

Calculate relevance score for document against query.

##### `_extract_match_context`
```python
_extract_match_context(self, doc: [CorpusDocument](src/corpus/registry.md#corpusdocument), query: str, fields: List[str], include_content: bool) -> List[str]
```

Extract context snippets around query matches.

##### `_get_match_fields`
```python
_get_match_fields(self, doc: [CorpusDocument](src/corpus/registry.md#corpusdocument), query: str, fields: List[str], include_content: bool) -> List[str]
```

Get list of fields that matched the query.

##### `_calculate_facets`
```python
_calculate_facets(self, documents: List[[CorpusDocument](src/corpus/registry.md#corpusdocument)]) -> Dict[Any]
```

Calculate facet counts for search results.

##### `_calculate_similarity`
```python
_calculate_similarity(self, doc1: [CorpusDocument](src/corpus/registry.md#corpusdocument), doc2: [CorpusDocument](src/corpus/registry.md#corpusdocument)) -> float
```

Calculate similarity score between two documents.

##### `_export_catalog_csv`
```python
_export_catalog_csv(self, documents: List[[CorpusDocument](src/corpus/registry.md#corpusdocument)], output_path: Path) -> Path
```

Export catalog as CSV.

##### `_export_catalog_json`
```python
_export_catalog_json(self, documents: List[[CorpusDocument](src/corpus/registry.md#corpusdocument)], output_path: Path) -> Path
```

Export catalog as JSON.

##### `_export_catalog_tsv`
```python
_export_catalog_tsv(self, documents: List[[CorpusDocument](src/corpus/registry.md#corpusdocument)], output_path: Path) -> Path
```

Export catalog as TSV.

---

*Generated on 2025-06-21 12:44:47*