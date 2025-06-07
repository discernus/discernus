#!/usr/bin/env python3
"""
Database Stress Test #2: Trump Joint Session + GPT-4o
Large text multi-run analysis to stress test the database system
"""

import sys
import asyncio
import time
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from src.api_clients.direct_api_client import DirectAPIClient
from src.prompts.template_manager import PromptTemplateManager
from src.utils.statistical_logger import logger

def test_trump_joint_gpt4o():
    """Test Trump joint session speech with GPT-4o multi-run"""
    
    print("🔥 STRESS TEST #2: Trump Joint Session + GPT-4o")
    print("=" * 50)
    
    # Load Trump joint session speech (the big one!)
    speech_file = Path("corpus/golden_set/presidential_speeches/txt/golden_trump_joint_01.txt")
    
    if not speech_file.exists():
        print(f"❌ Speech file not found: {speech_file}")
        return
        
    with open(speech_file, 'r', encoding='utf-8') as f:
        speech_text = f.read()
    
    print(f"📄 Loaded: {len(speech_text)} characters (BIG TEXT!)")
    print(f"📝 First 200 chars: {speech_text[:200]}...")
    
    # Initialize client and template manager
    client = DirectAPIClient()
    template_manager = PromptTemplateManager()
    
    print(f"\n🤖 Running 5-run analysis with GPT-4o")
    print("⚠️ Warning: Large text may be expensive!")
    
    individual_runs = []
    total_cost = 0
    start_time = time.time()
    
    for run_num in range(1, 6):
        print(f"\n--- RUN {run_num}/5 ---")
        
        try:
            run_start = time.time()
            
            # Generate prompt using template manager
            prompt = template_manager.generate_api_prompt(
                text=speech_text,
                framework="civic_virtue",
                model="gpt-4o"
            )
            
            # Make API call using DirectAPIClient
            result, cost = client.analyze_text(
                text=speech_text,
                framework="civic_virtue",
                model_name="gpt-4o"
            )
            
            run_duration = time.time() - run_start
            run_cost = cost
            total_cost += run_cost
            
            print(f"✅ Success: ${run_cost:.4f}, {run_duration:.1f}s")
            
            # Store run data with enhanced logging info
            run_data = {
                'result': result,
                'cost': run_cost,
                'duration': run_duration,
                'success': True,
                'prompt': prompt,  # Enhanced: capture prompt
                'model_parameters': {
                    'model': 'gpt-4o',
                    'temperature': 0.1,
                    'max_tokens': 4000
                },
                'api_metadata': {
                    'request_timestamp': time.time(),
                    'framework': 'civic_virtue',
                    'text_length': len(speech_text)
                }
            }
            
            individual_runs.append(run_data)
            
        except Exception as e:
            print(f"❌ Failed: {e}")
            individual_runs.append({
                'result': {},
                'cost': 0,
                'duration': 0,
                'success': False,
                'error': str(e)
            })
    
    total_duration = time.time() - start_time
    successful_runs = len([r for r in individual_runs if r.get('success', False)])
    
    print(f"\n💰 COST ANALYSIS:")
    print(f"   Success Rate: {successful_runs}/5 ({successful_runs/5*100:.0f}%)")
    print(f"   Total Cost: ${total_cost:.4f}")
    print(f"   Total Duration: {total_duration:.1f}s")
    print(f"   Avg Duration: {total_duration/5:.1f}s per run")
    print(f"   Cost per successful run: ${total_cost/max(successful_runs,1):.4f}")
    
    # Prepare data for dashboard (which will log to database)
    raw_data = {
        'individual_runs': individual_runs,
        'input_text': speech_text,
        'metadata': {
            'speaker': 'Trump',
            'speech_type': 'Joint Session',
            'model': 'gpt-4o',
            'framework': 'civic_virtue',
            'run_count': 5
        }
    }
    
    return raw_data

if __name__ == "__main__":
    test_trump_joint_gpt4o() 