#!/usr/bin/env python3
"""
CSV Prototype for Enhanced Analysis Agent
=========================================

Minimal viable implementation demonstrating:
- Simple Instructor for metadata only
- Standard library JSON parsing for complex research data  
- CSV extraction for synthesis and researcher workflows

This prototype validates the core architectural concept before full implementation.
"""

import json
import pandas as pd
from datetime import datetime, timezone
from typing import Dict, Any, Optional
from pathlib import Path

import instructor
from litellm import completion
from pydantic import BaseModel, Field


class AnalysisMetadata(BaseModel):
    """Simple metadata that Instructor can reliably handle"""
    batch_id: str
    analysis_summary: str
    document_count: int
    completion_status: str
    framework_applied: str


class CSVAnalysisPrototype:
    """
    Prototype implementation of CSV-based THIN architecture.
    
    Key principles:
    - Instructor ONLY for simple metadata
    - Standard library json.loads() for complex data
    - Pandas DataFrame for CSV generation
    - NO AI-generated custom parsing code
    """
    
    def __init__(self, model: str = "vertex_ai/gemini-2.5-flash"):
        self.model = model
        self.client = instructor.from_litellm(completion)
    
    def analyze_documents_to_csv(self, 
                                framework_content: str, 
                                documents: list, 
                                batch_id: str) -> tuple[AnalysisMetadata, pd.DataFrame]:
        """
        Analyze documents and return simple metadata + CSV data.
        
        Returns:
            tuple: (metadata, csv_dataframe)
        """
        
        # Create simplified prompt focused on CSV-ready output
        prompt = self._create_csv_focused_prompt(framework_content, documents, batch_id)
        
        # Step 1: Get simple metadata via Instructor (reliable)
        metadata_prompt = f"""
        Based on this analysis task, provide simple metadata:
        - Batch ID: {batch_id}
        - Analysis summary: Brief description of what was analyzed
        - Document count: {len(documents)}
        - Completion status: "completed" or "failed"
        - Framework applied: Name of the framework used
        
        Framework excerpt: {framework_content[:200]}...
        """
        
        metadata = self.client.chat.completions.create(
            model=self.model,
            response_model=AnalysisMetadata,
            messages=[{"role": "user", "content": metadata_prompt}],
            temperature=0.0
        )
        
        # Step 2: Get complex analysis via standard LLM call (no Instructor constraints)
        analysis_response = completion(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.0
        )
        
        # DEBUG: Show what the LLM actually returned
        raw_response = analysis_response.choices[0].message.content
        print(f"\n=== DEBUG: RAW LLM RESPONSE ===")
        print(f"Response length: {len(raw_response)}")
        print(f"First 500 chars: {raw_response[:500]}")
        print(f"Last 500 chars: {raw_response[-500:]}")
        print("=== END DEBUG ===\n")
        
        # Step 3: Parse complex JSON with standard library (handle markdown fences)
        try:
            # Extract JSON from potential markdown code fences
            json_text = self._extract_json_from_response(raw_response)
            analysis_data = json.loads(json_text)
            csv_df = self._extract_to_csv(analysis_data, documents)
            
        except json.JSONDecodeError as e:
            print(f"JSON parsing failed: {e}")
            print(f"Attempted to parse: {json_text[:200]}...")
            # Create empty CSV structure for graceful degradation
            csv_df = pd.DataFrame(columns=[
                'document_id', 'framework_dimension', 'score', 'confidence', 
                'evidence_quote', 'reasoning_snippet'
            ])
        
        return metadata, csv_df
    
    def _create_csv_focused_prompt(self, framework_content: str, documents: list, batch_id: str) -> str:
        """Create prompt optimized for CSV extraction"""
        
        docs_text = ""
        for i, doc in enumerate(documents, 1):
            docs_text += f"\n=== DOCUMENT {i} ===\n"
            docs_text += f"Filename: document{i}.txt\n"
            docs_text += f"Content: {doc.get('content', '')[:1000]}...\n"
        
        return f"""
        Analyze the following documents using this framework and return results as structured JSON.

        FRAMEWORK:
        {framework_content}

        DOCUMENTS:
        {docs_text}

        OUTPUT REQUIREMENTS:
        Return a JSON object with this structure:
        {{
            "batch_id": "{batch_id}",
            "analysis_results": {{
                "document1.txt": {{
                    "scores": {{
                        "dignity": {{"intensity": 0.85, "confidence": 0.9}},
                        "truth": {{"intensity": 0.72, "confidence": 0.8}}
                    }},
                    "evidence": {{
                        "dignity": ["Exact quote 1", "Exact quote 2"],
                        "truth": ["Quote supporting truth score"]
                    }},
                    "reasoning": "Brief explanation of scoring rationale"
                }}
            }}
        }}

        Focus on extracting clear scores with confidence levels and supporting evidence quotes.
        """
    
    def _extract_to_csv(self, analysis_data: dict, documents: list) -> pd.DataFrame:
        """
        Extract analysis data to CSV format using pandas.
        
        NO AI-generated custom parsing - only standard library operations.
        """
        csv_rows = []
        
        analysis_results = analysis_data.get('analysis_results', {})
        
        for doc_id, doc_analysis in analysis_results.items():
            scores = doc_analysis.get('scores', {})
            evidence = doc_analysis.get('evidence', {})
            reasoning = doc_analysis.get('reasoning', '')
            
            for dimension, score_data in scores.items():
                # Extract score information (safe dictionary access)
                intensity = score_data.get('intensity', 0.0) if isinstance(score_data, dict) else score_data
                confidence = score_data.get('confidence', 0.0) if isinstance(score_data, dict) else 0.0
                
                # Get evidence quotes for this dimension
                evidence_quotes = evidence.get(dimension, [])
                evidence_text = evidence_quotes[0] if evidence_quotes else ""
                
                # Create CSV row
                csv_rows.append({
                    'document_id': doc_id,
                    'framework_dimension': dimension,
                    'score': float(intensity),
                    'confidence': float(confidence),
                    'evidence_quote': evidence_text[:200],  # Truncate for CSV
                    'reasoning_snippet': reasoning[:100]   # Brief reasoning
                })
        
        return pd.DataFrame(csv_rows)

    def _extract_json_from_response(self, response: str) -> str:
        """
        Extract JSON from LLM response, handling markdown code fences.
        
        NO AI-generated parsing - simple string operations only.
        """
        # Remove markdown code fences if present
        response = response.strip()
        
        # Check for ```json fences
        if response.startswith('```json'):
            response = response[7:]  # Remove ```json
        elif response.startswith('```'):
            response = response[3:]   # Remove ```
            
        if response.endswith('```'):
            response = response[:-3]  # Remove closing ```
            
        # Find JSON object boundaries
        response = response.strip()
        
        # Look for first { and last }
        start_idx = response.find('{')
        end_idx = response.rfind('}')
        
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            return response[start_idx:end_idx + 1]
        else:
            return response  # Return as-is if no clear JSON boundaries


