#!/usr/bin/env python3
"""
Framework Synchronization Tool
Manages the relationship between filesystem frameworks (development) and database frameworks (source of truth).

Database = Source of Truth (used by application)
Filesystem = Development Workspace (for editing and testing)

Usage:
    python scripts/framework_sync.py status                    # Show sync status
    python scripts/framework_sync.py export [framework]        # Export DB -> filesystem
    python scripts/framework_sync.py import [framework]        # Import filesystem -> DB
    python scripts/framework_sync.py validate [framework]      # Validate framework files
    python scripts/framework_sync.py migrate-all              # Migrate all to v2.0
"""

import os
import sys
import json
import argparse
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple
import hashlib

# Add src to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.models.component_models import FrameworkVersion
from src.utils.database import get_database_url

class FrameworkSyncManager:
    """Manages synchronization between filesystem and database frameworks."""
    
    def __init__(self):
        self.engine = create_engine(get_database_url())
        self.Session = sessionmaker(bind=self.engine)
        self.frameworks_dir = Path("frameworks")
        
    def get_filesystem_frameworks(self) -> Dict[str, Dict]:
        """Get all frameworks from filesystem with metadata."""
        frameworks = {}
        
        if not self.frameworks_dir.exists():
            return frameworks
            
        for framework_dir in self.frameworks_dir.iterdir():
            if not framework_dir.is_dir():
                continue
                
            framework_name = framework_dir.name
            framework_file = framework_dir / "framework.json"
            
            if not framework_file.exists():
                continue
                
            try:
                with open(framework_file, 'r') as f:
                    framework_data = json.load(f)
                
                # Calculate file hash for change detection
                file_hash = self._calculate_framework_hash(framework_dir)
                
                frameworks[framework_name] = {
                    'path': framework_dir,
                    'data': framework_data,
                    'version': framework_data.get('version', 'unknown'),
                    'hash': file_hash,
                    'last_modified': framework_file.stat().st_mtime
                }
                
            except Exception as e:
                print(f"⚠️  Error reading {framework_name}: {e}")
                
        return frameworks
    
    def get_database_frameworks(self) -> Dict[str, FrameworkVersion]:
        """Get all frameworks from database."""
        session = self.Session()
        try:
            frameworks = {}
            db_frameworks = session.query(FrameworkVersion).all()
            
            for fw in db_frameworks:
                key = f"{fw.framework_name}:{fw.version}"
                frameworks[key] = fw
                
            return frameworks
        finally:
            session.close()
    
    def _calculate_framework_hash(self, framework_dir: Path) -> str:
        """Calculate hash of all framework files for change detection."""
        hasher = hashlib.sha256()
        
        # Hash all JSON files in order
        for filename in ['framework.json', 'dipoles.json', 'weights.json']:
            file_path = framework_dir / filename
            if file_path.exists():
                with open(file_path, 'rb') as f:
                    hasher.update(f.read())
                    
        return hasher.hexdigest()[:16]  # Short hash for display
    
    def show_status(self):
        """Show synchronization status between filesystem and database."""
        print("🔄 Framework Synchronization Status")
        print("=" * 50)
        
        fs_frameworks = self.get_filesystem_frameworks()
        db_frameworks = self.get_database_frameworks()
        
        print(f"\n📁 Filesystem: {len(fs_frameworks)} frameworks")
        print(f"🗄️  Database: {len(db_frameworks)} framework versions")
        
        # Show filesystem frameworks
        print(f"\n📁 Filesystem Frameworks (Development Workspace):")
        if not fs_frameworks:
            print("   (none)")
        else:
            for name, info in fs_frameworks.items():
                version = info['version']
                hash_short = info['hash']
                modified = datetime.fromtimestamp(info['last_modified']).strftime('%Y-%m-%d %H:%M')
                print(f"   📄 {name}:{version} (hash:{hash_short}, modified:{modified})")
        
        # Show database frameworks
        print(f"\n🗄️  Database Frameworks (Source of Truth):")
        if not db_frameworks:
            print("   (none)")
        else:
            for key, fw in db_frameworks.items():
                created = fw.created_at.strftime('%Y-%m-%d %H:%M') if fw.created_at else 'unknown'
                status_icon = "✅" if fw.validation_status == "validated" else "🟡" if fw.validation_status == "tested" else "⚪"
                print(f"   {status_icon} {key} ({fw.validation_status}, created:{created})")
        
        # Show sync analysis
        print(f"\n🔍 Sync Analysis:")
        self._analyze_sync_status(fs_frameworks, db_frameworks)
    
    def _analyze_sync_status(self, fs_frameworks: Dict, db_frameworks: Dict):
        """Analyze and report sync status between filesystem and database."""
        fs_names = set(fs_frameworks.keys())
        db_names = set(fw.framework_name for fw in db_frameworks.values())
        
        # Frameworks only in filesystem
        fs_only = fs_names - db_names
        if fs_only:
            print(f"   📁➡️🗄️  Only in filesystem (ready to import): {', '.join(fs_only)}")
        
        # Frameworks only in database
        db_only = db_names - fs_names
        if db_only:
            print(f"   🗄️➡️📁 Only in database (can export): {', '.join(db_only)}")
        
        # Frameworks in both - check versions
        common = fs_names & db_names
        if common:
            print(f"   🔄 In both locations:")
            for name in common:
                fs_version = fs_frameworks[name]['version']
                db_versions = [fw.version for fw in db_frameworks.values() if fw.framework_name == name]
                latest_db_version = max(db_versions) if db_versions else "none"
                
                if fs_version == latest_db_version:
                    print(f"      ✅ {name}: filesystem:{fs_version} = database:{latest_db_version}")
                else:
                    print(f"      ⚠️  {name}: filesystem:{fs_version} ≠ database:{latest_db_version}")
        
        if not fs_only and not db_only and all(
            fs_frameworks[name]['version'] == max([fw.version for fw in db_frameworks.values() if fw.framework_name == name])
            for name in common
        ):
            print("   ✅ All frameworks are in sync!")
    
    def export_framework(self, framework_name: str, version: str = None):
        """Export framework from database to filesystem."""
        session = self.Session()
        try:
            # Get framework from database
            query = session.query(FrameworkVersion).filter_by(framework_name=framework_name)
            if version:
                query = query.filter_by(version=version)
            else:
                # Get latest version
                query = query.order_by(FrameworkVersion.created_at.desc())
            
            framework = query.first()
            if not framework:
                print(f"❌ Framework {framework_name}:{version or 'latest'} not found in database")
                return False
            
            # Create filesystem directory
            framework_dir = self.frameworks_dir / framework_name
            framework_dir.mkdir(parents=True, exist_ok=True)
            
            # Export framework.json
            framework_file = framework_dir / "framework.json"
            with open(framework_file, 'w') as f:
                json.dump(framework.framework_json, f, indent=2)
            
            # Export dipoles.json
            dipoles_file = framework_dir / "dipoles.json"
            with open(dipoles_file, 'w') as f:
                json.dump(framework.dipoles_json, f, indent=2)
            
            # Export weights.json
            weights_file = framework_dir / "weights.json"
            with open(weights_file, 'w') as f:
                json.dump(framework.weights_json, f, indent=2)
            
            # Create/update README.md
            readme_file = framework_dir / "README.md"
            readme_content = self._generate_readme(framework)
            with open(readme_file, 'w') as f:
                f.write(readme_content)
            
            print(f"✅ Exported {framework_name}:{framework.version} from database to filesystem")
            return True
            
        finally:
            session.close()
    
    def import_framework(self, framework_name: str, create_new_version: bool = True):
        """Import framework from filesystem to database."""
        framework_dir = self.frameworks_dir / framework_name
        
        if not framework_dir.exists():
            print(f"❌ Framework directory {framework_dir} not found")
            return False
        
        # Load framework files
        try:
            framework_file = framework_dir / "framework.json"
            with open(framework_file, 'r') as f:
                framework_data = json.load(f)
            
            dipoles_file = framework_dir / "dipoles.json"
            with open(dipoles_file, 'r') as f:
                dipoles_data = json.load(f)
            
            weights_file = framework_dir / "weights.json"
            with open(weights_file, 'r') as f:
                weights_data = json.load(f)
                
        except Exception as e:
            print(f"❌ Error loading framework files: {e}")
            return False
        
        # Import to database
        session = self.Session()
        try:
            version = framework_data.get('version', 'v1.0')
            
            # Check if version already exists
            existing = session.query(FrameworkVersion).filter_by(
                framework_name=framework_name, 
                version=version
            ).first()
            
            if existing and not create_new_version:
                print(f"❌ Framework {framework_name}:{version} already exists in database")
                return False
            
            if existing and create_new_version:
                # Generate new version
                version = self._generate_next_version(session, framework_name)
                framework_data['version'] = version
            
            # Create new framework version
            framework = FrameworkVersion(
                framework_name=framework_name,
                version=version,
                dipoles_json=dipoles_data,
                framework_json=framework_data,
                weights_json=weights_data,
                description=framework_data.get('description', f'Imported from filesystem'),
                validation_status="draft"
            )
            
            session.add(framework)
            session.commit()
            
            print(f"✅ Imported {framework_name}:{version} from filesystem to database")
            return True
            
        finally:
            session.close()
    
    def _generate_next_version(self, session, framework_name: str) -> str:
        """Generate next version number for framework."""
        existing_versions = session.query(FrameworkVersion.version).filter_by(
            framework_name=framework_name
        ).all()
        
        if not existing_versions:
            return "v1.0"
        
        # Simple increment - could be made more sophisticated
        max_version = max([v[0] for v in existing_versions])
        if max_version.startswith('v'):
            try:
                major, minor = max_version[1:].split('.')
                return f"v{major}.{int(minor) + 1}"
            except:
                pass
        
        # Fallback to timestamp-based version
        return f"v{datetime.now().strftime('%Y.%m.%d')}"
    
    def _generate_readme(self, framework: FrameworkVersion) -> str:
        """Generate README content for framework."""
        return f"""# {framework.framework_name.title()} Framework

**Version:** {framework.version}  
**Status:** {framework.validation_status}  
**Created:** {framework.created_at.strftime('%Y-%m-%d') if framework.created_at else 'Unknown'}

## Description

{framework.description or 'No description provided.'}

## Theoretical Foundation

{framework.theoretical_foundation or 'No theoretical foundation documented.'}

## Framework Structure

This framework contains {len(framework.dipoles_json)} dipoles with the following wells:

{self._format_wells_list(framework.dipoles_json)}

## Files

- `framework.json`: Complete framework configuration
- `dipoles.json`: Dipole and well definitions  
- `weights.json`: Mathematical weighting configuration
- `README.md`: This documentation file

## Usage

This framework is stored in the database as the source of truth. To use:

```python
        from src.models.component_models import FrameworkVersion
framework = session.query(FrameworkVersion).filter_by(
    framework_name="{framework.framework_name}", 
    version="{framework.version}"
).first()
```

## Development Notes

{framework.development_notes or 'No development notes.'}

---
*Generated automatically by framework_sync.py*
"""
    
    def _format_wells_list(self, dipoles_data: Dict) -> str:
        """Format wells list for README."""
        if not dipoles_data:
            return "No wells defined."
        
        lines = []
        for dipole_name, dipole_data in dipoles_data.items():
            if isinstance(dipole_data, dict) and 'positive_well' in dipole_data:
                pos_name = dipole_data['positive_well'].get('name', 'Unknown')
                neg_name = dipole_data['negative_well'].get('name', 'Unknown')
                lines.append(f"- **{dipole_name}**: {pos_name} ↔ {neg_name}")
        
        return '\n'.join(lines) if lines else "Wells structure not recognized."
    
    def validate_framework(self, framework_name: str) -> bool:
        """Validate framework files in filesystem."""
        framework_dir = self.frameworks_dir / framework_name
        
        if not framework_dir.exists():
            print(f"❌ Framework directory {framework_dir} not found")
            return False
        
        print(f"🔍 Validating {framework_name} framework files...")
        
        # Check required files
        required_files = ['framework.json', 'dipoles.json', 'weights.json']
        missing_files = []
        
        for filename in required_files:
            file_path = framework_dir / filename
            if not file_path.exists():
                missing_files.append(filename)
        
        if missing_files:
            print(f"❌ Missing required files: {', '.join(missing_files)}")
            return False
        
        # Validate JSON structure
        try:
            # Load and validate each file
            framework_file = framework_dir / "framework.json"
            with open(framework_file, 'r') as f:
                framework_data = json.load(f)
            
            dipoles_file = framework_dir / "dipoles.json"
            with open(dipoles_file, 'r') as f:
                dipoles_data = json.load(f)
            
            weights_file = framework_dir / "weights.json"
            with open(weights_file, 'r') as f:
                weights_data = json.load(f)
            
            # Basic structure validation
            if 'framework_name' not in framework_data:
                print("❌ framework.json missing 'framework_name' field")
                return False
            
            if 'version' not in framework_data:
                print("❌ framework.json missing 'version' field")
                return False
            
            print(f"✅ {framework_name} framework files are valid")
            return True
            
        except json.JSONDecodeError as e:
            print(f"❌ JSON parsing error: {e}")
            return False
        except Exception as e:
            print(f"❌ Validation error: {e}")
            return False
    
    def migrate_all_to_v2(self):
        """Migrate all frameworks to v2.0 specification."""
        print("🚀 Migrating all frameworks to v2.0 specification...")
        
        # Import the migration classes
        sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
        from migrate_frameworks_to_v2 import FrameworkMigrator
        
        migrator = FrameworkMigrator()
        fs_frameworks = self.get_filesystem_frameworks()
        
        for framework_name in fs_frameworks.keys():
            print(f"\n📋 Migrating {framework_name}...")
            try:
                framework_file = self.frameworks_dir / framework_name / "framework.json"
                if framework_file.exists():
                    result = migrator.migrate_framework(str(framework_file), dry_run=False)
                    if result:
                        print(f"✅ {framework_name} migrated successfully")
                        # Import the migrated version to database
                        self.import_framework(framework_name, create_new_version=True)
                    else:
                        print(f"❌ {framework_name} migration failed")
                else:
                    print(f"❌ Framework file not found: {framework_file}")
            except Exception as e:
                print(f"❌ Error migrating {framework_name}: {e}")


def main():
    parser = argparse.ArgumentParser(description="Framework Synchronization Tool")
    parser.add_argument('command', choices=['status', 'export', 'import', 'validate', 'migrate-all'],
                       help='Command to execute')
    parser.add_argument('framework', nargs='?', help='Framework name (for export/import/validate)')
    parser.add_argument('--version', help='Specific version (for export)')
    parser.add_argument('--force', action='store_true', help='Force operation')
    
    args = parser.parse_args()
    
    sync_manager = FrameworkSyncManager()
    
    if args.command == 'status':
        sync_manager.show_status()
    
    elif args.command == 'export':
        if not args.framework:
            print("❌ Framework name required for export")
            sys.exit(1)
        sync_manager.export_framework(args.framework, args.version)
    
    elif args.command == 'import':
        if not args.framework:
            print("❌ Framework name required for import")
            sys.exit(1)
        sync_manager.import_framework(args.framework, create_new_version=not args.force)
    
    elif args.command == 'validate':
        if not args.framework:
            print("❌ Framework name required for validation")
            sys.exit(1)
        sync_manager.validate_framework(args.framework)
    
    elif args.command == 'migrate-all':
        sync_manager.migrate_all_to_v2()


if __name__ == "__main__":
    main() 