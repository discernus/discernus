#!/usr/bin/env python3
"""
Model Availability Test Script

Tests that the restored Claude 3.5 Sonnet models are actually operational
using the API keys configured in the environment.

Usage:
    python3 scripts/test_model_availability.py
    python3 scripts/test_model_availability.py --model vertex_ai/claude-3-5-sonnet@20240620
    python3 scripts/test_model_availability.py --quick  # Test only priority models
"""

import os
import sys
import argparse
import yaml
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    import litellm
except ImportError:
    print("❌ LiteLLM not installed. Run: pip install litellm")
    sys.exit(1)

class ModelAvailabilityTester:
    def __init__(self, config_path: str = "discernus/gateway/models.yaml"):
        self.config_path = Path(config_path)
        self.models = self.load_models()
        self.test_results = []
        self.setup_environment()
        
    def load_models(self) -> Dict[str, Dict]:
        """Load model configuration from YAML file"""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Models config not found: {self.config_path}")
            
        with open(self.config_path, 'r') as f:
            config = yaml.safe_load(f)
            return config.get('models', {})
    
    def setup_environment(self):
        """Configure environment for testing"""
        # Set up Vertex AI defaults if not configured
        if not os.getenv('VERTEXAI_PROJECT'):
            os.environ['VERTEXAI_PROJECT'] = 'gen-lang-client-0199646265'
        if not os.getenv('VERTEXAI_LOCATION'):
            os.environ['VERTEXAI_LOCATION'] = 'us-central1'
            
        # Show environment status
        print("🔧 Environment Configuration:")
        print(f"   ANTHROPIC_API_KEY: {'✅ Set' if os.getenv('ANTHROPIC_API_KEY') else '❌ Not set'}")
        print(f"   OPENAI_API_KEY: {'✅ Set' if os.getenv('OPENAI_API_KEY') else '❌ Not set'}")
        print(f"   VERTEXAI_PROJECT: {os.getenv('VERTEXAI_PROJECT', 'Not set')}")
        print(f"   VERTEXAI_LOCATION: {os.getenv('VERTEXAI_LOCATION', 'Not set')}")
        print()
    
    def test_model(self, model_id: str, model_info: Dict) -> Tuple[bool, str, Dict]:
        """Test a single model with a minimal call"""
        test_message = "Hello! Please respond with just 'OK' to confirm you're working."
        
        try:
            print(f"   Testing {model_id}...", end=" ")
            
            # Use the same parameter management as LLMGateway
            from discernus.gateway.provider_parameter_manager import ProviderParameterManager
            param_manager = ProviderParameterManager()
            
            # Get clean parameters using the same logic as LLMGateway
            base_params = {"max_tokens": 50}
            clean_params = param_manager.get_clean_parameters(model_id, base_params)
            
            # Make test call with cleaned parameters
            response = litellm.completion(
                model=model_id,
                messages=[{"role": "user", "content": test_message}],
                **clean_params
            )
            
            # Extract response text safely
            response_text = ""
            try:
                choices = getattr(response, 'choices', None)
                if choices and len(choices) > 0:
                    choice = choices[0]
                    message = getattr(choice, 'message', None)
                    if message:
                        content = getattr(message, 'content', None)
                        if content:
                            response_text = str(content).strip()
            except Exception:
                response_text = ""
            
            # Check if response is reasonable
            if response_text and len(response_text) > 0:
                print("✅ SUCCESS")
                
                # Extract usage information safely
                usage_info = None
                try:
                    usage = getattr(response, 'usage', None)
                    if usage:
                        if hasattr(usage, 'dict'):
                            usage_info = usage.dict()
                        else:
                            usage_info = str(usage)
                except Exception:
                    usage_info = None
                
                return True, response_text, {
                    "status": "success",
                    "response": response_text,
                    "model": getattr(response, 'model', 'unknown'),
                    "usage": usage_info
                }
            else:
                print("❌ EMPTY RESPONSE")
                return False, "Empty response", {"status": "empty_response"}
                
        except Exception as e:
            error_msg = str(e)
            print(f"❌ ERROR: {error_msg}")
            return False, error_msg, {"status": "error", "error": error_msg}
    
    def test_claude_models(self) -> List[Dict]:
        """Test all Claude 3.5 Sonnet models specifically"""
        claude_models = {}
        
        # Find all Claude models
        for model_id, model_info in self.models.items():
            if any(claude_name in model_id.lower() for claude_name in ['claude-3-5-sonnet', 'claude-3-7-sonnet', 'claude-sonnet-4']):
                claude_models[model_id] = model_info
        
        print(f"🔍 Testing {len(claude_models)} Claude 3.5+ Sonnet models:")
        print()
        
        results = []
        for model_id, model_info in claude_models.items():
            success, response, details = self.test_model(model_id, model_info)
            
            result = {
                "model_id": model_id,
                "provider": model_info.get('provider'),
                "utility_tier": model_info.get('utility_tier'),
                "success": success,
                "response": response,
                "details": details,
                "timestamp": datetime.now().isoformat()
            }
            results.append(result)
            
            if success:
                print(f"      Response: '{response}'")
                if details.get('usage'):
                    usage = details['usage']
                    print(f"      Usage: {usage.get('prompt_tokens', 0)} prompt + {usage.get('completion_tokens', 0)} completion tokens")
            print()
        
        return results
    
    def test_priority_models(self) -> List[Dict]:
        """Test only high-priority models (utility_tier 1-3)"""
        priority_models = {}
        
        for model_id, model_info in self.models.items():
            utility_tier = model_info.get('utility_tier', 10)
            if utility_tier <= 3:
                priority_models[model_id] = model_info
        
        print(f"🔍 Testing {len(priority_models)} priority models (utility_tier 1-3):")
        print()
        
        results = []
        for model_id, model_info in priority_models.items():
            success, response, details = self.test_model(model_id, model_info)
            
            result = {
                "model_id": model_id,
                "provider": model_info.get('provider'),
                "utility_tier": model_info.get('utility_tier'),
                "success": success,
                "response": response,
                "details": details,
                "timestamp": datetime.now().isoformat()
            }
            results.append(result)
            
            if success:
                print(f"      Response: '{response}'")
        
        return results
    
    def test_single_model(self, model_id: str) -> Dict:
        """Test a single specified model"""
        if model_id not in self.models:
            print(f"❌ Model '{model_id}' not found in registry")
            return {"error": "Model not found", "model_id": model_id}
        
        model_info = self.models[model_id]
        print(f"🔍 Testing single model: {model_id}")
        print(f"   Provider: {model_info.get('provider')}")
        print(f"   Utility Tier: {model_info.get('utility_tier')}")
        print()
        
        success, response, details = self.test_model(model_id, model_info)
        
        result = {
            "model_id": model_id,
            "provider": model_info.get('provider'),
            "utility_tier": model_info.get('utility_tier'),
            "success": success,
            "response": response,
            "details": details,
            "timestamp": datetime.now().isoformat()
        }
        
        if success:
            print(f"✅ Model is operational!")
            print(f"   Response: '{response}'")
            if details.get('usage'):
                usage = details['usage']
                print(f"   Usage: {usage.get('prompt_tokens', 0)} prompt + {usage.get('completion_tokens', 0)} completion tokens")
        else:
            print(f"❌ Model test failed: {response}")
        
        return result
    
    def generate_report(self, results: List[Dict]) -> str:
        """Generate a summary report of test results"""
        total_tests = len(results)
        successful_tests = sum(1 for r in results if r.get('success', False))
        failed_tests = total_tests - successful_tests
        
        report = f"""
## Model Availability Test Report

**Summary:**
- Total models tested: {total_tests}
- Successful: {successful_tests} ✅
- Failed: {failed_tests} ❌
- Success rate: {(successful_tests/total_tests*100):.1f}%

**Test Results:**
"""
        
        # Group by provider
        providers = {}
        for result in results:
            provider = result.get('provider', 'unknown')
            if provider not in providers:
                providers[provider] = []
            providers[provider].append(result)
        
        for provider, provider_results in providers.items():
            successful = sum(1 for r in provider_results if r.get('success', False))
            total = len(provider_results)
            
            report += f"\n### {provider.upper()} ({successful}/{total} successful)\n"
            
            for result in provider_results:
                status = "✅" if result.get('success', False) else "❌"
                model_id = result.get('model_id', 'unknown')
                tier = result.get('utility_tier', 'N/A')
                
                report += f"- {status} `{model_id}` (tier {tier})"
                
                if result.get('success', False):
                    response = str(result.get('response', '') or '')[:50]
                    report += f" - Response: '{response}'"
                else:
                    error = str(result.get('response', 'Unknown error') or 'Unknown error')[:100]
                    report += f" - Error: {error}"
                    
                report += "\n"
        
        return report
    
    def save_results(self, results: List[Dict], filename: Optional[str] = None):
        """Save test results to a JSON file"""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"model_test_results_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"📄 Results saved to: {filename}")

