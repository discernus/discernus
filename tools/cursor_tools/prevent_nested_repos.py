#!/usr/bin/env python3
"""
Nested Git Repository Prevention System
======================================

Prevents accidental creation of nested git repositories that break the 
GitHub-as-persistence-layer architecture for research provenance.

Usage:
    python3 scripts/prevent_nested_repos.py --scan     # Check for nested repos
    python3 scripts/prevent_nested_repos.py --clean    # Remove nested repos
    python3 scripts/prevent_nested_repos.py --install  # Install git hooks
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path
from typing import List, Dict, Any

class NestedRepoPreventionSystem:
    """
    Comprehensive system to prevent nested git repositories that break 
    the chronolog provenance system.
    """
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.main_git_dir = self.project_root / ".git"
        
        if not self.main_git_dir.exists():
            raise ValueError(f"Not a git repository: {self.project_root}")
    
    def scan_for_nested_repos(self) -> List[Path]:
        """Find all nested git repositories"""
        nested_repos = []
        
        for root, dirs, files in os.walk(self.project_root):
            if '.git' in dirs:
                git_path = Path(root) / '.git'
                # Skip the main project .git directory
                if git_path != self.main_git_dir:
                    nested_repos.append(git_path)
        
        return nested_repos
    
    def clean_nested_repos(self, confirm: bool = False) -> Dict[str, Any]:
        """Remove all nested git repositories"""
        nested_repos = self.scan_for_nested_repos()
        
        if not nested_repos:
            return {'status': 'clean', 'removed': 0, 'repos': []}
        
        if not confirm:
            print(f"🔍 Found {len(nested_repos)} nested git repositories:")
            for repo in nested_repos:
                print(f"  - {repo}")
            print("\nThese break the GitHub-as-persistence-layer architecture!")
            print("Run with --confirm to remove them.")
            return {'status': 'found', 'removed': 0, 'repos': [str(r) for r in nested_repos]}
        
        removed_repos = []
        for repo in nested_repos:
            try:
                subprocess.run(['rm', '-rf', str(repo)], check=True)
                removed_repos.append(str(repo))
                print(f"✅ Removed nested repo: {repo}")
            except subprocess.CalledProcessError as e:
                print(f"❌ Failed to remove {repo}: {e}")
        
        return {'status': 'cleaned', 'removed': len(removed_repos), 'repos': removed_repos}
    
    def install_git_hooks(self) -> bool:
        """Install git hooks to prevent nested repo creation"""
        hooks_dir = self.main_git_dir / "hooks"
        hooks_dir.mkdir(exist_ok=True)
        
        # Pre-commit hook to detect nested repos
        pre_commit_hook = hooks_dir / "pre-commit"
        
        hook_content = '''#!/bin/bash
# Discernus Nested Repository Prevention Hook
# Prevents commits that would create nested git repositories

echo "🔍 Checking for nested git repositories..."

# Find any .git directories except the main one
nested_repos=$(find . -name ".git" -type d | grep -v "^\./\.git$")

if [ -n "$nested_repos" ]; then
    echo "❌ COMMIT BLOCKED: Nested git repositories detected!"
    echo ""
    echo "The following nested repositories break GitHub-as-persistence-layer:"
    echo "$nested_repos"
    echo ""
    echo "💡 To fix this issue:"
    echo "   1. Remove nested repos: python3 scripts/prevent_nested_repos.py --clean --confirm"
    echo "   2. Add files to main repo: git add ."
    echo "   3. Commit normally: git commit -m 'your message'"
    echo ""
    echo "📚 Why this matters:"
    echo "   - Chronolog system requires all files in main repository"
    echo "   - Nested repos break academic provenance tracking"
    echo "   - GitHub persistence layer becomes unreliable"
    echo ""
    exit 1
fi

echo "✅ No nested repositories found - commit proceeding"
'''
        
        try:
            with open(pre_commit_hook, 'w') as f:
                f.write(hook_content)
            
            # Make hook executable
            os.chmod(pre_commit_hook, 0o755)
            
            print(f"✅ Installed pre-commit hook: {pre_commit_hook}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to install git hook: {e}")
            return False
    
    def create_gitignore_patterns(self) -> bool:
        """Add patterns to .gitignore to prevent common nested repo scenarios"""
        gitignore_path = self.project_root / ".gitignore"
        
        patterns_to_add = [
            "",
            "# Prevent nested git repositories",
            "**/.git/",
            "**/git/",
            "",
            "# Prevent common experiment repo creation patterns",
            "experiments/**/.git/",
            "projects/**/.git/",
            "results/**/.git/",
            ""
        ]
        
        try:
            # Read existing .gitignore
            existing_patterns = set()
            if gitignore_path.exists():
                with open(gitignore_path, 'r') as f:
                    existing_patterns = set(line.strip() for line in f.readlines())
            
            # Add new patterns that don't already exist
            new_patterns = []
            for pattern in patterns_to_add:
                if pattern not in existing_patterns:
                    new_patterns.append(pattern)
            
            if new_patterns:
                with open(gitignore_path, 'a') as f:
                    f.write('\n'.join(new_patterns))
                
                print(f"✅ Added nested repo prevention patterns to .gitignore")
                return True
            else:
                print("✅ .gitignore already contains nested repo prevention patterns")
                return True
                
        except Exception as e:
            print(f"❌ Failed to update .gitignore: {e}")
            return False
    
    def create_user_guidance(self) -> bool:
        """Create user guidance document"""
        guidance_path = self.project_root / "docs" / "GIT_BEST_PRACTICES.md"
        guidance_path.parent.mkdir(exist_ok=True)
        
        guidance_content = '''# Git Best Practices for Discernus Research
**Preventing Nested Repository Issues**

## ⚠️ Critical Rule: Never Run `git init` in Project Subdirectories

### Why This Matters
- **GitHub is our persistence layer** for research provenance
- **Chronolog system** requires all files in the main repository
- **Nested repositories break academic integrity** tracking
- **Peer review becomes impossible** without complete audit trail

### ❌ What NOT to Do
```bash
# NEVER do this in experiment directories:
cd projects/my_experiment/
git init  # ❌ This breaks everything!

# NEVER do this in any subdirectory:
cd results/some_analysis/
git init  # ❌ This breaks provenance!
```

### ✅ What TO Do Instead
```bash
# Always work from the main repository:
cd /path/to/discernus/
git add projects/my_experiment/
git commit -m "Add new experiment"

# All experiment files belong in main repo:
git add projects/my_experiment/framework.md
git add projects/my_experiment/experiment.md
git add projects/my_experiment/results/
git commit -m "Complete experiment analysis"
```

### 🔧 If You Accidentally Created Nested Repos
```bash
# Scan for problems:
python3 scripts/prevent_nested_repos.py --scan

# Clean them up:
python3 scripts/prevent_nested_repos.py --clean --confirm

# Add files to main repo:
git add .
git commit -m "Fix nested repository issue"
```

### 🛡️ Prevention System
- **Git hooks** automatically detect nested repos before commit
- **Scanning script** finds existing problems
- **Cleanup script** removes nested repos safely
- **.gitignore patterns** prevent common mistakes

### 📚 Academic Integrity Impact
When nested repositories exist:
- **Chronolog events** get logged but files don't get committed
- **Provenance chain** breaks between logs and actual files
- **Peer reviewers** can't verify complete research record
- **Replication** becomes impossible due to missing files

### 🆘 Emergency Recovery
If you've lost work due to nested repos:
1. **Don't panic** - files are still on disk
2. **Run cleanup script** to remove nested .git directories
3. **Add all files** to main repository: `git add .`
4. **Commit everything** to restore provenance
5. **Verify chronolog** integrity with scanning tools

### 💡 Pro Tips
- **Use git status** regularly to see what's tracked
- **Check for nested repos** before major commits
- **Keep experiments** in projects/ directory structure
- **Let chronolog system** handle all git operations automatically

Remember: The entire academic integrity system depends on having a single, unified git repository with complete provenance tracking.
'''
        
        try:
            with open(guidance_path, 'w') as f:
                f.write(guidance_content)
            
            print(f"✅ Created user guidance: {guidance_path}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to create user guidance: {e}")
            return False

def main():
    parser = argparse.ArgumentParser(description='Prevent nested git repositories')
    parser.add_argument('--scan', action='store_true', help='Scan for nested repositories')
    parser.add_argument('--clean', action='store_true', help='Remove nested repositories')
    parser.add_argument('--confirm', action='store_true', help='Confirm destructive operations')
    parser.add_argument('--install', action='store_true', help='Install prevention system')
    
    args = parser.parse_args()
    
    try:
        system = NestedRepoPreventionSystem()
        
        if args.scan:
            nested_repos = system.scan_for_nested_repos()
            if nested_repos:
                print(f"🔍 Found {len(nested_repos)} nested repositories:")
                for repo in nested_repos:
                    print(f"  - {repo}")
                print("\n💡 Run with --clean --confirm to remove them")
            else:
                print("✅ No nested repositories found")
        
        elif args.clean:
            result = system.clean_nested_repos(confirm=args.confirm)
            if result['status'] == 'cleaned':
                print(f"✅ Cleaned up {result['removed']} nested repositories")
            elif result['status'] == 'found':
                print("💡 Add --confirm to actually remove the repositories")
        
        elif args.install:
            print("🔧 Installing nested repository prevention system...")
            
            # Install git hooks
            hook_success = system.install_git_hooks()
            
            # Update .gitignore
            gitignore_success = system.create_gitignore_patterns()
            
            # Create user guidance
            guidance_success = system.create_user_guidance()
            
            if hook_success and gitignore_success and guidance_success:
                print("✅ Prevention system installed successfully!")
                print("💡 Users will now be warned before creating nested repos")
            else:
                print("⚠️ Some components failed to install")
        
        else:
            parser.print_help()
    
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 