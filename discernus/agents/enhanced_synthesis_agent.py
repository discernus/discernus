#!/usr/bin/env python3
"""
Enhanced Synthesis Agent for Discernus THIN v2.0
================================================

Enhanced version of SynthesisAgent with:
- Mathematical spot-checking of analysis agent calculations
- Dual-LLM validation for numerical accuracy
- Enhanced synthesis with confidence assessment
- Direct function call interface (bypasses Redis coordination)

Implements the simplified 2-agent pipeline: AnalysisAgent → SynthesisAgent
"""

import json
import base64
import hashlib
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, List, Optional
from litellm import completion

from discernus.core.security_boundary import ExperimentSecurityBoundary, SecurityError
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage


class EnhancedSynthesisAgentError(Exception):
    """Enhanced synthesis agent specific exceptions"""
    pass


class EnhancedSynthesisAgent:
    """
    Enhanced synthesis agent with mathematical spot-checking capabilities.
    
    Key enhancements over original SynthesisAgent:
    - Mathematical spot-checking of analysis results
    - Dual-LLM validation for numerical accuracy
    - Enhanced synthesis with confidence assessment
    - Direct function call interface (no Redis)
    - Comprehensive error detection and reporting
    """
    
    def __init__(self, 
                 security_boundary: ExperimentSecurityBoundary,
                 audit_logger: AuditLogger,
                 artifact_storage: LocalArtifactStorage):
        """
        Initialize enhanced synthesis agent.
        
        Args:
            security_boundary: Security boundary for file access
            audit_logger: Audit logger for comprehensive logging
            artifact_storage: Local artifact storage for caching
        """
        self.security = security_boundary
        self.audit = audit_logger
        self.storage = artifact_storage
        self.agent_name = "EnhancedSynthesisAgent"
        
        # Load enhanced prompt template
        self.synthesis_prompt_template = self._load_synthesis_prompt_template()
        self.validation_prompt_template = self._load_validation_prompt_template()
        
        print(f"🧠 {self.agent_name} initialized with mathematical spot-checking")
        
        self.audit.log_agent_event(self.agent_name, "initialization", {
            "security_boundary": self.security.get_boundary_info(),
            "capabilities": ["mathematical_spot_checking", "dual_llm_validation", "synthesis", "direct_calls"]
        })
    
    def _load_synthesis_prompt_template(self) -> str:
        """Load enhanced synthesis prompt template."""
        return """You are an enhanced computational research synthesis agent with mathematical validation capabilities. Your task is to synthesize analysis results while VALIDATING mathematical accuracy.

CRITICAL MATHEMATICAL VALIDATION REQUIREMENTS:
1. SPOT-CHECK all numerical calculations from the analysis results
2. Recalculate key mathematical operations independently  
3. Flag any mathematical discrepancies or concerns
4. Provide confidence assessment for numerical results
5. Generate mathematical validation notes for the final report

ENHANCED SYNTHESIS INSTRUCTIONS:
1. FIRST: Review the analysis results and identify all numerical calculations
2. MATHEMATICAL SPOT-CHECKING: Independently verify key calculations:
   - Recalculate sample scores using the stated methodology
   - Verify statistical operations (averages, aggregations)
   - Check that scores fall within expected framework ranges
   - Validate any confidence estimates provided
3. SYNTHESIS: Create comprehensive synthesis incorporating:
   - Analysis results with mathematical validation notes
   - Cross-document patterns and trends
   - Statistical summaries with verified calculations
   - Quality assessment including mathematical confidence
4. MATHEMATICAL CONFIDENCE ASSESSMENT: Provide overall confidence in numerical results

MATHEMATICAL VALIDATION SECTION (Required):
Include a section called "MATHEMATICAL VALIDATION REPORT" that contains:
- Summary of spot-check results
- Any discrepancies or concerns identified
- Independent recalculation of key metrics
- Overall mathematical confidence assessment (0.0-1.0)
- Recommendations for mathematical improvements

OUTPUT FORMAT:
Provide a comprehensive synthesis report with:
1. Executive summary of findings
2. Synthesized analysis results with validation notes
3. Mathematical validation report
4. Final assessment with confidence metrics

---
**SYNTHESIS ID:** {synthesis_id}
**ANALYSIS RESULTS TO SYNTHESIZE:** {num_analyses}
**MATHEMATICAL VALIDATION:** ENABLED

---
**ANALYSIS RESULTS:**
{analysis_results}

Begin enhanced synthesis with mathematical validation now.

QUALITY REQUIREMENTS:
- Validate ALL numerical calculations independently
- Flag any mathematical inconsistencies or errors
- Provide confidence estimates for synthesized results
- Include mathematical validation report
- Generate actionable recommendations for improvements
- Maintain scientific rigor in all assessments
"""

    def _load_validation_prompt_template(self) -> str:
        """Load mathematical validation prompt template."""
        return """You are a mathematical validation specialist. Your ONLY task is to verify the mathematical accuracy of analysis results.

MATHEMATICAL VALIDATION INSTRUCTIONS:
1. Extract all numerical calculations from the analysis results
2. Independently recalculate key metrics using the stated methodologies
3. Verify statistical operations and formulas
4. Check that all scores fall within expected ranges
5. Identify any mathematical errors or inconsistencies

VALIDATION FOCUS AREAS:
- Scoring calculations (verify formulas and arithmetic)
- Statistical operations (averages, aggregations, etc.)
- Range validation (scores within framework bounds)
- Consistency checking (internal mathematical coherence)
- Confidence estimate validation

OUTPUT FORMAT:
Provide a structured mathematical validation report:
1. CALCULATIONS VERIFIED: List of calculations checked
2. MATHEMATICAL ERRORS: Any errors or inconsistencies found
3. CONFIDENCE ASSESSMENT: Mathematical confidence level (0.0-1.0)
4. RECOMMENDATIONS: Suggestions for mathematical improvements

---
**VALIDATION ID:** {validation_id}
**ANALYSIS TO VALIDATE:** {analysis_summary}

---
**ANALYSIS RESULTS:**
{analysis_content}

Begin mathematical validation now.
"""

    def synthesize_results(self, 
                          analysis_results: List[Dict[str, Any]],
                          experiment_config: Dict[str, Any],
                          model: str = "vertex_ai/gemini-2.5-flash") -> Dict[str, Any]:
        """
        Perform enhanced synthesis with mathematical spot-checking.
        
        Args:
            analysis_results: List of analysis result dictionaries
            experiment_config: Experiment configuration
            model: LLM model to use
            
        Returns:
            Synthesis results with mathematical validation
        """
        start_time = datetime.now(timezone.utc).isoformat()
        synthesis_id = f"synthesis_{hashlib.sha256(f'{start_time}{len(analysis_results)}'.encode()).hexdigest()[:12]}"
        
        self.audit.log_agent_event(self.agent_name, "synthesis_start", {
            "synthesis_id": synthesis_id,
            "num_analyses": len(analysis_results),
            "model": model,
            "experiment": experiment_config.get("name", "unknown")
        })
        
        try:
            # Store input analysis artifacts and prepare for synthesis
            analysis_hashes = []
            analysis_content_for_llm = []
            
            for i, result in enumerate(analysis_results):
                # Store analysis result as artifact
                analysis_hash = self.storage.put_artifact(
                    json.dumps(result, indent=2).encode('utf-8'),
                    {"artifact_type": "analysis_input", "synthesis_id": synthesis_id}
                )
                analysis_hashes.append(analysis_hash)
                
                # Prepare content for LLM synthesis
                analysis_content_for_llm.append(f"""
=== ANALYSIS RESULT {i+1} ===
Batch ID: {result.get('batch_id', 'unknown')}
Agent: {result.get('agent_name', 'unknown')}
Model: {result.get('model_used', 'unknown')}

{result.get('analysis_results', 'No analysis content available')}
""")
            
            # Step 1: Mathematical Validation (separate LLM call for focused validation)
            validation_results = self._perform_mathematical_validation(
                analysis_results, synthesis_id, model
            )
            
            # Step 2: Enhanced Synthesis (incorporating validation results)
            synthesis_results = self._perform_enhanced_synthesis(
                analysis_results, validation_results, synthesis_id, model, analysis_content_for_llm
            )
            
            # Create comprehensive result artifact
            end_time = datetime.now(timezone.utc).isoformat()
            duration = self._calculate_duration(start_time, end_time)
            
            enhanced_synthesis = {
                "synthesis_id": synthesis_id,
                "agent_name": self.agent_name,
                "agent_version": "enhanced_v2.0_mathematical",
                "experiment_name": experiment_config.get("name", "unknown"),
                "model_used": model,
                "synthesis_results": synthesis_results,
                "mathematical_validation": validation_results,
                "execution_metadata": {
                    "start_time": start_time,
                    "end_time": end_time,
                    "duration_seconds": duration,
                    "validation_enabled": True,
                    "dual_llm_validation": True
                },
                "input_artifacts": {
                    "analysis_hashes": analysis_hashes,
                    "num_analyses": len(analysis_results)
                },
                "provenance": {
                    "security_boundary": self.security.get_boundary_info(),
                    "audit_session_id": self.audit.session_id
                }
            }
            
            # Store synthesis result artifact
            result_hash = self.storage.put_artifact(
                json.dumps(enhanced_synthesis, indent=2).encode('utf-8'),
                {"artifact_type": "synthesis_result", "synthesis_id": synthesis_id}
            )
            
            # Log artifact transformation
            self.audit.log_artifact_chain(
                stage="enhanced_synthesis",
                input_hashes=analysis_hashes,
                output_hash=result_hash,
                agent_name=self.agent_name
            )
            
            # Log completion
            self.audit.log_agent_event(self.agent_name, "synthesis_complete", {
                "synthesis_id": synthesis_id,
                "result_hash": result_hash,
                "duration_seconds": duration,
                "mathematical_validation": "completed",
                "validation_confidence": validation_results.get("confidence", 0.0)
            })
            
            print(f"✅ Enhanced synthesis complete: {synthesis_id} ({duration:.1f}s)")
            
            return {
                "synthesis_id": synthesis_id,
                "result_hash": result_hash,
                "result_content": enhanced_synthesis,
                "duration_seconds": duration,
                "mathematical_validation": validation_results,
                "synthesis_confidence": validation_results.get("confidence", 0.0)
            }
            
        except Exception as e:
            # Log error
            self.audit.log_error("enhanced_synthesis_error", str(e), {
                "synthesis_id": synthesis_id,
                "agent_name": self.agent_name
            })
            
            raise EnhancedSynthesisAgentError(f"Enhanced synthesis failed: {e}")
    
    def _perform_mathematical_validation(self, 
                                       analysis_results: List[Dict[str, Any]], 
                                       synthesis_id: str, 
                                       model: str) -> Dict[str, Any]:
        """Perform dedicated mathematical validation of analysis results."""
        validation_id = f"validation_{synthesis_id}"
        
        self.audit.log_agent_event(self.agent_name, "mathematical_validation_start", {
            "validation_id": validation_id,
            "num_analyses": len(analysis_results)
        })
        
        # Prepare analysis content for validation
        analysis_summary = f"{len(analysis_results)} analysis results requiring mathematical validation"
        analysis_content = "\n\n".join([
            f"=== ANALYSIS {i+1} ===\n{result.get('analysis_results', '')}"
            for i, result in enumerate(analysis_results)
        ])
        
        # Format validation prompt
        validation_prompt = self.validation_prompt_template.format(
            validation_id=validation_id,
            analysis_summary=analysis_summary,
            analysis_content=analysis_content
        )
        
        # Call LLM for mathematical validation
        response = completion(
            model=model,
            messages=[{"role": "user", "content": validation_prompt}],
            temperature=0.0,
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        )
        
        validation_content = response.choices[0].message.content
        
        # Log validation interaction
        validation_interaction_hash = self.audit.log_llm_interaction(
            model=model,
            prompt=validation_prompt,
            response=validation_content,
            agent_name=self.agent_name,
            interaction_type="mathematical_validation",
            metadata={
                "validation_id": validation_id,
                "analysis_count": len(analysis_results)
            }
        )
        
        return {
            "validation_id": validation_id,
            "validation_content": validation_content,
            "validation_interaction_hash": validation_interaction_hash,
            "confidence": self._extract_confidence_from_validation(validation_content),
            "mathematical_errors_found": self._extract_errors_from_validation(validation_content)
        }
    
    def _perform_enhanced_synthesis(self, 
                                  analysis_results: List[Dict[str, Any]], 
                                  validation_results: Dict[str, Any],
                                  synthesis_id: str, 
                                  model: str,
                                  analysis_content_for_llm: List[str]) -> str:
        """Perform enhanced synthesis incorporating validation results."""
        
        # Format synthesis prompt with validation results
        synthesis_prompt = self.synthesis_prompt_template.format(
            synthesis_id=synthesis_id,
            num_analyses=len(analysis_results),
            analysis_results="\n".join(analysis_content_for_llm) + 
                           f"\n\n=== MATHEMATICAL VALIDATION RESULTS ===\n{validation_results['validation_content']}"
        )
        
        # Call LLM for synthesis
        response = completion(
            model=model,
            messages=[{"role": "user", "content": synthesis_prompt}],
            temperature=0.0,
            safety_settings=[
                {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
                {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"}
            ]
        )
        
        synthesis_content = response.choices[0].message.content
        
        # Log synthesis interaction
        synthesis_interaction_hash = self.audit.log_llm_interaction(
            model=model,
            prompt=synthesis_prompt,
            response=synthesis_content,
            agent_name=self.agent_name,
            interaction_type="enhanced_synthesis",
            metadata={
                "synthesis_id": synthesis_id,
                "includes_validation": True,
                "validation_confidence": validation_results.get("confidence", 0.0)
            }
        )
        
        return synthesis_content
    
    def _extract_confidence_from_validation(self, validation_content: str) -> float:
        """Extract confidence score from validation content."""
        # Simple pattern matching for confidence scores
        import re
        confidence_patterns = [
            r"confidence.*?(\d+\.?\d*)",
            r"(\d+\.?\d*).*confidence",
            r"mathematical confidence.*?(\d+\.?\d*)"
        ]
        
        for pattern in confidence_patterns:
            matches = re.findall(pattern, validation_content.lower())
            if matches:
                try:
                    confidence = float(matches[0])
                    return min(1.0, max(0.0, confidence))  # Clamp to [0.0, 1.0]
                except:
                    continue
        
        return 0.8  # Default moderate confidence if not found
    
    def _extract_errors_from_validation(self, validation_content: str) -> List[str]:
        """Extract mathematical errors from validation content."""
        errors = []
        error_indicators = ["error", "incorrect", "wrong", "mistake", "discrepancy"]
        
        lines = validation_content.split('\n')
        for line in lines:
            line_lower = line.lower()
            if any(indicator in line_lower for indicator in error_indicators):
                errors.append(line.strip())
        
        return errors
    
    def _calculate_duration(self, start: str, end: str) -> float:
        """Calculate duration between timestamps in seconds."""
        try:
            start_dt = datetime.fromisoformat(start.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end.replace('Z', '+00:00'))
            return (end_dt - start_dt).total_seconds()
        except Exception:
            return 0.0 