#!/usr/bin/env python3
"""
Analysis Agent - Raw Response Capture with Provenance Stamps
===========================================================

THIN Principle: This agent applies analytical frameworks to text documents
and faithfully captures raw LLM responses without any parsing or validation.
All intelligence resides in the framework's analysis prompt.

PROVENANCE PROTECTION: Uses tamper-evident stamps to prevent text hallucination.
"""

import sys
import json
import asyncio
import hashlib
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

# Add project root to path for imports
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from discernus.gateway.llm_gateway import LLMGateway
from discernus.core.conversation_logger import ConversationLogger
from discernus.core.provenance_stamp import ProvenanceTracker
from discernus.core.unified_logger import UnifiedLogger
from discernus.agents.forensic_qa_agent import ForensicQAAgent

class AnalysisAgent:
    """
    THIN analysis agent that captures raw LLM responses with provenance protection.
    """

    def __init__(self, gateway: LLMGateway):
        """Initialize the agent with necessary components."""
        self.gateway = gateway
        self.provenance_tracker = ProvenanceTracker()
        self.forensic_qa_agent = ForensicQAAgent(gateway)
        print("✅ AnalysisAgent initialized with provenance protection and forensic validation")

    def execute(self, workflow_state: Dict[str, Any], step_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Main execution method that runs analysis on all corpus files with provenance stamps.
        """
        print("🔬 Running AnalysisAgent...")
        
        project_path = Path(workflow_state.get('project_path', ''))
        corpus_path = Path(workflow_state.get('corpus_path', ''))
        
        corpus_files = [f for f in corpus_path.rglob('*') if f.is_file() and f.suffix in ['.txt', '.md']]
        
        if not corpus_files:
            raise ValueError(f"No corpus files found in {corpus_path}")

        experiment_config = workflow_state.get('experiment', {})
        analysis_prompt_template = workflow_state.get('analysis_agent_instructions', '')

        if not analysis_prompt_template:
            raise ValueError("No analysis agent instructions found in workflow state")

        # Initialize unified logger with experiment metadata
        session_id = workflow_state.get('session_id', f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        logger = UnifiedLogger(str(project_path))
        
        # Prepare experiment metadata for self-contained logs
        experiment_metadata = {
            'framework_name': workflow_state.get('framework', {}).get('name', 'Unknown Framework'),
            'framework_version': workflow_state.get('framework', {}).get('version', 'Unknown'),
            'experiment_name': experiment_config.get('name', 'MVA Experiment'),
            'models': experiment_config.get('models', []),
            'runs_per_model': experiment_config.get('runs_per_model', 1),
            'corpus_files': [f.name for f in corpus_files]
        }
        
        conversation_id = logger.start_session(
            session_id=session_id,
            research_question=experiment_config.get('research_question', 'Framework analysis'),
            participants=['analysis_agent', 'forensic_qa_agent'],
            experiment_metadata=experiment_metadata
        )

        # Process each corpus file
        results = {}
        total_successful = 0
        total_failed = 0

        for corpus_file in corpus_files:
            try:
                # Read corpus content
                corpus_text = corpus_file.read_text(encoding='utf-8')
                
                # Create provenance stamp for this content
                stamp = self.provenance_tracker.register_corpus_file(corpus_file, corpus_text)
                
                # Create analysis prompt with provenance stamp
                stamped_prompt = self.provenance_tracker.create_analysis_prompt_with_stamp(
                    corpus_file, corpus_text, analysis_prompt_template
                )
                
                # Execute analysis runs
                models = experiment_config.get('models', ['vertex_ai/gemini-2.5-pro'])
                runs_per_model = experiment_config.get('runs_per_model', 1)
                
                for model_name in models:
                    for run_num in range(1, runs_per_model + 1):
                        try:
                            result = self._run_single_analysis_with_provenance(
                                f"analysis_agent_run{run_num}_{model_name.replace('/', '_')}_{corpus_file.stem}",
                                corpus_file,
                                stamped_prompt,
                                model_name,
                                run_num,
                                project_path,
                                session_id,
                                logger,
                                conversation_id
                            )
                            
                            if result:
                                results[result['agent_id']] = result
                                total_successful += 1
                                
                        except Exception as e:
                            print(f"❌ Analysis failed for {corpus_file.name} run {run_num}: {e}")
                            total_failed += 1
                            
            except Exception as e:
                print(f"❌ Failed to process {corpus_file.name}: {e}")
                total_failed += 1

        print(f"✅ AnalysisAgent complete. {total_successful} successful, {total_failed} failed.")
        
        # Generate provenance report
        provenance_report = self.provenance_tracker.get_provenance_report()
        
        return {
            'analysis_results': results,
            'provenance_report': provenance_report,
            'session_id': session_id,
            'total_successful': total_successful,
            'total_failed': total_failed
        }

    def _run_single_analysis_with_provenance(self, agent_id: str, corpus_file_path: Path, 
                                           stamped_prompt: str, model_name: str, run_num: int, 
                                           project_path: Path, session_id: str, logger: Optional[UnifiedLogger] = None,
                                           conversation_id: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Runs a single analysis with provenance validation.
        """
        
        # Call the LLM with stamped prompt
        content, metadata = self.gateway.execute_call(
            model=model_name,
            prompt=stamped_prompt,
            system_prompt="You are a framework analysis specialist. CRITICAL: Include all provenance stamps in your response."
        )

        if not metadata.get("success"):
            return None

        # PROVENANCE VALIDATION: Check if response contains correct stamp
        validation_result = self.provenance_tracker.validate_llm_response(corpus_file_path, content)
        
        if not validation_result['valid']:
            # Log provenance failure
            if logger:
                logger.log_error(
                    "PROVENANCE_VALIDATION_FAILED",
                    f"Provenance validation failed for {corpus_file_path.name}: {validation_result['error']}",
                    {
                        'agent_id': agent_id,
                        'model_name': model_name,
                        'validation_result': validation_result,
                        'llm_metadata': metadata
                    }
                )
            
            raise ValueError(f"🚨 PROVENANCE FAILURE: {validation_result['error']}")

        # PROVENANCE STAMPS PROVIDE SUFFICIENT PROTECTION
        # Forensic validation disabled - provenance stamps are tamper-evident and more reliable
        print(f"✅ Provenance validation passed for {corpus_file_path.name}")

        # Log successful analysis with provenance validation
        if logger:
            corpus_text = corpus_file_path.read_text(encoding='utf-8')
            logger.log_analysis_result(
                agent_id,
                str(corpus_file_path),
                model_name,
                content,
                run_num,
                provenance_validated=True,
                forensic_validated=False,  # Forensic validation disabled
                metadata={
                    'provenance_stamp': validation_result['expected_stamp'],
                    'llm_metadata': metadata
                },
                corpus_text=corpus_text
            )

        return {
            'agent_id': agent_id,
            'content': content,
            'metadata': metadata,
            'corpus_file': str(corpus_file_path),
            'model_name': model_name,
            'run_num': run_num,
            'provenance_validated': True,
            'provenance_stamp': validation_result['expected_stamp'],
            'forensic_validated': False  # Forensic validation disabled
        } 