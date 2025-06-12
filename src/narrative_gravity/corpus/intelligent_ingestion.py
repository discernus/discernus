#!/usr/bin/env python3
"""
Intelligent Corpus Ingestion Service

Automatically extracts metadata from messy text files with confidence scoring.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import hashlib
import shutil

import openai
from openai import OpenAI

from .registry import CorpusRegistry


@dataclass
class ExtractedMetadata:
    """Container for extracted metadata with confidence scoring"""
    title: Optional[str] = None
    author: Optional[str] = None
    date: Optional[str] = None
    document_type: Optional[str] = None
    description: Optional[str] = None
    language: Optional[str] = "en"
    confidence_score: float = 0.0
    extraction_notes: List[str] = None
    
    def __post_init__(self):
        if self.extraction_notes is None:
            self.extraction_notes = []


class MetadataExtractor:
    """LLM-powered metadata extraction with confidence scoring"""
    
    def __init__(self, api_key: Optional[str] = None, content_limit: int = 4000):
        self.client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        self.content_limit = content_limit  # Configurable content limit
        
    def extract_metadata(self, text_content: str, filename: str) -> ExtractedMetadata:
        """Extract metadata from text content using LLM with retry logic"""
        
        # Prepare the prompt
        prompt = self._build_extraction_prompt(text_content, filename)
        
        # Retry logic for intermittent API failures
        max_retries = 3
        retry_delay = [1, 2, 4]  # Exponential backoff
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    import time
                    time.sleep(retry_delay[min(attempt-1, len(retry_delay)-1)])
                    print(f"  🔄 Retry attempt {attempt + 1}/{max_retries}")
                
                response = self.client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are an expert librarian who extracts metadata from text documents."},
                        {"role": "user", "content": prompt}
                    ],
                    temperature=0.1,
                    max_tokens=500
                )
                
                # Check for valid response
                response_text = response.choices[0].message.content
                if not response_text or not response_text.strip():
                    raise ValueError("Empty response from API")
                
                # Parse the JSON response
                response_text = response_text.strip()
                
                # Remove markdown code block markers if present
                if response_text.startswith('```json'):
                    response_text = response_text[7:]  # Remove ```json
                if response_text.startswith('```'):
                    response_text = response_text[3:]   # Remove ```
                if response_text.endswith('```'):
                    response_text = response_text[:-3]  # Remove ending ```
                
                response_text = response_text.strip()
                metadata_dict = json.loads(response_text)
                
                # Create ExtractedMetadata object
                metadata = ExtractedMetadata(**metadata_dict)
                
                # Calculate confidence score
                metadata.confidence_score = self._calculate_confidence(metadata, text_content)
                
                if attempt > 0:
                    metadata.extraction_notes.append(f"Succeeded on retry attempt {attempt + 1}")
                
                return metadata
                
            except Exception as e:
                last_error = str(e)
                if attempt == max_retries - 1:
                    # Final attempt failed, return fallback
                    break
                else:
                    print(f"  ⚠️  Attempt {attempt + 1} failed: {last_error}")
                    continue
        
        # All retries failed, return minimal metadata with low confidence
        return ExtractedMetadata(
            title=self._extract_title_fallback(text_content, filename),
            confidence_score=0.1,
            extraction_notes=[f"LLM extraction failed after {max_retries} attempts: {last_error}"]
        )
    
    def _build_extraction_prompt(self, text_content: str, filename: str) -> str:
        """Build the prompt for metadata extraction with smart truncation"""
        
        # Smart truncation: keep beginning and end for better metadata extraction
        if len(text_content) <= self.content_limit:
            content_preview = text_content
        else:
            # Keep first 60% and last 40% of the limit
            first_part_len = int(self.content_limit * 0.6)
            last_part_len = int(self.content_limit * 0.4)
            
            first_part = text_content[:first_part_len]
            last_part = text_content[-last_part_len:]
            
            content_preview = (
                first_part + 
                f"\n\n... [TRUNCATED {len(text_content) - self.content_limit:,} characters] ...\n\n" + 
                last_part
            )
            
        return f"""
Extract metadata from this document and return ONLY valid JSON with these exact fields:

{{
    "title": "the main title of the document",
    "author": "the author or speaker name", 
    "date": "date in YYYY-MM-DD format if found, null otherwise",
    "document_type": "speech|address|inaugural|message|letter|article|other",
    "description": "brief 1-2 sentence description of the document",
    "language": "language code (en, es, fr, etc)",
    "extraction_notes": ["any notes about confidence or issues"]
}}

Filename: {filename}

Document content:
{content_preview}

