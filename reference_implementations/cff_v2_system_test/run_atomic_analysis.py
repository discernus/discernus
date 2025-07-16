#!/usr/bin/env python3
"""
CFF v2.0 Atomic Analysis Runner
===============================

Runs the reconnaissance mission as defined in our test protocol:
- Run A: Identity axis only (Individual Dignity vs Tribal Dominance)
- Run B: Fear/Hope emotional axis only  
- THIN Synthesis: Integrate atomic analyses

Historic test of graduated normative layering with competitive dynamics.
"""

import asyncio
import sys
import os
import json
from pathlib import Path
from datetime import datetime

# Add project root to path
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.orchestration.orchestrator import ThinOrchestrator, ResearchConfig

class CFFAtomicAnalysisRunner:
    """Runs atomic CFF analyses following THIN synthesis methodology"""
    
    def __init__(self, test_dir: Path):
        self.test_dir = Path(test_dir)
        self.results_dir = self.test_dir / "atomic_results"
        self.results_dir.mkdir(exist_ok=True)
        self.orchestrator = ThinOrchestrator(str(project_root))
        
    async def run_identity_axis_analysis(self) -> dict:
        """Run A: Identity axis only (Individual Dignity vs Tribal Dominance)"""
        
        print("🎯 STARTING RUN A: Identity Axis Analysis")
        print("=" * 60)
        print("Focus: Individual Dignity vs Tribal Dominance")
        print("Layer: CFF Layer 3 (Normative) - Identity axis only")
        print("Expected: High tribal dominance, low individual dignity")
        print()
        
        # Load the Trump speech
        speech_file = self.test_dir / "source_texts" / "trump_announcement_2016_06_16.txt"
        speech_text = speech_file.read_text()
        
        # Create focused research question for Identity axis
        research_question = """
Using the Cohesive Flourishing Framework (CFF) v2.0, analyze ONLY the Identity axis of this speech.

Focus exclusively on:
- Individual Dignity vs Tribal Dominance positioning
- Evidence for universal human worth, moral agency, pluralistic respect
- Evidence for group loyalty over universal principles, hierarchical exclusion
- Competitive dynamics between these two poles
- Confidence levels based on evidence quality

Apply CFF Layer 3 (Comprehensive Social Health Assessment) but ONLY for the Identity axis.
Use the full normative evaluation capability but constrain to identity dimensions only.

Provide structured analysis with:
1. Individual Dignity score (0.0-1.0) with specific evidence citations
2. Tribal Dominance score (0.0-1.0) with specific evidence citations  
3. Competitive dynamics analysis between the two poles
4. Confidence levels and uncertainty flags
5. Reasoning chains for all scoring decisions

Expected format: Complete CFF v2.0 analysis structure but limited to Identity axis.
"""
        
        # Create research configuration
        config = ResearchConfig(
            research_question=research_question,
            source_texts=speech_text,
            enable_code_execution=True
        )
        
        # Run the analysis
        session_id = await self.orchestrator.start_research_session(config)
        print(f"✅ Session started: {session_id}")
        
        # Get design consultation
        design_response = await self.orchestrator.run_design_consultation(session_id)
        
        # Auto-approve for automated testing
        self.orchestrator.approve_design(session_id, True)
        
        # Execute analysis
        results = await self.orchestrator.execute_approved_analysis(session_id)
        
        # Save results
        output_file = self.results_dir / "identity_axis_analysis.json"
        with open(output_file, 'w') as f:
            json.dump({
                'analysis_type': 'identity_axis_only',
                'timestamp': datetime.now().isoformat(),
                'session_id': session_id,
                'conversation_id': results.get('conversation_id'),
                'research_question': research_question,
                'status': results.get('status'),
                'results': results
            }, f, indent=2)
        
        print(f"✅ Run A completed - Results saved to: {output_file}")
        return results
        
    async def run_fear_hope_axis_analysis(self) -> dict:
        """Run B: Fear/Hope emotional axis only"""
        
        print("\n🎯 STARTING RUN B: Fear/Hope Axis Analysis")
        print("=" * 60)
        print("Focus: Fear vs Hope emotional orientation")
        print("Layer: CFF Layer 1 (Descriptive) - Emotional climate only")
        print("Expected: Moderate fear and hope with competitive dynamics")
        print()
        
        # Load the Trump speech
        speech_file = self.test_dir / "source_texts" / "trump_announcement_2016_06_16.txt"
        speech_text = speech_file.read_text()
        
        # Create focused research question for Fear/Hope axis
        research_question = """
Using the Cohesive Flourishing Framework (CFF) v2.0, analyze ONLY the Fear/Hope emotional axis of this speech.

Focus exclusively on:
- Fear patterns: anxiety, threat perception, catastrophic thinking
- Hope patterns: optimism, constructive vision, positive possibility  
- Competitive dynamics between fear and hope messaging
- Temporal patterns in emotional positioning
- Evidence quality and confidence levels

Apply CFF Layer 1 (Descriptive Emotional Climate) for neutral analysis without normative judgment.
Avoid cohesive/fragmentative language - focus purely on emotional patterns.

Provide structured analysis with:
1. Fear score (0.0-1.0) with specific evidence citations
2. Hope score (0.0-1.0) with specific evidence citations
3. Competitive dynamics analysis (dilution, replacement, amplification)
4. Temporal emotional evolution patterns
5. Confidence levels and uncertainty flags
6. Reasoning chains for all assessments

Expected format: Complete CFF v2.0 emotional climate analysis with mathematical competitive dynamics modeling.
"""
        
        # Create research configuration  
        config = ResearchConfig(
            research_question=research_question,
            source_texts=speech_text,
            enable_code_execution=True
        )
        
        # Run the analysis
        session_id = await self.orchestrator.start_research_session(config)
        print(f"✅ Session started: {session_id}")
        
        # Get design consultation
        design_response = await self.orchestrator.run_design_consultation(session_id)
        
        # Auto-approve for automated testing
        self.orchestrator.approve_design(session_id, True)
        
        # Execute analysis
        results = await self.orchestrator.execute_approved_analysis(session_id)
        
        # Save results
        output_file = self.results_dir / "fear_hope_axis_analysis.json"
        with open(output_file, 'w') as f:
            json.dump({
                'analysis_type': 'fear_hope_axis_only',
                'timestamp': datetime.now().isoformat(),
                'session_id': session_id,
                'conversation_id': results.get('conversation_id'),
                'research_question': research_question,
                'status': results.get('status'),
                'results': results
            }, f, indent=2)
        
        print(f"✅ Run B completed - Results saved to: {output_file}")
        return results

    async def run_thin_synthesis(self) -> dict:
        """THIN Synthesis: Integrate atomic analyses using corpus approach"""
        
        print("\n🎯 STARTING THIN SYNTHESIS")
        print("=" * 60)
        print("Approach: Feed atomic analysis files as 'corpus' to synthesis agent")
        print("Task: Integrate Identity + Fear/Hope into comprehensive CFF analysis")
        print("Innovation: THIN methodology - let LLM handle complex reassembly")
        print()
        
        # Load atomic analysis results as "corpus"
        identity_file = self.results_dir / "identity_axis_analysis.json"
        fear_hope_file = self.results_dir / "fear_hope_axis_analysis.json"
        
        if not identity_file.exists() or not fear_hope_file.exists():
            raise FileNotFoundError("Atomic analyses must be completed before synthesis")
        
        # Read atomic analyses
        with open(identity_file) as f:
            identity_analysis = json.load(f)
        with open(fear_hope_file) as f:
            fear_hope_analysis = json.load(f)
        
        # Create synthesis corpus
        synthesis_corpus = f"""
=== ATOMIC ANALYSIS 1: IDENTITY AXIS ===
{json.dumps(identity_analysis, indent=2)}

=== ATOMIC ANALYSIS 2: FEAR/HOPE AXIS ===
{json.dumps(fear_hope_analysis, indent=2)}

=== ORIGINAL SOURCE TEXT ===
FILE: trump_announcement_2016_06_16.txt
{(self.test_dir / "source_texts" / "trump_announcement_2016_06_16.txt").read_text()}
"""
        
        # Create synthesis research question
        research_question = """
You are a CFF v2.0 synthesis specialist. I'm providing you with multiple focused analyses of the same text from different analytical perspectives.

CORPUS OF ANALYSES:
- identity_axis_analysis.json: Identity axis (Individual Dignity vs Tribal Dominance) analysis
- fear_hope_axis_analysis.json: Fear/Hope emotional axis analysis
- Original source text for reference

Your task: Synthesize these atomic analyses into a comprehensive CFF v2.0 analysis that includes:

1. **Integrated Axis Scoring**: Combine Identity and Fear/Hope axes with competitive dynamics
2. **Cross-Axis Competitive Dynamics**: Model how Identity positioning amplifies or dilutes emotional patterns
3. **Mathematical Consistency**: Apply proper competitive dynamics adjustments (dilution, replacement, amplification)
4. **Confidence Harmonization**: Reconcile confidence assessments across analyses
5. **Complete CFF v2.0 Package**: Generate full results structure with all required fields

Preserve all evidence chains and reasoning from the atomic analyses. Apply competitive dynamics adjustments based on the integrated evidence. Flag any inconsistencies between atomic analyses for review.

Focus especially on:
- How tribal dominance positioning affects fear/hope competitive dynamics
- Whether identity and emotional positioning show strategic coherence
- Mathematical modeling of cross-axis amplification effects
- Comprehensive confidence assessment across integrated results

Expected output: Complete CFF v2.0 analysis meeting framework specification with cross-axis competitive dynamics modeling.
"""
        
        # Create research configuration using synthesis corpus
        config = ResearchConfig(
            research_question=research_question,
            source_texts=synthesis_corpus,
            enable_code_execution=True
        )
        
        # Run synthesis analysis
        session_id = await self.orchestrator.start_research_session(config)
        print(f"✅ Synthesis session started: {session_id}")
        
        # Get design consultation
        design_response = await self.orchestrator.run_design_consultation(session_id)
        
        # Auto-approve for automated testing
        self.orchestrator.approve_design(session_id, True)
        
        # Execute synthesis
        results = await self.orchestrator.execute_approved_analysis(session_id)
        
        # Save synthesis results
        output_file = self.results_dir / "thin_synthesis_analysis.json"
        with open(output_file, 'w') as f:
            json.dump({
                'analysis_type': 'thin_synthesis',
                'timestamp': datetime.now().isoformat(),
                'session_id': session_id,
                'conversation_id': results.get('conversation_id'),
                'research_question': research_question,
                'atomic_inputs': [str(identity_file), str(fear_hope_file)],
                'status': results.get('status'),
                'results': results
            }, f, indent=2)
        
        print(f"✅ THIN Synthesis completed - Results saved to: {output_file}")
        return results

    async def run_full_reconnaissance_mission(self):
        """Execute the complete reconnaissance mission"""
        
        print("🚀 CFF v2.0 RECONNAISSANCE MISSION")
        print("=" * 80)
        print("Historic test: First systematic validation of graduated normative layering")
        print("Methodology: THIN synthesis approach with atomic analysis")
        print("Framework: CFF v2.0 with competitive dynamics modeling")
        print()
        
        try:
            # Run atomic analyses
            identity_results = await self.run_identity_axis_analysis()
            fear_hope_results = await self.run_fear_hope_axis_analysis()
            
            # Run THIN synthesis
            synthesis_results = await self.run_thin_synthesis()
            
            # Create mission summary
            mission_summary = {
                'mission_type': 'cff_v2_reconnaissance',
                'start_time': datetime.now().isoformat(),
                'atomic_analyses': {
                    'identity_axis': {
                        'status': identity_results.get('status'),
                        'session_id': identity_results.get('conversation_id')
                    },
                    'fear_hope_axis': {
                        'status': fear_hope_results.get('status'),
                        'session_id': fear_hope_results.get('conversation_id')
                    }
                },
                'thin_synthesis': {
                    'status': synthesis_results.get('status'),
                    'session_id': synthesis_results.get('conversation_id')
                },
                'mission_status': 'completed',
                'results_directory': str(self.results_dir)
            }
            
            # Save mission summary
            summary_file = self.results_dir / "mission_summary.json"
            with open(summary_file, 'w') as f:
                json.dump(mission_summary, f, indent=2)
            
            print("\n" + "=" * 80)
            print("🎉 RECONNAISSANCE MISSION COMPLETED!")
            print("=" * 80)
            print(f"📁 All results saved to: {self.results_dir}")
            print(f"📋 Mission summary: {summary_file}")
            print()
            print("Ready for evaluation against test protocol success criteria!")
            
        except Exception as e:
            print(f"\n❌ MISSION FAILED: {e}")
            raise

async def main():
    """Main execution function"""
    
    # Get current test directory
    test_dir = Path(__file__).parent
    
    # Initialize runner
    runner = CFFAtomicAnalysisRunner(test_dir)
    
    # Execute reconnaissance mission
    await runner.run_full_reconnaissance_mission()

if __name__ == "__main__":
    asyncio.run(main()) 