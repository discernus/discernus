#!/usr/bin/env python3
"""
Single Model Single File Test: Trump Joint Address Analysis
Test the civic virtue framework with GPT-4o on Trump's joint address
"""

import sys
import json
import time
from pathlib import Path
from datetime import datetime
from typing import Dict, Any

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.api_clients.direct_api_client import DirectAPIClient

def load_trump_joint_text():
    """Load the Trump joint address txt file"""
    trump_file = Path("corpus/golden_set/presidential_speeches/txt/golden_trump_joint_01.txt")
    
    if not trump_file.exists():
        raise FileNotFoundError(f"Trump joint address file not found: {trump_file}")
    
    with open(trump_file, 'r', encoding='utf-8') as f:
        text = f.read().strip()
    
    print(f"📄 Loaded: {trump_file.name}")
    print(f"📏 Length: {len(text):,} characters")
    print(f"📝 Preview: {text[:200]}...")
    
    return text

def run_single_analysis():
    """Run civic virtue analysis on Trump joint address with GPT-4o"""
    
    print("🧪 Single Model Single File Test")
    print("=" * 50)
    print("🤖 Model: GPT-4o")
    print("📊 Framework: Civic Virtue")
    print("📄 File: Trump Joint Address")
    print()
    
    # Initialize client
    try:
        client = DirectAPIClient()
        print("✅ DirectAPIClient initialized")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return
    
    # Load text
    try:
        text = load_trump_joint_text()
        print("✅ Text loaded successfully")
    except Exception as e:
        print(f"❌ Failed to load text: {e}")
        return
    
    print()
    
    # Run analysis
    print("🔄 Running civic virtue analysis...")
    start_time = time.time()
    
    try:
        result, cost = client.analyze_text(text, "civic_virtue", "gpt-4o")
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"✅ Analysis completed in {duration:.1f} seconds")
        print(f"💰 Cost: ${cost:.4f}")
        print()
        
        # Display results
        print("📊 CIVIC VIRTUE ANALYSIS RESULTS")
        print("=" * 40)
        
        if 'scores' in result:
            scores = result['scores']
            print("\n🏛️ CIVIC VIRTUE WELLS:")
            
            # Positive wells
            positive_wells = ['Dignity', 'Truth', 'Hope', 'Justice', 'Pragmatism']
            print("\n✨ Positive Wells:")
            for well in positive_wells:
                if well in scores:
                    score = scores[well]
                    print(f"  {well:12}: {score:.2f}")
            
            # Negative wells
            negative_wells = ['Tribalism', 'Manipulation', 'Fantasy', 'Resentment', 'Fear']
            print("\n⚠️ Negative Wells:")
            for well in negative_wells:
                if well in scores:
                    score = scores[well]
                    print(f"  {well:12}: {score:.2f}")
            
            # Calculate aggregate scores
            positive_total = sum(scores.get(well, 0) for well in positive_wells)
            negative_total = sum(scores.get(well, 0) for well in negative_wells)
            overall_score = positive_total - negative_total
            
            print(f"\n📈 SUMMARY:")
            print(f"  Positive Total: {positive_total:.2f}")
            print(f"  Negative Total: {negative_total:.2f}")
            print(f"  Overall Score:  {overall_score:.2f}")
        
        # Display analysis if available
        if 'analysis' in result:
            analysis = result['analysis']
            print(f"\n📝 DETAILED ANALYSIS:")
            print("=" * 40)
            # Show first 500 characters of analysis
            print(analysis[:500] + ("..." if len(analysis) > 500 else ""))
        
        # Save results
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_file = f"trump_joint_civic_virtue_gpt4o_{timestamp}.json"
        
        output_data = {
            'file': 'golden_trump_joint_01.txt',
            'model': 'gpt-4o',
            'framework': 'civic_virtue',
            'timestamp': timestamp,
            'duration_seconds': duration,
            'cost_usd': cost,
            'character_count': len(text),
            'result': result
        }
        
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        
        print(f"\n💾 Results saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Analysis failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    run_single_analysis() 