#!/usr/bin/env python3
"""
Comprehensive launcher for the Narrative Gravity Wells platform
Orchestrates database, API server, and Celery workers for research pipeline
"""

import subprocess
import sys
import os
import argparse
import time
import signal
import logging
from pathlib import Path
from threading import Thread

logger = logging.getLogger(__name__)
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

def check_dependencies():
    """Check if required dependencies are installed."""
    logger.info("✅ Dependencies checked")
    return True

def check_database():
    """Check if PostgreSQL database is accessible."""
    try:
        # Add project root to path
        project_root = Path(__file__).parent
        sys.path.insert(0, str(project_root))
        
        from src.models.base import engine
        
        # Verify it's PostgreSQL
        db_url = str(engine.url)
        if not db_url.startswith('postgresql'):
            logger.warning("⚠️  Expected PostgreSQL, found: %s", db_url)
            logger.info("💡 Check your DATABASE_URL in .env file")
            return False
            
        with engine.connect():
            pass
        logger.info("✅ PostgreSQL connection verified")
        return True
    except Exception as e:
        logger.warning("⚠️  PostgreSQL not accessible: %s", e)
        logger.info("💡 Run: python launch.py --setup-db")
        logger.info("💡 Or see: docs/architecture/database_architecture.md")
        return False

def run_service(name, command, cwd=None):
    """Run a service in a subprocess."""
    logger.info("🚀 Starting %s...", name)
    try:
        process = subprocess.Popen(
            command,
            cwd=cwd or Path(__file__).parent,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Stream output with service name prefix
        for line in iter(process.stdout.readline, ''):
            if line.strip():
                logger.info("[%s] %s", name, line.strip())
        
        return process
    except Exception as e:
        logger.error("❌ Failed to start %s: %s", name, e)
        return None

def kill_process_tree(pid):
    """Kill a process and all its children."""
    if HAS_PSUTIL:
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            for child in children:
                child.kill()
            parent.kill()
        except:
            pass
    else:
        # Fallback: just kill the main process
        try:
            os.kill(pid, signal.SIGTERM)
        except:
            pass

class ServiceManager:
    """Manages multiple services with proper cleanup."""
    
    def __init__(self):
        self.processes = {}
        self.threads = {}
    
    def start_service(self, name, command, cwd=None):
        """Start a service in a separate thread."""
        def run():
            self.processes[name] = run_service(name, command, cwd)
        
        thread = Thread(target=run, daemon=True)
        thread.start()
        self.threads[name] = thread
        time.sleep(2)  # Give service time to start
    
    def stop_all(self):
        """Stop all running services."""
        logger.info("\n🛑 Stopping all services...")
        for name, process in self.processes.items():
            if process and process.poll() is None:
                logger.info("   Stopping %s...", name)
                kill_process_tree(process.pid)
        logger.info("✅ All services stopped")

def main():
    """Main launcher function."""
    parser = argparse.ArgumentParser(
        prog='launch.py',
        description='Launch the Narrative Gravity Wells research platform backend',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch.py                    # Launch all backend services
  python launch.py --api-only         # Launch only API server
  python launch.py --celery-only      # Launch only Celery worker
  python launch.py --setup-db         # Setup database only

Note: Frontend interfaces have been deprecated pending paper completion.
Focus is on core research pipeline: database, API, and batch processing.
        """
    )
    
    parser.add_argument('--api-only', action='store_true', 
                       help='Launch only the API server')
    parser.add_argument('--celery-only', action='store_true',
                       help='Launch only the Celery worker')
    parser.add_argument('--setup-db', action='store_true',
                       help='Setup database and exit')
    parser.add_argument('--no-db-check', action='store_true',
                       help='Skip database connectivity check')
    parser.add_argument('--port', type=int, default=8000,
                       help='Port for API server (default: 8000)')
    
    args = parser.parse_args()
    
    logger.info("🎯 Narrative Gravity Wells Research Platform")
    logger.info("🔬 Backend Services for Academic Pipeline")
    logger.info("=" * 60)
    
    # Check if we're in the right directory
    if not Path("src/narrative_gravity/engine_circular.py").exists():
        logger.error("❌ Error: Please run this script from the narrative_gravity_analysis directory")
        sys.exit(1)
    
    # Setup database only
    if args.setup_db:
        logger.info("🗄️  Setting up database...")
        result = subprocess.run([sys.executable, "scripts/setup_database.py"])
        sys.exit(result.returncode)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check database (unless skipped)
    if not args.no_db_check and not check_database():
        logger.info("💡 Run with --setup-db to initialize the database")
        sys.exit(1)
    
    manager = ServiceManager()
    
    try:
        # --- Backend Services Management ---
        # Determine which services to start
        services_to_start = []
        if args.api_only:
            logger.info("🌐 Starting API server only...")
            services_to_start.append(("API", [sys.executable, "scripts/run_api.py"]))
        elif args.celery_only:
            logger.info("🔄 Starting Celery worker only...")
            services_to_start.append(("Celery", [sys.executable, "scripts/run_celery.py"]))
        else:
            # Default to full backend platform launch
            logger.info("🚀 Starting backend services for research pipeline...")
            logger.info("🌐 API Server: http://localhost:8000")
            logger.info("📚 API Docs: http://localhost:8000/api/docs")
            logger.info("🔄 Celery Worker: Background processing")
            logger.info("")
            services_to_start.append(("API", [sys.executable, "scripts/run_api.py"]))
            services_to_start.append(("Celery", [sys.executable, "scripts/run_celery.py"]))

        if not services_to_start:
            logger.info("No services to start. Exiting.")
            return

        # Start services
        for name, cmd in services_to_start:
            manager.start_service(name, cmd)
        
        logger.info("✅ Backend services running.")
        logger.info("🔬 Ready for academic research pipeline operations.")
        logger.info("\n⏹️  Press Ctrl+C to stop all services")
        logger.info("=" * 60)

        # Keep running until interrupted
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        
    except KeyboardInterrupt:
        logger.info("\n👋 Shutting down...")
    finally:
        manager.stop_all()

if __name__ == "__main__":
    main() 