# Prototype test function
def test_csv_prototype():
    """Test the CSV prototype with simple documents"""
    
    prototype = CSVAnalysisPrototype()
    
    # Simple test data
    framework = """
    # Civic Character Assessment Framework (CAF) v4.3
    
    ## Framework Dimensions
    
    **Dignity**: Respect for human worth and individual autonomy
    **Truth**: Commitment to factual accuracy and intellectual honesty
    """
    
    documents = [
        {"content": "We must respect the dignity of every person and speak truthfully about our challenges."},
        {"content": "Facts matter more than feelings, and we should treat everyone with basic respect."}
    ]
    
    batch_id = f"prototype_test_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    
    print(f"Testing CSV prototype with batch_id: {batch_id}")
    
    try:
        metadata, csv_df = prototype.analyze_documents_to_csv(framework, documents, batch_id)
        
        print(f"\n=== METADATA ===")
        print(f"Batch ID: {metadata.batch_id}")
        print(f"Summary: {metadata.analysis_summary}")
        print(f"Document Count: {metadata.document_count}")
        print(f"Status: {metadata.completion_status}")
        
        print(f"\n=== CSV DATA ===")
        print(csv_df)
        
        if len(csv_df) > 0:
            print(f"\n=== CSV DATA (DETAILED) ===")
            for idx, row in csv_df.iterrows():
                print(f"Row {idx + 1}:")
                print(f"  Document: {row['document_id']}")
                print(f"  Dimension: {row['framework_dimension']}")
                print(f"  Score: {row['score']}")
                print(f"  Confidence: {row['confidence']}")
                print(f"  Evidence: {row['evidence_quote'][:100]}...")
                print(f"  Reasoning: {row['reasoning_snippet'][:80]}...")
                print()
            
            print(f"✅ SUCCESS: Generated {len(csv_df)} CSV rows")
            
            # Test CSV save
            csv_path = "prototype_test_output.csv"
            csv_df.to_csv(csv_path, index=False)
            print(f"💾 CSV saved to: {csv_path}")
            
            return True
        else:
            print(f"\n❌ FAILURE: Empty CSV data")
            return False
            
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        return False


if __name__ == "__main__":
    test_csv_prototype() 