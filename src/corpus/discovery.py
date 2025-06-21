"""
Corpus Discovery - Search and exploration tools for corpus navigation.

Provides:
- Semantic and text-based search across corpus
- Faceted browsing by metadata fields
- Document similarity and clustering
- Corpus statistics and analytics
"""

import re
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Union
from dataclasses import dataclass, field

from .registry import CorpusRegistry, CorpusDocument


@dataclass
class SearchResult:
    """Single search result with relevance scoring."""
    
    document: CorpusDocument
    relevance_score: float = 0.0
    match_context: List[str] = field(default_factory=list)  # Snippets showing matches
    match_fields: List[str] = field(default_factory=list)   # Fields where matches found
    
    def __str__(self) -> str:
        return f"{self.document.text_id} (score: {self.relevance_score:.3f})"


@dataclass
class SearchResults:
    """Collection of search results with metadata."""
    
    results: List[SearchResult] = field(default_factory=list)
    query: str = ""
    total_matches: int = 0
    search_time_ms: int = 0
    facets: Dict[str, Dict[str, int]] = field(default_factory=dict)  # Field -> value -> count
    
    def __len__(self) -> int:
        return len(self.results)
    
    def __iter__(self):
        return iter(self.results)
    
    def top(self, n: int = 10) -> List[SearchResult]:
        """Get top N results by relevance."""
        return self.results[:n]
    
    def summary(self) -> str:
        """Generate search results summary."""
        if not self.results:
            return f"No results found for '{self.query}'"
        
        lines = [
            f"🔍 Search Results for '{self.query}'",
            f"Found {self.total_matches} matches in {self.search_time_ms}ms",
            "=" * 50
        ]
        
        for i, result in enumerate(self.results[:10], 1):
            lines.append(f"{i:2d}. {result.document.title}")
            lines.append(f"    {result.document.author} ({result.document.date.year})")
            lines.append(f"    Score: {result.relevance_score:.3f} | URI: {result.document.uri}")
            
            if result.match_context:
                lines.append(f"    Context: {result.match_context[0][:100]}...")
            lines.append("")
        
        return "\n".join(lines)


@dataclass 
class CorpusStatistics:
    """Comprehensive corpus statistics."""
    
    # Basic counts
    total_documents: int = 0
    total_authors: int = 0
    total_words: int = 0
    total_file_size: int = 0
    
    # Time range
    earliest_date: Optional[datetime] = None
    latest_date: Optional[datetime] = None
    date_span_years: float = 0.0
    
    # Document types
    document_types: Dict[str, int] = field(default_factory=dict)
    
    # Authors
    authors: Dict[str, int] = field(default_factory=dict)  # author -> doc count
    
    # File formats
    file_formats: Dict[str, int] = field(default_factory=dict)
    
    # Years active
    years_active: Dict[int, int] = field(default_factory=dict)  # year -> doc count
    
    def summary(self) -> str:
        """Generate statistics summary."""
        lines = [
            "📊 Corpus Statistics",
            "=" * 40,
            f"Documents: {self.total_documents:,}",
            f"Authors: {self.total_authors:,}",
            f"Total Words: {self.total_words:,}" if self.total_words else "Total Words: Not calculated",
            f"File Size: {self.total_file_size / 1024 / 1024:.1f} MB",
            ""
        ]
        
        if self.earliest_date and self.latest_date:
            lines.extend([
                f"Time Range: {self.earliest_date.year} - {self.latest_date.year}",
                f"Span: {self.date_span_years:.1f} years",
                ""
            ])
        
        if self.document_types:
            lines.extend([
                "Document Types:",
                *[f"  {doc_type}: {count}" for doc_type, count in 
                  sorted(self.document_types.items(), key=lambda x: x[1], reverse=True)],
                ""
            ])
        
        if self.authors:
            lines.extend([
                "Top Authors:",
                *[f"  {author}: {count}" for author, count in 
                  sorted(self.authors.items(), key=lambda x: x[1], reverse=True)[:10]],
                ""
            ])
        
        return "\n".join(lines)


