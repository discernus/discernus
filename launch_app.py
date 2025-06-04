#!/usr/bin/env python3
"""
Simple launcher for the Moral Gravity Wells Streamlit app
Handles dependency installation and launches the interface
"""

import subprocess
import sys
import os
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
    print("🚀 Launching Moral Gravity Wells Analysis Interface...")
    print("📱 Your browser should open automatically")
    print("🌐 If not, go to: http://localhost:8501")
    print("⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "moral_gravity_app.py",
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
    print("🎯 Moral Gravity Wells Analysis - Streamlit Interface")
    print("=" * 50)
    
    # Check if we're in the right directory
    if not Path("moral_gravity_elliptical.py").exists():
        print("❌ Error: Please run this script from the moral_gravity_analysis directory")
        sys.exit(1)
    
    # Check if streamlit is installed
    try:
        import streamlit
        print("✅ Streamlit already installed")
    except ImportError:
        print("📦 Streamlit not found - installing dependencies...")
        if not install_dependencies():
            sys.exit(1)
    
    # Launch the app
    launch_streamlit()

if __name__ == "__main__":
    main() 