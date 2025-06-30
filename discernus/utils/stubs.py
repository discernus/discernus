# src/reboot/utils/stubs.py
# This file contains placeholder classes to satisfy legacy dependencies
# in the rebooted LiteLLM client, ensuring full isolation from the old codebase.


class CostManager:
    """Real cost manager with configurable limits and tracking."""
    
    def __init__(self, daily_limit=10.0, per_request_limit=1.0):
        self.daily_limit = daily_limit  # $10/day default
        self.per_request_limit = per_request_limit  # $1/request default
        self.daily_spent = 0.0
        self.session_spent = 0.0
        
        # Model pricing (per 1k tokens) - current as of late 2024
        self.pricing = {
            # OpenAI
            "gpt-4o": {"input": 0.0025, "output": 0.01},
            "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
            "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015},
            "gpt-4-turbo": {"input": 0.01, "output": 0.03},
            
            # Anthropic 
            "claude-3-5-sonnet-20241022": {"input": 0.003, "output": 0.015},
            "claude-3-5-haiku-20241022": {"input": 0.00025, "output": 0.00125},
            "claude-3-opus-20240229": {"input": 0.015, "output": 0.075},
            
            # Mistral
            "mistral-large-latest": {"input": 0.004, "output": 0.012},
            "mistral-small-latest": {"input": 0.001, "output": 0.003},
            
            # Google
            "gemini-1.5-flash": {"input": 0.000075, "output": 0.0003},
            "gemini-1.5-pro": {"input": 0.00125, "output": 0.005},
            
            # Local models (free)
            "ollama": {"input": 0.0, "output": 0.0}
        }

    def estimate_cost(self, text, provider, model_name):
        """Estimate cost for a request"""
        if provider == "ollama":
            return 0.0, 0.0, 0.0
            
        # Rough token estimation (4 chars = 1 token)
        input_tokens = len(text) / 4
        output_tokens = 500  # Conservative estimate for output
        
        # Get pricing for this model
        model_pricing = self._get_model_pricing(model_name)
        if not model_pricing:
            # Unknown model - use conservative estimate
            input_cost = input_tokens * 0.001 / 1000  # $0.001 per 1k tokens
            output_cost = output_tokens * 0.003 / 1000  # $0.003 per 1k tokens
        else:
            input_cost = input_tokens * model_pricing["input"] / 1000
            output_cost = output_tokens * model_pricing["output"] / 1000
            
        total_cost = input_cost + output_cost
        return total_cost, input_cost, output_cost

    def check_limits_before_request(self, estimated_cost):
        """Check if request would exceed cost limits"""
        # Check per-request limit
        if estimated_cost > self.per_request_limit:
            return False, f"Request cost ${estimated_cost:.4f} exceeds per-request limit ${self.per_request_limit:.2f}"
        
        # Check daily limit  
        if self.daily_spent + estimated_cost > self.daily_limit:
            remaining = self.daily_limit - self.daily_spent
            return False, f"Request would exceed daily limit (${remaining:.4f} remaining of ${self.daily_limit:.2f})"
            
        # Check session total (additional safety)
        if self.session_spent + estimated_cost > self.daily_limit * 2:  # 2x daily as session max
            return False, f"Request would exceed session limit (${self.session_spent:.4f} already spent)"
        
        return True, f"Cost approved: ${estimated_cost:.4f} (daily: ${self.daily_spent:.2f}/${self.daily_limit:.2f})"
    
    def record_actual_cost(self, actual_cost):
        """Record actual cost after request completion"""
        self.daily_spent += actual_cost
        self.session_spent += actual_cost
        
    def _get_model_pricing(self, model_name):
        """Get pricing for a specific model"""
        # Direct lookup first
        if model_name in self.pricing:
            return self.pricing[model_name]
            
        # Try partial matches for model families
        model_lower = model_name.lower()
        for pricing_key in self.pricing:
            if pricing_key.lower() in model_lower:
                return self.pricing[pricing_key]
                
        return None  # Unknown model


class TPMRateLimiter:
    """A stub for the legacy TPMRateLimiter."""

    def estimate_tokens(self, *args, **kwargs):
        return 0

    def wait_if_needed(self, *args, **kwargs):
        return True

    def record_usage(self, *args, **kwargs):
        pass


class APIRetryHandler:
    """A stub for the legacy APIRetryHandler."""

    def with_retry(self, *args, **kwargs):
        def decorator(func):
            return func

        return decorator


class ProviderFailoverHandler:
    """A stub for the legacy ProviderFailoverHandler."""

    def mark_provider_healthy(self, *args, **kwargs):
        pass
