#!/usr/bin/env python3
"""
Auto-run migration for remaining 6 frameworks
"""

import subprocess
import sys
from pathlib import Path

def run_migration():
    """Execute the framework migration automatically."""
    
    frameworks_dir = Path("/Volumes/code/discernus/pm/frameworks")
    migrator_script = frameworks_dir / "framework_migrator.py"
    
    print("🚀 Auto-executing framework migration...")
    print("Processing all remaining v3.2 frameworks")
    print("=" * 50)
    
    try:
        # Import and run the migrator directly
        sys.path.insert(0, str(frameworks_dir))
        from framework_migrator import FrameworkMigrator
        
        migrator = FrameworkMigrator()
        
        # Discover frameworks
        frameworks = migrator.discover_v32_frameworks()
        
        # Filter out already migrated ones
        existing_v4 = []
        for existing in frameworks_dir.glob("*_v4.md"):
            existing_v4.append(existing.stem.replace('_v4', ''))
        
        print(f"Found {len(frameworks)} total v3.2 frameworks")
        print(f"Already migrated: {', '.join(existing_v4)}")
        
        # Execute migration
        results = migrator.migrate_all_frameworks()
        
        # Generate report
        report = migrator.generate_migration_report(results)
        report_path = frameworks_dir / "auto_migration_report.md"
        
        with open(report_path, 'w', encoding='utf-8') as f:
            f.write(report)
        
        print(f"\\n📋 Auto-migration report saved: {report_path}")
        
        # Summary
        successful = sum(results.values())
        total = len(results)
        print(f"\\n🎯 MIGRATION COMPLETE: {successful}/{total} frameworks migrated")
        
        return True
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
