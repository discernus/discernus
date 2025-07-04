#!/usr/bin/env python3
"""
Minimal Corpus Test - Isolate Directory Reading
==============================================

Test the corpus reading functionality without heavy imports.
This isolates the issue to see if it's the directory reading or the orchestrator setup.
"""

import os
from pathlib import Path

def read_directory_corpus(directory_path):
    """Read all files from directory - pure infrastructure, no interpretation"""
    print(f"\n📖 Reading corpus from: {directory_path}")
    
    files = {}
    errors = []
    
    try:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            
            # Skip directories
            if os.path.isdir(file_path):
                continue
                
            # Attempt to read as text
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    files[filename] = content
                    print(f"✅ Read {filename} ({len(content)} chars)")
            except UnicodeDecodeError:
                try:
                    # Try different encoding
                    with open(file_path, 'r', encoding='latin-1') as f:
                        content = f.read()
                        files[filename] = content
                        print(f"✅ Read {filename} ({len(content)} chars) [latin-1 encoding]")
                except Exception as e:
                    errors.append(f"{filename}: {str(e)}")
                    files[filename] = f"[Could not read as text: {str(e)}]"
                    print(f"⚠️ Could not read {filename}: {str(e)}")
            except Exception as e:
                errors.append(f"{filename}: {str(e)}")
                files[filename] = f"[Could not read: {str(e)}]"
                print(f"⚠️ Could not read {filename}: {str(e)}")
    
    except Exception as e:
        print(f"❌ Error reading directory: {e}")
        return {}
    
    if not files:
        print("❌ No readable files found in directory")
        return {}
    
    print(f"\n📊 CORPUS SUMMARY: {len(files)} files read, {len(errors)} errors")
    return files

def mock_llm_analysis(files: dict) -> str:
    """Mock LLM analysis without actual LLM calls"""
    print("\n🔍 MOCK LLM CORPUS DETECTIVE")
    print("-" * 40)
    
    # Simple analysis based on filenames and content previews
    analysis_parts = []
    analysis_parts.append("CORPUS ANALYSIS:")
    
    for filename, content in files.items():
        preview = content[:100] + "..." if len(content) > 100 else content
        analysis_parts.append(f"- {filename}: {preview}")
    
    analysis_parts.append("\nDUPLICATES/VERSIONS:")
    analysis_parts.append("I need to examine content more carefully to identify duplicates.")
    
    analysis_parts.append("\nMETADATA INFERENCE:")
    analysis_parts.append("Based on filenames, I can see these appear to be political speeches.")
    
    analysis_parts.append("\nUSABLE FILES:")
    analysis_parts.append("All files appear readable and suitable for analysis.")
    
    analysis_parts.append("\nCLARIFYING QUESTIONS:")
    analysis_parts.append("What specific research question would you like to explore with this corpus?")
    
    return "\n".join(analysis_parts)

def test_bolsonaro_corpus():
    """Test with the Bolsonaro corpus"""
    print("🧪 Testing Bolsonaro 2018 Corpus")
    print("=" * 40)
    
    # Test directory reading
    corpus_path = "/Volumes/dev/discernus/data/bolsonaro_2018"
    
    if not os.path.exists(corpus_path):
        print(f"❌ Corpus path not found: {corpus_path}")
        return
    
    # Read corpus
    files = read_directory_corpus(corpus_path)
    
    if not files:
        print("❌ No files loaded")
        return
    
    # Mock LLM analysis
    analysis = mock_llm_analysis(files)
    
    print("\n🔍 MOCK LLM ANALYSIS:")
    print("=" * 60)
    print(analysis)
    print("=" * 60)
    
    # Test user input (the problematic part)
    print("\n🤔 TESTING USER INPUT")
    print("-" * 40)
    print("What's your intuition about these texts?")
    
    observation = input("\nYour observation: ").strip()
    
    print(f"\n✅ Recorded: {observation}")
    print("\n🎉 Test completed successfully!")

if __name__ == "__main__":
    print("🌟 Minimal Corpus Test")
    print("This tests corpus reading without heavy imports")
    print()
    
    try:
        test_bolsonaro_corpus()
    except KeyboardInterrupt:
        print("\n\n🛑 Test interrupted by user")
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc() 