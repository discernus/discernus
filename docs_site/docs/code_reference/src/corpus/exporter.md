# Exporter

**Module:** `src.corpus.exporter`
**File:** `/app/src/corpus/exporter.py`
**Package:** `corpus`

Corpus Exporter - Academic format exports with citation support.

Provides:
- Research-ready dataset exports (CSV, JSON, R, Python)
- Citation format generation (APA, MLA, Chicago, BibTeX)
- Academic metadata standards compliance
- Replication package creation

## Dependencies

- `csv`
- `dataclasses`
- `datetime`
- `json`
- `pathlib`
- `registry`
- `typing`
- `yaml`

## Table of Contents

### Classes
- [CorpusExporter](#corpusexporter)

## Classes

### CorpusExporter

Academic format exporter for corpus data.

Provides:
- Multiple export formats for different research tools
- Standard citation format generation
- Research replication packages
- Academic metadata compliance

#### Methods

##### `__init__`
```python
__init__(self, registry: Optional[[CorpusRegistry](src/corpus/registry.md#corpusregistry)])
```

##### `export_research_dataset`
```python
export_research_dataset(self, output_dir: Path, corpus_name: Optional[str], formats: List[str], include_content: bool, include_analysis_code: bool) -> Dict[Any]
```

Export comprehensive research dataset in multiple formats.

Args:
    output_dir: Directory for export files
    corpus_name: Optional corpus name to filter by
    formats: Export formats ['csv', 'json', 'r', 'python', 'stata']
    include_content: Whether to include full text content
    include_analysis_code: Whether to include analysis templates
    
Returns:
    Dictionary mapping format names to output file paths

##### `generate_citations`
```python
generate_citations(self, documents: List[[CorpusDocument](src/corpus/registry.md#corpusdocument)], style: str, output_file: Optional[Path]) -> Union[Any]
```

Generate academic citations for corpus documents.

Args:
    documents: List of documents to cite
    style: Citation style ('apa', 'mla', 'chicago', 'bibtex')
    output_file: Optional file to write citations to
    
Returns:
    Citation text if no output_file, otherwise path to output file

##### `create_replication_package`
```python
create_replication_package(self, output_dir: Path, experiment_ids: Optional[List[int]], corpus_name: Optional[str]) -> Path
```

Create complete replication package for research.

Args:
    output_dir: Directory for replication package
    experiment_ids: Optional specific experiments to include
    corpus_name: Optional corpus name to include
    
Returns:
    Path to created replication package directory

##### `export_corpus_metadata`
```python
export_corpus_metadata(self, output_file: Path, corpus_name: Optional[str], format: str) -> Path
```

Export comprehensive corpus metadata for archival and discovery.

Args:
    output_file: Output file path
    corpus_name: Optional corpus name to filter by
    format: Output format ('json', 'xml', 'yaml')
    
Returns:
    Path to created metadata file

##### `_export_csv`
```python
_export_csv(self, documents: List[[CorpusDocument](src/corpus/registry.md#corpusdocument)], output_dir: Path, include_content: bool) -> Path
```

Export corpus as CSV.

##### `_export_json`
```python
_export_json(self, documents: List[[CorpusDocument](src/corpus/registry.md#corpusdocument)], output_dir: Path, include_content: bool) -> Path
```

Export corpus as JSON.

##### `_export_r_dataset`
```python
_export_r_dataset(self, documents: List[[CorpusDocument](src/corpus/registry.md#corpusdocument)], output_dir: Path, include_content: bool) -> Path
```

Export corpus as R dataset with analysis script.

##### `_export_python_dataset`
```python
_export_python_dataset(self, documents: List[[CorpusDocument](src/corpus/registry.md#corpusdocument)], output_dir: Path, include_content: bool) -> Path
```

Export corpus as Python dataset with analysis script.

##### `_export_stata_dataset`
```python
_export_stata_dataset(self, documents: List[[CorpusDocument](src/corpus/registry.md#corpusdocument)], output_dir: Path, include_content: bool) -> Path
```

Export corpus as Stata dataset.

##### `_format_citation`
```python
_format_citation(self, doc: [CorpusDocument](src/corpus/registry.md#corpusdocument), style: str) -> str
```

Format citation for a document in specified style.

##### `_create_export_metadata`
```python
_create_export_metadata(self, documents: List[[CorpusDocument](src/corpus/registry.md#corpusdocument)], export_dir: Path, exported_files: Dict[Any]) -> None
```

Create metadata file for export.

##### `_create_analysis_templates`
```python
_create_analysis_templates(self, export_dir: Path, formats: List[str]) -> None
```

Create analysis templates for different formats.

##### `_create_export_readme`
```python
_create_export_readme(self, export_dir: Path, corpus_name: Optional[str], formats: List[str], include_content: bool) -> None
```

Create README for export directory.

##### `_export_experiment_data`
```python
_export_experiment_data(self, experiment_ids: List[int], output_dir: Path) -> None
```

Export experiment data for replication package.

##### `_create_replication_scripts`
```python
_create_replication_scripts(self, scripts_dir: Path) -> None
```

Create replication analysis scripts.

##### `_create_replication_docs`
```python
_create_replication_docs(self, docs_dir: Path, corpus_name: Optional[str], experiment_ids: Optional[List[int]]) -> None
```

Create replication documentation.

##### `_create_replication_readme`
```python
_create_replication_readme(self, package_dir: Path, corpus_name: Optional[str], experiment_ids: Optional[List[int]]) -> None
```

Create master README for replication package.

##### `_export_metadata_xml`
```python
_export_metadata_xml(self, metadata: Dict[Any], output_file: Path) -> None
```

Export metadata as XML (placeholder implementation).

---

*Generated on 2025-06-21 20:19:04*