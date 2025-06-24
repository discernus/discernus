#!/usr/bin/env python3
"""
Enhanced system discovery tool with provenance tracking information.
"""

import sys
import os
from pathlib import Path
import json
import hashlib
import sqlite3
from datetime import datetime

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

def check_existing_systems(functionality_query: str):
    """
    Check existing production systems and provide guidance on results organization.
    
    Enhanced with provenance tracking and workspace organization information.
    """
    print(f"🔍 Searching for existing systems: '{functionality_query}'")
    print("=" * 60)
    
    # Core production systems
    systems = {
        "Quality Assurance": {
            "system": "LLMQualityAssuranceSystem",
            "location": "src/analysis/llm_quality_assurance.py",
            "description": "6-layer mathematical validation system",
            "capabilities": [
                "Syntactic validation",
                "Semantic coherence checking", 
                "Statistical analysis",
                "Confidence scoring",
                "Bias detection",
                "Academic compliance"
            ]
        },
        "Component Validation": {
            "system": "ComponentQualityValidator", 
            "location": "src/utils/component_quality_validator.py",
            "description": "Component validation and registration",
            "capabilities": [
                "Framework validation",
                "Corpus validation", 
                "Prompt template validation",
                "Asset integrity checking"
            ]
        },
        "Academic Export": {
            "system": "QAEnhancedDataExporter",
            "location": "src/academic/qa_enhanced_data_exporter.py", 
            "description": "Academic export with quality assurance",
            "capabilities": [
                "CSV export with metadata",
                "Statistical summaries",
                "Quality metrics",
                "Academic documentation"
            ]
        },
        "Experiment Orchestration": {
            "system": "ComprehensiveExperimentOrchestrator",
            "location": "scripts/applications/comprehensive_experiment_orchestrator.py",
            "description": "Complete experiment execution pipeline",
            "capabilities": [
                "Experiment execution",
                "Results management", 
                "Enhanced analysis pipeline",
                "Provenance tracking",
                "Research workspace integration"
            ]
        },
        "System Health": {
            "system": "SystemHealthCheck",
            "location": "scripts/system_health_check.sh",
            "description": "Comprehensive system validation",
            "capabilities": [
                "Database connectivity",
                "Framework loading",
                "API validation",
                "Mock analysis testing",
                "Results generation"
            ]
        }
    }
    
    # Check which systems are relevant
    relevant_systems = []
    query_lower = functionality_query.lower()
    
    for system_name, system_info in systems.items():
        if (query_lower in system_name.lower() or 
            query_lower in system_info["description"].lower() or
            any(query_lower in cap.lower() for cap in system_info["capabilities"])):
            relevant_systems.append((system_name, system_info))
    
    if relevant_systems:
        print("✅ FOUND RELEVANT PRODUCTION SYSTEMS:")
        print()
        
        for system_name, system_info in relevant_systems:
            print(f"📦 {system_name}")
            print(f"   System: {system_info['system']}")
            print(f"   Location: {system_info['location']}")
            print(f"   Description: {system_info['description']}")
            print(f"   Capabilities:")
            for cap in system_info['capabilities']:
                print(f"     - {cap}")
            print()
    
    # Enhanced results organization information
    print("📁 RESULTS ORGANIZATION & PROVENANCE TRACKING:")
    print()
    print("🏥 System Health Results:")
    print("   Location: tests/system_health/results/")
    print("   Retention: Only most recent result kept")
    print("   Contents: HTML reports, visualizations, academic exports")
    print()
    print("🔬 Live Experiment Results:")
    print("   Location: {research_workspace}/results/")
    print("   Naming: {experiment}_{version}_{timestamp}_{run_hash}")
    print("   Provenance: Database run ID hash for audit trail")
    print("   Contents: Complete replication packages")
    print()
    print("🔗 Provenance Tracking Features:")
    print("   - Content-addressable storage")
    print("   - Hash-based integrity verification")
    print("   - Complete audit trails")
    print("   - Research workspace integration")
    print("   - Database run ID correlation")
    print()
    
    # Workspace setup guidance
    print("🚀 RECOMMENDED WORKFLOW:")
    print()
    print("1. System Health Check:")
    print("   ./scripts/system_health_check.sh basic")
    print("   Results → tests/system_health/results/")
    print()
    print("2. Live Experiments:")
    print("   python3 scripts/applications/comprehensive_experiment_orchestrator.py \\")
    print("     --experiment-config path/to/experiment.yaml \\")
    print("     --research-workspace path/to/workspace")
    print("   Results → workspace/results/{experiment}_{hash}/")
    print()
    print("3. Provenance Verification:")
    print("   - Check database run IDs in results folder names")
    print("   - Verify content hashes in .provenance.yaml files")
    print("   - Use replication packages for independent verification")
    print()
    
    if not relevant_systems:
        print("⚠️  NO DIRECT MATCHES FOUND")
        print()
        print("Consider using these general-purpose systems:")
        print("- ComprehensiveExperimentOrchestrator for most functionality")
        print("- LLMQualityAssuranceSystem for quality validation")
        print("- SystemHealthCheck for validation testing")
    
    print("=" * 60)
    print("✅ REMEMBER: Always check existing systems before building new ones!")
    print("📖 See ai_assistant_compliance_rules.md for complete guidance")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        check_existing_systems(query)
    else:
        print("Usage: python3 check_existing_systems.py <functionality_description>")
        print("Example: python3 check_existing_systems.py 'system health check'") 