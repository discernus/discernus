#!/usr/bin/env python3
"""
Multi-LLM Testing for Narrative Gravity Analysis

Tests the framework with multiple models available through HuggingFace that represent:
- GPT-4/ChatGPT-like capabilities 
- Claude-like capabilities
- Mistral capabilities

Usage: python test_multi_llm.py [--framework civic_virtue] [--quick]
"""

import os
import sys
import json
import asyncio
from pathlib import Path
from typing import Dict, List, Any
import argparse
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Test Models Configuration
# Based on HuggingFace's currently available text generation models
# Using models that represent the capabilities of ChatGPT, Claude, and Mistral
TEST_MODELS = {
    # GPT-style models (ChatGPT-like conversational and creative)
    "gpt_style": [
        "google/gemma-2-2b-it",  # Google's instruction-tuned model
        "microsoft/phi-4",  # Microsoft's latest powerful model
        "microsoft/DialoGPT-medium",  # Conversational model
    ],
    
    # Claude-style models (analytical, reasoning-focused)
    "claude_style": [
        "Qwen/Qwen2.5-7B-Instruct",  # Strong analytical reasoning
        "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",  # Reasoning-focused
        "meta-llama/Llama-3.2-3B-Instruct",  # Instruction following
    ],
    
    # Mistral family models (efficient, balanced)
    "mistral_style": [
        "mistralai/Mistral-7B-Instruct-v0.3",  # Latest Mistral Instruct
        "mistralai/Mistral-7B-v0.3",  # Base Mistral v0.3
        "mistralai/Mistral-Nemo-Instruct-2407",  # Advanced Mistral
    ]
}

# Quick test models (verified as working through HF Inference API)
QUICK_TEST_MODELS = {
    "gpt_style": ["gpt2", "microsoft/DialoGPT-medium"],
    "claude_style": ["microsoft/DialoGPT-medium", "gpt2-medium"], 
    "mistral_style": ["mistralai/Mistral-7B-Instruct-v0.3", "gpt2"]
}

# Test text samples
TEST_TEXTS = {
    "short_political": """
    We must unite as Americans to build a stronger, more just society where every person has the opportunity to succeed through hard work and determination.
    """,
    
    "persuasive_speech": """
    My fellow citizens, the challenges we face today require bold action and unwavering commitment to our founding principles. We cannot allow fear to divide us or cynicism to paralyze us. Instead, we must choose hope over despair, unity over division, and progress over the status quo. The time for half-measures has passed.
    """,
    
    "policy_argument": """
    The proposed legislation represents a balanced approach that protects individual liberty while ensuring collective security. Critics who claim this threatens freedom ignore the careful safeguards built into the framework. Supporters who demand stronger measures must recognize the constitutional limits we operate within.
    """
}

