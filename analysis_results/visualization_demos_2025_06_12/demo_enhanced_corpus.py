#!/usr/bin/env python3
"""
Enhanced Corpus Management System Demonstration

Tests the new corpus management system with:
- Stable identifiers and URIs
- FAIR data compliance
- Academic standards
- Discovery and validation tools
"""

import sys
from pathlib import Path
from datetime import datetime

# Add project root to path for imports
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.narrative_gravity.corpus import (
    CorpusRegistry, CorpusValidator, CorpusDiscovery, CorpusExporter
)


def demo_corpus_registration():
    """Demonstrate corpus registration with stable identifiers."""
    print("🔗 Enhanced Corpus Registration Demo")
    print("=" * 50)
    
    registry = CorpusRegistry()
    
    # Register a sample document with proper metadata
    obama_file = Path("corpus/golden_set/presidential_speeches/txt/golden_obama_inaugural_01.txt")
    
    if obama_file.exists():
        try:
            # Register with enhanced metadata
            doc = registry.register_document(
                file_path=obama_file,
                title="First Inaugural Address",
                author="Barack Obama", 
                date=datetime(2009, 1, 20),
                document_type="inaugural",
                publication="Presidential Inaugural Addresses",
                medium="speech",
                source_url="https://www.presidency.ucsb.edu/documents/inaugural-address-44th-president-united-states",
                document_metadata={
                    "historical_significance": "First African American President",
                    "word_count": 2395,
                    "famous_quotes": ["Yes we can", "Change has come to America"]
                }
            )
            
            print(f"✅ Registered document:")
            print(f"   Text ID: {doc.text_id}")
            print(f"   URI: {doc.uri}")
            print(f"   Content Hash: {doc.content_hash[:16]}...")
            print(f"   File Size: {doc.file_size} bytes")
            print(f"   Registered: {doc.registered_at}")
            
        except Exception as e:
            print(f"❌ Registration failed: {e}")
    else:
        print(f"⚠️  Sample file not found: {obama_file}")
    
    print()


def demo_corpus_validation():
    """Demonstrate corpus validation and FAIR compliance."""
    print("🔍 Corpus Validation & FAIR Compliance Demo")
    print("=" * 50)
    
    validator = CorpusValidator()
    
    # Run comprehensive validation
    print("Running validation...")
    result = validator.validate_corpus()
    
    print(result.summary())
    
    # Check FAIR compliance
    print("Checking FAIR compliance...")
    fair_scores = validator.check_fair_compliance()
    
    print("🎯 FAIR Data Principles Compliance:")
    for principle, score in fair_scores.items():
        status = "✅" if score > 0.7 else "⚠️" if score > 0.4 else "❌"
        print(f"   {status} {principle.title()}: {score:.1%}")
    
    overall_score = sum(fair_scores.values()) / 4
    print(f"   📊 Overall FAIR Score: {overall_score:.1%}")
    
    print()


def demo_corpus_discovery():
    """Demonstrate corpus discovery and search tools."""
    print("🔍 Corpus Discovery & Search Demo")
    print("=" * 50)
    
    discovery = CorpusDiscovery()
    
    # Search examples
    print("1. Searching for 'freedom'...")
    results = discovery.search("freedom", limit=5)
    if results:
        print(f"Found {len(results)} matches:")
        for i, result in enumerate(results.top(3), 1):
            print(f"   {i}. {result.document.title} by {result.document.author}")
            print(f"      Score: {result.relevance_score:.3f}")
    else:
        print("   No matches found")
    
    print("\n2. Browse by document type...")
    doc_types = discovery.browse_by_facet('document_type')
    print("   Document types:")
    for doc_type, count in doc_types.items():
        print(f"     {doc_type}: {count}")
    
    print("\n3. Browse by author...")
    authors = discovery.browse_by_facet('author')
    print("   Authors:")
    for author, count in sorted(authors.items(), key=lambda x: x[1], reverse=True)[:5]:
        print(f"     {author}: {count}")
    
    print("\n4. Corpus statistics...")
    stats = discovery.get_corpus_statistics()
    print(stats.summary())
    
    print()


