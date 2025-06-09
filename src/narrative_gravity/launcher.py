#!/usr/bin/env python3
"""
Simple launcher for the Narrative Gravity Wells Streamlit app
Handles dependency installation and launches the interface
"""

import subprocess
import sys
import os
import argparse
from pathlib import Path

def install_dependencies():
    """Install required dependencies"""
    print("🔧 Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {e}")
        return False

def launch_streamlit():
    """Launch the Streamlit app"""
    print("🚀 Launching Narrative Gravity Maps Interface...")
    print("📱 Your browser should open automatically")
    print("🌐 If not, go to: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "src/narrative_gravity/app.py",
            "--server.headless", "false",
            "--server.address", "localhost",
            "--server.port", "8501"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error launching app: {e}")

def main():
    """Main launcher function"""
    parser = argparse.ArgumentParser(
        prog='launch_app.py',
        description='Launch the Narrative Gravity Maps Streamlit interface',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python launch_app.py           # Launch the app normally
  python launch_app.py --help    # Show this help message
        """
    )
    
    parser.add_argument(
        '--no-install', 
        action='store_true',
        help='Skip dependency installation check'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=8501,
        help='Port to run the Streamlit app on (default: 8501)'
    )
    
    args = parser.parse_args()
    
    print("🎯 Narrative Gravity Maps - Streamlit Interface")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("src/narrative_gravity/engine.py").exists():
        print("❌ Error: Please run this script from the narrative_gravity_analysis directory")
        sys.exit(1)
    
    # Check if streamlit is installed (unless skipped)
    if not args.no_install:
        try:
            import streamlit
            print("✅ Streamlit already installed")
        except ImportError:
            print("📦 Streamlit not found - installing dependencies...")
            if not install_dependencies():
                sys.exit(1)
    
    # Launch the app
    launch_streamlit_with_port(args.port)

def launch_streamlit_with_port(port=8501):
    """Launch the Streamlit app on specified port"""
    print("🚀 Launching Narrative Gravity Maps Interface...")
    print("📱 Your browser should open automatically")
    print(f"🌐 If not, go to: http://localhost:{port}")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "src/narrative_gravity/app.py",
            "--server.headless", "false",
            "--server.address", "localhost",
            "--server.port", str(port)
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error launching app: {e}")

if __name__ == "__main__":
    main() 