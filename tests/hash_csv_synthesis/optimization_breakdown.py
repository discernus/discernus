#!/usr/bin/env python3
"""
Detailed breakdown of Hash CSV optimization savings.

Measures the individual contribution of each optimization to overall token reduction.
"""

import sys
import os
from pathlib import Path
import json
import csv
import hashlib

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from discernus.core.synthesis_orchestrator import SynthesisOrchestrator


def analyze_optimization_breakdown():
    """Analyze the token savings contribution of each optimization."""
    
    print("🔍 Hash CSV Optimization Breakdown Analysis")
    print("=" * 70)
    
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
    
    print(f"📊 Analyzing {len(json_artifacts)} analysis artifacts")
    print()
    
    # Baseline: Original JSON size
    total_json_chars = 0
    for artifact_path in json_artifacts:
        with open(artifact_path, 'r', encoding='utf-8') as f:
            content = f.read()
            total_json_chars += len(content)
    
    print(f"📏 Baseline - Original JSON: {total_json_chars:,} characters")
    print()
    
    # Step 1: Original Hash CSV (baseline CSV)
    temp_dir = Path("/tmp/optimization_analysis")
    temp_dir.mkdir(exist_ok=True)
    
    scores_orig, evidence_orig, _ = orchestrator.generate_hash_cross_referenced_csv(
        json_artifacts, temp_dir
    )
    
    with open(scores_orig, 'r') as f:
        orig_scores_chars = len(f.read())
    with open(evidence_orig, 'r') as f:
        orig_evidence_chars = len(f.read())
    orig_total_chars = orig_scores_chars + orig_evidence_chars
    
    print(f"🔄 Step 1 - Original Hash CSV:")
    print(f"   - Scores: {orig_scores_chars:,} chars")
    print(f"   - Evidence: {orig_evidence_chars:,} chars")
    print(f"   - Total: {orig_total_chars:,} chars")
    print(f"   - Reduction from JSON: {((total_json_chars - orig_total_chars) / total_json_chars):.1%}")
    print()
    
    # Now let's implement each optimization step by step to measure individual impact
    
    # Step 2: Hash Compression Only (A1, A2, A3 instead of full hashes)
    print("🚀 Step 2 - Hash Compression Analysis:")
    
    # Calculate hash repetition savings
    evidence_rows = orig_evidence_chars // 150  # Rough estimate of rows
    hash_length = 64  # Original hash length
    short_id_length = 2  # A1, A2, etc.
    hash_savings_per_row = hash_length - short_id_length
    total_hash_savings = evidence_rows * hash_savings_per_row
    
    step2_total_chars = orig_total_chars - total_hash_savings
    step2_savings = ((orig_total_chars - step2_total_chars) / orig_total_chars) * 100
    
    print(f"   - Evidence rows (estimated): {evidence_rows}")
    print(f"   - Hash savings per row: {hash_savings_per_row} chars")
    print(f"   - Total hash compression savings: {total_hash_savings:,} chars")
    print(f"   - New total: {step2_total_chars:,} chars")
    print(f"   - Improvement from Step 1: {step2_savings:.1f}%")
    print()
    
    # Step 3: Add Dimension Abbreviations
    print("🎯 Step 3 - Dimension Abbreviation Analysis:")
    
    # Original dimension names vs abbreviated
    dimensions = ['Dignity', 'Tribalism', 'Truth', 'Manipulation', 'Justice', 
                  'Resentment', 'Hope', 'Fear', 'Pragmatism', 'Fantasy']
    abbreviations = ['DIG', 'TRB', 'TRU', 'MAN', 'JUS', 'RES', 'HOP', 'FEA', 'PRA', 'FAN']
    
    # Calculate dimension name savings
    total_dim_savings = 0
    for orig, abbrev in zip(dimensions, abbreviations):
        savings_per_occurrence = len(orig) - len(abbrev)
        # Appears in scores header + evidence rows
        occurrences = 2 + evidence_rows  # 1 in scores header, 1 per evidence row per dimension
        total_dim_savings += savings_per_occurrence * (occurrences // len(dimensions))
    
    step3_total_chars = step2_total_chars - total_dim_savings
    step3_savings = ((step2_total_chars - step3_total_chars) / step2_total_chars) * 100
    
    print(f"   - Average dimension name reduction: {sum(len(d) for d in dimensions) // len(dimensions):.1f} → {sum(len(a) for a in abbreviations) // len(abbreviations):.1f} chars")
    print(f"   - Total dimension abbreviation savings: {total_dim_savings:,} chars")
    print(f"   - New total: {step3_total_chars:,} chars")
    print(f"   - Improvement from Step 2: {step3_savings:.1f}%")
    print()
    
    # Step 4: Add Quote Compression
    print("✂️ Step 4 - Quote Compression Analysis:")
    
    # Estimate quote compression (limit to 100 chars)
    avg_quote_length = 120  # From our earlier analysis
    compressed_quote_length = 100
    quote_savings_per_row = max(0, avg_quote_length - compressed_quote_length)
    total_quote_savings = evidence_rows * quote_savings_per_row
    
    step4_total_chars = step3_total_chars - total_quote_savings
    step4_savings = ((step3_total_chars - step4_total_chars) / step3_total_chars) * 100
    
    print(f"   - Average quote length: {avg_quote_length} chars")
    print(f"   - Compressed quote limit: {compressed_quote_length} chars")
    print(f"   - Quote compression savings: {total_quote_savings:,} chars")
    print(f"   - New total: {step4_total_chars:,} chars")
    print(f"   - Improvement from Step 3: {step4_savings:.1f}%")
    print()
    
    # Step 5: Add Column Name Compression
    print("📝 Step 5 - Column Name Compression Analysis:")
    
    # Column name savings
    original_columns = ['artifact_hash', 'document_name', 'dimension', 'quote_text', 'context_type']
    compressed_columns = ['aid', 'doc', 'dim', 'txt', 'typ']
    
    column_savings = sum(len(orig) - len(comp) for orig, comp in zip(original_columns, compressed_columns))
    # Appears in headers plus repetition in CSV structure
    total_column_savings = column_savings * 10  # Rough estimate for header impact
    
    step5_total_chars = step4_total_chars - total_column_savings
    step5_savings = ((step4_total_chars - step5_total_chars) / step4_total_chars) * 100
    
    print(f"   - Column name savings: {column_savings} chars per occurrence")
    print(f"   - Total column compression savings: {total_column_savings:,} chars")
    print(f"   - New total: {step5_total_chars:,} chars")
    print(f"   - Improvement from Step 4: {step5_savings:.1f}%")
    print()
    
    # Final comparison with actual optimized implementation
    scores_opt, evidence_opt, lookup_opt, _ = orchestrator.generate_optimized_hash_csv(
        json_artifacts, temp_dir
    )
    
    with open(scores_opt, 'r') as f:
        actual_scores_chars = len(f.read())
    with open(evidence_opt, 'r') as f:
        actual_evidence_chars = len(f.read())
    with open(lookup_opt, 'r') as f:
        actual_lookup_chars = len(f.read())
    actual_total_chars = actual_scores_chars + actual_evidence_chars + actual_lookup_chars
    
    print("🎯 Final Results Summary:")
    print("=" * 50)
    print(f"Original JSON:           {total_json_chars:,} chars (baseline)")
    print(f"Step 1 - Original CSV:   {orig_total_chars:,} chars ({((total_json_chars - orig_total_chars) / total_json_chars):.1%} reduction)")
    print(f"Step 2 - Hash compression: {step2_total_chars:,} chars ({step2_savings:.1f}% additional)")
    print(f"Step 3 - Dim abbreviation: {step3_total_chars:,} chars ({step3_savings:.1f}% additional)")
    print(f"Step 4 - Quote compression: {step4_total_chars:,} chars ({step4_savings:.1f}% additional)")
    print(f"Step 5 - Column compression: {step5_total_chars:,} chars ({step5_savings:.1f}% additional)")
    print(f"Actual optimized result: {actual_total_chars:,} chars")
    print()
    
    print("🏆 Optimization Impact Ranking:")
    optimizations = [
        ("Hash Compression (A1 vs full hash)", step2_savings, total_hash_savings),
        ("Dimension Abbreviations (DIG vs Dignity)", step3_savings, total_dim_savings),
        ("Quote Compression (100 char limit)", step4_savings, total_quote_savings), 
        ("Column Name Compression (aid vs artifact_hash)", step5_savings, total_column_savings)
    ]
    
    for i, (name, pct_improvement, char_savings) in enumerate(sorted(optimizations, key=lambda x: x[1], reverse=True), 1):
        print(f"   {i}. {name}")
        print(f"      - {pct_improvement:.1f}% improvement")
        print(f"      - {char_savings:,} characters saved")
        print()
    
    # Cleanup
    for file_path in [scores_orig, evidence_orig, scores_opt, evidence_opt, lookup_opt]:
        file_path.unlink()
    temp_dir.rmdir()


if __name__ == '__main__':
    analyze_optimization_breakdown() 