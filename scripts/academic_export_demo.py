#!/usr/bin/env python3
"""
Database-First Academic Export Demo

Demonstrates the enhanced PostgreSQL-first architecture with comprehensive
exports for academic statistical analysis tools.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent.parent))

def demo_database_architecture():
    """Demonstrate database-first architecture"""
    print("🗄️ DATABASE-FIRST ARCHITECTURE DEMO")
    print("=" * 60)
    
    # Initialize logger (will auto-detect PostgreSQL vs SQLite)
    from src.utils.statistical_logger import StatisticalLogger
    
    # Try PostgreSQL first, fallback to SQLite
    logger = StatisticalLogger(prefer_postgresql=True)
    
    print("\n📊 CORPUS STATISTICS:")
    stats = logger.get_corpus_stats()
    print(f"   Total Analyses: {stats.get('total_runs', 0)}")
    print(f"   Unique Models: {stats.get('unique_models', 0)}")
    print(f"   Total Cost: ${stats.get('total_cost', 0):.4f}")
    
    if stats.get('total_runs', 0) == 0:
        print("   ⚠️ No data in database yet. Run some analyses first!")
        return
    
    print("\n🎓 ACADEMIC EXPORT FORMATS:")
    
    # Export for different academic workflows
    export_results = logger.export_for_academics(
        export_format="all",
        output_dir="exports/academic_formats/",
        include_raw_responses=False  # Exclude for faster processing
    )
    
    print("\n📂 EXPORTED FILES:")
    for format_name, files in export_results.items():
        print(f"\n   {format_name.upper()}:")
        if isinstance(files, dict):
            for file_type, filepath in files.items():
                print(f"     {file_type}: {filepath}")
        else:
            print(f"     {files}")
    
    print("\n🔍 DATABASE QUERY CAPABILITIES:")
    
    # Demonstrate advanced querying
    claude_responses = logger.get_full_response_corpus(filters={
        'model_name': 'claude-3-5-sonnet-20241022'
    })
    print(f"   Claude responses: {len(claude_responses)}")
    
    expensive_analyses = logger.get_full_response_corpus(filters={
        'min_cost': 0.01
    })
    print(f"   High-cost analyses: {len(expensive_analyses)}")
    
    print("\n✅ Database-first architecture provides:")
    print("   • Single source of truth (no scattered JSON files)")
    print("   • Direct connectivity to Looker, Tableau, etc.")
    print("   • Native academic format exports")
    print("   • Full raw response corpus for analysis")
    print("   • Enterprise-grade PostgreSQL backend")

def demo_looker_compatibility():
    """Show how this connects to business intelligence tools"""
    print("\n🔍 BUSINESS INTELLIGENCE COMPATIBILITY")
    print("=" * 60)
    
    print("PostgreSQL Connection String for Looker:")
    print("   Host: localhost")
    print("   Database: narrative_gravity")
    print("   Schema: public")
    print("   Tables: jobs, runs, variance_stats, performance_metrics")
    
    print("\nKey Looker Dimensions & Measures:")
    print("   Dimensions: speaker, model_name, framework, timestamp")
    print("   Measures: total_cost, success_rate, variance, duration")
    print("   Advanced: JSONB fields for well scores and parameters")
    
    print("\nSample Looker SQL:")
    print('''
    SELECT 
        speaker,
        model_name,
        AVG(total_cost) as avg_cost,
        AVG(successful_runs::float / total_runs) as success_rate,
        COUNT(*) as job_count
    FROM jobs 
    WHERE timestamp >= '2025-01-01'
    GROUP BY speaker, model_name
    ORDER BY success_rate DESC;
    ''')

if __name__ == "__main__":
    demo_database_architecture()
    demo_looker_compatibility() 