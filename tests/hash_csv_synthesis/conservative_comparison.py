#!/usr/bin/env python3
"""
Conservative Hash CSV optimization comparison.

Shows the tradeoffs between efficiency and academic clarity.
"""

import sys
import os
from pathlib import Path
import json

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from discernus.core.synthesis_orchestrator import SynthesisOrchestrator


def compare_conservative_approach():
    """Compare original, conservative, and aggressive optimization approaches."""
    
    print("🎯 Conservative Hash CSV Optimization Analysis")
    print("=" * 70)
    print("Comparing academic quality vs token efficiency tradeoffs")
    print()
    
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
    
    # Baseline: Original JSON size
    total_json_chars = 0
    for artifact_path in json_artifacts:
        with open(artifact_path, 'r', encoding='utf-8') as f:
            content = f.read()
            total_json_chars += len(content)
    
    print(f"📏 Baseline - Original JSON: {total_json_chars:,} characters")
    print()
    
    temp_dir = Path("/tmp/conservative_comparison")
    temp_dir.mkdir(exist_ok=True)
    
    # Test all three approaches
    approaches = []
    
    # 1. Original Hash CSV
    print("🔄 Approach 1: Original Hash CSV")
    scores_orig, evidence_orig, _ = orchestrator.generate_hash_cross_referenced_csv(
        json_artifacts, temp_dir
    )
    
    with open(scores_orig, 'r') as f:
        orig_scores_chars = len(f.read())
    with open(evidence_orig, 'r') as f:
        orig_evidence_chars = len(f.read())
    orig_total_chars = orig_scores_chars + orig_evidence_chars
    
    approaches.append(("Original", orig_total_chars, orig_scores_chars, orig_evidence_chars, 0))
    print(f"   - Total: {orig_total_chars:,} chars ({((total_json_chars - orig_total_chars) / total_json_chars):.1%} reduction)")
    print()
    
    # 2. Conservative optimization
    print("🎯 Approach 2: Conservative Hash CSV (Recommended)")
    scores_cons, evidence_cons, lookup_cons, _ = orchestrator.generate_conservative_hash_csv(
        json_artifacts, temp_dir
    )
    
    with open(scores_cons, 'r') as f:
        cons_scores_chars = len(f.read())
    with open(evidence_cons, 'r') as f:
        cons_evidence_chars = len(f.read())
    with open(lookup_cons, 'r') as f:
        cons_lookup_chars = len(f.read())
    cons_total_chars = cons_scores_chars + cons_evidence_chars + cons_lookup_chars
    
    approaches.append(("Conservative", cons_total_chars, cons_scores_chars, cons_evidence_chars, cons_lookup_chars))
    print(f"   - Total: {cons_total_chars:,} chars ({((total_json_chars - cons_total_chars) / total_json_chars):.1%} reduction)")
    print()
    
    # 3. Aggressive optimization
    print("🚀 Approach 3: Aggressive Hash CSV")
    scores_aggr, evidence_aggr, lookup_aggr, _ = orchestrator.generate_optimized_hash_csv(
        json_artifacts, temp_dir
    )
    
    with open(scores_aggr, 'r') as f:
        aggr_scores_chars = len(f.read())
    with open(evidence_aggr, 'r') as f:
        aggr_evidence_chars = len(f.read())
    with open(lookup_aggr, 'r') as f:
        aggr_lookup_chars = len(f.read())
    aggr_total_chars = aggr_scores_chars + aggr_evidence_chars + aggr_lookup_chars
    
    approaches.append(("Aggressive", aggr_total_chars, aggr_scores_chars, aggr_evidence_chars, aggr_lookup_chars))
    print(f"   - Total: {aggr_total_chars:,} chars ({((total_json_chars - aggr_total_chars) / total_json_chars):.1%} reduction)")
    print()
    
    # Comparison table
    print("📊 Detailed Comparison:")
    print("=" * 70)
    print(f"{'Approach':<12} {'Total':<8} {'Scores':<8} {'Evidence':<10} {'Lookup':<8} {'Reduction':<10}")
    print("-" * 70)
    for name, total, scores, evidence, lookup in approaches:
        reduction = f"{((total_json_chars - total) / total_json_chars):.1%}"
        print(f"{name:<12} {total:<8,} {scores:<8,} {evidence:<10,} {lookup:<8,} {reduction:<10}")
    print()
    
    # Academic quality analysis
    print("🎓 Academic Quality Analysis:")
    print("=" * 40)
    
    # Show sample content from each approach
    print("📋 Sample Content Comparison:")
    print()
    
    # Conservative scores sample
    print("🎯 Conservative Scores CSV (Full dimension names):")
    with open(scores_cons, 'r') as f:
        lines = f.readlines()[:3]
        for i, line in enumerate(lines, 1):
            if len(line) > 120:
                line = line[:117] + "..."
            print(f"   {i}: {line.strip()}")
    print()
    
    # Conservative evidence sample  
    print("🎯 Conservative Evidence CSV (Full quotes):")
    with open(evidence_cons, 'r') as f:
        lines = f.readlines()[:4]
        for i, line in enumerate(lines, 1):
            if i == 1:  # Header
                print(f"   {i}: {line.strip()}")
            else:  # Show first 100 chars of quote to demonstrate full preservation
                if len(line) > 100:
                    parts = line.split('","')
                    if len(parts) >= 4:
                        quote_part = parts[3][:100] + "..." if len(parts[3]) > 100 else parts[3]
                        print(f"   {i}: {parts[0]},{parts[1]},{parts[2]},\"{quote_part}\"...")
                    else:
                        print(f"   {i}: {line[:100]}...")
                else:
                    print(f"   {i}: {line.strip()}")
    print()
    
    # Token efficiency analysis
    orig_tokens = orig_total_chars // 4
    cons_tokens = cons_total_chars // 4  
    aggr_tokens = aggr_total_chars // 4
    
    print("🧠 Synthesis Agent Token Impact:")
    print(f"   - Original approach:    ~{orig_tokens:,} tokens")
    print(f"   - Conservative approach: ~{cons_tokens:,} tokens ({((orig_tokens - cons_tokens) / orig_tokens):.1%} reduction)")
    print(f"   - Aggressive approach:   ~{aggr_tokens:,} tokens ({((orig_tokens - aggr_tokens) / orig_tokens):.1%} reduction)")
    print()
    
    print("✅ Recommendation: Conservative Approach")
    print("=" * 50)
    print("Advantages:")
    print("  ✓ Hash compression provides the biggest efficiency gain (39.5%)")
    print("  ✓ Full dimension names (Dignity, Hope) preserve LLM semantic understanding")
    print("  ✓ Complete quotes eliminate need for evidence lookups")
    print("  ✓ Academic quality maintained with professional readability")
    print("  ✓ Still achieves substantial token reduction for scalability")
    print()
    print("Trade-offs accepted:")
    print(f"  • {cons_total_chars - aggr_total_chars:,} additional characters vs aggressive approach")
    print(f"  • {((cons_tokens - aggr_tokens) / aggr_tokens):.1%} more tokens than maximum optimization")
    print("  • Academic clarity prioritized over maximum efficiency")
    
    # Cleanup
    for file_path in [scores_orig, evidence_orig, scores_cons, evidence_cons, lookup_cons,
                      scores_aggr, evidence_aggr, lookup_aggr]:
        file_path.unlink()
    temp_dir.rmdir()


if __name__ == '__main__':
    compare_conservative_approach() 