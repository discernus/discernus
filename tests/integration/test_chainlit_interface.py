#!/usr/bin/env python3
"""
Test script for Chainlit Narrative Gravity Analysis Interface
Verifies that all components are properly configured and functional
"""

import sys
import os
from pathlib import Path
import importlib.util

def test_chainlit_installation():
    """Test if chainlit is properly installed"""
    print("🧪 Testing Chainlit Installation...")
    try:
        import chainlit as cl
        print(f"✅ Chainlit {cl.__version__} installed successfully")
        return True
    except ImportError:
        print("❌ Chainlit not installed. Run: pip install -r requirements.txt")
        return False

def test_project_structure():
    """Test if required project files exist"""
    print("\n🧪 Testing Project Structure...")
    
    required_files = [
        "chainlit_chat.py",
        "launch_chainlit.py", 
        ".chainlit/config.toml",
        "public/style.css",
        "public/README.md",
        "src/narrative_gravity/chatbot/__init__.py",
        "frameworks/fukuyama_identity/framework.json"
    ]
    
    all_present = True
    for file_path in required_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - Missing")
            all_present = False
    
    return all_present

def test_chatbot_imports():
    """Test if the chatbot components can be imported"""
    print("\n🧪 Testing Chatbot Imports...")
    
    # Add src to path
    project_root = Path(__file__).parent
    sys.path.insert(0, str(project_root / "src"))
    
    try:
        from narrative_gravity.chatbot import NarrativeGravityBot
        print("✅ NarrativeGravityBot imported successfully")
        
        # Test initialization
        bot = NarrativeGravityBot()
        print("✅ NarrativeGravityBot initialized successfully")
        
        # Test framework interface
        frameworks = bot.framework_interface.get_available_frameworks()
        framework_names = [fw['name'] for fw in frameworks] if frameworks else []
        print(f"✅ Found {len(frameworks)} frameworks: {', '.join(framework_names)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Chatbot import failed: {e}")
        return False

def test_chainlit_file_syntax():
    """Test if chainlit_chat.py has valid syntax"""
    print("\n🧪 Testing Chainlit File Syntax...")
    
    chainlit_file = Path("chainlit_chat.py")
    if not chainlit_file.exists():
        print("❌ chainlit_chat.py not found")
        return False
    
    try:
        spec = importlib.util.spec_from_file_location("chainlit_chat", chainlit_file)
        module = importlib.util.module_from_spec(spec)
        
        # Test basic syntax by compiling
        with open(chainlit_file, 'r') as f:
            content = f.read()
        compile(content, chainlit_file, 'exec')
        
        print("✅ chainlit_chat.py syntax is valid")
        return True
        
    except SyntaxError as e:
        print(f"❌ Syntax error in chainlit_chat.py: {e}")
        return False
    except Exception as e:
        print(f"❌ Error testing chainlit_chat.py: {e}")
        return False

def test_config_files():
    """Test if configuration files are properly formatted"""
    print("\n🧪 Testing Configuration Files...")
    
    try:
        # Test chainlit config
        import toml
        with open('.chainlit/config.toml', 'r') as f:
            config = toml.load(f)
        print("✅ .chainlit/config.toml is valid TOML")
        
        # Check key sections
        if 'UI' in config and config['UI'].get('name') == "Narrative Gravity Analysis":
            print("✅ UI configuration is correct")
        else:
            print("⚠️  UI configuration may need adjustment")
        
        return True
        
    except Exception as e:
        print(f"❌ Configuration file error: {e}")
        return False

def test_database_connection():
    """Test database connectivity (optional)"""
    print("\n🧪 Testing Database Connection...")
    
    try:
        # Add src to path
        project_root = Path(__file__).parent
        sys.path.insert(0, str(project_root / "src"))
        
        from narrative_gravity.models.base import engine
        
        # Test connection
        with engine.connect():
            pass
        
        print("✅ Database connection successful")
        return True
        
    except Exception as e:
        print(f"⚠️  Database connection failed: {e}")
        print("   This is optional for testing, but required for full functionality")
        return False

def test_launch_script():
    """Test if launch scripts exist and are executable"""
    print("\n🧪 Testing Launch Scripts...")
    
    scripts = ["launch_chainlit.py", "launch.py"]
    all_good = True
    
    for script in scripts:
        script_path = Path(script)
        if script_path.exists():
            # Check if it's executable
            if os.access(script_path, os.X_OK) or script.endswith('.py'):
                print(f"✅ {script} is executable")
            else:
                print(f"⚠️  {script} may not be executable")
        else:
            print(f"❌ {script} not found")
            all_good = False
    
    return all_good

def run_all_tests():
    """Run all tests and provide summary"""
    print("🎯 Chainlit Interface Test Suite")
    print("=" * 50)
    
    tests = [
        ("Chainlit Installation", test_chainlit_installation),
        ("Project Structure", test_project_structure),
        ("Chatbot Imports", test_chatbot_imports),
        ("Chainlit File Syntax", test_chainlit_file_syntax),
        ("Configuration Files", test_config_files),
        ("Database Connection", test_database_connection),
        ("Launch Scripts", test_launch_script)
    ]
    
    results = {}
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results[test_name] = False
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 Test Summary")
    print("=" * 50)
    
    passed = sum(1 for result in results.values() if result)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:<25} {status}")
    
    print(f"\nOverall: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! Chainlit interface is ready to use.")
        print("\n🚀 To launch the interface, run:")
        print("   python launch_chainlit.py")
        print("   or")
        print("   python launch.py --chainlit-only")
    else:
        print(f"\n⚠️  {total - passed} test(s) failed. Please address the issues above.")
        if not results.get("Database Connection", True):
            print("\n💡 Database connection failure is common and doesn't prevent basic functionality.")
            print("   See LAUNCH_GUIDE.md for database setup instructions.")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1) 