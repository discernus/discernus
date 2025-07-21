#!/usr/bin/env python3
"""
Corpus Inspector - File Reading Infrastructure for Corpus Detective Agent
=========================================================================

THIN Principle: Provides robust file system operations for corpus detective agent.
Software handles messy real-world file reading; LLM provides intelligence about content.

This is the infrastructure equivalent of discernuslibrarian.py - the corpus detective agent
needs this to actually inspect files from user-provided directories.
"""

import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple, Any, Optional

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.core.corpus_chunking import (
    should_use_chunking, 
    analyze_corpus_in_chunks, 
    estimate_token_count,
    chunk_corpus_by_size
)

try:
    from discernus.core.ultra_thin_llm_client import UltraThinLLMClient as ThinLiteLLMClient
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False


class CorpusInspector:
    """
    THIN corpus file inspection infrastructure
    
    Provides robust file reading for corpus detective agent to analyze messy real-world corpora.
    Software handles file system operations; LLM provides intelligence about content.
    """
    
    def __init__(self):
        if LITELLM_AVAILABLE:
            self.llm_client = ThinLiteLLMClient()
        else:
            self.llm_client = None
    
    def inspect_directory_corpus(self, directory_path: str) -> Tuple[Dict[str, str], List[str]]:
        """
        Read all files from user-provided directory with robust error handling
        
        Args:
            directory_path: Path to directory containing corpus files
            
        Returns:
            Tuple of (files_dict, errors_list)
            - files_dict: {filename: content} for successfully read files
            - errors_list: List of error messages for problematic files
            
        THIN Principle: Pure file system operations with graceful error handling
        """
        print(f"\n📖 Reading corpus from: {directory_path}")
        
        files = {}
        errors = []
        
        if not os.path.exists(directory_path):
            return {}, [f"Directory not found: {directory_path}"]
        
        if not os.path.isdir(directory_path):
            return {}, [f"Path is not a directory: {directory_path}"]
        
        try:
            for filename in os.listdir(directory_path):
                file_path = os.path.join(directory_path, filename)
                
                # Skip directories and system files
                if os.path.isdir(file_path) or filename.startswith('.'):
                    continue
                
                file_content, file_error = self._read_single_file(file_path, filename)
                
                if file_content is not None:
                    files[filename] = file_content
                    print(f"  ✅ {filename}: {len(file_content)} chars")
                else:
                    errors.append(file_error)
                    print(f"  ❌ {filename}: {file_error}")
        
        except Exception as e:
            return {}, [f"Error reading directory {directory_path}: {str(e)}"]
        
        print(f"\n📊 Read {len(files)} files successfully")
        if errors:
            print(f"⚠️  {len(errors)} files had issues")
        
        return files, errors
    
    def _read_single_file(self, file_path: str, filename: str) -> Tuple[Optional[str], Optional[str]]:
        """
        Read a single file with encoding fallback
        
        Returns:
            Tuple of (content, error_message)
            - If successful: (content_string, None)
            - If failed: (None, error_message)
            
        THIN Principle: Robust encoding detection with graceful fallback
        """
        try:
            # Try UTF-8 first (most common)
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                return content, None
        except UnicodeDecodeError:
            try:
                # Fallback to latin-1 for legacy files
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
                    return content, None
            except Exception as e:
                return None, f"Encoding error: {str(e)}"
        except Exception as e:
            return None, f"Read error: {str(e)}"
    
    async def analyze_corpus_with_detective(self, files: Dict[str, str], research_question: str = "") -> str:
        """
        Analyze corpus using corpus detective agent with rate limit management
        
        Args:
            files: Dictionary of {filename: content}
            research_question: Optional research question for context
            
        Returns:
            Detective analysis report
            
        THIN Principle: Minimal orchestration, maximum LLM intelligence
        """
        if not files:
            return "No files provided for analysis."
        
        # Check if we need chunking for rate limit management
        total_tokens = sum(estimate_token_count(content) for content in files.values())
        print(f"📊 Total corpus size: ~{total_tokens:,} tokens")
        
        if should_use_chunking(files):
            print("🔄 Large corpus detected - using intelligent chunking...")
            return await analyze_corpus_in_chunks(files, self.llm_client)
        else:
            # Small corpus - analyze directly
            return await self._analyze_corpus_direct(files, research_question)
    
    async def _analyze_corpus_direct(self, files: Dict[str, str], research_question: str) -> str:
        """
        Direct corpus analysis for smaller corpora
        
        THIN Principle: Build prompt, call LLM, return result
        """
        # Build corpus text for analysis
        corpus_text = "\n\n".join([
            f"FILE: {filename}\n{content}" 
            for filename, content in files.items()
        ])
        
        # Build detective prompt
        detective_prompt = f"""You are a corpus detective analyzing a user-provided text corpus.

RESEARCH CONTEXT: {research_question or "General corpus analysis"}

CORPUS TO ANALYZE:
{corpus_text}

Your Task:
Analyze this corpus systematically and provide a structured report covering:

1. **Document Inventory**: What types of texts and how many of each
2. **Authorship & Sources**: Who created these texts and their contexts  
3. **Time Periods**: What timeframes are covered
4. **Content Themes**: Major topics and subjects present
5. **Technical Issues**: Any encoding, formatting, or quality problems
6. **Metadata Gaps**: What information is missing or unclear
7. **Clarifying Questions**: Specific questions to resolve ambiguities

Be systematic but practical - help the researcher understand their corpus for effective analysis."""
        
        print("🤖 Calling LLM for corpus analysis...")
        
        if self.llm_client:
            response = self.llm_client.call_llm(detective_prompt, "corpus_detective")
        else:
            response = f"""**CORPUS ANALYSIS REPORT**

**Document Inventory**: {len(files)} files detected
**Authorship & Sources**: Analysis would require LLM client
**Time Periods**: Cannot determine without LLM analysis
**Content Themes**: Requires content analysis
**Technical Issues**: No obvious encoding issues detected
**Metadata Gaps**: Full analysis requires LLM client
**Clarifying Questions**: What specific aspects should be prioritized?

*Note: Mock response - LLM client not available*"""
        
        return response
    
    def create_corpus_preview(self, files: Dict[str, str], max_preview_files: int = 5) -> str:
        """
        Create a preview of the corpus for logging/display
        
        THIN Principle: Simple text formatting, no intelligence
        """
        preview_lines = []
        
        for i, (filename, content) in enumerate(files.items()):
            if i >= max_preview_files:
                preview_lines.append(f"... and {len(files) - max_preview_files} more files")
                break
            
            preview_lines.append(f"**{filename}** ({len(content)} chars)")
            # Show first few lines
            lines = content.split('\n')[:3]
            preview_lines.append("```")
            for line in lines:
                preview_lines.append(line[:100] + "..." if len(line) > 100 else line)
            preview_lines.append("```")
            preview_lines.append("")
        
        return "\n".join(preview_lines)
    
    def get_corpus_stats(self, files: Dict[str, str]) -> Dict[str, Any]:
        """
        Get basic statistics about the corpus
        
        THIN Principle: Simple counting operations, no interpretation
        """
        if not files:
            return {"file_count": 0, "total_chars": 0, "total_tokens": 0, "file_types": []}
        
        total_chars = sum(len(content) for content in files.values())
        total_tokens = sum(estimate_token_count(content) for content in files.values())
        
        # Extract file extensions
        file_types = set()
        for filename in files.keys():
            if '.' in filename:
                file_types.add(filename.split('.')[-1].lower())
        
        return {
            "file_count": len(files),
            "total_chars": total_chars,
            "total_tokens": total_tokens,
            "file_types": list(file_types),
            "avg_file_size": total_chars // len(files) if files else 0
        }


