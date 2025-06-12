#!/usr/bin/env python3
"""
Launch Script for Chainlit Narrative Gravity Analysis Interface
"""

import sys
import subprocess
from pathlib import Path
import os

def check_dependencies():
    """Check if chainlit is installed"""
    try:
        import chainlit
        print("✅ Chainlit is installed")
        return True
    except ImportError:
        print("❌ Chainlit not found. Please install dependencies:")
        print("   pip install -r requirements.txt")
        return False

def setup_environment():
    """Set up environment variables and paths"""
    
    # Set up project root path
    project_root = Path(__file__).parent
    
    # Add project to Python path
    if str(project_root) not in sys.path:
        sys.path.insert(0, str(project_root))
    
    # Set environment variables if not already set
    env_file = project_root / ".env"
    if env_file.exists():
        print("📄 Loading environment from .env file")
        from dotenv import load_dotenv
        load_dotenv(env_file)
    else:
        print("⚠️  No .env file found, using defaults")
    
    return project_root

def launch_chainlit(project_root):
    """Launch the chainlit interface"""
    
    chainlit_file = project_root / "src" / "narrative_gravity" / "chatbot" / "chainlit_chat.py"
    
    if not chainlit_file.exists():
        print(f"❌ Chainlit file not found: {chainlit_file}")
        return False
    
    print("🚀 Starting Chainlit Narrative Gravity Analysis Interface")
    print("🌐 Interface will be available at: http://localhost:8000")
    print("📝 Supports advanced conversational political discourse analysis")
    print()
    print("💡 Features:")
    print("   • Multi-framework analysis (Fukuyama Identity, Civic Virtue, etc.)")
    print("   • Framework switching mid-conversation")
    print("   • Custom framework creation")
    print("   • Large text support (up to 1.2MB)")
    print("   • Interactive action buttons")
    print("   • Professional UI with custom styling")
    print()
    
    try:
        # Launch using chainlit run command
        cmd = [
            sys.executable, "-m", "chainlit", "run", 
            str(chainlit_file),
            "--host", "0.0.0.0",
            "--port", "8002"
        ]
        
        print(f"🔧 Running command: {' '.join(cmd)}")
        print("📋 Press Ctrl+C to stop the interface")
        print("=" * 60)
        
        subprocess.run(cmd, cwd=project_root)
        
    except KeyboardInterrupt:
        print("\n\n🛑 Chainlit interface stopped by user")
        return True
    except Exception as e:
        print(f"❌ Error launching chainlit: {e}")
        return False

def main():
    """Main launch function"""
    
    print("🎯 Narrative Gravity Analysis - Chainlit Interface Launcher")
    print("=" * 60)
    
    # Check dependencies
    if not check_dependencies():
        return False
    
    # Setup environment
    project_root = setup_environment()
    
    # Launch chainlit
    return launch_chainlit(project_root)

if __name__ == "__main__":
    success = main()
    if not success:
        sys.exit(1) 