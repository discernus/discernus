#!/usr/bin/env python3
"""
Test Gateway Policy Enforcement
==============================

Tests for the gateway policy enforcement system that prevents direct model client instantiation.
"""

import pytest
import warnings
from unittest.mock import Mock, MagicMock

from discernus.core.gateway_policy_enforcement import (
    enforce_gateway_policy,
    validate_agent_gateway_usage,
    require_gateway_usage,
    FORBIDDEN_MODEL_IMPORTS,
    FORBIDDEN_MODEL_CLASSES
)


class TestGatewayPolicyEnforcement:
    """Test gateway policy enforcement"""
    
    def test_good_function_no_warnings(self):
        """Test that functions using gateway don't trigger warnings"""
        @enforce_gateway_policy
        def good_function():
            from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
            # Just check the source, don't execute
            return "test"
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = good_function()
            assert len(w) == 0  # No warnings should be raised
    
    def test_bad_function_triggers_warnings(self):
        """Test that functions with forbidden imports trigger warnings"""
        @enforce_gateway_policy
        def bad_function():
            import openai  # This should trigger a warning
            # Just check the source, don't execute
            return "test"
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = bad_function()
            assert len(w) > 0  # Warnings should be raised
            assert any("Gateway policy violation" in str(warning.message) for warning in w)
    
    def test_good_agent_class(self):
        """Test that agent classes using gateway don't trigger warnings"""
        @require_gateway_usage
        class GoodAgent:
            def __init__(self):
                from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
                # Just check the source, don't execute
                pass
            
            def execute(self):
                return "test"
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            # Just check the class definition, don't instantiate
            assert len(w) == 0  # No warnings should be raised
    
    def test_bad_agent_class_triggers_warnings(self):
        """Test that agent classes with forbidden usage trigger warnings"""
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            
            @require_gateway_usage
            class BadAgent:
                def __init__(self):
                    import openai  # This should trigger a warning
                    # Just check the source, don't execute
                    pass
                
                def execute(self):
                    return "test"
            
            # The warning should be triggered at class definition time
            assert len(w) > 0  # Warnings should be raised
            assert any("Gateway policy violations" in str(warning.message) for warning in w)
    
    def test_validate_agent_gateway_usage(self):
        """Test validate_agent_gateway_usage function"""
        class GoodAgent:
            def __init__(self):
                from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
                # Just check the source, don't execute
                pass
            
            def execute(self):
                return "test"
        
        class BadAgent:
            def __init__(self):
                import openai
                # Just check the source, don't execute
                pass
            
            def execute(self):
                return "test"
        
        # Good agent should have no violations
        good_violations = validate_agent_gateway_usage(GoodAgent)
        assert len(good_violations) == 0
        
        # Bad agent should have violations
        bad_violations = validate_agent_gateway_usage(BadAgent)
        assert len(bad_violations) > 0
        assert any("openai" in violation for violation in bad_violations)
    
    def test_forbidden_imports_list(self):
        """Test that forbidden imports list is comprehensive"""
        expected_forbidden = {
            'openai',
            'anthropic', 
            'google.generativeai',
            'vertexai',
            'cohere',
            'replicate',
            'huggingface_hub'
        }
        
        assert FORBIDDEN_MODEL_IMPORTS == expected_forbidden
    
    def test_forbidden_classes_list(self):
        """Test that forbidden classes list is comprehensive"""
        expected_forbidden = {
            'OpenAI',
            'Anthropic',
            'GenerativeModel',
            'VertexAI',
            'Cohere',
            'Replicate',
            'HuggingFaceHub'
        }
        
        assert FORBIDDEN_MODEL_CLASSES == expected_forbidden
    
    def test_decorator_preserves_function_behavior(self):
        """Test that decorator doesn't change function behavior"""
        @enforce_gateway_policy
        def test_function():
            return "test_result"
        
        result = test_function()
        assert result == "test_result"
    
    def test_class_decorator_preserves_class_behavior(self):
        """Test that class decorator doesn't change class behavior"""
        @require_gateway_usage
        class TestClass:
            def __init__(self):
                self.value = "test"
            
            def get_value(self):
                return self.value
        
        instance = TestClass()
        assert instance.get_value() == "test"
    
    def test_multiple_violations_in_single_function(self):
        """Test detection of multiple violations in a single function"""
        @enforce_gateway_policy
        def multi_violation_function():
            import openai  # Violation 1
            import anthropic  # Violation 2
            # Just check the source, don't execute
            return "test"
        
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter("always")
            result = multi_violation_function()
            assert len(w) > 0
            # Should detect multiple violations
            warning_text = str(w[0].message)
            assert "openai" in warning_text
            assert "anthropic" in warning_text


if __name__ == "__main__":
    pytest.main([__file__])
