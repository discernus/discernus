#!/usr/bin/env python3
"""
Provenance Stamp System - Tamper-Evident Content Tracking
========================================================

THIN Principle: Simple cryptographic stamps that detect content tampering.
This system creates content hashes that must match throughout the pipeline.

CRITICAL FAILURE ADDRESSED: The hallucination incident where LLM analyzed
fabricated text instead of actual corpus content would be immediately detected.
"""

# Copyright (C) 2025  Discernus Team

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import hashlib
import json
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, Optional

class ProvenanceStamp:
    """
    Creates tamper-evident stamps for content integrity throughout analysis pipeline.
    """
    
    def __init__(self, content: str, source_file: Path, stamp_type: str = "corpus"):
        """
        Create a provenance stamp for content.
        
        Args:
            content: The actual text content
            source_file: Path to the source file
            stamp_type: Type of content (corpus, analysis, etc.)
        """
        self.content_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        self.short_hash = self.content_hash[:12]  # First 12 chars for readability
        self.source_file = str(source_file)
        self.stamp_type = stamp_type
        self.created_at = datetime.now().isoformat()
        self.content_length = len(content)
        self.content_preview = content[:100]  # First 100 chars for verification
        
    def to_dict(self) -> Dict[str, Any]:
        """Convert stamp to dictionary for logging."""
        return {
            'content_hash': self.content_hash,
            'short_hash': self.short_hash,
            'source_file': self.source_file,
            'stamp_type': self.stamp_type,
            'created_at': self.created_at,
            'content_length': self.content_length,
            'content_preview': self.content_preview
        }
    
    def verify_content(self, content: str) -> Dict[str, Any]:
        """
        Verify that content matches this stamp.
        
        Args:
            content: Content to verify against stamp
            
        Returns:
            Verification result with success/failure details
        """
        current_hash = hashlib.sha256(content.encode('utf-8')).hexdigest()
        
        return {
            'verified': current_hash == self.content_hash,
            'original_hash': self.short_hash,
            'current_hash': current_hash[:12],
            'verification_timestamp': datetime.now().isoformat(),
            'error': None if current_hash == self.content_hash else "CONTENT TAMPERING DETECTED"
        }
    
    def create_reference_stamp(self) -> str:
        """
        Create a reference stamp string that can be embedded in prompts/responses.
        This allows validation that LLM is referencing the correct content.
        """
        return f"[PROVENANCE:{self.short_hash}@{self.source_file}]"

class ProvenanceTracker:
    """
    Tracks provenance stamps throughout the analysis pipeline.
    """
    
    def __init__(self):
        self.stamps = {}
        self.validation_log = []
        
    def register_corpus_file(self, corpus_file: Path, content: str) -> ProvenanceStamp:
        """
        Register a corpus file with provenance stamp.
        
        Args:
            corpus_file: Path to corpus file
            content: Content of the file
            
        Returns:
            ProvenanceStamp for the file
        """
        stamp = ProvenanceStamp(content, corpus_file, "corpus")
        self.stamps[str(corpus_file)] = stamp
        return stamp
    
    def validate_llm_response(self, corpus_file: Path, llm_response: str) -> Dict[str, Any]:
        """
        Validate that LLM response contains the correct provenance stamp.
        This catches hallucination where LLM claims to analyze different content.
        
        Args:
            corpus_file: Original corpus file
            llm_response: LLM response to validate
            
        Returns:
            Validation result
        """
        corpus_key = str(corpus_file)
        
        if corpus_key not in self.stamps:
            return {
                'valid': False,
                'error': f"No provenance stamp found for {corpus_file}",
                'timestamp': datetime.now().isoformat()
            }
        
        stamp = self.stamps[corpus_key]
        expected_reference = stamp.create_reference_stamp()
        
        # Check if LLM response contains the correct provenance reference
        has_correct_stamp = expected_reference in llm_response
        
        validation_result = {
            'valid': has_correct_stamp,
            'corpus_file': corpus_key,
            'expected_stamp': expected_reference,
            'stamp_found': has_correct_stamp,
            'original_hash': stamp.short_hash,
            'validation_timestamp': datetime.now().isoformat(),
            'error': None if has_correct_stamp else f"PROVENANCE TAMPERING: Expected {expected_reference} not found in response"
        }
        
        self.validation_log.append(validation_result)
        return validation_result
    
    def create_analysis_prompt_with_stamp(self, corpus_file: Path, content: str, base_prompt: str) -> str:
        """
        Create analysis prompt that includes provenance stamp.
        This ensures the LLM knows what content it should be analyzing.
        
        Args:
            corpus_file: Path to corpus file
            content: Content to analyze
            base_prompt: Base analysis prompt
            
        Returns:
            Enhanced prompt with provenance stamp
        """
        if str(corpus_file) not in self.stamps:
            self.register_corpus_file(corpus_file, content)
        
        stamp = self.stamps[str(corpus_file)]
        reference_stamp = stamp.create_reference_stamp()
        
        enhanced_prompt = f"""{base_prompt}

PROVENANCE VERIFICATION:
You are analyzing content from file: {corpus_file}
Content hash: {stamp.short_hash}
Content preview: "{stamp.content_preview}..."

CRITICAL: You must include this provenance stamp in your response: {reference_stamp}

TEXT TO ANALYZE:
{content}

Remember to include the provenance stamp {reference_stamp} in your response to verify content integrity."""
        
        return enhanced_prompt
    
    def get_provenance_report(self) -> Dict[str, Any]:
        """Generate complete provenance report."""
        
        total_validations = len(self.validation_log)
        failed_validations = [v for v in self.validation_log if not v['valid']]
        
        return {
            'registered_files': len(self.stamps),
            'total_validations': total_validations,
            'failed_validations': len(failed_validations),
            'failures': failed_validations,
            'stamps': {k: v.to_dict() for k, v in self.stamps.items()},
            'report_timestamp': datetime.now().isoformat()
        } 