#!/usr/bin/env python3
"""
JSONL Corpus Generator for Narrative Gravity Analysis

Converts various source formats (CSV, Markdown, plain text) to JSONL format
compliant with the core schema. Supports multiple chunking strategies and
validates output against schema.
"""

import json
import argparse
import sys
import csv
import re
from pathlib import Path
from typing import Dict, Any, List, Union, Optional
from datetime import datetime, timezone
import hashlib
import jsonschema
try:
    import yaml
except ImportError:
    yaml = None
from dataclasses import dataclass, asdict
import uuid
import math

@dataclass
class DocumentMetadata:
    """Structured document metadata"""
    text_id: str
    title: str
    document_type: str
    author: str
    date: str
    publication: Optional[str] = None
    medium: Optional[str] = None
    campaign_name: Optional[str] = None
    audience_size: Optional[int] = None
    source_url: Optional[str] = None
    schema_version: str = "1.0.0"
    document_metadata: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.document_metadata is None:
            self.document_metadata = {}

@dataclass
class ChunkData:
    """Structured chunk information"""
    chunk_id: int
    total_chunks: int
    chunk_type: str
    chunk_size: int
    chunk_overlap: Optional[int] = None
    document_position: float = 0.0
    word_count: int = 0
    unique_words: int = 0
    word_density: float = 0.0
    chunk_content: str = ""
    framework_data: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.framework_data is None:
            self.framework_data = {}

class TextChunker:
    """Handles different text chunking strategies"""
    
    @staticmethod
    def count_words(text: str) -> int:
        """Count words in text"""
        return len(text.split())
    
    @staticmethod
    def count_unique_words(text: str) -> int:
        """Count unique words in text (case-insensitive)"""
        words = text.lower().split()
        return len(set(words))
    
    @staticmethod
    def calculate_word_density(text: str) -> float:
        """Calculate word density (unique words / total words)"""
        total = TextChunker.count_words(text)
        unique = TextChunker.count_unique_words(text)
        return unique / total if total > 0 else 0.0
    
    @staticmethod
    def fixed_chunking(text: str, chunk_size: int = 1000, overlap: int = 100) -> List[str]:
        """Split text into fixed-size chunks with overlap"""
        if not text:
            return []
        
        chunks = []
        start = 0
        
        while start < len(text):
            end = min(start + chunk_size, len(text))
            chunk = text[start:end]
            
            # Try to break at word boundaries
            if end < len(text) and not text[end].isspace():
                # Find the last space before the end
                space_pos = chunk.rfind(' ')
                if space_pos > 0 and space_pos > chunk_size // 2:  # Don't make chunks too small
                    end = start + space_pos
                    chunk = text[start:end]
            
            chunk_content = chunk.strip()
            if chunk_content:  # Only add non-empty chunks
                chunks.append(chunk_content)
            
            # Move start position for next chunk
            start = max(start + 1, end - overlap)  # Ensure we make progress
            
            if start >= len(text):
                break
        
        return chunks
    
    @staticmethod
    def sectional_chunking(text: str, section_markers: List[str] = None) -> List[str]:
        """Split text by section markers (headings, paragraphs, etc.)"""
        if section_markers is None:
            section_markers = [
                r'\n\s*#{1,6}\s+',  # Markdown headers
                r'\n\s*\d+\.\s+',   # Numbered sections
                r'\n\s*[A-Z][^.]*:\s*\n',  # Labeled sections
                r'\n\s*\n\s*',      # Double newlines (paragraphs)
            ]
        
        # Create a pattern that matches any of the section markers
        pattern = '|'.join(f'({marker})' for marker in section_markers)
        
        # Split by pattern but keep the separators
        parts = re.split(pattern, text)
        
        chunks = []
        current_chunk = ""
        
        for part in parts:
            if part is None:
                continue
                
            # If this is a separator, start a new chunk
            if any(re.match(marker, part) for marker in section_markers):
                if current_chunk.strip():
                    chunks.append(current_chunk.strip())
                current_chunk = part
            else:
                current_chunk += part
        
        # Add the last chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return [c for c in chunks if c and len(c) > 20]  # Filter out very short chunks
    
    @staticmethod
    def semantic_chunking(text: str, max_chunk_size: int = 1500) -> List[str]:
        """Semantic chunking based on sentence and paragraph boundaries"""
        if not text:
            return []
        
        # Split into sentences
        sentence_pattern = r'[.!?]+\s+'
        sentences = re.split(sentence_pattern, text)
        
        chunks = []
        current_chunk = ""
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Check if adding this sentence would exceed max size
            if current_chunk and len(current_chunk) + len(sentence) > max_chunk_size:
                # Try to find a good break point
                paragraphs = current_chunk.split('\n\n')
                if len(paragraphs) > 1:
                    # Break at paragraph boundary
                    chunks.append('\n\n'.join(paragraphs[:-1]).strip())
                    current_chunk = paragraphs[-1] + ' ' + sentence
                else:
                    # No good break point, just split here
                    chunks.append(current_chunk.strip())
                    current_chunk = sentence
            else:
                if current_chunk:
                    current_chunk += ' ' + sentence
                else:
                    current_chunk = sentence
        
        # Add the last chunk
        if current_chunk.strip():
            chunks.append(current_chunk.strip())
        
        return chunks

