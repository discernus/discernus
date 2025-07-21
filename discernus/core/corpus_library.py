#!/usr/bin/env python3
"""
Corpus Library - THIN corpus discovery and description
=====================================================

THIN Principle: Let LLM generate corpus descriptions while software provides directory discovery
Software just scans directories and calls LLM for intelligent descriptions - zero intelligence
"""

import os
import json
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from discernus.core.ultra_thin_llm_client import UltraThinLLMClient as ThinLiteLLMClient
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False


class CorpusLibrary:
    """
    THIN corpus discovery - LLM generates descriptions, software provides directory listing
    Software provides zero intelligence about corpus content - just file system operations
    """
    
    def __init__(self):
        if LITELLM_AVAILABLE:
            self.llm_client = ThinLiteLLMClient()
        else:
            self.llm_client = None
    
    def discover_all_corpora(self) -> Dict[str, Dict[str, Any]]:
        """
        Discover all available corpora in the project
        
        THIN Principle: Software scans directories, LLM provides intelligence about content
        """
        corpora = {}
        
        # Scan known corpus directories
        corpus_directories = [
            "data/inaugural_addresses",
            "data/bolsonaro_2018", 
            "projects/vanderveen"
        ]
        
        for corpus_dir in corpus_directories:
            corpus_path = Path(corpus_dir)
            if corpus_path.exists():
                corpus_info = self._analyze_corpus_directory(corpus_path)
                if corpus_info:
                    corpora[corpus_dir] = corpus_info
        
        return corpora
    
    def _analyze_corpus_directory(self, corpus_path: Path) -> Optional[Dict[str, Any]]:
        """
        Analyze a corpus directory to generate description
        
        THIN Principle: Software provides file listing, LLM provides intelligence
        THIN Caching: Simple file-based cache with directory timestamp invalidation
        """
        # Check for cached description first
        cached_description = self._load_cached_corpus_description(corpus_path)
        if cached_description:
            return cached_description
        
        # Get basic file system information
        file_info = self._scan_directory_files(corpus_path)
        
        if not file_info['files']:
            return None
        
        # Let LLM generate intelligent description
        description = self._generate_corpus_description(corpus_path, file_info)
        
        result = {
            'path': str(corpus_path),
            'friendly_name': description.get('friendly_name', corpus_path.name),
            'description': description.get('description', 'Academic corpus for research'),
            'file_count': file_info['file_count'],
            'total_size': file_info['total_size'],
            'file_types': file_info['file_types'],
            'sample_files': file_info['sample_files'][:5],  # First 5 files as preview
            'language': description.get('language', 'Unknown'),
            'time_period': description.get('time_period', 'Unknown'),
            'research_themes': description.get('research_themes', []),
        }
        
        # Cache the result
        self._save_cached_corpus_description(corpus_path, result)
        
        return result
    
    def _scan_directory_files(self, corpus_path: Path) -> Dict[str, Any]:
        """
        Scan directory for basic file information
        
        THIN Principle: Pure file system operations, no intelligence
        """
        files = []
        file_types = set()
        total_size = 0
        
        try:
            for item in corpus_path.rglob('*'):
                if item.is_file() and not item.name.startswith('.'):
                    file_size = item.stat().st_size
                    files.append({
                        'name': item.name,
                        'relative_path': str(item.relative_to(corpus_path)),
                        'size': file_size
                    })
                    file_types.add(item.suffix.lower())
                    total_size += file_size
        
        except Exception as e:
            print(f"Error scanning {corpus_path}: {e}")
            return {'files': [], 'file_count': 0, 'total_size': 0, 'file_types': [], 'sample_files': []}
        
        return {
            'files': files,
            'file_count': len(files),
            'total_size': total_size,
            'file_types': list(file_types),
            'sample_files': [f['name'] for f in files[:10]]  # First 10 filenames
        }
    
    def _generate_corpus_description(self, corpus_path: Path, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate LLM description of corpus
        
        THIN Principle: All intelligence in LLM layer, software just calls and parses
        """
        sample_files = file_info['sample_files'][:10]  # Limit context
        corpus_name = corpus_path.name
        
        llm_prompt = f"""You are a corpus librarian. Analyze this corpus directory and provide a structured description.

CORPUS DIRECTORY: {corpus_path}
FILE COUNT: {file_info['file_count']} files
TOTAL SIZE: {file_info['total_size']:,} bytes
FILE TYPES: {', '.join(file_info['file_types'])}

SAMPLE FILES:
{chr(10).join(f'- {filename}' for filename in sample_files)}

Based on the directory name and file names, generate a JSON response with:
1. "friendly_name": A clear, academic name for this corpus (2-5 words)
2. "description": A 1-2 sentence description suitable for researchers
3. "language": Primary language of the texts (English, Portuguese, etc.)
4. "time_period": Time period covered (e.g., "2018 Brazilian Election", "19th Century America")
5. "research_themes": Array of 2-4 research themes this corpus supports

Format as valid JSON. Be academic and precise.

Example format:
{{
  "friendly_name": "Bolsonaro Campaign Speeches",
  "description": "Collection of transcribed campaign speeches from the 2018 Brazilian presidential election, suitable for populist rhetoric analysis.",
  "language": "Portuguese",
  "time_period": "2018 Brazilian Election",
  "research_themes": ["populist rhetoric", "political discourse", "campaign analysis", "Brazilian politics"]
}}"""

        if self.llm_client:
            response = self.llm_client.call_llm(llm_prompt, "corpus_librarian")
            return self._parse_corpus_description(response)
        else:
            return self._generate_mock_description(corpus_path, file_info)
    
    def _parse_corpus_description(self, response: str) -> Dict[str, Any]:
        """
        Parse LLM response as JSON
        
        THIN Principle: Minimal parsing with graceful fallback
        """
        try:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {"friendly_name": "Research Corpus", "description": "Academic corpus for analysis"}
        except Exception:
            return {"friendly_name": "Research Corpus", "description": "Academic corpus for analysis"}
    
    def _load_cached_corpus_description(self, corpus_path: Path) -> Optional[Dict[str, Any]]:
        """
        Load cached corpus description if it exists and is fresh
        
        THIN Principle: Simple directory timestamp comparison, no intelligence
        """
        cache_file = corpus_path / ".corpus_manifest.json"
        
        # Check if cache exists
        if not cache_file.exists():
            return None
        
        # Check if cache is fresh (newer than any file in directory)
        try:
            cache_time = cache_file.stat().st_mtime
            directory_max_time = self._get_directory_max_mtime(corpus_path)
            
            if cache_time < directory_max_time:
                # Cache is stale
                return None
        except Exception:
            # Error checking timestamps, assume stale
            return None
        
        # Load cached description
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except Exception:
            # Corrupted cache, ignore
            return None
    
    def _save_cached_corpus_description(self, corpus_path: Path, description: Dict[str, Any]) -> None:
        """
        Save corpus description to cache file
        
        THIN Principle: Simple file write, no intelligence
        """
        cache_file = corpus_path / ".corpus_manifest.json"
        
        try:
            with open(cache_file, 'w') as f:
                json.dump(description, f, indent=2)
        except Exception:
            # Cache write failed, continue without caching
            pass
    
    def _get_directory_max_mtime(self, corpus_path: Path) -> float:
        """
        Get the maximum modification time of files in directory
        
        THIN Principle: Pure file system operation, no intelligence
        """
        max_time = 0.0
        try:
            for item in corpus_path.rglob('*'):
                if item.is_file() and not item.name.startswith('.'):
                    max_time = max(max_time, item.stat().st_mtime)
        except Exception:
            # Error scanning directory, return current time
            import time
            return time.time()
        
        return max_time

    def _generate_mock_description(self, corpus_path: Path, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock description for testing"""
        corpus_name = corpus_path.name.lower()
        
        if 'bolsonaro' in corpus_name:
            return {
                "friendly_name": "Bolsonaro Campaign Speeches",
                "description": "Brazilian political campaign speeches from 2018 presidential election.",
                "language": "Portuguese",
                "time_period": "2018 Brazilian Election",
                "research_themes": ["populist rhetoric", "campaign analysis", "Brazilian politics"]
            }
        elif 'inaugural' in corpus_name:
            return {
                "friendly_name": "Presidential Inaugural Addresses",
                "description": "American presidential inaugural addresses for comparative analysis.",
                "language": "English", 
                "time_period": "19th-21st Century America",
                "research_themes": ["presidential rhetoric", "American politics", "comparative analysis"]
            }
        elif 'vanderveen' in corpus_name:
            return {
                "friendly_name": "Van der Veen Political Corpus",
                "description": "Multi-candidate political speech corpus for computational discourse analysis.",
                "language": "English",
                "time_period": "2016 US Election",
                "research_themes": ["political discourse", "candidate comparison", "election analysis"]
            }
        else:
            return {
                "friendly_name": f"{corpus_path.name.title()} Corpus",
                "description": f"Academic research corpus with {file_info['file_count']} files.",
                "language": "Unknown",
                "time_period": "Unknown",
                "research_themes": ["text analysis"]
            }


def discover_corpora() -> Dict[str, Dict[str, Any]]:
    """
    Convenience function to discover all available corpora
    
    THIN interface: Just call and return, no complex logic
    """
    library = CorpusLibrary()
    return library.discover_all_corpora()


def get_corpus_info(corpus_path: str) -> Optional[Dict[str, Any]]:
    """
    Get detailed information about a specific corpus
    
    THIN interface: Simple path lookup with LLM description
    """
    library = CorpusLibrary()
    path = Path(corpus_path)
    
    if not path.exists():
        return None
    
    return library._analyze_corpus_directory(path)


if __name__ == "__main__":
    # Test corpus discovery
    print("📚 Discovering Available Corpora...")
    
    corpora = discover_corpora()
    
    print(f"✅ Found {len(corpora)} corpora:")
    for corpus_path, info in corpora.items():
        print(f"\n📂 {info['friendly_name']}")
        print(f"   📍 Path: {corpus_path}")
        print(f"   📝 Description: {info['description']}")
        print(f"   📊 {info['file_count']} files ({info['total_size']:,} bytes)")
        print(f"   🌐 Language: {info['language']}")
        print(f"   📅 Period: {info['time_period']}")
        print(f"   🔬 Themes: {', '.join(info['research_themes'])}")
        
        if info['sample_files']:
            print(f"   📋 Sample files: {', '.join(info['sample_files'][:3])}...") 