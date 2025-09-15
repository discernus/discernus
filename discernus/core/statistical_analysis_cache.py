#!/usr/bin/env python3
"""
Statistical Analysis Cache Manager - THIN Component
==================================================

Manages caching of statistical analysis function generation for development velocity.
Pure software component - no LLM intelligence.
"""

import json
import hashlib
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger


@dataclass
class StatisticalAnalysisCacheResult:
    """Result of statistical analysis cache lookup."""
    hit: bool
    artifact_hash: Optional[str] = None
    cached_functions: Optional[Dict[str, Any]] = None


class StatisticalAnalysisCacheManager:
    """
    Manages caching of statistical analysis function generation using content-addressable storage.
    
    THIN Principle: Pure software caching infrastructure.
    No LLM intelligence - just deterministic cache management.
    """
    
    def __init__(self, storage: LocalArtifactStorage, audit: AuditLogger):
        self.storage = storage
        self.audit = audit
    
    def generate_cache_key(self, framework_content: str, experiment_content: str, 
                          corpus_content: str, model: str) -> str:
        """
        Generate deterministic cache key for statistical analysis functions.
        
        Args:
            framework_content: Framework markdown content
            experiment_content: Experiment markdown content
            corpus_content: Corpus manifest content
            model: LLM model used for function generation
            
        Returns:
            Deterministic cache key based on input content hashes and model
        """
        # Include prompt template hash to invalidate cache when prompt changes
        prompt_template_hash = self._get_prompt_template_hash()
        
        # Combine all input content for cache key (not outputs from previous phases)
        combined_content = f'{framework_content}{experiment_content}{corpus_content}{model}{prompt_template_hash}'
        cache_hash = hashlib.sha256(combined_content.encode()).hexdigest()[:12]
        
        return f"statistical_analysis_{cache_hash}"
    
    def _extract_python_code_from_response(self, llm_response: str) -> str:
        """
        Extract Python code from StatisticalAgent LLM response.
        
        Args:
            llm_response: Raw LLM response containing Python code
            
        Returns:
            Extracted Python code or empty string if not found
        """
        if not llm_response:
            return ""
        
        # Look for Python code blocks in markdown format
        import re
        
        # Pattern 1: ```python ... ```
        python_pattern = r'```python\s*\n(.*?)\n```'
        match = re.search(python_pattern, llm_response, re.DOTALL)
        if match:
            return match.group(1).strip()
        
        # Pattern 2: ``` ... ``` (generic code block)
        code_pattern = r'```\s*\n(.*?)\n```'
        match = re.search(code_pattern, llm_response, re.DOTALL)
        if match:
            code = match.group(1).strip()
            # Check if it looks like Python code
            if any(keyword in code for keyword in ['import ', 'def ', 'class ', 'pandas', 'numpy']):
                return code
        
        # Pattern 3: Look for function definitions directly
        if 'def ' in llm_response and 'import ' in llm_response:
            # Try to extract everything from the first import to the end
            lines = llm_response.split('\n')
            start_idx = None
            for i, line in enumerate(lines):
                if line.strip().startswith('import '):
                    start_idx = i
                    break
            
            if start_idx is not None:
                return '\n'.join(lines[start_idx:]).strip()
        
        return ""
    
    def _get_prompt_template_hash(self) -> str:
        """Get hash of the current prompt template to invalidate cache when prompt changes."""
        try:
            from pathlib import Path
            prompt_path = Path(__file__).parent.parent / "agents" / "automated_statistical_analysis" / "prompt.yaml"
            if prompt_path.exists():
                prompt_content = prompt_path.read_text(encoding='utf-8')
                return hashlib.sha256(prompt_content.encode()).hexdigest()[:8]
        except Exception:
            pass
        return "unknown"
    
    def check_cache(self, cache_key: str, agent_name: str = "StatisticalAnalysisAgent") -> StatisticalAnalysisCacheResult:
        """
        Check if statistical analysis functions are already cached.
        
        Args:
            cache_key: Cache key for lookup
            agent_name: Name of the agent for logging
            
        Returns:
            StatisticalAnalysisCacheResult indicating hit/miss and cached functions if available
        """
        # Search through artifact registry for matching statistical analysis functions
        for artifact_hash, artifact_info in self.storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            
            if (metadata.get("artifact_type") == "statistical_analysis_functions" and
                metadata.get("cache_key") == cache_key):
                
                # Verify artifact actually exists before claiming cache hit
                if not self.storage.artifact_exists(artifact_hash):
                    print(f"⚠️ Cache metadata found but artifact missing: {cache_key} (hash: {artifact_hash[:8]})")
                    continue
                
                # Cache hit!
                pass  # Reduced verbosity - statistical analysis cache hit
                
                try:
                    cached_content = self.storage.get_artifact(artifact_hash)
                    cached_functions = json.loads(cached_content.decode('utf-8'))
                    
                    self.audit.log_agent_event(agent_name, "cache_hit", {
                        "cache_key": cache_key,
                        "cached_artifact_hash": artifact_hash,
                        "phase": "statistical_analysis"
                    })
                    
                    return StatisticalAnalysisCacheResult(
                        hit=True,
                        artifact_hash=artifact_hash,
                        cached_functions=cached_functions
                    )
                    
                except Exception as e:
                    print(f"⚠️ Cache hit but failed to load statistical analysis functions: {e}")
                    # Continue searching for other cached results
                    continue
        
        # No cache hit
        pass  # Reduced verbosity - no statistical analysis cache hit
        return StatisticalAnalysisCacheResult(hit=False)
    
    def store_functions(self, cache_key: str, functions_result: Dict[str, Any], 
                       workspace_path: Optional[str] = None, metadata: Optional[Dict[str, Any]] = None) -> str:
        """
        Store statistical analysis functions in cache with actual function code.
        
        Args:
            cache_key: Cache key for the functions
            functions_result: Complete functions result to cache
            workspace_path: Path to workspace containing generated functions file
            metadata: Additional metadata for the artifact
            
        Returns:
            Hash of the stored artifact
        """
        # Create enhanced functions result that includes the actual function code
        enhanced_functions_result = functions_result.copy()
        
        # Check if this is from StatisticalAgent (THIN v2.0) or AutomatedStatisticalAnalysisAgent
        if 'statistical_analysis' in functions_result and 'statistical_functions_and_results' in functions_result['statistical_analysis']:
            # This is from StatisticalAgent - extract code from the LLM response
            statistical_analysis = functions_result['statistical_analysis']
            llm_response = statistical_analysis.get('statistical_functions_and_results', '')
            
            # Extract Python code from the LLM response
            function_code = self._extract_python_code_from_response(llm_response)
            if function_code:
                enhanced_functions_result['function_code_content'] = function_code
                enhanced_functions_result['cached_with_code'] = True
                print(f"💾 Cached statistical function code content from StatisticalAgent ({len(function_code)} chars)")
                
                # Also save to workspace if provided
                if workspace_path:
                    from pathlib import Path
                    functions_file = Path(workspace_path) / "automatedstatisticalanalysisagent_functions.py"
                    functions_file.write_text(function_code, encoding='utf-8')
                    print(f"📝 Saved statistical functions to workspace: {functions_file}")
            else:
                enhanced_functions_result['cached_with_code'] = False
                print(f"⚠️ Could not extract Python code from StatisticalAgent response")
        elif workspace_path:
            # This is from AutomatedStatisticalAnalysisAgent - read the function file
            from pathlib import Path
            functions_file = Path(workspace_path) / "automatedstatisticalanalysisagent_functions.py"
            if functions_file.exists():
                try:
                    function_code = functions_file.read_text(encoding='utf-8')
                    enhanced_functions_result['function_code_content'] = function_code
                    enhanced_functions_result['cached_with_code'] = True
                    print(f"💾 Cached statistical function code content from file ({len(function_code)} chars)")
                except Exception as e:
                    print(f"⚠️ Failed to read statistical function file for caching: {e}")
                    enhanced_functions_result['cached_with_code'] = False
            else:
                print(f"⚠️ Statistical function file not found for caching: {functions_file}")
                enhanced_functions_result['cached_with_code'] = False
        else:
            enhanced_functions_result['cached_with_code'] = False
        
        # Add cache-specific metadata
        cache_metadata = {
            **(metadata or {}),
            "artifact_type": "statistical_analysis_functions",
            "cache_key": cache_key,
            "functions_generated": enhanced_functions_result.get('functions_generated', 0),
            "generation_model": enhanced_functions_result.get('model', 'unknown'),
            "has_function_code": enhanced_functions_result.get('cached_with_code', False)
        }
        
        # Store the enhanced functions result
        functions_json = json.dumps(enhanced_functions_result, indent=2)
        artifact_hash = self.storage.put_artifact(
            functions_json.encode('utf-8'),
            cache_metadata
        )
        
        print(f"💾 Stored statistical analysis functions in cache: {cache_key} (with code: {enhanced_functions_result.get('cached_with_code', False)})")
        self.audit.log_agent_event("StatisticalAnalysisAgent", "cache_store", {
            "cache_key": cache_key,
            "artifact_hash": artifact_hash,
            "has_function_code": enhanced_functions_result.get('cached_with_code', False),
            "phase": "statistical_analysis"
        })
        
        return artifact_hash
