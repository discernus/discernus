#!/usr/bin/env python3
"""
Development Test Runner for Discernus
====================================

Convenient script for running automated research sessions during development.
Simulates human researcher interactions for end-to-end testing.

USAGE:
    # Quick test with Lincoln/Trump corpus
    python3 dev_test_runner.py

    # Custom research question and corpus
    python3 dev_test_runner.py --question "How does rhetoric work?" --corpus "data/my_texts/"

    # Different researcher profile
    python3 dev_test_runner.py --profile "political_discourse_expert"

    # Test DiscernusLibrarian specifically
    python3 dev_test_runner.py --test-knowledgenaut
"""

import asyncio
import argparse
import logging
import json
from pathlib import Path
from datetime import datetime
from typing import Dict

# Add project root to path
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from discernus.orchestration.workflow_orchestrator import WorkflowOrchestrator
from discernus.core.agent_roles import get_available_researcher_profiles, add_custom_researcher_profile

# Configure logging for dev testing
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class DevTestRunner:
    """Development test runner for automated sessions"""
    
    def __init__(self):
        self.orchestrator = WorkflowOrchestrator("/tmp/test_project")  # Use current orchestrator
        # Get available profiles from the externalized system
        self.available_profiles = get_available_researcher_profiles()
    
    def get_researcher_profile_descriptions(self) -> Dict[str, str]:
        """Get descriptions for available researcher profiles"""
        descriptions = {
            'experienced_computational_social_scientist': 'Emphasizes quantitative validation, statistical rigor, and reproducible computational methods',
            'political_discourse_expert': 'Focuses on rhetorical sophistication, historical context, and communication nuances',
            'digital_humanities_scholar': 'Bridges computational and humanistic approaches with interpretive depth',
            'skeptical_methodologist': 'Applies high methodological standards with critical evaluation of potential flaws'
        }
        
        # Add any custom profiles that might have been added
        for profile in self.available_profiles:
            if profile not in descriptions:
                descriptions[profile] = 'Custom researcher profile'
        
        return descriptions
    
    async def run_quick_test(self, 
                           research_question: str = None,
                           corpus_path: str = None,
                           researcher_profile: str = "experienced_computational_social_scientist") -> dict:
        """Run a quick automated test with default or provided parameters"""
        
        # Default test case
        if not research_question:
            research_question = "How do the rhetorical strategies and emotional appeals differ between Lincoln's 1865 Second Inaugural and Trump's 2025 Inaugural addresses?"
        
        if not corpus_path:
            corpus_path = "data/inaugural_addresses/"
        
        logger.info(f"🧪 Running automated test")
        logger.info(f"📋 Research Question: {research_question}")
        logger.info(f"📂 Corpus: {corpus_path}")
        logger.info(f"🧑‍🔬 Researcher Profile: {researcher_profile}")
        
        try:
            results = await ThinOrchestrator.quick_analysis(
                research_question=research_question,
                corpus_path=corpus_path,
                researcher_profile=researcher_profile
            )
            
            logger.info("✅ Automated test completed successfully!")
            logger.info(f"📁 Results saved to: {results['session_path']}")
            
            return results
            
        except Exception as e:
            logger.error(f"❌ Test failed: {e}")
            raise
    
    async def test_knowledgenaut_specifically(self) -> dict:
        """Run a test specifically designed to test the DiscernusLibrarian agent"""
        
        research_question = """
I've developed the Cohesive Flourishing Framework (CFF) v2.0 as a comprehensive computational rhetoric analysis framework. 
I need framework interrogation to validate novel terminology like "graduated normative layering" against academic literature 
and identify any semantic gaps or terminology issues. Please conduct thorough framework validation with academic literature mapping.
"""
        
        # Small test corpus for framework validation
        corpus_text = """
FRAMEWORK EXCERPT:
Graduated Normative Layering: The systematic ability to scale analysis depth from neutral description to explicit moral evaluation.

Competitive Dynamics Modeling: Mathematical modeling of how rhetorical strategies compete within texts.

Five Orthogonal Axes: Identity, Fear/Hope, Envy/Compersion, Enmity/Amity, Goal orientation.
"""
        
        config = ResearchConfig(
            research_question=research_question,
            source_texts=corpus_text,
            enable_code_execution=True,
            dev_mode=True,
            simulated_researcher_profile="computational_social_scientist"
        )
        
        logger.info("🧪 Testing DiscernusLibrarian agent specifically")
        logger.info("📋 Framework validation scenario")
        
        results = await self.orchestrator.run_automated_session(config)
        
        logger.info("✅ Knowledgenaut test completed!")
        logger.info(f"📁 Results saved to: {results['session_path']}")
        
        return results
    
    def list_profiles(self):
        """List available researcher profiles"""
        print("📋 Available Researcher Profiles:")
        print()
        for profile, description in self.get_researcher_profile_descriptions().items():
            print(f"  {profile}")
            print(f"    {description}")
            print()

    def add_custom_profile_example(self):
        """Add an example custom researcher profile to demonstrate customization"""
        add_custom_researcher_profile(
            'strict_experimentalist',
            feedback_prompt="""
You are simulating a strict experimental psychologist reviewing a research design proposal.

RESEARCH QUESTION: {research_question}

DESIGN PROPOSAL TO REVIEW:
{context}

Your Task:
Apply rigorous experimental standards. Consider:
- Is there proper experimental control?
- Can we establish causation, not just correlation?
- Are confounding variables adequately controlled?
- Is the sample size sufficient for statistical power?
- Can findings be replicated?

Be demanding about experimental rigor. Reject designs that rely too heavily on observational or correlational methods without strong justification.

Keep your response concise but thorough (2-3 paragraphs maximum).
""",
            decision_prompt="""
You are a strict experimentalist deciding whether to approve a research design.

RESEARCH QUESTION: {research_question}

LATEST DESIGN PROPOSAL:
{design_response}

YOUR PREVIOUS FEEDBACK:
{feedback}

Your Task:
Apply experimental psychology standards rigorously.

Approve ONLY if:
- The design includes proper experimental controls
- Causal claims are justified by the methodology
- Confounding variables are adequately addressed
- Sample sizes are sufficient for statistical power
- The approach supports replicable findings

Request revisions if:
- Methodology is primarily observational without strong justification
- Causal claims exceed what the design can support
- Insufficient control for confounding variables
- Statistical power concerns not addressed

Respond with just: "APPROVE" or "REVISE: [specific experimental concern]"
"""
        )
        
        print("✅ Added custom 'strict_experimentalist' profile")
        print("📋 This profile emphasizes experimental control and causal inference")
        
        # Update available profiles
        self.available_profiles = get_available_researcher_profiles()

