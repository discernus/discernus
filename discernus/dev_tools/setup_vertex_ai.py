#!/usr/bin/env python3
"""
Vertex AI Setup Script for Discernus
===================================

Quick setup script to configure Vertex AI integration for access to 
faster and significantly cheaper Gemini models.

Cost Comparison (per 1M tokens):
- Gemini 1.5 Flash: $0.13 input / $0.38 output  
- Gemini 1.5 Pro: $1.25 input / $10 output
- GPT-4 Turbo: ~$10 input / ~$30 output  
- GPT-4o: ~$5 input / ~$15 output

= 10-40x cheaper than OpenAI models! =
"""

import os
import json
from pathlib import Path

def setup_vertex_ai():
    """Guide user through Vertex AI setup"""
    
    print("🚀 VERTEX AI SETUP FOR DISCERNUS")
    print("=" * 50)
    print("Access to Google's Gemini models - up to 40x cheaper than OpenAI!")
    print("Gemini 1.5 Flash: $0.13/$0.38 per 1M tokens (vs GPT-4: $10/$30)")
    print()
    
    # Check if already configured
    if os.getenv('VERTEXAI_PROJECT'):
        print("✅ Vertex AI already configured!")
        print(f"   Project: {os.getenv('VERTEXAI_PROJECT')}")
        print(f"   Location: {os.getenv('VERTEXAI_LOCATION', 'us-central1')}")
        print()
        test_connection()
        return
    
    print("📋 SETUP STEPS:")
    print("1. Create/select a Google Cloud Project")
    print("2. Enable Vertex AI API")
    print("3. Create service account credentials")
    print("4. Configure environment variables")
    print()
    
    # Step 1: Project ID
    project_id = input("📁 Enter your Google Cloud Project ID: ").strip()
    if not project_id:
        print("❌ Project ID required. Exiting.")
        return
    
    # Step 2: Location
    location = input("🌎 Enter location (default: us-central1): ").strip() or "us-central1"
    
    # Step 3: Credentials
    print()
    print("🔑 CREDENTIALS SETUP:")
    print("Option 1: Service Account JSON file path")
    print("Option 2: Set up Application Default Credentials (gcloud auth)")
    print()
    
    creds_option = input("Choose credentials method (1 or 2): ").strip()
    
    credentials_path = None
    if creds_option == "1":
        credentials_path = input("📄 Enter path to service account JSON file: ").strip()
        if credentials_path and not Path(credentials_path).exists():
            print(f"⚠️ File not found: {credentials_path}")
            print("You can continue and set this up later.")
    
    # Step 4: Create .env file
    env_path = Path(".env")
    env_content = []
    
    if env_path.exists():
        with open(env_path, 'r') as f:
            env_content = f.readlines()
    
    # Remove existing Vertex AI entries
    env_content = [line for line in env_content if not line.startswith(('VERTEXAI_', 'VERTEX_', 'GOOGLE_APPLICATION_CREDENTIALS'))]
    
    # Add new entries
    env_content.append(f"\n# Vertex AI Configuration\n")
    env_content.append(f"VERTEXAI_PROJECT={project_id}\n")
    env_content.append(f"VERTEXAI_LOCATION={location}\n")
    
    if credentials_path:
        env_content.append(f"GOOGLE_APPLICATION_CREDENTIALS={credentials_path}\n")
    
    # Write .env file
    with open(env_path, 'w') as f:
        f.writelines(env_content)
    
    print()
    print("✅ Configuration saved to .env file!")
    print()
    
    # Test the setup
    print("🧪 Testing configuration...")
    test_connection()
    
    print()
    print("🎉 SETUP COMPLETE!")
    print()
    print("💰 COST SAVINGS:")
    print("- Gemini 1.5 Flash: $0.13/$0.38 per 1M tokens")
    print("- Gemini 1.5 Pro: $1.25/$10 per 1M tokens") 
    print("- 10-40x cheaper than OpenAI equivalents!")
    print()
    print("⚡ SPEED:")
    print("- Gemini models are generally faster")
    print("- Huge 1M token context window")
    print("- Native multimodal support")
    print()
    print("🚀 Usage:")
    print("Models are now available in your Discernus research sessions:")
    print("- vertex_ai/gemini-1.5-flash (fastest, cheapest)")
    print("- vertex_ai/gemini-1.5-pro (most capable)")
    print("- vertex_ai/gemini-2.5-flash (latest fast model)")
    print("- vertex_ai/gemini-2.5-pro (thinking-native model)")


def test_connection():
    """Test Vertex AI connection"""
    try:
        # Load environment
        from dotenv import load_dotenv
        load_dotenv()
        
        # Import our client
        from discernus.core.ultra_thin_llm_client import UltraThinLLMClient as ThinLiteLLMClient
        
        # Check configuration
        vertex_config = {
            'project': os.environ.get('VERTEXAI_PROJECT', 'gen-lang-client-0199646265'),
            'location': os.environ.get('VERTEXAI_LOCATION', 'us-central1')
        }
        if not vertex_config:
            print("❌ No Vertex AI configuration found")
            return False
        
        print(f"✅ Project: {vertex_config['project']}")
        print(f"✅ Location: {vertex_config['location']}")
        
        # Test client
        client = ThinLiteLLMClient()
        available_models = client.get_available_models()
        
        vertex_models = [m for m in available_models if m.startswith('vertex_ai/')]
        if vertex_models:
            print(f"✅ {len(vertex_models)} Vertex AI models available:")
            for model in vertex_models[:3]:  # Show first 3
                print(f"   - {model}")
            if len(vertex_models) > 3:
                print(f"   - ... and {len(vertex_models) - 3} more")
            return True
        else:
            print("❌ No Vertex AI models available")
            return False
            
    except Exception as e:
        print(f"❌ Connection test failed: {e}")
        print("💡 This is normal if you haven't set up credentials yet")
        return False


def print_setup_instructions():
    """Print detailed setup instructions"""
    print()
    print("📚 DETAILED SETUP INSTRUCTIONS:")
    print("=" * 40)
    print()
    print("1. CREATE GOOGLE CLOUD PROJECT:")
    print("   - Go to: https://console.cloud.google.com/")
    print("   - Create new project or select existing one")
    print("   - Note the Project ID")
    print()
    print("2. ENABLE VERTEX AI API:")
    print("   - In Google Cloud Console, go to APIs & Services")
    print("   - Search for 'Vertex AI API'")
    print("   - Click Enable")
    print()
    print("3. CREATE SERVICE ACCOUNT:")
    print("   - Go to IAM & Admin > Service Accounts")
    print("   - Create service account")
    print("   - Add role: 'Vertex AI User'")
    print("   - Generate JSON key and download")
    print()
    print("4. ALTERNATIVE - APPLICATION DEFAULT CREDENTIALS:")
    print("   - Install Google Cloud CLI")
    print("   - Run: gcloud auth application-default login")
    print("   - This sets up credentials automatically")
    print()


if __name__ == "__main__":
    try:
        setup_vertex_ai()
    except KeyboardInterrupt:
        print("\n\n🛑 Setup cancelled by user")
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        print("\n📚 For detailed instructions, run:")
        print("python3 discernus/setup_vertex_ai.py --help")
        print_setup_instructions() 