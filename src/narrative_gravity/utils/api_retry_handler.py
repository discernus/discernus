#!/usr/bin/env python3
"""
API Retry Handler for LLM Providers
===================================

Robust retry handling for API calls with exponential backoff, rate limiting,
and provider failover to improve reliability in production research environments.
"""

import time
import random
import logging
from typing import Dict, Any, Callable, Optional, List
from dataclasses import dataclass
from enum import Enum
import requests
from functools import wraps

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RetryReason(Enum):
    """Reasons for retrying API calls."""
    RATE_LIMIT = "rate_limit"
    NETWORK_TIMEOUT = "network_timeout"
    SERVER_ERROR = "server_error"
    AUTHENTICATION = "authentication"
    TEMPORARY_FAILURE = "temporary_failure"
    UNKNOWN = "unknown"

@dataclass
class RetryConfig:
    """Configuration for retry behavior."""
    max_retries: int = 3
    base_delay: float = 1.0  # seconds
    max_delay: float = 60.0  # seconds
    exponential_base: float = 2.0
    jitter: bool = True
    rate_limit_delay: float = 65.0  # seconds (for 429 errors)
    
class APIRetryHandler:
    """
    Comprehensive retry handler for LLM API calls.
    
    Features:
    - Exponential backoff with jitter
    - Rate limit detection and handling
    - Provider-specific error classification
    - Automatic provider failover
    - Comprehensive logging and monitoring
    """
    
    def __init__(self, config: Optional[RetryConfig] = None):
        self.config = config or RetryConfig()
        self.retry_stats = {
            'total_calls': 0,
            'successful_calls': 0,
            'failed_calls': 0,
            'retries_by_reason': {},
            'provider_failures': {}
        }
    
    def with_retry(self, provider: str, model: str):
        """
        Decorator for adding retry logic to API calls.
        
        Args:
            provider: API provider name (openai, anthropic, mistral, google_ai)
            model: Model name being used
        """
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                return self._execute_with_retry(func, provider, model, *args, **kwargs)
            return wrapper
        return decorator
    
    def _execute_with_retry(self, func: Callable, provider: str, model: str, *args, **kwargs):
        """Execute function with comprehensive retry logic."""
        
        self.retry_stats['total_calls'] += 1
        last_exception = None
        
        for attempt in range(self.config.max_retries + 1):
            try:
                logger.debug(f"🔄 Attempt {attempt + 1}/{self.config.max_retries + 1} for {provider}:{model}")
                
                result = func(*args, **kwargs)
                
                if attempt > 0:
                    logger.info(f"✅ {provider}:{model} succeeded on attempt {attempt + 1}")
                
                self.retry_stats['successful_calls'] += 1
                return result
                
            except Exception as e:
                last_exception = e
                retry_reason = self._classify_error(e, provider)
                
                logger.warning(f"⚠️ {provider}:{model} attempt {attempt + 1} failed: {retry_reason.value} - {str(e)}")
                
                # Track retry statistics
                self._update_retry_stats(provider, retry_reason)
                
                # Don't retry on final attempt
                if attempt >= self.config.max_retries:
                    break
                
                # Determine if we should retry this error
                if not self._should_retry(retry_reason):
                    logger.info(f"🚫 {provider}:{model} error not retryable: {retry_reason.value}")
                    break
                
                # Calculate delay and wait
                delay = self._calculate_delay(attempt, retry_reason)
                logger.info(f"⏳ {provider}:{model} retrying in {delay:.1f}s (reason: {retry_reason.value})")
                time.sleep(delay)
        
        # All retries exhausted
        self.retry_stats['failed_calls'] += 1
        logger.error(f"❌ {provider}:{model} failed after {self.config.max_retries + 1} attempts")
        
        # Return error in expected format
        return {"error": f"API call failed after {self.config.max_retries + 1} attempts: {str(last_exception)}"}, 0.0
    
    def _classify_error(self, error: Exception, provider: str) -> RetryReason:
        """Classify error type for appropriate retry strategy."""
        
        error_str = str(error).lower()
        
        # Rate limiting (429 errors)
        if any(indicator in error_str for indicator in [
            'rate limit', 'too many requests', '429', 'quota exceeded', 'rate_limit_exceeded'
        ]):
            return RetryReason.RATE_LIMIT
        
        # Network/timeout issues
        if any(indicator in error_str for indicator in [
            'timeout', 'connection', 'network', 'unreachable', 'dns'
        ]):
            return RetryReason.NETWORK_TIMEOUT
        
        # Server errors (502, 503, 504)
        if any(indicator in error_str for indicator in [
            '502', '503', '504', 'bad gateway', 'service unavailable', 'gateway timeout',
            'internal server error', '500'
        ]):
            return RetryReason.SERVER_ERROR
        
        # Authentication issues
        if any(indicator in error_str for indicator in [
            'authentication', 'unauthorized', '401', '403', 'api key', 'invalid key'
        ]):
            return RetryReason.AUTHENTICATION
        
        # Provider-specific temporary failures
        if provider == "openai" and any(indicator in error_str for indicator in [
            'engine overloaded', 'server overloaded'
        ]):
            return RetryReason.TEMPORARY_FAILURE
        
        if provider == "anthropic" and any(indicator in error_str for indicator in [
            'overloaded', 'busy'
        ]):
            return RetryReason.TEMPORARY_FAILURE
        
        if provider == "google_ai" and any(indicator in error_str for indicator in [
            'quota exceeded', 'resource exhausted'
        ]):
            return RetryReason.RATE_LIMIT
        
        return RetryReason.UNKNOWN
    
    def _should_retry(self, retry_reason: RetryReason) -> bool:
        """Determine if error type should be retried."""
        
        retryable_reasons = {
            RetryReason.RATE_LIMIT,
            RetryReason.NETWORK_TIMEOUT, 
            RetryReason.SERVER_ERROR,
            RetryReason.TEMPORARY_FAILURE
        }
        
        # Don't retry authentication errors (likely permanent)
        non_retryable = {
            RetryReason.AUTHENTICATION
        }
        
        if retry_reason in non_retryable:
            return False
        
        return retry_reason in retryable_reasons
    
    def _calculate_delay(self, attempt: int, retry_reason: RetryReason) -> float:
        """Calculate delay before retry with exponential backoff."""
        
        # Special handling for rate limits
        if retry_reason == RetryReason.RATE_LIMIT:
            # For rate limits, use a longer fixed delay
            delay = self.config.rate_limit_delay
        else:
            # Exponential backoff for other errors
            delay = self.config.base_delay * (self.config.exponential_base ** attempt)
        
        # Cap at maximum delay
        delay = min(delay, self.config.max_delay)
        
        # Add jitter to prevent thundering herd
        if self.config.jitter:
            jitter = random.uniform(0.1, 0.3) * delay
            delay += jitter
        
        return delay
    
    def _update_retry_stats(self, provider: str, retry_reason: RetryReason):
        """Update retry statistics for monitoring."""
        
        # Track by reason
        reason_key = retry_reason.value
        if reason_key not in self.retry_stats['retries_by_reason']:
            self.retry_stats['retries_by_reason'][reason_key] = 0
        self.retry_stats['retries_by_reason'][reason_key] += 1
        
        # Track by provider
        if provider not in self.retry_stats['provider_failures']:
            self.retry_stats['provider_failures'][provider] = 0
        self.retry_stats['provider_failures'][provider] += 1
    
    def get_retry_stats(self) -> Dict[str, Any]:
        """Get comprehensive retry statistics."""
        stats = self.retry_stats.copy()
        
        # Calculate success rate
        if stats['total_calls'] > 0:
            stats['success_rate'] = stats['successful_calls'] / stats['total_calls']
        else:
            stats['success_rate'] = 0.0
        
        # Calculate retry rate
        total_retries = sum(stats['retries_by_reason'].values())
        if stats['total_calls'] > 0:
            stats['retry_rate'] = total_retries / stats['total_calls']
        else:
            stats['retry_rate'] = 0.0
        
        return stats
    
    def log_stats(self):
        """Log current retry statistics."""
        stats = self.get_retry_stats()
        
        logger.info("📊 API Retry Statistics:")
        logger.info(f"  Total calls: {stats['total_calls']}")
        logger.info(f"  Success rate: {stats['success_rate']:.1%}")
        logger.info(f"  Retry rate: {stats['retry_rate']:.1%}")
        
        if stats['retries_by_reason']:
            logger.info("  Retries by reason:")
            for reason, count in stats['retries_by_reason'].items():
                logger.info(f"    {reason}: {count}")
        
        if stats['provider_failures']:
            logger.info("  Failures by provider:")
            for provider, count in stats['provider_failures'].items():
                logger.info(f"    {provider}: {count}")