class SourceParser:
    """Parse various source formats into structured data"""
    
    @staticmethod
    def parse_frontmatter(content: str) -> tuple:
        """Parse YAML frontmatter from content"""
        if not content.startswith('---'):
            return {}, content
        
        if yaml is None:
            print("Warning: PyYAML not installed, skipping frontmatter parsing")
            return {}, content
        
        try:
            # Find the end of frontmatter
            end_marker = content.find('---', 3)
            if end_marker == -1:
                return {}, content
            
            frontmatter_text = content[3:end_marker].strip()
            remaining_content = content[end_marker + 3:].strip()
            
            metadata = yaml.safe_load(frontmatter_text) or {}
            return metadata, remaining_content
        
        except Exception as e:
            print(f"Warning: Failed to parse frontmatter: {e}")
            return {}, content
    
    @staticmethod
    def parse_markdown(file_path: Path) -> List[Dict[str, Any]]:
        """Parse markdown file with optional frontmatter"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        frontmatter, text_content = SourceParser.parse_frontmatter(content)
        
        # Extract metadata with defaults
        doc_metadata = DocumentMetadata(
            text_id=frontmatter.get('text_id', file_path.stem),
            title=frontmatter.get('title', file_path.stem.replace('_', ' ').title()),
            document_type=frontmatter.get('document_type', 'other'),
            author=frontmatter.get('author', 'Unknown'),
            date=frontmatter.get('date', datetime.now(timezone.utc).isoformat()),
            publication=frontmatter.get('publication'),
            medium=frontmatter.get('medium'),
            campaign_name=frontmatter.get('campaign_name'),
            audience_size=frontmatter.get('audience_size'),
            source_url=frontmatter.get('source_url'),
            document_metadata=frontmatter.get('document_metadata', {})
        )
        
        return [{'metadata': doc_metadata, 'content': text_content}]
    
    @staticmethod
    def parse_csv(file_path: Path, text_column: str = 'content', 
                  metadata_columns: List[str] = None) -> List[Dict[str, Any]]:
        """Parse CSV file with text and metadata columns"""
        documents = []
        
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for i, row in enumerate(reader):
                if text_column not in row:
                    raise ValueError(f"Text column '{text_column}' not found in CSV")
                
                # Extract text content
                content = row[text_column].strip()
                if not content:
                    continue
                
                # Build metadata
                text_id = row.get('text_id', f"{file_path.stem}_{i}")
                
                doc_metadata = DocumentMetadata(
                    text_id=text_id,
                    title=row.get('title', f"Document {i}"),
                    document_type=row.get('document_type', 'other'),
                    author=row.get('author', 'Unknown'),
                    date=row.get('date', datetime.now(timezone.utc).isoformat()),
                    publication=row.get('publication'),
                    medium=row.get('medium'),
                    campaign_name=row.get('campaign_name'),
                    audience_size=int(row['audience_size']) if row.get('audience_size') else None,
                    source_url=row.get('source_url'),
                    document_metadata={}
                )
                
                # Add extra metadata columns
                if metadata_columns:
                    for col in metadata_columns:
                        if col in row:
                            doc_metadata.document_metadata[col] = row[col]
                
                documents.append({'metadata': doc_metadata, 'content': content})
        
        return documents
    
    @staticmethod
    def parse_plain_text(file_path: Path, metadata: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Parse plain text file with optional metadata"""
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # Use provided metadata or defaults
        if metadata is None:
            metadata = {}
        
        doc_metadata = DocumentMetadata(
            text_id=metadata.get('text_id', file_path.stem),
            title=metadata.get('title', file_path.stem.replace('_', ' ').title()),
            document_type=metadata.get('document_type', 'other'),
            author=metadata.get('author', 'Unknown'),
            date=metadata.get('date', datetime.now(timezone.utc).isoformat()),
            publication=metadata.get('publication'),
            medium=metadata.get('medium'),
            campaign_name=metadata.get('campaign_name'),
            audience_size=metadata.get('audience_size'),
            source_url=metadata.get('source_url'),
            document_metadata=metadata.get('document_metadata', {})
        )
        
        return [{'metadata': doc_metadata, 'content': content}]

