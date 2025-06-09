#!/usr/bin/env python3
"""
Test script for Narrative Gravity Analysis API.
Verifies that the FastAPI application starts and responds correctly.
"""

import sys
import os
from pathlib import Path

# Add src to Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

def test_api_startup():
    """Test that the API can start without errors."""
    from src.narrative_gravity.api.main import app
    print("✅ FastAPI app created successfully")
    
    # Test that we can access the app
    assert app.title == "Narrative Gravity Analysis API"
    print("✅ App configuration correct")

def test_database_models():
    """Test that database models can be imported."""
    from src.narrative_gravity.models.models import Corpus, Document, Chunk, Job, Task
    print("✅ Database models imported successfully")
    
    # Test model creation (without database)
    corpus = Corpus(name="test", record_count=0)
    assert corpus.name == "test"
    print("✅ Model instantiation works")

def test_schemas():
    """Test that Pydantic schemas work correctly."""
    from src.narrative_gravity.api.schemas import CorpusResponse, JobCreate, DocumentType
    print("✅ API schemas imported successfully")
    
    # Test enum
    doc_type = DocumentType.speech
    assert doc_type == "speech"
    print("✅ Schema enums work correctly")

def main():
    """Run all tests."""
    print("🚀 Testing Narrative Gravity Analysis API")
    print("=" * 50)
    
    tests = [
        ("Database Models", test_database_models),
        ("API Schemas", test_schemas),
        ("API Startup", test_api_startup),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Testing {test_name}...")
        if test_func():
            passed += 1
        else:
            print(f"❌ {test_name} failed")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! API is ready for development.")
        return True
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 