#!/usr/bin/env python3
"""
Analysis Cache for the Enhanced Analysis Agent.

Handles caching and retrieval of analysis results to avoid redundant LLM calls.
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


import json
from typing import Optional, Dict, Any

from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.core.audit_logger import AuditLogger


class AnalysisCache:
    """Handles caching for the EnhancedAnalysisAgent."""

    def __init__(self, storage: LocalArtifactStorage, audit: AuditLogger, agent_name: str):
        self.storage = storage
        self.audit = audit
        self.agent_name = agent_name

    def check_cache(self, analysis_id: str) -> Optional[Dict[str, Any]]:
        """Check if an analysis result is already cached."""
        for artifact_hash, artifact_info in self.storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            if (metadata.get("artifact_type") == "analysis_result" and
                    metadata.get("analysis_id") == analysis_id):

                print(f"💾 Cache hit for analysis: {analysis_id}")
                self.audit.log_agent_event(
                    self.agent_name, "cache_hit",
                    {"analysis_id": analysis_id, "cached_artifact_hash": artifact_hash}
                )
                cached_content = self.storage.get_artifact(artifact_hash)
                return json.loads(cached_content.decode('utf-8'))
        
        print(f"🔍 No cache hit for {analysis_id} - will perform analysis...")
        return None


