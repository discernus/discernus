#!/usr/bin/env python3
"""
Test Real Available Models (June 2025)
Check what models actually exist vs what our client thinks exists
"""

import os
from dotenv import load_dotenv
load_dotenv()

def test_openai_real_models():
    """Test what OpenAI models actually exist"""
    print("🧪 Testing Real OpenAI Models")
    print("-" * 30)
    
    try:
        import openai
        client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        # Test models that definitely exist
        real_models = [
            "gpt-4o-mini",
            "gpt-4o", 
            "gpt-4-turbo",
            "gpt-3.5-turbo"
        ]
        
        # Test fictional models our client tries to use
        fictional_models = [
            "gpt-4.1",
            "gpt-4.1-mini",
            "o4-mini"
        ]
        
        print("✅ REAL MODELS:")
        for model in real_models:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "Hi"}],
                    max_tokens=5
                )
                print(f"   ✅ {model} works")
            except Exception as e:
                print(f"   ❌ {model} failed: {str(e)[:50]}...")
        
        print("\n❌ FICTIONAL MODELS (what our client tries):")
        for model in fictional_models:
            try:
                response = client.chat.completions.create(
                    model=model,
                    messages=[{"role": "user", "content": "Hi"}],
                    max_tokens=5
                )
                print(f"   ✅ {model} works (surprising!)")
            except Exception as e:
                error_msg = str(e)
                if "does not exist" in error_msg or "404" in error_msg:
                    print(f"   ❌ {model} DOESN'T EXIST (as expected)")
                else:
                    print(f"   ❌ {model} failed: {error_msg[:50]}...")
                    
    except Exception as e:
        print(f"❌ OpenAI test failed: {e}")

def test_google_real_models():
    """Test what Google models actually exist"""
    print("\n🧪 Testing Real Google Models")
    print("-" * 30)
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=os.getenv("GOOGLE_AI_API_KEY"))
        
        # Test models that definitely exist
        real_models = [
            "gemini-1.5-flash",
            "gemini-1.5-pro",
            "gemini-1.0-pro"
        ]
        
        # Test newer models that might exist
        maybe_models = [
            "gemini-2.0-flash-exp",
            "gemini-1.5-flash-002"
        ]
        
        # Test fictional models our client tries to use
        fictional_models = [
            "gemini-2-5-pro-preview",
            "gemini-2-5-flash-preview",
            "gemini-2.5-pro"
        ]
        
        print("✅ REAL MODELS:")
        for model in real_models:
            try:
                ai_model = genai.GenerativeModel(model)
                response = ai_model.generate_content("Hi")
                print(f"   ✅ {model} works")
            except Exception as e:
                print(f"   ❌ {model} failed: {str(e)[:50]}...")
        
        print("\n🤔 MAYBE MODELS:")
        for model in maybe_models:
            try:
                ai_model = genai.GenerativeModel(model)
                response = ai_model.generate_content("Hi")
                print(f"   ✅ {model} works!")
            except Exception as e:
                error_msg = str(e)
                if "not found" in error_msg.lower() or "404" in error_msg:
                    print(f"   ❌ {model} doesn't exist")
                else:
                    print(f"   ❌ {model} failed: {error_msg[:50]}...")
        
        print("\n❌ FICTIONAL MODELS (what our client tries):")
        for model in fictional_models:
            try:
                ai_model = genai.GenerativeModel(model)
                response = ai_model.generate_content("Hi")
                print(f"   ✅ {model} works (surprising!)")
            except Exception as e:
                error_msg = str(e)
                if "not found" in error_msg.lower() or "404" in error_msg:
                    print(f"   ❌ {model} DOESN'T EXIST (as expected)")
                else:
                    print(f"   ❌ {model} failed: {error_msg[:50]}...")
                    
    except Exception as e:
        print(f"❌ Google test failed: {e}")

def test_anthropic_real_models():
    """Test what Anthropic models actually exist"""
    print("\n🧪 Testing Real Anthropic Models")
    print("-" * 30)
    
    try:
        import anthropic
        client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        
        # Test models that definitely exist
        real_models = [
            "claude-3-5-sonnet-20241022",
            "claude-3-5-haiku-20241022", 
            "claude-3-haiku-20240307",
            "claude-3-sonnet-20240229"
        ]
        
        # Test fictional models our client tries to use
        fictional_models = [
            "claude-4-sonnet",
            "claude-4.0-sonnet",
            "claude-4-opus"
        ]
        
        print("✅ REAL MODELS:")
        for model in real_models:
            try:
                response = client.messages.create(
                    model=model,
                    max_tokens=5,
                    messages=[{"role": "user", "content": "Hi"}]
                )
                print(f"   ✅ {model} works")
            except Exception as e:
                print(f"   ❌ {model} failed: {str(e)[:50]}...")
        
        print("\n❌ FICTIONAL MODELS (what our client tries):")
        for model in fictional_models:
            try:
                response = client.messages.create(
                    model=model,
                    max_tokens=5,
                    messages=[{"role": "user", "content": "Hi"}]
                )
                print(f"   ✅ {model} works (surprising!)")
            except Exception as e:
                error_msg = str(e)
                if "not_found_error" in error_msg or "404" in error_msg:
                    print(f"   ❌ {model} DOESN'T EXIST (as expected)")
                else:
                    print(f"   ❌ {model} failed: {error_msg[:50]}...")
                    
    except Exception as e:
        print(f"❌ Anthropic test failed: {e}")

if __name__ == "__main__":
    print("🎯 REALITY CHECK: What Models Actually Exist")
    print("=" * 50)
    print("Testing real vs fictional models in our client...")
    
    test_openai_real_models()
    test_google_real_models()
    test_anthropic_real_models()
    
    print("\n" + "=" * 50)
    print("🎯 CONCLUSION:")
    print("Our client is trying to use models that don't exist yet!")
    print("This explains why Cursor works (uses real models) but we don't.") 