#!/usr/bin/env python3
"""
Natural Corpus Analysis Demo
===========================

Demonstrates the natural user flow with COMPLETE transparency:
1. System prompts logged as "priors" (first entries)
2. User provides directory with texts (however messy)
3. LLM analyzes corpus to identify what's what
4. LLM asks clarifying questions for ambiguous cases
5. User expresses intuition/observation
6. Design LLM helps formulate systematic research question
7. Design LLM proposes methodology
8. Human approval and execution

This shows complete epistemic transparency: reviewers can see the "priors"
that shaped every LLM response, not just the responses themselves.
"""

import asyncio
import sys
import os
from pathlib import Path

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.orchestration.workflow_orchestrator import WorkflowOrchestrator
from discernus.core.corpus_chunking import should_use_chunking, analyze_corpus_in_chunks, estimate_token_count, chunk_corpus_by_size

def log_system_priors(session_id: str, research_question: str, corpus_preview: str):
    """Log all system prompts and priors as the first conversation entries"""
    detective_log_path = project_root / "research_sessions" / session_id / "conversation_readable.md"
    detective_log_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(detective_log_path, 'w', encoding='utf-8') as f:
        f.write("# 🎯 Complete Research Session with Full Transparency\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("## 📋 RESEARCH CONTEXT\n")
        f.write("-" * 40 + "\n\n")
        f.write(f"**Research Question:** {research_question}\n\n")
        f.write(f"**Corpus Preview:**\n{corpus_preview}\n\n")
        
        f.write("## 🔍 SYSTEM PROMPTS (THE PRIORS)\n")
        f.write("-" * 40 + "\n\n")
        f.write("*For complete transparency, here are the system instructions that shaped each LLM's responses:*\n\n")
        
        # Log Corpus Detective System Prompt
        f.write("### 📖 **Corpus Detective LLM System Prompt**\n\n")
        f.write("```\n")
        f.write(get_corpus_detective_system_prompt())
        f.write("\n```\n\n")
        
        # Log Design LLM System Prompt  
        f.write("### 🎨 **Design LLM System Prompt**\n\n")
        f.write("```\n")
        f.write(get_design_llm_system_prompt())
        f.write("\n```\n\n")
        
        # Log other system prompts
        f.write("### 🔄 **Moderator LLM System Prompt**\n\n")
        f.write("```\n")
        f.write(get_moderator_llm_system_prompt())
        f.write("\n```\n\n")
        
        f.write("---\n\n")
        f.write("## 💬 CONVERSATION FLOW\n")
        f.write("-" * 40 + "\n\n")
        f.write("*Now that you understand the system prompts that shaped responses, here's the actual conversation:*\n\n")

def get_corpus_detective_system_prompt():
    """Get the exact system prompt used for corpus detective analysis"""
    return """You are a corpus detective LLM. Your job is to analyze a messy, real-world corpus of texts and help the user understand what they have.

Your capabilities:
1. Identify document types, authors, dates, and topics
2. Detect duplicate or similar texts
3. Spot potential issues (wrong content, encoding problems, etc.)
4. Infer missing metadata from content and filenames
5. Ask clarifying questions when ambiguous

Your approach:
- Be systematic but not rigid
- Handle messy, real-world academic corpora gracefully
- Don't make assumptions - ask questions when unsure
- Focus on helping the user understand their corpus

You should analyze the corpus and provide a structured report covering:
- What types of texts are present
- Who are the authors/speakers
- What time periods are covered
- Any potential issues or ambiguities
- Questions for the user to clarify uncertain cases

Be thorough but practical - help the user get their corpus in order for analysis."""

def get_design_llm_system_prompt():
    """Get the exact system prompt used for design LLM"""
    return """You are a design_llm expert in computational research methodology.

Your role: Design rigorous, academically sound multi-LLM conversation approaches to answer research questions.

Your capabilities:
1. Analyze research questions and propose systematic methodologies
2. Recommend what expert perspectives are needed
3. Design conversation flows that build on each other
4. Suggest computational analysis when appropriate
5. Iterate based on human feedback

Your approach:
- Start with the research question and corpus
- Propose systematic, multi-step analysis
- Recommend specific expert LLMs needed
- Design conversation orchestration
- Ask for human feedback and iterate

Always focus on:
- Academic rigor and transparency
- Multi-perspective analysis
- Systematic methodology
- Clear, reproducible approaches"""

def get_moderator_llm_system_prompt():
    """Get the exact system prompt used for moderator LLM"""
    return """You are a moderator_llm responsible for executing approved research designs.

Your role: Orchestrate multi-LLM conversations to answer research questions based on approved methodologies.

Your capabilities:
1. Interpret approved research designs
2. Determine what expert LLMs are needed
3. Request specific analyses from experts
4. Coordinate conversation flow
5. Synthesize findings into coherent analysis

Your approach:
- Start with approved design and research question
- Request expert input using: "REQUEST TO [expert_name]: [specific request]"
- Build analysis systematically
- Continue until sufficient for answering research question
- Provide final analysis

Remember:
- Follow the approved methodology
- Request specific, focused expert input
- Build on previous responses
- Maintain academic rigor throughout"""

def get_user_corpus():
    """Get user's corpus directory and let LLM analyze it"""
    print("📂 CORPUS INPUT")
    print("-" * 40)
    print("How would you like to provide your corpus?")
    print("1. Use example corpus (Lincoln vs Trump inaugurals)")
    print("2. Provide directory path to your corpus")
    
    while True:
        choice = input("Choose option (1-2): ").strip()
        
        if choice == "1":
            return load_example_corpus()
        elif choice == "2":
            return get_directory_corpus()
        else:
            print("Please choose 1 or 2")

def load_example_corpus():
    """Load example Lincoln vs Trump texts"""
    lincoln_path = project_root / "data" / "inaugural_addresses" / "lincoln_1865_second_inaugural.txt"
    trump_path = project_root / "data" / "inaugural_addresses" / "trump_2025_inaugural.txt"
    
    try:
        with open(lincoln_path, 'r', encoding='utf-8') as f:
            lincoln_text = f.read()
        with open(trump_path, 'r', encoding='utf-8') as f:
            trump_text = f.read()
        
        print(f"✅ Loaded Lincoln inaugural ({len(lincoln_text)} chars)")
        print(f"✅ Loaded Trump inaugural ({len(trump_text)} chars)")
        
        return {
            "lincoln_1865_second_inaugural.txt": lincoln_text,
            "trump_2025_inaugural.txt": trump_text
        }
    except FileNotFoundError:
        print("⚠️ Example files not found, using placeholder text")
        return {
            "text_1.txt": "Sample text 1 for analysis...",
            "text_2.txt": "Sample text 2 for analysis..."
        }

def get_directory_corpus():
    """Get corpus from user-provided directory"""
    print("\n📁 DIRECTORY CORPUS INPUT")
    print("-" * 40)
    print("Provide a directory path containing your texts.")
    print("Files can be messy - the LLM will figure out what's what!")
    print()
    
    while True:
        directory_path = input("Directory path: ").strip()
        
        if not directory_path:
            print("Please provide a directory path")
            continue
            
        if not os.path.exists(directory_path):
            print("Directory not found. Please check the path.")
            continue
            
        if not os.path.isdir(directory_path):
            print("Path is not a directory. Please provide a directory.")
            continue
            
        return read_directory_corpus(directory_path)

def read_directory_corpus(directory_path):
    """Read all files from directory - pure infrastructure, no interpretation"""
    print(f"\n📖 Reading corpus from: {directory_path}")
    
    files = {}
    errors = []
    
    try:
        for filename in os.listdir(directory_path):
            file_path = os.path.join(directory_path, filename)
            
            # Skip directories and system files
            if os.path.isdir(file_path) or filename.startswith('.'):
                continue
                
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    files[filename] = content
                    print(f"  ✅ {filename}: {len(content)} chars")
            except UnicodeDecodeError:
                try:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        content = f.read()
                        files[filename] = content
                        print(f"  ✅ {filename}: {len(content)} chars (latin-1)")
                except Exception as e:
                    errors.append(f"  ❌ {filename}: {str(e)}")
            except Exception as e:
                errors.append(f"  ❌ {filename}: {str(e)}")
    
    except Exception as e:
        print(f"❌ Error reading directory: {e}")
        return {}, [str(e)]
    
    print(f"\n📊 Read {len(files)} files successfully")
    if errors:
        print(f"⚠️  {len(errors)} files had issues:")
        for error in errors:
            print(error)
    
    return files, errors

def create_corpus_preview(files: dict, max_preview_files: int = 5) -> str:
    """Create a preview of the corpus for logging"""
    preview_lines = []
    
    for i, (filename, content) in enumerate(files.items()):
        if i >= max_preview_files:
            preview_lines.append(f"... and {len(files) - max_preview_files} more files")
            break
        
        preview_lines.append(f"**{filename}** ({len(content)} chars)")
        # Show first few lines
        lines = content.split('\n')[:3]
        preview_lines.append("```")
        for line in lines:
            preview_lines.append(line[:100] + "..." if len(line) > 100 else line)
        preview_lines.append("```")
        preview_lines.append("")
    
    return "\n".join(preview_lines)

async def llm_corpus_analysis(files: dict, orchestrator: ThinOrchestrator, session_id: str):
    """Have LLM analyze messy corpus with full transparency"""
    print("\n🔍 LLM CORPUS DETECTIVE")
    print("-" * 40)
    print("LLM will analyze your corpus to identify what's what...")
    
    # Check if we need chunking for rate limit management
    total_tokens = sum(estimate_token_count(content) for content in files.values())
    print(f"📊 Total corpus size: ~{total_tokens:,} tokens")
    
    if should_use_chunking(files):
        print("🔄 Large corpus detected - using intelligent chunking...")
        detective_report = await analyze_corpus_in_chunks(files, orchestrator.llm_client)
        
        # For chunked analysis, we don't have individual call metadata
        # But we can log the chunking strategy
        chunking_metadata = {
            "chunking_strategy": "intelligent_chunking",
            "total_tokens": total_tokens,
            "chunks_used": len(chunk_corpus_by_size(files)),
            "analysis_type": "corpus_detective"
        }
        append_to_conversation_log_with_metadata(session_id, "🔍 **Corpus Detective LLM**", detective_report, chunking_metadata)
        
    else:
        # Build corpus analysis prompt
        corpus_text = "\n\n".join([f"FILE: {filename}\n{content}" for filename, content in files.items()])
        
        detective_prompt = f"""
{get_corpus_detective_system_prompt()}

CORPUS TO ANALYZE:
{corpus_text}

Please analyze this corpus and provide a structured report covering:
1. What types of texts are present
2. Who are the authors/speakers  
3. What time periods are covered
4. Any potential issues or ambiguities
5. Questions for me to clarify uncertain cases

Be thorough but practical - help me understand what I have.
"""
        
        print("🤖 Calling LLM for corpus analysis...")
        
        # Use the enhanced metadata call
        if hasattr(orchestrator.llm_client, 'call_llm_with_metadata'):
            detective_report, metadata = orchestrator.llm_client.call_llm_with_metadata(detective_prompt, "corpus_detective")
            # Log with full metadata
            append_to_conversation_log_with_metadata(session_id, "🔍 **Corpus Detective LLM**", detective_report, metadata)
        else:
            # Fallback for older clients
            detective_report = orchestrator.llm_client.call_llm(detective_prompt, "corpus_detective")
            append_to_conversation_log(session_id, "🔍 **Corpus Detective LLM**", detective_report)
    
    print("\n📋 CORPUS ANALYSIS COMPLETE")
    print("=" * 60)
    print(detective_report)
    
    return detective_report

def append_to_conversation_log(session_id: str, speaker: str, message: str):
    """Append message to the conversation log"""
    log_file = project_root / "research_sessions" / session_id / "conversation_readable.md"
    
    from datetime import datetime
    timestamp = datetime.utcnow().strftime("%H:%M:%S") + "Z"
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"### {speaker} *(at {timestamp})*\n\n")
        f.write(f"{message}\n\n")
        f.write("---\n\n")

