#!/usr/bin/env python3
"""
MVA Project Migration to Provenance Specification v3.0
======================================================

Migrates the MVA project from mixed organizational patterns to the 
Research Provenance Guide v3.0 standard structure.

Current structure:
projects/MVA/
├── PROJECT_CHRONOLOG_MVA.jsonl ✅
├── experiment_1/ (legacy root level)
│   ├── experiment.md
│   ├── cff_v4_mva.md  
│   ├── corpus/
│   ├── results/{timestamp}/
│   └── conversations/
├── experiment_2/ (similar structure)
└── experiments/experiment_3/ (already mostly compliant)

Target structure:
projects/MVA/
├── PROJECT_CHRONOLOG_MVA.jsonl ✅  
└── experiments/
    ├── experiment_1/
    │   ├── experiment_snapshot.md
    │   ├── framework_snapshot.md
    │   ├── corpus_manifest.json
    │   └── sessions/{SESSION_ID}/
    │       ├── SESSION_CHRONOLOG.jsonl
    │       ├── llm_archive/
    │       ├── analysis_results/ 
    │       ├── system_state/
    │       └── fault_recovery/
    ├── experiment_2/ (same structure)
    └── experiment_3/ (clean up extras)
"""

import os
import json
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Tuple
import re

class MVAMigrator:
    def __init__(self, base_path: str = "projects/MVA"):
        self.base_path = Path(base_path)
        self.backup_path = Path(f"{base_path}_backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        self.dry_run = True  # Safety first!
        
    def migrate_experiment(self, experiment_name: str) -> bool:
        """Migrate a single experiment to provenance specification."""
        print(f"\n=== Migrating {experiment_name} ===")
        
        # Source paths (current structure)
        source_path = self.base_path / experiment_name
        target_path = self.base_path / "experiments" / experiment_name
        
        if not source_path.exists():
            print(f"❌ Source path does not exist: {source_path}")
            return False
            
        if experiment_name == "experiments":
            # experiment_3 is already in experiments/ - handle separately
            return self.clean_experiment_3()
            
        print(f"📁 Source: {source_path}")
        print(f"📁 Target: {target_path}")
        
        # Analyze current structure
        sessions = self.discover_sessions(source_path)
        print(f"📊 Found {len(sessions)} sessions")
        
        if not self.dry_run:
            # Create target directory structure
            target_path.mkdir(parents=True, exist_ok=True)
            
            # Migrate snapshots
            self.migrate_snapshots(source_path, target_path, experiment_name)
            
            # Generate corpus manifest
            self.create_corpus_manifest(source_path, target_path)
            
            # Migrate sessions
            self.migrate_sessions(source_path, target_path, sessions)
            
        return True
        
    def discover_sessions(self, source_path: Path) -> Dict[str, Dict]:
        """Discover all sessions by analyzing results and conversations."""
        sessions = {}
        
        # Session directories from results/
        results_path = source_path / "results"
        if results_path.exists():
            for session_dir in results_path.iterdir():
                if session_dir.is_dir() and re.match(r'\d{4}-\d{2}-\d{2}_\d{2}-\d{2}-\d{2}', session_dir.name):
                    session_id = session_dir.name
                    sessions[session_id] = {
                        'timestamp': session_id,
                        'system_state_path': session_dir,
                        'conversations': [],
                        'has_state': True
                    }
                    
        # Conversation files
        conversations_path = source_path / "conversations"  
        if conversations_path.exists():
            for conv_file in conversations_path.glob("*.jsonl"):
                # Extract timestamp from filename: conversation_20250717_124053_42451b8d.jsonl
                match = re.search(r'(\d{8})_(\d{6})', conv_file.name)
                if match:
                    date_str, time_str = match.groups()
                    # Convert to session format: 2025-07-17_12-40-53
                    session_id = f"{date_str[:4]}-{date_str[4:6]}-{date_str[6:8]}_{time_str[:2]}-{time_str[2:4]}-{time_str[4:6]}"
                    
                    if session_id not in sessions:
                        sessions[session_id] = {
                            'timestamp': session_id,
                            'system_state_path': None,
                            'conversations': [],
                            'has_state': False
                        }
                    sessions[session_id]['conversations'].append(conv_file)
                    
        return sessions
        
    def migrate_snapshots(self, source_path: Path, target_path: Path, experiment_name: str):
        """Create snapshot files from original experiment and framework files."""
        
        # Find experiment file
        experiment_files = list(source_path.glob("experiment*.md"))
        if experiment_files:
            shutil.copy2(experiment_files[0], target_path / "experiment_snapshot.md")
            print(f"📝 Copied {experiment_files[0].name} → experiment_snapshot.md")
            
        # Find framework file  
        framework_files = list(source_path.glob("*.md"))
        framework_files = [f for f in framework_files if not f.name.startswith("experiment")]
        if framework_files:
            shutil.copy2(framework_files[0], target_path / "framework_snapshot.md")  
            print(f"📝 Copied {framework_files[0].name} → framework_snapshot.md")
            
    def create_corpus_manifest(self, source_path: Path, target_path: Path):
        """Generate corpus_manifest.json from corpus directory."""
        corpus_path = source_path / "corpus"
        if not corpus_path.exists():
            return
            
        manifest = {
            "manifest_version": "2.0",
            "created": datetime.now().isoformat(),
            "corpus_state": "original", # Default assumption
            "total_files": 0,
            "file_list": []
        }
        
        for file_path in corpus_path.rglob("*"):
            if file_path.is_file() and not file_path.name.startswith('.'):
                manifest["file_list"].append({
                    "name": file_path.name,
                    "relative_path": str(file_path.relative_to(corpus_path)),
                    "size_bytes": file_path.stat().st_size
                })
                manifest["total_files"] += 1
                
        with open(target_path / "corpus_manifest.json", 'w') as f:
            json.dump(manifest, f, indent=2)
            
        print(f"📄 Created corpus_manifest.json ({manifest['total_files']} files)")
        
    def migrate_sessions(self, source_path: Path, target_path: Path, sessions: Dict):
        """Migrate all sessions to provenance spec structure."""
        sessions_path = target_path / "sessions"
        sessions_path.mkdir(exist_ok=True)
        
        for session_id, session_data in sessions.items():
            session_path = sessions_path / session_id
            session_path.mkdir(exist_ok=True)
            
            print(f"  📁 Session: {session_id}")
            
            # Create directory structure
            (session_path / "llm_archive").mkdir(exist_ok=True)
            (session_path / "analysis_results").mkdir(exist_ok=True)  
            (session_path / "system_state").mkdir(exist_ok=True)
            (session_path / "fault_recovery").mkdir(exist_ok=True)
            
            # Migrate LLM archive (conversations)
            for conv_file in session_data['conversations']:
                shutil.copy2(conv_file, session_path / "llm_archive" / conv_file.name)
                
            # Migrate system state
            if session_data['system_state_path'] and session_data['system_state_path'].exists():
                for state_file in session_data['system_state_path'].iterdir():
                    if state_file.is_file():
                        shutil.copy2(state_file, session_path / "system_state" / state_file.name)
                        
            # Create SESSION_CHRONOLOG.jsonl
            self.create_session_chronolog(session_path, session_id, session_data)
            
    def create_session_chronolog(self, session_path: Path, session_id: str, session_data: Dict):
        """Generate SESSION_CHRONOLOG.jsonl for the session."""
        chronolog_path = session_path / "SESSION_CHRONOLOG.jsonl"
        
        events = [
            {
                "timestamp": f"{session_id.replace('_', 'T').replace('-', ':')}Z",
                "event": "session_start", 
                "session_id": session_id,
                "migration_note": "Migrated from legacy structure"
            },
            {
                "timestamp": f"{session_id.replace('_', 'T').replace('-', ':')}Z",
                "event": "migration_complete",
                "conversations_migrated": len(session_data['conversations']),
                "system_state_migrated": session_data['has_state']
            }
        ]
        
        with open(chronolog_path, 'w') as f:
            for event in events:
                f.write(json.dumps(event) + '\n')
                
        print(f"    📝 Created SESSION_CHRONOLOG.jsonl")
        
    def clean_experiment_3(self) -> bool:
        """Clean up experiment_3 which is already mostly compliant."""
        exp3_path = self.base_path / "experiments" / "experiment_3"
        if not exp3_path.exists():
            print("❌ experiment_3 not found in experiments/ directory")
            return False
            
        print("\n=== Cleaning up experiment_3 ===")
        
        # Move extra directories to sessions if they don't belong at root
        extra_dirs = ['logs', 'results', 'conversations']
        sessions_path = exp3_path / "sessions"
        
        if not sessions_path.exists():
            print("ℹ️ No sessions directory in experiment_3 - structure already clean")
            return True
            
        for extra_dir in extra_dirs:
            extra_path = exp3_path / extra_dir
            if extra_path.exists():
                print(f"🧹 Found extra directory: {extra_dir}")
                if not self.dry_run:
                    # This would need more sophisticated logic to properly organize
                    # these into the correct session directories
                    print(f"    ⚠️ Manual review needed for {extra_dir}")
                    
        return True
        
    def create_backup(self) -> bool:
        """Create full backup before migration."""
        if self.dry_run:
            print(f"🔄 DRY RUN: Would create backup at {self.backup_path}")
            return True
            
        try:
            shutil.copytree(self.base_path, self.backup_path)
            print(f"💾 Backup created: {self.backup_path}")
            return True
        except Exception as e:
            print(f"❌ Backup failed: {e}")
            return False
            
    def run_migration(self, confirm: bool = False):
        """Run the complete migration process."""
        print("🚀 MVA Project Migration to Provenance Specification v3.0")
        print("=" * 60)
        
        if not self.base_path.exists():
            print(f"❌ Base path does not exist: {self.base_path}")
            return False
            
        self.dry_run = not confirm
        
        if self.dry_run:
            print("🔍 DRY RUN MODE - No changes will be made")
        else:
            print("⚠️ LIVE MODE - Changes will be made to filesystem")
            
        # Create backup
        if not self.create_backup():
            return False
            
        # Migrate experiments
        experiments_to_migrate = []
        for item in self.base_path.iterdir():
            if item.is_dir() and item.name.startswith("experiment"):
                experiments_to_migrate.append(item.name)
                
        print(f"\n📊 Found experiments to migrate: {experiments_to_migrate}")
        
        for experiment in experiments_to_migrate:
            success = self.migrate_experiment(experiment)
            if not success:
                print(f"❌ Failed to migrate {experiment}")
                return False
                
        print("\n✅ Migration analysis complete!")
        
        if self.dry_run:
            print("\nTo execute migration, run with confirm=True:")
            print("python3 scripts/migrate_mva_to_provenance_spec.py --confirm")
        else:
            print(f"\n💾 Original data backed up to: {self.backup_path}")
            print("✅ Migration complete! Verify results and remove backup when satisfied.")
            
        return True

def main():
    import sys
    confirm = "--confirm" in sys.argv
    
    migrator = MVAMigrator()
    success = migrator.run_migration(confirm=confirm)
    
    if success:
        print("\n🎉 Migration process completed successfully!")
    else:
        print("\n💥 Migration process failed!")
        sys.exit(1)

if __name__ == "__main__":
    main() 