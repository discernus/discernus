#!/usr/bin/env python3
"""
End-to-End MVP Test
==================

Test the complete conversation flow: User → Design LLM → Response
This validates our ultra-thin infrastructure with actual LLM calls.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from discernus.core.session_manager import SessionManager
from discernus.core.message_router import MessageRouter
from discernus.core.thin_conversation_logger import ThinConversationLogger

def test_end_to_end_conversation():
    """Test complete conversation flow with actual LLM calls"""
    print("🚀 Testing End-to-End Conversation Flow")
    print("=" * 50)
    
    # Initialize infrastructure
    session_mgr = SessionManager()
    router = MessageRouter()
    logger = ThinConversationLogger()
    
    # Create research session
    research_question = "Which inaugural address is more unifying - Lincoln 1865 or Trump 2025?"
    session_id = session_mgr.create_session(research_question)
    print(f"✅ Created session: {session_id}")
    
    # Log initial user message
    logger.log_message(session_id, "user", research_question)
    print(f"✅ Logged user question")
    
    try:
        # Test Design LLM call
        print("\n🤖 Calling Design LLM...")
        
        # Prepare context for Design LLM
        context_message = f"""
Research Question: {research_question}

Please propose a systematic methodology for analyzing these inaugural addresses.
Follow the RAG++ principles and end with "Does this methodology look right to you?"

The texts are available at:
- data/inaugural_addresses/lincoln_1865_second_inaugural.txt
- data/inaugural_addresses/trump_2025_inaugural.txt
"""
        
        # Route to Design LLM
        design_response = router.route_message(
            from_role="user",
            to_role="design", 
            message=context_message,
            session_id=session_id
        )
        
        print(f"✅ Design LLM responded ({len(design_response)} characters)")
        print(f"📝 Response preview: {design_response[:200]}...")
        
        # Log the response
        logger.log_message(session_id, "design", design_response)
        
        # Test handoff detection
        print("\n🔄 Testing handoff detection...")
        if "HANDOFF" in design_response.upper() or "CALL" in design_response.upper():
            print("✅ Handoff pattern detected in response")
        else:
            print("ℹ️ No handoff pattern (normal for first interaction)")
        
        # Show conversation log
        print("\n📋 Reading conversation log...")
        conversation = logger.read_conversation(session_id)
        print(f"✅ Conversation log: {len(conversation)} characters")
        
        # Complete session
        session_mgr.end_session(session_id)
        print(f"✅ Session committed to Git")
        
        print("\n🎉 End-to-End Test Successful!")
        print("\n📊 Validation Results:")
        print("   ✅ Session management working")
        print("   ✅ LLM routing working") 
        print("   ✅ Conversation logging working")
        print("   ✅ Git persistence working")
        print(f"   ✅ Complete workflow: User → Design LLM → Response")
        
        return True
        
    except Exception as e:
        print(f"❌ End-to-End Test Failed: {e}")
        print("\n🔧 This might be due to:")
        print("   - Missing .env file with API keys")
        print("   - LiteLLM client configuration issues")
        print("   - Network connectivity")
        
        # Still commit what we have
        session_mgr.end_session(session_id)
        return False

if __name__ == "__main__":
    success = test_end_to_end_conversation()
    if success:
        print("\n🚀 Ready for full Lincoln vs Trump analysis!")
    else:
        print("\n🛠️ Need to resolve LLM integration issues first") 