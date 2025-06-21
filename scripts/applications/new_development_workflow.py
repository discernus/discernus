#!/usr/bin/env python3
"""
New Development Workflow

Guided workflow that enforces AI assistant rules automatically.
Makes following the rules easier than breaking them.

Usage:
    python3 scripts/production/new_development_workflow.py
"""

import sys
import subprocess
from pathlib import Path

def run_command(command, check=True):
    """Run a command and return the result."""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if check and result.returncode != 0:
            print(f"❌ Command failed: {command}")
            print(f"Error: {result.stderr}")
            return None
        return result
    except Exception as e:
        print(f"❌ Error running command: {e}")
        return None

def search_existing_systems(functionality):
    """Run the mandatory production search."""
    print(f"🔍 MANDATORY: Searching for existing systems...")
    search_command = f'python3 scripts/production/check_existing_systems.py "{functionality}"'
    result = run_command(search_command, check=False)
    
    if result and result.stdout:
        print(result.stdout)
        return "FOUND PRODUCTION SYSTEMS" in result.stdout
    return False

def validate_compliance(suggestion):
    """Validate suggestion compliance."""
    print(f"\n🛡️ Validating compliance...")
    compliance_command = f'python3 scripts/production/validate_ai_assistant_compliance.py --check-suggestion "{suggestion}"'
    result = run_command(compliance_command, check=False)
    
    if result:
        print(result.stdout)
        return result.returncode == 0
    return False

def main():
    """Main workflow function."""
    print("🚀 NEW DEVELOPMENT WORKFLOW")
    print("=" * 50)
    print("This workflow enforces AI assistant rules automatically.\n")
    
    # Step 1: Get functionality description
    print("📝 Step 1: What functionality do you want to build?")
    functionality = input("Describe what you want to create: ").strip()
    
    if not functionality:
        print("❌ Please provide a functionality description.")
        sys.exit(1)
    
    # Step 2: Mandatory production search
    print(f"\n🔍 Step 2: Searching production systems for '{functionality}'...")
    found_production = search_existing_systems(functionality)
    
    if found_production:
        print("\n✅ PRODUCTION SYSTEMS FOUND!")
        print("🎯 RECOMMENDATION: Enhance existing production code instead of rebuilding.")
        
        enhance = input("\nDo you want to enhance existing systems? (y/n): ").strip().lower()
        if enhance in ['y', 'yes']:
            print("\n✅ CORRECT CHOICE: Enhancing existing systems")
            print("📚 Next steps:")
            print("1. Review the production code found above")
            print("2. Identify specific enhancement points")
            print("3. Create enhancement plan in experimental/ first")
            print("4. Test enhancements before applying to production")
            sys.exit(0)
        else:
            print("\n⚠️ WARNING: You chose to build new instead of enhancing existing.")
    
    # Step 3: Validate the development approach
    print(f"\n🛡️ Step 3: Validating development approach...")
    approach = input("Describe your development approach: ").strip()
    
    if not approach:
        print("❌ Please provide a development approach.")
        sys.exit(1)
    
    is_compliant = validate_compliance(approach)
    
    if not is_compliant:
        print("\n❌ COMPLIANCE VIOLATION DETECTED!")
        print("🔧 Please revise your approach to follow project rules.")
        print("📚 See .ai_assistant_rules.md for guidance.")
        sys.exit(1)
    
    # Step 4: Set up experimental development
    print(f"\n🧪 Step 4: Setting up experimental development...")
    project_name = input("Enter project name (lowercase, underscores): ").strip()
    
    if not project_name or not project_name.replace('_', '').isalnum():
        print("❌ Please provide a valid project name (lowercase, underscores only).")
        sys.exit(1)
    
    # Create experimental directory
    experimental_path = Path(f"experimental/prototypes/{project_name}")
    experimental_path.mkdir(parents=True, exist_ok=True)
    
    # Create initial files
    readme_content = f"""# {project_name.title().replace('_', ' ')} - Experimental Development

## Functionality
{functionality}

## Development Approach  
{approach}

## Production Search Results
- Existing systems were searched on {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}
- Found production systems: {'Yes' if found_production else 'No'}

## Next Steps
1. Develop prototype in this experimental directory
2. Test thoroughly with representative data
3. Document enhancement over existing systems (if applicable)
4. Prepare for promotion to production when ready

## Promotion Checklist
- [ ] Code quality validation passes
- [ ] Comprehensive testing completed
- [ ] Documentation written
- [ ] Integration with existing systems verified
- [ ] Performance meets production standards
"""
    
    with open(experimental_path / "README.md", "w") as f:
        f.write(readme_content)
    
    init_py_content = f'"""{project_name.title().replace("_", " ")} - Experimental prototype."""\n'
    with open(experimental_path / "__init__.py", "w") as f:
        f.write(init_py_content)
    
    print(f"\n✅ EXPERIMENTAL SETUP COMPLETE!")
    print(f"📁 Created: {experimental_path}")
    print(f"📁 Files created:")
    print(f"   - README.md (project documentation)")
    print(f"   - __init__.py (Python package initialization)")
    
    # Step 5: Final guidance
    print(f"\n🎯 NEXT STEPS:")
    print(f"1. cd {experimental_path}")
    print(f"2. Develop your prototype")
    print(f"3. Test thoroughly")
    print(f"4. When ready, run promotion workflow")
    
    print(f"\n🛡️ RULES ENFORCED:")
    print(f"✅ Production search performed first")
    print(f"✅ Compliance validation passed")
    print(f"✅ Development started in experimental/")
    print(f"✅ Enhancement over rebuilding encouraged")
    
    print(f"\n📚 REMEMBER:")
    print(f"- Build in experimental/ first")
    print(f"- Enhance existing systems when possible")
    print(f"- Follow production promotion process")
    print(f"- Never reference deprecated code")

if __name__ == "__main__":
    main() 