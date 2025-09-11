
Copyright (C) 2025  Discernus Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

import unittest
from unittest.mock import patch, MagicMock
import os
import yaml

# Adjust the import path based on your project structure
from discernus.core.secure_code_executor import SecureCodeExecutor
from discernus.core.llm_code_sanitizer import LLMCodeSanitizer
from discernus.core.capability_registry import CapabilityRegistry

class TestCodeExecutionInfrastructure(unittest.TestCase):
    
    def setUp(self):
        """Set up a fresh SecureCodeExecutor for each test."""
        # Create a registry instance for testing
        self.registry = CapabilityRegistry()
        self.executor = SecureCodeExecutor(timeout_seconds=5, memory_limit_mb=128, capability_registry=self.registry)

    def test_execute_safe_code_successfully(self):
        """Test that simple, safe Python code executes correctly."""
        safe_code = "my_result = 1 + 1"
        
        # Create a minimal preset for this test
        presets_dir = "test_presets_safe"
        os.makedirs(presets_dir, exist_ok=True)
        core_yaml_path = os.path.join(presets_dir, "core_capabilities.yaml")
        core_yaml_content = "name: core\nlibraries:\n  - math\n"
        with open(core_yaml_path, "w") as f:
            f.write(core_yaml_content)
        
        registry = CapabilityRegistry(presets_dir=presets_dir, extensions_dir="test_extensions_safe")
        executor = SecureCodeExecutor(capability_registry=registry)

        result = executor.execute_code(safe_code, {})
        self.assertTrue(result['success'], f"Execution failed: {result['error']}")
        self.assertIn('my_result', result['context'])
        self.assertEqual(result['context']['my_result'], 2)

        # Clean up
        os.remove(core_yaml_path)
        os.rmdir(presets_dir)

    def test_prevent_file_system_access(self):
        """Test that code attempting to access the file system is blocked."""
        malicious_code = "import os; os.listdir('/')"
        result = self.executor.execute_code(malicious_code, {})
        self.assertFalse(result['success'])
        self.assertIn("Security violations", result['error'])

    def test_prevent_network_access(self):
        """Test that code attempting to make network calls is blocked."""
        malicious_code = "import socket; socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect(('google.com', 80))"
        result = self.executor.execute_code(malicious_code, {})
        self.assertFalse(result['success'])
        self.assertIn("Security violations", result['error'])
        
    def test_execution_timeout(self):
        """Test that code exceeding the timeout limit is terminated."""
        slow_code = "while True: pass"
        executor_short_timeout = SecureCodeExecutor(timeout_seconds=1, memory_limit_mb=128)
        result = executor_short_timeout.execute_code(slow_code, {})
        self.assertFalse(result['success'])
        self.assertIn("timed out", result['error'])

    def test_sanitizer_removes_problematic_wrappers(self):
        """Test that the sanitizer removes markdown and python wrappers."""
        code_with_wrappers = """```python
def calculate():
    return 10
result = calculate()
```"""
        sanitizer = LLMCodeSanitizer()
        sanitized_code, _ = sanitizer.sanitize_code(code_with_wrappers)
        self.assertNotIn("```python", sanitized_code)
        self.assertNotIn("```", sanitized_code)
        self.assertTrue(sanitized_code.strip().startswith("def calculate():"))

    def test_sanitizer_handles_clean_code(self):
        """Test that the sanitizer doesn't alter already-clean code."""
        clean_code = "result = 5 * 5"
        sanitizer = LLMCodeSanitizer()
        sanitized_code, _ = sanitizer.sanitize_code(clean_code)
        self.assertEqual(clean_code.strip(), sanitized_code.strip())

    def test_capability_registry_loads_and_checks_permissions(self):
        """Test the CapabilityRegistry loads from YAML and correctly checks permissions."""
        
        # Create a dummy presets and extensions dir for the test
        presets_dir = "test_presets"
        extensions_dir = "test_extensions"
        os.makedirs(presets_dir, exist_ok=True)
        os.makedirs(extensions_dir, exist_ok=True)
        
        core_yaml_path = os.path.join(presets_dir, "core_capabilities.yaml")
        core_yaml_content = "name: core\nlibraries:\n  - math\n"
        with open(core_yaml_path, "w") as f:
            f.write(core_yaml_content)

        ext_yaml_path = os.path.join(extensions_dir, "test_extension.yaml")
        ext_yaml_content = "name: test_ext\nlibraries:\n  - my_test_lib\n"
        with open(ext_yaml_path, "w") as f:
            f.write(ext_yaml_content)
        
        registry = CapabilityRegistry(extensions_dir=extensions_dir, presets_dir=presets_dir)

        # Test allowed operations (core + extended)
        allowed_libs = registry.get_allowed_libraries()
        self.assertIn("math", allowed_libs) # Core lib from test preset
        self.assertIn("my_test_lib", allowed_libs) # Extended lib
        
        # Test disallowed operations
        self.assertNotIn("os", allowed_libs)

        # Clean up the dummy files and dirs
        os.remove(core_yaml_path)
        os.remove(ext_yaml_path)
        os.rmdir(presets_dir)
        os.rmdir(extensions_dir)


    def test_integration_executor_with_capability_registry(self):
        """Test that the executor uses the registry to allow/disallow imports."""
        # Create a dummy presets and extensions dir for the test
        presets_dir = "test_presets_int"
        extensions_dir = "test_extensions_int"
        os.makedirs(presets_dir, exist_ok=True)
        os.makedirs(extensions_dir, exist_ok=True)
        
        core_yaml_path = os.path.join(presets_dir, "core_capabilities.yaml")
        core_yaml_content = "name: core\nlibraries:\n  - pandas\n"
        with open(core_yaml_path, "w") as f:
            f.write(core_yaml_content)
        
        # Create a new registry that will load the extension
        registry = CapabilityRegistry(extensions_dir=extensions_dir, presets_dir=presets_dir)
        executor_with_registry = SecureCodeExecutor(capability_registry=registry)
        
        # This code should be allowed because 'pandas' is in our test core preset
        allowed_code = "import pandas as pd; df = pd.DataFrame()"
        result = executor_with_registry.execute_code(allowed_code, {})
        self.assertTrue(result['success'], f"Execution failed unexpectedly: {result['error']}")

        # This code should be blocked because 'tkinter' is not in the registry
        disallowed_code = "import tkinter"
        result = executor_with_registry.execute_code(disallowed_code, {})
        self.assertFalse(result['success'])
        self.assertIn("Forbidden import: tkinter", result['error'])

        # Clean up
        os.remove(core_yaml_path)
        os.rmdir(presets_dir)
        os.rmdir(extensions_dir)

if __name__ == '__main__':
    unittest.main()
