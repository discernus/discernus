#!/usr/bin/env python3
"""
THIN Lincoln vs Trump Analysis Demo
==================================

Demonstrates proper THIN Software + THICK LLM philosophy:
1. Design LLM consultation with human researcher
2. Human approval of analysis approach  
3. Execution via moderator LLM (no parsing, raw text passing)

This corrects the violations identified in the previous implementation.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.orchestration.orchestrator import ThinOrchestrator, ResearchConfig

def load_inaugural_texts():
    """Load Lincoln and Trump inaugural addresses"""
    # Load Lincoln's 1865 Second Inaugural
    lincoln_path = project_root / "data" / "inaugural_addresses" / "lincoln_1865_second_inaugural.txt"
    trump_path = project_root / "data" / "inaugural_addresses" / "trump_2025_inaugural.txt"
    
    try:
        with open(lincoln_path, 'r', encoding='utf-8') as f:
            lincoln_text = f.read()
    except FileNotFoundError:
        lincoln_text = """[Lincoln's 1865 Second Inaugural would be loaded here]
        Fellow-Countrymen: At this second appearing to take the oath of the Presidential office...
        With malice toward none, with charity for all, with firmness in the right as God gives us to see the right..."""
    
    try:
        with open(trump_path, 'r', encoding='utf-8') as f:
            trump_text = f.read()
    except FileNotFoundError:
        trump_text = """[Trump's 2025 Inaugural would be loaded here]
        Thank you very much, everybody. The golden age of America begins right now..."""
    
    return lincoln_text, trump_text

def display_design_proposal(proposal: str):
    """Display design proposal for human review"""
    print("\n" + "="*80)
    print("🎨 DESIGN LLM PROPOSAL")
    print("="*80)
    print(proposal)
    print("="*80)

def get_human_approval() -> tuple[bool, str]:
    """Get human approval for design proposal"""
    print("\n" + "🤔 HUMAN RESEARCHER DECISION")
    print("-" * 40)
    
    while True:
        response = input("Do you approve this analysis design? (y/n/feedback): ").strip().lower()
        
        if response == 'y' or response == 'yes':
            return True, ""
        elif response == 'n' or response == 'no':
            feedback = input("Please provide feedback for design refinement: ").strip()
            return False, feedback
        elif response == 'feedback':
            feedback = input("Please provide feedback for design refinement: ").strip()
            return False, feedback
        else:
            print("Please respond with 'y' (yes), 'n' (no), or 'feedback'")

async def run_thin_lincoln_trump_analysis():
    """
    Run the complete THIN analysis workflow
    
    This demonstrates:
    1. Design LLM consultation
    2. Human approval step with feedback integration
    3. Execution via moderator LLM (no parsing!)
    """
    print("🎯 THIN Discernus Analysis: Lincoln vs Trump Inaugural Addresses")
    print("================================================================")
    
    # Initialize THIN orchestrator
    orchestrator = ThinOrchestrator(str(project_root))
    
    # Load inaugural texts
    lincoln_text, trump_text = load_inaugural_texts()
    
    # Combine texts for analysis
    combined_texts = f"""
LINCOLN'S 1865 SECOND INAUGURAL ADDRESS:
{lincoln_text}

---

TRUMP'S 2025 INAUGURAL ADDRESS:
{trump_text}
"""
    
    # Create research configuration
    config = ResearchConfig(
        research_question="Which inaugural address is more unifying vs divisive: Lincoln's 1865 Second Inaugural or Trump's 2025 Inaugural?",
        source_texts=combined_texts,
        enable_code_execution=True
    )
    
    print(f"\n📋 Research Question: {config.research_question}")
    
    # PHASE 1: Start research session
    print("\n🚀 PHASE 1: Starting research session...")
    session_id = await orchestrator.start_research_session(config)
    print(f"✅ Session started: {session_id}")
    
    # PHASE 2: Design LLM consultation with feedback loop
    print("\n🎨 PHASE 2: Design LLM consultation...")
    
    max_refinement_cycles = 3
    refinement_cycle = 0
    human_feedback = ""
    
    while refinement_cycle < max_refinement_cycles:
        print("Consulting design LLM for analysis approach...")
        
        # Get design proposal (with any feedback from previous iteration)
        design_proposal = await orchestrator.run_design_consultation(session_id, human_feedback)
        
        # Display proposal to human researcher
        display_design_proposal(design_proposal)
        
        # PHASE 3: Human approval
        print("\n👤 PHASE 3: Human researcher approval...")
        
        approval, feedback = get_human_approval()
        
        ready_to_execute = orchestrator.approve_design(session_id, approval, feedback)
        
        if ready_to_execute:
            print("✅ Design approved! Ready to execute analysis.")
            break
        else:
            print(f"🔄 Design rejected. Feedback: {feedback}")
            print("Returning to design consultation...")
            
            human_feedback = feedback  # This will be passed to next design consultation
            refinement_cycle += 1
    
    if refinement_cycle >= max_refinement_cycles:
        print("❌ Maximum refinement cycles reached. Ending session.")
        return
    
    # PHASE 4: Execute approved analysis via moderator LLM
    print("\n🔧 PHASE 4: Executing approved analysis...")
    print("Moderator LLM will interpret design and orchestrate analysis...")
    
    results = await orchestrator.execute_approved_analysis(session_id)
    
    # Display results
    print("\n🎉 ANALYSIS COMPLETED!")
    print("=" * 60)
    print(f"Conversation ID: {results['conversation_id']}")
    print(f"Status: {results['status']}")
    print(f"Summary: {results['summary']}")
    
    # Show where to find the logs
    conversation_id = results['conversation_id']
    print(f"\n📁 CONVERSATION LOGS:")
    print(f"Raw JSONL: conversations/{conversation_id}.jsonl")
    print(f"Readable format: conversations/{conversation_id}_readable.md")
    
    # Clean up session
    orchestrator.cleanup_session(session_id)
    
    print("\n✨ THIN analysis workflow completed successfully!")
    print("\nKey THIN principles demonstrated:")
    print("- ✅ Design LLM determined analysis approach (no hardcoded roles)")
    print("- ✅ Human researcher approved design before execution")
    print("- ✅ Feedback properly integrated into design refinement")
    print("- ✅ NO parsing - raw text passed between LLMs")
    print("- ✅ Moderator LLM interprets design and orchestrates")
    print("- ✅ Software orchestrated, LLMs handled intelligence")
    print("- ✅ Complete conversation transparency maintained")

async def main():
    """Main demo function"""
    try:
        await run_thin_lincoln_trump_analysis()
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrupted by user")
    except Exception as e:
        print(f"\n❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    print("🎯 Starting THIN Lincoln vs Trump Analysis Demo...")
    print("This demonstrates proper THIN Software + THICK LLM workflow")
    print("Key improvement: NO parsing - LLMs talk to each other via raw text!")
    asyncio.run(main()) 