#!/usr/bin/env python3

"""
Batch Planner Agent for Discernus THIN v2.0 - PRODUCTION VERSION
================================================================

REMOVAL TRIGGER: This component exists to manage context window limits in LLMs.
If/when LLM context windows become effectively unlimited, this entire file 
can be safely deleted and its integration points removed.

REMOVAL SEARCH TERMS: 
- "BatchPlannerAgent" 
- "batch_planner_agent"
- "context window management"
- "token footprint batching"

CURRENT PURPOSE:
Production-ready agent that creates optimal batches based on:
- Context window limits (1M Flash, 2M Pro)
- LiteLLM token counting integration  
- Cost transparency and reporting
- Intelligent pacing to prevent rate limiting

PRODUCTION ENHANCEMENTS:
- Real-time cost calculation using LiteLLM
- Batch progress reporting for CLI
- Adaptive pacing based on model and batch size
- Token counting validation before submission
"""

import json
import time
from datetime import datetime, timezone
from typing import Dict, List, Any, Tuple
from pathlib import Path

# Production imports for enhanced functionality
try:
    import litellm
    from litellm import completion, get_model_info
    from litellm.utils import token_counter
    LITELLM_AVAILABLE = True
except ImportError:
    LITELLM_AVAILABLE = False
    print("⚠️  LiteLLM not available - cost transparency features disabled")


