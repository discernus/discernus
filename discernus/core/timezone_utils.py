#!/usr/bin/env python3
"""
Timezone Utilities for Discernus
===============================

Provides consistent timezone handling and debugging tools for temporal correlation.
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


from datetime import datetime, timezone
from typing import Optional, Dict, Any
import json
from pathlib import Path


def get_current_utc_timestamp() -> str:
    """Get current UTC timestamp with timezone indicator."""
    return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')


def get_current_utc_iso() -> str:
    """Get current UTC timestamp in ISO format."""
    return datetime.now(timezone.utc).isoformat()


def parse_timestamp_with_timezone(timestamp_str: str) -> Optional[datetime]:
    """
    Parse timestamp string with timezone handling.
    
    Handles various formats:
    - ISO format: 2025-01-27T10:15:23Z
    - ISO with timezone: 2025-01-27T10:15:23+00:00
    - UTC format: 2025-01-27 10:15:23 UTC
    - Local format: 2025-01-27 10:15:23 (assumes UTC)
    """
    try:
        # Try ISO format first
        if 'T' in timestamp_str:
            if timestamp_str.endswith('Z'):
                # Remove Z and add timezone
                clean_timestamp = timestamp_str.replace('Z', '+00:00')
                return datetime.fromisoformat(clean_timestamp)
            elif '+' in timestamp_str or timestamp_str.count('-') > 2:
                # Already has timezone info
                return datetime.fromisoformat(timestamp_str)
            else:
                # ISO without timezone, assume UTC
                return datetime.fromisoformat(timestamp_str).replace(tzinfo=timezone.utc)
        
        # Try UTC format
        if timestamp_str.endswith(' UTC'):
            clean_timestamp = timestamp_str.replace(' UTC', '')
            return datetime.strptime(clean_timestamp, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
        
        # Try local format (assume UTC)
        return datetime.strptime(timestamp_str, '%Y-%m-%d %H:%M:%S').replace(tzinfo=timezone.utc)
        
    except Exception:
        return None


def correlate_timestamps(log_timestamp: str, artifact_timestamp: str, 
                        tolerance_seconds: int = 300) -> Dict[str, Any]:
    """
    Correlate timestamps from logs and artifacts to help with debugging.
    
    Args:
        log_timestamp: Timestamp from log file
        artifact_timestamp: Timestamp from artifact
        tolerance_seconds: Maximum time difference to consider as correlated
    
    Returns:
        Dictionary with correlation analysis
    """
    log_dt = parse_timestamp_with_timezone(log_timestamp)
    artifact_dt = parse_timestamp_with_timezone(artifact_timestamp)
    
    if not log_dt or not artifact_dt:
        return {
            "correlated": False,
            "error": "Could not parse one or both timestamps",
            "log_parsed": log_dt is not None,
            "artifact_parsed": artifact_dt is not None
        }
    
    time_diff = abs((log_dt - artifact_dt).total_seconds())
    
    return {
        "correlated": time_diff <= tolerance_seconds,
        "time_difference_seconds": time_diff,
        "log_timestamp": log_dt.isoformat(),
        "artifact_timestamp": artifact_dt.isoformat(),
        "log_utc": log_dt.strftime('%Y-%m-%d %H:%M:%S UTC'),
        "artifact_utc": artifact_dt.strftime('%Y-%m-%d %H:%M:%S UTC'),
        "tolerance_seconds": tolerance_seconds
    }


def analyze_experiment_timeline(run_directory: Path) -> Dict[str, Any]:
    """
    Analyze timestamps across an experiment run to identify timezone issues.
    
    Args:
        run_directory: Path to experiment run directory
    
    Returns:
        Dictionary with timeline analysis
    """
    timeline_analysis = {
        "run_directory": str(run_directory),
        "analysis_timestamp": get_current_utc_timestamp(),
        "log_files": [],
        "artifacts": [],
        "timezone_issues": [],
        "recommendations": []
    }
    
    # Analyze log files
    logs_dir = run_directory / "logs"
    if logs_dir.exists():
        for log_file in logs_dir.glob("*.jsonl"):
            try:
                with open(log_file) as f:
                    timestamps = []
                    for line in f:
                        if line.strip():
                            entry = json.loads(line)
                            if 'timestamp' in entry:
                                timestamps.append(entry['timestamp'])
                    
                    if timestamps:
                        timeline_analysis["log_files"].append({
                            "file": log_file.name,
                            "entry_count": len(timestamps),
                            "first_timestamp": timestamps[0],
                            "last_timestamp": timestamps[-1],
                            "sample_timestamps": timestamps[:3]  # First 3 for analysis
                        })
            except Exception as e:
                timeline_analysis["timezone_issues"].append(f"Error reading {log_file.name}: {e}")
    
    # Analyze artifacts
    artifacts_dir = run_directory / "shared_cache" / "artifacts"
    if artifacts_dir.exists():
        registry_file = artifacts_dir / "artifact_registry.json"
        if registry_file.exists():
            try:
                with open(registry_file) as f:
                    registry = json.load(f)
                
                artifact_timestamps = []
                for artifact_id, info in registry.items():
                    if 'created_at' in info:
                        artifact_timestamps.append(info['created_at'])
                
                if artifact_timestamps:
                    timeline_analysis["artifacts"] = {
                        "total_artifacts": len(artifact_timestamps),
                        "first_artifact": artifact_timestamps[0],
                        "last_artifact": artifact_timestamps[-1],
                        "sample_timestamps": artifact_timestamps[:3]
                    }
            except Exception as e:
                timeline_analysis["timezone_issues"].append(f"Error reading artifact registry: {e}")
    
    # Check for timezone consistency
    all_timestamps = []
    for log_file in timeline_analysis["log_files"]:
        all_timestamps.extend(log_file["sample_timestamps"])
    
    if timeline_analysis["artifacts"]:
        all_timestamps.extend(timeline_analysis["artifacts"]["sample_timestamps"])
    
    # Analyze timestamp formats
    timezone_formats = {}
    for timestamp in all_timestamps:
        if 'Z' in timestamp:
            timezone_formats['Z_suffix'] = timezone_formats.get('Z_suffix', 0) + 1
        elif 'UTC' in timestamp:
            timezone_formats['UTC_suffix'] = timezone_formats.get('UTC_suffix', 0) + 1
        elif '+' in timestamp or timestamp.count('-') > 2:
            timezone_formats['timezone_offset'] = timezone_formats.get('timezone_offset', 0) + 1
        else:
            timezone_formats['no_timezone'] = timezone_formats.get('no_timezone', 0) + 1
    
    if len(timezone_formats) > 1:
        timeline_analysis["timezone_issues"].append(
            f"Inconsistent timezone formats detected: {timezone_formats}"
        )
        timeline_analysis["recommendations"].append(
            "Standardize all timestamps to use UTC with explicit timezone indicators"
        )
    
    if timezone_formats.get('no_timezone', 0) > 0:
        timeline_analysis["timezone_issues"].append(
            f"Found {timezone_formats['no_timezone']} timestamps without timezone indicators"
        )
        timeline_analysis["recommendations"].append(
            "Add timezone indicators to all timestamps for better correlation"
        )
    
    return timeline_analysis


def create_timezone_debug_report(run_directory: Path, output_file: Optional[Path] = None) -> str:
    """
    Create a comprehensive timezone debug report for an experiment run.
    
    Args:
        run_directory: Path to experiment run directory
        output_file: Optional output file path
    
    Returns:
        Report content as string
    """
    analysis = analyze_experiment_timeline(run_directory)
    
    report = f"""# Timezone Debug Report
