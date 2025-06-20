#!/usr/bin/env python3
"""
Test Isolation System

Provides isolated testing environments that prevent test data from
contaminating production storage, databases, and logs.
"""

import os
import tempfile
import shutil
from pathlib import Path
from typing import Dict, Any, Optional
from contextlib import contextmanager
import json
import yaml
import logging

class TestIsolationManager:
    """Manages isolated test environments"""
    
    def __init__(self, project_root: Path = None):
        self.project_root = project_root or Path.cwd()
        self.test_root = None
        self.original_env = {}
        
        # Configure logging for test isolation
        self.logger = logging.getLogger(__name__)
    
    @contextmanager
    def isolated_test_environment(self, test_name: str = "test"):
        """Context manager for isolated test environment"""
        try:
            # Create isolated environment
            self.test_root = Path(tempfile.mkdtemp(prefix=f"narrative_gravity_test_{test_name}_"))
            self.logger.info(f"🧪 Created isolated test environment: {self.test_root}")
            
            # Set up isolated directory structure
            self._setup_isolated_directories()
            
            # Set environment variables for isolation
            self._set_isolation_environment()
            
            yield self.test_root
            
        finally:
            # Cleanup isolated environment
            self._cleanup_isolated_environment()
    
    def _setup_isolated_directories(self):
        """Set up isolated directory structure"""
        # Create isolated directories
        isolated_dirs = [
            "experiments",
            "logs", 
            "asset_storage",
            "exports",
            "tmp"
        ]
        
        for dir_name in isolated_dirs:
            isolated_dir = self.test_root / dir_name
            isolated_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy essential files from production if they exist
            prod_dir = self.project_root / dir_name
            if dir_name == "asset_storage" and prod_dir.exists():
                # Copy only essential framework assets for testing
                self._copy_essential_assets(prod_dir, isolated_dir)
    
    def _copy_essential_assets(self, source_dir: Path, target_dir: Path):
        """Copy only essential assets needed for testing"""
        # Copy framework assets (needed for tests)
        framework_dir = source_dir / "framework"
        if framework_dir.exists():
            target_framework_dir = target_dir / "framework"
            target_framework_dir.mkdir(parents=True, exist_ok=True)
            
            # Copy only the MFT framework (essential for most tests)
            mft_hash_prefix = "52"  # Known MFT framework hash prefix
            mft_dir = framework_dir / mft_hash_prefix
            if mft_dir.exists():
                target_mft_dir = target_framework_dir / mft_hash_prefix
                shutil.copytree(mft_dir, target_mft_dir, dirs_exist_ok=True)
                self.logger.info(f"  📦 Copied essential framework assets to test environment")
    
    def _set_isolation_environment(self):
        """Set environment variables to isolate test data"""
        # Store original environment
        isolation_vars = [
            'NARRATIVE_GRAVITY_EXPERIMENTS_DIR',
            'NARRATIVE_GRAVITY_LOGS_DIR',
            'NARRATIVE_GRAVITY_ASSET_STORAGE_DIR',
            'NARRATIVE_GRAVITY_EXPORTS_DIR',
            'NARRATIVE_GRAVITY_DB_NAME'
        ]
        
        for var in isolation_vars:
            self.original_env[var] = os.environ.get(var)
        
        # Set isolated environment variables
        os.environ['NARRATIVE_GRAVITY_EXPERIMENTS_DIR'] = str(self.test_root / "experiments")
        os.environ['NARRATIVE_GRAVITY_LOGS_DIR'] = str(self.test_root / "logs")
        os.environ['NARRATIVE_GRAVITY_ASSET_STORAGE_DIR'] = str(self.test_root / "asset_storage")
        os.environ['NARRATIVE_GRAVITY_EXPORTS_DIR'] = str(self.test_root / "exports")
        os.environ['NARRATIVE_GRAVITY_DB_NAME'] = f"narrative_gravity_test_{os.getpid()}"
        
        self.logger.info(f"  🔒 Set isolated environment variables")
    
    def _cleanup_isolated_environment(self):
        """Clean up isolated test environment"""
        # Restore original environment
        for var, value in self.original_env.items():
            if value is None:
                os.environ.pop(var, None)
            else:
                os.environ[var] = value
        
        # Remove isolated directory
        if self.test_root and self.test_root.exists():
            shutil.rmtree(self.test_root)
            self.logger.info(f"🧹 Cleaned up isolated test environment: {self.test_root}")
    
    def create_test_experiment(self, name: str, **kwargs) -> Path:
        """Create a test experiment definition in isolated environment"""
        if not self.test_root:
            raise RuntimeError("Must be used within isolated_test_environment context")
        
        experiment_data = {
            "experiment_meta": {
                "name": f"TEST_{name}",
                "version": "v1.0.0",
                "description": f"Test experiment: {name}",
                "tags": ["test", "isolated"]
            },
            "components": {
                "frameworks": [{
                    "id": "moral_foundations_theory",
                    "version": "v2025.06.19",
                    "type": "database_lookup"
                }]
            },
            "execution": {
                "matrix": [{
                    "run_id": f"test_{name}_run_1"
                }]
            }
        }
        
        # Merge with provided kwargs
        if kwargs:
            experiment_data.update(kwargs)
        
        # Save to isolated experiments directory
        experiment_file = self.test_root / "experiments" / f"{name}_test.yaml"
        with open(experiment_file, 'w') as f:
            yaml.dump(experiment_data, f, default_flow_style=False)
        
        self.logger.info(f"  📋 Created test experiment: {experiment_file}")
        return experiment_file

