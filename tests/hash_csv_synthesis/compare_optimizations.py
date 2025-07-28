#!/usr/bin/env python3
"""
Comparison script for Hash CSV optimization approaches.

Compares original vs optimized Hash CSV generation to measure token efficiency gains.
"""

import sys
import os
from pathlib import Path
import json

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from discernus.core.synthesis_orchestrator import SynthesisOrchestrator


def compare_approaches():
    """Compare original vs optimized Hash CSV approaches."""
    
    print("🔍 Hash CSV Optimization Comparison")
    print("=" * 60)
    
    # Setup
    orchestrator = SynthesisOrchestrator()
    fixtures_dir = Path(__file__).parent / "fixtures" / "sample_artifacts"
    
    # Find JSON artifacts
    json_artifacts = []
    for artifact in fixtures_dir.glob("*"):
        if artifact.is_file() and artifact.name != "artifact_registry.json":
            try:
                with open(artifact, 'r', encoding='utf-8') as f:
                    json.load(f)
                json_artifacts.append(artifact)
            except json.JSONDecodeError:
                continue
    
    if not json_artifacts:
        print("❌ No valid JSON artifacts found")
        return
    
    print(f"📊 Testing with {len(json_artifacts)} analysis artifacts")
    print()
    
    # Measure original JSON size
    total_json_chars = 0
    for artifact_path in json_artifacts:
        with open(artifact_path, 'r', encoding='utf-8') as f:
            content = f.read()
            total_json_chars += len(content)
    
    print(f"📏 Original JSON Size: {total_json_chars:,} characters")
    print()
    
    # Test original approach
    print("🔄 Testing Original Hash CSV Approach...")
    temp_dir_orig = Path("/tmp/hash_csv_original")
    temp_dir_orig.mkdir(exist_ok=True)
    
    scores_orig, evidence_orig, quarantined_orig = orchestrator.generate_hash_cross_referenced_csv(
        json_artifacts, temp_dir_orig
    )
    
    orig_scores_size = scores_orig.stat().st_size
    orig_evidence_size = evidence_orig.stat().st_size
    orig_total_size = orig_scores_size + orig_evidence_size
    
    with open(scores_orig, 'r') as f:
        orig_scores_chars = len(f.read())
    with open(evidence_orig, 'r') as f:
        orig_evidence_chars = len(f.read())
    orig_total_chars = orig_scores_chars + orig_evidence_chars
    
    print(f"   - Scores CSV: {orig_scores_size:,} bytes ({orig_scores_chars:,} chars)")
    print(f"   - Evidence CSV: {orig_evidence_size:,} bytes ({orig_evidence_chars:,} chars)")
    print(f"   - Total: {orig_total_size:,} bytes ({orig_total_chars:,} chars)")
    print(f"   - Reduction: {((total_json_chars - orig_total_chars) / total_json_chars):.1%}")
    print()
    
    # Test optimized approach
    print("🚀 Testing Optimized Hash CSV Approach...")
    temp_dir_opt = Path("/tmp/hash_csv_optimized")
    temp_dir_opt.mkdir(exist_ok=True)
    
    scores_opt, evidence_opt, lookup_opt, quarantined_opt = orchestrator.generate_optimized_hash_csv(
        json_artifacts, temp_dir_opt
    )
    
    opt_scores_size = scores_opt.stat().st_size
    opt_evidence_size = evidence_opt.stat().st_size
    opt_lookup_size = lookup_opt.stat().st_size
    opt_total_size = opt_scores_size + opt_evidence_size + opt_lookup_size
    
    with open(scores_opt, 'r') as f:
        opt_scores_chars = len(f.read())
    with open(evidence_opt, 'r') as f:
        opt_evidence_chars = len(f.read())
    with open(lookup_opt, 'r') as f:
        opt_lookup_chars = len(f.read())
    opt_total_chars = opt_scores_chars + opt_evidence_chars + opt_lookup_chars
    
    print(f"   - Scores CSV: {opt_scores_size:,} bytes ({opt_scores_chars:,} chars)")
    print(f"   - Evidence CSV: {opt_evidence_size:,} bytes ({opt_evidence_chars:,} chars)")
    print(f"   - Lookup CSV: {opt_lookup_size:,} bytes ({opt_lookup_chars:,} chars)")
    print(f"   - Total: {opt_total_size:,} bytes ({opt_total_chars:,} chars)")
    print(f"   - Reduction: {((total_json_chars - opt_total_chars) / total_json_chars):.1%}")
    print()
    
    # Comparison analysis
    improvement = ((orig_total_chars - opt_total_chars) / orig_total_chars) * 100
    overall_reduction = ((total_json_chars - opt_total_chars) / total_json_chars) * 100
    
    print("📈 Optimization Results:")
    print(f"   - Original CSV: {orig_total_chars:,} chars")
    print(f"   - Optimized CSV: {opt_total_chars:,} chars")
    print(f"   - CSV-to-CSV improvement: {improvement:.1f}%")
    print(f"   - Overall JSON reduction: {overall_reduction:.1f}%")
    print()
    
    # Show sample optimized content
    print("📋 Sample Optimized CSV Content:")
    print()
    print("🔢 Optimized Scores CSV:")
    with open(scores_opt, 'r') as f:
        lines = f.readlines()[:3]
        for i, line in enumerate(lines, 1):
            if len(line) > 80:
                line = line[:77] + "..."
            print(f"   {i}: {line.strip()}")
    print()
    
    print("📝 Optimized Evidence CSV:")
    with open(evidence_opt, 'r') as f:
        lines = f.readlines()[:5]
        for i, line in enumerate(lines, 1):
            if len(line) > 80:
                line = line[:77] + "..."
            print(f"   {i}: {line.strip()}")
    print()
    
    print("🔗 Lookup Table CSV:")
    with open(lookup_opt, 'r') as f:
        lines = f.readlines()[:3]
        for i, line in enumerate(lines, 1):
            if len(line) > 80:
                line = line[:77] + "..."
            print(f"   {i}: {line.strip()}")
    print()
    
    # Token implications
    est_orig_tokens = orig_total_chars // 4
    est_opt_tokens = opt_total_chars // 4
    
    print("🧠 Synthesis Agent Token Impact:")
    print(f"   - Original approach: ~{est_orig_tokens:,} tokens")
    print(f"   - Optimized approach: ~{est_opt_tokens:,} tokens")
    print(f"   - Token savings: ~{est_orig_tokens - est_opt_tokens:,} tokens ({improvement:.1f}%)")
    
    # Cleanup
    for file_path in [scores_orig, evidence_orig, scores_opt, evidence_opt, lookup_opt]:
        file_path.unlink()
    temp_dir_orig.rmdir()
    temp_dir_opt.rmdir()


if __name__ == '__main__':
    compare_approaches() 