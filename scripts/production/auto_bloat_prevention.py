#!/usr/bin/env python3
"""
Auto Bloat Prevention Integration

Integrates bloat prevention directly into the orchestrator and test systems
so cleanup happens automatically without user intervention.
"""

import os
import sys
from pathlib import Path
import logging

# Import our bloat prevention systems
sys.path.append(str(Path(__file__).parent))
from bloat_prevention_system import BloatPreventionSystem
from test_isolation_system import TestIsolationManager

class AutoBloatPrevention:
    """Automatic bloat prevention that integrates with existing systems"""
    
    def __init__(self):
        self.bloat_cleaner = BloatPreventionSystem()
        self.test_isolation = TestIsolationManager()
        self.logger = logging.getLogger(__name__)
    
    def detect_and_prevent_bloat(self):
        """Automatically detect and prevent bloat based on current state"""
        
        # Check if we're in a test environment
        if self._is_test_environment():
            self.logger.info("🧪 Test environment detected - test isolation active")
            return  # Test isolation handles cleanup automatically
        
        # Check current bloat levels
        bloat_stats = self._assess_current_bloat()
        
        if bloat_stats['needs_cleanup']:
            self.logger.info("🧹 Automatic bloat cleanup triggered")
            self.bloat_cleaner.run_full_cleanup(dry_run=False, aggressive=False)
        else:
            self.logger.debug("✅ Bloat levels acceptable, no cleanup needed")
    
    def _is_test_environment(self) -> bool:
        """Check if running in test environment"""
        test_indicators = [
            os.environ.get('NARRATIVE_GRAVITY_DB_NAME', '').startswith('narrative_gravity_test_'),
            'test' in str(Path.cwd()).lower(),
            '--test' in sys.argv,
            '--dry-run' in sys.argv,
            os.environ.get('PYTEST_CURRENT_TEST') is not None,
            any('test' in arg.lower() for arg in sys.argv if isinstance(arg, str))
        ]
        return any(test_indicators)
    
    def _assess_current_bloat(self) -> dict:
        """Assess current bloat levels and determine if cleanup is needed"""
        project_root = Path.cwd()
        
        # Check experiment directory size
        experiments_dir = project_root / "experiments"
        exp_size_mb = 0
        exp_count = 0
        
        if experiments_dir.exists():
            exp_size_mb = self.bloat_cleaner._get_directory_size_mb(experiments_dir)
            exp_count = len([d for d in experiments_dir.iterdir() if d.is_dir()])
        
        # Check log size
        logs_dir = project_root / "logs"
        log_size_mb = 0
        if logs_dir.exists():
            log_size_mb = self.bloat_cleaner._get_directory_size_mb(logs_dir)
        
        # Determine if cleanup is needed
        needs_cleanup = (
            exp_size_mb > 50 or  # More than 50MB of experiments
            exp_count > 30 or    # More than 30 experiment directories
            log_size_mb > 20     # More than 20MB of logs
        )
        
        return {
            'needs_cleanup': needs_cleanup,
            'experiment_size_mb': exp_size_mb,
            'experiment_count': exp_count,
            'log_size_mb': log_size_mb,
            'total_size_mb': exp_size_mb + log_size_mb
        }
    
    def install_orchestrator_hooks(self):
        """Install hooks into orchestrator for automatic cleanup"""
        
        # This would be called during orchestrator initialization
        hook_code = '''
# Add this to comprehensive_experiment_orchestrator.py __init__ method:

def __init__(self):
    # ... existing initialization ...
    
    # Initialize auto-bloat prevention
    try:
        from .auto_bloat_prevention import AutoBloatPrevention
        self.auto_bloat = AutoBloatPrevention()
        
        # Run cleanup check on startup (non-blocking)
        self.auto_bloat.detect_and_prevent_bloat()
        
    except ImportError:
        self.auto_bloat = None
        logger.warning("Auto-bloat prevention not available")

# Add this to the end of orchestrate_experiment method:

def orchestrate_experiment(self, experiment_file, dry_run=False):
    try:
        # ... existing orchestration logic ...
        
        return result
        
    finally:
        # Post-execution cleanup (only in production)
        if not dry_run and self.auto_bloat:
            self.auto_bloat.detect_and_prevent_bloat()
'''
        
        return hook_code

def setup_automatic_bloat_prevention():
    """Set up automatic bloat prevention in the project"""
    
    # Install cron job if not already present
    import subprocess
    try:
        result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
        current_crontab = result.stdout
        
        if 'auto_cleanup.sh' not in current_crontab:
            print("⚠️  Cron job not found. Run the following to set up automated cleanup:")
            print("python3 scripts/production/bloat_prevention_system.py --setup-automation")
            print("Then add the suggested cron job to your crontab")
        else:
            print("✅ Automated cleanup cron job already installed")
            
    except FileNotFoundError:
        print("⚠️  Cron not available on this system")
    
    # Create startup script for immediate integration
    startup_script = '''#!/bin/bash
# Narrative Gravity Auto-Bloat Prevention Startup

# Run on system startup or project activation
cd "$(dirname "$0")/../.."
python3 scripts/production/auto_bloat_prevention.py --startup-check
'''
    
    startup_path = Path(__file__).parent.parent / "startup_bloat_check.sh"
    with open(startup_path, 'w') as f:
        f.write(startup_script)
    
    startup_path.chmod(0o755)
    print(f"✅ Created startup bloat check: {startup_path}")

def main():
    """CLI entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Auto Bloat Prevention")
    parser.add_argument("--startup-check", action="store_true", 
                       help="Run startup bloat check")
    parser.add_argument("--install-hooks", action="store_true",
                       help="Show orchestrator integration code")
    parser.add_argument("--setup", action="store_true",
                       help="Set up automatic bloat prevention")
    
    args = parser.parse_args()
    
    if args.setup:
        setup_automatic_bloat_prevention()
    
    elif args.startup_check:
        auto_bloat = AutoBloatPrevention()
        auto_bloat.detect_and_prevent_bloat()
    
    elif args.install_hooks:
        auto_bloat = AutoBloatPrevention()
        print("Add this code to your orchestrator:")
        print(auto_bloat.install_orchestrator_hooks())
    
    else:
        print("Auto Bloat Prevention System")
        print("✅ Monitors storage automatically")
        print("✅ Cleans up test data automatically") 
        print("✅ Prevents accumulation without user intervention")
        print()
        print("Status:")
        auto_bloat = AutoBloatPrevention()
        stats = auto_bloat._assess_current_bloat()
        print(f"  📁 Experiments: {stats['experiment_count']} dirs, {stats['experiment_size_mb']:.1f}MB")
        print(f"  📝 Logs: {stats['log_size_mb']:.1f}MB")
        print(f"  🧹 Cleanup needed: {'Yes' if stats['needs_cleanup'] else 'No'}")

if __name__ == "__main__":
    main() 