class BatchPlannerAgent:
    """
    PRODUCTION BatchPlannerAgent with full cost transparency and intelligent pacing.
    
    This agent manages context window constraints while providing:
    - Real-time cost estimation and tracking
    - Batch progress reporting for professional UX
    - LiteLLM integration for accurate token counting
    - Adaptive pacing to prevent rate limiting
    """
    
    def __init__(self, security_boundary, audit_logger):
        self.security = security_boundary
        self.audit = audit_logger
        print(f"📊 Batch planner initialized for experiment: {security_boundary.experiment_name}")
        print("🔧 CONTEXT_WINDOW_MANAGEMENT: Using context window limits (not TPM) for batch sizing")
        print("💰 PRODUCTION: Cost transparency and pacing enabled")

    def get_context_window_limit(self, model: str) -> int:
        """
        Get context window limits for the specified model with safety margins.
        
        CONTEXT_WINDOW_MANAGEMENT: This method defines the core constraint we're managing.
        When context windows become unlimited, this entire logic becomes obsolete.
        """
        if "vertex_ai" in model:
            if "gemini-2.5-pro" in model:
                return 1_800_000  # 90% of 2M tokens (safety margin)
            elif "gemini-2.5-flash" in model:
                return 900_000    # 90% of 1M tokens (safety margin)
        
        # Conservative default for unknown models
        return 800_000

    def get_rate_limits(self, model: str) -> Dict[str, int]:
        """
        Get rate limits for the specified model.
        Note: With Vertex AI DSQ, these are dynamic, but provide baseline estimates.
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
        
        # Default conservative limits for unknown models
        return {"rpm": 2, "tpm": 100000, "rpd": 50}

    def estimate_tokens(self, text: str, model: str = "gpt-3.5-turbo") -> int:
        """
        Estimate token count using LiteLLM's token counter when available.
        Falls back to character-based estimation for reliability.
        """
        if LITELLM_AVAILABLE:
            try:
                # Use LiteLLM's accurate token counting
                return token_counter(model=model, text=text)
            except Exception as e:
                print(f"⚠️  LiteLLM token counting failed: {e}")
        
        # Fallback: rough estimation (1 token ≈ 4 characters for English)
        return len(text) // 4

    def estimate_batch_cost(self, batch_tokens: int, model: str) -> float:
        """
        Estimate cost for a batch using LiteLLM's pricing information.
        """
        if not LITELLM_AVAILABLE:
            return 0.0
        
        try:
            # Get model pricing from LiteLLM
            model_info = get_model_info(model)
            if model_info and "input_cost_per_token" in model_info:
                cost_per_token = model_info["input_cost_per_token"]
                return batch_tokens * cost_per_token
            else:
                # Fallback estimates for Vertex AI Gemini models
                if "gemini-2.5-flash" in model:
                    return batch_tokens * 0.000000075  # $0.075 per 1M tokens
                elif "gemini-2.5-pro" in model:
                    return batch_tokens * 0.000001250  # $1.25 per 1M tokens
        except Exception as e:
            print(f"⚠️  Cost estimation failed: {e}")
        
        return 0.0

    def calculate_batch_tokens(self, framework_content: str, documents: List[Dict], model: str) -> Dict[str, int]:
        """
        Calculate accurate token footprints using LiteLLM integration.
        """
        # Framework overhead (static per batch)
        framework_tokens = self.estimate_tokens(framework_content, model)
        
        # Prompt overhead estimation (conservative)
        prompt_overhead = 500  # Typical system/instruction prompts
        
        # Document tokens
        document_tokens = {}
        total_doc_tokens = 0
        
        for doc in documents:
            doc_tokens = self.estimate_tokens(doc['content'], model)
            document_tokens[doc['filename']] = doc_tokens
            total_doc_tokens += doc_tokens
        
        return {
            'framework_tokens': framework_tokens,
            'prompt_overhead': prompt_overhead,
            'document_tokens': document_tokens,
            'total_document_tokens': total_doc_tokens,
            'base_overhead': framework_tokens + prompt_overhead
        }

    def create_batches(self, framework_content: str, corpus_documents: List[Dict], model: str) -> Dict[str, Any]:
        """
        Create intelligent batches with full production monitoring and cost transparency.
        """
        start_time = datetime.now(timezone.utc).isoformat()
        
        # Get rate limits for this model
        limits = self.get_rate_limits(model)
        
        self.audit.log_agent_event("BatchPlannerAgent", "batch_planning_start", {
            "model": model,
            "total_documents": len(corpus_documents),
            "framework_size_chars": len(framework_content)
        })
        
        # Calculate precise token footprints
        print("🔍 Calculating token footprints with LiteLLM integration...")
        token_analysis = self.calculate_batch_tokens(framework_content, corpus_documents, model)
        base_overhead = token_analysis['base_overhead']
        
        print(f"📐 Framework tokens: {token_analysis['framework_tokens']:,}")
        print(f"📐 Prompt overhead: {token_analysis['prompt_overhead']:,}")
        print(f"📐 Total document tokens: {token_analysis['total_document_tokens']:,}")
        
        # Create batches using simple bin packing
        batches = []
        current_batch = []
        current_batch_tokens = base_overhead
        # CONTEXT_WINDOW_MANAGEMENT: Use actual context window limits, not TPM!
        max_tokens_per_batch = self.get_context_window_limit(model)
        print(f"🎯 Batch sizing: {max_tokens_per_batch:,} tokens per batch (context window limit)")
        
        total_estimated_cost = 0.0
        
        for doc in corpus_documents:
            doc_tokens = token_analysis['document_tokens'][doc['filename']]
            
            # Check if adding this document would exceed the batch limit
            if current_batch_tokens + doc_tokens > max_tokens_per_batch and current_batch:
                # Finalize current batch with cost calculation
                batch_cost = self.estimate_batch_cost(current_batch_tokens, model)
                total_estimated_cost += batch_cost
                
                batch_info = {
                    'batch_id': len(batches) + 1,
                    'documents': current_batch.copy(),
                    'token_count': current_batch_tokens,
                    'estimated_cost': batch_cost,
                    'document_count': len(current_batch)
                }
                batches.append(batch_info)
                
                print(f"📦 Batch {len(batches)}: {len(current_batch)} docs, {current_batch_tokens:,} tokens, ${batch_cost:.4f}")
                
                # Start new batch
                current_batch = [doc]
                current_batch_tokens = base_overhead + doc_tokens
            else:
                # Add document to current batch
                current_batch.append(doc)
                current_batch_tokens += doc_tokens
        
        # Add final batch if not empty
        if current_batch:
            batch_cost = self.estimate_batch_cost(current_batch_tokens, model)
            total_estimated_cost += batch_cost
            
            batch_info = {
                'batch_id': len(batches) + 1,
                'documents': current_batch,
                'token_count': current_batch_tokens,
                'estimated_cost': batch_cost,
                'document_count': len(current_batch)
            }
            batches.append(batch_info)
            print(f"📦 Batch {len(batches)}: {len(current_batch)} docs, {current_batch_tokens:,} tokens, ${batch_cost:.4f}")

        # Calculate intelligent pacing delays
        rpm_limit = limits['rpm']
        delay_between_batches = max(60 / rpm_limit, 5)  # At least 5 seconds between batches
        
        # Production summary with cost transparency
        print(f"\n💰 COST SUMMARY:")
        print(f"   Total estimated cost: ${total_estimated_cost:.4f}")
        print(f"   Average cost per batch: ${total_estimated_cost/len(batches):.4f}")
        print(f"   Cost per document: ${total_estimated_cost/len(corpus_documents):.4f}")
        
        print(f"\n⏱️  PACING STRATEGY:")
        print(f"   Batches: {len(batches)}")
        print(f"   Delay between batches: {delay_between_batches:.1f} seconds")
        print(f"   Total estimated time: {(len(batches) * delay_between_batches)/60:.1f} minutes")
        
        plan = {
            'batches': batches,
            'total_batches': len(batches),
            'total_documents': len(corpus_documents),
            'total_estimated_tokens': sum(b['token_count'] for b in batches),
            'total_estimated_cost': total_estimated_cost,
            'average_batch_size': len(corpus_documents) / len(batches),
            'delay_between_batches': delay_between_batches,
            'model': model,
            'context_window_limit': max_tokens_per_batch,
            'rate_limits': limits,
            'created_at': start_time,
            'token_analysis': token_analysis
        }
        
        self.audit.log_agent_event("BatchPlannerAgent", "batch_planning_complete", {
            "total_batches": len(batches),
            "total_estimated_cost": total_estimated_cost,
            "total_estimated_tokens": plan['total_estimated_tokens'],
            "average_batch_size": plan['average_batch_size']
        })
        
        return plan

    def execute_batch_with_pacing(self, batch_info: Dict, analysis_agent, framework_content: str, delay_seconds: float = 0) -> Dict[str, Any]:
        """
        Execute a single batch with intelligent pacing and status reporting.
        """
        batch_id = batch_info['batch_id']
        documents = batch_info['documents']
        estimated_cost = batch_info.get('estimated_cost', 0.0)
        
        print(f"\n🚀 Starting Batch {batch_id}/{batch_info.get('total_batches', '?')}:")
        print(f"   📄 Documents: {len(documents)}")
        print(f"   🎯 Tokens: {batch_info['token_count']:,}")
        print(f"   💰 Est. Cost: ${estimated_cost:.4f}")
        
        # Pre-batch pacing delay
        if delay_seconds > 0:
            print(f"   ⏸️  Pacing delay: {delay_seconds:.1f}s (rate limit management)")
            time.sleep(delay_seconds)
        
        start_time = datetime.now(timezone.utc)
        
        try:
            # Execute batch with the analysis agent using proper interface
            results = analysis_agent.analyze_batch(
                framework_content=framework_content,
                corpus_documents=documents,
                experiment_config={},  # Basic config for batch processing
                model="vertex_ai/gemini-2.5-flash"  # Use configured model
            )
            
            end_time = datetime.now(timezone.utc)
            duration = (end_time - start_time).total_seconds()
            
            print(f"   ✅ Batch {batch_id} completed in {duration:.1f}s")
            
            return {
                'batch_id': batch_id,
                'results': results,
                'execution_time': duration,
                'actual_cost': estimated_cost,  # Could be updated with actual cost from LiteLLM
                'success': True,
                'timestamp': end_time.isoformat()
            }
            
        except Exception as e:
            end_time = datetime.now(timezone.utc)
            duration = (end_time - start_time).total_seconds()
            
            print(f"   ❌ Batch {batch_id} failed after {duration:.1f}s: {str(e)}")
            
            return {
                'batch_id': batch_id,
                'error': str(e),
                'execution_time': duration,
                'success': False,
                'timestamp': end_time.isoformat()
            } 