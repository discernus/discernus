#!/usr/bin/env python3
"""
Demo version of Intelligent Corpus Ingestion Service

Uses rule-based extraction instead of LLM for demonstration.
Shows the complete workflow without requiring OpenAI API keys.
"""

import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
import hashlib
import sys

# Add src to Python path
PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from narrative_gravity.corpus.registry import CorpusRegistry


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


class DemoMetadataExtractor:
    """Rule-based metadata extraction for demonstration"""
    
    def extract_metadata(self, text_content: str, filename: str) -> ExtractedMetadata:
        """Extract metadata using rule-based approach"""
        
        metadata = ExtractedMetadata()
        
        # Extract title (first substantial line)
        metadata.title = self._extract_title(text_content, filename)
        
        # Extract author from filename or content
        metadata.author = self._extract_author(text_content, filename)
        
        # Extract date from filename or content
        metadata.date = self._extract_date(text_content, filename)
        
        # Extract document type from filename
        metadata.document_type = self._extract_document_type(filename)
        
        # Generate description
        metadata.description = self._generate_description(text_content, metadata)
        
        # Calculate confidence
        metadata.confidence_score = self._calculate_confidence(metadata, text_content)
        
        metadata.extraction_notes = ["Demo rule-based extraction"]
        
        return metadata
    
    def _extract_title(self, text_content: str, filename: str) -> str:
        """Extract title from content or filename"""
        lines = text_content.split('\n')
        
        # Look for title in first few lines
        for line in lines[:10]:
            line = line.strip()
            if len(line) > 15 and len(line) < 200:
                # Skip lines that look like metadata
                if not re.match(r'^(date|author|by):', line, re.I):
                    return line
        
        # Fallback to filename-based title
        return Path(filename).stem.replace('_', ' ').title()
    
    def _extract_author(self, text_content: str, filename: str) -> Optional[str]:
        """Extract author from filename or content"""
        filename_lower = filename.lower()
        
        # Known authors from filenames
        authors = {
            'lincoln': 'Abraham Lincoln',
            'washington': 'George Washington',
            'jefferson': 'Thomas Jefferson',
            'roosevelt': 'Franklin D. Roosevelt',
            'reagan': 'Ronald Reagan',
            'kennedy': 'John F. Kennedy',
            'nixon': 'Richard Nixon',
            'jackson': 'Andrew Jackson',
            'adams': 'John Adams',
            'madison': 'James Madison',
            'grant': 'Ulysses S. Grant',
            'hoover': 'Herbert Hoover',
            'johnson': 'Lyndon B. Johnson',
            'eisenhower': 'Dwight D. Eisenhower',
            'mandela': 'Nelson Mandela',
            'chavez': 'Hugo Chávez',
            'lenin': 'Vladimir Lenin',
            'ortega': 'Daniel Ortega'
        }
        
        for key, author in authors.items():
            if key in filename_lower:
                return author
        
        # Look for author in content
        lines = text_content.split('\n')[:20]
        for line in lines:
            if re.search(r'by\s+([A-Z][a-z]+\s+[A-Z][a-z]+)', line, re.I):
                match = re.search(r'by\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)+)', line, re.I)
                if match:
                    return match.group(1)
        
        return None
    
    def _extract_date(self, text_content: str, filename: str) -> Optional[str]:
        """Extract date from filename or content"""
        
        # Extract year from filename
        year_match = re.search(r'(\d{4})', filename)
        if year_match:
            year = year_match.group(1)
            
            # Known inaugural dates
            inaugural_dates = {
                '1789': '1789-04-30',  # Washington
                '1797': '1797-03-04',  # Adams
                '1801': '1801-03-04',  # Jefferson 1st
                '1805': '1805-03-04',  # Jefferson 2nd
                '1809': '1809-03-04',  # Madison 1st
                '1813': '1813-03-04',  # Madison 2nd
                '1829': '1829-03-04',  # Jackson 1st
                '1833': '1833-03-04',  # Jackson 2nd
                '1861': '1861-03-04',  # Lincoln 1st
                '1865': '1865-03-04',  # Lincoln 2nd
                '1869': '1869-03-04',  # Grant 1st
                '1905': '1905-03-04',  # T. Roosevelt
                '1929': '1929-03-04',  # Hoover
                '1933': '1933-03-04',  # F. Roosevelt 1st
                '1941': '1941-01-20',  # F. Roosevelt 3rd
                '1953': '1953-01-20',  # Eisenhower
                '1961': '1961-01-20',  # Kennedy
                '1965': '1965-01-20',  # Johnson
                '1969': '1969-01-20',  # Nixon 1st
                '1973': '1973-01-20',  # Nixon 2nd
                '1981': '1981-01-20',  # Reagan 1st
                '1985': '1985-01-20',  # Reagan 2nd
                '1994': '1994-05-10',  # Mandela
                '2006': '2006-09-20',  # Chávez UN
                '2023': '2023-09-19'   # Ortega UN
            }
            
            if year in inaugural_dates:
                return inaugural_dates[year]
            
            return f"{year}-01-01"  # Generic date if year found
        
        # Look for dates in content
        date_patterns = [
            r'(\d{4}-\d{2}-\d{2})',
            r'(\w+ \d{1,2}, \d{4})',
            r'(\d{1,2} \w+ \d{4})'
        ]
        
        for pattern in date_patterns:
            match = re.search(pattern, text_content[:1000])
            if match:
                date_str = match.group(1)
                try:
                    # Try to normalize date
                    if '-' in date_str:
                        return date_str
                    else:
                        # Convert to YYYY-MM-DD format if possible
                        pass
                except:
                    pass
        
        return None
    
    def _extract_document_type(self, filename: str) -> str:
        """Extract document type from filename"""
        filename_lower = filename.lower()
        
        if 'inaugural' in filename_lower:
            return 'inaugural'
        elif 'speech' in filename_lower:
            return 'speech'
        elif 'address' in filename_lower:
            return 'address'
        elif 'letter' in filename_lower:
            return 'letter'
        elif 'message' in filename_lower:
            return 'message'
        else:
            return 'text'
    
    def _generate_description(self, text_content: str, metadata: ExtractedMetadata) -> str:
        """Generate a description based on extracted metadata"""
        parts = []
        
        if metadata.author:
            parts.append(f"{metadata.author}'s")
        
        if metadata.document_type:
            parts.append(metadata.document_type)
        
        if metadata.date:
            year = metadata.date.split('-')[0]
            parts.append(f"from {year}")
        
        if not parts:
            return "Historical document"
        
        return " ".join(parts).capitalize() + "."
    
    def _calculate_confidence(self, metadata: ExtractedMetadata, text_content: str) -> float:
        """Calculate confidence score"""
        score = 0.0
        
        if metadata.title and len(metadata.title.strip()) > 5:
            score += 25
        if metadata.author:
            score += 30
        if metadata.date:
            score += 25
        if metadata.document_type and metadata.document_type != 'text':
            score += 15
        if metadata.description:
            score += 5
        
        return min(score, 100.0)


