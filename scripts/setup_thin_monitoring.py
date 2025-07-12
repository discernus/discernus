#!/usr/bin/env python3
"""
THIN Monitoring Setup Script
===========================

Sets up and starts the complete THIN monitoring system for Cursor agents.
"""

import sys
import subprocess
import os
from pathlib import Path

def install_dependencies():
    """Install required dependencies"""
    print("📦 Installing THIN monitoring dependencies...")
    
    dependencies = [
        'watchdog',  # For file monitoring
        'pylint',    # For linting integration
    ]
    
    for dep in dependencies:
        try:
            print(f"   Installing {dep}...")
            subprocess.run([sys.executable, '-m', 'pip', 'install', dep], 
                         check=True, capture_output=True)
            print(f"   ✅ {dep} installed")
        except subprocess.CalledProcessError as e:
            print(f"   ❌ Failed to install {dep}: {e}")
            return False
    
    return True

def check_cursor_setup():
    """Check if Cursor/VSCode setup is correct"""
    print("🔍 Checking Cursor/VSCode setup...")
    
    cursor_dir = Path('.cursor')
    vscode_dir = Path('.vscode')
    
    # Check Cursor rules
    if (cursor_dir / 'rules').exists():
        print("   ✅ Cursor rules file found")
    else:
        print("   ❌ Cursor rules file missing")
        return False
    
    # Check VSCode settings
    if (vscode_dir / 'settings.json').exists():
        print("   ✅ VSCode settings found")
    else:
        print("   ❌ VSCode settings missing")
        return False
    
    # Check pylint plugin
    if Path('scripts/thin_pylint_plugin.py').exists():
        print("   ✅ THIN pylint plugin found")
    else:
        print("   ❌ THIN pylint plugin missing")
        return False
    
    return True

def test_thin_linting():
    """Test the THIN linting setup"""
    print("🧪 Testing THIN linting...")
    
    # Create a test file with THICK patterns
    test_file = Path('test_thick_patterns.py')
    thick_code = '''
import re
import bs4

def parse_content(text):
    if re.search(r'pattern', text):
        if text.split(','):
            if text.replace(' ', ''):
                return text.strip()
    return None

def extract_data(html):
    soup = bs4.BeautifulSoup(html, 'html.parser')
    return soup.find('div')
'''
    
    test_file.write_text(thick_code)
    
    try:
        # Run pylint with THIN plugin
        result = subprocess.run([
            sys.executable, '-m', 'pylint',
            '--load-plugins=scripts.thin_pylint_plugin',
            '--disable=all',
            '--enable=thick-regex-import,thick-content-processing,thick-complex-logic,thick-string-manipulation,thick-html-xml-parsing',
            str(test_file)
        ], capture_output=True, text=True)
        
        if 'thick-' in result.stdout:
            print("   ✅ THIN linting is working - detected THICK patterns")
            print("   Sample violations found:")
            for line in result.stdout.split('\n'):
                if 'thick-' in line:
                    print(f"     {line.strip()}")
        else:
            print("   ❌ THIN linting not detecting violations")
            print(f"   Pylint output: {result.stdout}")
            return False
        
    except Exception as e:
        print(f"   ❌ Error testing linting: {e}")
        return False
    
    finally:
        # Clean up test file
        if test_file.exists():
            test_file.unlink()
    
    return True

def start_monitoring():
    """Start the THIN monitoring system"""
    print("🚀 Starting THIN monitoring system...")
    
    try:
        # Import and start the watcher
        sys.path.append('scripts')
        from cursor_thin_watcher import start_watcher
        
        print("   Real-time THICK pattern detection started")
        print("   Press Ctrl+C to stop monitoring")
        start_watcher()
        
    except KeyboardInterrupt:
        print("\n   👋 THIN monitoring stopped")
    except ImportError as e:
        print(f"   ❌ Failed to import watcher: {e}")
    except Exception as e:
        print(f"   ❌ Error starting monitoring: {e}")

def show_usage_instructions():
    """Show how to use the THIN monitoring system"""
    print("\n📚 THIN Monitoring Usage Instructions")
    print("=" * 50)
    print()
    print("🎯 The system is now active and will:")
    print("   • Monitor Python files for THICK patterns")
    print("   • Create warning files when violations detected")
    print("   • Show linting errors in VSCode/Cursor")
    print("   • Constrain Cursor AI with THIN rules")
    print()
    print("💡 Manual Commands:")
    print("   • Start monitoring: python scripts/cursor_thin_watcher.py")
    print("   • Test linting: pylint --load-plugins=scripts.thin_pylint_plugin your_file.py")
    print("   • Check Cursor rules: cat .cursor/rules")
    print()
    print("🚨 When you see warnings:")
    print("   • Replace parsing logic with: llm_client.call_llm()")
    print("   • Use LLM for content processing, not custom logic")
    print("   • Keep functions under 50 lines")
    print("   • Simple orchestration only")
    print()
    print("✅ Success indicators:")
    print("   • Cursor suggests llm_client.call_llm() instead of parsing")
    print("   • Warning files appear when writing THICK code")
    print("   • Linting errors show in editor for violations")

def main():
    """Main setup function"""
    print("🔧 THIN Monitoring System Setup")
    print("=" * 40)
    print()
    
    # Check if we're in the right directory
    if not Path('discernus').exists():
        print("❌ Run this from the project root directory")
        sys.exit(1)
    
    # Install dependencies
    if not install_dependencies():
        print("❌ Dependency installation failed")
        sys.exit(1)
    
    # Check setup
    if not check_cursor_setup():
        print("❌ Cursor/VSCode setup incomplete")
        print("💡 Make sure you have .cursor/rules and .vscode/settings.json")
        sys.exit(1)
    
    # Test linting
    if not test_thin_linting():
        print("❌ THIN linting test failed")
        sys.exit(1)
    
    print("\n✅ THIN monitoring system setup complete!")
    print()
    
    # Ask if user wants to start monitoring
    response = input("Start real-time monitoring now? (y/n): ").lower()
    
    if response == 'y':
        start_monitoring()
    else:
        show_usage_instructions()

if __name__ == '__main__':
    main() 