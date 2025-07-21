#!/usr/bin/env python3
"""
Execute Framework Migration
==========================

Simple script to migrate all v3.2 frameworks to v4.0 format.
"""

import subprocess
import sys
from pathlib import Path

def run_migration():
    """Execute the framework migration."""
    
    frameworks_dir = Path("/Volumes/code/discernus/pm/frameworks")
    migrator_script = frameworks_dir / "framework_migrator.py"
    
    if not migrator_script.exists():
        print(f"❌ Migration script not found: {migrator_script}")
        return False
    
    try:
        print("🚀 Executing framework migration...")
        result = subprocess.run([
            sys.executable, str(migrator_script)
        ], cwd=str(frameworks_dir), capture_output=True, text=True)
        
        print("STDOUT:")
        print(result.stdout)
        
        if result.stderr:
            print("STDERR:")
            print(result.stderr)
        
        if result.returncode == 0:
            print("✅ Migration completed successfully!")
            return True
        else:
            print(f"❌ Migration failed with return code: {result.returncode}")
            return False
            
    except Exception as e:
        print(f"❌ Error running migration: {e}")
        return False

if __name__ == "__main__":
    success = run_migration()
    sys.exit(0 if success else 1)