class JSONLGenerator:
    """Main JSONL corpus generator"""
    
    def __init__(self, schema_path: Path = None):
        self.schema = None
        if schema_path:
            self.load_schema(schema_path)
        
        self.chunker = TextChunker()
        self.parser = SourceParser()
    
    def load_schema(self, schema_path: Path):
        """Load JSON schema for validation"""
        with open(schema_path, 'r', encoding='utf-8') as f:
            self.schema = json.load(f)
    
    def create_chunk_record(self, doc_metadata: DocumentMetadata, 
                          chunk_data: ChunkData) -> Dict[str, Any]:
        """Create a complete chunk record"""
        return {
            "document": asdict(doc_metadata),
            "chunk_id": chunk_data.chunk_id,
            "total_chunks": chunk_data.total_chunks,
            "chunk_type": chunk_data.chunk_type,
            "chunk_size": chunk_data.chunk_size,
            "chunk_overlap": chunk_data.chunk_overlap,
            "document_position": chunk_data.document_position,
            "word_count": chunk_data.word_count,
            "unique_words": chunk_data.unique_words,
            "word_density": chunk_data.word_density,
            "chunk_content": chunk_data.chunk_content,
            "framework_data": chunk_data.framework_data
        }
    
    def process_document(self, doc_data: Dict[str, Any], 
                        chunk_type: str = "fixed",
                        chunk_size: int = 1000,
                        chunk_overlap: int = 100) -> List[Dict[str, Any]]:
        """Process a single document into chunks"""
        doc_metadata = doc_data['metadata']
        content = doc_data['content']
        
        # Apply chunking strategy
        if chunk_type == "fixed":
            chunks = self.chunker.fixed_chunking(content, chunk_size, chunk_overlap)
        elif chunk_type == "sectional":
            chunks = self.chunker.sectional_chunking(content)
        elif chunk_type == "semantic":
            chunks = self.chunker.semantic_chunking(content, chunk_size)
        else:
            raise ValueError(f"Unknown chunking type: {chunk_type}")
        
        if not chunks:
            # Fallback to single chunk if no chunks generated
            chunks = [content]
        
        # Create chunk records
        records = []
        total_chunks = len(chunks)
        
        for i, chunk_content in enumerate(chunks):
            # Calculate position in document
            position = i / total_chunks if total_chunks > 1 else 0.0
            
            chunk_data = ChunkData(
                chunk_id=i,
                total_chunks=total_chunks,
                chunk_type=chunk_type,
                chunk_size=len(chunk_content),
                chunk_overlap=chunk_overlap if chunk_type == "fixed" else None,
                document_position=position,
                word_count=self.chunker.count_words(chunk_content),
                unique_words=self.chunker.count_unique_words(chunk_content),
                word_density=self.chunker.calculate_word_density(chunk_content),
                chunk_content=chunk_content
            )
            
            record = self.create_chunk_record(doc_metadata, chunk_data)
            records.append(record)
        
        return records
    
    def validate_record(self, record: Dict[str, Any]) -> List[str]:
        """Validate a record against the schema"""
        if not self.schema:
            return []
        
        try:
            jsonschema.validate(record, self.schema)
            return []
        except jsonschema.ValidationError as e:
            return [str(e)]
    
    def generate_from_files(self, input_files: List[Path],
                          output_path: Path,
                          format_type: str = "auto",
                          chunk_type: str = "fixed",
                          chunk_size: int = 1000,
                          chunk_overlap: int = 100,
                          csv_text_column: str = "content",
                          metadata_override: Dict[str, Any] = None) -> Dict[str, Any]:
        """Generate JSONL from input files"""
        
        all_records = []
        validation_errors = []
        
        for file_path in input_files:
            print(f"Processing: {file_path}")
            
            # Determine format
            if format_type == "auto":
                if file_path.suffix.lower() == '.csv':
                    file_format = "csv"
                elif file_path.suffix.lower() in ['.md', '.markdown']:
                    file_format = "markdown"
                else:
                    file_format = "text"
            else:
                file_format = format_type
            
            # Parse the file
            try:
                if file_format == "csv":
                    documents = self.parser.parse_csv(file_path, csv_text_column)
                elif file_format == "markdown":
                    documents = self.parser.parse_markdown(file_path)
                elif file_format == "text":
                    documents = self.parser.parse_plain_text(file_path, metadata_override)
                else:
                    raise ValueError(f"Unknown format: {file_format}")
                
                # Process each document
                for doc_data in documents:
                    # Override metadata if provided
                    if metadata_override:
                        doc_data['metadata'].document_metadata.update(metadata_override)
                    
                    # Generate chunks
                    records = self.process_document(
                        doc_data, chunk_type, chunk_size, chunk_overlap
                    )
                    
                    # Validate records
                    for record in records:
                        errors = self.validate_record(record)
                        if errors:
                            validation_errors.extend(errors)
                        else:
                            all_records.append(record)
            
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue
        
        # Write JSONL output
        with open(output_path, 'w', encoding='utf-8') as f:
            for record in all_records:
                f.write(json.dumps(record, ensure_ascii=False) + '\n')
        
        # Return summary
        return {
            "total_records": len(all_records),
            "validation_errors": validation_errors,
            "output_file": str(output_path)
        }

