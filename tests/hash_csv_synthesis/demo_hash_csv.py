#!/usr/bin/env python3
"""
Demo script for Hash Cross-Referenced CSV generation.

Shows the practical token efficiency gains achieved by the Hash CSV approach.
"""

import sys
import os
from pathlib import Path
import json

# Add the project root to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from discernus.core.synthesis_orchestrator import SynthesisOrchestrator


def measure_token_efficiency():
    """Demonstrate token efficiency gains with Hash CSV approach."""
    
    print("🔍 Hash Cross-Referenced CSV Token Efficiency Demo")
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
    
    print(f"📏 Original JSON Size:")
    print(f"   - Total characters: {total_json_chars:,}")
    print(f"   - Average per artifact: {total_json_chars // len(json_artifacts):,}")
    print()
    
    # Generate Hash CSV files
    print("🔄 Generating Hash Cross-Referenced CSV files...")
    temp_dir = Path("/tmp/hash_csv_demo")
    temp_dir.mkdir(exist_ok=True)
    
    scores_path, evidence_path, quarantined = orchestrator.generate_hash_cross_referenced_csv(
        json_artifacts, temp_dir
    )
    
    # Measure CSV sizes
    scores_size = scores_path.stat().st_size
    evidence_size = evidence_path.stat().st_size
    total_csv_size = scores_size + evidence_size
    
    with open(scores_path, 'r', encoding='utf-8') as f:
        scores_content = f.read()
        scores_chars = len(scores_content)
    
    with open(evidence_path, 'r', encoding='utf-8') as f:
        evidence_content = f.read()
        evidence_chars = len(evidence_content)
    
    total_csv_chars = scores_chars + evidence_chars
    
    print(f"✅ Hash CSV Generation Complete:")
    print(f"   - Scores CSV: {scores_path.name}")
    print(f"     - Size: {scores_size:,} bytes ({scores_chars:,} chars)")
    print(f"   - Evidence CSV: {evidence_path.name}")
    print(f"     - Size: {evidence_size:,} bytes ({evidence_chars:,} chars)")
    print(f"   - Quarantined: {len(quarantined)} artifacts")
    print()
    
    # Calculate efficiency gains
    reduction_ratio = (total_json_chars - total_csv_chars) / total_json_chars
    compression_ratio = total_json_chars / total_csv_chars
    
    print(f"🎯 Token Efficiency Analysis:")
    print(f"   - Original JSON: {total_json_chars:,} characters")
    print(f"   - Hash CSV total: {total_csv_chars:,} characters")
    print(f"   - Reduction: {reduction_ratio:.1%}")
    print(f"   - Compression ratio: {compression_ratio:.1f}x")
    print()
    
    # Show CSV content samples
    print("📋 Sample CSV Content:")
    print()
    print("🔢 Scores CSV (first 3 lines):")
    scores_lines = scores_content.split('\n')[:3]
    for i, line in enumerate(scores_lines):
        if len(line) > 100:
            line = line[:97] + "..."
        print(f"   {i+1}: {line}")
    print()
    
    print("📝 Evidence CSV (first 5 lines):")
    evidence_lines = evidence_content.split('\n')[:5]
    for i, line in enumerate(evidence_lines):
        if len(line) > 100:
            line = line[:97] + "..."
        print(f"   {i+1}: {line}")
    print()
    
    # Synthesis implications
    estimated_tokens_json = total_json_chars // 4  # Rough token estimate
    estimated_tokens_csv = total_csv_chars // 4
    
    print(f"🧠 Synthesis Agent Implications:")
    print(f"   - Estimated JSON tokens: ~{estimated_tokens_json:,}")
    print(f"   - Estimated CSV tokens: ~{estimated_tokens_csv:,}")
    print(f"   - Token reduction: ~{((estimated_tokens_json - estimated_tokens_csv) / estimated_tokens_json):.1%}")
    
    if estimated_tokens_json > 6000:
        print(f"   ⚠️  Original JSON would exceed 6K token limit")
    if estimated_tokens_csv <= 6000:
        print(f"   ✅ CSV approach stays within synthesis limits")
    
    print()
    print("🎯 Conclusion:")
    print(f"   The Hash Cross-Referenced CSV approach achieves {reduction_ratio:.1%} token reduction")
    print(f"   while preserving both statistical rigor and evidence grounding capability.")
    
    # Cleanup
    scores_path.unlink()
    evidence_path.unlink()
    temp_dir.rmdir()


if __name__ == '__main__':
    measure_token_efficiency() 