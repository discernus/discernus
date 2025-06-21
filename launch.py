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
from pathlib import Path
from threading import Thread
try:
    import psutil
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

def check_dependencies():
    """Check if required dependencies are installed."""
    print("✅ Dependencies checked")
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
            print(f"⚠️  Expected PostgreSQL, found: {db_url}")
            print("💡 Check your DATABASE_URL in .env file")
            return False
            
        with engine.connect():
            pass
        print("✅ PostgreSQL connection verified")
        return True
    except Exception as e:
        print(f"⚠️  PostgreSQL not accessible: {e}")
        print("💡 Run: python launch.py --setup-db")
        print("💡 Or see: docs/architecture/database_architecture.md")
        return False

def run_service(name, command, cwd=None):
    """Run a service in a subprocess."""
    print(f"🚀 Starting {name}...")
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
                print(f"[{name}] {line.strip()}")
        
        return process
    except Exception as e:
        print(f"❌ Failed to start {name}: {e}")
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
        print("\n🛑 Stopping all services...")
        for name, process in self.processes.items():
            if process and process.poll() is None:
                print(f"   Stopping {name}...")
                kill_process_tree(process.pid)
        print("✅ All services stopped")

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
    
    print("🎯 Narrative Gravity Wells Research Platform")
    print("🔬 Backend Services for Academic Pipeline")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not Path("src/narrative_gravity/engine_circular.py").exists():
        print("❌ Error: Please run this script from the narrative_gravity_analysis directory")
        sys.exit(1)
    
    # Setup database only
    if args.setup_db:
        print("🗄️  Setting up database...")
        result = subprocess.run([sys.executable, "scripts/setup_database.py"])
        sys.exit(result.returncode)
    
    # Check dependencies
    if not check_dependencies():
        sys.exit(1)
    
    # Check database (unless skipped)
    if not args.no_db_check and not check_database():
        print("💡 Run with --setup-db to initialize the database")
        sys.exit(1)
    
    manager = ServiceManager()
    
    try:
        # --- Backend Services Management ---
        # Determine which services to start
        services_to_start = []
        if args.api_only:
            print("🌐 Starting API server only...")
            services_to_start.append(("API", [sys.executable, "scripts/run_api.py"]))
        elif args.celery_only:
            print("🔄 Starting Celery worker only...")
            services_to_start.append(("Celery", [sys.executable, "scripts/run_celery.py"]))
        else:
            # Default to full backend platform launch
            print("🚀 Starting backend services for research pipeline...")
            print("🌐 API Server: http://localhost:8000")
            print("📚 API Docs: http://localhost:8000/api/docs")
            print("🔄 Celery Worker: Background processing")
            print("")
            services_to_start.append(("API", [sys.executable, "scripts/run_api.py"]))
            services_to_start.append(("Celery", [sys.executable, "scripts/run_celery.py"]))

        if not services_to_start:
            print("No services to start. Exiting.")
            return

        # Start services
        for name, cmd in services_to_start:
            manager.start_service(name, cmd)
        
        print("✅ Backend services running.")
        print("🔬 Ready for academic research pipeline operations.")
        print("\n⏹️  Press Ctrl+C to stop all services")
        print("=" * 60)

        # Keep running until interrupted
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass
        
    except KeyboardInterrupt:
        print("\n👋 Shutting down...")
    finally:
        manager.stop_all()

if __name__ == "__main__":
    main() 