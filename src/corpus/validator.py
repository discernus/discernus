"""
Corpus Validator - Integrity checking and FAIR data compliance validation.

Provides:
- File integrity validation (existence, hashes, permissions)
- Metadata completeness checking
- FAIR data principles compliance assessment
- Academic standards validation
"""

import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
from dataclasses import dataclass, field

from .registry import CorpusRegistry, CorpusDocument


@dataclass
class ValidationResult:
    """Results of corpus validation."""
    
    # Overall status
    is_valid: bool = False
    total_documents: int = 0
    valid_documents: int = 0
    
    # File integrity issues
    missing_files: List[str] = field(default_factory=list)
    hash_mismatches: List[str] = field(default_factory=list)
    permission_errors: List[str] = field(default_factory=list)
    
    # Metadata issues
    missing_metadata: List[Tuple[str, str]] = field(default_factory=list)  # (text_id, field)
    invalid_dates: List[str] = field(default_factory=list)
    duplicate_text_ids: List[str] = field(default_factory=list)
    
    # FAIR compliance issues
    missing_stable_ids: List[str] = field(default_factory=list)
    missing_descriptions: List[str] = field(default_factory=list)
    access_restrictions: List[str] = field(default_factory=list)
    
    # Academic standards
    citation_format_issues: List[str] = field(default_factory=list)
    schema_version_mismatches: List[str] = field(default_factory=list)
    
    # Warnings (non-critical)
    warnings: List[str] = field(default_factory=list)
    
    def summary(self) -> str:
        """Generate human-readable validation summary."""
        lines = [
            f"📊 Validation Summary",
            f"=" * 50,
            f"Documents: {self.valid_documents}/{self.total_documents} valid",
            f"Overall Status: {'✅ VALID' if self.is_valid else '❌ INVALID'}",
            ""
        ]
        
        if self.missing_files:
            lines.extend([
                "🚨 Missing Files:",
                *[f"  - {text_id}" for text_id in self.missing_files],
                ""
            ])
        
        if self.hash_mismatches:
            lines.extend([
                "🔍 Hash Mismatches (content changed):",
                *[f"  - {text_id}" for text_id in self.hash_mismatches], 
                ""
            ])
        
        if self.missing_metadata:
            lines.extend([
                "📝 Missing Metadata:",
                *[f"  - {text_id}: {field}" for text_id, field in self.missing_metadata],
                ""
            ])
        
        if self.duplicate_text_ids:
            lines.extend([
                "🔄 Duplicate Text IDs:",
                *[f"  - {text_id}" for text_id in self.duplicate_text_ids],
                ""
            ])
        
        if self.warnings:
            lines.extend([
                "⚠️  Warnings:",
                *[f"  - {warning}" for warning in self.warnings], 
                ""
            ])
        
        return "\n".join(lines)


