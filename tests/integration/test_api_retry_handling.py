#!/usr/bin/env python3
"""
Integration Tests for API Retry Handling
=========================================

Tests the comprehensive retry handling system to ensure robust API reliability
in production research environments.
"""

import pytest
import time
import sys
sys.path.append('.')
sys.path.append('./src')

from src.utils.api_retry_handler import (
    APIRetryHandler, 
    ProviderFailoverHandler, 
    RetryConfig, 
    RetryReason
)
from src.api_clients.direct_api_client import DirectAPIClient

class TestAPIRetryHandler:
    """Test suite for API retry handling functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.retry_config = RetryConfig(
            max_retries=2,  # Faster tests
            base_delay=0.1,  # Quick delays for testing
            max_delay=1.0,
            rate_limit_delay=0.5
        )
        self.retry_handler = APIRetryHandler(self.retry_config)
    
    def test_retry_handler_initialization(self):
        """Test retry handler initializes correctly."""
        assert self.retry_handler.config.max_retries == 2
        assert self.retry_handler.config.base_delay == 0.1
        assert self.retry_handler.retry_stats['total_calls'] == 0
    
    def test_error_classification(self):
        """Test that errors are classified correctly."""
        
        # Rate limit errors
        rate_limit_error = Exception("Rate limit exceeded")
        assert self.retry_handler._classify_error(rate_limit_error, "openai") == RetryReason.RATE_LIMIT
        
        # Network timeout errors
        timeout_error = Exception("Connection timeout")
        assert self.retry_handler._classify_error(timeout_error, "openai") == RetryReason.NETWORK_TIMEOUT
        
        # Server errors
        server_error = Exception("502 Bad Gateway")
        assert self.retry_handler._classify_error(server_error, "openai") == RetryReason.SERVER_ERROR
        
        # Authentication errors
        auth_error = Exception("401 Unauthorized - Invalid API key")
        assert self.retry_handler._classify_error(auth_error, "openai") == RetryReason.AUTHENTICATION
    
    def test_retry_decision_logic(self):
        """Test retry decision logic for different error types."""
        
        # Should retry these
        assert self.retry_handler._should_retry(RetryReason.RATE_LIMIT) == True
        assert self.retry_handler._should_retry(RetryReason.NETWORK_TIMEOUT) == True
        assert self.retry_handler._should_retry(RetryReason.SERVER_ERROR) == True
        assert self.retry_handler._should_retry(RetryReason.TEMPORARY_FAILURE) == True
        
        # Should NOT retry these
        assert self.retry_handler._should_retry(RetryReason.AUTHENTICATION) == False
    
    def test_delay_calculation(self):
        """Test exponential backoff delay calculation."""
        
        # Regular exponential backoff
        delay1 = self.retry_handler._calculate_delay(0, RetryReason.NETWORK_TIMEOUT)
        delay2 = self.retry_handler._calculate_delay(1, RetryReason.NETWORK_TIMEOUT)
        assert delay2 > delay1  # Should increase
        
        # Rate limit special handling (with jitter, should be close to base delay)
        rate_delay = self.retry_handler._calculate_delay(0, RetryReason.RATE_LIMIT)
        assert 0.5 <= rate_delay <= 0.65  # Should use rate_limit_delay from config + jitter
    
    def test_successful_call_tracking(self):
        """Test that successful calls are tracked properly."""
        
        @self.retry_handler.with_retry("test_provider", "test_model")
        def successful_function():
            return {"result": "success"}, 0.0
        
        result = successful_function()
        
        assert result == ({"result": "success"}, 0.0)
        stats = self.retry_handler.get_retry_stats()
        assert stats['total_calls'] == 1
        assert stats['successful_calls'] == 1
        assert stats['success_rate'] == 1.0
    
    def test_retry_on_failure(self):
        """Test retry behavior on transient failures."""
        call_count = 0
        
        @self.retry_handler.with_retry("test_provider", "test_model")
        def failing_then_succeeding_function():
            nonlocal call_count
            call_count += 1
            if call_count <= 1:  # Fail on first call
                raise Exception("Rate limit exceeded")
            return {"result": "success"}, 0.0
        
        result = failing_then_succeeding_function()
        
        assert result == ({"result": "success"}, 0.0)
        assert call_count == 2  # Should have called twice
        stats = self.retry_handler.get_retry_stats()
        assert stats['total_calls'] == 1
        assert stats['successful_calls'] == 1

class TestProviderFailoverHandler:
    """Test suite for provider failover functionality."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.failover_handler = ProviderFailoverHandler(["provider1", "provider2", "provider3"])
    
    def test_initial_health_status(self):
        """Test that all providers start healthy."""
        status = self.failover_handler.get_health_status()
        assert len(status['healthy_providers']) == 3
        assert all(status['provider_health'].values())
    
    def test_provider_failure_tracking(self):
        """Test provider failure tracking and circuit breaker."""
        
        # Simulate failures
        next_provider = self.failover_handler.get_next_provider("provider1")
        assert next_provider == "provider1"  # First call, still healthy
        
        # Fail provider1 multiple times
        for _ in range(3):
            self.failover_handler.get_next_provider("provider1")
        
        # provider1 should now be unhealthy
        status = self.failover_handler.get_health_status()
        assert not status['provider_health']['provider1']
        assert len(status['healthy_providers']) == 2
    
    def test_provider_recovery(self):
        """Test provider recovery marking."""
        
        # Mark provider as unhealthy
        for _ in range(3):
            self.failover_handler.get_next_provider("provider1")
        
        # Mark as healthy
        self.failover_handler.mark_provider_healthy("provider1")
        
        status = self.failover_handler.get_health_status()
        assert status['provider_health']['provider1']
        assert status['failure_counts']['provider1'] == 0

class TestDirectAPIClientIntegration:
    """Test integration of retry handling with DirectAPIClient."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.client = DirectAPIClient()
    
    def test_retry_handler_integration(self):
        """Test that DirectAPIClient integrates retry handler."""
        
        # Should have retry handler available
        stats = self.client.get_retry_statistics()
        
        # These should be present regardless of whether retry handler imported successfully
        assert 'retry_handler_available' in stats
        assert 'failover_handler_available' in stats
        
        # If available, should have proper structure
        if stats['retry_handler_available']:
            assert 'total_calls' in stats
            assert 'success_rate' in stats
    
    def test_reliability_report(self):
        """Test reliability report generation."""
        
        # Should not raise an exception
        try:
            self.client.log_reliability_report()
            success = True
        except Exception:
            success = False
        
        assert success == True

if __name__ == "__main__":
    pytest.main([__file__, "-v"]) 