#!/usr/bin/env python3
"""
THIN Pre-Check Script
=====================

Enforces THIN discipline before code changes by asking the critical questions
that prevent us from falling into THICK patterns.

Usage: python3 scripts/thin_precheck.py [file_to_check]
"""

import sys
import os
from pathlib import Path

def main():
    """Run the THIN pre-check questions."""
    
    print("🎯 THIN Architecture Pre-Check")
    print("=" * 50)
    
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
        print(f"📁 Checking: {file_path}")
    else:
        print("📁 General THIN compliance check")
    
    print("\n🤔 Before writing ANY parsing, validation, or 'smart' logic:")
    print("   Answer these questions honestly...")
    
    questions = [
        "1. Could an LLM do this better than regex/parsing logic?",
        "2. Do we have a pattern for this in ExperimentCoherenceAgent?",
        "3. Am I writing >10 lines of transformation/cleaning code?", 
        "4. Is this parsing/validating/reformatting LLM output?",
        "5. Am I creating multi-strategy fallback systems?"
    ]
    
    print("\n" + "=" * 60)
    for question in questions:
        print(f"❓ {question}")
    print("=" * 60)
    
    print("\n🚨 RULE: If ANY answer is YES → Use LLM intelligence, not software logic")
    print("\n✅ THIN Pattern:")
    print("   1. Try simple parsing (json.loads, basic extraction)")
    print("   2. If it fails → Ask LLM to reformat/fix it")  
    print("   3. Follow ExperimentCoherenceAgent._request_llm_reformat() pattern")
    
    print("\n❌ ANTI-PATTERN (What we keep doing wrong):")
    print("   1. Complex regex cleaning")
    print("   2. Multi-strategy parsing (try A, try B, try C...)")
    print("   3. Brittle text processing") 
    print("   4. Writing parsers for LLM output")
    
    print(f"\n📊 Current THIN violations: Run 'python3 scripts/thin_compliance_check.py'")
    print("🎯 Goal: Reduce violations, never increase them")
    
    print("\n" + "=" * 60)
    print("💭 Remember: LLMs understand structure better than regex")
    print("🤖 Trust LLM intelligence, minimize software complexity")
    print("=" * 60)

if __name__ == "__main__":
    main()
