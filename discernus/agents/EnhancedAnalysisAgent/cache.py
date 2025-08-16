#!/usr/bin/env python3
"""
Analysis Cache for the Enhanced Analysis Agent.

Handles caching and retrieval of analysis results to avoid redundant LLM calls.
"""

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

    def check_cache(self, batch_id: str) -> Optional[Dict[str, Any]]:
        """Check if an analysis result is already cached."""
        for artifact_hash, artifact_info in self.storage.registry.items():
            metadata = artifact_info.get("metadata", {})
            if (metadata.get("artifact_type") == "analysis_result" and
                    metadata.get("batch_id") == batch_id):

                print(f"💾 Cache hit for analysis: {batch_id}")
                self.audit.log_agent_event(
                    self.agent_name, "cache_hit",
                    {"batch_id": batch_id, "cached_artifact_hash": artifact_hash}
                )
                cached_content = self.storage.get_artifact(artifact_hash)
                return json.loads(cached_content.decode('utf-8'))
        
        print(f"🔍 No cache hit for {batch_id} - will perform analysis...")
        return None