# Convenience functions for easy integration
def inspect_corpus_directory(directory_path: str) -> Tuple[Dict[str, str], List[str]]:
    """
    Convenience function to inspect a corpus directory
    
    Returns:
        Tuple of (files_dict, errors_list)
    """
    inspector = CorpusInspector()
    return inspector.inspect_directory_corpus(directory_path)


async def analyze_corpus_directory(directory_path: str, research_question: str = "") -> str:
    """
    Convenience function to inspect and analyze a corpus directory
    
    Returns:
        Detective analysis report
    """
    inspector = CorpusInspector()
    files, errors = inspector.inspect_directory_corpus(directory_path)
    
    if not files:
        error_summary = "\n".join(errors) if errors else "No files found in directory"
        return f"❌ Could not read corpus from {directory_path}\n\nErrors:\n{error_summary}"
    
    analysis = await inspector.analyze_corpus_with_detective(files, research_question)
    
    if errors:
        analysis += f"\n\n⚠️ **File Reading Issues:**\n" + "\n".join(f"- {error}" for error in errors)
    
    return analysis


if __name__ == "__main__":
    import asyncio
    
    # Test corpus inspection
    print("🔍 Corpus Inspector Test")
    print("=" * 40)
    
    test_directory = input("Enter directory path to inspect: ").strip()
    
    if test_directory:
        inspector = CorpusInspector()
        files, errors = inspector.inspect_directory_corpus(test_directory)
        
        print(f"\n📊 Corpus Statistics:")
        stats = inspector.get_corpus_stats(files)
        for key, value in stats.items():
            print(f"  {key}: {value}")
        
        if files:
            print(f"\n📋 Corpus Preview:")
            preview = inspector.create_corpus_preview(files)
            print(preview)
            
            print(f"\n🔍 Running Detective Analysis...")
            analysis = asyncio.run(inspector.analyze_corpus_with_detective(files, "Test analysis"))
            print(f"\n📋 Detective Report:")
            print("=" * 60)
            print(analysis) 