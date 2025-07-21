#!/usr/bin/env python3
"""
Session Summarizer - THIN LLM-powered research session naming
===========================================================

THIN Principle: Let LLM generate friendly names and summaries for research sessions
Software just orchestrates the LLM call and returns results - zero intelligence
"""

import json
import sys
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

try:
    from discernus.core.ultra_thin_llm_client import UltraThinLLMClient as ThinLiteLLMClient
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False


class SessionSummarizer:
    """
    THIN session summarizer - LLM generates friendly names and summaries
    Software provides zero intelligence, just orchestrates LLM calls
    """
    
    def __init__(self):
        if LITELLM_AVAILABLE:
            self.llm_client = ThinLiteLLMClient()
        else:
            self.llm_client = None
    
    def generate_session_manifest(self, session_path: Path) -> Dict[str, Any]:
        """
        Generate friendly name and summary for a research session
        
        THIN Principle: LLM does all the intelligence, software just orchestrates
        THIN Caching: Simple file-based cache with timestamp invalidation
        """
        # Check for cached manifest first
        cached_manifest = self._load_cached_manifest(session_path)
        if cached_manifest:
            return cached_manifest
        
        # Read session metadata and conversation
        metadata = self._read_session_metadata(session_path)
        conversation_preview = self._read_conversation_preview(session_path)
        
        if not metadata or not conversation_preview:
            return self._generate_fallback_manifest(session_path)
        
        # Let LLM generate intelligent summary
        manifest = self._call_llm_summarizer(metadata, conversation_preview)
        
        # Add technical details software can provide
        manifest['session_path'] = str(session_path)
        manifest['timestamp'] = metadata.get('started_at', '')
        manifest['research_question'] = metadata.get('research_question', '')
        
        # Cache the result
        self._save_cached_manifest(session_path, manifest)
        
        return manifest
    
    def _read_session_metadata(self, session_path: Path) -> Optional[Dict[str, Any]]:
        """Read metadata.json if it exists"""
        metadata_file = session_path / "metadata.json"
        if not metadata_file.exists():
            return None
        
        try:
            with open(metadata_file, 'r') as f:
                return json.load(f)
        except Exception:
            return None
    
    def _read_conversation_preview(self, session_path: Path) -> Optional[str]:
        """Read first 2000 chars of conversation for context"""
        conversation_file = session_path / "conversation_readable.md"
        if not conversation_file.exists():
            return None
        
        try:
            with open(conversation_file, 'r', encoding='utf-8') as f:
                return f.read(2000)  # First 2000 chars for context
        except Exception:
            return None
    
    def _call_llm_summarizer(self, metadata: Dict[str, Any], conversation_preview: str) -> Dict[str, Any]:
        """
        Call LLM to generate friendly name and summary
        
        THIN Principle: All intelligence happens in LLM, software just calls and returns
        """
        research_question = metadata.get('research_question', 'Unknown research question')
        
        llm_prompt = f"""You are a research session summarizer. Generate a user-friendly manifest for this academic research session.

RESEARCH QUESTION: {research_question}

CONVERSATION PREVIEW:
{conversation_preview}

Based on this information, generate a JSON response with:
1. "friendly_name": A concise 2-4 word title describing the research focus
2. "summary": A 1-2 sentence academic summary of what was studied
3. "key_findings": Array of 2-3 bullet points highlighting main insights (only if analysis is complete)
4. "corpus_description": Brief description of the texts/data analyzed

Format as valid JSON. Be concise and academic in tone.

Example format:
{{
  "friendly_name": "Populist Rhetoric Evolution",
  "summary": "Analysis of strategic populist deployment across different campaign audiences in 2018 Brazilian election.",
  "key_findings": [
    "Strategic audience-specific rhetoric deployment identified",
    "Evolution from August to October 2018 documented"
  ],
  "corpus_description": "12 Bolsonaro campaign speeches from July-October 2018"
}}"""

        if self.llm_client:
            response = self.llm_client.call_llm(llm_prompt, "session_summarizer")
            return self._parse_llm_response(response)
        else:
            return self._generate_mock_manifest(metadata)
    
    def _parse_llm_response(self, response: str) -> Dict[str, Any]:
        """
        Parse LLM response as JSON
        
        THIN Principle: Minimal parsing, fallback gracefully
        """
        try:
            # Try to extract JSON from response
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
            else:
                return {"friendly_name": "Research Session", "summary": "LLM response could not be parsed"}
        except Exception:
            return {"friendly_name": "Research Session", "summary": "LLM response could not be parsed"}
    
    def _generate_mock_manifest(self, metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Generate mock manifest for testing"""
        research_question = metadata.get('research_question', 'Unknown')
        
        if 'bolsonaro' in research_question.lower():
            return {
                "friendly_name": "Bolsonaro Rhetoric Analysis",
                "summary": "Analysis of populist rhetoric in Brazilian campaign speeches.",
                "key_findings": ["Mock finding 1", "Mock finding 2"],
                "corpus_description": "Political speech corpus"
            }
        elif 'lincoln' in research_question.lower():
            return {
                "friendly_name": "Lincoln vs Trump Analysis",
                "summary": "Comparative analysis of presidential inaugural addresses.",
                "key_findings": ["Mock comparative finding"],
                "corpus_description": "2 inaugural addresses"
            }
        else:
            return {
                "friendly_name": "Research Session",
                "summary": f"Analysis of: {research_question[:50]}...",
                "corpus_description": "Research corpus"
            }
    
    def _load_cached_manifest(self, session_path: Path) -> Optional[Dict[str, Any]]:
        """
        Load cached manifest if it exists and is fresh
        
        THIN Principle: Simple timestamp comparison, no intelligence
        """
        cache_file = session_path / "session_manifest.json"
        conversation_file = session_path / "conversation_readable.md"
        
        # Check if cache exists
        if not cache_file.exists():
            return None
        
        # Check if cache is fresh (newer than conversation file)
        if conversation_file.exists():
            cache_time = cache_file.stat().st_mtime
            conversation_time = conversation_file.stat().st_mtime
            
            if cache_time < conversation_time:
                # Cache is stale
                return None
        
        # Load cached manifest
        try:
            with open(cache_file, 'r') as f:
                return json.load(f)
        except Exception:
            # Corrupted cache, ignore
            return None
    
    def _save_cached_manifest(self, session_path: Path, manifest: Dict[str, Any]) -> None:
        """
        Save manifest to cache file
        
        THIN Principle: Simple file write, no intelligence
        """
        cache_file = session_path / "session_manifest.json"
        
        try:
            with open(cache_file, 'w') as f:
                json.dump(manifest, f, indent=2)
        except Exception:
            # Cache write failed, continue without caching
            pass

    def _generate_fallback_manifest(self, session_path: Path) -> Dict[str, Any]:
        """Generate basic manifest when files are missing"""
        return {
            "friendly_name": "Research Session",
            "summary": "Session metadata or conversation not available",
            "session_path": str(session_path),
            "timestamp": "",
            "research_question": "Unknown",
            "corpus_description": "Unknown corpus"
        }


def summarize_session(session_path: str) -> Dict[str, Any]:
    """
    Convenience function to summarize a single session
    
    THIN interface: Just call and return, no complex logic
    """
    summarizer = SessionSummarizer()
    return summarizer.generate_session_manifest(Path(session_path))


def summarize_all_sessions(sessions_dir: str = "research_sessions") -> Dict[str, Dict[str, Any]]:
    """
    Generate manifests for all completed research sessions
    
    THIN approach: Only process sessions with readable conversation files
    """
    sessions_path = Path(sessions_dir)
    if not sessions_path.exists():
        return {}
    
    summarizer = SessionSummarizer()
    manifests = {}
    
    for session_folder in sessions_path.iterdir():
        if not session_folder.is_dir():
            continue
        
        # Only process completed sessions (have readable conversation)
        conversation_file = session_folder / "conversation_readable.md"
        if not conversation_file.exists():
            continue
        
        manifest = summarizer.generate_session_manifest(session_folder)
        manifests[session_folder.name] = manifest
    
    return manifests


if __name__ == "__main__":
    # Test the summarizer
    print("🔬 Testing Session Summarizer...")
    
    # Test with existing session
    test_session = "research_sessions/session_20250704_083032"
    if Path(test_session).exists():
        manifest = summarize_session(test_session)
        print(f"✅ Generated manifest: {manifest}")
    
    # Test summarizing all sessions
    all_manifests = summarize_all_sessions()
    print(f"✅ Found {len(all_manifests)} completed sessions")
    for session_id, manifest in all_manifests.items():
        print(f"  📂 {manifest['friendly_name']} ({session_id})") 