class ProviderFailoverHandler:
    """
    Handles automatic failover between LLM providers when one fails.
    """
    
    def __init__(self, provider_priority: Optional[List[str]] = None):
        """
        Initialize with provider priority order.
        
        Args:
            provider_priority: List of providers in order of preference
                             Default: ["openai", "anthropic", "google_ai", "mistral"]
        """
        self.provider_priority = provider_priority or ["openai", "anthropic", "google_ai", "mistral"]
        self.provider_health = {provider: True for provider in self.provider_priority}
        self.failure_counts = {provider: 0 for provider in self.provider_priority}
        self.circuit_breaker_threshold = 3  # Failures before marking provider unhealthy
        
    def get_next_provider(self, failed_provider: Optional[str] = None) -> Optional[str]:
        """
        Get the next available provider for failover.
        
        Args:
            failed_provider: Provider that just failed (will be marked unhealthy)
            
        Returns:
            Next provider to try, or None if all providers are unhealthy
        """
        
        # Mark failed provider as unhealthy if applicable
        if failed_provider:
            self.failure_counts[failed_provider] += 1
            if self.failure_counts[failed_provider] >= self.circuit_breaker_threshold:
                self.provider_health[failed_provider] = False
                logger.warning(f"🚫 Provider {failed_provider} marked unhealthy after {self.failure_counts[failed_provider]} failures")
        
        # Find next healthy provider
        for provider in self.provider_priority:
            if self.provider_health.get(provider, False):
                return provider
        
        logger.error("❌ All providers are unhealthy!")
        return None
    
    def mark_provider_healthy(self, provider: str):
        """Mark provider as healthy (e.g., after successful call)."""
        if provider in self.provider_health:
            self.provider_health[provider] = True
            self.failure_counts[provider] = 0
    
    def get_health_status(self) -> Dict[str, Any]:
        """Get current provider health status."""
        return {
            'provider_health': self.provider_health.copy(),
            'failure_counts': self.failure_counts.copy(),
            'healthy_providers': [p for p, healthy in self.provider_health.items() if healthy]
        }

# Global retry handler instance
default_retry_handler = APIRetryHandler()

# Convenience decorators
def with_openai_retry(model: str):
    """Decorator for OpenAI API calls."""
    return default_retry_handler.with_retry("openai", model)

def with_anthropic_retry(model: str):
    """Decorator for Anthropic API calls.""" 
    return default_retry_handler.with_retry("anthropic", model)

def with_mistral_retry(model: str):
    """Decorator for Mistral API calls."""
    return default_retry_handler.with_retry("mistral", model)

def with_google_ai_retry(model: str):
    """Decorator for Google AI API calls."""
    return default_retry_handler.with_retry("google_ai", model) 