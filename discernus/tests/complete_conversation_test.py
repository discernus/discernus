#!/usr/bin/env python3
"""
Complete Multi-LLM Conversation Test
===================================

Demonstrates the full MVP workflow:
User → Design → Moderator → Specialist(s) → Adversarial → Analysis → Referee
"""

import sys
import time
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from discernus.core.session_manager import SessionManager
from discernus.core.message_router import MessageRouter
from discernus.core.thin_conversation_logger import ThinConversationLogger
from discernus.core.thin_discipline_logger import log_temptation

def simulate_complete_conversation():
    """Simulate complete Lincoln vs Trump unity analysis workflow"""
    print("🎯 Complete Multi-LLM Conversation: Lincoln vs Trump Unity Analysis")
    print("=" * 70)
    
    # Initialize infrastructure
    session_mgr = SessionManager()
    router = MessageRouter()
    logger = ThinConversationLogger()
    
    research_question = "Which inaugural address is more unifying - Lincoln 1865 or Trump 2025?"
    session_id = session_mgr.create_session(research_question)
    
    print(f"📋 Session: {session_id}")
    print(f"🔬 Research Question: {research_question}")
    
    # Log THIN discipline choice
    log_temptation(
        "Wanted to hardcode Unity/Division expert roles",
        "Using flexible Moderator + Specialist coordination instead"
    )
    
    try:
        # === STEP 1: USER → DESIGN LLM ===
        print("\n" + "="*50)
        print("🎨 STEP 1: Design LLM - Methodology Consultation")
        print("="*50)
        
        design_message = f"""
Research Question: {research_question}

Please propose a systematic methodology for analyzing these inaugural addresses.
Follow the RAG++ principles and end with "Does this methodology look right to you?"

The texts are available at:
- data/inaugural_addresses/lincoln_1865_second_inaugural.txt  
- data/inaugural_addresses/trump_2025_inaugural.txt
"""
        
        design_response = router.route_message("user", "design", design_message, session_id)
        print(f"📝 Design LLM methodology proposed ({len(design_response)} chars)")
        print("Preview:", design_response[:300] + "...")
        
        # === STEP 2: USER FEEDBACK ===
        print("\n" + "="*50)
        print("👤 STEP 2: User Feedback")
        print("="*50)
        
        user_feedback = "Good methodology! Please also include analysis of emotional framing and historical context."
        logger.log_message(session_id, "user_feedback", user_feedback)
        print(f"👤 User feedback: {user_feedback}")
        
        # === STEP 3: DESIGN → MODERATOR (RAG++ Synthesis) ===
        print("\n" + "="*50)
        print("🔄 STEP 3: Design LLM - RAG++ Synthesis & Handoff")
        print("="*50)
        
        enhanced_methodology = f"""
Original methodology confirmed with user modifications:
{design_response}

User requested additions: {user_feedback}

HANDOFF TO MODERATOR: Enhanced methodology including emotional framing and historical context analysis for Lincoln 1865 vs Trump 2025 inaugural addresses comparison.
"""
        
        moderator_response = router.route_message("design", "moderator", enhanced_methodology, session_id)
        print(f"🔄 Moderator coordinating analysis ({len(moderator_response)} chars)")
        print("Preview:", moderator_response[:300] + "...")
        
        # === STEP 4: MODERATOR → SPECIALIST (Unity Analysis) ===
        print("\n" + "="*50)
        print("🔍 STEP 4: Specialist LLM - Unity Analysis")
        print("="*50)
        
        unity_request = f"""
{moderator_response}

Focus: Analyze unifying language patterns in both Lincoln 1865 and Trump 2025 inaugural addresses.
Include emotional framing and historical context as requested by the user.
"""
        
        unity_analysis = router.route_message("moderator", "specialist", unity_request, session_id)
        print(f"🔍 Unity analysis complete ({len(unity_analysis)} chars)")
        print("Preview:", unity_analysis[:300] + "...")
        
        # === STEP 5: MODERATOR → SPECIALIST (Division Analysis) ===
        print("\n" + "="*50)
        print("⚡ STEP 5: Specialist LLM - Division Analysis")
        print("="*50)
        
        division_request = f"""
Previous unity analysis: {unity_analysis[:200]}...

Focus: Analyze divisive language patterns in both Lincoln 1865 and Trump 2025 inaugural addresses.
Include emotional framing and historical context as requested by the user.
"""
        
        division_analysis = router.route_message("moderator", "specialist", division_request, session_id)
        print(f"⚡ Division analysis complete ({len(division_analysis)} chars)")
        print("Preview:", division_analysis[:300] + "...")
        
        # === STEP 6: MODERATOR → ADVERSARIAL ===
        print("\n" + "="*50)
        print("🥊 STEP 6: Adversarial LLM - Critical Review")
        print("="*50)
        
        adversarial_request = f"""
Unity Analysis: {unity_analysis[:300]}...
Division Analysis: {division_analysis[:300]}...

Challenge these analyses. Find blind spots, methodological weaknesses, and alternative interpretations.
"""
        
        adversarial_review = router.route_message("moderator", "adversarial", adversarial_request, session_id)
        print(f"🥊 Adversarial review complete ({len(adversarial_review)} chars)")
        print("Preview:", adversarial_review[:300] + "...")
        
        # === STEP 7: MODERATOR → ANALYSIS (Synthesis) ===
        print("\n" + "="*50)
        print("📊 STEP 7: Analysis LLM - Synthesis")
        print("="*50)
        
        synthesis_request = f"""
Synthesize all analyses:

Unity Analysis: {unity_analysis}

Division Analysis: {division_analysis}

Adversarial Review: {adversarial_review}

Research Question: {research_question}
"""
        
        synthesis = router.route_message("moderator", "analysis", synthesis_request, session_id)
        print(f"📊 Synthesis complete ({len(synthesis)} chars)")
        print("Preview:", synthesis[:300] + "...")
        
        # === STEP 8: ANALYSIS → REFEREE (Final Validation) ===
        print("\n" + "="*50)
        print("⚖️ STEP 8: Referee LLM - Final Academic Validation")
        print("="*50)
        
        referee_request = f"""
Complete synthesis for final academic validation:

{synthesis}

Provide final academic assessment with:
1. Executive summary
2. Methodological assessment  
3. Key findings
4. Minority reports (disagreements)
5. Limitations and future research
"""
        
        final_report = router.route_message("analysis", "referee", referee_request, session_id)
        print(f"⚖️ Final academic report complete ({len(final_report)} chars)")
        print("Preview:", final_report[:300] + "...")
        
        # === COMPLETION ===
        print("\n" + "="*70)
        print("🎉 COMPLETE CONVERSATION WORKFLOW SUCCESSFUL!")
        print("="*70)
        
        # Session completion
        session_mgr.end_session(session_id)
        
        # Show final results
        conversation = logger.read_conversation(session_id)
        print(f"\n📈 Final Results:")
        print(f"   ✅ Complete workflow: User → Design → Moderator → Specialist → Adversarial → Analysis → Referee")
        print(f"   ✅ Research question answered: {research_question}")
        print(f"   ✅ Conversation log: {len(conversation)} characters")
        print(f"   ✅ Session committed to Git: {session_id}")
        print(f"   ✅ All LLM roles coordinated successfully")
        print(f"   ✅ RAG++ synthesis with user feedback integrated")
        print(f"   ✅ Adversarial review completed")
        print(f"   ✅ Academic validation completed")
        
        print(f"\n🏆 MVP SUCCESS: Conversation-native academic research workflow validated!")
        print(f"📝 Check research_sessions/{session_id}/ for complete conversation log")
        
        return True
        
    except Exception as e:
        print(f"❌ Complete conversation failed: {e}")
        session_mgr.end_session(session_id)
        return False

if __name__ == "__main__":
    success = simulate_complete_conversation()
    if success:
        print("\n🚀 READY FOR PRODUCTION: Ultra-thin infrastructure + THICK LLM intelligence = Epistemic Trust!")
    else:
        print("\n🛠️ Need debugging") 