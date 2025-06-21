"""
Corpus Registry - Enhanced corpus management with stable identifiers.

Provides:
- Stable URIs for corpus and document identification  
- Database integration while preserving file workflow
- FAIR data principles compliance
- Academic citation support
"""

import os
import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union, Tuple
from dataclasses import dataclass, asdict
from urllib.parse import urljoin

from sqlalchemy import text, create_engine
from src.utils.database import get_database_url

# Create a scoped engine for the registry
engine = create_engine(get_database_url())


@dataclass
class CorpusDocument:
    """Enhanced document representation with stable identifiers."""
    
    # Stable identifiers (FAIR compliance)
    uri: str                          # Stable URI for citations
    text_id: str                     # Semantic identifier (e.g., "lincoln_inaugural_1865")
    content_hash: str                # SHA-256 of content for integrity
    
    # Core metadata
    title: str
    author: str
    date: datetime
    document_type: str               # "inaugural", "sotu", "speech", etc.
    
    # File system integration
    file_path: Path                  # Path to source file
    file_format: str                 # "txt", "md", "csv"
    file_size: int                   # Bytes
    file_modified: datetime          # Last modification time
    
    # Optional metadata
    publication: Optional[str] = None
    medium: Optional[str] = None
    campaign_name: Optional[str] = None
    audience_size: Optional[int] = None
    source_url: Optional[str] = None
    
    # Academic metadata
    schema_version: str = "1.0.0"
    document_metadata: Dict = None   # JSONB field for flexible metadata
    
    # Registry metadata
    registered_at: Optional[datetime] = None
    registered_by: Optional[str] = None
    database_id: Optional[int] = None


