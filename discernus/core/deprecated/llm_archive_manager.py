#!/usr/bin/env python3
"""
LLM Archive Manager
==================

THIN Principle: This component is a pure utility for immediate file persistence.
It takes LLM responses and saves them to individual files within 500ms to prevent
data loss. It has no intelligence - just fast, reliable file I/O.
"""

import json
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional
import threading
import uuid

class LLMArchiveManager:
    """
    Manages immediate persistence of LLM responses to individual files.
    
    Key Requirements:
    - Save responses within 500ms of completion
    - Individual files (response_001.txt, response_002.txt) not monolithic blobs
    - Include comprehensive metadata for forensic analysis
    - Thread-safe for concurrent LLM calls
    """
    
    def __init__(self, session_path: Path):
        """
        Initialize the archive manager for a specific session.
        
        Args:
            session_path: Path to the session directory
        """
        self.session_path = Path(session_path)
        self.archive_path = self.session_path / "llm_archive"
        self.archive_path.mkdir(parents=True, exist_ok=True)
        
        # Thread-safe counter for response numbering
        self._counter = 0
        self._lock = threading.Lock()
        
        # Metadata tracking
        self.metadata_file = self.archive_path / "metadata.jsonl"
        
    def save_call(self, prompt: str, system_prompt: str, response: str, 
                  model: str, usage_data: Dict[str, Any], 
                  success: bool = True, error: Optional[str] = None) -> str:
        """
        Save LLM call data immediately upon response.
        
        Args:
            prompt: The user prompt sent to the LLM
            system_prompt: The system prompt used
            response: The LLM response content
            model: The model identifier used
            usage_data: Token usage statistics
            success: Whether the call succeeded
            error: Error message if call failed
            
        Returns:
            call_id: Unique identifier for this call
        """
        start_time = time.time()
        
        # Generate unique call ID and get sequential number
        call_id = str(uuid.uuid4())[:8]
        
        with self._lock:
            self._counter += 1
            call_number = self._counter
            
        # Create filename with zero-padded number
        response_file = self.archive_path / f"response_{call_number:03d}.txt"
        prompt_file = self.archive_path / f"prompt_{call_number:03d}.txt"
        
        # Create comprehensive metadata
        metadata = {
            "call_id": call_id,
            "call_number": call_number,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "model": model,
            "success": success,
            "error": error if error is not None else "",
            "usage": usage_data,
            "response_file": str(response_file.name),
            "prompt_file": str(prompt_file.name),
            "prompt_length": len(prompt),
            "response_length": len(response) if response else 0,
            "system_prompt_length": len(system_prompt)
        }
        
        try:
            # Save response content
            with open(response_file, 'w', encoding='utf-8') as f:
                f.write(response or "")
                
            # Save prompt content
            with open(prompt_file, 'w', encoding='utf-8') as f:
                f.write(f"=== SYSTEM PROMPT ===\n{system_prompt}\n\n=== USER PROMPT ===\n{prompt}")
                
            # Append metadata to JSONL file
            with open(self.metadata_file, 'a', encoding='utf-8') as f:
                f.write(json.dumps(metadata) + '\n')
                
        except Exception as e:
            # If file writing fails, we still want to return the call_id
            # but log the persistence failure
            print(f"❌ LLMArchiveManager persistence failed for call {call_id}: {e}")
            metadata["persistence_error"] = str(e)
            
        # Check if we met the 500ms requirement
        elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        metadata["persistence_time_ms"] = elapsed_time
        
        if elapsed_time > 500:
            print(f"⚠️ LLMArchiveManager took {elapsed_time:.1f}ms (>500ms target) for call {call_id}")
            
        return call_id
    
    def load_call(self, call_id: str) -> Optional[Dict[str, Any]]:
        """
        Load existing LLM call data by ID.
        
        Args:
            call_id: The unique identifier for the call
            
        Returns:
            Dictionary containing call data or None if not found
        """
        # Find the call in metadata
        if not self.metadata_file.exists():
            return None
            
        try:
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                for line in f:
                    metadata = json.loads(line.strip())
                    if metadata.get("call_id") == call_id:
                        # Load the actual content files
                        response_file = self.archive_path / metadata["response_file"]
                        prompt_file = self.archive_path / metadata["prompt_file"]
                        
                        response_content = ""
                        prompt_content = ""
                        
                        if response_file.exists():
                            with open(response_file, 'r', encoding='utf-8') as rf:
                                response_content = rf.read()
                                
                        if prompt_file.exists():
                            with open(prompt_file, 'r', encoding='utf-8') as pf:
                                prompt_content = pf.read()
                                
                        return {
                            "metadata": metadata,
                            "response": response_content,
                            "prompt_content": prompt_content
                        }
                        
        except Exception as e:
            print(f"❌ Failed to load call {call_id}: {e}")
            return None
            
        return None
    
    def exists(self, call_id: str) -> bool:
        """
        Check if call already exists (prevent duplicate API calls).
        
        Args:
            call_id: The unique identifier for the call
            
        Returns:
            True if call exists, False otherwise
        """
        return self.load_call(call_id) is not None
    
    def get_call_statistics(self) -> Dict[str, Any]:
        """
        Get statistics about archived calls.
        
        Returns:
            Dictionary with call statistics
        """
        if not self.metadata_file.exists():
            return {"total_calls": 0, "successful_calls": 0, "failed_calls": 0}
            
        total_calls = 0
        successful_calls = 0
        failed_calls = 0
        total_tokens = 0
        models_used = set()
        
        try:
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                for line in f:
                    metadata = json.loads(line.strip())
                    total_calls += 1
                    
                    if metadata.get("success", False):
                        successful_calls += 1
                    else:
                        failed_calls += 1
                        
                    usage = metadata.get("usage", {})
                    total_tokens += usage.get("total_tokens", 0)
                    models_used.add(metadata.get("model", "unknown"))
                    
        except Exception as e:
            print(f"❌ Failed to generate statistics: {e}")
            
        return {
            "total_calls": total_calls,
            "successful_calls": successful_calls,
            "failed_calls": failed_calls,
            "success_rate": successful_calls / total_calls if total_calls > 0 else 0,
            "total_tokens": total_tokens,
            "models_used": list(models_used)
        }
    
    def list_calls(self) -> list:
        """
        List all archived calls with basic metadata.
        
        Returns:
            List of call metadata dictionaries
        """
        calls = []
        
        if not self.metadata_file.exists():
            return calls
            
        try:
            with open(self.metadata_file, 'r', encoding='utf-8') as f:
                for line in f:
                    metadata = json.loads(line.strip())
                    calls.append(metadata)
                    
        except Exception as e:
            print(f"❌ Failed to list calls: {e}")
            
        return calls 