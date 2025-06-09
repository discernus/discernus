#!/usr/bin/env python3
"""
Database Stress Test #1: Obama Inaugural + Claude 3.5 Sonnet
Multi-run analysis to test database logging system
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

def test_obama_inaugural_claude():
    """Test Obama inaugural speech with Claude 3.5 Sonnet multi-run"""
    
    print("🔥 STRESS TEST #1: Obama Inaugural + Claude")
    print("=" * 50)
    
    # Load Obama inaugural speech
    speech_file = Path("corpus/golden_set/presidential_speeches/txt/golden_obama_inaugural_01.txt")
    
    if not speech_file.exists():
        print(f"❌ Speech file not found: {speech_file}")
        return
        
    with open(speech_file, 'r', encoding='utf-8') as f:
        speech_text = f.read()
    
    print(f"📄 Loaded: {len(speech_text)} characters")
    print(f"📝 First 200 chars: {speech_text[:200]}...")
    
    # Initialize client and template manager
    client = DirectAPIClient()
    template_manager = PromptTemplateManager()
    
    print(f"\n🤖 Running 5-run analysis with Claude 3.5 Sonnet")
    
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
                model="claude-3-5-sonnet-20241022"
            )
            
            # Make API call using DirectAPIClient
            result, cost = client.analyze_text(
                text=speech_text,
                framework="civic_virtue", 
                model_name="claude-3-5-sonnet-20241022"
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
                    'model': 'claude-3-5-sonnet-20241022',
                    'temperature': 0.1,
                    'max_tokens': 4000
                },
                'api_metadata': {
                    'request_timestamp': time.time(),
                    'framework': 'civic_virtue'
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
    
    print(f"\n📊 SUMMARY:")
    print(f"   Success Rate: {successful_runs}/5 ({successful_runs/5*100:.0f}%)")
    print(f"   Total Cost: ${total_cost:.4f}")
    print(f"   Total Duration: {total_duration:.1f}s")
    print(f"   Avg Duration: {total_duration/5:.1f}s per run")
    
    # Prepare data for dashboard (which will log to database)
    raw_data = {
        'individual_runs': individual_runs,
        'input_text': speech_text,
        'metadata': {
            'speaker': 'Obama',
            'speech_type': 'Inaugural',
            'model': 'claude-3-5-sonnet-20241022',
            'framework': 'civic_virtue',
            'run_count': 5
        }
    }
    
    return raw_data

if __name__ == "__main__":
    test_obama_inaugural_claude() 