Generated: {analysis['analysis_timestamp']}
Run Directory: {analysis['run_directory']}

## Summary
"""
    
    if analysis['timezone_issues']:
        report += f"❌ Found {len(analysis['timezone_issues'])} timezone issues\n\n"
        report += "## Issues Found\n"
        for issue in analysis['timezone_issues']:
            report += f"- {issue}\n"
        report += "\n"
    else:
        report += "✅ No timezone issues detected\n\n"
    
    if analysis['recommendations']:
        report += "## Recommendations\n"
        for rec in analysis['recommendations']:
            report += f"- {rec}\n"
        report += "\n"
    
    if analysis['log_files']:
        report += "## Log File Analysis\n"
        for log_file in analysis['log_files']:
            report += f"### {log_file['file']}\n"
            report += f"- Entries: {log_file['entry_count']}\n"
            report += f"- First: {log_file['first_timestamp']}\n"
            report += f"- Last: {log_file['last_timestamp']}\n"
            report += f"- Sample: {', '.join(log_file['sample_timestamps'])}\n\n"
    
    if analysis['artifacts']:
        report += "## Artifact Analysis\n"
        artifacts = analysis['artifacts']
        report += f"- Total artifacts: {artifacts['total_artifacts']}\n"
        report += f"- First: {artifacts['first_artifact']}\n"
        report += f"- Last: {artifacts['last_artifact']}\n"
        report += f"- Sample: {', '.join(artifacts['sample_timestamps'])}\n\n"
    
    report += "## Usage Tips\n"
    report += "- All system timestamps are in UTC\n"
    report += "- Use 'Z' suffix or 'UTC' indicator for clarity\n"
    report += "- Local time observations should be converted to UTC for correlation\n"
    report += "- 5-hour difference typically indicates EST/EDT vs UTC\n\n"
    
    if output_file:
        output_file.write_text(report)
        report += f"Report saved to: {output_file}\n"
    
    return report
