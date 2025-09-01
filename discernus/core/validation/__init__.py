#!/usr/bin/env python3
"""
Unified Validation Classes for Discernus Platform

Provides standardized validation data structures used across all validation agents.
These classes ensure consistency and reduce code duplication.
"""

from .validation_types import ValidationIssue, ValidationResult

__all__ = ['ValidationIssue', 'ValidationResult']

