#!/usr/bin/env python3
"""
Test script to check if narrative agents are working and identify placeholder issues.
"""

import sys
from pathlib import Path

# Add the project root to the path
sys.path.insert(0, str(Path(__file__).parent))

def test_narrative_agents():
    """Test the narrative agents to see if they're working."""
    
    print("🔬 Testing narrative agents...")
    
    try:
        # Test NotebookMethodologyAgent
        from discernus.agents.notebook_methodology_agent import NotebookMethodologyAgent
        from discernus.core.audit_logger import AuditLogger
        from discernus.core.security_boundary import ExperimentSecurityBoundary
        
        # Create test environment
        test_path = Path("/Volumes/code/discernus-epic-401/projects/simple_test")
        security = ExperimentSecurityBoundary(test_path)
        audit_logger = AuditLogger(security, test_path / "test_logs")
        
        # Initialize agent
        methodology_agent = NotebookMethodologyAgent(
            model="vertex_ai/gemini-2.5-flash",
            audit_logger=audit_logger
        )
        
        print("✅ NotebookMethodologyAgent initialized")
        
        # Test generation
        framework_content = """
        # Cohesive Flourishing Framework v8.0
        
        ## Research Purpose
        Analyze political discourse for cohesive vs. fragmentative patterns.
        
        ## Dimensions
        - **tribal_dominance_score**: Measures group-based power dynamics
        - **individual_dignity_score**: Measures respect for individual worth
        - **hope_score**: Measures optimistic future orientation
        - **fear_score**: Measures threat perception and anxiety
        """
        
        methodology = methodology_agent.generate_methodology(
            framework_content=framework_content,
            experiment_name="test_experiment",
            framework_name="cohesive_flourishing_framework",
            document_count=4,
            analysis_model="vertex_ai/gemini-2.5-flash"
        )
        
        print(f"✅ Methodology generated: {len(methodology)} characters")
        print(f"📝 Preview: {methodology[:200]}...")
        
        # Check for placeholders
        if "placeholder" in methodology.lower() or "insert" in methodology.lower():
            print("❌ WARNING: Placeholder content detected in methodology!")
        else:
            print("✅ No placeholder content detected")
            
    except Exception as e:
        print(f"❌ Error testing methodology agent: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        # Test NotebookInterpretationAgent
        from discernus.agents.notebook_interpretation_agent import NotebookInterpretationAgent
        
        interpretation_agent = NotebookInterpretationAgent(
            model="vertex_ai/gemini-2.5-flash",
            audit_logger=audit_logger
        )
        
        print("✅ NotebookInterpretationAgent initialized")
        
        # Test generation
        interpretation = interpretation_agent.generate_interpretation(
            framework_name="cohesive_flourishing_framework",
            experiment_name="test_experiment",
            document_count=4,
            statistical_summary="ANOVA F=15.2, p<0.001 for tribal dominance",
            key_findings="High tribal dominance scores across all documents"
        )
        
        print(f"✅ Interpretation generated: {len(interpretation)} characters")
        print(f"📝 Preview: {interpretation[:200]}...")
        
        # Check for placeholders
        if "placeholder" in interpretation.lower() or "insert" in interpretation.lower():
            print("❌ WARNING: Placeholder content detected in interpretation!")
        else:
            print("✅ No placeholder content detected")
            
    except Exception as e:
        print(f"❌ Error testing interpretation agent: {e}")
        import traceback
        traceback.print_exc()
    
    try:
        # Test NotebookDiscussionAgent
        from discernus.agents.notebook_discussion_agent import NotebookDiscussionAgent
        
        discussion_agent = NotebookDiscussionAgent(
            model="vertex_ai/gemini-2.5-flash",
            audit_logger=audit_logger
        )
        
        print("✅ NotebookDiscussionAgent initialized")
        
        # Test generation
        discussion = discussion_agent.generate_discussion(
            framework_name="cohesive_flourishing_framework",
            experiment_name="test_experiment",
            document_count=4,
            key_interpretations="High tribal dominance suggests political polarization",
            research_context="Computational analysis of political discourse"
        )
        
        print(f"✅ Discussion generated: {len(discussion)} characters")
        print(f"📝 Preview: {discussion[:200]}...")
        
        # Check for placeholders
        if "placeholder" in discussion.lower() or "insert" in discussion.lower():
            print("❌ WARNING: Placeholder content detected in discussion!")
        else:
            print("✅ No placeholder content detected")
            
    except Exception as e:
        print(f"❌ Error testing discussion agent: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n🎯 Narrative agents test complete!")

if __name__ == "__main__":
    test_narrative_agents()
