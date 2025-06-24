#!/usr/bin/env python3
"""
Test Google Changelog Models (June 2025)
Test the exact model names from Google AI Studio changelog
"""

import os
from dotenv import load_dotenv
load_dotenv()

def test_google_changelog_models():
    """Test exact model names from Google's changelog"""
    print("🧪 Testing Google Changelog Models")
    print("=" * 50)
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))
        
        # Models from June 17, 2025 changelog
        june_17_models = [
            "gemini-2.5-pro",  # Stable version
            "gemini-2.5-flash",  # First stable 2.5 Flash
            "gemini-2.5-flash-lite-preview-06-17"  # Low-cost model
        ]
        
        # Models from June 05, 2025 changelog  
        june_05_models = [
            "gemini-2.5-pro-preview-06-05"  # With adaptive thinking
        ]
        
        # Models from May 20, 2025 changelog
        may_20_models = [
            "gemini-2.5-flash-preview-05-20",  # Price-performance optimized
            "gemini-2.5-pro-preview-tts",      # With speech generation
            "gemini-2.5-flash-preview-tts"     # Flash with speech
        ]
        
        # Test all model groups
        model_groups = [
            ("June 17, 2025 (Latest Stable)", june_17_models),
            ("June 05, 2025 (Preview)", june_05_models), 
            ("May 20, 2025 (Features)", may_20_models)
        ]
        
        working_models = []
        
        for group_name, models in model_groups:
            print(f"\n📅 {group_name}:")
            for model in models:
                try:
                    ai_model = genai.GenerativeModel(model)
                    response = ai_model.generate_content("Hello")
                    print(f"   ✅ {model} WORKS!")
                    working_models.append(model)
                except Exception as e:
                    error_msg = str(e)
                    if "not found" in error_msg.lower() or "404" in error_msg:
                        print(f"   ❌ {model} not found")
                    elif "quota" in error_msg.lower() or "429" in error_msg:
                        print(f"   💳 {model} quota exceeded (but exists)")
                        working_models.append(model)  # Count as working
                    elif "permission" in error_msg.lower() or "403" in error_msg:
                        print(f"   🔒 {model} permission denied (but exists)")
                        working_models.append(model)  # Count as working
                    else:
                        print(f"   ❌ {model} error: {error_msg[:60]}...")
        
        # Summary
        print(f"\n🎯 SUMMARY:")
        print(f"Working models found: {len(working_models)}")
        if working_models:
            print("✅ Available Gemini 2.5 models:")
            for model in working_models:
                print(f"   - {model}")
            
            # Recommend best model for experiments
            if "gemini-2.5-pro" in working_models:
                recommended = "gemini-2.5-pro"
            elif "gemini-2.5-flash" in working_models:
                recommended = "gemini-2.5-flash"
            else:
                recommended = working_models[0]
            
            print(f"\n🚀 RECOMMENDED: {recommended}")
            print("   (Use this in your experiments)")
        else:
            print("❌ No working Gemini 2.5 models found")
            
    except Exception as e:
        print(f"❌ Google API test failed: {e}")

if __name__ == "__main__":
    test_google_changelog_models() 