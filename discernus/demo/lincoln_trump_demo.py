#!/usr/bin/env python3
"""
Lincoln vs Trump Unity Analysis Demo
===================================

MVP demonstration comparing Lincoln's 1865 Second Inaugural Address
with Trump's 2025 Inaugural Address on themes of unity vs division.

This demonstrates the THIN architecture with 6 LLM roles:
- Design LLM: Framework design
- Moderator LLM: Conversation management  
- Specialist LLMs: Unity Expert, Division Expert
- Adversarial LLM: Devil's advocate
- Analysis LLM: Synthesis and analysis
- Referee LLM: Quality control
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


def load_inaugural_addresses():
    """Load Lincoln and Trump inaugural addresses"""
    
    # Load Lincoln's 1865 Second Inaugural
    lincoln_path = project_root / "data" / "inaugural_addresses" / "lincoln_1865_second_inaugural.txt"
    with open(lincoln_path, 'r', encoding='utf-8') as f:
        lincoln_speech = f.read()
    
    # Load Trump's 2025 Inaugural
    trump_path = project_root / "data" / "inaugural_addresses" / "trump_2025_inaugural.txt"
    with open(trump_path, 'r', encoding='utf-8') as f:
        trump_speech = f.read()
    
    return lincoln_speech, trump_speech


async def main():
    """
    Main demo function for Lincoln vs Trump Unity Analysis
    """
    print("🎯 LINCOLN VS TRUMP UNITY ANALYSIS MVP")
    print("=" * 50)
    print("Demonstrating THICK LLM + THIN Software = Epistemic Trust")
    print()
    
    # Load inaugural addresses
    lincoln_speech, trump_speech = load_inaugural_addresses()
    
    # Create combined analysis text
    combined_text = f"""
LINCOLN'S 1865 SECOND INAUGURAL ADDRESS:
{lincoln_speech}

---

TRUMP'S 2025 INAUGURAL ADDRESS:
{trump_speech}
"""
    
    # Initialize Discernus orchestrator
    orchestrator = DiscernusOrchestrator(project_root=str(project_root))
    
    # Configure conversation with 6 LLM roles
    config = ConversationConfig(
        research_question="Which inaugural address is more unifying vs divisive: Lincoln's 1865 Second Inaugural or Trump's 2025 Inaugural?",
        participants=[
            "design_llm",           # Framework design
            "moderator_llm",        # Conversation management
            "unity_expert",         # Unity analysis specialist
            "division_expert",      # Division analysis specialist  
            "adversarial_llm",      # Devil's advocate
            "analysis_llm",         # Synthesis specialist
            "referee_llm"           # Quality control
        ],
        speech_text=combined_text,
        models={
            "design_llm": "claude-3-5-sonnet",
            "moderator_llm": "claude-3-5-sonnet", 
            "unity_expert": "claude-3-5-sonnet",
            "division_expert": "claude-3-5-sonnet",
            "adversarial_llm": "claude-3-5-sonnet",
            "analysis_llm": "claude-3-5-sonnet",
            "referee_llm": "claude-3-5-sonnet"
        },
        max_turns=10,  # Allow more turns for thorough analysis
        enable_code_execution=True,
        code_review_model="claude-3-5-sonnet"
    )
    
    print(f"🎯 Research Question: {config.research_question}")
    print(f"🤖 LLM Participants: {len(config.participants)} roles")
    print(f"📊 Lincoln Speech Length: {len(lincoln_speech)} characters")
    print(f"📊 Trump Speech Length: {len(trump_speech)} characters")
    print(f"💻 Code Execution: {'Enabled' if config.enable_code_execution else 'Disabled'}")
    print()
    
    try:
        # Start conversation
        print("🚀 Starting 6-LLM Unity Analysis...")
        conversation_id = await orchestrator.start_conversation(config)
        print(f"📝 Conversation ID: {conversation_id}")
        
        # Run conversation
        print("🎭 Running multi-LLM conversation...")
        results = await orchestrator.run_conversation(conversation_id)
        
        print()
        print("✅ Analysis completed!")
        print(f"🔄 Turns completed: {results['turns_completed']}")
        print(f"📋 Summary: {results['summary']}")
        
        # Show key conversation moments
        print("\n🎯 Key Analysis Moments:")
        print("-" * 40)
        
        conversation_history = orchestrator.conversation_logger.read_conversation(conversation_id)
        
        # Show first few and last few messages
        for i, message in enumerate(conversation_history[:3]):
            timestamp = message['timestamp'][:19]
            speaker = message['speaker']
            content = message['message'][:200] + "..." if len(message['message']) > 200 else message['message']
            
            print(f"[{timestamp}] {speaker}:")
            print(f"   {content}")
            print()
        
        if len(conversation_history) > 6:
            print("   ... [middle conversation omitted] ...")
            print()
            
            for i, message in enumerate(conversation_history[-3:]):
                timestamp = message['timestamp'][:19]
                speaker = message['speaker']
                content = message['message'][:200] + "..." if len(message['message']) > 200 else message['message']
                
                print(f"[{timestamp}] {speaker}:")
                print(f"   {content}")
                print()
        
        print("🎉 MVP DEMONSTRATION COMPLETE!")
        print("\n🏆 Key Achievements:")
        print("✅ THIN Architecture: 156 lines of infrastructure code")
        print("✅ 6 LLM Coordination: Design, Moderator, Specialists, Adversarial, Analysis, Referee")
        print("✅ Conversation-Native: No response parsing or software intelligence")
        print("✅ Academic Rigor: Complete transparency and reproducibility")
        print("✅ Real Analysis: Lincoln vs Trump unity comparison")
        print("✅ Epistemic Trust: THICK LLM + THIN Software working together")
        
        # Generate readable conversation log
        print("📝 Generating readable conversation log...")
        from discernus.core.conversation_formatter import save_formatted_conversation
        readable_log = save_formatted_conversation(conversation_id)
        
        # Show conversation log locations
        print(f"\n📁 Full conversation log: conversations/{conversation_id}.jsonl")
        print(f"📁 Readable conversation log: {readable_log}")
        print(f"📁 Code execution logs: code_workspace/")
        
    except Exception as e:
        logger.error(f"MVP Demo failed: {e}")
        print(f"❌ MVP Demo failed: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code) 