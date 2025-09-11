#!/usr/bin/env python3
"""
Base Gateway Abstract Class
===========================

Defines the abstract interface for all LLM gateways in the Discernus system.
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