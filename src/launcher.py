#!/usr/bin/env python3
"""
🚨 DEPRECATED: Streamlit Interface Launcher

This launcher previously started the Streamlit interface, which has been deprecated.
Please use the modern React Research Workbench instead.
"""

import sys
from pathlib import Path

def show_migration_info():
    """Show information about migrating to React interface"""
    print("🚨 STREAMLIT INTERFACE DEPRECATED")
    print("=" * 50)
    print("The Streamlit interface has been replaced with a modern React research workbench.")
    print("")
    print("🎯 NEW REACT INTERFACE:")
    print("   📁 Location: frontend/")
    print("   🚀 Launch: cd frontend && npm run dev")
    print("   🌐 URL: http://localhost:3000")
    print("")
    print("✨ BENEFITS:")
    print("   • Modern React 18 + TypeScript + Tailwind CSS")
    print("   • Autonomous debug monitoring")
    print("   • Real-time error detection")
    print("   • Professional research interface")
    print("   • Better performance and user experience")
    print("")
    print("📁 ARCHIVED STREAMLIT:")
    print("   The original Streamlit app is preserved in:")
    print("   archive/streamlit_legacy/")
    print("")
    print("📖 MIGRATION GUIDE:")
    print("   See: STREAMLIT_MIGRATION_NOTICE.md")
    print("   See: archive/streamlit_legacy/STREAMLIT_DEPRECATION_NOTICE.md")
    print("")
    print("❓ NEED HELP?")
    print("   • React setup: frontend/README.md")
    print("   • Backend services: python launch.py")
    print("   • Questions: Contact development team")

def main():
    """Main function - shows deprecation notice"""
    show_migration_info()
    
    # Ask if user wants to continue to archived Streamlit
    print("\n" + "=" * 50)
    response = input("Continue to archived Streamlit app anyway? (y/N): ").lower().strip()
    
    if response in ['y', 'yes']:
        print("\n🔄 Redirecting to archived Streamlit...")
        print("⚠️  Note: This interface is no longer maintained.")
        
        # Check if archived app exists
        archived_app = Path("archive/streamlit_legacy/src/narrative_gravity/app.py")
        if archived_app.exists():
            import subprocess
            try:
                subprocess.run([
                    sys.executable, "-m", "streamlit", "run", 
                    str(archived_app),
                    "--server.headless", "false",
                    "--server.address", "localhost",
                    "--server.port", "8501"
                ])
            except KeyboardInterrupt:
                print("\n🛑 Archived Streamlit stopped")
            except Exception as e:
                print(f"❌ Error launching archived app: {e}")
                print("💡 Try: cd archive/streamlit_legacy && streamlit run src/narrative_gravity/app.py")
        else:
            print("❌ Archived Streamlit app not found")
            print("💡 Files may have been moved or deleted")
    else:
        print("\n✅ Great choice! The React interface is much better.")
        print("🚀 Run: cd frontend && npm run dev")

if __name__ == "__main__":
    main() 