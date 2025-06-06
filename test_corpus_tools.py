#!/usr/bin/env python3
"""
Quick test script for corpus generation tools
"""

import subprocess
import sys
from pathlib import Path

def test_schema_generator():
    """Test the schema generator tool"""
    print("🧪 Testing Schema Generator...")
    
    cmd = [
        sys.executable, "src/cli/schema_generator.py",
        "--input", "test_data/sample_corpus.jsonl",
        "--output", "test_generated_schema.json",
        "--title", "Test Generated Schema"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ Schema generator works!")
        print(f"Output: {result.stdout}")
        
        # Check if file was created
        if Path("test_generated_schema.json").exists():
            print("✅ Schema file created successfully")
        else:
            print("❌ Schema file not found")
    
    except subprocess.CalledProcessError as e:
        print(f"❌ Schema generator failed: {e}")
        print(f"Error output: {e.stderr}")

def test_jsonl_generator():
    """Test the JSONL generator tool"""
    print("\n🧪 Testing JSONL Generator...")
    
    # Create a simple test file
    test_content = """This is a test document for the JSONL generator.

It has multiple paragraphs to test the chunking functionality.

The tool should be able to process this text and generate proper JSONL output."""
    
    with open("test_input.txt", "w") as f:
        f.write(test_content)
    
    cmd = [
        sys.executable, "src/cli/jsonl_generator.py",
        "--input", "test_input.txt",
        "--output", "test_output.jsonl",
        "--format", "text",
        "--chunk-type", "fixed",
        "--chunk-size", "100",
        "--metadata", '{"author": "Test Author", "document_type": "other", "title": "Test Document"}',
        "--schema", "schemas/core_schema_v1.0.0.json"
    ]
    
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print("✅ JSONL generator works!")
        print(f"Output: {result.stdout}")
        
        # Check if file was created
        if Path("test_output.jsonl").exists():
            print("✅ JSONL file created successfully")
            # Count records
            with open("test_output.jsonl", "r") as f:
                record_count = sum(1 for line in f if line.strip())
            print(f"📊 Generated {record_count} records")
        else:
            print("❌ JSONL file not found")
    
    except subprocess.CalledProcessError as e:
        print(f"❌ JSONL generator failed: {e}")
        print(f"Error output: {e.stderr}")

def cleanup():
    """Clean up test files"""
    test_files = [
        "test_generated_schema.json",
        "test_input.txt", 
        "test_output.jsonl"
    ]
    
    for file_path in test_files:
        if Path(file_path).exists():
            Path(file_path).unlink()
            print(f"🧹 Cleaned up {file_path}")

def main():
    """Run all tests"""
    print("🚀 Testing Corpus Generation Tools")
    print("="*50)
    
    try:
        test_schema_generator()
        test_jsonl_generator()
        
        print("\n🎉 All tests completed!")
    
    finally:
        print("\n🧹 Cleaning up...")
        cleanup()

if __name__ == "__main__":
    main() 