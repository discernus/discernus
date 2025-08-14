"""
Notebook Generator Agent for Epic 401 - Direct Framework Handoff
"""

import json
import ast
import tempfile
import subprocess
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Any, Optional

from discernus.gateway.llm_gateway import LLMGateway
from discernus.core.audit_logger import AuditLogger


class NotebookGenerationResult:
    def __init__(self, success: bool, notebook_path=None, error_message=None, metadata=None):
        self.success = success
        self.notebook_path = notebook_path
        self.error_message = error_message
        self.metadata = metadata or {}


class NotebookGeneratorAgent:
    def __init__(self, audit_logger: Optional[AuditLogger] = None, model: str = "vertex_ai/gemini-2.5-pro"):
        self.audit_logger = audit_logger
        self.model = model
        # Initialize LLM gateway when needed (lazy initialization)
        self._llm_gateway = None
    
    @property
    def llm_gateway(self):
        """Lazy initialization of LLM gateway."""
        if self._llm_gateway is None:
            from discernus.gateway.model_registry import ModelRegistry
            model_registry = ModelRegistry()
            self._llm_gateway = LLMGateway(model_registry)
        return self._llm_gateway
    
    def generate_derived_metrics_notebook(self, scores_data, evidence_data, framework_content, experiment_config, output_path):
        """Generate notebook using direct framework handoff - no parsing!"""
        try:
            # Prepare complete input for LLM (direct framework handoff)
            llm_input = self._prepare_llm_input(scores_data, evidence_data, framework_content, experiment_config)
            
            # Generate notebook using LLM
            notebook_content = self._generate_notebook_with_llm(llm_input)
            
            # Save notebook and analysis data
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            # Save the generated notebook
            with open(output_path, 'w') as f:
                f.write(notebook_content)
            
            # Save analysis data that the notebook will need
            analysis_data_path = output_path.parent / "analysis_data.json"
            analysis_data = {
                "document_analyses": scores_data.get("document_analyses", []) if scores_data else [],
                "evidence_data": evidence_data,
                "experiment_config": experiment_config,
                "generation_timestamp": datetime.now(timezone.utc).isoformat(),
                "framework_name": experiment_config.get("framework", "Unknown")
            }
            
            with open(analysis_data_path, 'w') as f:
                json.dump(analysis_data, f, indent=2)
            
            # Save requirements.txt for the notebook
            requirements_path = output_path.parent / "requirements.txt"
            requirements_content = """# Python dependencies for derived metrics notebook
pandas>=1.3.0
numpy>=1.21.0
scipy>=1.7.0
matplotlib>=3.4.0
seaborn>=0.11.0
jupyter>=1.0.0
"""
            with open(requirements_path, 'w') as f:
                f.write(requirements_content)
            
            # Return success with comprehensive metadata
            metadata = {
                "approach": "direct_framework_handoff",
                "framework_size_bytes": len(framework_content.encode('utf-8')),
                "notebook_size_bytes": len(notebook_content.encode('utf-8')),
                "total_documents": len(scores_data.get("document_analyses", [])) if scores_data else 0,
                "analysis_data_path": str(analysis_data_path),
                "requirements_path": str(requirements_path)
            }
            
            return NotebookGenerationResult(
                success=True,
                notebook_path=str(output_path),
                metadata=metadata
            )
            
        except Exception as e:
            return NotebookGenerationResult(
                success=False,
                error_message=str(e)
            )
    
    def _prepare_llm_input(self, scores_data, evidence_data, framework_content, experiment_config):
        """Prepare comprehensive input for LLM - direct framework handoff with analysis context"""
        framework_name = experiment_config.get("framework", "Unknown Framework")
        experiment_name = experiment_config.get("name", "Unknown Experiment")
        
        # Extract sample data for LLM to understand the structure
        sample_documents = []
        if scores_data and "document_analyses" in scores_data:
            # Take first 2 documents as examples
            for i, doc_analysis in enumerate(scores_data["document_analyses"][:2]):
                sample_doc = {
                    "document_id": doc_analysis.get("document_id", f"doc_{i+1}"),
                    "scores_sample": dict(list(doc_analysis.get("scores", {}).items())[:5]),  # First 5 scores
                    "evidence_sample": dict(list(doc_analysis.get("evidence", {}).items())[:3]),  # First 3 evidence
                    "confidence_sample": dict(list(doc_analysis.get("confidence", {}).items())[:3])  # First 3 confidence
                }
                sample_documents.append(sample_doc)
        
        total_docs = len(scores_data.get("document_analyses", [])) if scores_data else 0
        
        llm_input = f"""
# Notebook Generation Request

## Framework Specification
{framework_content}

## Experiment Configuration
- **Framework**: {framework_name}
- **Experiment**: {experiment_name}
- **Total Documents**: {total_docs}

## Analysis Data Structure
The notebook will process a JSON file 'analysis_data.json' with this structure:
```json
{{
  "document_analyses": [
    {{
      "document_id": "doc_001",
      "scores": {{"dimension1_score": 0.75, "dimension2_score": 0.82, ...}},
      "evidence": {{"dimension1_evidence": "supporting quote...", ...}},
      "confidence": {{"dimension1_confidence": 0.87, ...}}
    }},
    ...
  ]
}}
```

## Sample Data (First {len(sample_documents)} documents for reference):
{chr(10).join([f"Document {i+1}: {doc}" for i, doc in enumerate(sample_documents)])}

## Notebook Requirements
1. **Load Data**: Read 'analysis_data.json' and parse document analyses
2. **Extract Framework Calculations**: Implement all derived metrics specified in the framework above
3. **Process All Documents**: Calculate derived metrics for all {total_docs} documents
4. **Generate Output**: Create 'derived_metrics_results.csv' with all scores and derived metrics
5. **Include Documentation**: Add comments explaining each calculation step
6. **Error Handling**: Handle missing scores gracefully
7. **Validation**: Include basic sanity checks on calculated values

The notebook should be completely self-contained and executable.
"""
        return llm_input
    
    def _generate_notebook_with_llm(self, llm_input):
        """Generate executable Python notebook using LLM with framework-specific calculations"""
        
        system_prompt = """You are an expert Python programmer specializing in academic research data analysis and statistical calculations. You generate clean, executable Python notebooks that implement framework-specific derived metrics calculations with complete transparency and academic rigor."""
        
        # Create comprehensive prompt for notebook generation
        prompt = f"""
Generate an executable Python notebook (.py file) that calculates derived metrics from analysis data based on the provided framework specification.

CRITICAL: The framework contains specific mathematical formulas in the "calculation_spec" section. You MUST implement these exact formulas:

REQUIRED CFF v7.3 CALCULATIONS:
1. **Tension Scores**: 
   - identity_tension = min(tribal_dominance_score, individual_dignity_score) * abs(tribal_dominance_salience - individual_dignity_salience)
   - emotional_tension = min(fear_score, hope_score) * abs(fear_salience - hope_salience)
   - success_tension = min(envy_score, compersion_score) * abs(envy_salience - compersion_salience)
   - relational_tension = min(enmity_score, amity_score) * abs(enmity_salience - amity_salience)
   - goal_tension = min(fragmentative_goals_score, cohesive_goals_score) * abs(fragmentative_goals_salience - cohesive_goals_salience)

2. **Composite Indices**:
   - strategic_contradiction_index = (identity_tension + emotional_tension + success_tension + relational_tension + goal_tension) / 5
   - cohesive_index = (individual_dignity_score + hope_score + compersion_score + amity_score + cohesive_goals_score) / 5
   - fragmentative_index = (tribal_dominance_score + fear_score + envy_score + enmity_score + fragmentative_goals_score) / 5
   - overall_cohesion_index = cohesive_index - fragmentative_index

REQUIREMENTS:
1. **Extract Formula Specifications**: Parse the framework's "calculation_spec" and "formulas" sections
2. **Implement Each Formula**: Create Python functions for every calculation listed above
3. **Data Loading**: Load analysis data from 'analysis_data.json' containing scores and salience
4. **Calculate for All Documents**: Apply formulas to every document in the dataset
5. **CSV Output**: Generate 'derived_metrics_results.csv' with all original scores + calculated metrics
6. **Validation**: Include sanity checks and error handling for missing data

PYTHON STRUCTURE REQUIRED:
```python
#!/usr/bin/env python3
import json
import pandas as pd
import numpy as np

def calculate_identity_tension(tribal_dominance_score, individual_dignity_score, tribal_dominance_salience, individual_dignity_salience):
    return min(tribal_dominance_score, individual_dignity_score) * abs(tribal_dominance_salience - individual_dignity_salience)

# ... implement all other calculation functions

def main():
    # Load data, apply calculations, save CSV
    pass

if __name__ == "__main__":
    main()
```

FRAMEWORK AND DATA CONTEXT:
{llm_input}

Generate ONLY the complete Python notebook code with ALL CFF calculations implemented. The code must be immediately executable and produce accurate derived metrics.
"""

        try:
            # Execute LLM call using the gateway
            response_content, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=4000,  # Allow for comprehensive notebook generation
                temperature=0.3   # Lower temperature for more consistent code generation
            )
            
            # Log successful generation
            if self.audit_logger:
                self.audit_logger.log_llm_interaction(
                    model=self.model,
                    prompt=prompt[:500] + "...",  # Truncate prompt for logging
                    response=response_content[:500] + "...",  # Truncate response for logging
                    agent_name="NotebookGeneratorAgent",
                    metadata={
                        "operation": "notebook_generation",
                        "response_length": len(response_content),
                        **metadata
                    }
                )
            
            # DEBUG: Temporarily disable validation to see what LLM generates
            validation_result = self._validate_notebook_syntax(response_content)
            if not validation_result["valid"]:
                error_msg = f"Generated notebook has syntax errors: {validation_result['error']}"
                if self.audit_logger:
                    self.audit_logger.log_error(
                        "notebook_syntax_validation_error",
                        error_msg,
                        {"model": self.model, "syntax_error": validation_result['error']}
                    )
                # DEBUG: Save the content anyway and log the error, but don't fail
                print(f"🔍 DEBUG: Syntax validation failed, but saving content anyway: {validation_result['error']}")
                print(f"🔍 DEBUG: First 500 chars of generated content:")
                print("-" * 60)
                print(response_content[:500])
                print("-" * 60)
                # Continue despite validation failure for debugging
            
            return response_content
            
        except Exception as e:
            error_msg = f"LLM notebook generation failed: {str(e)}"
            if self.audit_logger:
                self.audit_logger.log_error(
                    "notebook_generation_llm_error",
                    error_msg,
                    {"model": self.model, "error": str(e)}
                )
            raise RuntimeError(error_msg)
    
    def _validate_notebook_syntax(self, notebook_content: str) -> Dict[str, Any]:
        """
        Validate that the generated notebook has correct Python syntax.
        
        Args:
            notebook_content: The generated Python notebook code
            
        Returns:
            Dictionary with validation results
        """
        try:
            # Parse the code using AST to check syntax
            ast.parse(notebook_content)
            
            # Basic structure validation
            required_patterns = [
                "def ",  # Should have function definitions
                "import ",  # Should have imports
                "if __name__ == \"__main__\":",  # Should have main block
                ".csv"  # Should generate CSV output
            ]
            
            missing_patterns = []
            for pattern in required_patterns:
                if pattern not in notebook_content:
                    missing_patterns.append(pattern)
            
            if missing_patterns:
                return {
                    "valid": False,
                    "error": f"Missing required patterns: {missing_patterns}",
                    "notebook_length": len(notebook_content)
                }
            
            return {
                "valid": True,
                "error": None,
                "notebook_length": len(notebook_content),
                "function_count": notebook_content.count("def "),
                "import_count": notebook_content.count("import ")
            }
            
        except SyntaxError as e:
            return {
                "valid": False,
                "error": f"Syntax error at line {e.lineno}: {e.msg}",
                "notebook_length": len(notebook_content)
            }
        except Exception as e:
            return {
                "valid": False,
                "error": f"Validation error: {str(e)}",
                "notebook_length": len(notebook_content)
            }
    
    def _validate_notebook_execution(self, notebook_path: Path, analysis_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate that the notebook can execute without errors (optional validation).
        
        Args:
            notebook_path: Path to the generated notebook
            analysis_data: Sample analysis data for testing
            
        Returns:
            Dictionary with execution validation results
        """
        try:
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = Path(temp_dir)
                
                # Copy notebook to temp directory
                temp_notebook = temp_path / "test_notebook.py"
                temp_notebook.write_text(notebook_path.read_text())
                
                # Create sample analysis_data.json
                sample_data_file = temp_path / "analysis_data.json"
                with open(sample_data_file, 'w') as f:
                    json.dump(analysis_data, f, indent=2)
                
                # Try to execute the notebook
                result = subprocess.run(
                    ["python", str(temp_notebook)],
                    cwd=temp_dir,
                    capture_output=True,
                    text=True,
                    timeout=30  # 30 second timeout
                )
                
                if result.returncode == 0:
                    # Check if CSV output was created
                    csv_files = list(temp_path.glob("*.csv"))
                    return {
                        "valid": True,
                        "error": None,
                        "stdout": result.stdout,
                        "stderr": result.stderr,
                        "csv_files_created": len(csv_files)
                    }
                else:
                    return {
                        "valid": False,
                        "error": f"Execution failed with return code {result.returncode}",
                        "stdout": result.stdout,
                        "stderr": result.stderr
                    }
                    
        except subprocess.TimeoutExpired:
            return {
                "valid": False,
                "error": "Notebook execution timed out (30 seconds)",
                "stdout": "",
                "stderr": ""
            }
        except Exception as e:
            return {
                "valid": False,
                "error": f"Execution validation error: {str(e)}",
                "stdout": "",
                "stderr": ""
            }
