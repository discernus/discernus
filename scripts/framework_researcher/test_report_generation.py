#!/usr/bin/env python3
"""
Test script to verify enhanced report generation without API calls
"""

import sys
from pathlib import Path

# Add the framework_validation directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "framework_validation"))

from enhanced_framework_validator import EnhancedFrameworkValidator

def test_report_generation():
    """Test enhanced report generation with mock data"""
    
    print("🧪 Testing Enhanced Report Generation...")
    
    # Initialize validator
    validator = EnhancedFrameworkValidator()
    
    # Mock data
    framework_path = "test_framework.md"
    structural_results = {
        'status': 'PASSED',
        'structural_score': 8.0,
        'summary': 'Framework validation passed',
        'issues': [
            {
                'type': 'QUALITY',
                'description': 'Minor scoring calibration inconsistency',
                'impact': 'Low impact on framework functionality',
                'fix': 'Standardize scoring ranges across dimensions'
            }
        ]
    }
    academic_results = {
        'academic_credibility_score': 7,
        'confidence_level': 'HIGH',
        'theoretical_validation': 'Strong theoretical foundations grounded in established populism literature',
        'literature_coverage': 'Good coverage of core concepts with room for expansion',
        'research_gaps': 'Minor gaps in cross-cultural applicability identified',
        'methodological_validation': 'Methodologically sound with clear operationalization',
        'recommendations': ['Improve citations', 'Expand examples', 'Address cross-cultural validity']
    }
    integrated_results = {
        'overall_score': 7.5,
        'overall_status': 'GOOD',
        'confidence_level': 'HIGH',
        'recommendations': 'Framework is well-structured and academically sound with minor improvements needed'
    }
    research_directions = {
        'research_questions': [
            {
                'priority': 1,
                'question': 'How does strategic contradiction theory support the tension mathematics?',
                'rationale': 'Core innovation needs theoretical grounding',
                'expected_outcomes': 'Validation or refinement of tension formula',
                'methodology_suggestions': 'Systematic literature review of political communication'
            },
            {
                'priority': 2,
                'question': 'What supports the three-tier dimensional categorization?',
                'rationale': 'Theoretical hierarchy needs academic justification',
                'expected_outcomes': 'Enhanced cross-ideological validity',
                'methodology_suggestions': 'Comparative literature review of populism studies'
            }
        ],
        'overall_research_strategy': 'Sequential validation from core innovation to foundational structure',
        'academic_impact': 'Significant enhancement of framework credibility and utility'
    }
    librarian_research = {
        'framework_path': 'test_framework.md',
        'total_questions': 2,
        'research_file_path': 'test_research.md',
        'research_results': [
            {
                'priority': 1,
                'question': 'How does strategic contradiction theory support the tension mathematics?',
                'status': 'COMPLETED',
                'summary': 'Research completed on strategic contradiction theory',
                'findings': 'Key findings on message inconsistency and cognitive dissonance',
                'detailed_report_path': 'test_detailed_report_1.md'
            },
            {
                'priority': 2,
                'question': 'What supports the three-tier dimensional categorization?',
                'status': 'COMPLETED',
                'summary': 'Research completed on dimensional categorization',
                'findings': 'Key findings on populism structure and host ideologies',
                'detailed_report_path': 'test_detailed_report_2.md'
            }
        ],
        'synthesis': {
            'theoretical_insights': 'Strategic contradiction theory provides partial support for tension formula',
            'literature_alignment': 'Strong alignment with populism core concepts, moderate with boundary distinctions',
            'theoretical_gaps': 'Tension mathematics needs additional theoretical grounding',
            'improvement_recommendations': 'Expand theoretical justification, refine dimensional structure',
            'research_gaps': 'Cross-cultural validation studies needed'
        }
    }
    
    # Generate report
    print("📝 Generating enhanced report...")
    report = validator._generate_enhanced_report(
        framework_path, structural_results, academic_results, 
        integrated_results, False, research_directions, librarian_research
    )
    
    # Debug: print report preview
    print(f"🔍 Report preview:\n{report}")
    
    # Debug: print the research directions section specifically
    if '## 🔬 Phase 4: Research Directions & Librarian Research' in report:
        start_idx = report.find('## 🔬 Phase 4: Research Directions & Librarian Research')
        end_idx = report.find('## 📊 Validation Summary')
        if end_idx == -1:
            end_idx = len(report)
        research_section = report[start_idx:end_idx]
        print(f"🔍 Research section:\n{research_section}")
    else:
        print("❌ Research section not found in report")
    
    # Debug: test the research directions method directly
    print("🔍 Testing research directions method directly...")
    research_section = validator._generate_research_directions_report_section(research_directions)
    print(f"🔍 Research section length: {len(research_section)} characters")
    print(f"🔍 Research section contains 'Three-tier dimensional categorization': {'Three-tier dimensional categorization' in research_section}")
    print(f"🔍 Research section preview:\n{research_section}")
    print(f"🔍 Full research section:\n{research_section}")
    
    # Debug: test string concatenation step by step
    print("🔍 Testing string concatenation step by step...")
    test_report = "Test report start\n"
    test_report += "Test section 1\n"
    test_report += research_section
    test_report += "Test section 2\n"
    print(f"🔍 Test report length: {len(test_report)} characters")
    print(f"🔍 Test report contains 'Three-tier dimensional categorization': {'Three-tier dimensional categorization' in test_report}")
    
    # Debug: check the research directions data directly
    print("🔍 Checking research directions data directly...")
    print(f"🔍 Research directions keys: {list(research_directions.keys())}")
    for key, value in research_directions.items():
        if isinstance(value, list):
            print(f"🔍 {key}: {len(value)} items")
            for i, item in enumerate(value):
                if isinstance(item, dict):
                    print(f"🔍   {key}[{i}] keys: {list(item.keys())}")
                    for subkey, subvalue in item.items():
                        if isinstance(subvalue, str):
                            print(f"🔍     {subkey}: {len(subvalue)} chars, contains 'Three-tier': {'Three-tier' in subvalue}")
                        else:
                            print(f"🔍     {subkey}: {type(subvalue)} = {subvalue}")
        elif isinstance(value, str):
            print(f"🔍 {key}: {len(value)} chars, contains 'Three-tier': {'Three-tier' in value}")
        else:
            print(f"🔍 {key}: {type(value)} = {value}")
    
    # Debug: print report length and check for specific content
    print(f"🔍 Full report length: {len(report)} characters")
    print(f"🔍 Contains 'Three-tier dimensional categorization': {'Three-tier dimensional categorization' in report}")
    print(f"🔍 Contains 'Strategic contradiction theory': {'Strategic contradiction theory' in report}")
    
    # Debug: print the end of the report to see where it's getting cut off
    print(f"🔍 End of report:\n{report[-500:]}")
    
    # Verify report structure
    print("🔍 Verifying report structure...")
    
    required_sections = [
        '## 📋 Phase 1: Structural Validation',
        '## 📚 Phase 2: Academic Validation', 
        '## 🎯 Phase 3: Integrated Assessment',
        '## 🔬 Phase 4: Research Directions & Librarian Research',
        '## 📊 Validation Summary'
    ]
    
    missing_sections = []
    for section in required_sections:
        if section not in report:
            missing_sections.append(section)
    
    if missing_sections:
        print(f"❌ Missing sections: {missing_sections}")
        return False
    
    # Verify content
    print("🔍 Verifying report content...")
    
    required_content = [
        'Framework validation passed',
        'Strong theoretical foundations',
        'Strategic contradiction theory',
        'Three-tier dimensional categorization',
        'Enhanced validation with structural + academic assessment + research synthesis'
    ]
    
    missing_content = []
    for content in required_content:
        if content not in report:
            missing_content.append(content)
    
    if missing_content:
        print(f"❌ Missing content: {missing_content}")
        return False
    
    print("✅ Enhanced report generation test PASSED!")
    print(f"📄 Report length: {len(report)} characters")
    
    # Save test report
    test_report_path = Path(__file__).parent / "test_enhanced_report.md"
    with open(test_report_path, 'w', encoding='utf-8') as f:
        f.write(report)
    print(f"📄 Test report saved to: {test_report_path}")
    
    return True

if __name__ == "__main__":
    success = test_report_generation()
    sys.exit(0 if success else 1)