def main():
    parser = argparse.ArgumentParser(description='Test model availability with configured API keys')
    parser.add_argument('--model', help='Test a specific model (e.g., vertex_ai/claude-3-5-sonnet@20240620)')
    parser.add_argument('--quick', action='store_true', help='Test only priority models (utility_tier 1-3)')
    parser.add_argument('--claude', action='store_true', help='Test only Claude 3.5+ Sonnet models')
    parser.add_argument('--save', action='store_true', help='Save results to JSON file')
    parser.add_argument('--report', action='store_true', help='Generate markdown report')
    
    args = parser.parse_args()
    
    try:
        tester = ModelAvailabilityTester()
        
        if args.model:
            # Test single model
            result = tester.test_single_model(args.model)
            results = [result] if 'error' not in result else []
            
        elif args.claude:
            # Test Claude models
            results = tester.test_claude_models()
            
        elif args.quick:
            # Test priority models
            results = tester.test_priority_models()
            
        else:
            # Default: test Claude models (most relevant for the current issue)
            results = tester.test_claude_models()
        
        # Generate report
        if args.report and results:
            report = tester.generate_report(results)
            print(report)
        
        # Save results
        if args.save and results:
            tester.save_results(results)
        
        # Summary
        if results:
            successful = sum(1 for r in results if r.get('success', False))
            total = len(results)
            print(f"\n🎯 **Test Summary**: {successful}/{total} models operational ({(successful/total*100):.1f}% success rate)")
            
            if successful < total:
                print("⚠️  Some models failed. Check API keys and network connectivity.")
                sys.exit(1)
            else:
                print("✅ All tested models are operational!")
                sys.exit(0)
        else:
            print("❌ No models tested successfully")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Test failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 