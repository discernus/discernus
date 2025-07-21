#!/usr/bin/env python3
"""
Prompt Engineering Harness
==========================

A flexible, configurable script for testing specific models with specific prompts
without fallback mechanisms. Perfect for rapid iteration and prompt tuning.

Usage Examples:
    # Test simple prompt with specific model
    python3 scripts/prompt_engineering_harness.py --model "anthropic/claude-3-5-sonnet-20240620" --prompt "What is 2+2?"
    
    # Test with prompt from file  
    python3 scripts/prompt_engineering_harness.py --model "perplexity/r1-1776" --prompt-file "test_prompt.txt"
    
    # Test with experiment assets
    python3 scripts/prompt_engineering_harness.py --model "vertex_ai/gemini-2.5-flash" --experiment "projects/simple_experiment" --corpus "speech1.txt"
    
    # List available models
    python3 scripts/prompt_engineering_harness.py --list-models
"""

import sys
import os
import argparse
import json
from pathlib import Path
from typing import Optional, Dict, Any, Tuple

# Add project root to path for imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Load environment variables from .env file
from dotenv import load_dotenv
load_dotenv()

from discernus.gateway.model_registry import ModelRegistry
import litellm

def direct_model_call(model: str, prompt: str, system_prompt: str = "You are a helpful assistant.") -> Tuple[str, Dict[str, Any]]:
    """
    Makes a direct call to the specified model WITHOUT fallback.
    If the model fails, the harness should fail - no hiding problems.
    """
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": prompt}
    ]
    
    print(f"🎯 Making direct call to: {model}")
    print(f"📝 System prompt: {system_prompt[:100]}{'...' if len(system_prompt) > 100 else ''}")
    print(f"💬 User prompt: {prompt[:200]}{'...' if len(prompt) > 200 else ''}")
    print("=" * 80)
    
    try:
        response = litellm.completion(
            model=model, 
            messages=messages, 
            stream=False,
            timeout=120
        )
        
        content = getattr(getattr(getattr(response, 'choices', [{}])[0], 'message', {}), 'content', '') or ""
        usage_obj = getattr(response, 'usage', None)
        
        usage_data = {
            "prompt_tokens": getattr(usage_obj, 'prompt_tokens', 0) if usage_obj else 0,
            "completion_tokens": getattr(usage_obj, 'completion_tokens', 0) if usage_obj else 0,
            "total_tokens": getattr(usage_obj, 'total_tokens', 0) if usage_obj else 0,
        }
        
        return content, {"success": True, "model": model, "usage": usage_data}
        
    except Exception as e:
        print(f"❌ DIRECT CALL FAILED: {e}")
        return "", {"success": False, "error": str(e), "model": model}

