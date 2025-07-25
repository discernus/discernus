#!/usr/bin/env python3
"""
Background Executor - Autonomous execution environment for Discernus
Handles virtual environment activation, background processes, and logging
without requiring user interaction.
"""

import os
import sys
import subprocess
import logging
import time
import threading
import signal
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Union

# Get the current Python executable (works in any environment)
PYTHON_EXECUTABLE = sys.executable

# Configure logging
log_dir = Path("logs/background_executor")
log_dir.mkdir(parents=True, exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_dir / f"executor_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class BackgroundExecutor:
    """Autonomous execution environment for development workflows"""
    
    def __init__(self, project_root: str = "/Volumes/code/discernus"):
        self.project_root = Path(project_root)
        self.venv_path = self.project_root / "venv" / "bin" / "activate"
        self.processes: Dict[str, subprocess.Popen] = {}
        self.running = True
        
        # Ensure we're in the right directory
        os.chdir(self.project_root)
        logger.info(f"Background executor initialized in {self.project_root}")
        
    def _get_venv_command(self, command: str) -> str:
        """Wrap command with virtual environment activation"""
        return f"source {self.venv_path} && {command}"
    
    def start_service(self, name: str, command: str, use_venv: bool = True) -> bool:
        """Start a background service with logging"""
        try:
            if name in self.processes:
                logger.warning(f"Service {name} already running")
                return True
                
            # Prepare command with venv if needed
            if use_venv:
                full_command = self._get_venv_command(command)
            else:
                full_command = command
                
            logger.info(f"Starting service {name}: {full_command}")
            
            # Create log file for this service
            service_log = log_dir / f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
            
            # Start process
            process = subprocess.Popen(
                full_command,
                shell=True,
                cwd=self.project_root,
                stdout=open(service_log, 'w'),
                stderr=subprocess.STDOUT,
                preexec_fn=os.setsid  # Create new process group
            )
            
            self.processes[name] = process
            logger.info(f"Service {name} started with PID {process.pid}, logging to {service_log}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start service {name}: {e}")
            return False
    
    def stop_service(self, name: str) -> bool:
        """Stop a background service"""
        try:
            if name not in self.processes:
                logger.warning(f"Service {name} not found")
                return False
                
            process = self.processes[name]
            if process.poll() is None:  # Still running
                logger.info(f"Stopping service {name} (PID {process.pid})")
                os.killpg(os.getpgid(process.pid), signal.SIGTERM)
                
                # Wait for graceful shutdown
                try:
                    process.wait(timeout=10)
                except subprocess.TimeoutExpired:
                    logger.warning(f"Force killing service {name}")
                    os.killpg(os.getpgid(process.pid), signal.SIGKILL)
                    
            del self.processes[name]
            logger.info(f"Service {name} stopped")
            return True
            
        except Exception as e:
            logger.error(f"Failed to stop service {name}: {e}")
            return False
    
    def run_command(self, command: str, use_venv: bool = True, timeout: Optional[int] = None) -> tuple[int, str, str]:
        """Run a command and return results"""
        try:
            if use_venv:
                full_command = self._get_venv_command(command)
            else:
                full_command = command
                
            logger.info(f"Running command: {full_command}")
            
            result = subprocess.run(
                full_command,
                shell=True,
                cwd=self.project_root,
                capture_output=True,
                text=True,
                timeout=timeout
            )
            
            logger.info(f"Command completed with exit code {result.returncode}")
            if result.stdout:
                logger.debug(f"STDOUT: {result.stdout[:500]}...")
            if result.stderr:
                logger.debug(f"STDERR: {result.stderr[:500]}...")
                
            return result.returncode, result.stdout, result.stderr
            
        except subprocess.TimeoutExpired:
            logger.error(f"Command timed out after {timeout} seconds")
            return -1, "", "Command timed out"
        except Exception as e:
            logger.error(f"Command failed: {e}")
            return -1, "", str(e)
    
    def check_service_health(self, name: str) -> bool:
        """Check if a service is still running"""
        if name not in self.processes:
            return False
            
        process = self.processes[name]
        return process.poll() is None
    
    def get_service_status(self) -> Dict[str, str]:
        """Get status of all services"""
        status = {}
        for name, process in self.processes.items():
            if process.poll() is None:
                status[name] = f"RUNNING (PID {process.pid})"
            else:
                status[name] = f"STOPPED (exit code {process.returncode})"
        return status
    
    def start_discernus_infrastructure(self) -> bool:
        """Start all required Discernus services"""
        logger.info("Starting Discernus infrastructure...")
        
        # Start Redis (if not running)
        redis_check = self.run_command("lsof -i :6379", use_venv=False, timeout=5)
        if redis_check[0] != 0:
            logger.info("Starting Redis...")
            self.start_service("redis", "redis-server", use_venv=False)
            time.sleep(2)
        else:
            logger.info("Redis already running")
        
        # Start MinIO (if not running) 
        minio_check = self.run_command("lsof -i :9000", use_venv=False, timeout=5)
        if minio_check[0] != 0:
            logger.info("Starting MinIO...")
            self.start_service("minio", "minio server data --console-address :9001", use_venv=False)
            time.sleep(3)
        else:
            logger.info("MinIO already running")
            
        # Start Router
        logger.info("Starting Router...")
        self.start_service("router", f"{PYTHON_EXECUTABLE} scripts/router.py", use_venv=False)
        time.sleep(2)
        
        # Verify all services
        time.sleep(5)
        status = self.get_service_status()
        logger.info(f"Service status: {status}")
        
        return all("RUNNING" in s for s in status.values())
    
    def monitor_services(self, check_interval: int = 30):
        """Monitor services and restart if needed"""
        logger.info(f"Starting service monitor (check every {check_interval}s)")
        
        while self.running:
            try:
                # Check each service
                for name in list(self.processes.keys()):
                    if not self.check_service_health(name):
                        logger.warning(f"Service {name} died, restarting...")
                        
                        # Restart based on service type
                        if name == "router":
                            self.start_service("router", f"{PYTHON_EXECUTABLE} scripts/router.py", use_venv=False)
                        elif name == "redis":
                            self.start_service("redis", "redis-server", use_venv=False)
                        elif name == "minio":
                            self.start_service("minio", "minio server data --console-address :9001", use_venv=False)
                
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                logger.info("Service monitor shutdown requested")
                break
            except Exception as e:
                logger.error(f"Service monitor error: {e}")
                time.sleep(check_interval)
    
    def run_test(self, test_name: str, timeout: int = 600) -> bool:
        """Run a test with proper logging and timeout"""
        logger.info(f"Running test: {test_name}")
        
        if test_name == "phase3_pipeline":
            command = f"{PYTHON_EXECUTABLE} scripts/phase3_test_runner.py --test full_pipeline"
        else:
            logger.error(f"Unknown test: {test_name}")
            return False
            
        exit_code, stdout, stderr = self.run_command(command, use_venv=True, timeout=timeout)
        
        if exit_code == 0:
            logger.info(f"Test {test_name} PASSED")
            return True
        else:
            logger.error(f"Test {test_name} FAILED with exit code {exit_code}")
            if stdout:
                logger.error(f"STDOUT: {stdout}")
            if stderr:
                logger.error(f"STDERR: {stderr}")
            return False
    
    def shutdown(self):
        """Graceful shutdown of all services"""
        logger.info("Shutting down background executor...")
        self.running = False
        
        # Stop all services
        for name in list(self.processes.keys()):
            self.stop_service(name)
            
        logger.info("Background executor shutdown complete")

def main():
    """Main entry point"""
    executor = BackgroundExecutor()
    
    try:
        # Set up signal handlers
        def signal_handler(signum, frame):
            logger.info(f"Received signal {signum}, shutting down...")
            executor.shutdown()
            sys.exit(0)
            
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        
        # Start infrastructure
        if executor.start_discernus_infrastructure():
            logger.info("Discernus infrastructure started successfully")
            
            # Start monitoring in background thread
            monitor_thread = threading.Thread(target=executor.monitor_services, daemon=True)
            monitor_thread.start()
            
            # Run tests or interactive mode
            if len(sys.argv) > 1:
                if sys.argv[1] == "test":
                    test_name = sys.argv[2] if len(sys.argv) > 2 else "phase3_pipeline"
                    success = executor.run_test(test_name)
                    sys.exit(0 if success else 1)
                elif sys.argv[1] == "status":
                    status = executor.get_service_status()
                    for name, state in status.items():
                        print(f"{name}: {state}")
                    sys.exit(0)
            
            # Interactive mode - keep running
            logger.info("Background executor ready - services running autonomously")
            logger.info("Press Ctrl+C to shutdown")
            
            while executor.running:
                time.sleep(1)
                
        else:
            logger.error("Failed to start infrastructure")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Shutdown requested")
    except Exception as e:
        logger.error(f"Background executor failed: {e}")
        sys.exit(1)
    finally:
        executor.shutdown()

if __name__ == "__main__":
    main() 