async def main():
    """Main CLI interface"""
    parser = argparse.ArgumentParser(
        description="Development test runner for Discernus automated sessions",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python3 dev_test_runner.py
  python3 dev_test_runner.py --question "How does rhetoric work?" --corpus "data/my_texts/"
  python3 dev_test_runner.py --profile "political_discourse_expert"
  python3 dev_test_runner.py --test-knowledgenaut
  python3 dev_test_runner.py --list-profiles
  python3 dev_test_runner.py --add-custom-profile
        """
    )
    
    parser.add_argument('--question', '-q', 
                       help='Research question to analyze')
    parser.add_argument('--corpus', '-c',
                       help='Path to corpus file or directory')
    parser.add_argument('--profile', '-p', 
                       default='experienced_computational_social_scientist',
                       help='Simulated researcher profile')
    parser.add_argument('--test-knowledgenaut', 
                       action='store_true',
                       help='Run specific test for DiscernusLibrarian agent')
    parser.add_argument('--list-profiles',
                       action='store_true', 
                       help='List available researcher profiles')
    parser.add_argument('--add-custom-profile',
                       action='store_true',
                       help='Add example custom researcher profile and test it')
    parser.add_argument('--output-json',
                       help='Save results to JSON file')
    
    args = parser.parse_args()
    
    runner = DevTestRunner()
    
    if args.list_profiles:
        runner.list_profiles()
        return
    
    if args.add_custom_profile:
        runner.add_custom_profile_example()
        print()
        print("🧪 Testing with custom 'strict_experimentalist' profile...")
        results = await runner.run_quick_test(
            research_question=args.question,
            corpus_path=args.corpus,
            researcher_profile='strict_experimentalist'
        )
    elif args.test_knowledgenaut:
        results = await runner.test_knowledgenaut_specifically()
    else:
        results = await runner.run_quick_test(
            research_question=args.question,
            corpus_path=args.corpus,
            researcher_profile=args.profile
        )
    
    # Save results if requested
    if args.output_json:
        output_path = Path(args.output_json)
        with open(output_path, 'w') as f:
            json.dump(results, f, indent=2, default=str)
        logger.info(f"💾 Results saved to: {output_path}")
    
    # Print summary
    print()
    print("🎯 Test Summary:")
    print(f"   Session ID: {results['session_id']}")
    print(f"   Status: {results['status']}")
    print(f"   Turns: {results['turns']}")
    print(f"   Design Iterations: {results['design_iterations']}")
    print(f"   Results Path: {results['session_path']}")
    print()
    print("📚 To view results:")
    print(f"   cat {results['session_path']}/conversation_readable.md")

if __name__ == "__main__":
    asyncio.run(main()) 