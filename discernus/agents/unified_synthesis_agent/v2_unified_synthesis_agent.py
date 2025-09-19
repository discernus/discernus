#!/usr/bin/env python3
"""
V2 Unified Synthesis Agent for Discernus
========================================

V2-compliant synthesis agent that generates publication-ready research reports using:
- V2 StandardAgent interface
- RunContext for data handoffs
- V2 native artifact formats
- Tool calling for structured output
- Enhanced synthesis features

This agent follows the V2 architecture principles and consumes V2-native artifacts.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional
from datetime import datetime

from ...core.standard_agent import StandardAgent
from ...core.agent_base_classes import SynthesisAgent
from ...core.agent_result import AgentResult, VerificationResult
from ...core.run_context import RunContext
from ...core.agent_config import AgentConfig
from ...core.security_boundary import ExperimentSecurityBoundary
from ...core.local_artifact_storage import LocalArtifactStorage
from ...core.audit_logger import AuditLogger
from ...gateway.llm_gateway import LLMGateway
from ...gateway.model_registry import get_model_registry
import yaml


class V2UnifiedSynthesisAgent(SynthesisAgent):
    """
    V2-compliant synthesis agent for research report generation.
    
    This agent implements the V2 StandardAgent interface and consumes V2-native artifacts
    through the RunContext, eliminating filesystem scanning and CSV parsing.
    """
    
    def __init__(self, 
                 security: ExperimentSecurityBoundary,
                 storage: LocalArtifactStorage,
                 audit: AuditLogger,
                 config: Optional[AgentConfig] = None):
        """
        Initialize the V2 UnifiedSynthesisAgent.
        
        Args:
            security: Security boundary for the experiment
            storage: Artifact storage for persistence
            audit: Audit logger for provenance tracking
            config: Optional agent configuration
        """
        super().__init__(security, storage, audit, config)
        
        self.agent_name = "V2UnifiedSynthesisAgent"
        self.logger = logging.getLogger(__name__)
        
        # Initialize LLM gateway
        self.llm_gateway = LLMGateway(get_model_registry())
        
        # Load prompt template
        self.prompt_template = self._load_enhanced_prompt_template()
        
        # Backward compatibility attributes
        self.model = config.model if config else "vertex_ai/gemini-2.5-pro"
        self.enhanced_mode = True
        self.analysis_model = None
        self.synthesis_model = self.model

    def execute(self, run_context: RunContext) -> AgentResult:
        """
        V2 StandardAgent execute method.
        
        Args:
            run_context: The RunContext object containing all necessary data
            
        Returns:
            AgentResult containing synthesis results and artifact hash
        """
        self.logger.info(f"Starting {self.agent_name} synthesis for experiment_id: {run_context.experiment_id}")
        
        try:
            # Validate required inputs from RunContext
            if not self._validate_run_context(run_context):
                return AgentResult(
                    success=False,
                    artifacts=[],
                    metadata={},
                    error_message="RunContext missing required synthesis inputs"
                )
            
            # Extract synthesis inputs from RunContext
            synthesis_inputs = self._extract_synthesis_inputs(run_context)
            
            # Generate the synthesis report
            self.logger.info("Generating synthesis report...")
            synthesis_result = self._generate_synthesis_report(synthesis_inputs)
            
            # Store synthesis results
            self.logger.info("Storing synthesis results...")
            synthesis_artifact_hash = self._store_synthesis_results(synthesis_result, run_context)
            
            # Update RunContext with new synthesis artifact
            run_context.add_artifact("synthesis", "synthesis_report", synthesis_artifact_hash)
            run_context.synthesis_results = synthesis_result
            run_context.metadata["latest_synthesis_hash"] = synthesis_artifact_hash
            
            # Log completion
            self.audit.log_agent_event(
                self.agent_name,
                "synthesis_complete",
                {
                    "report_length": len(synthesis_result.get('final_report', '')),
                    "synthesis_artifact_hash": synthesis_artifact_hash,
                    "framework": synthesis_inputs.get('framework_name', 'Unknown')
                }
            )
            
            return AgentResult(
                success=True,
                artifacts=[{"type": "synthesis_report", "hash": synthesis_artifact_hash}],
                metadata={
                    "framework": synthesis_inputs.get('framework_name', 'Unknown'),
                    "report_length": len(synthesis_result.get('final_report', '')),
                    "synthesis_result": synthesis_result
                }
            )
            
        except Exception as e:
            self.logger.error(f"{self.agent_name} synthesis failed: {e}", exc_info=True)
            self.audit.log_error(
                "synthesis_failed",
                str(e),
                {"agent": self.agent_name, "experiment_id": run_context.experiment_id}
            )
            return AgentResult(success=False, artifacts=[], metadata={}, error_message=f"Synthesis failed: {e}")

    def synthesize(self, source_data: Dict[str, Any], **kwargs) -> AgentResult:
        """
        SynthesisAgent synthesize method.
        
        Args:
            source_data: Data to synthesize
            **kwargs: Additional synthesis parameters
            
        Returns:
            AgentResult with synthesis results
        """
        # Create a minimal RunContext for synthesis
        run_context = RunContext(
            experiment_id=kwargs.get('run_id', 'synthesis_only'),
            framework_path=kwargs.get('framework_path', '/test/framework.yaml'),
            corpus_path=kwargs.get('corpus_path', '/test/corpus')
        )
        
        # Populate RunContext with source data
        run_context.analysis_results = source_data.get('analysis_results', {})
        run_context.derived_metrics = source_data.get('derived_metrics', {})
        run_context.evidence = source_data.get('evidence', [])
        run_context.statistical_results = source_data.get('statistical_results', {})
        run_context.metadata.update(source_data.get('metadata', {}))
        
        return self.execute(run_context)

    def get_capabilities(self) -> List[str]:
        """Get agent capabilities"""
        return super().get_capabilities() + [
            "academic_report_generation",
            "evidence_integration",
            "statistical_synthesis",
            "multi_audience_synthesis",
            "tool_calling",
            "structured_output"
        ]

    def get_required_inputs(self) -> List[str]:
        """Get required input parameters"""
        return [
            "analysis_results",
            "statistical_results", 
            "framework_path",
            "experiment_path"
        ]

    def get_optional_inputs(self) -> List[str]:
        """Get optional input parameters"""
        return [
            "evidence",
            "derived_metrics",
            "computational_work",
            "verification_results"
        ]

    def _validate_run_context(self, run_context: RunContext) -> bool:
        """Validate that RunContext contains required synthesis inputs."""
        required_fields = [
            'analysis_results',
            'statistical_results',
            'metadata'
        ]
        
        for field in required_fields:
            if not hasattr(run_context, field) or not getattr(run_context, field):
                self.logger.error(f"RunContext missing required field: {field}")
                return False
        
        # Check for framework and corpus paths
        if not run_context.framework_path:
            self.logger.error("RunContext missing framework_path")
            return False
            
        if not run_context.corpus_path:
            self.logger.error("RunContext missing corpus_path")
            return False
        
        return True

    def _extract_synthesis_inputs(self, run_context: RunContext) -> Dict[str, Any]:
        """Extract synthesis inputs from RunContext."""
        return {
            'analysis_results': run_context.analysis_results,
            'statistical_results': run_context.statistical_results,
            'evidence': run_context.evidence,
            'derived_metrics': run_context.derived_metrics,
            'framework_path': run_context.framework_path,
            'corpus_path': run_context.corpus_path,
            'experiment_path': run_context.metadata.get('experiment_path', f"{run_context.corpus_path}/experiment.md"),
            'framework_name': Path(run_context.framework_path).name,
            'experiment_name': run_context.experiment_id,
            'run_id': run_context.experiment_id,
            'computational_work': run_context.metadata.get('computational_work', {}),
            'verification_results': run_context.metadata.get('verification_results', [])
        }

    def _generate_synthesis_report(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the synthesis report using V2 native formats."""
        try:
            # Load framework and experiment content
            framework_content = self._load_framework_content(inputs['framework_path'])
            experiment_content = self._load_experiment_content(inputs['experiment_path'])
            
            # Prepare research data from V2 native formats
            research_data_context = self._prepare_research_data_context(inputs)
            
            # Prepare evidence context from V2 evidence format
            evidence_context = self._prepare_evidence_context(inputs['evidence'])
            
            # Prepare computational work context
            computational_context = self._prepare_computational_context(inputs.get('computational_work', {}))
            
            # Prepare verification context
            verification_context = self._prepare_verification_context(inputs.get('verification_results', []))
            
            # Assemble experiment metadata
            experiment_metadata = self._assemble_experiment_metadata(inputs)
            
            # Load corpus manifest
            corpus_manifest = self._load_corpus_manifest(inputs['corpus_path'])
            
            # Assemble prompt using template
            base_prompt = self.prompt_template['template'].format(
                experiment_metadata=experiment_metadata,
                framework_content=framework_content,
                experiment_content=experiment_content,
                corpus_manifest=corpus_manifest,
                research_data=research_data_context,
                evidence_context=evidence_context,
                computational_context=computational_context,
                verification_context=verification_context
            )
            
            # Execute LLM call
            final_report, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=base_prompt,
                temperature=0.2,
                context="Generating comprehensive research report"
            )
            
            # Log cost information
            if metadata.get("usage"):
                self._log_synthesis_cost(metadata)
            
            return {
                "final_report": final_report,
                "llm_metadata": metadata,
                "synthesis_inputs": inputs
            }
            
        except Exception as e:
            self.logger.error(f"Synthesis report generation failed: {e}", exc_info=True)
            raise

    def _load_framework_content(self, framework_path: str) -> str:
        """Load framework content from file."""
        try:
            path = Path(framework_path)
            if not path.exists():
                raise FileNotFoundError(f"Framework file not found: {framework_path}")
            return path.read_text(encoding='utf-8')
        except Exception as e:
            self.logger.error(f"Failed to load framework content: {e}")
            raise

    def _load_experiment_content(self, experiment_path: str) -> str:
        """Load experiment content from file."""
        try:
            path = Path(experiment_path)
            if not path.exists():
                raise FileNotFoundError(f"Experiment file not found: {experiment_path}")
            return path.read_text(encoding='utf-8')
        except Exception as e:
            self.logger.error(f"Failed to load experiment content: {e}")
            raise

    def _prepare_research_data_context(self, inputs: Dict[str, Any]) -> str:
        """Prepare research data context from V2 native formats."""
        # Combine analysis results and statistical results
        research_data = {
            "analysis_results": inputs['analysis_results'],
            "statistical_results": inputs['statistical_results'],
            "derived_metrics": inputs.get('derived_metrics', {})
        }
        
        # Convert to safe representation for LLM
        safe_research_data = self._convert_tuple_keys_for_repr(research_data)
        research_data_repr = repr(safe_research_data)
        
        return f"Complete Research Data:\n{research_data_repr}"

    def _prepare_evidence_context(self, evidence: List[Dict[str, Any]]) -> str:
        """Prepare evidence context from V2 evidence format."""
        if not evidence:
            return "⚠️ **EVIDENCE STATUS**: No evidence available for synthesis."
        
        evidence_lines = [
            "🔍 **EVIDENCE AVAILABLE FOR SYNTHESIS**",
            f"Found {len(evidence)} evidence pieces.",
            "",
            "📋 **EVIDENCE CITATION REQUIREMENTS**:",
            "- Every major statistical claim MUST be supported by evidence",
            "- Use format: 'As [Speaker] stated: \"[exact quote]\" (Source: [document_name])'",
            "- Include speaker identification and source document for every quote",
            "- Weave evidence quotes naturally into your analysis",
            ""
        ]
        
        # Add evidence pieces
        for i, evidence_piece in enumerate(evidence[:10]):  # Limit to first 10
            quote_text = evidence_piece.get('quote_text', '')
            if quote_text and quote_text.strip():
                display_quote = quote_text[:200] + ('...' if len(quote_text) > 200 else '')
                evidence_lines.append(f"📝 Evidence {i+1}: \"{display_quote}\"")
                evidence_lines.append(f"   Source: {evidence_piece.get('document_name', 'Unknown')} | Confidence: {evidence_piece.get('confidence', 0.0):.2f}")
                evidence_lines.append("")
        
        return "\n".join(evidence_lines)

    def _prepare_computational_context(self, computational_work: Dict[str, Any]) -> str:
        """Prepare computational work context."""
        if not computational_work:
            return "No computational work available for synthesis."
        
        return f"Computational Work:\n{json.dumps(computational_work, indent=2)}"

    def _prepare_verification_context(self, verification_results: List[Dict[str, Any]]) -> str:
        """Prepare verification results context."""
        if not verification_results:
            return "No verification results available for synthesis."
        
        verified_count = sum(1 for result in verification_results if result.get('verified', False))
        total_count = len(verification_results)
        
        return f"Verification Results: {verified_count}/{total_count} verified\n{json.dumps(verification_results, indent=2)}"

    def _assemble_experiment_metadata(self, inputs: Dict[str, Any]) -> str:
        """Assemble experiment metadata."""
        return f"""
        Experiment: {inputs['experiment_name']}
        Run ID: {inputs['run_id']}
        Framework: {inputs['framework_name']}
        Analysis Model: {self.analysis_model or 'Unknown'}
        Synthesis Model: {self.synthesis_model}
        Document Count: {len(inputs['analysis_results'].get('documents', []))}
        Evidence Count: {len(inputs['evidence'])}
        """

    def _load_corpus_manifest(self, corpus_path: str) -> str:
        """Load corpus manifest."""
        try:
            path = Path(corpus_path)
            if path.exists():
                return path.read_text(encoding='utf-8')
            return "Corpus manifest not available"
        except Exception as e:
            self.logger.warning(f"Failed to load corpus manifest: {e}")
            return "Corpus manifest not available"

    def _convert_tuple_keys_for_repr(self, obj):
        """Convert tuple keys to strings for safe repr() serialization."""
        if isinstance(obj, dict):
            converted = {}
            for k, v in obj.items():
                if isinstance(k, tuple):
                    converted_key = str(k)
                else:
                    converted_key = k
                converted[converted_key] = self._convert_tuple_keys_for_repr(v)
            return converted
        elif isinstance(obj, list):
            return [self._convert_tuple_keys_for_repr(item) for item in obj]
        elif isinstance(obj, tuple):
            return tuple(self._convert_tuple_keys_for_repr(item) for item in obj)
        else:
            return obj

    def _load_enhanced_prompt_template(self) -> Dict[str, Any]:
        """Load enhanced synthesis prompt template."""
        try:
            prompt_file = Path(__file__).parent / "prompt.yaml"
            if prompt_file.exists():
                with open(prompt_file, 'r') as f:
                    return yaml.safe_load(f)
            else:
                # Fallback to basic template
                return self._get_basic_prompt_template()
        except Exception as e:
            self.logger.warning(f"Failed to load enhanced prompt template: {e}")
            return self._get_basic_prompt_template()

    def _get_basic_prompt_template(self) -> Dict[str, Any]:
        """Get basic synthesis prompt template."""
        return {
            "template": """
You are an expert academic synthesis agent. Generate a comprehensive research report using the provided data.

Experiment Metadata:
{experiment_metadata}

Framework Specification:
{framework_content}

Experiment Specification:
{experiment_content}

Corpus Manifest:
{corpus_manifest}

Research Data:
{research_data}

Evidence Context:
{evidence_context}

Computational Context:
{computational_context}

Verification Context:
{verification_context}

Generate a comprehensive academic report that synthesizes all available information.
"""
        }

    def _log_synthesis_cost(self, metadata: Dict[str, Any]):
        """Log synthesis cost information."""
        try:
            usage_data = metadata.get("usage", {})
            self.audit.log_cost(
                operation="synthesis_report_generation",
                model=metadata.get("model", self.model),
                tokens_used=usage_data.get("total_tokens", 0),
                cost_usd=usage_data.get("response_cost_usd", 0.0),
                agent_name=self.agent_name,
                metadata={
                    "prompt_tokens": usage_data.get("prompt_tokens", 0),
                    "completion_tokens": usage_data.get("completion_tokens", 0),
                    "attempts": metadata.get("attempts", 1)
                }
            )
        except Exception as e:
            self.logger.warning(f"Failed to log synthesis cost: {e}")

    def _store_synthesis_results(self, synthesis_result: Dict[str, Any], run_context: RunContext) -> str:
        """Store synthesis results as a structured artifact."""
        timestamp = datetime.now().isoformat()
        artifact_data = {
            "agent_name": self.agent_name,
            "timestamp": timestamp,
            "experiment_id": run_context.experiment_id,
            "synthesis_result": synthesis_result,
            "summary": f"Generated synthesis report with {len(synthesis_result.get('final_report', ''))} characters"
        }
        
        # Store as JSON artifact
        artifact_content = json.dumps(artifact_data, indent=2).encode('utf-8')
        artifact_hash = self.storage.store_artifact(
            content=artifact_content,
            artifact_type="synthesis_report_v2",
            metadata={
                "agent": self.agent_name,
                "timestamp": timestamp,
                "experiment_id": run_context.experiment_id,
                "report_length": len(synthesis_result.get('final_report', ''))
            }
        )
        
        self.logger.info(f"Stored synthesis results as artifact: {artifact_hash}")
        return artifact_hash

    @classmethod
    def from_legacy_config(cls, config: Dict[str, Any]) -> 'V2UnifiedSynthesisAgent':
        """
        Create V2UnifiedSynthesisAgent from legacy config for backward compatibility.
        
        Args:
            config: Legacy configuration dictionary
            
        Returns:
            V2UnifiedSynthesisAgent instance
        """
        # Extract parameters from legacy config
        model = config.get('model', 'vertex_ai/gemini-2.5-pro')
        enhanced_mode = config.get('enhanced_mode', True)
        
        # Create V2 dependencies
        security = config.get('security_boundary')
        storage = config.get('artifact_storage')
        audit = config.get('audit_logger')
        
        if security is None or storage is None or audit is None:
            raise ValueError("Legacy config must provide security_boundary, artifact_storage, and audit_logger")
        
        # Create AgentConfig
        agent_config = AgentConfig(
            model=model,
            timeout_seconds=300.0
        )
        
        # Create agent instance
        agent = cls(security, storage, audit, agent_config)
        agent.enhanced_mode = enhanced_mode
        
        return agent
