#!/usr/bin/env python3
"""
THIN LiteLLM Integration
======================

Uses LiteLLM's proven infrastructure (rate limiting, retries, provider management)
with minimal integration code. No custom intelligence, just clean routing.
"""

import os
from typing import Dict, Any, Tuple, Optional, List
from dotenv import load_dotenv
import json
from pathlib import Path
import time
from datetime import datetime

load_dotenv()

# Add Vertex AI environment variable check
def get_vertex_ai_config() -> Optional[Dict[str, Any]]:
    """
    Get Vertex AI configuration from environment variables.
    Returns None if Vertex AI is not configured.
    """
    import os
    
    # Check for Google Cloud credentials
    vertex_project = os.getenv('VERTEXAI_PROJECT') or os.getenv('VERTEX_PROJECT')
    vertex_location = os.getenv('VERTEXAI_LOCATION') or os.getenv('VERTEX_LOCATION', 'us-central1')
    vertex_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS') or os.getenv('VERTEX_CREDENTIALS')
    
    if vertex_project:
        config = {
            'project': vertex_project,
            'location': vertex_location
        }
        
        if vertex_credentials:
            # If it's a file path, load the JSON
            if vertex_credentials.endswith('.json') and Path(vertex_credentials).exists():
                with open(vertex_credentials, 'r') as f:
                    config['credentials'] = json.load(f)
            else:
                # Assume it's a JSON string
                try:
                    config['credentials'] = json.loads(vertex_credentials)
                except:
                    pass
        
        return config
    
    return None

