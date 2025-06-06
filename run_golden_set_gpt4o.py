#!/usr/bin/env python3
"""
Golden Set Analysis with GPT-4o
Run end-to-end narrative gravity analysis on all presidential speech txt files using GPT-4o
"""

import sys
import json
import time
import os
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, List

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.api_clients.direct_api_client import DirectAPIClient

# Analysis frameworks
FRAMEWORKS = [
    "civic_virtue",
    "political_spectrum", 
    "moral_rhetorical_posture"
]

# Golden set corpus path
GOLDEN_SET_PATH = Path("corpus/golden_set/presidential_speeches/txt")

def load_golden_set_texts():
    """Load all txt files from the golden set corpus"""
    texts = {}
    
    if not GOLDEN_SET_PATH.exists():
        print(f"❌ Golden set path not found: {GOLDEN_SET_PATH}")
        return texts
    
    # Get all txt files (excluding .DS_Store)
    txt_files = [f for f in GOLDEN_SET_PATH.glob("*.txt") if not f.name.startswith('.')]
    
    print(f"📚 Found {len(txt_files)} presidential speeches:")
    
    for txt_file in sorted(txt_files):
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
                texts[txt_file.stem] = {
                    'content': content,
                    'file_path': str(txt_file),
                    'size_chars': len(content),
                    'size_words': len(content.split())
                }
                print(f"  📄 {txt_file.name} - {len(content):,} chars, {len(content.split()):,} words")
        except Exception as e:
            print(f"  ❌ Failed to load {txt_file.name}: {e}")
    
    return texts

def run_golden_set_analysis():
    """Run GPT-4o analysis on all golden set texts"""
    
    print("🚀 Golden Set Analysis with GPT-4o")
    print("=" * 50)
    
    # Load texts
    texts = load_golden_set_texts()
    if not texts:
        print("❌ No texts loaded. Exiting.")
        return
    
    # Initialize client
    try:
        client = DirectAPIClient()
        print("✅ DirectAPIClient initialized")
    except Exception as e:
        print(f"❌ Failed to initialize client: {e}")
        return
    
    # Create output directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = Path(f"analysis_results/golden_set_gpt4o_{timestamp}")
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"📁 Output directory: {output_dir}")
    print(f"🤖 Model: gpt-4o")
    print(f"📊 Frameworks: {', '.join(FRAMEWORKS)}")
    print(f"📚 Texts: {len(texts)}")
    print("=" * 50)
    
    # Track overall results
    all_results = {}
    total_cost = 0.0
    successful_analyses = 0
    failed_analyses = 0
    
    # Process each text
    for text_id, text_info in texts.items():
        print(f"\n📄 Processing: {text_id}")
        print(f"   Size: {text_info['size_chars']:,} chars, {text_info['size_words']:,} words")
        
        text_results = {}
        text_cost = 0.0
        
        # Run analysis for each framework
        for framework in FRAMEWORKS:
            print(f"   🔍 Framework: {framework}")
            
            try:
                start_time = time.time()
                result, cost = client.analyze_text(text_info['content'], framework, "gpt-4o")
                duration = time.time() - start_time
                
                text_results[framework] = {
                    "success": True,
                    "result": result,
                    "cost": cost,
                    "duration": duration,
                    "timestamp": datetime.now().isoformat()
                }
                
                text_cost += cost
                successful_analyses += 1
                
                print(f"      ✅ Success - Cost: ${cost:.4f}, Duration: {duration:.1f}s")
                
                # Show key insights
                if "scores" in result and result["scores"]:
                    top_scores = sorted(result["scores"].items(), key=lambda x: x[1], reverse=True)[:2]
                    print(f"      📊 Top: {', '.join([f'{k}({v:.2f})' for k, v in top_scores])}")
                
            except Exception as e:
                text_results[framework] = {
                    "success": False,
                    "error": str(e),
                    "timestamp": datetime.now().isoformat()
                }
                failed_analyses += 1
                print(f"      ❌ Failed: {e}")
        
        # Save individual text results
        text_file = output_dir / f"{text_id}_analysis.json"
        with open(text_file, 'w') as f:
            json.dump({
                "text_id": text_id,
                "text_info": text_info,
                "model": "gpt-4o",
                "frameworks": text_results,
                "total_cost": text_cost,
                "analysis_timestamp": datetime.now().isoformat()
            }, f, indent=2, default=str)
        
        all_results[text_id] = text_results
        total_cost += text_cost
        
        print(f"   💰 Text cost: ${text_cost:.4f}")
        print(f"   💾 Saved: {text_file.name}")
    
    # Create comprehensive summary
    summary = {
        "analysis_timestamp": datetime.now().isoformat(),
        "model": "gpt-4o",
        "frameworks": FRAMEWORKS,
        "corpus_path": str(GOLDEN_SET_PATH),
        "total_texts": len(texts),
        "total_frameworks": len(FRAMEWORKS),
        "total_analyses": len(texts) * len(FRAMEWORKS),
        "successful_analyses": successful_analyses,
        "failed_analyses": failed_analyses,
        "success_rate": successful_analyses / (successful_analyses + failed_analyses) if (successful_analyses + failed_analyses) > 0 else 0,
        "total_cost": total_cost,
        "average_cost_per_text": total_cost / len(texts) if texts else 0,
        "average_cost_per_analysis": total_cost / successful_analyses if successful_analyses > 0 else 0,
        "corpus_stats": {
            "total_chars": sum(info['size_chars'] for info in texts.values()),
            "total_words": sum(info['size_words'] for info in texts.values()),
            "avg_chars_per_text": sum(info['size_chars'] for info in texts.values()) / len(texts) if texts else 0,
            "avg_words_per_text": sum(info['size_words'] for info in texts.values()) / len(texts) if texts else 0
        },
        "results": all_results
    }
    
    # Save summary
    summary_file = output_dir / "golden_set_analysis_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(summary, f, indent=2, default=str)
    
    # Print final results
    print("\n" + "=" * 50)
    print("📊 GOLDEN SET ANALYSIS COMPLETE")
    print("=" * 50)
    print(f"🤖 Model: gpt-4o")
    print(f"📚 Texts analyzed: {len(texts)}")
    print(f"🔍 Frameworks: {len(FRAMEWORKS)}")
    print(f"✅ Successful analyses: {successful_analyses}")
    print(f"❌ Failed analyses: {failed_analyses}")
    print(f"📈 Success rate: {summary['success_rate']:.1%}")
    print(f"💰 Total cost: ${total_cost:.4f}")
    print(f"💵 Average cost per text: ${summary['average_cost_per_text']:.4f}")
    print(f"📁 Results saved in: {output_dir}")
    print(f"📄 Summary: {summary_file.name}")
    
    # Corpus statistics
    print(f"\n📊 Corpus Statistics:")
    print(f"   Total characters: {summary['corpus_stats']['total_chars']:,}")
    print(f"   Total words: {summary['corpus_stats']['total_words']:,}")
    print(f"   Average per text: {summary['corpus_stats']['avg_chars_per_text']:,.0f} chars, {summary['corpus_stats']['avg_words_per_text']:,.0f} words")
    
    return summary

if __name__ == "__main__":
    run_golden_set_analysis() 