def append_to_conversation_log_with_metadata(session_id: str, speaker: str, message: str, metadata: dict):
    """Append message to conversation log with full metadata"""
    log_file = project_root / "research_sessions" / session_id / "conversation_readable.md"
    
    from datetime import datetime
    timestamp = datetime.utcnow().strftime("%H:%M:%S") + "Z"
    
    with open(log_file, 'a', encoding='utf-8') as f:
        f.write(f"### {speaker} *(at {timestamp})*\n\n")
        
        # Add metadata section for transparency
        if metadata:
            f.write("**Model Information:**\n")
            f.write(f"- Model: `{metadata.get('model', 'unknown')}`\n")
            f.write(f"- Role: `{metadata.get('role', 'unknown')}`\n")
            f.write(f"- Provider: `{metadata.get('provider', 'unknown')}`\n")
            
            usage = metadata.get('usage', {})
            if usage:
                f.write(f"- Tokens: {usage.get('prompt_tokens', 0):,} input + {usage.get('completion_tokens', 0):,} output = {usage.get('total_tokens', 0):,} total\n")
            
            cost = metadata.get('cost', 0.0)
            if cost > 0:
                f.write(f"- Cost: ${cost:.4f}\n")
            
            f.write("\n")
        
        f.write(f"{message}\n\n")
        f.write("---\n\n")