class CorpusRegistry:
    """
    Enhanced corpus registry with stable identifiers and FAIR data compliance.
    
    Provides:
    - Stable URI generation for citations
    - Database integration with file system preservation
    - Content integrity validation
    - Academic metadata standards
    """
    
    def __init__(self, base_uri: str = "https://narrative-gravity.org/corpus"):
        self.base_uri = base_uri.rstrip('/')
        self.corpus_root = Path("corpus/golden_set")
        
    def generate_text_id(self, author: str, title: str, date: datetime, doc_type: str) -> str:
        """
        Generate semantic text identifier for stable referencing.
        
        Format: {author_last}_{type}_{year}[_{sequence}]
        Example: lincoln_inaugural_1865, obama_sotu_2009_01
        """
        # Extract last name, handle compound names
        author_parts = author.lower().split()
        author_last = author_parts[-1] if author_parts else "unknown"
        
        # Clean author name
        author_clean = ''.join(c for c in author_last if c.isalnum())
        
        # Clean document type
        type_clean = ''.join(c for c in doc_type.lower() if c.isalnum())
        
        # Base ID
        base_id = f"{author_clean}_{type_clean}_{date.year}"
        
        # Check for conflicts and add sequence number if needed
        sequence = 1
        candidate_id = base_id
        
        while self._text_id_exists(candidate_id):
            candidate_id = f"{base_id}_{sequence:02d}"
            sequence += 1
            
        return candidate_id
    
    def generate_uri(self, text_id: str) -> str:
        """Generate stable URI for document citation (FUTURE: not yet implemented)."""
        # TODO: Implement actual web service at base_uri before enabling
        # return f"{self.base_uri}/document/{text_id}"
        return f"placeholder://corpus/{text_id}"  # Placeholder until web service exists
    
    def calculate_content_hash(self, file_path: Path) -> str:
        """Calculate SHA-256 hash of file content for integrity checking."""
        hasher = hashlib.sha256()
        with open(file_path, 'rb') as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hasher.update(chunk)
        return hasher.hexdigest()
    
    def register_document(self, 
                         file_path: Union[str, Path],
                         title: str,
                         author: str,
                         date: datetime,
                         document_type: str,
                         **metadata) -> CorpusDocument:
        """
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
        """
        file_path = Path(file_path)
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        # Generate stable identifiers
        text_id = metadata.get('text_id') or self.generate_text_id(author, title, date, document_type)
        uri = self.generate_uri(text_id)
        content_hash = self.calculate_content_hash(file_path)
        
        # File metadata
        stat = file_path.stat()
        file_size = stat.st_size
        file_modified = datetime.fromtimestamp(stat.st_mtime)
        file_format = file_path.suffix.lstrip('.')
        
        # Create document object
        doc = CorpusDocument(
            uri=uri,
            text_id=text_id,
            content_hash=content_hash,
            title=title,
            author=author,
            date=date,
            document_type=document_type,
            file_path=file_path,
            file_format=file_format,
            file_size=file_size,
            file_modified=file_modified,
            publication=metadata.get('publication'),
            medium=metadata.get('medium'),
            campaign_name=metadata.get('campaign_name'),
            audience_size=metadata.get('audience_size'),
            source_url=metadata.get('source_url'),
            document_metadata=metadata.get('document_metadata', {}),
            registered_at=datetime.now(),
            registered_by=metadata.get('registered_by', 'system')
        )
        
        # Save to database
        self._save_to_database(doc)
        
        return doc
    
    def register_corpus_directory(self, 
                                 directory: Union[str, Path],
                                 corpus_name: str,
                                 metadata_file: Optional[str] = None) -> List[CorpusDocument]:
        """
        Register all documents in a directory as a corpus.
        
        Args:
            directory: Directory containing corpus files
            corpus_name: Name for the corpus
            metadata_file: Optional CSV/JSON file with document metadata
            
        Returns:
            List of registered CorpusDocument objects
        """
        directory = Path(directory)
        if not directory.exists():
            raise FileNotFoundError(f"Directory not found: {directory}")
        
        # Load metadata if provided
        doc_metadata = {}
        if metadata_file:
            doc_metadata = self._load_metadata_file(Path(metadata_file))
        
        # Register corpus in database
        corpus_id = self._create_corpus_record(corpus_name, len(list(directory.glob("*.txt"))))
        
        # Register each document
        documents = []
        for file_path in directory.glob("*.txt"):
            try:
                # Extract metadata from filename or metadata file
                file_metadata = doc_metadata.get(file_path.name, {})
                
                # Parse filename for basic metadata if not in metadata file
                if not file_metadata:
                    file_metadata = self._parse_filename_metadata(file_path.name)
                
                doc = self.register_document(
                    file_path=file_path,
                    corpus_id=corpus_id,
                    **file_metadata
                )
                documents.append(doc)
                
            except Exception as e:
                print(f"Warning: Failed to register {file_path.name}: {e}")
                continue
        
        print(f"✅ Registered {len(documents)} documents in corpus '{corpus_name}'")
        return documents
    
    def get_document_by_text_id(self, text_id: str) -> Optional[CorpusDocument]:
        """Retrieve document by text_id."""
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT * FROM document WHERE text_id = :text_id
            """), {"text_id": text_id}).fetchone()
            
            if not result:
                return None
            
            return self._row_to_document(result)
    
    def get_document_by_uri(self, uri: str) -> Optional[CorpusDocument]:
        """Retrieve document by URI."""
        # Extract text_id from URI
        if not uri.startswith(self.base_uri):
            return None
        
        text_id = uri.split('/')[-1]
        return self.get_document_by_text_id(text_id)
    
    def list_documents(self, corpus_name: Optional[str] = None) -> List[CorpusDocument]:
        """List all registered documents, optionally filtered by corpus."""
        with engine.connect() as conn:
            if corpus_name:
                result = conn.execute(text("""
                    SELECT d.* FROM document d
                    JOIN corpus c ON d.corpus_id = c.id
                    WHERE c.name = :corpus_name
                    ORDER BY d.date, d.title
                """), {"corpus_name": corpus_name}).fetchall()
            else:
                result = conn.execute(text("""
                    SELECT * FROM document 
                    ORDER BY date, title
                """)).fetchall()
            
            return [self._row_to_document(row) for row in result]
    
    def validate_integrity(self) -> Dict[str, List[str]]:
        """
        Validate corpus integrity - check files exist and hashes match.
        
        Returns:
            Dictionary with 'valid', 'missing_files', 'hash_mismatches', 'errors'
        """
        results = {
            'valid': [],
            'missing_files': [],
            'hash_mismatches': [],
            'errors': []
        }
        
        documents = self.list_documents()
        
        for doc in documents:
            try:
                if not doc.file_path.exists():
                    results['missing_files'].append(doc.text_id)
                    continue
                
                current_hash = self.calculate_content_hash(doc.file_path)
                if current_hash != doc.content_hash:
                    results['hash_mismatches'].append(doc.text_id)
                    continue
                
                results['valid'].append(doc.text_id)
                
            except Exception as e:
                results['errors'].append(f"{doc.text_id}: {str(e)}")
        
        return results
    
    # Private helper methods
    
    def _text_id_exists(self, text_id: str) -> bool:
        """Check if text_id already exists in database."""
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT COUNT(*) FROM document WHERE text_id = :text_id
            """), {"text_id": text_id}).fetchone()
            
            return result[0] > 0
    
    def _save_to_database(self, doc: CorpusDocument) -> None:
        """Save document to database."""
        with engine.connect() as conn:
            # Check if corpus exists, create if not
            corpus_result = conn.execute(text("""
                SELECT id FROM corpus WHERE name = 'presidential_speeches'
            """)).fetchone()
            
            if not corpus_result:
                corpus_id = self._create_corpus_record('presidential_speeches', 1)
            else:
                corpus_id = corpus_result[0]
            
            # Insert document
            result = conn.execute(text("""
                INSERT INTO document (
                    corpus_id, text_id, title, document_type, author, date,
                    publication, medium, campaign_name, audience_size, source_url,
                    schema_version, document_metadata, created_at, updated_at
                ) VALUES (
                    :corpus_id, :text_id, :title, :document_type, :author, :date,
                    :publication, :medium, :campaign_name, :audience_size, :source_url,
                    :schema_version, :document_metadata, :created_at, :updated_at
                )
                RETURNING id
            """), {
                "corpus_id": corpus_id,
                "text_id": doc.text_id,
                "title": doc.title,
                "document_type": doc.document_type,
                "author": doc.author,
                "date": doc.date,
                "publication": doc.publication,
                "medium": doc.medium,
                "campaign_name": doc.campaign_name,
                "audience_size": doc.audience_size,
                "source_url": doc.source_url,
                "schema_version": doc.schema_version,
                "document_metadata": json.dumps(doc.document_metadata or {}),
                "created_at": doc.registered_at,
                "updated_at": doc.registered_at
            })
            
            doc.database_id = result.fetchone()[0]
            conn.commit()
    
    def _create_corpus_record(self, name: str, record_count: int) -> int:
        """Create corpus record in database."""
        with engine.connect() as conn:
            result = conn.execute(text("""
                INSERT INTO corpus (name, upload_timestamp, record_count, description)
                VALUES (:name, :timestamp, :count, :description)
                RETURNING id
            """), {
                "name": name,
                "timestamp": datetime.now(),
                "count": record_count,
                "description": f"Enhanced corpus registry: {name}"
            })
            
            corpus_id = result.fetchone()[0]
            conn.commit()
            return corpus_id
    
    def _parse_filename_metadata(self, filename: str) -> Dict:
        """Parse basic metadata from filename patterns like 'golden_author_type_seq.txt'."""
        # Remove extension and 'golden_' prefix
        base = filename.replace('.txt', '').replace('golden_', '')
        parts = base.split('_')
        
        if len(parts) >= 3:
            author = parts[0].title()
            doc_type = parts[1].lower()
            sequence = parts[2] if len(parts) > 2 else "01"
            
            # Default metadata - would be enhanced with actual data
            return {
                'title': f"{author} {doc_type.title()} {sequence}",
                'author': author,
                'date': datetime(2020, 1, 1),  # Placeholder
                'document_type': doc_type
            }
        
        # Fallback
        return {
            'title': filename,
            'author': 'Unknown',
            'date': datetime(2020, 1, 1),
            'document_type': 'speech'
        }
    
    def _load_metadata_file(self, metadata_path: Path) -> Dict:
        """Load document metadata from CSV or JSON file."""
        # Implementation would parse CSV/JSON metadata
        # For now, return empty dict
        return {}
    
    def _row_to_document(self, row) -> CorpusDocument:
        """Convert database row to CorpusDocument object."""
        # This would need to be implemented based on the actual row structure
        # For now, returning a basic implementation
        return CorpusDocument(
            uri=self.generate_uri(row.text_id),
            text_id=row.text_id,
            content_hash="",  # Would need to be calculated or stored
            title=row.title,
            author=row.author,
            date=row.date,
            document_type=row.document_type,
            file_path=Path(f"corpus/golden_set/presidential_speeches/txt/{row.text_id}.txt"),
            file_format="txt",
            file_size=0,  # Would need to be calculated
            file_modified=datetime.now(),
            publication=row.publication,
            medium=row.medium,
            campaign_name=row.campaign_name,
            audience_size=row.audience_size,
            source_url=row.source_url,
            schema_version=row.schema_version,
            document_metadata=row.document_metadata if row.document_metadata else {},
            registered_at=row.created_at,
            database_id=row.id
        ) 