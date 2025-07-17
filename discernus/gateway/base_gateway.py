#!/usr/bin/env python3
"""
Base Gateway Abstract Class
===========================

Defines the abstract interface for all LLM gateways in the Discernus system.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Tuple

class BaseGateway(ABC):
    """
    Abstract base class for LLM gateways. All gateways, real or mock, must
    implement this interface.
    """

    @abstractmethod
    def execute_call(self, model: str, prompt: str, **kwargs) -> Tuple[str, Dict[str, Any]]:
        """
        Executes a call to an LLM provider.

        Args:
            model: The identifier of the model to use.
            prompt: The prompt to send to the model.
            **kwargs: Additional provider-specific parameters.

        Returns:
            A tuple containing the string content of the response and a
            dictionary of metadata.
        """
        pass 