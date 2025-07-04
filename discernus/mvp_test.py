#!/usr/bin/env python3
"""
MVP Infrastructure Test
======================

Test the ultra-thin infrastructure components.
"""

import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from discernus.core.session_manager import SessionManager
from discernus.core.message_router import MessageRouter
from discernus.core.thin_conversation_logger import ThinConversationLogger
from discernus.core.llm_roles import get_available_roles

def test_infrastructure():
    """Test the ultra-thin infrastructure components"""
    print("🧪 Testing Ultra-Thin Infrastructure")
    print("=" * 40)
    
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
    
    # Test LLM Roles
    print("\n3. Testing LLM Roles...")
    roles = get_available_roles()
    print(f"   ✅ Available roles: {roles}")
    
    # Test Message Router (without actual LLM calls)
    print("\n4. Testing Message Router...")
    router = MessageRouter()
    print(f"   ✅ Message router initialized")
    print(f"   ✅ Configured LLM roles: {list(router.llm_roles.keys())}")
    
    print("\n🎉 All components initialized successfully!")
    print("\n📊 Line Count Analysis:")
    
    # Count lines in each file
    files = [
        'discernus/core/session_manager.py',
        'discernus/core/thin_conversation_logger.py', 
        'discernus/core/message_router.py',
        'discernus/core/simple_code_executor.py'
    ]
    
    total_lines = 0
    for file_path in files:
        if Path(file_path).exists():
            lines = len(Path(file_path).read_text().splitlines())
            total_lines += lines
            budget = {'session_manager': 20, 'thin_conversation_logger': 30, 'message_router': 50, 'simple_code_executor': 40}
            file_name = Path(file_path).stem
            budget_status = "✅" if lines <= budget.get(file_name, 100) else "❌"
            print(f"   {budget_status} {file_name}: {lines} lines (budget: {budget.get(file_name, 'N/A')})")
    
    print(f"\n📈 Total Infrastructure: {total_lines} lines (budget: ~140 lines)")
    print(f"   {'✅ THIN' if total_lines <= 200 else '❌ TOO THICK'}")
    
    return session_id

if __name__ == "__main__":
    test_infrastructure() 