#!/usr/bin/env python3
"""
TPM-Aware Rate Limiter for Discernus Experiment Orchestrator
Simple patch to prevent rate limiting issues without LiteLLM dependency
"""

import time
import tiktoken
from typing import Dict, List, Tuple, Optional
from collections import defaultdict, deque

class TPMRateLimiter:
    """
    Token-Per-Minute aware rate limiter for LLM API calls
    Tracks token usage and enforces delays to prevent TPM overruns
    """
    
    def __init__(self):
        # TPM limits for different models
        self.tpm_limits = {
            'gpt-4o': 30000,
            'gpt-4': 10000,
            'gpt-4-turbo': 450000,
            'gpt-3.5-turbo': 200000,
            'claude-3-5-sonnet': 40000,
            'claude-3-5-sonnet-20241022': 40000,
            'claude-3-5-haiku': 50000,
            'claude-3-5-haiku-20241022': 50000,
            'mistral-large-latest': 30000,
            'mistral-small-latest': 60000,
            'gemini-1.5-pro': 32000,
            'gemini-1.5-flash': 100000
        }
        
        # Track token usage per model over time
        self.token_usage: Dict[str, deque] = defaultdict(lambda: deque())
        self.window_seconds = 60  # 1 minute window
        
        # Safety margin (use 80% of limit to be conservative)
        self.safety_margin = 0.8
        
    def estimate_tokens(self, text: str, model: str = "gpt-4") -> int:
        """
        Estimate token count for text using tiktoken
        Falls back to word-based estimation if tiktoken fails
        """
        try:
            # Try to get encoding for the model
            if model.startswith('gpt'):
                encoding_name = model.replace('gpt-', 'gpt').replace('-turbo', '')
                if encoding_name not in ['gpt-3.5', 'gpt-4']:
                    encoding_name = 'gpt-4'  # Default to gpt-4 encoding
                encoding = tiktoken.encoding_for_model(encoding_name + '-turbo' if encoding_name != 'gpt-4' else encoding_name)
            else:
                # For non-OpenAI models, use gpt-4 encoding as approximation
                encoding = tiktoken.encoding_for_model("gpt-4")
            
            return len(encoding.encode(text))
            
        except Exception:
            # Fallback: word-based estimation (approximately 1.3 tokens per word)
            return int(len(text.split()) * 1.3)
    
    def _clean_old_usage(self, model: str):
        """Remove token usage entries older than the window"""
        current_time = time.time()
        cutoff_time = current_time - self.window_seconds
        
        # Remove old entries
        while self.token_usage[model] and self.token_usage[model][0][0] < cutoff_time:
            self.token_usage[model].popleft()
    
    def _get_current_usage(self, model: str) -> int:
        """Get current token usage for model within the time window"""
        self._clean_old_usage(model)
        return sum(tokens for _, tokens in self.token_usage[model])
    
    def _get_model_tpm_limit(self, model: str) -> int:
        """Get TPM limit for model, with fallback for unknown models"""
        # Direct lookup
        if model in self.tpm_limits:
            return self.tpm_limits[model]
        
        # Pattern matching for model variants
        model_lower = model.lower()
        if 'gpt-4o' in model_lower:
            return 30000
        elif 'gpt-4' in model_lower:
            return 10000
        elif 'gpt-3.5' in model_lower:
            return 200000
        elif 'claude-3-5-sonnet' in model_lower or 'claude-3.5-sonnet' in model_lower:
            return 40000
        elif 'claude-3-5-haiku' in model_lower or 'claude-3.5-haiku' in model_lower:
            return 50000
        elif 'mistral-large' in model_lower:
            return 30000
        elif 'mistral-small' in model_lower:
            return 60000
        elif 'gemini-1.5-pro' in model_lower:
            return 32000
        elif 'gemini-1.5-flash' in model_lower:
            return 100000
        else:
            # Conservative default for unknown models
            return 10000
    
    def can_make_request(self, model: str, estimated_tokens: int) -> Tuple[bool, int]:
        """
        Check if request can be made without exceeding TPM limits
        Returns (can_proceed, wait_seconds)
        """
        tpm_limit = self._get_model_tpm_limit(model)
        safe_limit = int(tpm_limit * self.safety_margin)
        current_usage = self._get_current_usage(model)
        
        # Check if request would exceed limit
        if current_usage + estimated_tokens > safe_limit:
            # Calculate wait time needed
            # Need to wait until enough tokens "expire" from the window
            total_needed = current_usage + estimated_tokens - safe_limit
            
            # Find the oldest tokens that need to expire
            if not self.token_usage[model]:
                return True, 0  # No usage history, can proceed
            
            # Calculate how long to wait for enough tokens to expire
            current_time = time.time()
            tokens_to_expire = 0
            wait_time = 0
            
            for timestamp, tokens in self.token_usage[model]:
                tokens_to_expire += tokens
                if tokens_to_expire >= total_needed:
                    # This is how long we need to wait
                    wait_time = max(0, int((timestamp + self.window_seconds) - current_time))
                    break
            
            # Add buffer for safety
            wait_time += 5
            return False, wait_time
        
        return True, 0
    
    def record_usage(self, model: str, tokens_used: int):
        """Record token usage for a model"""
        current_time = time.time()
        self.token_usage[model].append((current_time, tokens_used))
        
        # Keep usage history reasonable size (max 100 entries per model)
        if len(self.token_usage[model]) > 100:
            self.token_usage[model].popleft()
    
    def wait_if_needed(self, model: str, estimated_tokens: int, prompt_text: str = "") -> bool:
        """
        Check TPM limits and wait if necessary before making API call
        Returns True if call should proceed, False if cancelled
        """
        can_proceed, wait_seconds = self.can_make_request(model, estimated_tokens)
        
        if not can_proceed:
            tpm_limit = self._get_model_tpm_limit(model)
            current_usage = self._get_current_usage(model)
            
            print(f"🚨 TPM Rate Limit Alert:")
            print(f"   Model: {model}")
            print(f"   TPM Limit: {tpm_limit:,} tokens/minute")  
            print(f"   Current Usage: {current_usage:,} tokens")
            print(f"   Request Tokens: {estimated_tokens:,} tokens")
            print(f"   Total Would Be: {current_usage + estimated_tokens:,} tokens")
            print(f"   ⏳ Waiting {wait_seconds} seconds before retry...")
            
            if len(prompt_text) > 100:
                print(f"   Text preview: {prompt_text[:100]}...")
            
            # Wait with progress indicator
            for remaining in range(wait_seconds, 0, -1):
                print(f"   ⏱️ {remaining} seconds remaining...", end='\r')
                time.sleep(1)
            print()  # New line after countdown
            
            # Recursive check after waiting
            return self.wait_if_needed(model, estimated_tokens, prompt_text)
        
        return True
    
    def get_stats(self) -> Dict[str, Dict]:
        """Get current usage statistics for all models"""
        stats = {}
        for model in self.token_usage:
            current_usage = self._get_current_usage(model)
            tpm_limit = self._get_model_tpm_limit(model)
            safe_limit = int(tpm_limit * self.safety_margin)
            
            stats[model] = {
                'current_usage': current_usage,
                'tpm_limit': tpm_limit,
                'safe_limit': safe_limit,
                'utilization_percent': (current_usage / tpm_limit) * 100,
                'remaining_capacity': safe_limit - current_usage,
                'request_count': len(self.token_usage[model])
            }
        
        return stats
    
    def print_stats(self):
        """Print current usage statistics"""
        stats = self.get_stats()
        if not stats:
            print("📊 No TPM usage recorded yet")
            return
        
        print("\n📊 TPM USAGE STATISTICS")
        print("=" * 50)
        for model, data in stats.items():
            print(f"Model: {model}")
            print(f"  Current Usage: {data['current_usage']:,} tokens")
            print(f"  TPM Limit: {data['tpm_limit']:,} tokens")
            print(f"  Utilization: {data['utilization_percent']:.1f}%")
            print(f"  Remaining: {data['remaining_capacity']:,} tokens")
            print(f"  Requests: {data['request_count']}")
            print()

