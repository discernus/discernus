#!/usr/bin/env python3
"""
THIN Discipline Violation Logger
===============================

Simple append-only logging for THICK software anti-patterns.
Helps future agents learn from past mistakes.
"""

from datetime import datetime
from pathlib import Path


def log_violation(violation_description: str, lesson_learned: str):
    """
    Log a THIN discipline violation for future agent learning
    
    Args:
        violation_description: What anti-pattern occurred
        lesson_learned: What should be done instead
    """
    project_root = Path(__file__).parent.parent.parent
    log_file = project_root / "thin_discipline_violations.log"
    
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n[{timestamp}] - VIOLATION: {violation_description}\n")
        f.write(f"LESSON: {lesson_learned}\n")


def log_temptation(temptation_description: str, thin_alternative: str):
    """
    Log when tempted by THICK patterns but chose THIN approach
    
    Args:
        temptation_description: What THICK pattern was tempting
        thin_alternative: What THIN approach was chosen instead
    """
    project_root = Path(__file__).parent.parent.parent
    log_file = project_root / "thin_discipline_violations.log"
    
    timestamp = datetime.now().strftime("%Y-%m-%d")
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"\n[{timestamp}] - TEMPTATION RESISTED: {temptation_description}\n")
        f.write(f"THIN CHOICE: {thin_alternative}\n")


# Quick usage examples for future agents:
# log_violation("Added database state management", "Use file-based logging with Git commits instead")
# log_temptation("Wanted to parse LLM responses", "Let LLMs include all needed data inline") 