class CorpusValidator:
    """
    Comprehensive corpus validation for integrity and academic standards.
    
    Validates:
    - File integrity (existence, content hashes, permissions)
    - Metadata completeness and consistency
    - FAIR data principles compliance
    - Academic citation standards
    - Text ID uniqueness and format
    """
    
    def __init__(self, registry: Optional[CorpusRegistry] = None):
        self.registry = registry or CorpusRegistry()
        
        # Required metadata fields for academic compliance
        self.required_fields = {
            'title', 'author', 'date', 'document_type'
        }
        
        # Recommended fields for FAIR compliance
        self.recommended_fields = {
            'publication', 'source_url', 'medium', 'schema_version'
        }
        
        # Generic document type categories (framework-agnostic)
        self.generic_document_types = {
            'text', 'document', 'speech', 'article', 'media', 
            'manuscript', 'correspondence', 'other'
        }
    
    def validate_corpus(self, corpus_name: Optional[str] = None) -> ValidationResult:
        """
        Comprehensive corpus validation.
        
        Args:
            corpus_name: Optional corpus name to validate specific corpus
            
        Returns:
            ValidationResult with all validation findings
        """
        result = ValidationResult()
        
        # Get documents to validate
        documents = self.registry.list_documents(corpus_name)
        result.total_documents = len(documents)
        
        if not documents:
            result.warnings.append("No documents found in corpus")
            return result
        
        # Track text_ids for duplicate detection
        text_ids_seen = set()
        
        # Validate each document
        for doc in documents:
            doc_valid = True
            
            # File integrity checks
            if not self._validate_file_integrity(doc, result):
                doc_valid = False
            
            # Metadata validation
            if not self._validate_metadata(doc, result):
                doc_valid = False
            
            # Text ID validation
            if not self._validate_text_id(doc, result, text_ids_seen):
                doc_valid = False
            
            # FAIR compliance
            self._check_fair_compliance(doc, result)
            
            # Academic standards
            self._check_academic_standards(doc, result)
            
            if doc_valid:
                result.valid_documents += 1
        
        # Overall validation
        result.is_valid = (
            result.valid_documents == result.total_documents and
            not result.missing_files and
            not result.hash_mismatches and
            not result.duplicate_text_ids and
            not result.invalid_dates
        )
        
        return result
    
    def validate_document(self, doc: CorpusDocument) -> Dict[str, List[str]]:
        """
        Validate a single document.
        
        Returns:
            Dictionary with validation issues by category
        """
        issues = {
            'file_integrity': [],
            'metadata': [],
            'text_id': [],
            'fair_compliance': [],
            'academic_standards': []
        }
        
        result = ValidationResult()  # Temporary result for helper methods
        
        # File integrity
        if not self._validate_file_integrity(doc, result):
            if doc.text_id in result.missing_files:
                issues['file_integrity'].append("File not found")
            if doc.text_id in result.hash_mismatches:
                issues['file_integrity'].append("Content hash mismatch")
            if doc.text_id in result.permission_errors:
                issues['file_integrity'].append("Permission denied")
        
        # Metadata
        if not self._validate_metadata(doc, result):
            for text_id, field in result.missing_metadata:
                if text_id == doc.text_id:
                    issues['metadata'].append(f"Missing {field}")
            if doc.text_id in result.invalid_dates:
                issues['metadata'].append("Invalid date format")
        
        # Text ID format
        text_ids_seen = set()
        if not self._validate_text_id(doc, result, text_ids_seen):
            issues['text_id'].append("Invalid text_id format")
        
        # FAIR compliance
        self._check_fair_compliance(doc, result)
        if doc.text_id in result.missing_stable_ids:
            issues['fair_compliance'].append("Missing stable identifier")
        if doc.text_id in result.missing_descriptions:
            issues['fair_compliance'].append("Missing description")
        
        # Academic standards
        self._check_academic_standards(doc, result)
        if doc.text_id in result.citation_format_issues:
            issues['academic_standards'].append("Citation format issues")
        if doc.text_id in result.schema_version_mismatches:
            issues['academic_standards'].append("Schema version mismatch")
        
        return {k: v for k, v in issues.items() if v}  # Only return categories with issues
    
    def check_fair_compliance(self, corpus_name: Optional[str] = None) -> Dict[str, float]:
        """
        Check FAIR data principles compliance.
        
        Returns:
            Dictionary with compliance scores (0.0-1.0) for each FAIR principle
        """
        documents = self.registry.list_documents(corpus_name)
        
        if not documents:
            return {'findable': 0.0, 'accessible': 0.0, 'interoperable': 0.0, 'reusable': 0.0}
        
        scores = {
            'findable': 0.0,
            'accessible': 0.0, 
            'interoperable': 0.0,
            'reusable': 0.0
        }
        
        for doc in documents:
            # Findable: stable identifiers, metadata, searchable
            findable_score = 0.0
            if doc.text_id:
                findable_score += 0.2  # Text identifier (not yet resolvable URI)
            # TODO: Add 0.2 more when stable URIs are actually resolvable
            if doc.title and doc.author:
                findable_score += 0.4  # Basic metadata (increased weight)
            if doc.document_metadata:
                findable_score += 0.4  # Rich metadata (increased weight)
            
            # Accessible: file exists, readable, documented access
            accessible_score = 0.0
            if doc.file_path.exists():
                accessible_score += 0.5  # File exists
            try:
                if doc.file_path.is_file() and doc.file_path.stat().st_size > 0:
                    accessible_score += 0.3  # File readable
            except:
                pass
            if doc.source_url:
                accessible_score += 0.2  # Source documented
            
            # Interoperable: standard format, schema, linked data
            interoperable_score = 0.0
            if doc.file_format in ['txt', 'csv', 'json']:
                interoperable_score += 0.4  # Standard format
            if doc.schema_version:
                interoperable_score += 0.3  # Schema versioned
            if doc.document_metadata:
                interoperable_score += 0.3  # Structured metadata
            
            # Reusable: license, provenance, standards
            reusable_score = 0.0
            if doc.author and doc.date:
                reusable_score += 0.4  # Provenance
            if doc.publication or doc.source_url:
                reusable_score += 0.3  # Attribution
            if doc.document_type in self.generic_document_types:
                reusable_score += 0.3  # Generic categories
            elif doc.document_type:  # Framework-specific types also acceptable
                reusable_score += 0.2  # Slightly lower score for specificity
            
            # Accumulate scores
            scores['findable'] += findable_score
            scores['accessible'] += accessible_score
            scores['interoperable'] += interoperable_score
            scores['reusable'] += reusable_score
        
        # Average scores
        num_docs = len(documents)
        return {k: v / num_docs for k, v in scores.items()}
    
    def generate_compliance_report(self, corpus_name: Optional[str] = None) -> str:
        """Generate comprehensive FAIR compliance report."""
        validation = self.validate_corpus(corpus_name)
        fair_scores = self.check_fair_compliance(corpus_name)
        
        lines = [
            f"📋 Corpus Compliance Report",
            f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"Corpus: {corpus_name or 'All corpora'}",
            "=" * 60,
            "",
            "🎯 FAIR Data Principles Compliance:",
            f"  Findable:      {fair_scores['findable']:.1%}",
            f"  Accessible:    {fair_scores['accessible']:.1%}", 
            f"  Interoperable: {fair_scores['interoperable']:.1%}",
            f"  Reusable:      {fair_scores['reusable']:.1%}",
            f"  Overall:       {sum(fair_scores.values())/4:.1%}",
            "",
            validation.summary()
        ]
        
        return "\n".join(lines)
    
    # Private validation methods
    
    def _validate_file_integrity(self, doc: CorpusDocument, result: ValidationResult) -> bool:
        """Validate file exists and content matches hash."""
        valid = True
        
        # Check file exists
        if not doc.file_path.exists():
            result.missing_files.append(doc.text_id)
            valid = False
            return valid
        
        # Check permissions
        try:
            if not doc.file_path.is_file():
                result.permission_errors.append(doc.text_id)
                valid = False
        except PermissionError:
            result.permission_errors.append(doc.text_id)
            valid = False
        
        # Check content hash if available
        if doc.content_hash:
            try:
                current_hash = self.registry.calculate_content_hash(doc.file_path)
                if current_hash != doc.content_hash:
                    result.hash_mismatches.append(doc.text_id)
                    valid = False
            except Exception:
                result.warnings.append(f"Could not calculate hash for {doc.text_id}")
        
        return valid
    
    def _validate_metadata(self, doc: CorpusDocument, result: ValidationResult) -> bool:
        """Validate required metadata fields."""
        valid = True
        
        # Check required fields
        for field in self.required_fields:
            value = getattr(doc, field, None)
            if not value:
                result.missing_metadata.append((doc.text_id, field))
                valid = False
        
        # Validate date format
        if doc.date:
            if not isinstance(doc.date, datetime):
                result.invalid_dates.append(doc.text_id)
                valid = False
        else:
            result.missing_metadata.append((doc.text_id, 'date'))
            valid = False
        
        # Check document type (framework-agnostic validation)
        if doc.document_type not in self.generic_document_types:
            result.warnings.append(f"{doc.text_id}: non-generic document_type '{doc.document_type}' (framework-specific types are acceptable)")
        
        return valid
    
    def _validate_text_id(self, doc: CorpusDocument, result: ValidationResult, text_ids_seen: Set[str]) -> bool:
        """Validate text_id format and uniqueness."""
        valid = True
        
        # Check format (author_type_year or author_type_year_seq)
        pattern = r'^[a-z]+_[a-z]+_\d{4}(_\d{2})?$'
        if not re.match(pattern, doc.text_id):
            result.warnings.append(f"{doc.text_id}: non-standard text_id format")
        
        # Check uniqueness
        if doc.text_id in text_ids_seen:
            result.duplicate_text_ids.append(doc.text_id)
            valid = False
        else:
            text_ids_seen.add(doc.text_id)
        
        return valid
    
    def _check_fair_compliance(self, doc: CorpusDocument, result: ValidationResult) -> None:
        """Check FAIR data principles compliance."""
        
        # Findable: stable identifiers (currently placeholder URIs only)
        if not doc.text_id:
            result.missing_stable_ids.append(doc.text_id)
        # Note: URIs are placeholder until web service is implemented
        
        # Findable: rich metadata 
        if not doc.document_metadata or len(doc.document_metadata) < 2:
            result.missing_descriptions.append(doc.text_id)
        
        # Accessible: file accessibility (already checked in file integrity)
        # Interoperable: standard formats (txt/csv/json are good)
        # Reusable: license and provenance info
        if not doc.source_url and not doc.publication:
            result.warnings.append(f"{doc.text_id}: missing provenance information")
    
    def _check_academic_standards(self, doc: CorpusDocument, result: ValidationResult) -> None:
        """Check academic citation and metadata standards."""
        
        # Schema version consistency
        expected_version = "1.0.0"
        if doc.schema_version != expected_version:
            result.schema_version_mismatches.append(doc.text_id)
        
        # Citation format (author, date, title minimum)
        citation_elements = [doc.author, doc.date, doc.title]
        if not all(citation_elements):
            result.citation_format_issues.append(doc.text_id)
        
        # Recommended fields for academic use
        for field in self.recommended_fields:
            if not getattr(doc, field, None):
                result.warnings.append(f"{doc.text_id}: missing recommended field '{field}'") 