class MultiLLMTester:
    """Test narrative gravity analysis across multiple LLM models."""
    
    def __init__(self, framework: str = "civic_virtue", quick_mode: bool = False):
        self.framework = framework
        self.models = QUICK_TEST_MODELS if quick_mode else TEST_MODELS
        self.results = {}
        
        # Initialize HuggingFace client
        try:
            from src.tasks.huggingface_client import HuggingFaceClient
            self.client = HuggingFaceClient()
            print(f"✅ HuggingFace client initialized")
            print(f"📊 Available frameworks: {self.client.get_available_frameworks()}")
        except Exception as e:
            print(f"❌ Failed to initialize HuggingFace client: {e}")
            sys.exit(1)
    
    def test_single_model(self, model_name: str, model_type: str, text_key: str) -> Dict[str, Any]:
        """Test a single model with a single text."""
        print(f"\n🤖 Testing {model_name} ({model_type}) with {text_key}...")
        
        try:
            text = TEST_TEXTS[text_key].strip()
            result, cost = self.client.analyze_text(text, self.framework, model_name)
            
            print(f"  ✅ Analysis completed - Cost: ${cost:.4f}")
            
            # Extract key metrics
            scores = result.get('scores', {})
            if scores:
                avg_score = sum(scores.values()) / len(scores)
                print(f"  📊 Average score: {avg_score:.3f}")
                print(f"  🎯 Top wells: {sorted(scores.items(), key=lambda x: x[1], reverse=True)[:3]}")
            
            return {
                'success': True,
                'model': model_name,
                'model_type': model_type,
                'text_key': text_key,
                'result': result,
                'cost': cost,
                'scores': scores,
                'timestamp': datetime.utcnow().isoformat()
            }
            
        except Exception as e:
            print(f"  ❌ Test failed: {e}")
            return {
                'success': False,
                'model': model_name,
                'model_type': model_type,
                'text_key': text_key,
                'error': str(e),
                'timestamp': datetime.utcnow().isoformat()
            }
    
    def run_comprehensive_test(self) -> Dict[str, Any]:
        """Run tests across all model types and text samples."""
        print(f"🚀 Starting comprehensive multi-LLM test")
        print(f"📋 Framework: {self.framework}")
        print(f"🎯 Model categories: {list(self.models.keys())}")
        print(f"📝 Text samples: {list(TEST_TEXTS.keys())}")
        
        all_results = []
        
        for model_type, model_list in self.models.items():
            print(f"\n🔧 Testing {model_type} models...")
            
            for model_name in model_list:
                for text_key in TEST_TEXTS.keys():
                    result = self.test_single_model(model_name, model_type, text_key)
                    all_results.append(result)
                    
                    # Add delay to avoid rate limiting
                    import time
                    time.sleep(2)
        
        # Generate summary
        successful_tests = [r for r in all_results if r['success']]
        failed_tests = [r for r in all_results if not r['success']]
        
        summary = {
            'test_completed': datetime.utcnow().isoformat(),
            'framework': self.framework,
            'total_tests': len(all_results),
            'successful_tests': len(successful_tests),
            'failed_tests': len(failed_tests),
            'success_rate': len(successful_tests) / len(all_results) if all_results else 0,
            'total_cost': sum(r.get('cost', 0) for r in successful_tests),
            'results': all_results
        }
        
        return summary
    
    def run_quick_comparison(self) -> Dict[str, Any]:
        """Run a quick comparison with one model per type."""
        print(f"⚡ Running quick comparison test")
        
        # Select one model per type and one text
        test_cases = []
        text_key = "short_political"  # Use consistent text for comparison
        
        for model_type, model_list in self.models.items():
            if model_list:
                model_name = model_list[0]  # Use first model in each category
                test_cases.append((model_name, model_type, text_key))
        
        results = []
        for model_name, model_type, text_key in test_cases:
            result = self.test_single_model(model_name, model_type, text_key)
            results.append(result)
            
            # Add delay
            import time
            time.sleep(3)
        
        # Compare results
        successful_results = [r for r in results if r['success']]
        
        comparison = {
            'test_completed': datetime.utcnow().isoformat(),
            'framework': self.framework,
            'text_analyzed': TEST_TEXTS[text_key].strip(),
            'model_comparisons': []
        }
        
        for result in successful_results:
            comparison['model_comparisons'].append({
                'model': result['model'],
                'model_type': result['model_type'],
                'scores': result['scores'],
                'cost': result['cost']
            })
        
        return comparison
    
    def save_results(self, results: Dict[str, Any], filename: str = None):
        """Save test results to JSON file."""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"multi_llm_test_{self.framework}_{timestamp}.json"
        
        output_dir = Path("model_output") / "multi_llm_tests"
        output_dir.mkdir(parents=True, exist_ok=True)
        
        filepath = output_dir / filename
        
        with open(filepath, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"💾 Results saved to: {filepath}")
        return filepath

def main():
    """Main test runner."""
    parser = argparse.ArgumentParser(description="Test narrative gravity analysis with multiple LLMs")
    parser.add_argument("--framework", default="civic_virtue", 
                       help="Framework to test (civic_virtue, political_spectrum, moral_rhetorical_posture)")
    parser.add_argument("--quick", action="store_true", 
                       help="Run quick comparison test instead of comprehensive test")
    parser.add_argument("--model-type", choices=["gpt_style", "claude_style", "mistral_style"],
                       help="Test only specific model type")
    
    args = parser.parse_args()
    
    # Verify API key is configured
    if not os.getenv('HUGGINGFACE_API_KEY'):
        print("❌ HUGGINGFACE_API_KEY not found in environment")
        print("💡 Make sure you have a .env file with your HuggingFace API key")
        return 1
    
    # Initialize tester
    try:
        tester = MultiLLMTester(framework=args.framework, quick_mode=args.quick)
    except Exception as e:
        print(f"❌ Failed to initialize tester: {e}")
        return 1
    
    # Run tests
    try:
        if args.quick:
            print("⚡ Running quick comparison test...")
            results = tester.run_quick_comparison()
        else:
            print("🚀 Running comprehensive test...")
            results = tester.run_comprehensive_test()
        
        # Save and display results
        filepath = tester.save_results(results)
        
        print("\n" + "="*60)
        print("📊 TEST SUMMARY")
        print("="*60)
        
        if 'total_tests' in results:
            print(f"Total tests: {results['total_tests']}")
            print(f"Successful: {results['successful_tests']}")
            print(f"Failed: {results['failed_tests']}")
            print(f"Success rate: {results['success_rate']:.1%}")
            print(f"Total cost: ${results['total_cost']:.4f}")
        else:
            print(f"Framework: {results['framework']}")
            print(f"Models tested: {len(results['model_comparisons'])}")
            for comp in results['model_comparisons']:
                print(f"  {comp['model_type']}: {comp['model']} (${comp['cost']:.4f})")
        
        print(f"📄 Detailed results: {filepath}")
        
        return 0
        
    except KeyboardInterrupt:
        print("\n⚠️  Test interrupted by user")
        return 1
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 