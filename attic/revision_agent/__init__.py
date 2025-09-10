"""
Revision Agent Package

This package contains the Revision Agent, which is responsible for:
- Taking fact checker findings and applying corrections to draft reports
- Using the search index to look up appropriate revisions
- Applying corrections based on predefined strategies
- Adding warnings when corrections cannot be made
"""

from .agent import RevisionAgent

__all__ = ['RevisionAgent']
