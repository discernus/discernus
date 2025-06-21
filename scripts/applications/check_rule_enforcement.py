#!/usr/bin/env python3
"""
Rule Enforcement Status Check

Quick verification that all AI assistant rule enforcement mechanisms 
are in place and functioning correctly.

Usage:
    python3 scripts/production/check_rule_enforcement.py
"""

import sys
from pathlib import Path

def check_file_exists(file_path, description):
    """Check if a required file exists."""
    path = Path(file_path)
    exists = path.exists()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {file_path}")
    return exists

def check_directory_exists(dir_path, description):
    """Check if a required directory exists."""
    path = Path(dir_path)
    exists = path.exists() and path.is_dir()
    status = "✅" if exists else "❌"
    print(f"{status} {description}: {dir_path}")
    return exists

def check_content_exists(file_path, search_text, description):
    """Check if specific content exists in a file."""
    try:
        path = Path(file_path)
        if not path.exists():
            print(f"❌ {description}: File {file_path} not found")
            return False
        
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        has_content = search_text in content
        status = "✅" if has_content else "❌"
        print(f"{status} {description}: Found in {file_path}")
        return has_content
        
    except Exception as e:
        print(f"❌ {description}: Error reading {file_path} - {e}")
        return False

def main():
    """Main status check function."""
    print("🛡️ AI ASSISTANT RULE ENFORCEMENT STATUS CHECK")
    print("=" * 60)
    
    all_good = True
    
    # 1. Core rule files
    print("\n📋 Core Rule Files:")
    all_good &= check_file_exists(".cursorrules", "Cursor AI Rules")
    all_good &= check_file_exists(".ai_assistant_rules.md", "AI Assistant Rules")
    all_good &= check_file_exists("DEVELOPMENT.md", "Development Guide")
    all_good &= check_file_exists(".ai_search_exclusions", "Search Exclusions")
    
    # 2. Documentation files
    print("\n📚 Documentation:")
    all_good &= check_file_exists("docs/EXISTING_SYSTEMS_INVENTORY.md", "Systems Inventory")
    all_good &= check_file_exists("docs/CODE_ORGANIZATION_STANDARDS.md", "Organization Standards")
    
    # 3. Production tools
    print("\n🔧 Production Tools:")
    all_good &= check_file_exists("scripts/production/check_existing_systems.py", "Production Search Tool")
    all_good &= check_file_exists("scripts/production/validate_ai_assistant_compliance.py", "Compliance Validator")
    all_good &= check_file_exists("scripts/production/new_development_workflow.py", "Guided Workflow")
    all_good &= check_file_exists("scripts/production/audit_code_organization.py", "Organization Auditor")
    
    # 4. Directory structure
    print("\n📁 Directory Structure:")
    all_good &= check_directory_exists("experimental/prototypes", "Experimental Prototypes")
    all_good &= check_directory_exists("sandbox", "Sandbox Directory")
    all_good &= check_directory_exists("deprecated", "Deprecated Code")
    all_good &= check_directory_exists("scripts/production", "Production Scripts")
    
    # 5. Content checks - warnings in production code
    print("\n🚨 Production Code Warnings:")
    all_good &= check_content_exists(
        "src/narrative_gravity/utils/llm_quality_assurance.py",
        "AI ASSISTANT WARNING",
        "QA System Warning"
    )
    all_good &= check_content_exists(
        "src/narrative_gravity/development/quality_assurance.py", 
        "AI ASSISTANT WARNING",
        "Component QA Warning"
    )
    
    # 6. Deprecated system moved
    print("\n🗑️ Deprecated Systems:")
    deprecated_moved = not Path("scripts/architectural_compliance_validator.py").exists()
    status = "✅" if deprecated_moved else "❌"
    print(f"{status} Deprecated AI Academic Advisor moved from scripts/")
    all_good &= deprecated_moved
    
    # 7. README warnings
    print("\n📖 README Integration:")
    all_good &= check_content_exists(
        "README.md",
        "BEFORE BUILDING ANYTHING NEW",
        "README Warning Section"
    )
    
    # Overall status
    print("\n" + "=" * 60)
    if all_good:
        print("🎉 ALL RULE ENFORCEMENT MECHANISMS IN PLACE!")
        print("✅ Future AI assistants should automatically follow rules")
        print("\n🎯 Quick test commands:")
        print("python3 scripts/production/check_existing_systems.py 'quality assurance'")
        print("python3 scripts/production/validate_ai_assistant_compliance.py --quick-check")
    else:
        print("❌ SOME ENFORCEMENT MECHANISMS MISSING!")
        print("⚠️  Rule enforcement may not be complete")
        print("🔧 Review the failed checks above and fix missing components")
    
    print(f"\n📊 Status: {sum(1 for _ in [True]) if all_good else 'INCOMPLETE'}")
    return 0 if all_good else 1

if __name__ == "__main__":
    sys.exit(main()) 