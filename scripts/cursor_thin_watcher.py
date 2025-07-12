#!/usr/bin/env python3
"""
Cursor THIN Watcher - Real-time detection of THICK patterns
============================================================

Monitors Python files for THICK antipatterns and creates warning files
that Cursor can see to alert about violations.
"""

import time
import threading
from pathlib import Path
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class CursorTHINWatcher(FileSystemEventHandler):
    """Watch for THICK patterns in Python files"""
    
    def __init__(self):
        self.last_warnings = {}
        self.warning_cooldown = 5  # seconds between warnings for same file
        
    def on_modified(self, event):
        if event.is_directory or not event.src_path.endswith('.py'):
            return
            
        filepath = Path(event.src_path)
        
        # Skip if warning recently shown for this file
        if self.is_on_cooldown(filepath):
            return
            
        try:
            content = filepath.read_text()
            violations = self.detect_thick_patterns(content)
            
            if violations:
                self.create_warning_file(filepath, violations)
                self.last_warnings[str(filepath)] = time.time()
                
        except Exception as e:
            # Skip files that can't be read
            pass
    
    def is_on_cooldown(self, filepath):
        """Check if file is on warning cooldown"""
        last_warning = self.last_warnings.get(str(filepath), 0)
        return time.time() - last_warning < self.warning_cooldown
    
    def detect_thick_patterns(self, content):
        """Detect THICK patterns in Python code"""
        violations = []
        
        # THICK imports
        if 'import re' in content or 'from re import' in content:
            violations.append("❌ THICK: Regex import - use LLM for parsing")
        
        if 'import regex' in content:
            violations.append("❌ THICK: Regex import - use LLM for parsing")
            
        if 'from bs4 import' in content or 'import bs4' in content:
            violations.append("❌ THICK: HTML parsing - use LLM for extraction")
            
        if 'import xml.etree' in content:
            violations.append("❌ THICK: XML parsing - use LLM for extraction")
        
        # THICK function names
        thick_functions = ['parse_', 'extract_', 'validate_', 'analyze_', 'process_']
        for func in thick_functions:
            if f'def {func}' in content:
                violations.append(f"❌ THICK: Function 'def {func}' - use LLM calls instead")
        
        # Complex conditional logic
        if_count = content.count('if ') + content.count('elif ')
        if if_count > 5:  # More forgiving than 3 for entire file
            violations.append(f"❌ THICK: {if_count} if/elif statements - use LLM logic")
        
        # String manipulation
        string_methods = ['.split(', '.replace(', '.strip(', '.find(', '.index(']
        for method in string_methods:
            if method in content:
                violations.append(f"❌ THICK: String manipulation '{method}' - use LLM formatting")
                break  # Only report once per file
        
        # Regex usage
        regex_patterns = ['re.search(', 're.match(', 're.findall(', 're.sub(']
        for pattern in regex_patterns:
            if pattern in content:
                violations.append(f"❌ THICK: Regex pattern '{pattern}' - use LLM parsing")
                break
        
        # Missing LLM usage in obvious places
        if violations and 'llm_client' not in content and 'call_llm' not in content:
            violations.append("💡 MISSING: No LLM usage detected - should use llm_client.call_llm()")
        
        return violations
    
    def create_warning_file(self, filepath, violations):
        """Create warning file that Cursor can see"""
        warning_file = filepath.parent / f".THICK_WARNING_{filepath.name}"
        
        warning_content = f"""🚨 THICK PATTERNS DETECTED in {filepath.name}
{'=' * 60}

{chr(10).join(violations)}

💡 THIN SOLUTION:
- Replace parsing logic with: llm_client.call_llm("Parse this: {{content}}")
- Use LLM for content processing: llm_client.call_llm("Process this: {{data}}")
- Keep functions under 50 lines
- Simple orchestration only: read → LLM → store

✅ THIN PATTERN EXAMPLE:
```python
def load_framework(path):
    content = Path(path).read_text()
    validation = llm_client.call_llm(f"Validate framework: {{content}}")
    return {{'content': content, 'validation': validation}}
```

🛑 STOP WRITING THICK CODE!
Use LLM calls for ANY content processing.
"""
        
        warning_file.write_text(warning_content)
        
        # Auto-delete warning after 30 seconds
        def cleanup():
            time.sleep(30)
            if warning_file.exists():
                warning_file.unlink()
        
        threading.Thread(target=cleanup, daemon=True).start()
        
        print(f"⚠️  THICK WARNING: {filepath.name}")
        print(f"   {len(violations)} violations detected")
        print(f"   Created warning file for Cursor")

def start_watcher():
    """Start the THIN watcher"""
    print("🔍 Cursor THIN Watcher Started")
    print("=" * 50)
    print("Monitoring Python files for THICK patterns...")
    print("Will create warning files when violations detected")
    print("Press Ctrl+C to stop")
    print()
    
    event_handler = CursorTHINWatcher()
    observer = Observer()
    observer.schedule(event_handler, '.', recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        print("\n👋 Cursor THIN Watcher stopped")
        
        # Clean up any remaining warning files
        for warning_file in Path('.').rglob('.THICK_WARNING_*'):
            warning_file.unlink()
        print("🧹 Cleaned up warning files")
    
    observer.join()

if __name__ == '__main__':
    start_watcher() 