def demo_academic_export():
    """Demonstrate academic format exports."""
    print("📚 Academic Export Demo")  
    print("=" * 50)
    
    exporter = CorpusExporter()
    
    # Create temporary export directory
    export_dir = Path("tmp") / f"corpus_export_demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    export_dir.mkdir(parents=True, exist_ok=True)
    
    try:
        # Export research dataset
        print("Exporting research dataset...")
        exported_files = exporter.export_research_dataset(
            output_dir=export_dir,
            formats=['csv', 'json', 'r'],
            include_content=False,  # Skip content for demo speed
            include_analysis_code=True
        )
        
        print("✅ Exported files:")
        for format_name, file_path in exported_files.items():
            print(f"   {format_name}: {file_path}")
        
        # Generate citations
        print("\nGenerating citations...")
        registry = CorpusRegistry()
        documents = registry.list_documents()[:3]  # Just first 3 for demo
        
        if documents:
            citation_file = export_dir / "citations.txt"
            exporter.generate_citations(documents, style='apa', output_file=citation_file)
            print(f"✅ Citations generated: {citation_file}")
        
        print(f"\n📁 All exports saved to: {export_dir}")
        
    except Exception as e:
        print(f"❌ Export failed: {e}")
    
    print()


def demo_full_workflow():
    """Demonstrate complete enhanced corpus workflow."""
    print("🚀 Complete Enhanced Corpus Workflow Demo")
    print("=" * 60)
    
    # 1. Initialize components
    registry = CorpusRegistry()
    validator = CorpusValidator(registry)
    discovery = CorpusDiscovery(registry)
    exporter = CorpusExporter(registry)
    
    print("✅ Initialized enhanced corpus management system")
    
    # 2. Validate existing corpus
    print("\n📋 Validating corpus integrity...")
    validation = validator.validate_corpus()
    print(f"   Status: {'✅ VALID' if validation.is_valid else '❌ INVALID'}")
    print(f"   Documents: {validation.valid_documents}/{validation.total_documents} valid")
    
    # 3. Check academic standards
    print("\n🎓 Checking academic compliance...")
    fair_scores = validator.check_fair_compliance()
    overall_fair = sum(fair_scores.values()) / 4
    print(f"   FAIR Compliance: {overall_fair:.1%}")
    
    # 4. Demonstrate discovery
    print("\n🔍 Testing discovery capabilities...")
    stats = discovery.get_corpus_statistics()
    print(f"   Total documents: {stats.total_documents}")
    print(f"   Authors: {stats.total_authors}")
    print(f"   Time span: {stats.date_span_years:.1f} years")
    
    # 5. Generate compliance report
    print("\n📊 Generating compliance report...")
    report = validator.generate_compliance_report()
    report_file = Path("tmp/corpus_compliance_report.txt")
    report_file.parent.mkdir(exist_ok=True)
    report_file.write_text(report)
    print(f"   Report saved: {report_file}")
    
    print("\n🎉 Enhanced Corpus Management System demonstration complete!")
    print("\nKey improvements delivered:")
    print("  ✅ Stable text identifiers (placeholder URIs until web service)")
    print("  ✅ FAIR data principles compliance")
    print("  ✅ Academic metadata standards")
    print("  ✅ Integrity validation and monitoring")
    print("  ✅ Powerful discovery and search tools")
    print("  ✅ Research-ready export formats")
    print("  ✅ Replication package generation")


def main():
    """Run all demonstrations."""
    print("🎯 Narrative Gravity Wells - Enhanced Corpus Management")
    print("=" * 60)
    print(f"Demonstration started: {datetime.now()}")
    print()
    
    try:
        # Run individual demos
        demo_corpus_registration()
        demo_corpus_validation()
        demo_corpus_discovery()
        demo_academic_export()
        
        # Run complete workflow
        demo_full_workflow()
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
    
    print(f"\nDemonstration completed: {datetime.now()}")


if __name__ == "__main__":
    main() 