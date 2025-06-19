#!/usr/bin/env python3
"""
Production Documentation Date Management System

Validates and corrects dates in documentation files to prevent daily recurrence
of date-related issues in changelogs and other documentation.

PRODUCTION READY - Graduated from experimental/prototypes/
"""

import re
import subprocess
from datetime import datetime, date
from pathlib import Path
from typing import List, Dict, Optional
import json
import argparse


class ProductionDateManager:
    """Production-ready documentation date management system."""
    
    def __init__(self, base_path: str = "."):
        self.base_path = Path(base_path)
        self.current_date = date.today()
        
        # Files to monitor for date issues
        self.monitored_files = [
            'docs/paper/PAPER_CHANGELOG.md',
            'CHANGELOG.md',
            'docs/DOCUMENTATION_INVENTORY.md'
        ]
        
        # Date patterns for validation
        self.date_patterns = {
            'changelog_version': r'\[.*?\]\s*-\s*(\d{4}-\d{2}-\d{2})',
            'iso_date': r'(\d{4}-\d{2}-\d{2})',
            'review_date': r'review\s*\((\d{4}-\d{2}-\d{2})\)',
        }
    
    def validate_all_docs(self) -> Dict:
        """Validate dates in all monitored documentation files."""
        
        results = {}
        total_issues = 0
        
        for doc_file in self.monitored_files:
            filepath = self.base_path / doc_file
            if filepath.exists():
                result = self._validate_single_file(doc_file)
                results[doc_file] = result
                if 'issues' in result:
                    total_issues += len(result['issues'])
        
        results['summary'] = {
            'total_files_checked': len([f for f in self.monitored_files if (self.base_path / f).exists()]),
            'total_issues_found': total_issues,
            'check_date': str(self.current_date)
        }
        
        return results
    
    def _validate_single_file(self, file_path: str) -> Dict:
        """Validate dates in a single file."""
        
        filepath = self.base_path / file_path
        if not filepath.exists():
            return {"error": f"File not found: {file_path}"}
        
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        issues = []
        all_dates = []
        
        # Find all dates
        for pattern_name, pattern in self.date_patterns.items():
            matches = re.finditer(pattern, content, re.IGNORECASE)
            for match in matches:
                date_str = match.group(1)
                line_num = content[:match.start()].count('\n') + 1
                all_dates.append({
                    'date': date_str,
                    'line': line_num,
                    'pattern': pattern_name
                })
        
        # Validate dates
        for date_info in all_dates:
            try:
                parsed_date = datetime.strptime(date_info['date'], '%Y-%m-%d').date()
                
                # Check for suspicious old dates (5+ months)
                months_old = (self.current_date - parsed_date).days / 30
                if months_old > 5:
                    issues.append({
                        'type': 'old_date',
                        'line': date_info['line'],
                        'date': date_info['date'],
                        'message': f"Date {date_info['date']} is {months_old:.1f} months old - verify accuracy"
                    })
                
                # Check for future dates
                if parsed_date > self.current_date:
                    issues.append({
                        'type': 'future_date',
                        'line': date_info['line'],
                        'date': date_info['date'],
                        'message': f"Date {date_info['date']} is in the future"
                    })
                    
            except ValueError:
                issues.append({
                    'type': 'invalid_format',
                    'line': date_info['line'],
                    'date': date_info['date'],
                    'message': f"Invalid date format: {date_info['date']}"
                })
        
        return {
            'file': file_path,
            'issues': issues,
            'total_dates': len(all_dates),
            'last_checked': str(self.current_date)
        }
    
    def create_date_template(self, version: str) -> str:
        """Create a changelog template with correct current date."""
        
        current_date_str = self.current_date.strftime('%Y-%m-%d')
        
        template = f"""## [{version}] - {current_date_str}

### Added

### Changed

### Fixed

### Removed

"""
        return template
    
    def get_git_dates(self, file_path: str) -> List[str]:
        """Get recent commit dates for a file."""
        
        try:
            result = subprocess.run(
                ['git', 'log', '--date=short', '--format=%cd', '-n', '5', file_path],
                cwd=self.base_path,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return [line.strip() for line in result.stdout.strip().split('\n') if line.strip()]
        except Exception:
            pass
        
        return []
    
    def daily_check(self) -> bool:
        """Run daily validation check. Returns True if issues found."""
        
        print(f"🗓️  Documentation Date Check - {self.current_date}")
        print("=" * 40)
        
        results = self.validate_all_docs()
        
        has_issues = False
        for file_path, result in results.items():
            if file_path == 'summary':
                continue
                
            if 'error' in result:
                print(f"❌ {file_path}: {result['error']}")
            elif result['issues']:
                has_issues = True
                print(f"⚠️  {file_path}: {len(result['issues'])} issues")
                for issue in result['issues'][:3]:  # Show first 3 issues
                    print(f"   Line {issue['line']}: {issue['message']}")
                if len(result['issues']) > 3:
                    print(f"   ... and {len(result['issues']) - 3} more issues")
            else:
                print(f"✅ {file_path}: No issues ({result['total_dates']} dates)")
        
        if has_issues:
            print(f"\n🔧 To fix issues:")
            print(f"   python3 scripts/production/documentation_date_management.py --fix")
            print(f"   python3 scripts/production/documentation_date_management.py --template v1.x.x")
        
        return has_issues
    
    def install_git_hook(self) -> bool:
        """Install pre-commit hook for date validation."""
        
        hook_content = f'''#!/bin/bash
# Auto-generated pre-commit hook for documentation date validation

echo "🗓️  Validating documentation dates..."

python3 scripts/production/documentation_date_management.py --check

if [ $? -eq 1 ]; then
    echo "⚠️  Documentation date issues detected."
    echo "Run: python3 scripts/production/documentation_date_management.py --daily"
    echo "Consider reviewing dates before committing."
fi
'''
        
        hooks_dir = self.base_path / ".git" / "hooks"
        if not hooks_dir.exists():
            print("Git hooks directory not found")
            return False
        
        hook_file = hooks_dir / "pre-commit"
        
        with open(hook_file, 'w') as f:
            f.write(hook_content)
        
        # Make executable
        import stat
        hook_file.chmod(hook_file.stat().st_mode | stat.S_IEXEC)
        
        print(f"✅ Installed pre-commit hook: {hook_file}")
        return True


def main():
    """CLI interface for production date management."""
    
    parser = argparse.ArgumentParser(description='Production Documentation Date Management')
    parser.add_argument('--daily', action='store_true', help='Run daily validation check')
    parser.add_argument('--check', action='store_true', help='Quick validation check (for git hooks)')
    parser.add_argument('--template', metavar='VERSION', help='Generate changelog template with current date')
    parser.add_argument('--install-hook', action='store_true', help='Install git pre-commit hook')
    parser.add_argument('--json', action='store_true', help='Output results in JSON format')
    
    args = parser.parse_args()
    
    manager = ProductionDateManager()
    
    if args.template:
        print(manager.create_date_template(args.template))
        return
    
    if args.install_hook:
        success = manager.install_git_hook()
        exit(0 if success else 1)
    
    if args.daily:
        has_issues = manager.daily_check()
        exit(1 if has_issues else 0)
    
    if args.check:
        # Quick check for git hooks
        results = manager.validate_all_docs()
        issues = sum(len(r.get('issues', [])) for r in results.values() if isinstance(r, dict) and 'issues' in r)
        
        if args.json:
            print(json.dumps(results, indent=2))
        elif issues > 0:
            print(f"Found {issues} date issues in documentation")
        
        exit(1 if issues > 0 else 0)
    
    # Default: show help
    parser.print_help()


if __name__ == '__main__':
    main() 