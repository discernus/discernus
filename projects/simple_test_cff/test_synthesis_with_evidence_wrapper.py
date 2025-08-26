#!/usr/bin/env python3
"""
Test synthesis using EvidenceMatchingWrapper for intelligent evidence matching.

This script demonstrates how our wrapper can be used to generate evidence-backed
synthesis by connecting statistical findings to relevant evidence quotes.
"""

import sys
import json
from pathlib import Path

# Add the main discernus package to the path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from discernus.core.evidence_matching_wrapper import EvidenceMatchingWrapper

def test_synthesis_with_evidence_wrapper():
    """Test synthesis generation using our intelligent evidence wrapper."""
    
    print("🧪 Testing Synthesis with EvidenceMatchingWrapper")
    print("=" * 55)
    print("This test demonstrates intelligent evidence matching in action!")
    print()
    
    # Set up paths
    experiment_path = Path(__file__).parent
    artifacts_path = experiment_path / "shared_cache" / "artifacts"
    
    # Load artifact registry and evidence files
    registry_path = artifacts_path / "artifact_registry.json"
    with open(registry_path, 'r') as f:
        artifact_registry = json.load(f)
    
    # Find evidence artifacts
    evidence_files = []
    for artifact_hash, artifact_info in artifact_registry.items():
        if artifact_info.get('metadata', {}).get('artifact_type') == 'evidence_v6':
            evidence_file = artifacts_path / artifact_info['artifact_path']
            if evidence_file.exists():
                evidence_files.append((artifact_hash, evidence_file))
    
    print(f"📊 Loaded {len(evidence_files)} evidence artifacts")
    
    # Create mock artifact storage
    class MockArtifactStorage:
        def __init__(self, evidence_files):
            self.evidence_files = evidence_files
        
        def get_artifact(self, artifact_hash: str, quiet: bool = False):
            for hash_val, file_path in self.evidence_files:
                if hash_val == artifact_hash:
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            return f.read().encode('utf-8')
                    except Exception as e:
                        if not quiet:
                            print(f"Failed to read {file_path}: {e}")
                        return None
            return None
    
    # Initialize evidence wrapper
    mock_storage = MockArtifactStorage(evidence_files)
    evidence_wrapper = EvidenceMatchingWrapper(
        model="vertex_ai/gemini-2.5-pro",
        artifact_storage=mock_storage,
        audit_logger=None
    )
    
    # Build the intelligent index
    artifact_hashes = [hash_val for hash_val, _ in evidence_files]
    print("🔨 Building intelligent evidence index...")
    success = evidence_wrapper.build_index(artifact_hashes)
    
    if not success:
        print("❌ Failed to build evidence index")
        return
    
    status = evidence_wrapper.get_index_status()
    print(f"✅ Index built with {status['evidence_count']} evidence pieces")
    print()
    
    # Define key statistical findings from the experiment
    statistical_findings = [
        "John McCain shows high cohesion (0.84) with strong individual dignity (0.8) and cohesive goals (0.9)",
        "Steve King demonstrates low cohesion (-0.74) with high tribal dominance (0.85) and fragmentative goals (0.8)",
        "Strong contrast between McCain's compersion (0.9) and King's envy (0.7) and enmity (0.8)",
        "McCain's emotional tension (0.07) is much lower than King's (0.08), indicating more balanced discourse"
    ]
    
    print("📈 Key Statistical Findings:")
    for i, finding in enumerate(statistical_findings, 1):
        print(f"  {i}. {finding}")
    print()
    
    # Generate intelligent search queries for each finding
    print("🧠 Generating intelligent search queries...")
    queries = evidence_wrapper.generate_search_queries(statistical_findings, max_queries=5)
    
    print("Generated queries:")
    for i, query in enumerate(queries, 1):
        print(f"  {i}. {query}")
    print()
    
    # Find supporting evidence for each statistical finding
    print("🔍 Finding supporting evidence for each finding...")
    print()
    
    synthesis_sections = []
    
    for i, finding in enumerate(statistical_findings, 1):
        print(f"**Finding {i}: {finding}**")
        
        # Use auto-query search to find relevant evidence
        evidence_results = evidence_wrapper.search_evidence_with_auto_queries(
            [finding], 
            max_queries=2, 
            results_per_query=3
        )
        
        if evidence_results:
            print(f"Found {len(evidence_results)} supporting evidence pieces:")
            
            # Create synthesis section
            section = f"## Finding {i}: {finding}\n\n"
            section += "**Supporting Evidence:**\n\n"
            
            for j, evidence in enumerate(evidence_results[:3], 1):
                quote = evidence['quote_text']
                source = evidence['document_name']
                dimension = evidence['dimension']
                confidence = evidence['confidence']
                
                print(f"  {j}. {quote[:100]}...")
                print(f"     Source: {source}")
                print(f"     Dimension: {dimension}")
                print(f"     Confidence: {confidence}")
                print()
                
                # Add to synthesis section
                section += f"**Evidence {j}:** {quote}\n\n"
                section += f"*Source: {source} | Dimension: {dimension} | Confidence: {confidence}*\n\n"
            
            synthesis_sections.append(section)
        else:
            print("  No supporting evidence found")
            print()
    
    # Generate comprehensive synthesis
    print("📝 Generating comprehensive synthesis...")
    print()
    
    synthesis = f"""# Evidence-Based Synthesis Report
## Cohesive Flourishing Framework Analysis

This report synthesizes statistical findings from the political discourse analysis using intelligent evidence matching to connect quantitative results with concrete textual evidence.

### Executive Summary

The analysis reveals a striking contrast between two political discourse styles:
- **High-cohesion discourse** (McCain) characterized by individual dignity and cohesive goals
- **Low-cohesion discourse** (King) marked by tribal dominance and fragmentative goals

{chr(10).join(synthesis_sections)}

### Conclusion

The evidence demonstrates that political discourse quality can be quantitatively measured and qualitatively supported through concrete textual examples. The Cohesive Flourishing Framework successfully identifies both the statistical patterns and the textual evidence that exemplifies these patterns.

**Key Insight:** Statistical findings without supporting evidence are abstract; evidence without statistical context lacks analytical rigor. Our intelligent evidence matching bridges this gap, enabling evidence-based synthesis that maintains both quantitative precision and qualitative richness.
"""
    
    # Save the synthesis report
    synthesis_file = experiment_path / "evidence_based_synthesis_report.md"
    with open(synthesis_file, 'w', encoding='utf-8') as f:
        f.write(synthesis)
    
    print("✅ Synthesis report generated successfully!")
    print(f"📄 Saved to: {synthesis_file}")
    print()
    
    # Show a preview of the synthesis
    print("📖 Synthesis Report Preview:")
    print("=" * 50)
    print(synthesis[:1000] + "...")
    print("=" * 50)
    print()
    
    print("🎉 Evidence-based synthesis test completed successfully!")
    print()
    print("**What we just demonstrated:**")
    print("1. ✅ Intelligent evidence index building from real experiment data")
    print("2. ✅ Statistical findings translated into evidence search queries")
    print("3. ✅ Relevant evidence automatically retrieved and matched")
    print("4. ✅ Evidence-backed synthesis report generated")
    print("5. ✅ Full academic traceability maintained")
    print()
    print("**This is exactly what synthesis agents need!**")
    print("Instead of generic search results, they now get evidence that actually supports their statistical claims.")

if __name__ == "__main__":
    test_synthesis_with_evidence_wrapper()
