#!/usr/bin/env python3
"""
Framework Manager for Narrative Gravity Wells

Manages multiple dipole frameworks and enables easy switching between them.
"""

import json
import os
from pathlib import Path
import argparse

class FrameworkManager:
    def __init__(self, base_dir="."):
        self.base_dir = Path(base_dir)
        self.frameworks_dir = self.base_dir / "frameworks"
        self.config_dir = self.base_dir / "config"
        self.prompts_dir = self.base_dir / "prompts"
    
    def list_frameworks(self):
        """List available frameworks"""
        if not self.frameworks_dir.exists():
            print("No frameworks directory found.")
            return []
        
        frameworks = []
        for framework_path in self.frameworks_dir.iterdir():
            if framework_path.is_dir():
                dipoles_file = framework_path / "dipoles.json"
                framework_file = framework_path / "framework.json"
                
                if dipoles_file.exists() and framework_file.exists():
                    try:
                        with open(dipoles_file) as f:
                            dipoles_data = json.load(f)
                        with open(framework_file) as f:
                            framework_data = json.load(f)
                        
                        # Use explicit framework_name from files, fallback to folder name
                        framework_name = dipoles_data.get('framework_name') or framework_data.get('framework_name') or framework_path.name
                        
                        frameworks.append({
                            'name': framework_name,
                            'directory': framework_path.name,  # Keep track of directory for switching
                            'path': framework_path,
                            'version': framework_data.get('version', 'unknown').lstrip('v'),  # Remove 'v' prefix if present
                            'description': dipoles_data.get('description', 'No description'),
                            'dipole_count': len(dipoles_data.get('dipoles', [])),
                            'well_count': len(framework_data.get('wells', {}))
                        })
                    except (json.JSONDecodeError, KeyError) as e:
                        print(f"Warning: Invalid framework in {framework_path}: {e}")
        
        return frameworks
    
    def get_active_framework(self):
        """Get currently active framework"""
        dipoles_link = self.config_dir / "dipoles.json"
        framework_link = self.config_dir / "framework.json"
        
        if dipoles_link.exists() and framework_link.exists():
            try:
                # Read framework name from the files themselves
                with open(dipoles_link) as f:
                    dipoles_data = json.load(f)
                with open(framework_link) as f:
                    framework_data = json.load(f)
                
                # Use explicit framework_name from files
                framework_name = dipoles_data.get('framework_name') or framework_data.get('framework_name')
                if framework_name:
                    return framework_name
                
                # Fallback: extract from symlink path if no explicit name
                if dipoles_link.is_symlink():
                    dipoles_target = os.readlink(dipoles_link)
                    parts = dipoles_target.split('/')
                    if len(parts) >= 3 and parts[-3] == 'frameworks':
                        return parts[-2]
            except (json.JSONDecodeError, OSError):
                pass
        
        return None
    
    def switch_framework(self, framework_name):
        """Switch to a different framework by name"""
        # Find the directory for this framework name
        frameworks = self.list_frameworks()
        target_framework = None
        for fw in frameworks:
            if fw['name'] == framework_name:
                target_framework = fw
                break
        
        if not target_framework:
            raise ValueError(f"Framework '{framework_name}' not found")
        
        framework_directory = target_framework['directory']
        framework_path = self.frameworks_dir / framework_directory
        
        if not framework_path.exists():
            raise ValueError(f"Framework directory '{framework_directory}' not found")
        
        dipoles_file = framework_path / "dipoles.json"
        framework_file = framework_path / "framework.json"
        
        if not dipoles_file.exists() or not framework_file.exists():
            raise ValueError(f"Framework '{framework_name}' is incomplete (missing dipoles.json or framework.json)")
        
        # Remove existing symlinks
        config_dipoles = self.config_dir / "dipoles.json"
        config_framework = self.config_dir / "framework.json"
        
        if config_dipoles.exists():
            config_dipoles.unlink()
        if config_framework.exists():
            config_framework.unlink()
        
        # Create new symlinks
        dipoles_target = f"../frameworks/{framework_directory}/dipoles.json"
        framework_target = f"../frameworks/{framework_directory}/framework.json"
        
        config_dipoles.symlink_to(dipoles_target)
        config_framework.symlink_to(framework_target)
        
        print(f"✅ Switched to framework: {framework_name}")
        return True
    
    def validate_framework(self, framework_name):
        """Validate a framework's structure"""
        framework_path = self.frameworks_dir / framework_name
        
        if not framework_path.exists():
            return False, f"Framework directory '{framework_name}' not found"
        
        dipoles_file = framework_path / "dipoles.json"
        framework_file = framework_path / "framework.json"
        
        if not dipoles_file.exists():
            return False, "Missing dipoles.json file"
        if not framework_file.exists():
            return False, "Missing framework.json file"
        
        try:
            # Validate dipoles.json structure
            with open(dipoles_file) as f:
                dipoles_data = json.load(f)
            
            required_dipoles_fields = ['version', 'description', 'dipoles']
            for field in required_dipoles_fields:
                if field not in dipoles_data:
                    return False, f"Missing required field '{field}' in dipoles.json"
            
            # Validate framework.json structure  
            with open(framework_file) as f:
                framework_data = json.load(f)
            
            required_framework_fields = ['version', 'description', 'wells']
            for field in required_framework_fields:
                if field not in framework_data:
                    return False, f"Missing required field '{field}' in framework.json"
            
            # Check that dipoles and wells are consistent
            dipole_wells = set()
            for dipole in dipoles_data['dipoles']:
                dipole_wells.add(dipole['positive']['name'])
                dipole_wells.add(dipole['negative']['name'])
            
            framework_wells = set(framework_data['wells'].keys())
            
            if dipole_wells != framework_wells:
                missing_in_framework = dipole_wells - framework_wells
                extra_in_framework = framework_wells - dipole_wells
                issues = []
                if missing_in_framework:
                    issues.append(f"Wells missing from framework.json: {missing_in_framework}")
                if extra_in_framework:
                    issues.append(f"Extra wells in framework.json: {extra_in_framework}")
                return False, "; ".join(issues)
            
            return True, "Framework is valid"
            
        except json.JSONDecodeError as e:
            return False, f"JSON parsing error: {e}"
        except Exception as e:
            return False, f"Validation error: {e}"
    
    def create_framework_summary(self):
        """Create a summary of all frameworks"""
        frameworks = self.list_frameworks()
        active = self.get_active_framework()
        
        print("🎯 Available Frameworks:")
        print("=" * 50)
        
        for fw in frameworks:
            status = "🟢 ACTIVE" if fw['name'] == active else "⚪ Available"
            print(f"\n{status} {fw['name']} (v{fw['version']})")
            print(f"   Description: {fw['description']}")
            print(f"   Dipoles: {fw['dipole_count']}, Wells: {fw['well_count']}")
            
            # Validate framework
            is_valid, message = self.validate_framework(fw['name'])
            validation_status = "✅ Valid" if is_valid else f"❌ {message}"
            print(f"   Status: {validation_status}")
        
        if not frameworks:
            print("No frameworks found in frameworks/ directory")

def main():
    parser = argparse.ArgumentParser(description="Manage Narrative Gravity Wells frameworks")
    parser.add_argument("command", choices=["list", "switch", "active", "validate", "summary"], 
                       help="Command to execute")
    parser.add_argument("framework", nargs="?", help="Framework name (for switch/validate commands)")
    
    args = parser.parse_args()
    
    manager = FrameworkManager()
    
    try:
        if args.command == "list":
            frameworks = manager.list_frameworks()
            for fw in frameworks:
                print(f"{fw['name']} (v{fw['version']}) - {fw['description']}")
        
        elif args.command == "switch":
            if not args.framework:
                print("Error: Framework name required for switch command")
                return 1
            manager.switch_framework(args.framework)
        
        elif args.command == "active":
            active = manager.get_active_framework()
            if active:
                print(f"Active framework: {active}")
            else:
                print("No active framework (config not properly linked)")
        
        elif args.command == "validate":
            if not args.framework:
                print("Error: Framework name required for validate command")
                return 1
            is_valid, message = manager.validate_framework(args.framework)
            print(f"Framework '{args.framework}': {message}")
            return 0 if is_valid else 1
        
        elif args.command == "summary":
            manager.create_framework_summary()
    
    except Exception as e:
        print(f"Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main()) 