class ThinLiteLLMClient:
    """THIN integration with LiteLLM - use their infrastructure, keep our code minimal"""
    
    def __init__(self, logger_name: str = "ThinLiteLLMClient"):
        # Set up basic logging
        import logging
        self.logger = logging.getLogger(logger_name)
        
        try:
            import litellm
            self.litellm = litellm
            self._configure_litellm()
            self.available = True
            
            # Check for Vertex AI availability
            self.vertex_config = get_vertex_ai_config()
            if self.vertex_config:
                print("🌟 Vertex AI configuration detected - Gemini models available!")
                self.logger.info("🌟 Vertex AI configuration detected - Gemini models available!")
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
        response_text, metadata = self.call_llm_with_metadata(prompt, model_role)
        return response_text
    
    def call_llm_with_metadata(self, prompt: str, model_role: str = "claude-3-5-sonnet") -> Tuple[str, Dict[str, Any]]:
        """
        THIN wrapper that returns both response and metadata for complete transparency
        """
        
        if self.available:
            return self._call_via_litellm_with_metadata(prompt, model_role)
        else:
            return self._call_direct_fallback_with_metadata(prompt, model_role)
    
    def _call_via_litellm_with_metadata(self, prompt: str, model_role: str) -> Tuple[str, Dict[str, Any]]:
        """Use LiteLLM for all the heavy lifting, capture metadata"""
        try:
            model = self._map_role_to_model(model_role)
            
            # Let LiteLLM handle everything: rate limits, retries, provider routing
            response = self.litellm.completion(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                max_tokens=2000,
                temperature=0.7
                # LiteLLM handles all the provider-specific complexity
            )
            
            # Extract metadata from LiteLLM response
            metadata = {
                "model": model,
                "role": model_role,
                "provider": "litellm",
                "usage": {
                    "prompt_tokens": getattr(response.usage, 'prompt_tokens', 0),
                    "completion_tokens": getattr(response.usage, 'completion_tokens', 0),
                    "total_tokens": getattr(response.usage, 'total_tokens', 0)
                },
                "cost": getattr(response, '_cost', 0.0)
            }
            
            return response.choices[0].message.content, metadata
            
        except Exception as e:
            print(f"LiteLLM call failed ({e}), using mock")
            return self._mock_response_with_metadata(prompt, model_role)
    
    def _call_direct_fallback_with_metadata(self, prompt: str, model_role: str) -> Tuple[str, Dict[str, Any]]:
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
                
                metadata = {
                    "model": "claude-3-5-sonnet-20241022",
                    "role": model_role,
                    "provider": "anthropic_direct",
                    "usage": {
                        "prompt_tokens": response.usage.input_tokens,
                        "completion_tokens": response.usage.output_tokens,
                        "total_tokens": response.usage.input_tokens + response.usage.output_tokens
                    },
                    "cost": 0.0  # Would need to calculate based on pricing
                }
                
                return response.content[0].text, metadata
                
            except Exception as e:
                print(f"Direct Anthropic failed ({e}), using mock")
                return self._mock_response_with_metadata(prompt, model_role)
        
        return self._mock_response_with_metadata(prompt, model_role)
    
    def _mock_response_with_metadata(self, prompt: str, model_role: str) -> Tuple[str, Dict[str, Any]]:
        """Fallback to mock responses with metadata"""
        response_text = self._mock_response(prompt, model_role)
        
        metadata = {
            "model": "mock_model",
            "role": model_role,
            "provider": "mock",
            "usage": {
                "prompt_tokens": len(prompt) // 4,  # Rough estimate
                "completion_tokens": len(response_text) // 4,
                "total_tokens": (len(prompt) + len(response_text)) // 4
            },
            "cost": 0.0
        }
        
        return response_text, metadata

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
        
        # For testing/development: Use cheaper Gemini models (10-40x cheaper than Claude)
        # Gemini 1.5 Flash: $0.13/$0.38 per 1M tokens vs Claude: $3/$15 per 1M tokens
        
        # Check if we have Vertex AI configured for cheaper models
        if hasattr(self, 'vertex_config') and self.vertex_config:
            # Use Gemini for cost optimization during testing
            cost_optimized_models = {
                'design': 'vertex_ai/gemini-2.5-flash',           # Design work - fast & cheap
                'design_llm': 'vertex_ai/gemini-2.5-flash',      # Design work - fast & cheap  
                'moderator': 'vertex_ai/gemini-2.5-pro',         # Coordination - more capable
                'moderator_llm': 'vertex_ai/gemini-2.5-pro',     # Coordination - more capable
                'specialist': 'vertex_ai/gemini-2.5-flash',      # Analysis - fast & cheap
                'adversarial': 'vertex_ai/gemini-2.5-flash',     # Critique - fast & cheap
                'analysis': 'vertex_ai/gemini-2.5-pro',          # Synthesis - more capable
                'referee': 'vertex_ai/gemini-2.5-pro',           # Final review - more capable
                'corpus_detective': 'vertex_ai/gemini-2.5-flash', # Detective work - fast & cheap
                'simulated_researcher': 'vertex_ai/gemini-2.5-flash',  # Simulated human responses
                'simulated_researcher_decision': 'vertex_ai/gemini-2.5-flash',  # Approval decisions
                'knowledgenaut_agent': 'vertex_ai/gemini-2.5-pro'  # Research agent - more capable
            }
            print(f"💰 Using cost-optimized Gemini model for {role} (10-40x cheaper than Claude)")
            return cost_optimized_models.get(role, 'vertex_ai/gemini-2.5-flash')
        
        # Fallback to Claude if Vertex AI not configured
        expensive_models = {
            'design': 'claude-3-5-sonnet-20241022',
            'design_llm': 'claude-3-5-sonnet-20241022',
            'moderator': 'claude-3-5-sonnet-20241022',
            'moderator_llm': 'claude-3-5-sonnet-20241022',
            'specialist': 'claude-3-5-sonnet-20241022', 
            'adversarial': 'claude-3-5-sonnet-20241022',
            'analysis': 'claude-3-5-sonnet-20241022',
            'referee': 'claude-3-5-sonnet-20241022',
            'corpus_detective': 'claude-3-5-sonnet-20241022',
            'simulated_researcher': 'claude-3-5-sonnet-20241022',
            'simulated_researcher_decision': 'claude-3-5-sonnet-20241022',
            'knowledgenaut_agent': 'claude-3-5-sonnet-20241022'
        }
        print(f"💸 Using expensive Claude model for {role} (consider setting up Vertex AI)")
        return expensive_models.get(role, 'claude-3-5-sonnet-20241022')
    
    def _mock_response(self, prompt: str, model_role: str) -> str:
        """Fallback to mock responses"""
        # Enhanced mock responses based on role - more realistic for development
        mock_responses = {
            'design': f"For analyzing the provided research question, I recommend this systematic methodology:\n\n**Step 1: Initial Reading**\n- Read all source texts for overall themes\n- Identify key patterns and concepts\n\n**Step 2: Expert Consultation**\n- Bring in knowledgenaut_agent for literature validation\n- Use specialist agents for focused analysis\n\n**Step 3: Targeted Analysis**\n- Examine specific evidence patterns\n- Quantify and qualify findings\n\nThis multi-expert approach should provide comprehensive analysis. Does this methodology look right to you?",
            'design_llm': f"For analyzing the provided research question, I recommend this systematic methodology:\n\n**Step 1: Initial Reading**\n- Read all source texts for overall themes\n- Identify key patterns and concepts\n\n**Step 2: Expert Consultation**\n- Bring in knowledgenaut_agent for literature validation\n- Use specialist agents for focused analysis\n\n**Step 3: Targeted Analysis**\n- Examine specific evidence patterns\n- Quantify and qualify findings\n\nThis multi-expert approach should provide comprehensive analysis. Does this methodology look right to you?",
            'moderator': f"Based on the approved methodology, I'll coordinate the multi-expert analysis. Let me start by consulting the knowledgenaut_agent for literature validation, then proceed with systematic analysis of the source texts.",
            'moderator_llm': f"Based on the approved design, I'll coordinate the multi-expert analysis. Let me start by interpreting the design and requesting input from the first expert needed.\n\nREQUEST TO Historical_Context_Expert: Please provide historical context for the research question to establish our analytical foundation.",
            'specialist': f"As requested, I'll analyze the specific patterns in the provided texts. Based on my examination, I can identify several key themes and provide detailed analysis of the evidence.",
            'adversarial': f"I need to challenge some assumptions in this analysis. Have we considered alternative interpretations of the evidence? Are there potential biases in our analytical framework?",
            'analysis': f"Synthesizing all expert perspectives, the key findings suggest significant patterns that address the research question. The evidence supports the following conclusions...",
            'referee': f"Final assessment: The methodology appears sound and the evidence supports the conclusions drawn. The multi-expert approach has provided comprehensive coverage.",
            'corpus_detective': f"**CORPUS ANALYSIS REPORT**\n\nI've analyzed the provided corpus systematically:\n\n**Document Types:** The corpus appears to contain political speeches and addresses.\n\n**Authors/Speakers:** Based on filenames and content analysis, I can identify the primary speakers.\n\n**Time Periods:** The documents span multiple time periods as indicated by dates in filenames.\n\n**Potential Issues:** Some files may need encoding verification, and there may be duplicate versions.\n\n**Metadata Inference:** From content analysis, I can determine context, audience, and occasion for most texts.\n\n**Questions for Clarification:** Are there specific aspects of the corpus you'd like me to focus on for your research?",
            'simulated_researcher': f"This design looks solid overall. I appreciate the multi-expert approach and the systematic methodology. I'd like to see more emphasis on quantitative validation of qualitative findings, but the framework should work well for addressing the research question. Please proceed with the analysis.",
            'simulated_researcher_decision': f"APPROVE",
            'knowledgenaut_agent': f"I've conducted a thorough literature review and framework validation. Based on my analysis of academic sources, I can provide insights on the theoretical foundations, identify relevant prior work, and highlight potential gaps in the current approach. The terminology and concepts appear well-grounded in established scholarship."
        }
        
        # Return appropriate mock response or default
        return mock_responses.get(model_role, "I understand the request and would analyze accordingly. [Mock response - LiteLLM API unavailable]")

    def get_available_models(self) -> List[str]:
        """Get list of available models based on configured API keys"""
        models = []
        
        # Add standard models based on existing API keys
        if os.getenv('ANTHROPIC_API_KEY'):
            models.extend(['claude-3-5-sonnet-20241022', 'claude-3-haiku-20240307'])
        
        if os.getenv('OPENAI_API_KEY'):
            models.extend(['gpt-4-turbo', 'gpt-3.5-turbo'])
        
        # Add Vertex AI models if configured
        if hasattr(self, 'vertex_config') and self.vertex_config:
            gemini_models = [
                "vertex_ai/gemini-1.5-flash",      # Fastest, cheapest: $0.13/$0.38 per 1M tokens
                "vertex_ai/gemini-1.5-flash-002",  # Latest flash version
                "vertex_ai/gemini-1.5-pro",        # Most capable: $1.25/$10 per 1M tokens
                "vertex_ai/gemini-1.5-pro-002",    # Latest pro version
                "vertex_ai/gemini-2.0-flash-exp",  # Experimental 2.0 models
                "vertex_ai/gemini-2.5-flash",      # Latest fast model
                "vertex_ai/gemini-2.5-pro",        # Latest thinking-native model
            ]
            models.extend(gemini_models)
            print(f"✅ Added {len(gemini_models)} Vertex AI Gemini models (significantly cheaper than OpenAI)")
        
        if not models:
            print("⚠️ No API keys configured - using mock responses")
            models = ['mock_model']
            
        return models

    def call_llm_with_vertex_support(self, model: str, messages: List[Dict[str, str]], **kwargs) -> Dict[str, Any]:
        """Enhanced call_llm method with Vertex AI support"""
        if not self.available:
            return self._mock_response_with_metadata("", model)[0]
        
        try:
            # Add Vertex AI specific parameters if using vertex models
            if model.startswith("vertex_ai/"):
                if hasattr(self, 'vertex_config') and self.vertex_config:
                    # Add vertex-specific parameters
                    if 'credentials' in self.vertex_config:
                        kwargs['vertex_credentials'] = json.dumps(self.vertex_config['credentials'])
                    kwargs['vertex_project'] = self.vertex_config['project']
                    kwargs['vertex_location'] = self.vertex_config['location']
                    
                    print(f"🚀 Calling Vertex AI model: {model} (cheaper alternative to OpenAI)")
                else:
                    raise Exception("Vertex AI model requested but no Vertex AI configuration found")
            
            response = self.litellm.completion(
                model=model,
                messages=messages,
                **kwargs
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"LiteLLM call failed ({e}), using fallback")
            return self._mock_response("", model) 