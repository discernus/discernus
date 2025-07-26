#!/usr/bin/env python3
"""
Batch Planner Agent for Discernus THIN v2.0
===========================================

REMOVAL TRIGGER: This component exists to manage context window limits in LLMs.
If/when LLM context windows become effectively unlimited, this entire file 
can be safely deleted and its integration points removed.

REMOVAL SEARCH TERMS: 
- "BatchPlannerAgent" 
- "batch_planner_agent"
- "context window management"
- "token footprint batching"

CURRENT PURPOSE:
Simple agent that creates optimal batches based on token footprints
and context window limits. Prevents 1M+ token errors that would otherwise
fail experiments with large corpora.

INTEGRATION POINTS TO REMOVE:
1. discernus/core/thin_orchestrator.py (import and usage)
2. discernus/agents/__init__.py (import statement)  
3. This file: discernus/agents/batch_planner_agent.py

ARCHITECTURAL RATIONALE:
Built to handle real context window limits discovered during testing
(47 presidential speeches = 1.4M tokens > 1M limit). Originally built
for rate limiting but repurposed for context management.
"""

import json
import time
from typing import Dict, Any, List, Tuple, Optional
from pathlib import Path
from datetime import datetime, timezone

from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger


class BatchPlannerAgent:
    """
    Simple batch planner that organizes corpus documents into batches
    based on token footprints and API rate limits.
    """
    
    def __init__(self, security_boundary: ExperimentSecurityBoundary, audit_logger: AuditLogger):
        self.security = security_boundary
        self.audit = audit_logger
        
        # Approximate token conversion rates
        self.CHARS_PER_TOKEN = 4  # Conservative estimate for English text
        self.PROMPT_OVERHEAD_TOKENS = 2000  # Instructions, formatting, JSON schemas
        self.DOCUMENT_OVERHEAD_TOKENS = 200  # Per-document metadata and structure
        
        print(f"📊 Batch planner initialized for experiment: {security_boundary.experiment_name}")
        print("🔧 CONTEXT_WINDOW_MANAGEMENT: Using context window limits (not TPM) for batch sizing")
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate token count from character count."""
        return len(text) // self.CHARS_PER_TOKEN
    
    def calculate_batch_tokens(self, framework_content: str, documents: List[Dict[str, Any]]) -> int:
        """Calculate total tokens for a batch including all overhead."""
        framework_tokens = self.estimate_tokens(framework_content)
        document_tokens = sum(self.estimate_tokens(doc.get('content', '')) for doc in documents)
        overhead_tokens = self.PROMPT_OVERHEAD_TOKENS + (len(documents) * self.DOCUMENT_OVERHEAD_TOKENS)
        
        total = framework_tokens + document_tokens + overhead_tokens
        return total
    
    def get_rate_limits(self, model: str) -> Dict[str, int]:
        """
        Get rate limits for the specified model.
        For Vertex AI, these are conservative estimates - actual limits may be higher due to DSQ.
        NOTE: These are for rate limiting, NOT context window management!
        """
        if "vertex_ai" in model:
            if "gemini-2.5-pro" in model:
                return {
                    "rpm": 5,          # Requests per minute (conservative for new projects)
                    "tpm": 250000,     # Tokens per minute 
                    "rpd": 100         # Requests per day (base tier)
                }
            elif "gemini-2.5-flash" in model:
                return {
                    "rpm": 15,         # Flash typically has higher RPM
                    "tpm": 1000000,    # Flash has higher TPM
                    "rpd": 1000        # Flash has higher daily limit
                }
        
        # Default conservative limits
        return {"rpm": 5, "tpm": 250000, "rpd": 100}
    
    def get_context_window_limit(self, model: str) -> int:
        """
        Get actual context window limits for batch sizing.
        
        CONTEXT_WINDOW_MANAGEMENT: This is the core fix - use context windows, not TPM!
        When LLM context windows become unlimited, this method can return a very large number.
        
        Args:
            model: LLM model identifier
            
        Returns:
            Maximum tokens per batch based on context window (with safety margin)
        """
        if "vertex_ai" in model:
            if "gemini-2.5-pro" in model:
                return 1_800_000  # 2M context window with 10% safety margin
            elif "gemini-2.5-flash" in model:
                return 900_000    # 1M context window with 10% safety margin
        
        # Conservative default for unknown models
        return 500_000
    
    def create_batches(self, 
                      framework_content: str, 
                      corpus_documents: List[Dict[str, Any]], 
                      model: str = "vertex_ai/gemini-2.5-flash") -> Dict[str, Any]:
        """
        Create optimal batches based on token footprints and rate limits.
        
        Returns:
            Dict containing batches, timing estimates, and execution plan
        """
        start_time = self._get_timestamp()
        
        # Get rate limits for this model
        limits = self.get_rate_limits(model)
        
        # CONTEXT_WINDOW_MANAGEMENT: Log the dramatic improvement in batch sizing
        context_window_limit = self.get_context_window_limit(model)
        old_tpm_limit = min(limits['tpm'] // 2, 100000)  # What it used to be
        improvement_factor = context_window_limit / old_tpm_limit
        
        self.audit.log_agent_event("BatchPlannerAgent", "batch_planning_start", {
            "model": model,
            "total_documents": len(corpus_documents),
            "framework_size_chars": len(framework_content),
            "context_window_limit": context_window_limit,
            "old_tpm_based_limit": old_tpm_limit,
            "improvement_factor": f"{improvement_factor:.1f}x larger batches"
        })
        
        # Calculate framework token overhead (constant across all batches)
        framework_tokens = self.estimate_tokens(framework_content)
        base_overhead = self.PROMPT_OVERHEAD_TOKENS + framework_tokens
        
        # Sort documents by size for better packing
        docs_with_tokens = []
        for doc in corpus_documents:
            doc_tokens = self.estimate_tokens(doc.get('content', ''))
            docs_with_tokens.append({
                **doc,
                'estimated_tokens': doc_tokens
            })
        
        # Sort by token count (largest first for better bin packing)
        docs_with_tokens.sort(key=lambda x: x['estimated_tokens'], reverse=True)
        
        # Create batches using simple bin packing
        batches = []
        current_batch = []
        current_batch_tokens = base_overhead
        # CONTEXT_WINDOW_MANAGEMENT: Use actual context window limits, not TPM!
        max_tokens_per_batch = self.get_context_window_limit(model)
        print(f"🎯 Batch sizing: {max_tokens_per_batch:,} tokens per batch (context window limit)")
        
        for doc in docs_with_tokens:
            doc_total_tokens = doc['estimated_tokens'] + self.DOCUMENT_OVERHEAD_TOKENS
            
            # Check if adding this document would exceed limits
            if (current_batch_tokens + doc_total_tokens > max_tokens_per_batch and 
                len(current_batch) > 0):
                
                # Finalize current batch
                batches.append({
                    'batch_id': len(batches) + 1,
                    'documents': current_batch,
                    'estimated_tokens': current_batch_tokens,
                    'document_count': len(current_batch)
                })
                
                # Start new batch
                current_batch = [doc]
                current_batch_tokens = base_overhead + doc_total_tokens
            else:
                # Add to current batch
                current_batch.append(doc)
                current_batch_tokens += doc_total_tokens
        
        # Don't forget the last batch
        if current_batch:
            batches.append({
                'batch_id': len(batches) + 1,
                'documents': current_batch,
                'estimated_tokens': current_batch_tokens,
                'document_count': len(current_batch)
            })
        
        # Calculate execution timing
        total_requests = len(batches)
        minutes_needed = max(1, (total_requests / limits['rpm']))  # At least 1 minute
        estimated_duration_minutes = int(minutes_needed) + 1  # Add buffer
        
        # Create execution plan
        execution_plan = {
            'total_batches': len(batches),
            'total_requests': total_requests,
            'estimated_duration_minutes': estimated_duration_minutes,
            'rate_limits': limits,
            'batching_strategy': {
                'max_tokens_per_batch': max_tokens_per_batch,
                'base_overhead_tokens': base_overhead,
                'framework_tokens': framework_tokens
            },
            'timing_windows': self._calculate_timing_windows(batches, limits)
        }
        
        result = {
            'batches': batches,
            'execution_plan': execution_plan,
            'model': model,
            'created_at': start_time,
            'planner_version': '1.0'
        }
        
        self.audit.log_agent_event("BatchPlannerAgent", "batch_planning_complete", {
            'total_batches': len(batches),
            'total_documents': len(corpus_documents),
            'estimated_duration_minutes': estimated_duration_minutes,
            'max_batch_tokens': max(b['estimated_tokens'] for b in batches),
            'min_batch_tokens': min(b['estimated_tokens'] for b in batches),
            'avg_documents_per_batch': sum(b['document_count'] for b in batches) / len(batches)
        })
        
        print(f"📊 Batch plan created: {len(batches)} batches, ~{estimated_duration_minutes} minutes")
        
        return result
    
    def _calculate_timing_windows(self, batches: List[Dict], limits: Dict[str, int]) -> List[Dict]:
        """Calculate when each batch should be executed to respect rate limits."""
        windows = []
        requests_per_minute = limits['rpm']
        
        for i, batch in enumerate(batches):
            minute_window = i // requests_per_minute
            position_in_window = i % requests_per_minute
            
            # Calculate delay within the minute (spread requests evenly)
            delay_seconds = (position_in_window * 60) // requests_per_minute
            
            windows.append({
                'batch_id': batch['batch_id'],
                'minute_window': minute_window,
                'delay_seconds': delay_seconds,
                'estimated_start': f"T+{minute_window}m {delay_seconds}s"
            })
        
        return windows
    
    def _get_timestamp(self) -> str:
        """Get current timestamp in ISO format."""
        return datetime.now(timezone.utc).isoformat() 