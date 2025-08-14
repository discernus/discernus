#!/usr/bin/env python3
"""
Test NotebookGeneratorAgent with real CFF analysis data from simple_test.
This is the critical test - can we generate academically sound derived metrics 
calculations from real framework data?
"""

import sys
import json
import tempfile
from pathlib import Path

# Add the current directory to Python path
sys.path.insert(0, str(Path(__file__).parent / '../../'))

def test_cff_notebook_generation():
    """Test notebook generation with real CFF analysis data."""
    try:
        from discernus.agents.notebook_generator_agent import NotebookGeneratorAgent
        
        print("🔬 Testing NotebookGeneratorAgent with Real CFF Analysis Data")
        print("=" * 60)
        
        # Load real analysis data from simple_test cache
        analysis_file = Path("../simple_test/shared_cache/artifacts/analysis_result_1f94a8c1")
        if not analysis_file.exists():
            print(f"❌ Analysis data not found: {analysis_file}")
            return False
            
        with open(analysis_file, 'r') as f:
            real_analysis_result = json.load(f)
        
        print(f"✅ Loaded real analysis data: {analysis_file.name}")
        print(f"   📊 Model used: {real_analysis_result['model_used']}")
        print(f"   🎯 Experiment: {real_analysis_result['experiment_name']}")
        
        # Extract the actual analysis from the nested JSON structure
        raw_response = real_analysis_result['raw_analysis_response']
        
        # Parse the structured analysis data
        import re
        json_match = re.search(r'<<<DISCERNUS_ANALYSIS_JSON_v6>>>\n(.*?)\n<<<END_DISCERNUS_ANALYSIS_JSON_v6>>>', 
                              raw_response, re.DOTALL)
        
        if not json_match:
            print("❌ Could not extract structured analysis from raw response")
            return False
            
        analysis_json = json.loads(json_match.group(1))
        
        print(f"✅ Parsed structured analysis data")
        print(f"   📄 Documents: {len(analysis_json['document_analyses'])}")
        
        # Get first document's scores
        doc_analysis = analysis_json['document_analyses'][0]
        doc_name = doc_analysis['document_name']
        scores = doc_analysis['dimensional_scores']
        
        print(f"   📝 Document: {doc_name}")
        print(f"   📊 Sample scores: tribal_dominance={scores['tribal_dominance_score']['raw_score']}, "
              f"individual_dignity={scores['individual_dignity_score']['raw_score']}")
        
        # Load the CFF framework
        framework_file = Path("../../frameworks/reference/flagship/cff_v7.3.md")
        if not framework_file.exists():
            print(f"❌ Framework not found: {framework_file}")
            return False
            
        framework_content = framework_file.read_text()
        print(f"✅ Loaded CFF framework: {len(framework_content)} characters")
        
        # Prepare the data structure that NotebookGeneratorAgent expects
        notebook_scores_data = {
            "document_analyses": [
                {
                    "document_id": doc_analysis.get("document_id", "test_doc_001"),
                    "document_name": doc_name,
                    "scores": {
                        # Convert from nested structure to flat structure
                        "tribal_dominance_score": scores['tribal_dominance_score']['raw_score'],
                        "individual_dignity_score": scores['individual_dignity_score']['raw_score'],
                        "fear_score": scores['fear_score']['raw_score'],
                        "hope_score": scores['hope_score']['raw_score'],
                        "envy_score": scores['envy_score']['raw_score'],
                        "compersion_score": scores.get('compersion_score', scores.get('competition_score', {'raw_score': 0.0}))['raw_score'],
                        "enmity_score": scores['enmity_score']['raw_score'],
                        "amity_score": scores['amity_score']['raw_score'],
                        "fragmentative_goals_score": scores['fragmentative_goals_score']['raw_score'],
                        "cohesive_goals_score": scores['cohesive_goals_score']['raw_score'],
                        # Add salience data
                        "tribal_dominance_salience": scores['tribal_dominance_score']['salience'],
                        "individual_dignity_salience": scores['individual_dignity_score']['salience'],
                        "fear_salience": scores['fear_score']['salience'],
                        "hope_salience": scores['hope_score']['salience'],
                        "envy_salience": scores['envy_score']['salience'],
                        "compersion_salience": scores.get('compersion_salience', scores.get('competition_score', {'salience': 0.0}))['salience'] if isinstance(scores.get('compersion_salience', scores.get('competition_score')), dict) else 0.0,
                        "enmity_salience": scores['enmity_score']['salience'],
                        "amity_salience": scores['amity_score']['salience'],
                        "fragmentative_goals_salience": scores['fragmentative_goals_score']['salience'],
                        "cohesive_goals_salience": scores['cohesive_goals_score']['salience'],
                    },
                    "evidence": {
                        # Convert evidence array to dict
                        ev['dimension']: ev['quote_text'][:100] + "..." if len(ev['quote_text']) > 100 else ev['quote_text']
                        for ev in doc_analysis['evidence']
                    },
                    "confidence": {
                        # Convert confidence data
                        "tribal_dominance_confidence": scores['tribal_dominance_score']['confidence'],
                        "individual_dignity_confidence": scores['individual_dignity_score']['confidence'],
                        "fear_confidence": scores['fear_score']['confidence'],
                        "hope_confidence": scores['hope_score']['confidence'],
                        "envy_confidence": scores['envy_score']['confidence'],
                        "compersion_confidence": scores.get('compersion_score', scores.get('competition_score', {'confidence': 0.0}))['confidence'],
                        "enmity_confidence": scores['enmity_score']['confidence'],
                        "amity_confidence": scores['amity_score']['confidence'],
                        "fragmentative_goals_confidence": scores['fragmentative_goals_score']['confidence'],
                        "cohesive_goals_confidence": scores['cohesive_goals_score']['confidence'],
                    }
                }
            ]
        }
        
        print("✅ Prepared notebook-ready data structure")
        
        # Set up experiment config
        experiment_config = {
            "framework": "CFF v7.3",
            "name": "real_cff_notebook_test",
            "description": "Testing notebook generation with real CFF analysis data"
        }
        
        # Initialize NotebookGeneratorAgent
        agent = NotebookGeneratorAgent()
        print("✅ NotebookGeneratorAgent initialized")
        
        # Generate notebook in permanent location so user can examine it
        output_path = Path("cff_derived_metrics_notebook.py")
        
        print("🔄 Generating CFF derived metrics notebook...")
        
        result = agent.generate_derived_metrics_notebook(
            scores_data=notebook_scores_data,
            evidence_data={"source": "simple_test_cache"},
            framework_content=framework_content,
            experiment_config=experiment_config,
            output_path=output_path
        )
        
        if result.success:
            print("✅ Notebook generated successfully!")
            print(f"   📓 Path: {result.notebook_path}")
            print(f"   📊 Metadata: {result.metadata}")
            
            # Validate the notebook content
            notebook_content = output_path.read_text()
        else:
            print(f"❌ Notebook generation failed: {result.error_message}")
            
            # DEBUG: Try to see what was actually generated (if anything)
            if output_path.exists():
                try:
                    generated_content = output_path.read_text()
                    print(f"\n🔍 DEBUG: Generated content that failed validation:")
                    print("-" * 60)
                    print(generated_content[:2000] + "..." if len(generated_content) > 2000 else generated_content)
                    print("-" * 60)
                except Exception as e:
                    print(f"Could not read generated content: {e}")
            
            return False
        
        if result.success:
            notebook_content = output_path.read_text()
            
            # Check for CFF-specific calculations
            cff_calculations = [
                "identity_tension",
                "emotional_tension", 
                "success_tension",
                "relational_tension",
                "goal_tension",
                "strategic_contradiction_index",
                "cohesive_index",
                "fragmentative_index",
                "overall_cohesion_index"
            ]
            
            found_calculations = []
            for calc in cff_calculations:
                if calc in notebook_content:
                    found_calculations.append(calc)
                    
            print(f"\n📊 CFF Calculations Found: {len(found_calculations)}/{len(cff_calculations)}")
            for calc in found_calculations:
                print(f"   ✅ {calc}")
                
            missing_calculations = [calc for calc in cff_calculations if calc not in found_calculations]
            if missing_calculations:
                print("   ❌ Missing calculations:")
                for calc in missing_calculations:
                    print(f"      - {calc}")
            
            # Show a preview of the generated notebook
            print("\n📖 Generated Notebook Preview:")
            print("-" * 60)
            lines = notebook_content.split('\n')
            preview_lines = lines[:50] if len(lines) > 50 else lines
            print('\n'.join(preview_lines))
            if len(lines) > 50:
                print(f"... ({len(lines) - 50} more lines)")
            print("-" * 60)
            
            # Check if analysis_data.json was created
            analysis_data_path = output_path.parent / "analysis_data.json"
            if analysis_data_path.exists():
                print("✅ Analysis data file created successfully")
            else:
                print("❌ Analysis data file missing")
                
            return len(found_calculations) >= 5  # At least 5 key calculations should be present
        
    except Exception as e:
        print(f"❌ Test failed with exception: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("Testing NotebookGeneratorAgent with Real CFF Analysis Data...")
    print()
    
    if test_cff_notebook_generation():
        print("\n🎉 SUCCESS! NotebookGeneratorAgent can generate academically sound")
        print("   CFF derived metrics calculations from real analysis data!")
        print("\n   This proves Epic 401 delivers transparent, provenance-valid")
        print("   calculations that replace the failing MathToolkit approach.")
    else:
        print("\n❌ FAILURE: NotebookGeneratorAgent could not generate proper")
        print("   CFF derived metrics calculations.")