class CorpusDiscovery:
    """
    Comprehensive corpus discovery and exploration tools.
    
    Provides:
    - Full-text and metadata search
    - Faceted browsing and filtering
    - Document similarity analysis
    - Corpus statistics and analytics
    """
    
    def __init__(self, registry: Optional[CorpusRegistry] = None):
        self.registry = registry or CorpusRegistry()
        
        # Cache for performance
        self._document_cache = None
        self._statistics_cache = None
        
    def search(self, 
               query: str,
               fields: Optional[List[str]] = None,
               filters: Optional[Dict[str, Union[str, List[str]]]] = None,
               limit: int = 50,
               include_content: bool = False) -> SearchResults:
        """
        Search corpus documents with text and metadata filtering.
        
        Args:
            query: Search query string
            fields: Fields to search in (default: all text fields)
            filters: Additional filters {field: value} or {field: [values]}
            limit: Maximum number of results
            include_content: Whether to search file content (slower)
            
        Returns:
            SearchResults with ranked matches
        """
        import time
        start_time = time.time()
        
        # Default search fields
        if fields is None:
            fields = ['title', 'author', 'document_type']
            if include_content:
                fields.append('content')
        
        # Get all documents
        documents = self._get_documents()
        
        # Apply filters first
        if filters:
            documents = self._apply_filters(documents, filters)
        
        # Search and score
        results = []
        for doc in documents:
            score = self._calculate_relevance(doc, query, fields, include_content)
            if score > 0:
                match_context = self._extract_match_context(doc, query, fields, include_content)
                match_fields = self._get_match_fields(doc, query, fields, include_content)
                
                results.append(SearchResult(
                    document=doc,
                    relevance_score=score,
                    match_context=match_context,
                    match_fields=match_fields
                ))
        
        # Sort by relevance and limit
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        results = results[:limit]
        
        # Calculate facets
        facets = self._calculate_facets(documents)
        
        search_time = int((time.time() - start_time) * 1000)
        
        return SearchResults(
            results=results,
            query=query,
            total_matches=len(results),
            search_time_ms=search_time,
            facets=facets
        )
    
    def browse_by_facet(self, 
                       facet_field: str,
                       facet_value: Optional[str] = None) -> Union[Dict[str, int], List[CorpusDocument]]:
        """
        Browse corpus by faceted metadata.
        
        Args:
            facet_field: Field to facet by (author, document_type, year, etc.)
            facet_value: Optional specific value to filter by
            
        Returns:
            If facet_value is None: Dictionary of {value: count}
            If facet_value is provided: List of matching documents
        """
        documents = self._get_documents()
        
        if facet_value is None:
            # Return facet counts
            facet_counts = defaultdict(int)
            
            for doc in documents:
                if facet_field == 'year':
                    value = str(doc.date.year) if doc.date else 'Unknown'
                elif facet_field == 'decade':
                    value = f"{doc.date.year // 10 * 10}s" if doc.date else 'Unknown'
                else:
                    value = getattr(doc, facet_field, 'Unknown')
                    if value is None:
                        value = 'Unknown'
                
                facet_counts[str(value)] += 1
            
            return dict(facet_counts)
        
        else:
            # Return filtered documents
            filtered_docs = []
            
            for doc in documents:
                if facet_field == 'year':
                    doc_value = str(doc.date.year) if doc.date else 'Unknown'
                elif facet_field == 'decade': 
                    doc_value = f"{doc.date.year // 10 * 10}s" if doc.date else 'Unknown'
                else:
                    doc_value = str(getattr(doc, facet_field, 'Unknown'))
                
                if doc_value == facet_value:
                    filtered_docs.append(doc)
            
            return filtered_docs
    
    def find_similar_documents(self, 
                              text_id: str,
                              limit: int = 10) -> List[Tuple[CorpusDocument, float]]:
        """
        Find documents similar to the given document.
        
        Args:
            text_id: Text ID of reference document
            limit: Maximum number of similar documents
            
        Returns:
            List of (document, similarity_score) tuples
        """
        # Get reference document
        ref_doc = self.registry.get_document_by_text_id(text_id)
        if not ref_doc:
            return []
        
        documents = self._get_documents()
        similarities = []
        
        for doc in documents:
            if doc.text_id == text_id:
                continue
            
            # Simple similarity based on metadata overlap
            similarity = self._calculate_similarity(ref_doc, doc)
            if similarity > 0:
                similarities.append((doc, similarity))
        
        # Sort by similarity and limit
        similarities.sort(key=lambda x: x[1], reverse=True)
        return similarities[:limit]
    
    def get_corpus_statistics(self, corpus_name: Optional[str] = None) -> CorpusStatistics:
        """
        Generate comprehensive corpus statistics.
        
        Args:
            corpus_name: Optional corpus name to filter by
            
        Returns:
            CorpusStatistics with comprehensive metrics
        """
        if self._statistics_cache is None or corpus_name:
            documents = self.registry.list_documents(corpus_name)
            
            stats = CorpusStatistics()
            stats.total_documents = len(documents)
            
            if not documents:
                return stats
            
            # Basic aggregations
            authors = set()
            total_size = 0
            dates = []
            doc_types = Counter()
            author_counts = Counter()
            file_formats = Counter()
            years_active = Counter()
            
            for doc in documents:
                # Authors
                if doc.author:
                    authors.add(doc.author)
                    author_counts[doc.author] += 1
                
                # File size
                total_size += doc.file_size
                
                # Dates
                if doc.date:
                    dates.append(doc.date)
                    years_active[doc.date.year] += 1
                
                # Document types
                if doc.document_type:
                    doc_types[doc.document_type] += 1
                
                # File formats
                if doc.file_format:
                    file_formats[doc.file_format] += 1
            
            # Set statistics
            stats.total_authors = len(authors)
            stats.total_file_size = total_size
            stats.document_types = dict(doc_types)
            stats.authors = dict(author_counts)
            stats.file_formats = dict(file_formats)
            stats.years_active = dict(years_active)
            
            # Date range
            if dates:
                stats.earliest_date = min(dates)
                stats.latest_date = max(dates)
                date_diff = stats.latest_date - stats.earliest_date
                stats.date_span_years = date_diff.days / 365.25
            
            if corpus_name is None:
                self._statistics_cache = stats
            
            return stats
        
        return self._statistics_cache
    
    def get_timeline(self, 
                    corpus_name: Optional[str] = None,
                    group_by: str = 'year') -> Dict[str, List[CorpusDocument]]:
        """
        Get corpus timeline grouped by time period.
        
        Args:
            corpus_name: Optional corpus name to filter by
            group_by: Time grouping ('year', 'decade', 'month')
            
        Returns:
            Dictionary mapping time periods to document lists
        """
        documents = self.registry.list_documents(corpus_name)
        timeline = defaultdict(list)
        
        for doc in documents:
            if not doc.date:
                timeline['Unknown'].append(doc)
                continue
            
            if group_by == 'year':
                key = str(doc.date.year)
            elif group_by == 'decade':
                key = f"{doc.date.year // 10 * 10}s"
            elif group_by == 'month':
                key = doc.date.strftime('%Y-%m')
            else:
                key = str(doc.date.year)
            
            timeline[key].append(doc)
        
        return dict(timeline)
    
    def export_catalog(self, 
                      output_path: Path,
                      format: str = 'csv',
                      corpus_name: Optional[str] = None) -> Path:
        """
        Export corpus catalog in various formats.
        
        Args:
            output_path: Path for output file
            format: Export format ('csv', 'json', 'tsv')
            corpus_name: Optional corpus name to filter by
            
        Returns:
            Path to created file
        """
        documents = self.registry.list_documents(corpus_name)
        
        if format.lower() == 'csv':
            return self._export_catalog_csv(documents, output_path)
        elif format.lower() == 'json':
            return self._export_catalog_json(documents, output_path)
        elif format.lower() == 'tsv':
            return self._export_catalog_tsv(documents, output_path)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    # Private helper methods
    
    def _get_documents(self) -> List[CorpusDocument]:
        """Get cached documents or load from registry."""
        if self._document_cache is None:
            self._document_cache = self.registry.list_documents()
        return self._document_cache
    
    def _apply_filters(self, 
                      documents: List[CorpusDocument],
                      filters: Dict[str, Union[str, List[str]]]) -> List[CorpusDocument]:
        """Apply metadata filters to document list."""
        filtered = []
        
        for doc in documents:
            matches = True
            
            for field, values in filters.items():
                if isinstance(values, str):
                    values = [values]
                
                if field == 'year':
                    doc_value = str(doc.date.year) if doc.date else None
                else:
                    doc_value = str(getattr(doc, field, None))
                
                if doc_value not in values:
                    matches = False
                    break
            
            if matches:
                filtered.append(doc)
        
        return filtered
    
    def _calculate_relevance(self, 
                           doc: CorpusDocument,
                           query: str,
                           fields: List[str],
                           include_content: bool) -> float:
        """Calculate relevance score for document against query."""
        query_lower = query.lower()
        query_terms = query_lower.split()
        score = 0.0
        
        # Field weights
        field_weights = {
            'title': 3.0,
            'author': 2.0,
            'document_type': 1.5,
            'content': 1.0
        }
        
        for field in fields:
            if field == 'content' and include_content:
                # Search in file content (expensive)
                try:
                    if doc.file_path.exists():
                        content = doc.file_path.read_text(encoding='utf-8', errors='ignore')
                        field_text = content.lower()
                    else:
                        continue
                except:
                    continue
            else:
                # Search in metadata
                field_value = getattr(doc, field, '')
                field_text = str(field_value).lower() if field_value else ''
            
            # Calculate matches
            weight = field_weights.get(field, 1.0)
            
            # Exact phrase match (highest score)
            if query_lower in field_text:
                score += weight * 2.0
            
            # Individual term matches
            for term in query_terms:
                if term in field_text:
                    score += weight * 0.5
        
        return score
    
    def _extract_match_context(self,
                             doc: CorpusDocument,
                             query: str,
                             fields: List[str],
                             include_content: bool) -> List[str]:
        """Extract context snippets around query matches."""
        contexts = []
        query_lower = query.lower()
        
        # Check metadata fields
        for field in fields:
            if field == 'content':
                continue
            
            field_value = getattr(doc, field, '')
            field_text = str(field_value) if field_value else ''
            
            if query_lower in field_text.lower():
                contexts.append(f"{field}: {field_text}")
        
        # Check content if requested
        if include_content and 'content' in fields:
            try:
                if doc.file_path.exists():
                    content = doc.file_path.read_text(encoding='utf-8', errors='ignore')
                    # Find first match and extract context
                    content_lower = content.lower()
                    match_pos = content_lower.find(query_lower)
                    if match_pos >= 0:
                        start = max(0, match_pos - 50)
                        end = min(len(content), match_pos + len(query) + 50)
                        context = content[start:end].strip()
                        contexts.append(f"content: ...{context}...")
            except:
                pass
        
        return contexts[:3]  # Limit to 3 contexts
    
    def _get_match_fields(self,
                         doc: CorpusDocument,
                         query: str,
                         fields: List[str],
                         include_content: bool) -> List[str]:
        """Get list of fields that matched the query."""
        match_fields = []
        query_lower = query.lower()
        
        for field in fields:
            if field == 'content' and include_content:
                try:
                    if doc.file_path.exists():
                        content = doc.file_path.read_text(encoding='utf-8', errors='ignore')
                        if query_lower in content.lower():
                            match_fields.append(field)
                except:
                    pass
            else:
                field_value = getattr(doc, field, '')
                field_text = str(field_value).lower() if field_value else ''
                if query_lower in field_text:
                    match_fields.append(field)
        
        return match_fields
    
    def _calculate_facets(self, documents: List[CorpusDocument]) -> Dict[str, Dict[str, int]]:
        """Calculate facet counts for search results."""
        facets = {
            'author': defaultdict(int),
            'document_type': defaultdict(int),
            'year': defaultdict(int),
            'decade': defaultdict(int)
        }
        
        for doc in documents:
            facets['author'][doc.author or 'Unknown'] += 1
            facets['document_type'][doc.document_type or 'Unknown'] += 1
            
            if doc.date:
                facets['year'][str(doc.date.year)] += 1
                facets['decade'][f"{doc.date.year // 10 * 10}s"] += 1
            else:
                facets['year']['Unknown'] += 1
                facets['decade']['Unknown'] += 1
        
        return {k: dict(v) for k, v in facets.items()}
    
    def _calculate_similarity(self, doc1: CorpusDocument, doc2: CorpusDocument) -> float:
        """Calculate similarity score between two documents."""
        similarity = 0.0
        
        # Same author
        if doc1.author == doc2.author:
            similarity += 0.4
        
        # Same document type
        if doc1.document_type == doc2.document_type:
            similarity += 0.3
        
        # Similar time period (within 5 years)
        if doc1.date and doc2.date:
            year_diff = abs(doc1.date.year - doc2.date.year)
            if year_diff <= 5:
                similarity += 0.3 * (1.0 - year_diff / 5.0)
        
        return similarity
    
    def _export_catalog_csv(self, documents: List[CorpusDocument], output_path: Path) -> Path:
        """Export catalog as CSV."""
        import csv
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Header
            writer.writerow([
                'text_id', 'uri', 'title', 'author', 'date', 'document_type',
                'file_path', 'file_size', 'publication', 'source_url',
                'content_hash', 'registered_at'
            ])
            
            # Data
            for doc in documents:
                writer.writerow([
                    doc.text_id,
                    doc.uri,
                    doc.title,
                    doc.author,
                    doc.date.isoformat() if doc.date else '',
                    doc.document_type,
                    str(doc.file_path),
                    doc.file_size,
                    doc.publication or '',
                    doc.source_url or '',
                    doc.content_hash,
                    doc.registered_at.isoformat() if doc.registered_at else ''
                ])
        
        return output_path
    
    def _export_catalog_json(self, documents: List[CorpusDocument], output_path: Path) -> Path:
        """Export catalog as JSON."""
        import json
        from dataclasses import asdict
        
        catalog_data = []
        for doc in documents:
            doc_dict = asdict(doc)
            # Convert Path and datetime objects to strings
            doc_dict['file_path'] = str(doc_dict['file_path'])
            if doc_dict['date']:
                doc_dict['date'] = doc_dict['date'].isoformat()
            if doc_dict['file_modified']:
                doc_dict['file_modified'] = doc_dict['file_modified'].isoformat()
            if doc_dict['registered_at']:
                doc_dict['registered_at'] = doc_dict['registered_at'].isoformat()
            
            catalog_data.append(doc_dict)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(catalog_data, f, indent=2, ensure_ascii=False)
        
        return output_path
    
    def _export_catalog_tsv(self, documents: List[CorpusDocument], output_path: Path) -> Path:
        """Export catalog as TSV."""
        # Similar to CSV but with tab delimiter
        import csv
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f, delimiter='\t')
            
            # Header
            writer.writerow([
                'text_id', 'uri', 'title', 'author', 'date', 'document_type',
                'file_path', 'file_size', 'publication', 'source_url',
                'content_hash', 'registered_at'
            ])
            
            # Data
            for doc in documents:
                writer.writerow([
                    doc.text_id,
                    doc.uri,
                    doc.title,
                    doc.author,
                    doc.date.isoformat() if doc.date else '',
                    doc.document_type,
                    str(doc.file_path),
                    doc.file_size,
                    doc.publication or '',
                    doc.source_url or '',
                    doc.content_hash,
                    doc.registered_at.isoformat() if doc.registered_at else ''
                ])
        
        return output_path 