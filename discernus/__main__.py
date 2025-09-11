#!/usr/bin/env python3
"""
Discernus Main Entry Point
==========================

Entry point for python -m discernus execution.
"""

# Copyright (C) 2025  Discernus Team

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


# Comprehensive LiteLLM debug suppression - must be done before ANY imports
import os
import logging

# Set critical environment variables immediately
os.environ['LITELLM_VERBOSE'] = 'false'
os.environ['LITELLM_LOG_LEVEL'] = 'ERROR'
os.environ['LITELLM_PROXY_LOG_LEVEL'] = 'ERROR'
os.environ['LITELLM_PROXY_DEBUG'] = 'false'
os.environ['JSON_LOGS'] = 'false'
os.environ['LITELLM_COLD_STORAGE_LOG_LEVEL'] = 'ERROR'

# Disable problematic loggers immediately
logging.getLogger('LiteLLM Proxy').setLevel(logging.ERROR)
logging.getLogger('LiteLLM Proxy').disabled = True
logging.getLogger('litellm.proxy').setLevel(logging.ERROR) 
logging.getLogger('litellm.proxy').disabled = True

from .cli import cli

if __name__ == "__main__":
    cli()
