#!/usr/bin/env python3
"""
Test Prompt Generation to Debug Well Names
"""

from src.prompts.template_manager import PromptTemplateManager

def test_prompt_generation():
    """Test the prompt generation to see what's being produced"""
    
    print("🧪 Testing Prompt Generation")
    print("=" * 50)
    
    try:
        template_manager = PromptTemplateManager()
        print("✅ PromptTemplateManager initialized")
    except Exception as e:
        print(f"❌ Failed to initialize template manager: {e}")
        return
    
    # Test text
    test_text = "We must work together with dignity and respect for all Americans to build a stronger democracy."
    
    try:
        prompt = template_manager.generate_api_prompt(test_text, "civic_virtue", "gpt-4o")
        
        print(f"\n📄 Generated Prompt:")
        print("=" * 80)
        print(prompt)
        print("=" * 80)
        
        # Also check if we can load the framework config correctly
        framework_config = template_manager._load_framework_config("civic_virtue")
        
        print(f"\n📊 Framework Info:")
        print(f"Framework name: {framework_config.get('name')}")
        
        if "dipoles" in framework_config and "dipoles" in framework_config["dipoles"]:
            dipoles = framework_config["dipoles"]["dipoles"]
            print(f"Number of dipoles: {len(dipoles)}")
            
            print(f"\n🎯 Expected Wells:")
            for dipole in dipoles:
                pos_name = dipole["positive"]["name"]
                neg_name = dipole["negative"]["name"]
                print(f"  {dipole['name']}: {pos_name} vs {neg_name}")
        
    except Exception as e:
        print(f"❌ Prompt generation failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_prompt_generation() 