def main():
    """Demo the intelligent ingestion service"""
    
    print("🎪 DEMO: Intelligent Corpus Ingestion Service")
    print("📝 Using rule-based extraction (no LLM required)")
    print()
    
    # Initialize services
    try:
        corpus_registry = CorpusRegistry()
        print("✅ CorpusRegistry connected")
    except Exception as e:
        print(f"⚠️  CorpusRegistry unavailable: {e}")
        corpus_registry = None
    
    # Create demo service
    extractor = DemoMetadataExtractor()
    
    # Process the messy data directory
    directory = Path("corpus/raw_sources/other_texts")
    if not directory.exists():
        print(f"❌ Directory not found: {directory}")
        return
    
    # Set up output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"tmp/demo_ingestion_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Processing: {directory}")
    print(f"💾 Output: {output_dir}")
    print()
    
    # Find files
    text_files = list(directory.glob("*.txt"))[:10]  # Limit to first 10 for demo
    
    results = {
        "processed": [],
        "successful": [],
        "uncertain": [],
        "failed": []
    }
    
    confidence_threshold = 70.0
    
    for file_path in text_files:
        print(f"📄 Processing: {file_path.name}")
        
        try:
            # Read file
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            # Extract metadata
            metadata = extractor.extract_metadata(content, file_path.name)
            
            # Create result
            result = {
                "filename": file_path.name,
                "confidence": metadata.confidence_score,
                "metadata": asdict(metadata),
                "content_length": len(content)
            }
            
            # Categorize
            if metadata.confidence_score >= confidence_threshold:
                results["successful"].append(result)
                status = "✅ Success"
                
                # Try to register if registry available
                if corpus_registry:
                    try:
                        text_id = generate_text_id(metadata)
                        registration = corpus_registry.register_document(
                            text_id=text_id,
                            file_path=str(file_path),
                            metadata={
                                "title": metadata.title,
                                "author": metadata.author,
                                "date": metadata.date,
                                "document_type": metadata.document_type,
                                "description": metadata.description,
                                "source": "demo_intelligent_ingestion"
                            }
                        )
                        result["registration"] = "✅ Registered"
                        result["text_id"] = text_id
                    except Exception as e:
                        result["registration"] = f"❌ Failed: {e}"
                
            elif metadata.confidence_score >= 40.0:
                results["uncertain"].append(result)
                status = "⚠️  Uncertain"
            else:
                results["failed"].append(result)
                status = "❌ Failed"
            
            print(f"  {status} ({metadata.confidence_score:.1f}%): {metadata.title}")
            print(f"    Author: {metadata.author or 'Unknown'}")
            print(f"    Date: {metadata.date or 'Unknown'}")
            print(f"    Type: {metadata.document_type or 'Unknown'}")
            print()
            
            results["processed"].append(result)
            
        except Exception as e:
            print(f"  💥 Error: {e}")
            results["failed"].append({"filename": file_path.name, "error": str(e)})
    
    # Summary
    total = len(text_files)
    successful = len(results["successful"])
    
    print(f"📊 Demo Results:")
    print(f"  ✅ Successful: {successful}/{total}")
    print(f"  ⚠️  Uncertain: {len(results['uncertain'])}")
    print(f"  ❌ Failed: {len(results['failed'])}")
    print(f"  📈 Success Rate: {successful/total*100:.1f}%")
    
    # Save results
    results_file = output_dir / "demo_results.json"
    with open(results_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    print(f"  💾 Results saved to: {results_file}")
    print()
    print("🎉 Demo complete! This shows how the intelligent ingestion service")
    print("   can automatically extract metadata from messy text files and")
    print("   integrate with the CorpusRegistry for research workflows.")


def generate_text_id(metadata: ExtractedMetadata) -> str:
    """Generate semantic text ID from metadata"""
    author_part = ""
    if metadata.author:
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
    
    if author_part and year_part:
        return f"{author_part}_{type_part}_{year_part}"
    elif author_part:
        return f"{author_part}_{type_part}"
    else:
        return f"unknown_{type_part}_{datetime.now().strftime('%Y%m%d')}"


if __name__ == "__main__":
    main() 