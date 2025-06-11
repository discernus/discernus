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
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = OpenAI(api_key=api_key or os.getenv('OPENAI_API_KEY'))
        
    def extract_metadata(self, text_content: str, filename: str) -> ExtractedMetadata:
        """Extract metadata from text content using LLM"""
        
        # Prepare the prompt
        prompt = self._build_extraction_prompt(text_content, filename)
        
        try:
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert librarian who extracts metadata from text documents."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.1,
                max_tokens=500
            )
            
            # Parse the JSON response
            response_text = response.choices[0].message.content.strip()
            metadata_dict = json.loads(response_text)
            
            # Create ExtractedMetadata object
            metadata = ExtractedMetadata(**metadata_dict)
            
            # Calculate confidence score
            metadata.confidence_score = self._calculate_confidence(metadata, text_content)
            
            return metadata
            
        except Exception as e:
            # Return minimal metadata with low confidence
            return ExtractedMetadata(
                title=self._extract_title_fallback(text_content, filename),
                confidence_score=0.1,
                extraction_notes=[f"LLM extraction failed: {str(e)}"]
            )
    
    def _build_extraction_prompt(self, text_content: str, filename: str) -> str:
        """Build the prompt for metadata extraction"""
        
        # Truncate content if too long (keep first 2000 chars)
        content_preview = text_content[:2000]
        if len(text_content) > 2000:
            content_preview += "... [TRUNCATED]"
            
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
                return line[:100]  # Truncate to reasonable length
        
        # Fallback to filename
        return Path(filename).stem.replace('_', ' ').title()


class IntelligentIngestionService:
    """Main service for intelligent corpus ingestion"""
    
    def __init__(self, corpus_registry: CorpusRegistry, confidence_threshold: float = 70.0):
        self.registry = corpus_registry
        self.extractor = MetadataExtractor()
        self.confidence_threshold = confidence_threshold
        
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
            
        print(f"\n📊 Ingestion Results:")
        print(f"  ✅ Successful: {results['summary']['successful']}")
        print(f"  ⚠️  Uncertain: {results['summary']['uncertain']}")
        print(f"  ❌ Failed: {results['summary']['failed']}")
        print(f"  📈 Success Rate: {results['summary']['success_rate']:.1f}%")
        print(f"  💾 Results saved to: {results_file}")
        
        return results
    
    def _process_file(self, file_path: Path, output_dir: Path) -> Dict[str, Any]:
        """Process a single file"""
        
        # Read file content
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        # Extract metadata
        metadata = self.extractor.extract_metadata(content, file_path.name)
        
        result = {
            "filename": file_path.name,
            "file_path": str(file_path),
            "confidence": metadata.confidence_score,
            "metadata": asdict(metadata),
            "content_length": len(content),
            "content_hash": hashlib.sha256(content.encode()).hexdigest()[:16]
        }
        
        # If confidence is high enough, register in corpus
        if metadata.confidence_score >= self.confidence_threshold:
            try:
                text_id = self._generate_text_id(metadata)
                registration_result = self.registry.register_document(
                    text_id=text_id,
                    file_path=str(file_path),
                    metadata={
                        "title": metadata.title,
                        "author": metadata.author,
                        "date": metadata.date,
                        "document_type": metadata.document_type,
                        "description": metadata.description,
                        "language": metadata.language,
                        "source": "intelligent_ingestion",
                        "confidence_score": metadata.confidence_score
                    }
                )
                result["registration"] = registration_result
                result["text_id"] = text_id
            except Exception as e:
                result["registration_error"] = str(e)
        
        # Save individual result file
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