def main():
    """CLI interface for the JSONL generator"""
    parser = argparse.ArgumentParser(
        description="Generate JSONL corpus files from various source formats",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert markdown files to JSONL
  python jsonl_generator.py --input *.md --output corpus.jsonl --chunk-type sectional

  # Convert CSV to JSONL with specific text column
  python jsonl_generator.py --input data.csv --output corpus.jsonl --format csv --csv-text-column article_text

  # Convert plain text with metadata override
  python jsonl_generator.py --input transcript.txt --output corpus.jsonl --format text --metadata '{"author": "John Doe", "document_type": "speech"}'

  # Fixed chunking with custom size
  python jsonl_generator.py --input document.txt --output corpus.jsonl --chunk-type fixed --chunk-size 1500 --chunk-overlap 150
        """
    )
    
    parser.add_argument('--input', '-i', required=True, nargs='+', type=Path,
                       help='Input files (supports wildcards)')
    parser.add_argument('--output', '-o', type=Path,
                       help='Output JSONL file (required unless --validate-only)')
    parser.add_argument('--format', choices=['auto', 'csv', 'markdown', 'text'], 
                       default='auto', help='Input format (auto-detected by default)')
    parser.add_argument('--schema', type=Path,
                       help='JSON schema file for validation')
    parser.add_argument('--chunk-type', choices=['fixed', 'sectional', 'semantic'],
                       default='fixed', help='Chunking strategy')
    parser.add_argument('--chunk-size', type=int, default=1000,
                       help='Chunk size in characters (for fixed/semantic chunking)')
    parser.add_argument('--chunk-overlap', type=int, default=100,
                       help='Chunk overlap in characters (for fixed chunking)')
    parser.add_argument('--csv-text-column', default='content',
                       help='CSV column containing text content')
    parser.add_argument('--metadata', type=str,
                       help='JSON string with metadata overrides')
    parser.add_argument('--validate-only', action='store_true',
                       help='Only validate against schema, do not generate')
    
    args = parser.parse_args()
    
    # Check required arguments
    if not args.validate_only and not args.output:
        parser.error("--output is required unless --validate-only is specified")
    
    # Expand wildcards in input files
    input_files = []
    for pattern in args.input:
        if '*' in str(pattern) or '?' in str(pattern):
            input_files.extend(Path().glob(str(pattern)))
        else:
            input_files.append(pattern)
    
    # Check that input files exist
    for file_path in input_files:
        if not file_path.exists():
            print(f"Error: Input file {file_path} does not exist")
            sys.exit(1)
    
    # Parse metadata override
    metadata_override = None
    if args.metadata:
        try:
            metadata_override = json.loads(args.metadata)
        except json.JSONDecodeError as e:
            print(f"Error: Invalid metadata JSON: {e}")
            sys.exit(1)
    
    # Create generator
    generator = JSONLGenerator(args.schema if args.schema else None)
    
    try:
        if args.validate_only:
            # Validation mode
            if not args.schema:
                print("Error: Schema required for validation")
                sys.exit(1)
            
            all_errors = []
            for file_path in input_files:
                with open(file_path, 'r') as f:
                    for line_num, line in enumerate(f, 1):
                        if line.strip():
                            try:
                                record = json.loads(line)
                                errors = generator.validate_record(record)
                                if errors:
                                    all_errors.extend([f"Line {line_num}: {e}" for e in errors])
                            except json.JSONDecodeError as e:
                                all_errors.append(f"Line {line_num}: Invalid JSON: {e}")
            
            if not all_errors:
                print(f"✅ All records are valid against the schema")
            else:
                print(f"❌ Found {len(all_errors)} validation errors:")
                for error in all_errors:
                    print(f"  {error}")
        
        else:
            # Generation mode
            result = generator.generate_from_files(
                input_files=input_files,
                output_path=args.output,
                format_type=args.format,
                chunk_type=args.chunk_type,
                chunk_size=args.chunk_size,
                chunk_overlap=args.chunk_overlap,
                csv_text_column=args.csv_text_column,
                metadata_override=metadata_override
            )
            
            print(f"✅ Generated {result['total_records']} records")
            print(f"📄 Output: {result['output_file']}")
            
            if result['validation_errors']:
                print(f"⚠️  {len(result['validation_errors'])} validation errors:")
                for error in result['validation_errors'][:5]:  # Show first 5 errors
                    print(f"  {error}")
                if len(result['validation_errors']) > 5:
                    print(f"  ... and {len(result['validation_errors']) - 5} more")
    
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 