Return ONLY the JSON object, no other text:
"""

    def _calculate_confidence(self, metadata: ExtractedMetadata, text_content: str) -> float:
        """Calculate confidence score based on completeness and validation"""
        
        score = 0.0
        
        # Base scoring for field completeness
        if metadata.title and len(metadata.title.strip()) > 5:
            score += 25
        if metadata.author and len(metadata.author.strip()) > 2:
            score += 20
        if metadata.date and self._is_valid_date(metadata.date):
            score += 20
        if metadata.document_type and metadata.document_type != "other":
            score += 15
        if metadata.description and len(metadata.description.strip()) > 10:
            score += 10
        if metadata.language:
            score += 5
            
        # Bonus for consistency checks
        if metadata.title and metadata.title.lower() in text_content.lower()[:500]:
            score += 5
            
        return min(score, 100.0)
    
    def _is_valid_date(self, date_str: str) -> bool:
        """Check if date string is valid"""
        if not date_str:
            return False
        try:
            datetime.strptime(date_str, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    def _extract_title_fallback(self, text_content: str, filename: str) -> str:
        """Fallback title extraction if LLM fails"""
        # Try to get first meaningful line
        lines = text_content.split('\n')
        for line in lines[:5]:
            line = line.strip()
            if len(line) > 10 and not line.startswith('#'):
                # Smart truncation: prefer at word boundaries
                if len(line) <= 200:
                    return line
                else:
                    # Find last space before 200 chars
                    truncated = line[:200]
                    last_space = truncated.rfind(' ')
                    if last_space > 100:  # Ensure we don't truncate too early
                        return truncated[:last_space] + "..."
                    else:
                        return truncated + "..."
        
        # Fallback to filename
        return Path(filename).stem.replace('_', ' ').title()


class IntelligentIngestionService:
    """Main service for intelligent corpus ingestion"""
    
    def __init__(self, corpus_registry: CorpusRegistry, confidence_threshold: float = 70.0, content_limit: int = 4000):
        self.registry = corpus_registry
        self.extractor = MetadataExtractor(content_limit=content_limit)
        self.confidence_threshold = confidence_threshold
        self.processed_storage = Path("corpus/processed")
        self.processed_storage.mkdir(parents=True, exist_ok=True)
        
    def ingest_directory(self, directory_path: str, output_dir: str = None) -> Dict[str, Any]:
        """Ingest all text files from a directory"""
        
        directory = Path(directory_path)
        if not directory.exists():
            raise ValueError(f"Directory not found: {directory_path}")
            
        # Set up output directory
        if output_dir is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_dir = f"tmp/intelligent_ingestion_{timestamp}"
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        results = {
            "processed": [],
            "successful": [],
            "uncertain": [],
            "failed": [],
            "summary": {}
        }
        
        # Find all text files
        text_files = list(directory.glob("*.txt")) + list(directory.glob("*.md"))
        
        print(f"🔍 Found {len(text_files)} text files to process...")
        
        for file_path in text_files:
            try:
                print(f"📄 Processing: {file_path.name}")
                result = self._process_file(file_path, output_path)
                results["processed"].append(result)
                
                # Categorize by confidence
                if result["confidence"] >= self.confidence_threshold:
                    results["successful"].append(result)
                    print(f"  ✅ Success ({result['confidence']:.1f}%): {result['metadata']['title']}")
                elif result["confidence"] >= 40.0:
                    results["uncertain"].append(result)
                    print(f"  ⚠️  Uncertain ({result['confidence']:.1f}%): {result['metadata']['title']}")
                else:
                    results["failed"].append(result)
                    print(f"  ❌ Failed ({result['confidence']:.1f}%): {result['filename']}")
                    
            except Exception as e:
                error_result = {
                    "filename": file_path.name,
                    "error": str(e),
                    "confidence": 0.0
                }
                results["failed"].append(error_result)
                print(f"  💥 Error: {str(e)}")
        
        # Generate summary
        results["summary"] = {
            "total_files": len(text_files),
            "successful": len(results["successful"]),
            "uncertain": len(results["uncertain"]),
            "failed": len(results["failed"]),
            "success_rate": len(results["successful"]) / len(text_files) * 100 if text_files else 0
        }
        
        # Save detailed results
        results_file = output_path / "ingestion_results.json"
        with open(results_file, 'w') as f:
            json.dump(results, f, indent=2)
        
        # Create a summary file with non-truncated key information
        summary_file = output_path / "ingestion_summary.txt"
        with open(summary_file, 'w') as f:
            f.write("Intelligent Ingestion Summary\n")
            f.write("=" * 50 + "\n\n")
            
            f.write(f"Total files processed: {results['summary']['total_files']}\n")
            f.write(f"Successful: {results['summary']['successful']}\n")
            f.write(f"Uncertain: {results['summary']['uncertain']}\n")
            f.write(f"Failed: {results['summary']['failed']}\n")
            f.write(f"Success rate: {results['summary']['success_rate']:.1f}%\n\n")
            
            for item in results['processed']:
                f.write(f"File: {item['filename']}\n")
                f.write(f"  Status: {item.get('status', 'unknown')}\n")
                f.write(f"  Confidence: {item['confidence']:.1f}%\n")
                if 'text_id' in item:
                    f.write(f"  Text ID: {item['text_id']}\n")
                if 'metadata' in item and isinstance(item['metadata'], dict):
                    if 'title' in item['metadata']:
                        f.write(f"  Title: {item['metadata']['title']}\n")
                    if 'author' in item['metadata']:
                        f.write(f"  Author: {item['metadata']['author']}\n")
                f.write("\n")
            
        print(f"\n📊 Ingestion Results:")
        print(f"  ✅ Successful: {results['summary']['successful']}")
        print(f"  ⚠️  Uncertain: {results['summary']['uncertain']}")
        print(f"  ❌ Failed: {results['summary']['failed']}")
        print(f"  📈 Success Rate: {results['summary']['success_rate']:.1f}%")
        print(f"  💾 Full results: {results_file}")
        print(f"  📄 Summary: {summary_file}")
        
        return results
    
    def _update_processed_manifest(self, text_id: str, file_path: Path, content_hash: str, metadata: ExtractedMetadata) -> None:
        """Update the global manifest of processed files."""
        manifest_file = self.processed_storage / ".manifest.json"
        
        # Load existing manifest
        if manifest_file.exists():
            with open(manifest_file, 'r') as f:
                manifest = json.load(f)
        else:
            manifest = {
                "version": "1.0.0",
                "created_at": datetime.now().isoformat(),
                "processed_files": {}
            }
        
        # Add/update entry
        manifest["processed_files"][text_id] = {
            "content_hash": content_hash,
            "file_path": str(file_path),
            "confidence_score": metadata.confidence_score,
            "processed_at": datetime.now().isoformat(),
            "title": metadata.title,
            "author": metadata.author,
            "date": metadata.date,
            "document_type": metadata.document_type
        }
        
        manifest["last_updated"] = datetime.now().isoformat()
        manifest["total_processed"] = len(manifest["processed_files"])
        
        # Save manifest
        with open(manifest_file, 'w') as f:
            json.dump(manifest, f, indent=2)
    
    def check_already_processed(self, content_hash: str) -> Optional[str]:
        """Check if content has already been processed by hash."""
        manifest_file = self.processed_storage / ".manifest.json"
        
        if not manifest_file.exists():
            return None
        
        with open(manifest_file, 'r') as f:
            manifest = json.load(f)
        
        # Look for existing content hash
        for text_id, info in manifest.get("processed_files", {}).items():
            if info.get("content_hash") == content_hash:
                return text_id
        
        return None
    
    def _process_file(self, file_path: Path, output_dir: Path) -> Dict[str, Any]:
        """Process a single file with organized storage for successful results."""
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Calculate content hash
        content_hash = hashlib.sha256(content.encode()).hexdigest()
        
        # Check if already processed
        existing_text_id = self.check_already_processed(content_hash)
        if existing_text_id:
            return {
                "filename": file_path.name,
                "file_path": str(file_path),
                "confidence": 100.0,
                "metadata": {"title": f"Already processed as {existing_text_id}"},
                "content_length": len(content),
                "content_hash": content_hash,
                "status": "duplicate",
                "existing_text_id": existing_text_id,
                "message": f"Content already processed as {existing_text_id}"
            }
        
        # Extract metadata
        metadata = self.extractor.extract_metadata(content, file_path.name)
        
        result = {
            "filename": file_path.name,
            "file_path": str(file_path),
            "confidence": metadata.confidence_score,
            "metadata": asdict(metadata),
            "content_length": len(content),
            "content_hash": content_hash
        }
        
        # If confidence is high enough, organize and register
        if metadata.confidence_score >= self.confidence_threshold:
            try:
                text_id = self._generate_text_id(metadata)
                
                # Move to organized storage
                stable_path = self._organize_processed_file(file_path, text_id, content_hash, metadata)
                
                # Register with stable path
                if self.registry:
                    # Parse date if it's a string
                    doc_date = metadata.date
                    if isinstance(doc_date, str):
                        from datetime import datetime
                        doc_date = datetime.strptime(doc_date, "%Y-%m-%d")
                    elif doc_date is None:
                        from datetime import datetime
                        doc_date = datetime.now()
                    
                    registration_result = self.registry.register_document(
                        file_path=str(stable_path),  # Use stable path, not original
                        title=metadata.title,
                        author=metadata.author,
                        date=doc_date,
                        document_type=metadata.document_type,
                        # Additional metadata as kwargs
                        text_id=text_id,
                        description=metadata.description,
                        language=metadata.language,
                        source="intelligent_ingestion",
                        confidence_score=metadata.confidence_score,
                        original_path=str(file_path),  # Track original location
                        content_hash=content_hash
                    )
                    # Convert registration result to JSON-serializable format
                    if registration_result:
                        reg_dict = asdict(registration_result)
                        # Convert any datetime objects to ISO strings and Path objects to strings
                        for key, value in reg_dict.items():
                            if isinstance(value, datetime):
                                reg_dict[key] = value.isoformat()
                            elif isinstance(value, Path):
                                reg_dict[key] = str(value)
                        result["registration"] = reg_dict
                    else:
                        result["registration"] = None
                    result["text_id"] = text_id
                    result["stable_path"] = str(stable_path)
                    result["status"] = "processed_and_organized"
                
            except Exception as e:
                result["registration_error"] = str(e)
                result["status"] = "extraction_success_registration_failed"
        else:
            result["status"] = "low_confidence"
        
        # Save individual result file (in temp output dir)
        result_file = output_dir / f"{file_path.stem}_result.json"
        with open(result_file, 'w') as f:
            json.dump(result, f, indent=2)
            
        return result
    
    def _generate_text_id(self, metadata: ExtractedMetadata) -> str:
        """Generate semantic text ID from metadata"""
        
        # Extract components for ID
        author_part = ""
        if metadata.author:
            # Take last name if possible
            name_parts = metadata.author.split()
            if name_parts:
                author_part = name_parts[-1].lower()
                author_part = re.sub(r'[^a-z]', '', author_part)
        
        type_part = metadata.document_type or "text"
        
        year_part = ""
        if metadata.date:
            try:
                year_part = metadata.date.split('-')[0]
            except:
                pass
        
        # Combine parts
        if author_part and year_part:
            return f"{author_part}_{type_part}_{year_part}"
        elif author_part:
            return f"{author_part}_{type_part}"
        else:
            return f"unknown_{type_part}_{datetime.now().strftime('%Y%m%d')}"

    def _organize_processed_file(self, file_path: Path, text_id: str, content_hash: str, metadata: ExtractedMetadata) -> Path:
        """
        Move successfully processed file to content-addressable storage.
        
        Args:
            file_path: Original file path
            text_id: Generated text ID (e.g., lincoln_inaugural_1865)  
            content_hash: SHA-256 hash of content
            metadata: Extracted metadata
            
        Returns:
            Path to new stable location
        """
        # Create hash-based directory structure: ab/cd/abcd1234.../
        hash_prefix = content_hash[:2]
        hash_middle = content_hash[2:4]
        hash_full = content_hash
        
        target_dir = self.processed_storage / hash_prefix / hash_middle / hash_full
        target_dir.mkdir(parents=True, exist_ok=True)
        
        # Use text_id for human-readable filename
        target_file = target_dir / f"{text_id}.txt"
        
        # Copy file to processed location (preserve original)
        shutil.copy2(file_path, target_file)
        
        # Create metadata sidecar file
        metadata_file = target_dir / ".metadata.json"
        with open(metadata_file, 'w') as f:
            json.dump({
                "text_id": text_id,
                "content_hash": content_hash,
                "extraction_confidence": metadata.confidence_score,
                "extracted_metadata": asdict(metadata),
                "processed_at": datetime.now().isoformat(),
                "original_path": str(file_path),
                "stable_path": str(target_file)
            }, f, indent=2)
        
        # Create provenance file
        provenance_file = target_dir / ".provenance.json"
        with open(provenance_file, 'w') as f:
            json.dump({
                "source_file": {
                    "original_path": str(file_path),
                    "filename": file_path.name,
                    "size_bytes": file_path.stat().st_size,
                    "modified_at": datetime.fromtimestamp(file_path.stat().st_mtime).isoformat()
                },
                "processing": {
                    "processed_at": datetime.now().isoformat(),
                    "confidence_score": metadata.confidence_score,
                    "extraction_method": "intelligent_ingestion",
                    "content_hash": content_hash
                },
                "stable_location": {
                    "directory": str(target_dir),
                    "text_file": str(target_file),
                    "metadata_file": str(metadata_file)
                }
            }, f, indent=2)
        
        # Update global manifest
        self._update_processed_manifest(text_id, target_file, content_hash, metadata)
        
        return target_file 