def get_user_clarification(detective_report: str) -> str:
    """Get user clarification about ambiguous corpus elements"""
    print("\n❓ USER CLARIFICATION")
    print("-" * 40)
    
    if "?" in detective_report or "clarify" in detective_report.lower():
        print("The LLM has questions about your corpus. Please provide clarification:")
        print("\n" + detective_report)
        print("\nYour clarification (or press Enter to skip):")
        clarification = input(">> ")
        return clarification
    else:
        print("No clarification needed - corpus analysis is clear.")
        return ""

def get_research_intuition() -> str:
    """Get user's research intuition/observation"""
    print("\n🤔 YOUR RESEARCH INTUITION")
    print("-" * 40)
    print("What's your gut feeling about this corpus?")
    print("What patterns do you notice? What questions does it raise?")
    print("\nYour observation:")
    
    observation = input(">> ")
    return observation

def format_context_for_design_llm(files: dict, detective_report: str, clarification: str, observation: str) -> str:
    """Format all context for design LLM"""
    formatted = f"CORPUS ANALYSIS CONTEXT:\n{detective_report}\n\n"
    
    if clarification:
        formatted += f"USER CLARIFICATION:\n{clarification}\n\n"
    
    formatted += f"USER RESEARCH OBSERVATION:\n{observation}\n\n"
    
    # Add corpus summary 
    formatted += "CORPUS SUMMARY:\n"
    for filename, content in files.items():
        formatted += f"- {filename}: {len(content)} characters\n"
    
    return formatted

