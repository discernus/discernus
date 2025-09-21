#!/usr/bin/env python3
"""
Error Reporter
==============

Generates detailed error reports for the Show Your Work architecture.
"""

import json
import traceback
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional, List


class ErrorReporter:
    """Generates detailed error reports for debugging and recovery"""
    
    def __init__(self, run_folder: Path):
        """
        Initialize the error reporter
        
        Args:
            run_folder: The run folder for this experiment
        """
        self.run_folder = run_folder
        self.error_dir = run_folder / "errors"
        self.error_dir.mkdir(exist_ok=True)
    
    def create_error_report(self, 
                           phase: str, 
                           error: str, 
                           context: Optional[Dict[str, Any]] = None,
                           document_name: Optional[str] = None) -> str:
        """
        Create a detailed error report
        
        Args:
            phase: The phase where the error occurred
            error: The error message
            context: Additional context information
            document_name: Optional document name if error is document-specific
            
        Returns:
            Error report file path
        """
        timestamp = datetime.now(timezone.utc)
        error_id = f"{phase}_{timestamp.strftime('%Y%m%d_%H%M%S')}"
        
        error_report = {
            "error_id": error_id,
            "phase": phase,
            "timestamp": timestamp.isoformat(),
            "error_message": str(error),
            "document_name": document_name,
            "context": context or {},
            "traceback": traceback.format_exc(),
            "run_folder": str(self.run_folder)
        }
        
        # Save error report
        error_file = self.error_dir / f"{error_id}.json"
        with open(error_file, 'w') as f:
            json.dump(error_report, f, indent=2)
        
        # Create human-readable summary
        summary_file = self.error_dir / f"{error_id}_summary.txt"
        with open(summary_file, 'w') as f:
            f.write(f"ERROR REPORT: {error_id}\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Phase: {phase}\n")
            f.write(f"Timestamp: {timestamp.isoformat()}\n")
            if document_name:
                f.write(f"Document: {document_name}\n")
            f.write(f"Error: {error}\n\n")
            f.write("Context:\n")
            f.write(json.dumps(context or {}, indent=2))
            f.write("\n\nTraceback:\n")
            f.write(traceback.format_exc())
        
        return str(error_file)
    
    def get_error_reports(self, phase: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get error reports, optionally filtered by phase
        
        Args:
            phase: Optional phase filter
            
        Returns:
            List of error reports
        """
        error_files = list(self.error_dir.glob("*.json"))
        reports = []
        
        for error_file in error_files:
            try:
                with open(error_file, 'r') as f:
                    report = json.load(f)
                
                if phase is None or report.get("phase") == phase:
                    reports.append(report)
            except Exception:
                # Skip corrupted error files
                continue
        
        return sorted(reports, key=lambda x: x["timestamp"], reverse=True)
    
    def get_latest_error(self, phase: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Get the most recent error report
        
        Args:
            phase: Optional phase filter
            
        Returns:
            Most recent error report or None
        """
        reports = self.get_error_reports(phase)
        return reports[0] if reports else None
