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
from ...gateway.llm_gateway_enhanced import EnhancedLLMGateway
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
        self.llm_gateway = EnhancedLLMGateway(get_model_registry())
        
        # Load prompt template
        self.prompt_template = self._load_enhanced_prompt_template()
        
        # Backward compatibility attributes
        self.model = config.model if config else "vertex_ai/gemini-2.5-pro"
        self.enhanced_mode = True
        self.analysis_model = None
        self.synthesis_model = self.model

    def execute(self, run_context: RunContext, **kwargs) -> AgentResult:
        """
        V2 StandardAgent execute method.
        
        Args:
            run_context: The RunContext object containing all necessary data
            
        Returns:
            AgentResult containing synthesis results and artifact hash
        """
        self.logger.info(f"Starting {self.agent_name} synthesis for experiment_id: {run_context.experiment_id}")
        
        try:
            self.log_execution_start(run_context=run_context, **kwargs)

            # 1. Validate and extract necessary data from RunContext
            synthesis_inputs = self._validate_and_extract_inputs(run_context)

            # 2. Generate the synthesis report by calling the LLM
            self.logger.info("Generating synthesis report...")
            synthesis_result = self._generate_synthesis_report(synthesis_inputs)

            # 3. Store the synthesis report as a persistent artifact
            self.logger.info("Storing synthesis results...")
            synthesis_artifact_hash = self._store_synthesis_results(synthesis_result, run_context)

            # 4. Update the RunContext with the results
            run_context.synthesis_results = synthesis_result
            run_context.add_artifact("synthesis", synthesis_artifact_hash, synthesis_artifact_hash)
            run_context.metadata["latest_synthesis_hash"] = synthesis_artifact_hash
            
            # 5. Log completion and return the result
            result = AgentResult(
                success=True,
                artifacts=[synthesis_artifact_hash],
                metadata={
                    "report_length": len(synthesis_result.get('final_report', '')),
                    "synthesis_artifact_hash": synthesis_artifact_hash,
                }
            )
            self.log_execution_complete(result)
            return result

        except Exception as e:
            self.logger.error(f"{self.agent_name} synthesis failed: {e}", exc_info=True)
            self.log_execution_error(e)
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
            "framework_content",
            "corpus_documents"
        ]

    def get_optional_inputs(self) -> List[str]:
        """Get optional input parameters"""
        return [
            "evidence",
            "derived_metrics",
            "computational_work",
            "verification_results"
        ]

    def _validate_and_extract_inputs(self, run_context: RunContext) -> Dict[str, Any]:
        """Validate RunContext and extract all necessary data for synthesis."""
        if not run_context:
            raise ValueError("RunContext is required.")

        inputs = {}
        required_fields = [
            "analysis_results", "statistical_results"
        ]
        for field in required_fields:
            if not getattr(run_context, field):
                raise ValueError(f"RunContext is missing required field: {field}")
            inputs[field] = getattr(run_context, field)

        required_metadata = ["framework_content"]
        for meta_field in required_metadata:
            if meta_field not in run_context.metadata:
                raise ValueError(f"RunContext metadata is missing required field: {meta_field}")
            inputs[meta_field] = run_context.metadata[meta_field]
            
        # Optional fields
        inputs['evidence'] = run_context.evidence or []
        inputs['derived_metrics'] = run_context.derived_metrics or {}
        inputs['computational_work'] = run_context.metadata.get('computational_work', {})
        inputs['verification_results'] = run_context.metadata.get('verification_results', [])
        
        # Experiment info
        inputs['experiment_name'] = run_context.experiment_id
        inputs['framework_name'] = Path(run_context.framework_path).name

        # Load experiment content from the standard file path
        experiment_file_path = Path(run_context.corpus_path).parent / 'experiment.md'
        if experiment_file_path.exists():
            inputs['experiment_content'] = experiment_file_path.read_text(encoding='utf-8')
        else:
            inputs['experiment_content'] = "No experiment content file found."

        # The orchestrator should have loaded this already
        inputs['corpus_manifest_content'] = run_context.metadata.get("corpus_manifest_content", "No corpus manifest content found.")

        return inputs

    def _generate_synthesis_report(self, inputs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate the synthesis report using V2 native formats."""
        try:
            # Prepare all data contexts by serializing them to JSON for the LLM
            research_data_context = self._prepare_research_data_context(inputs)
            evidence_context = self._prepare_evidence_context(inputs['evidence'])
            computational_context = self._prepare_computational_context(inputs.get('computational_work', {}))
            verification_context = self._prepare_verification_context(inputs.get('verification_results', []))
            experiment_metadata = self._assemble_experiment_metadata(inputs)

            # Assemble prompt using template
            base_prompt = self.prompt_template['template'].format(
                experiment_metadata=json.dumps(experiment_metadata, indent=2),
                framework_content=inputs['framework_content'],
                experiment_content=inputs['experiment_content'],
                corpus_manifest=inputs['corpus_manifest_content'],
                research_data=json.dumps(research_data_context, indent=2),
                evidence_context=json.dumps(evidence_context, indent=2),
                computational_context=json.dumps(computational_context, indent=2),
                verification_context=json.dumps(verification_context, indent=2)
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
            }

        except Exception as e:
            self.logger.error(f"Synthesis report generation failed: {e}", exc_info=True)
            raise

    def _prepare_research_data_context(self, inputs: Dict[str, Any]) -> Dict:
        """Prepare research data context by combining relevant data."""
        # Only include statistical results and derived metrics - NOT composite analysis data
        # Composite analysis contains full transcripts and markup which consume too many tokens
        return {
            "statistical_results": inputs['statistical_results'],
            "derived_metrics": inputs.get('derived_metrics', {})
        }

    def _prepare_evidence_context(self, evidence: List[Dict[str, Any]]) -> Dict:
        """Prepare evidence context, providing raw data for the LLM."""
        if not evidence:
            return {"status": "No evidence available for synthesis."}
        
        return {
            "status": f"Evidence available. Found {len(evidence)} findings.",
            "evidence_payload": evidence
        }

    def _prepare_computational_context(self, computational_work: Dict[str, Any]) -> Dict:
        """Prepare computational work context."""
        if not computational_work:
            return {"status": "No computational work available for synthesis."}
        return computational_work

    def _prepare_verification_context(self, verification_results: List[Dict[str, Any]]) -> Dict:
        """Prepare verification results context."""
        if not verification_results:
            return {"status": "No verification results available for synthesis."}

        verified_count = sum(1 for result in verification_results if result.get('verified', False))
        total_count = len(verification_results)
        
        return {
            "status": f"{verified_count}/{total_count} items verified.",
            "verification_payload": verification_results
        }

    def _assemble_experiment_metadata(self, inputs: Dict[str, Any]) -> Dict:
        """Assemble experiment metadata into a dictionary."""
        return {
           "experiment_name": inputs['experiment_name'],
           "framework_name": inputs['framework_name'],
           "synthesis_model": self.synthesis_model,
           "evidence_findings_count": len(inputs.get('evidence', []))
        }

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
You are an expert academic synthesis agent. Your task is to generate a comprehensive, publication-ready research report by synthesizing the provided JSON data objects. Adhere strictly to an academic tone.

### Instructions:
1.  **Synthesize, Do Not Summarize**: Do not simply list the data. Weave the information from all provided JSON objects into a coherent, well-structured academic narrative.
2.  **Cite Evidence**: When making claims based on the `research_data`, you MUST support them with specific quotes from the `evidence_context`. Use parenthetical citations referencing the document ID.
3.  **Structure**: The report should include an introduction, methodology, results, discussion, and conclusion.
4.  **Tone**: Maintain a neutral, objective, and analytical tone throughout.

### Data Payloads (JSON Objects):

**Experiment Metadata:**
```json
{experiment_metadata}
```

**Framework Specification:**
```
{framework_content}
```

**Experiment Specification:**
```
{experiment_content}
```

**Corpus Manifest:**
```
{corpus_manifest}
```

**Research Data (Analysis, Statistics, Metrics):**
```json
{research_data}
```

**Evidence Context (for citation):**
```json
{evidence_context}
```

**Computational Context (optional):**
```json
{computational_context}
```

**Verification Context (optional):**
```json
{verification_context}
```

Begin the report now.
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
        
        # The final report is the markdown content we want to store.
        final_report_content = synthesis_result.get("final_report", "# Synthesis Report Error\n\nNo report content was generated.")
        
        # Store the markdown report directly.
        artifact_content = final_report_content.encode('utf-8')
        artifact_hash = self.storage.put_artifact(
            content=artifact_content,
            metadata={
                "artifact_type": "synthesis_report_v2_markdown",
                "agent": self.agent_name,
                "timestamp": timestamp,
                "experiment_id": run_context.experiment_id,
                "report_length": len(final_report_content),
                "llm_metadata": synthesis_result.get("llm_metadata", {})
            }
        )
        
        self.logger.info(f"Stored synthesis markdown report as artifact: {artifact_hash}")
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
