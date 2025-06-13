#!/usr/bin/env python3
"""
Test QA Integration

Tests the new QAEnhancedDataExporter to validate that Phase 1 of QA integration
is working properly. This script tests the enhanced academic data export with
quality assurance validation.
"""

import sys
import os
from pathlib import Path
from datetime import datetime

# Add the project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root / "src"))

def test_qa_enhanced_export():
    """Test the QA-enhanced data export functionality."""
    
    print("🧪 Testing QA Integration - Phase 1")
    print("=" * 50)
    
    try:
        # Import QA-enhanced exporter
        from narrative_gravity.academic.data_export import QAEnhancedDataExporter
        print("✅ QAEnhancedDataExporter imported successfully")
        
        # Initialize exporter
        exporter = QAEnhancedDataExporter()
        print(f"✅ QA system available: {exporter.qa_available}")
        
        if not exporter.qa_available:
            print("⚠️  QA system not available - testing basic functionality only")
        
        # Test export with QA validation
        print("\n🔍 Testing QA-enhanced data export...")
        
        # Export recent experimental data with QA validation
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        study_name = f"qa_integration_test_{timestamp}"
        
        output_files = exporter.export_experiments_data(
            study_name=study_name,
            start_date="2025-06-01",  # Recent data
            include_qa_validation=True,
            qa_confidence_threshold=0.5,
            output_dir="exports/qa_integration_test"
        )
        
        print(f"\n📦 Export completed successfully!")
        print(f"📁 Generated {len(output_files)} files:")
        
        for format_name, file_path in output_files.items():
            file_size = Path(file_path).stat().st_size if Path(file_path).exists() else 0
            print(f"   - {format_name}: {file_path} ({file_size:,} bytes)")
        
        # Validate QA report if generated
        if 'qa_report' in output_files:
            print("\n🔍 QA Validation Report Generated:")
            import json
            
            qa_report_path = Path(output_files['qa_report'])
            if qa_report_path.exists():
                with open(qa_report_path, 'r') as f:
                    qa_report = json.load(f)
                
                print(f"   - Total runs analyzed: {qa_report.get('total_runs', 0)}")
                print(f"   - High confidence: {qa_report.get('high_confidence_count', 0)}")
                print(f"   - Medium confidence: {qa_report.get('medium_confidence_count', 0)}")
                print(f"   - Low confidence: {qa_report.get('low_confidence_count', 0)}")
                
                quality_issues = qa_report.get('quality_issues', {})
                print(f"   - Critical issues: {quality_issues.get('total_critical_issues', 0)}")
                print(f"   - Anomalies detected: {quality_issues.get('total_anomalies_detected', 0)}")
                print(f"   - Second opinion needed: {quality_issues.get('second_opinion_rate', '0%')}")
                
                overall_quality = qa_report.get('quality_assessment', {}).get('overall_quality', 'UNKNOWN')
                print(f"   - Overall quality: {overall_quality}")
        
        # Test CSV output structure
        if 'csv' in output_files:
            print("\n📊 Validating CSV output structure...")
            import pandas as pd
            
            csv_path = Path(output_files['csv'])
            if csv_path.exists():
                df = pd.read_csv(csv_path)
                print(f"   - Rows: {len(df)}")
                print(f"   - Columns: {len(df.columns)}")
                
                # Check for QA columns
                qa_columns = [col for col in df.columns if col.startswith('qa_')]
                print(f"   - QA columns: {len(qa_columns)}")
                
                if qa_columns:
                    print("   - QA columns found:")
                    for col in qa_columns:
                        print(f"     • {col}")
                    
                    # Check confidence score distribution
                    if 'qa_confidence_score' in df.columns:
                        confidence_stats = df['qa_confidence_score'].describe()
                        print(f"   - Confidence score stats:")
                        print(f"     • Mean: {confidence_stats['mean']:.3f}")
                        print(f"     • Min: {confidence_stats['min']:.3f}")
                        print(f"     • Max: {confidence_stats['max']:.3f}")
                    
                    # Check confidence level distribution
                    if 'qa_confidence_level' in df.columns:
                        level_counts = df['qa_confidence_level'].value_counts()
                        print(f"   - Confidence level distribution:")
                        for level, count in level_counts.items():
                            print(f"     • {level}: {count}")
                else:
                    print("   - No QA columns found (QA validation may have been skipped)")
        
        print("\n✅ QA Integration Test Complete")
        return True
        
    except ImportError as e:
        print(f"❌ Import failed: {e}")
        print("💡 Make sure you've run: source scripts/setup_dev_env.sh")
        return False
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_convenience_function():
    """Test the convenience function for QA-enhanced export."""
    
    print("\n🧪 Testing Convenience Function")
    print("=" * 30)
    
    try:
        from narrative_gravity.academic.data_export import export_qa_enhanced_academic_data
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        study_name = f"convenience_test_{timestamp}"
        
        print(f"🔍 Testing convenience function: export_qa_enhanced_academic_data()")
        
        output_files = export_qa_enhanced_academic_data(
            study_name=study_name,
            include_qa_validation=True,
            start_date="2025-06-01",
            output_dir="exports/qa_convenience_test"
        )
        
        print(f"✅ Convenience function test successful!")
        print(f"📁 Generated {len(output_files)} files via convenience function")
        
        return True
        
    except Exception as e:
        print(f"❌ Convenience function test failed: {e}")
        return False

def main():
    """Run all QA integration tests."""
    
    print("🚀 QA Integration Testing Suite")
    print("=" * 60)
    print(f"📅 Test run: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Set up environment
    os.chdir(project_root)
    
    # Run tests
    tests = [
        ("Core QA Integration", test_qa_enhanced_export),
        ("Convenience Function", test_convenience_function)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name} {'='*20}")
        try:
            success = test_func()
            results.append((test_name, success))
        except Exception as e:
            print(f"❌ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "="*60)
    print("🏁 TEST SUMMARY")
    print("="*60)
    
    passed = sum(1 for _, success in results if success)
    total = len(results)
    
    for test_name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}  {test_name}")
    
    print(f"\n📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All QA integration tests passed!")
        print("🚀 Phase 1 QA integration is operational!")
        return 0
    else:
        print("⚠️  Some tests failed - check output above for details")
        return 1

if __name__ == "__main__":
    exit(main()) 