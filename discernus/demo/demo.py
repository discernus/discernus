#!/usr/bin/env python3
"""
Discernus Demonstration Script
==============================

Demonstrates the Discernus (Conversational Academic Research Architecture) approach
with multi-LLM conversation, secure code execution, and complete transparency.

This script showcases the core Discernus principles:
1. Conversation-Native Processing (no parsing)
2. Strategic Thinness (minimal custom code)
3. Complete Transparency (Git logging)
4. Secure Code Execution (Docker sandboxing)
5. Academic Rigor (code review workflow)
"""

import asyncio
import sys
import logging
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.orchestration.orchestrator import DiscernusOrchestrator, ConversationConfig

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


async def main():
    """
    Main demo function showing Discernus capabilities
    """
    print("🚀 Discernus Demonstration")
    print("=" * 50)
    
    # Sample political speech for analysis
    sample_speech = """
    The corrupt politicians in Washington have betrayed the hardworking Americans who built this country. 
    While the establishment gets rich, ordinary families struggle to pay their bills. 
    We need to drain the swamp and return power to the people. 
    The elite media won't tell you this, but we're going to fight for every forgotten American.
    """
    
    # Initialize Discernus orchestrator
    orchestrator = DiscernusOrchestrator(project_root=str(project_root))
    
    # Configure conversation
    config = ConversationConfig(
        research_question="Is this speech populist or pluralist in nature?",
        participants=["populist_expert", "pluralist_expert"],
        speech_text=sample_speech,
        models={
            "populist_expert": "claude-3-5-sonnet",
            "pluralist_expert": "claude-3-5-sonnet"
        },
        max_turns=3,
        enable_code_execution=True,
        code_review_model="claude-3-5-sonnet"
    )
    
    print(f"Research Question: {config.research_question}")
    print(f"Participants: {config.participants}")
    print(f"Code Execution: {'Enabled' if config.enable_code_execution else 'Disabled'}")
    print()
    
    try:
        # Start conversation
        print("🎯 Starting multi-LLM conversation...")
        conversation_id = await orchestrator.start_conversation(config)
        print(f"Conversation ID: {conversation_id}")
        
        # Run conversation
        print("💬 Running conversation...")
        results = await orchestrator.run_conversation(conversation_id)
        
        print()
        print("✅ Conversation completed!")
        print(f"Turns completed: {results['turns_completed']}")
        print(f"Summary: {results['summary']}")
        
        # Show conversation history
        print("\n📋 Conversation History:")
        print("-" * 30)
        
        conversation_history = orchestrator.conversation_logger.read_conversation(conversation_id)
        for i, message in enumerate(conversation_history[-10:]):  # Show last 10 messages
            timestamp = message['timestamp'][:19]  # Truncate timestamp
            speaker = message['speaker']
            content = message['message'][:100] + "..." if len(message['message']) > 100 else message['message']
            
            print(f"{i+1}. [{timestamp}] {speaker}:")
            print(f"   {content}")
            print()
        
        # Show conversation list
        print("\n📚 All Conversations:")
        print("-" * 30)
        all_conversations = orchestrator.list_conversations()
        for i, conv in enumerate(all_conversations[:5]):  # Show first 5
            print(f"{i+1}. {conv['conversation_id']}")
            print(f"   Started: {conv['started_at'][:19]}")
            print(f"   Messages: {conv['message_count']}")
            print(f"   Status: {conv['status']}")
            print()
        
        print("🎉 Demo completed successfully!")
        print("\nKey Discernus Features Demonstrated:")
        print("✅ Conversation-Native Processing (no parsing)")
        print("✅ Multi-LLM Coordination")
        print("✅ Secure Code Execution")
        print("✅ Complete Git Transparency")
        print("✅ Academic Code Review")
        print("✅ Resource Management")
        
    except Exception as e:
        logger.error(f"Demo failed: {e}")
        print(f"❌ Demo failed: {e}")
        return 1
    
    return 0


async def quick_test():
    """
    Quick test without full conversation for debugging
    """
    print("🔧 Quick Discernus Test")
    print("=" * 30)
    
    # Initialize components
    orchestrator = DiscernusOrchestrator(project_root=str(project_root))
    
    # Test conversation logger
    print("Testing conversation logger...")
    conversation_id = orchestrator.conversation_logger.start_conversation(
        speech_text="Test speech",
        research_question="Test question",
        participants=["test_expert"]
    )
    
    orchestrator.conversation_logger.log_llm_message(
        conversation_id, "test_expert", "Test message"
    )
    
    orchestrator.conversation_logger.end_conversation(conversation_id, "Test complete")
    
    # Test code executor
    print("Testing code executor...")
    test_code_response = """
I need to test the code execution:

```python
import math
print(f"Square root of 16: {math.sqrt(16)}")
print("Code execution test successful!")
```

This should work fine.
"""
    
    from discernus.core.simple_code_executor import process_llm_notebook_request
    
    enhanced_response = process_llm_notebook_request(
        conversation_id, "test_expert", test_code_response
    )
    
    print(f"Enhanced response includes code results: {enhanced_response != test_code_response}")
    if enhanced_response != test_code_response:
        print("Code execution working!")
    else:
        print("No code executed")
    
    print("✅ Quick test completed!")
    return 0


def cli_main():
    """
    CLI entry point for pyproject.toml scripts
    """
    # Check if quick test requested
    if len(sys.argv) > 1 and sys.argv[1] == "--quick":
        exit_code = asyncio.run(quick_test())
    else:
        exit_code = asyncio.run(main())
    
    sys.exit(exit_code)


if __name__ == "__main__":
    cli_main() 