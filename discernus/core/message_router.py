#!/usr/bin/env python3
"""
Message Router - Ultra-thin routing between LLM roles
==================================================

Pure message routing with handoff detection. No intelligence, just clean routing.
"""

import re
from typing import Dict, List, Optional, Tuple
from .thin_litellm_client import ThinLiteLLMClient

class MessageRouter:
    """Ultra-thin message routing between LLM roles"""
    
    def __init__(self):
        self.llm_client = ThinLiteLLMClient()
        self.conversation_history: List[Dict] = []
        
    def route_message(self, message: str, from_role: str, to_role: str) -> str:
        """Route message between LLM roles"""
        
        # Log the message
        self.conversation_history.append({
            'from': from_role,
            'to': to_role,
            'message': message,
            'timestamp': self._get_timestamp()
        })
        
        # Get role-specific prompt
        full_prompt = self._build_role_prompt(to_role, message)
        
        # Call LLM (with LiteLLM handling rate limits, retries, etc.)
        response = self.llm_client.call_llm(full_prompt, to_role)
        
        # Log response
        self.conversation_history.append({
            'from': to_role,
            'to': from_role,
            'message': response,
            'timestamp': self._get_timestamp()
        })
        
        return response
    
    def detect_handoff(self, message: str) -> Optional[str]:
        """Detect if message contains handoff to another role"""
        
        handoff_patterns = [
            (r'@(\w+)', r'\1'),  # @ModeratorLLM -> moderator
            (r'handoff to (\w+)', r'\1'),  # handoff to specialist -> specialist
            (r'passing to (\w+)', r'\1'),  # passing to adversarial -> adversarial
            (r'(\w+) should handle', r'\1'),  # analysis should handle -> analysis
        ]
        
        for pattern, replacement in handoff_patterns:
            match = re.search(pattern, message, re.IGNORECASE)
            if match:
                return match.group(1).lower()
        
        return None
    
    def _build_role_prompt(self, role: str, message: str) -> str:
        """Build role-specific prompt"""
        from .agent_roles import get_expert_prompt as get_role_prompt
        
        # Get base role prompt
        base_prompt = get_role_prompt(role)
        
        # Add conversation context
        context = self._get_conversation_context()
        
        # Combine into full prompt
        full_prompt = f"{base_prompt}\n\n"
        
        if context:
            full_prompt += f"## Conversation Context:\n{context}\n\n"
        
        full_prompt += f"## Current Message:\n{message}\n\n"
        full_prompt += "## Your Response:"
        
        return full_prompt
    
    def _get_conversation_context(self) -> str:
        """Get recent conversation context"""
        if not self.conversation_history:
            return ""
        
        # Get last 3 exchanges for context
        recent_messages = self.conversation_history[-6:]  # 3 back-and-forth exchanges
        
        context_lines = []
        for msg in recent_messages:
            context_lines.append(f"**{msg['from']}**: {msg['message'][:200]}...")
        
        return "\n".join(context_lines)
    
    def _get_timestamp(self) -> str:
        """Get UTC timestamp"""
        from datetime import datetime
        return datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
    
    def get_conversation_history(self) -> List[Dict]:
        """Get full conversation history"""
        return self.conversation_history.copy() 