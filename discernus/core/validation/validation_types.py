#!/usr/bin/env python3
"""
Unified Validation Types for Discernus Platform

Standardized validation data structures that consolidate functionality from:
- Framework Validator (framework_validator.py)
- Experiment Coherence Agent (experiment_coherence_agent/agent.py)

Provides backwards compatibility while reducing code duplication.
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


from typing import Any, Dict, List, Optional
from dataclasses import dataclass


@dataclass
class ValidationIssue:
    """
    Represents a validation issue with clear description and fix.

    Unified version that supports all use cases:
    - Framework validation (basic fields)
    - Experiment validation (with affected_files)
    """
    category: str
    description: str
    impact: str
    fix: str
    priority: str = "BLOCKING"  # BLOCKING, QUALITY, SUGGESTION
    affected_files: Optional[List[str]] = None

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'ValidationIssue':
        """Create ValidationIssue from dictionary (backwards compatibility)."""
        return cls(
            category=data.get('category', data.get('type', 'unknown')),
            description=data.get('description', 'Unknown issue'),
            impact=data.get('impact', 'Unknown impact'),
            fix=data.get('fix', 'No fix provided'),
            priority=data.get('priority', 'BLOCKING'),
            affected_files=data.get('affected_files', [])
        )


@dataclass
class ValidationResult:
    """
    Unified validation result that supports all use cases.

    Combines functionality from:
    - Framework Validator (framework_name, framework_version)
    - Experiment Coherence Agent (llm_metadata)
    """
    success: bool
    issues: List[ValidationIssue]
    suggestions: List[str]

    # Framework-specific fields (optional for backwards compatibility)
    framework_name: Optional[str] = None
    framework_version: Optional[str] = None

    # Experiment-specific fields (optional for backwards compatibility)
    llm_metadata: Optional[Dict[str, Any]] = None

    def has_blocking_issues(self) -> bool:
        """Check if any issues are blocking."""
        return any(issue.priority == "BLOCKING" for issue in self.issues)

    def get_issues_by_priority(self, priority: str) -> List[ValidationIssue]:
        """Get issues filtered by priority level."""
        return [issue for issue in self.issues if issue.priority == priority]

    def get_blocking_issues(self) -> List[ValidationIssue]:
        """Get all blocking issues."""
        return self.get_issues_by_priority("BLOCKING")

    def get_quality_issues(self) -> List[ValidationIssue]:
        """Get all quality issues."""
        return self.get_issues_by_priority("QUALITY")

    def get_suggestion_issues(self) -> List[ValidationIssue]:
        """Get all suggestion issues."""
        return self.get_issues_by_priority("SUGGESTION")

    @classmethod
    def for_framework(cls, success: bool, issues: List[ValidationIssue],
                     suggestions: List[str], framework_name: str,
                     framework_version: str) -> 'ValidationResult':
        """Factory method for framework validation results."""
        return cls(
            success=success,
            issues=issues,
            suggestions=suggestions,
            framework_name=framework_name,
            framework_version=framework_version
        )

    @classmethod
    def for_experiment(cls, success: bool, issues: List[ValidationIssue],
                      suggestions: List[str],
                      llm_metadata: Optional[Dict[str, Any]] = None) -> 'ValidationResult':
        """Factory method for experiment validation results."""
        return cls(
            success=success,
            issues=issues,
            suggestions=suggestions,
            llm_metadata=llm_metadata
        )