def load_prompt_from_file(file_path: str) -> str:
    """Load prompt text from a file."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Prompt file not found: {file_path}")
    return path.read_text().strip()

def load_experiment_assets(experiment_dir: str, corpus_file: str) -> Tuple[str, str]:
    """Load framework and corpus from experiment directory."""
    exp_path = Path(experiment_dir)
    if not exp_path.exists():
        raise FileNotFoundError(f"Experiment directory not found: {experiment_dir}")
    
    # Look for framework file
    framework_files = list(exp_path.glob("framework.md")) + list(exp_path.glob("*framework*.md"))
    if not framework_files:
        raise FileNotFoundError(f"No framework file found in {experiment_dir}")
    
    framework_content = framework_files[0].read_text()
    
    # Look for corpus file
    corpus_path = exp_path / "corpus" / corpus_file
    if not corpus_path.exists():
        # Try direct path
        corpus_path = exp_path / corpus_file
        if not corpus_path.exists():
            raise FileNotFoundError(f"Corpus file not found: {corpus_file} in {experiment_dir}")
    
    corpus_content = corpus_path.read_text()
    
    return framework_content, corpus_content

def list_available_models() -> None:
    """List all models available in the registry."""
    registry = ModelRegistry()
    models = registry.list_models()
    
    if not models:
        print("❌ No models found in registry")
        return
    
    print(f"📋 Available Models ({len(models)}):")
    print("=" * 60)
    
    # Group by provider
    by_provider = {}
    for model in models:
        details = registry.get_model_details(model)
        provider = details.get('provider', 'unknown') if details else 'unknown'
        if provider not in by_provider:
            by_provider[provider] = []
        by_provider[provider].append(model)
    
    for provider, provider_models in sorted(by_provider.items()):
        print(f"\n🔧 {provider.upper()}:")
        for model in sorted(provider_models):
            details = registry.get_model_details(model)
            tier = details.get('utility_tier', '?') if details else '?'
            perf = details.get('performance_tier', '?') if details else '?'
            print(f"  - {model} (tier: {tier}, perf: {perf})")

def main():
    parser = argparse.ArgumentParser(
        description="Flexible prompt engineering harness for testing specific models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --model "anthropic/claude-3-5-sonnet-20240620" --prompt "What is 2+2?"
  %(prog)s --model "perplexity/r1-1776" --prompt-file "my_test.txt"
  %(prog)s --model "vertex_ai/gemini-2.5-flash" --experiment "projects/simple_experiment" --corpus "speech1.txt"
  %(prog)s --list-models
        """
    )
    
    # Model selection (required unless listing)
    parser.add_argument('--model', '-m', 
                       help='Model to test (from model registry)')
    
    # Prompt options (mutually exclusive)
    prompt_group = parser.add_mutually_exclusive_group()
    prompt_group.add_argument('--prompt', '-p',
                             help='Direct prompt text to test')
    prompt_group.add_argument('--prompt-file', '-f',
                             help='Path to file containing prompt text')
    
    # Experiment-based testing
    parser.add_argument('--experiment', '-e',
                       help='Path to experiment directory')
    parser.add_argument('--corpus', '-c',
                       help='Corpus file name (used with --experiment)')
    
    # System prompt customization
    parser.add_argument('--system-prompt', '-s',
                       default="You are a helpful assistant.",
                       help='Custom system prompt (default: "You are a helpful assistant.")')
    
    # Utility actions
    parser.add_argument('--list-models', '-l', action='store_true',
                       help='List all available models in registry')
    
    args = parser.parse_args()
    
    # Handle list models
    if args.list_models:
        list_available_models()
        return
    
    # Validate model is provided
    if not args.model:
        parser.error("--model is required unless using --list-models")
    
    # Validate model exists in registry
    registry = ModelRegistry()
    if args.model not in registry.list_models():
        print(f"❌ Model '{args.model}' not found in registry")
        print("\nRun with --list-models to see available models")
        sys.exit(1)
    
    # Determine prompt source
    prompt_text = ""
    
    if args.experiment and args.corpus:
        # Load from experiment
        try:
            framework_content, corpus_content = load_experiment_assets(args.experiment, args.corpus)
            
            # Create experiment-based prompt (simplified version)
            prompt_text = f"""Please analyze the following text according to the provided framework.

FRAMEWORK:
{framework_content[:2000]}{'...' if len(framework_content) > 2000 else ''}

TEXT TO ANALYZE:
{corpus_content}

Provide your analysis following the framework's methodology."""
            
            print(f"✅ Loaded experiment from: {args.experiment}")
            print(f"✅ Using corpus: {args.corpus}")
            
        except Exception as e:
            print(f"❌ Failed to load experiment assets: {e}")
            sys.exit(1)
            
    elif args.prompt_file:
        # Load from file
        try:
            prompt_text = load_prompt_from_file(args.prompt_file)
            print(f"✅ Loaded prompt from: {args.prompt_file}")
        except Exception as e:
            print(f"❌ Failed to load prompt file: {e}")
            sys.exit(1)
            
    elif args.prompt:
        # Use direct prompt
        prompt_text = args.prompt
        print(f"✅ Using direct prompt")
        
    else:
        parser.error("Must specify either --prompt, --prompt-file, or --experiment with --corpus")
    
    # Execute the test
    print(f"\n🚀 Testing Model: {args.model}")
    print("=" * 80)
    
    response, metadata = direct_model_call(args.model, prompt_text, args.system_prompt)
    
    print("\n📊 RESULTS:")
    print("=" * 80)
    
    if metadata["success"]:
        print("✅ SUCCESS")
        print(f"📝 Response Length: {len(response)} characters")
        if metadata.get("usage"):
            usage = metadata["usage"]
            print(f"🔢 Token Usage: {usage.get('prompt_tokens', 0)} prompt + {usage.get('completion_tokens', 0)} completion = {usage.get('total_tokens', 0)} total")
        
        print(f"\n📄 MODEL RESPONSE:")
        print("-" * 40)
        print(response)
        print("-" * 40)
        
    else:
        print("❌ FAILED")
        print(f"💥 Error: {metadata.get('error', 'Unknown error')}")
        print("\nThis is intentional - no fallback mechanism to hide the problem.")
    
    print(f"\n🏁 Test completed for model: {args.model}")

if __name__ == '__main__':
    main() 