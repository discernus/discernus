#!/usr/bin/env python3
"""
Simple launcher for Streamlit Chat Interface
"""

import subprocess
import sys
import os
from pathlib import Path

def main():
    """Launch the Streamlit chat interface"""
    print("🎯 Launching Narrative Gravity Streamlit Chat...")
    print("🌐 Opening: http://localhost:8501")
    print("💬 Chat interface with your existing AI backend")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 50)
    
    try:
        # Launch Streamlit
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "streamlit_chat.py",
            "--server.port=8501",
            "--server.headless=false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Chat interface stopped")
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Make sure you're in the narrative_gravity_analysis directory")
        print("💡 And that streamlit is installed: pip install streamlit")

if __name__ == "__main__":
    main() 