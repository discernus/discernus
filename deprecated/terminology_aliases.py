#!/usr/bin/env python3
"""Deprecated terminology aliases for backward compatibility.

Importing these classes will raise a DeprecationWarning. They map the old
Narrative Gravity names to the new cartographic terminology.
"""

import warnings

__all__ = ["Well", "Dipole"]


class Well:
    """Alias for :class:`Anchor` (deprecated)."""

    def __new__(cls, *args, **kwargs):
        warnings.warn(
            "Class 'Well' is deprecated; use 'Anchor' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        # Try to import and delegate to Anchor class
        try:
            from ..src.models.anchor import Anchor  # Adjust import path as needed
            return Anchor(*args, **kwargs)
        except ImportError:
            # Fallback: create a basic proxy object if Anchor doesn't exist yet
            instance = super().__new__(cls)
            instance._args = args
            instance._kwargs = kwargs
            return instance

    def __init__(self, *args, **kwargs):
        # Only initialize if we're the fallback proxy
        if hasattr(self, '_args'):
            self.args = args
            self.kwargs = kwargs


class Dipole:
    """Alias for :class:`Axis` (deprecated)."""

    def __new__(cls, *args, **kwargs):
        warnings.warn(
            "Class 'Dipole' is deprecated; use 'Axis' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
        # Try to import and delegate to Axis class
        try:
            from ..src.models.axis import Axis  # Adjust import path as needed
            return Axis(*args, **kwargs)
        except ImportError:
            # Fallback: create a basic proxy object if Axis doesn't exist yet
            instance = super().__new__(cls)
            instance._args = args
            instance._kwargs = kwargs
            return instance

    def __init__(self, *args, **kwargs):
        # Only initialize if we're the fallback proxy
        if hasattr(self, '_args'):
            self.args = args
            self.kwargs = kwargs