# ========================================================================
# ENHANCED ORCHESTRATOR FOR TEST ISOLATION
# ========================================================================

class IsolatedOrchestrator:
    """Orchestrator that automatically uses isolated environments for tests"""
    
    def __init__(self):
        self.isolation_manager = TestIsolationManager()
        self.logger = logging.getLogger(__name__)
    
    def run_isolated_test(self, test_name: str, orchestrator_args: list = None):
        """Run orchestrator in isolated environment"""
        orchestrator_args = orchestrator_args or []
        
        with self.isolation_manager.isolated_test_environment(test_name):
            # Create test experiment
            test_experiment = self.isolation_manager.create_test_experiment(test_name)
            
            # Import orchestrator in isolated environment
            import sys
            sys.path.insert(0, str(Path(__file__).parent))
            
            try:
                from comprehensive_experiment_orchestrator import ExperimentOrchestrator
                
                # Run orchestrator with isolated settings
                orchestrator = ExperimentOrchestrator()
                
                self.logger.info(f"🚀 Running isolated test: {test_name}")
                result = orchestrator.orchestrate_experiment(
                    experiment_file=test_experiment,
                    dry_run=True  # Always dry run in tests
                )
                
                self.logger.info(f"✅ Isolated test completed: {test_name}")
                return result
                
            except Exception as e:
                self.logger.error(f"❌ Isolated test failed: {test_name} - {e}")
                raise

# ========================================================================
# INTEGRATION WITH EXISTING SYSTEMS
# ========================================================================

def setup_test_isolation_in_orchestrator():
    """Add test isolation detection to existing orchestrator"""
    
    # This would be integrated into the main orchestrator
    isolation_check = """
    def _is_test_environment(self) -> bool:
        '''Check if running in test environment'''
        test_indicators = [
            os.environ.get('NARRATIVE_GRAVITY_DB_NAME', '').startswith('narrative_gravity_test_'),
            'test' in str(self.experiment_file).lower(),
            '--test' in sys.argv,
            os.environ.get('PYTEST_CURRENT_TEST') is not None
        ]
        return any(test_indicators)
    
    def _apply_test_isolation_settings(self):
        '''Apply test-specific settings to prevent bloat'''
        if self._is_test_environment():
            # Use isolated directories
            self.experiments_dir = Path(os.environ.get('NARRATIVE_GRAVITY_EXPERIMENTS_DIR', 'experiments'))
            self.logs_dir = Path(os.environ.get('NARRATIVE_GRAVITY_LOGS_DIR', 'logs'))
            self.asset_storage_dir = Path(os.environ.get('NARRATIVE_GRAVITY_ASSET_STORAGE_DIR', 'asset_storage'))
            
            # Shorter log retention
            self.log_retention_days = 1
            
            # Test-specific database settings
            self.database_name = os.environ.get('NARRATIVE_GRAVITY_DB_NAME', 'narrative_gravity_test')
            
            logger.info("🧪 Test environment detected - using isolated settings")
    """
    
    return isolation_check

# ========================================================================
# PYTEST INTEGRATION
# ========================================================================

def pytest_configure():
    """Pytest configuration hook for automatic test isolation"""
    # This would be added to conftest.py
    pytest_integration = """
import pytest
from scripts.production.test_isolation_system import TestIsolationManager

@pytest.fixture(scope="session")
def isolated_test_env():
    '''Session-scoped isolated test environment'''
    manager = TestIsolationManager()
    with manager.isolated_test_environment("pytest_session") as test_root:
        yield test_root

@pytest.fixture(scope="function")
def test_experiment_file(isolated_test_env):
    '''Create a test experiment file for each test'''
    manager = TestIsolationManager()
    manager.test_root = isolated_test_env
    return manager.create_test_experiment("pytest_test")

# Usage in tests:
def test_orchestrator_validation(test_experiment_file):
    from comprehensive_experiment_orchestrator import ExperimentOrchestrator
    
    orchestrator = ExperimentOrchestrator()
    result = orchestrator.orchestrate_experiment(test_experiment_file, dry_run=True)
    
    assert result is not None
    # Test runs in isolation - no production data contamination!
"""
    
    return pytest_integration

def main():
    """CLI entry point for test isolation utilities"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Test Isolation System")
    parser.add_argument("--demo", action="store_true", help="Run demonstration")
    parser.add_argument("--setup-pytest", action="store_true", help="Show pytest integration")
    
    args = parser.parse_args()
    
    if args.demo:
        # Demonstrate isolated testing
        isolated_orchestrator = IsolatedOrchestrator()
        isolated_orchestrator.run_isolated_test("demo_test")
    
    elif args.setup_pytest:
        print("Add this to your conftest.py:")
        print(pytest_configure())
    
    else:
        print("Test Isolation System")
        print("Options:")
        print("  --demo: Run isolation demonstration")
        print("  --setup-pytest: Show pytest integration code")

if __name__ == "__main__":
    main() 