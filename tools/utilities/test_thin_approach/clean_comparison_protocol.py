#!/usr/bin/env python3
"""
Clean, systematic comparison protocol for show work vs production
All tests use identical PDAF framework and dimensions
"""

import json
import sys
from pathlib import Path
from datetime import datetime, timezone
import re

sys.path.append('/Volumes/code/discernus')
from discernus.core.security_boundary import ExperimentSecurityBoundary
from discernus.core.audit_logger import AuditLogger
from discernus.core.local_artifact_storage import LocalArtifactStorage
from discernus.gateway.llm_gateway_enhanced import EnhancedLLMGateway
from tmp.AnalysisAgent.prompt_builder import create_analysis_prompt

class CleanComparisonProtocol:
    """Systematic comparison with identical frameworks."""
    
    def __init__(self):
        self.experiment_dir = Path("/Volumes/code/discernus/tmp")
        self.test_dir = Path("/Volumes/code/discernus/test_thin_approach")
        
        # Initialize components
        self.security = ExperimentSecurityBoundary(self.experiment_dir)
        self.audit = AuditLogger(self.security, self.experiment_dir / "logs")
        self.storage = LocalArtifactStorage(self.security, self.experiment_dir / "artifacts")
        self.gateway = EnhancedLLMGateway(self.audit)
        
        # Load framework and document
        self.framework_content = self._load_framework()
        self.document_content = self._load_document()
        
    def _load_framework(self):
        """Load the actual PDAF framework."""
        framework_path = self.experiment_dir / "framework" / "pdaf_v10_0_2.md"
        with open(framework_path, 'r') as f:
            return f.read()
    
    def _load_document(self):
        """Load the test document."""
        doc_path = self.experiment_dir / "corpus" / "Trump_SOTU_2020.txt"
        with open(doc_path, 'r') as f:
            return f.read()
    
    def test_show_work_with_pdaf(self):
        """Test show work approach with actual PDAF framework."""
        print("=== TEST 1: SHOW WORK WITH ACTUAL PDAF ===")
        
        # Prepare documents
        documents = [{
            'index': 0,
            'filename': 'Trump_SOTU_2020.txt',
            'hash': 'test_hash',
            'content': self.document_content
        }]
        
        # Create prompt using actual PDAF framework
        prompt_text = create_analysis_prompt(
            self._get_show_work_prompt_template(), 
            "test_show_work", 
            self.framework_content, 
            documents
        )
        
        print(f"Prompt length: {len(prompt_text)} characters")
        print("Executing show work test...")
        
        # Execute LLM call
        response = self.gateway.execute_call(
            model="vertex_ai/gemini-2.5-flash",
            prompt=prompt_text
        )
        
        # Handle response
        if isinstance(response, tuple):
            content, metadata = response
        else:
            content = response.get('content', '')
            metadata = response.get('metadata', {})
        
        # Save results
        result = {
            'test_type': 'show_work_with_pdaf',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'prompt': prompt_text,
            'response': content,
            'metadata': metadata
        }
        
        with open(self.test_dir / "artifacts" / "show_work_pdaf_test.json", 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"Response length: {len(content)} characters")
        print("Results saved to: show_work_pdaf_test.json")
        
        return result
    
    def test_production_mode(self):
        """Test production mode with same framework."""
        print("\n=== TEST 2: PRODUCTION MODE ===")
        
        # Prepare documents
        documents = [{
            'index': 0,
            'filename': 'Trump_SOTU_2020.txt',
            'hash': 'test_hash',
            'content': self.document_content
        }]
        
        # Create prompt using production template
        prompt_text = create_analysis_prompt(
            self._get_production_prompt_template(), 
            "test_production", 
            self.framework_content, 
            documents
        )
        
        print(f"Prompt length: {len(prompt_text)} characters")
        print("Executing production test...")
        
        # Execute LLM call
        response = self.gateway.execute_call(
            model="vertex_ai/gemini-2.5-flash",
            prompt=prompt_text
        )
        
        # Handle response
        if isinstance(response, tuple):
            content, metadata = response
        else:
            content = response.get('content', '')
            metadata = response.get('metadata', {})
        
        # Save results
        result = {
            'test_type': 'production_mode',
            'timestamp': datetime.now(timezone.utc).isoformat(),
            'prompt': prompt_text,
            'response': content,
            'metadata': metadata
        }
        
        with open(self.test_dir / "artifacts" / "production_mode_test.json", 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"Response length: {len(content)} characters")
        print("Results saved to: production_mode_test.json")
        
        return result
    
    def test_production_consistency(self, num_runs=3):
        """Test production mode consistency with multiple runs."""
        print(f"\n=== TEST 3: PRODUCTION CONSISTENCY ({num_runs} runs) ===")
        
        results = []
        
        for i in range(num_runs):
            print(f"Run {i+1}/{num_runs}...")
            
            # Prepare documents
            documents = [{
                'index': 0,
                'filename': 'Trump_SOTU_2020.txt',
                'hash': 'test_hash',
                'content': self.document_content
            }]
            
            # Create prompt using production template
            prompt_text = create_analysis_prompt(
                self._get_production_prompt_template(), 
                f"test_consistency_{i+1}", 
                self.framework_content, 
                documents
            )
            
            # Execute LLM call
            response = self.gateway.execute_call(
                model="vertex_ai/gemini-2.5-flash",
                prompt=prompt_text
            )
            
            # Handle response
            if isinstance(response, tuple):
                content, metadata = response
            else:
                content = response.get('content', '')
                metadata = response.get('metadata', {})
            
            results.append({
                'run': i+1,
                'timestamp': datetime.now(timezone.utc).isoformat(),
                'response': content,
                'metadata': metadata
            })
        
        # Save results
        with open(self.test_dir / "artifacts" / "production_consistency_test.json", 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"Consistency test completed. Results saved to: production_consistency_test.json")
        
        return results
    
    def _get_show_work_prompt_template(self):
        """Get prompt template that asks LLM to show its work."""
        return """You are an expert discourse analyst specializing in dimensional analysis of political and social texts. Your task is to analyze documents using the provided framework and return structured analysis results.

**ANALYSIS REQUIREMENTS:**
- Apply the framework's dimensional definitions precisely
- Score each dimension on a 0.0-1.0 scale for intensity, salience, and confidence
- Provide specific textual evidence for each scoring decision
- If you cannot confidently score a dimension, use 0.0 score with low confidence and provide explanation in evidence

**THREE INDEPENDENT ANALYTICAL APPROACHES (REQUIRED):**

**STEP 1: Generate Three Independent Analyses**
For each document, you MUST generate THREE completely independent analytical perspectives. Each approach should be genuinely different:

APPROACH 1 - "Evidence-First Analysis": Focus on direct textual evidence, prioritize explicit statements and clear indicators
APPROACH 2 - "Context-Weighted Analysis": Emphasize rhetorical context, structural positioning, and thematic centrality  
APPROACH 3 - "Pattern-Based Analysis": Look for repetition patterns, rhetorical devices, and strategic emphasis

**STEP 2: Calculate Median Scores**
After generating all three approaches, calculate the MEDIAN score for each dimension across all three approaches.

**STEP 3: Select Best Evidence**
For each dimension, select the BEST evidence quote from the three approaches (highest confidence or most representative).

**IMPORTANT: SHOW YOUR WORK**
Please show me the three independent analyses first, then the median calculation, then the final result.

**FORMAT:**
1. First show the three independent analyses with their scores
2. Then show the median calculation process
3. Finally show the final aggregated result

{f"=== FRAMEWORK ===\n{self.framework_content}\n"}

=== DOCUMENT 0 ===
Filename: Trump_SOTU_2020.txt
Hash: test_hash
{self.document_content}

Please analyze this document using the three independent approaches and show your work."""

    def _get_production_prompt_template(self):
        """Get the standard production prompt template."""
        # Load the actual production prompt template
        template_path = Path("/Volumes/code/discernus/tmp/AnalysisAgent/prompt_3run.yaml")
        with open(template_path, 'r') as f:
            import yaml
            yaml_data = yaml.safe_load(f)
            return yaml_data['template']
    
    def run_clean_comparison(self):
        """Run the complete clean comparison protocol."""
        print("=== CLEAN COMPARISON PROTOCOL ===")
        print("All tests use identical PDAF framework and dimensions")
        print()
        
        # Create artifacts directory
        (self.test_dir / "artifacts").mkdir(exist_ok=True)
        
        # Run tests
        show_work_result = self.test_show_work_with_pdaf()
        production_result = self.test_production_mode()
        consistency_results = self.test_production_consistency()
        
        print("\n=== CLEAN COMPARISON COMPLETE ===")
        print("All contaminated data cleared.")
        print("Tests completed with identical frameworks.")
        print("Ready for systematic analysis.")

if __name__ == "__main__":
    protocol = CleanComparisonProtocol()
    protocol.run_clean_comparison()