# Utility functions for orchestrator integration
def estimate_framework_tokens(framework_path: str) -> int:
    """Estimate tokens for framework specification"""
    try:
        with open(framework_path, 'r', encoding='utf-8') as f:
            framework_text = f.read()
        return TPMRateLimiter().estimate_tokens(framework_text)
    except Exception:
        # Fallback estimate for MFT framework
        return 3000

def estimate_corpus_tokens(corpus_path: str) -> int:
    """Estimate tokens for corpus text"""
    try:
        with open(corpus_path, 'r', encoding='utf-8') as f:
            corpus_text = f.read()
        return TPMRateLimiter().estimate_tokens(corpus_text)
    except Exception:
        # Fallback based on file size
        try:
            import os
            file_size = os.path.getsize(corpus_path)
            return int(file_size / 4)  # Rough estimate: 4 bytes per token
        except Exception:
            return 5000  # Conservative fallback

if __name__ == "__main__":
    # Test the rate limiter
    limiter = TPMRateLimiter()
    
    print("🧪 Testing TPM Rate Limiter")
    print("=" * 30)
    
    # Test token estimation
    test_text = "This is a test of the token estimation system for narrative analysis."
    tokens = limiter.estimate_tokens(test_text)
    print(f"Test text tokens: {tokens}")
    
    # Test rate limiting logic
    model = "gpt-4o"
    large_request = 25000  # Near the limit
    
    can_proceed, wait_time = limiter.can_make_request(model, large_request)
    print(f"Can make {large_request} token request to {model}: {can_proceed}")
    if not can_proceed:
        print(f"Need to wait {wait_time} seconds")
    
    # Test usage recording
    limiter.record_usage(model, large_request)
    limiter.print_stats()
    
    # Test second request (should trigger rate limiting)
    can_proceed2, wait_time2 = limiter.can_make_request(model, large_request)
    print(f"Can make second {large_request} token request: {can_proceed2}")
    if not can_proceed2:
        print(f"Need to wait {wait_time2} seconds")
    
    print("\n✅ TPM Rate Limiter test complete") 