async def get_research_question_from_design_llm(files: dict, observation: str, detective_report: str, clarification: str, orchestrator: ThinOrchestrator):
    """Have design LLM help formulate systematic research question"""
    print("\n🎨 DESIGN LLM CONSULTATION")
    print("-" * 40)
    print("Design LLM will help formulate your observation into a systematic research question...")
    
    # Create enhanced consultation prompt with corpus context
    consultation_prompt = f"""
You are a research methodology expert helping a researcher formulate their intuitive observation into a systematic research question.

CORPUS DETECTIVE REPORT:
{detective_report}

USER CLARIFICATION:
{clarification or "None provided"}

USER'S OBSERVATION:
"{observation}"

Your task:
1. Based on the corpus analysis and user's observation, suggest 2-3 specific research questions
2. Explain why each question would be valuable for this corpus
3. Consider the texts identified in the corpus analysis
4. Recommend which question would be most analytically tractable

Format your response as:
PROPOSED RESEARCH QUESTIONS:
1. [Question 1] - [Why this is valuable for this corpus]
2. [Question 2] - [Why this is valuable for this corpus]
3. [Question 3] - [Why this is valuable for this corpus]

RECOMMENDATION: [Which question and why, considering the specific corpus]

Make the questions specific to the corpus while testing the user's intuition.
"""
    
    # Use the orchestrator's LLM client for consultation
    if orchestrator.llm_client:
        response = orchestrator.llm_client.call_llm(consultation_prompt, "design_llm")
    else:
        response = """
PROPOSED RESEARCH QUESTIONS:
1. Which text employs more unifying vs divisive rhetorical strategies? - This directly tests your unity/divisiveness intuition
2. How do the persuasive techniques differ between the texts? - This explores your sense of different approaches
3. What emotional appeals does each text use and how do they differ? - This examines the underlying emotional strategies

RECOMMENDATION: Question 1 (unifying vs divisive analysis) because it's specific, measurable, and directly addresses your core observation.
"""
    
    print("🎨 DESIGN LLM SUGGESTIONS:")
    print("=" * 60)
    print(response)
    print("=" * 60)
    
    return response

