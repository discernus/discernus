#!/usr/bin/env python3
"""
Test script for YouTube ingestion improvements

Tests the enhanced cross-validation and speaker identification features
"""

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

def test_speaker_conflict_detection():
    """Test the speaker conflict detection system"""
    
    from narrative_gravity.corpus.youtube_ingestion import YouTubeCorpusIngestionService
    
    # Create service without registry for testing
    service = YouTubeCorpusIngestionService(corpus_registry=None)
    
    # Test cases that should detect conflicts
    test_cases = [
        {
            "llm_speaker": "Greg Abbott",
            "youtube_title": "Gov Perry ALEC 2016",
            "should_conflict": True,
            "description": "Perry/Abbott misidentification"
        },
        {
            "llm_speaker": "Barack Obama", 
            "youtube_title": "President Obama 2012 DNC Speech",
            "should_conflict": False,
            "description": "Correct identification"
        },
        {
            "llm_speaker": "John McCain",
            "youtube_title": "Senator McCain Concession Speech 2008", 
            "should_conflict": False,
            "description": "Title/last name match"
        },
        {
            "llm_speaker": "Hillary Clinton",
            "youtube_title": "Gov Romney Victory Speech",
            "should_conflict": True,
            "description": "Completely different speakers"
        }
    ]
    
    print("🧪 Testing Speaker Conflict Detection")
    print("=" * 50)
    
    for i, test_case in enumerate(test_cases, 1):
        conflict_detected = service._check_speaker_conflict(
            test_case["llm_speaker"], 
            test_case["youtube_title"]
        )
        
        expected = test_case["should_conflict"]
        passed = conflict_detected == expected
        
        status = "✅ PASS" if passed else "❌ FAIL"
        
        print(f"Test {i}: {test_case['description']} - {status}")
        print(f"  LLM: {test_case['llm_speaker']}")
        print(f"  Title: {test_case['youtube_title']}")
        print(f"  Expected conflict: {expected}, Detected: {conflict_detected}")
        print()
    
    return True

def test_enhanced_speaker_extraction():
    """Test enhanced speaker extraction from content"""
    
    from narrative_gravity.corpus.youtube_ingestion import YouTubeCorpusIngestionService
    
    service = YouTubeCorpusIngestionService(corpus_registry=None)
    
    test_texts = [
        {
            "content": "Thank you. My name is Rick Perry and I'm here to talk about...",
            "channel": "ALEC Videos",
            "expected": "Rick Perry",
            "description": "Direct name introduction"
        },
        {
            "content": "Good morning, I'm Governor Abbott speaking to you from Texas...",
            "channel": "Texas GOP",
            "expected": "Governor Abbott", 
            "description": "Title + name pattern"
        },
        {
            "content": "Thank you for that introduction. This is Senator Warren...",
            "channel": "Progressive Channel",
            "expected": "Senator Warren",
            "description": "This is + title pattern"
        }
    ]
    
    print("🧪 Testing Enhanced Speaker Extraction")
    print("=" * 50)
    
    for i, test_case in enumerate(test_texts, 1):
        extracted = service._extract_speaker_from_youtube(
            test_case["channel"],
            test_case["content"]
        )
        
        expected = test_case["expected"]
        passed = expected.lower() in extracted.lower()
        
        status = "✅ PASS" if passed else "❌ FAIL"
        
        print(f"Test {i}: {test_case['description']} - {status}")
        print(f"  Content start: {test_case['content'][:50]}...")
        print(f"  Expected: {expected}")
        print(f"  Extracted: {extracted}")
        print()
    
    return True

def main():
    """Run all tests"""
    print("🎬 YouTube Ingestion Improvements - Test Suite")
    print("=" * 60)
    print()
    
    try:
        test_speaker_conflict_detection()
        test_enhanced_speaker_extraction()
        
        print("✅ All tests completed!")
        print("\n💡 These improvements should help prevent speaker misidentification")
        print("   like the Rick Perry/Greg Abbott case.")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    main() 