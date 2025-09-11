#!/usr/bin/env python3
"""
Mock LLM Gateway for Testing
============================

A mock implementation of the LLMGateway for use in unit and integration tests.
This allows for rapid, cost-free testing of agent workflows without making
live API calls.
"""

Copyright (C) 2025  Discernus Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.


from typing import Dict, Any, Tuple, List, Optional
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.gateway.base_gateway import BaseGateway

class MockLLMGateway(BaseGateway):
    """
    A mock gateway that returns pre-defined responses instead of calling a real LLM.
    """
    def __init__(self, responses: List[str] | Dict[str, str]):
        """
        Initializes the mock gateway with a list of responses (for queuing)
        or a dictionary of responses (for key-based lookups).
        """
        self.responses = responses
        self.call_history = []
        print("🤫 MockLLMGateway initialized")

    def execute_call(self, model: str, prompt: str, **kwargs) -> Tuple[str, Dict[str, Any]]:
        """
        Overrides the real execute_call method. Handles both queued and keyed responses.
        """
        self.call_history.append({'model': model, 'prompt': prompt, 'kwargs': kwargs})
        
        content = None
        
        if isinstance(self.responses, list):
            if self.responses:
                content = self.responses.pop(0) # FIFO queue
        elif isinstance(self.responses, dict):
            # Key-based lookup logic
            response_key = next((key for key in self.responses if key in prompt), None)
            if response_key:
                content = self.responses[response_key]

        if content is not None:
            metadata = {
                "success": True,
                "model": f"mock_{model}",
                "usage": {"prompt_tokens": len(prompt), "completion_tokens": len(content), "total_tokens": len(prompt) + len(content)},
                "attempts": 1
            }
            return content, metadata
        else:
            # If no response is found, return an error.
            error_message = "MockLLMGateway: No mock response found for prompt."
            metadata = {
                "success": False,
                "error": error_message,
                "model": f"mock_{model}",
                "attempts": 1
            }
            return "", metadata

    def get_last_call(self) -> Optional[Dict[str, Any]]:
        """Returns the last call made to the gateway for assertion."""
        return self.call_history[-1] if self.call_history else None 