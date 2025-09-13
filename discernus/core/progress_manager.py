#!/usr/bin/env python3
"""
Progress Manager
================

Simple progress tracking for the Show Your Work architecture.
"""

from typing import Dict, Any, Optional


class ProgressManager:
    """Simple progress tracking manager"""
    
    def __init__(self):
        """Initialize the progress manager"""
        self.current_progress = {}
    
    def update_progress(self, phase: str, current: int, total: int, message: str = "") -> None:
        """
        Update progress for a phase
        
        Args:
            phase: The phase name
            current: Current progress (0-based)
            total: Total items
            message: Optional progress message
        """
        percentage = (current / total * 100) if total > 0 else 0
        
        self.current_progress[phase] = {
            "current": current,
            "total": total,
            "percentage": percentage,
            "message": message
        }
    
    def get_progress(self, phase: Optional[str] = None) -> Dict[str, Any]:
        """
        Get current progress
        
        Args:
            phase: Optional specific phase, or None for all phases
            
        Returns:
            Progress information
        """
        if phase:
            return self.current_progress.get(phase, {})
        return self.current_progress
    
    def clear_progress(self) -> None:
        """Clear all progress information"""
        self.current_progress.clear()
