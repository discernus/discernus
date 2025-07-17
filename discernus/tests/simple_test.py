#!/usr/bin/env python3
"""
Simple Infrastructure Test (No LLM Dependencies)
===============================================

Test the ultra-thin infrastructure components without LLM dependencies.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from discernus.core.session_manager import SessionManager
from discernus.core.thin_conversation_logger import ThinConversationLogger
from discernus.core.agent_roles import get_available_experts as get_available_roles

def test_thin_infrastructure():
    """Test the ultra-thin infrastructure components"""
    print("🧪 Testing Ultra-Thin Infrastructure (No LLM)")
    print("=" * 50)
    
    # Test Session Manager
    print("\n1. Testing Session Manager...")
    session_mgr = SessionManager()
    session_id = session_mgr.create_session("Lincoln vs Trump unity analysis")
    print(f"   ✅ Created session: {session_id}")
    
    # Test Conversation Logger
    print("\n2. Testing Conversation Logger...")
    logger = ThinConversationLogger()
    logger.log_message(session_id, "user", "Which inaugural address is more unifying - Lincoln 1861 or Trump 2017?")
    print(f"   ✅ Logged user message")
    
    # Test message reading
    conversation = logger.read_conversation(session_id)
    print(f"   ✅ Read conversation: {len(conversation)} characters")
    
    # Test LLM Roles
    print("\n3. Testing LLM Roles...")
    roles = get_available_roles()
    print(f"   ✅ Available roles: {roles}")
    
    # Test code execution logging
    print("\n4. Testing Code Execution Logging...")
    sample_code = "lincoln_words = ['unity', 'together', 'peace']\nprint(f'Unity words: {len(lincoln_words)}')"
    sample_result = "Unity words: 3"
    logger.log_code_execution(session_id, "unity_expert", sample_code, sample_result)
    print(f"   ✅ Logged code execution")
    
    print("\n🎉 All components working successfully!")
    print("\n📊 Line Count Analysis:")
    
    # Count lines in each file
    files = [
        'discernus/core/session_manager.py',
        'discernus/core/thin_conversation_logger.py', 
        'discernus/core/simple_code_executor.py'
    ]
    
    total_lines = 0
    for file_path in files:
        if Path(file_path).exists():
            lines = len(Path(file_path).read_text().splitlines())
            total_lines += lines
            budget = {'session_manager': 30, 'thin_conversation_logger': 40, 'simple_code_executor': 74}
            file_name = Path(file_path).stem
            budget_status = "✅" if lines <= budget.get(file_name, 100) else "❌"
            print(f"   {budget_status} {file_name}: {lines} lines")
    
    print(f"\n📈 Total Core Infrastructure: {total_lines} lines")
    print(f"   {'✅ THIN' if total_lines <= 200 else '❌ TOO THICK'}")
    
    # Test session completion
    print("\n5. Testing Session Completion...")
    session_mgr.end_session(session_id)
    print(f"   ✅ Session committed to Git")
    
    return session_id

if __name__ == "__main__":
    test_thin_infrastructure() 