#!/usr/bin/env python3
"""
Forensic QA Agent - THIN Content Validation
==========================================

THIN Principle: LLM provides validation intelligence, software provides infrastructure.
This agent uses LLM intelligence to detect text hallucination, not hardcoded parsing.

CRITICAL FAILURE ADDRESSED: In MVA Experiment 2, LLM analyzed completely
fabricated populist text instead of actual criminal justice reform speech.
"""

import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Any

class ForensicQAAgent:
    """
    THIN forensic validation agent that uses LLM intelligence to detect text hallucination.
    """
    
    def __init__(self, gateway):
        self.gateway = gateway
        self.validation_log = []
        
    def validate_content_integrity(self, corpus_file_path: Path, corpus_text: str, 
                                 llm_response: str) -> Dict[str, Any]:
        """
        THIN validation: Use LLM intelligence to detect text hallucination.
        """
        
        # Create forensic record
        content_hash = hashlib.sha256(corpus_text.encode('utf-8')).hexdigest()[:12]
        
        # Use LLM intelligence for validation
        validation_prompt = f"""You are a forensic validation expert. Your job is to detect if an LLM hallucinated text content.

ACTUAL CORPUS TEXT:
{corpus_text[:500]}...

LLM RESPONSE CLAIMING TO ANALYZE THIS TEXT:
{llm_response[:1000]}...

VALIDATION TASK:
Does the LLM response contain quoted text that matches the actual corpus text? 
Look for text the LLM claims to be analyzing and compare it to the actual content.

Respond with:
VALID: [YES/NO]
CONFIDENCE: [HIGH/MEDIUM/LOW]
EXPLANATION: [Brief explanation of your finding]
EVIDENCE: [Key phrases that match or don't match]"""

        # Get LLM validation decision
        validation_response, metadata = self.gateway.execute_call(
            model="vertex_ai/gemini-2.5-pro",  # Fast, cheap model for validation
            prompt=validation_prompt,
            system_prompt="You are a forensic text validation expert."
        )
        
        # Simple parsing of LLM decision (minimal THIN parsing)
        is_valid = "VALID: YES" in validation_response
        
        validation_result = {
            'valid': is_valid,
            'content_hash': content_hash,
            'corpus_file': str(corpus_file_path),
            'actual_length': len(corpus_text),
            'validation_timestamp': datetime.now().isoformat(),
            'llm_validation_response': validation_response,
            'validation_model': metadata.get('model', 'unknown'),
            'error': None if is_valid else "TEXT HALLUCINATION DETECTED by LLM validator"
        }
        
        self.validation_log.append(validation_result)
        return validation_result
    
    def pre_analysis_validation(self, corpus_file_path: Path, corpus_text: str) -> Dict[str, Any]:
        """
        THIN pre-analysis record: Simple forensic logging without complex logic.
        """
        
        content_hash = hashlib.sha256(corpus_text.encode('utf-8')).hexdigest()[:12]
        
        return {
            'corpus_file': str(corpus_file_path),
            'content_hash': content_hash,
            'text_length': len(corpus_text),
            'first_100_chars': corpus_text[:100],
            'last_100_chars': corpus_text[-100:] if len(corpus_text) > 100 else corpus_text,
            'validation_timestamp': datetime.now().isoformat(),
            'validation_type': 'pre_analysis'
        }
    
    def get_forensic_report(self) -> Dict[str, Any]:
        """Simple forensic report generation."""
        
        total_validations = len(self.validation_log)
        failed_validations = [v for v in self.validation_log if not v['valid']]
        
        return {
            'total_validations': total_validations,
            'failed_validations': len(failed_validations),
            'failures': failed_validations,
            'report_timestamp': datetime.now().isoformat()
        } 