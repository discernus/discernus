#!/usr/bin/env python3
"""
FULL DATABASE STRESS TEST 🔥

Tests the complete database-first architecture:
1. Obama Inaugural + Claude 3.5 Sonnet (5 runs)
2. Trump Joint Session + GPT-4o (5 runs) 
3. Dashboard generation from database
4. Academic exports
5. Corpus analysis

Let's watch everything burn down! 😄
"""

import sys
import asyncio
import time
import json
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from test_database_stress_obama_claude import test_obama_inaugural_claude
from test_database_stress_trump_gpt4o import test_trump_joint_gpt4o
from create_generic_multi_run_dashboard import create_dashboard
from src.utils.statistical_logger import logger

def full_database_stress_test():
    """Run comprehensive database stress test"""
    
    print("🔥🔥🔥 FULL DATABASE STRESS TEST 🔥🔥🔥")
    print("=" * 60)
    print("Testing: Database logging, multi-run analysis, dashboards, exports")
    print("Expected casualties: JSON files, sanity, possibly the server")
    print("=" * 60)
    
    test_results = {}
    
    # TEST 1: Obama Inaugural + Claude
    print("\n\n🎯 TEST 1: Obama Inaugural + Claude 3.5 Sonnet")
    print("-" * 50)
    
    try:
        obama_data = test_obama_inaugural_claude()
        if obama_data:
            print("✅ Obama/Claude test completed successfully")
            test_results['obama_claude'] = obama_data
        else:
            print("❌ Obama/Claude test failed")
    except Exception as e:
        print(f"💥 Obama/Claude test exploded: {e}")
        test_results['obama_claude'] = None
    
    # TEST 2: Trump Joint Session + GPT-4o  
    print("\n\n🎯 TEST 2: Trump Joint Session + GPT-4o")
    print("-" * 50)
    
    try:
        trump_data = test_trump_joint_gpt4o()
        if trump_data:
            print("✅ Trump/GPT-4o test completed successfully")
            test_results['trump_gpt4o'] = trump_data
        else:
            print("❌ Trump/GPT-4o test failed")
    except Exception as e:
        print(f"💥 Trump/GPT-4o test exploded: {e}")
        test_results['trump_gpt4o'] = None
    
    # TEST 3: Dashboard Generation + Database Logging
    print("\n\n🎯 TEST 3: Dashboard Generation + Database Logging")
    print("-" * 50)
    
    dashboard_count = 0
    for test_name, data in test_results.items():
        if data is None:
            continue
            
        try:
            print(f"\n📊 Generating dashboard for {test_name}...")
            
            # Save data to JSON file first (expected format)
            output_dir = Path("model_output/stress_test/")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            # Create filename in expected format
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            model_name_clean = data['metadata']['model'].replace('-', '_').replace('.', '_')
            json_filename = f"{data['metadata']['speaker'].lower()}_{test_name}_{model_name_clean}_{timestamp}.json"
            json_filepath = output_dir / json_filename
            
            # Save raw data to JSON file
            with open(json_filepath, 'w') as f:
                json.dump(data, f, indent=2, default=str)
            
            print(f"   💾 Saved data to: {json_filepath}")
            
            # Now generate dashboard from the file (this triggers database logging!)
            dashboard_file = create_dashboard(
                results_file=str(json_filepath),
                speaker=data['metadata']['speaker'],
                speech_type=data['metadata']['speech_type'],
                framework=data['metadata']['framework']
            )
            
            if dashboard_file:
                print(f"✅ Dashboard created: {dashboard_file}")
                dashboard_count += 1
            else:
                print(f"❌ Dashboard creation failed for {test_name}")
                
        except Exception as e:
            print(f"💥 Dashboard generation exploded for {test_name}: {e}")
            import traceback
            traceback.print_exc()
    
    # TEST 4: Database Query & Analysis
    print("\n\n🎯 TEST 4: Database Corpus Analysis")
    print("-" * 50)
    
    try:
        # Check what we logged
        stats = logger.get_corpus_stats()
        print(f"📊 DATABASE CONTENTS:")
        print(f"   Total Runs: {stats.get('total_runs', 0)}")
        print(f"   Total Jobs: {stats.get('total_jobs', 0)}")
        print(f"   Total Cost: ${stats.get('total_cost', 0):.4f}")
        print(f"   Unique Models: {stats.get('unique_models', 0)}")
        
        # Show model distribution
        if stats.get('model_distribution'):
            print(f"\n🤖 MODEL DISTRIBUTION:")
            for model_info in stats['model_distribution']:
                print(f"   {model_info['model']}: {model_info['count']} runs")
        
        # Show speaker distribution  
        if stats.get('speaker_distribution'):
            print(f"\n🎤 SPEAKER DISTRIBUTION:")
            for speaker_info in stats['speaker_distribution']:
                print(f"   {speaker_info['speaker']}: {speaker_info['count']} runs")
        
        print("✅ Database analysis completed")
        
    except Exception as e:
        print(f"💥 Database analysis exploded: {e}")
        import traceback
        traceback.print_exc()
    
    # TEST 5: Academic Exports
    print("\n\n🎯 TEST 5: Academic Export Testing")
    print("-" * 50)
    
    try:
        if stats.get('total_runs', 0) > 0:
            print("📚 Generating academic exports...")
            
            exports = logger.export_for_academics(
                export_format="all",
                output_dir="exports/stress_test/",
                include_raw_responses=False  # Keep it manageable
            )
            
            print("✅ ACADEMIC EXPORTS GENERATED:")
            for format_name, files in exports.items():
                print(f"\n   {format_name.upper()}:")
                if isinstance(files, dict):
                    for file_type, filepath in files.items():
                        print(f"     {file_type}: {filepath}")
                else:
                    print(f"     {files}")
        else:
            print("⚠️ No data in database - skipping academic exports")
            
    except Exception as e:
        print(f"💥 Academic export exploded: {e}")
        import traceback
        traceback.print_exc()
    
    # FINAL DAMAGE REPORT
    print("\n\n🏆 STRESS TEST DAMAGE REPORT")
    print("=" * 60)
    
    successful_tests = len([k for k, v in test_results.items() if v is not None])
    print(f"✅ Successful API tests: {successful_tests}/2")
    print(f"📊 Dashboards generated: {dashboard_count}")
    print(f"🗄️ Database entries: {stats.get('total_runs', 0)} runs, {stats.get('total_jobs', 0)} jobs")
    print(f"💰 Total spent: ${stats.get('total_cost', 0):.4f}")
    
    if successful_tests == 2 and dashboard_count == 2 and stats.get('total_runs', 0) > 0:
        print("\n🎉 STRESS TEST PASSED! Database architecture survived! 🎉")
    else:
        print("\n💥 STRESS TEST REVEALED ISSUES - Check logs above")
    
    print("\n🔍 Next steps:")
    print("   • Check database contents")
    print("   • Review generated dashboards")
    print("   • Test academic export files")
    print("   • Query corpus for analysis")

if __name__ == "__main__":
    full_database_stress_test() 