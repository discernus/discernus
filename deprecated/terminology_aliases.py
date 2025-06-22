#!/usr/bin/env python3
"""Deprecated terminology aliases for backward compatibility.

Importing these classes will raise a DeprecationWarning. They map the old
Narrative Gravity names to the new cartographic terminology.
"""

import warnings

__all__ = ["Well", "Dipole"]


class Well:
    """Alias for :class:`Anchor` (deprecated)."""

    def __init__(self, *args, **kwargs):
        warnings.warn(
            "Class 'Well' is deprecated; use 'Anchor' instead.",
            DeprecationWarning,
            stacklevel=2,
        )


class Dipole:
    """Alias for :class:`Axis` (deprecated)."""

    def __init__(self, *args, **kwargs):
        warnings.warn(
            "Class 'Dipole' is deprecated; use 'Axis' instead.",
            DeprecationWarning,
            stacklevel=2,
        )