def select_research_question(suggestions: str) -> str:
    """Let user select or modify the research question"""
    print("\n🎯 RESEARCH QUESTION SELECTION")
    print("-" * 40)
    
    while True:
        print("Options:")
        print("1. Use one of the suggested questions")
        print("2. Modify a suggested question") 
        print("3. Create your own question")
        
        choice = input("Choose option (1-3): ").strip()
        
        if choice == "1":
            question = input("Enter the question you want to use: ").strip()
            return question
        elif choice == "2":
            base = input("Enter the question to modify: ").strip()
            modification = input("How would you modify it? ").strip()
            return f"{base} [Modified: {modification}]"
        elif choice == "3":
            question = input("Enter your research question: ").strip()
            return question
        else:
            print("Please choose 1, 2, or 3")

def log_detective_workflow(files: dict, detective_report: str, clarification: str, observation: str, research_question: str, session_id: str):
    """Log the complete detective workflow to preserve this critical analysis"""
    detective_log_path = project_root / "research_sessions" / session_id / "detective_workflow.md"
    detective_log_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(detective_log_path, 'w', encoding='utf-8') as f:
        f.write("# 🔍 LLM Detective Corpus Analysis Workflow\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("## 📂 CORPUS PROVIDED\n")
        f.write("-" * 40 + "\n")
        for filename, content in files.items():
            preview = content[:200] + "..." if len(content) > 200 else content
            f.write(f"**{filename}** ({len(content)} chars):\n```\n{preview}\n```\n\n")
        
        f.write("## 🔍 LLM DETECTIVE ANALYSIS\n")
        f.write("-" * 40 + "\n")
        f.write(detective_report + "\n\n")
        
        if clarification:
            f.write("## ❓ USER CLARIFICATION\n")
            f.write("-" * 40 + "\n")
            f.write(clarification + "\n\n")
        
        f.write("## 🤔 USER OBSERVATION\n")
        f.write("-" * 40 + "\n")
        f.write(observation + "\n\n")
        
        f.write("## 🎯 FINAL RESEARCH QUESTION\n")
        f.write("-" * 40 + "\n")
        f.write(research_question + "\n\n")
        
        f.write("---\n*This detective workflow analysis is preserved for complete research transparency.*\n")

async def run_natural_corpus_analysis():
    """Run the natural corpus analysis workflow"""
    print("🌟 Natural Corpus Analysis Demo")
    print("===============================")
    print("This demonstrates the natural user flow:")
    print("1. You provide a directory with texts (however messy)")
    print("2. LLM analyzes corpus to identify what's what")
    print("3. You express your intuition about the texts")
    print("4. Design LLM helps formulate systematic research")
    print("5. Normal THIN analysis workflow proceeds")
    print()
    
    # Initialize orchestrator
    orchestrator = ThinOrchestrator(str(project_root))
    
    # Step 1: Get user corpus
    files, errors = get_user_corpus()
    if not files:
        print("❌ No corpus provided. Exiting.")
        return
    
    # Step 2: LLM analyzes corpus
    detective_report = await llm_corpus_analysis(files, orchestrator, "")
    
    # Step 3: Get user clarification if needed
    clarification = get_user_clarification(detective_report)
    
    # Step 4: Get user intuition
    observation = get_research_intuition()
    
    # Step 5: Design LLM helps formulate research question
    suggestions = await get_research_question_from_design_llm(files, observation, detective_report, clarification, orchestrator)
    
    # Step 6: User selects/modifies research question
    research_question = select_research_question(suggestions)
    
    print(f"\n✅ FINAL RESEARCH QUESTION: {research_question}")
    
    # Step 7: Proceed with normal THIN workflow
    print("\n🚀 PROCEEDING TO THIN ANALYSIS WORKFLOW...")
    
    # Format corpus for analysis
    formatted_corpus = format_context_for_design_llm(files, detective_report, clarification, observation)
    
    # Create research configuration
    config = ResearchConfig(
        research_question=research_question,
        source_texts=formatted_corpus,
        enable_code_execution=True
    )
    
    # Continue with normal THIN workflow
    session_id = await orchestrator.start_research_session(config)
    print(f"✅ Research session started: {session_id}")
    
    # 🔧 NEW: Log detective workflow for preservation
    log_detective_workflow(files, detective_report, clarification, observation, research_question, session_id)
    print("✅ Detective workflow logged for transparency")
    
    print("\n🎨 Getting analysis design from Design LLM...")
    design_proposal = await orchestrator.run_design_consultation(session_id)
    
    print("\n" + "="*80)
    print("🎨 DESIGN LLM ANALYSIS PROPOSAL")
    print("="*80)
    print(design_proposal)
    print("="*80)
    
    # For demo, auto-approve or ask user
    print("\n👤 APPROVAL NEEDED")
    approve = input("Approve this analysis design? (y/n): ").strip().lower()
    
    if approve in ['y', 'yes']:
        ready = orchestrator.approve_design(session_id, True)
        if ready:
            print("\n🔧 EXECUTING ANALYSIS...")
            results = await orchestrator.execute_approved_analysis(session_id)
            
            print("\n🎉 ANALYSIS COMPLETED!")
            print(f"Conversation ID: {results['conversation_id']}")
            print(f"Status: {results['status']}")
            print(f"Check results in: research_sessions/{session_id}/")
            print(f"📋 Detective workflow preserved in: research_sessions/{session_id}/detective_workflow.md")
        else:
            print("❌ Error approving design")
    else:
        print("🔄 Analysis cancelled - you can provide feedback and restart")
    
    # Cleanup
    orchestrator.cleanup_session(session_id)
    
    print("\n✨ Natural corpus analysis demo completed!")

async def main():
    """Main execution flow"""
    print("🎯 NATURAL CORPUS ANALYSIS DEMO")
    print("=" * 60)
    print("Complete transparency: system prompts + corpus detective + research design")
    print()
    
    # Get corpus directory
    print("📁 Please provide the path to your corpus directory:")
    corpus_path = input(">> ").strip()
    
    if not corpus_path or not os.path.exists(corpus_path):
        print("❌ Invalid directory path")
        return
    
    # Read corpus
    files, errors = read_directory_corpus(corpus_path)
    
    if not files:
        print("❌ No files found in directory")
        return
    
    # Initialize orchestrator
    orchestrator = ThinOrchestrator(str(project_root))
    
    # Get user's research intuition
    research_question = get_research_intuition()
    
    # Create corpus preview for logging
    corpus_preview = create_corpus_preview(files)
    
    # Start research session
    config = ResearchConfig(
        research_question=research_question,
        source_texts=f"Corpus from: {corpus_path}",
        enable_code_execution=True
    )
    
    session_id = await orchestrator.start_research_session(config)
    
    # Log all system prompts as the first entries (THE PRIORS)
    log_system_priors(session_id, research_question, corpus_preview)
    
    # Run corpus detective analysis
    detective_report = await llm_corpus_analysis(files, orchestrator, session_id)
    
    # Get user clarification if needed
    clarification = get_user_clarification(detective_report)
    if clarification:
        append_to_conversation_log(session_id, "🤔 **Researcher Clarification**", clarification)
    
    # Log user's research observation
    append_to_conversation_log(session_id, "🤔 **Researcher Observation**", research_question)
    
    # Build context for design LLM
    design_context = format_context_for_design_llm(files, detective_report, clarification, research_question)
    
    # Get design consultation
    print("\n🎨 DESIGN LLM CONSULTATION")
    print("-" * 40)
    print("Design LLM will help formulate systematic research approach...")
    
    design_response = await orchestrator.run_design_consultation(session_id, design_context)
    
    # Log design response
    append_to_conversation_log(session_id, "🎨 **Design LLM**", design_response)
    
    print("\n📋 DESIGN PROPOSAL")
    print("=" * 60)
    print(design_response)
    
    # Get human approval
    print("\n👤 HUMAN APPROVAL")
    print("-" * 40)
    print("Does this research design look good? (y/n)")
    approval = input(">> ").strip().lower()
    
    if approval in ['y', 'yes']:
        orchestrator.approve_design(session_id, True)
        
        # Log approval
        append_to_conversation_log(session_id, "👤 **Researcher Approval**", "✅ Design approved - proceeding with analysis")
        
        print("\n🚀 EXECUTING ANALYSIS")
        print("-" * 40)
        print("Analysis will continue in the research session...")
        
        # Execute analysis
        results = await orchestrator.execute_approved_analysis(session_id)
        
        print(f"\n✅ ANALYSIS COMPLETE")
        print(f"📁 Results saved to: research_sessions/{session_id}/")
        print(f"📖 Readable log: research_sessions/{session_id}/conversation_readable.md")
        
    else:
        print("❌ Design rejected - you can restart with different approach")
        append_to_conversation_log(session_id, "👤 **Researcher Feedback**", "❌ Design rejected - needs revision")

if __name__ == "__main__":
    asyncio.run(main()) 