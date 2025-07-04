#!/usr/bin/env python3
"""
THIN LiteLLM Integration
======================

Uses LiteLLM's proven infrastructure (rate limiting, retries, provider management)
with minimal integration code. No custom intelligence, just clean routing.
"""

import os
from dotenv import load_dotenv

load_dotenv()

class ThinLiteLLMClient:
    """THIN integration with LiteLLM - use their infrastructure, keep our code minimal"""
    
    def __init__(self):
        try:
            import litellm
            self.litellm = litellm
            self._configure_litellm()
            self.available = True
        except ImportError:
            print("📦 LiteLLM not available - using direct API fallback")
            self.available = False
            self._setup_direct_fallback()
    
    def _configure_litellm(self):
        """Minimal LiteLLM configuration - let it handle the complexity"""
        # Let LiteLLM handle rate limiting, retries, and provider management
        self.litellm.drop_params = True  # Handle unsupported params gracefully
        self.litellm.set_verbose = False  # Clean logs
        print("✅ LiteLLM configured - handling rate limits, retries, provider management")
    
    def _setup_direct_fallback(self):
        """Fallback to direct API if LiteLLM unavailable"""
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        self.openai_key = os.getenv('OPENAI_API_KEY')
    
    def call_llm(self, prompt: str, model_role: str = "claude-3-5-sonnet") -> str:
        """
        THIN wrapper: prompt → LiteLLM → response
        Let LiteLLM handle all the infrastructure complexity
        """
        
        if self.available:
            return self._call_via_litellm(prompt, model_role)
        else:
            return self._call_direct_fallback(prompt, model_role)
    
    def _call_via_litellm(self, prompt: str, model_role: str) -> str:
        """Use LiteLLM for all the heavy lifting"""
        try:
            # Let LiteLLM handle everything: rate limits, retries, provider routing
            response = self.litellm.completion(
                model=self._map_role_to_model(model_role),
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7
                # LiteLLM handles all the provider-specific complexity
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"LiteLLM call failed ({e}), using mock")
            return self._mock_response(prompt, model_role)
    
    def _call_direct_fallback(self, prompt: str, model_role: str) -> str:
        """Direct API fallback when LiteLLM unavailable"""
        if self.anthropic_key:
            try:
                import anthropic
                client = anthropic.Anthropic(api_key=self.anthropic_key)
                response = client.messages.create(
                    model="claude-3-5-sonnet-20241022",
                    max_tokens=2000,
                    messages=[{"role": "user", "content": prompt}]
                )
                return response.content[0].text
            except Exception as e:
                print(f"Direct Anthropic failed ({e}), using mock")
                return self._mock_response(prompt, model_role)
        
        return self._mock_response(prompt, model_role)
    
    def _map_role_to_model(self, role: str) -> str:
        """Simple role to model mapping with provider-specific format for LiteLLM"""
        role_models = {
            'design': 'claude-3-5-sonnet-20241022',
            'moderator': 'claude-3-5-sonnet-20241022',
            'specialist': 'claude-3-5-sonnet-20241022', 
            'adversarial': 'claude-3-5-sonnet-20241022',
            'analysis': 'claude-3-5-sonnet-20241022',
            'referee': 'claude-3-5-sonnet-20241022'
        }
        return role_models.get(role, 'claude-3-5-sonnet-20241022')
    
    def _mock_response(self, prompt: str, model_role: str) -> str:
        """Fallback to mock responses"""
        # Simple mock responses based on role
        mock_responses = {
            'design': f"For analyzing unity vs division in inaugural addresses, I recommend this systematic methodology:\n\n**Step 1: Initial Reading**\n- Read both texts for overall themes\n- Identify key rhetorical patterns\n\n**Step 2: Theme Ranking**\n- Rank themes by frequency and prominence\n- Focus on unifying vs divisive language\n\n**Step 3: Targeted Analysis**\n- Examine specific passages for evidence\n- Quantify rhetorical devices\n\nDoes this methodology look right to you?",
            'moderator': f"Based on the methodology provided, I'll coordinate analysis of both inaugural addresses focusing on unity vs division themes. Let me start by examining the texts systematically...",
            'specialist': f"As requested, I'll analyze the specific rhetorical patterns in both texts. Looking at the evidence provided...",
            'adversarial': f"I need to challenge some assumptions in this analysis. Have we considered alternative interpretations?",
            'analysis': f"Synthesizing all perspectives, the key findings suggest...",
            'referee': f"Final assessment: The methodology appears sound and the evidence supports the conclusions drawn."
        }
        
        return mock_responses.get(model_role, "I understand the request and would analyze accordingly.") 