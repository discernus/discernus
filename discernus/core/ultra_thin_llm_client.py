#!/usr/bin/env python3
"""
Ultra-Thin LLM Client
====================

Pure message routing infrastructure. No intelligence, no complex features.
Just: prompt + model → API call → response
"""

import os
from dotenv import load_dotenv

load_dotenv()

class UltraThinLLMClient:
    """Pure infrastructure LLM client - just routes messages"""
    
    def __init__(self):
        self.anthropic_key = os.getenv('ANTHROPIC_API_KEY')
        self.openai_key = os.getenv('OPENAI_API_KEY')
    
    def call_llm(self, prompt: str, model_role: str = "claude-3-5-sonnet") -> str:
        """
        Pure message routing: prompt → API → response
        
        Args:
            prompt: The prompt to send
            model_role: Model identifier (for routing)
            
        Returns:
            Response string
        """
        
        # Try real API first, fall back to mock
        if self.anthropic_key:
            return self._call_anthropic(prompt)
        elif self.openai_key:
            return self._call_openai(prompt)
        else:
            return self._mock_response(prompt, model_role)
    
    def _call_anthropic(self, prompt: str) -> str:
        """Call Anthropic API directly"""
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
            print(f"Real Anthropic API failed ({e}), using mock")
            return self._mock_response(prompt, "anthropic")
    
    def _call_openai(self, prompt: str) -> str:
        """Call OpenAI API directly"""
        try:
            import openai
            
            client = openai.OpenAI(api_key=self.openai_key)
            response = client.chat.completions.create(
                model="gpt-4",
                max_tokens=2000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Real OpenAI API failed ({e}), using mock")
            return self._mock_response(prompt, "openai")
    
    def _mock_response(self, prompt: str, model_role: str) -> str:
        """Simple mock responses for testing infrastructure"""
        
        # Import our existing mock logic
        from discernus.core.simple_llm_client import SimpleLLMClient
        mock_client = SimpleLLMClient()
        return mock_client._mock_response(prompt, model_role) 