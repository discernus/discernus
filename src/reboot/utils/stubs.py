# src/reboot/utils/stubs.py
# This file contains placeholder classes to satisfy legacy dependencies
# in the rebooted LiteLLM client, ensuring full isolation from the old codebase.

class CostManager:
    """A stub for the legacy CostManager."""
    def estimate_cost(self, *args, **kwargs):
        return 0.0, 0.0, 0.0
    def check_limits_before_request(self, *args, **kwargs):
        return True, "Cost limits not enforced in reboot MVP."

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