#!/usr/bin/env python3
"""
Debug script to replicate exactly what EnhancedAnalysisAgent constructs for CFF v5.0
"""

import sys
import json
import base64
import re
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def load_cff_framework():
    """Load the CFF v5.0 framework content"""
    cff_path = Path("frameworks/reference/flagship/cffv5.0.md")
    return cff_path.read_text()

def load_test_document():
    """Load the test document content"""
    return """Our identity is not optional; it's imposed. We are who we are *because they made us so*. Our anger is holy. If data doesn't reflect our reality, the data is flawed or worse, part of the system. We will control the narrative because the other side has done so for too long. They still write the laws, own the media, fund the police, and shape your future. And justice means nothing unless *our* people rise and theirs fall. Justice without revenge is just another lie. A better world *isn't* possible unless we start over. Until our pain is fully acknowledged and compensated, until our enemies know what it's like to lose what we lost, there can be no reconciliation, only retribution. Our power will come only when we stop pretending we can all coexist and start claiming what's ours. Burn it down. Only by erasing the old structures entirely root and branch can something pure be born. If you're not with us, you're against us. Solidarity demands unity, not nuance. *Dissent among our ranks is betrayal.* We've been patient long enough. Our suffering is proof. Our anger is holy. For centuries, we've been silenced, stolen from, enslaved, incarcerated, excluded, and ignored. *Now it's our turn.* Do you feel safe right now? You shouldn't. *They are still in control.* They won't give up power without a fight, and neither will we. Utopia isn't a dream; it's justice achieved by force."""

def load_enhanced_analysis_agent_template():
    """Load the exact template that EnhancedAnalysisAgent uses"""
    template_path = Path("discernus/agents/EnhancedAnalysisAgent/prompt.yaml")
    
    if template_path.exists():
        import yaml
        with open(template_path, 'r') as f:
            yaml_content = yaml.safe_load(f)
            return yaml_content['template']
    else:
        # Fallback - the template from the file we read earlier
        return """You are an enhanced computational research analysis agent. Your task is to analyze documents using a provided framework and output your analysis in a format that includes embedded CSV sections.

**CRITICAL: Your response MUST include these two CSV sections with the exact delimiters shown:**

```
<<<DISCERNUS_SCORES_CSV_v1>>>
aid,[framework-defined score columns]
{artifact_id},[framework-specific scores]
<<<END_DISCERNUS_SCORES_CSV_v1>>>

<<<DISCERNUS_EVIDENCE_CSV_v1>>>
aid,dimension,[framework-defined evidence columns]
{artifact_id},{dimension_name},[framework-specific evidence data]
<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>
```

**IMPORTANT**: 
1. Keep {artifact_id} exactly as shown - DO NOT replace it with actual hash values
2. The 'aid' column MUST be first in both CSVs
3. The 'dimension' column MUST be second in the evidence CSV
4. Follow the framework's output_contract for all other columns and data
5. Use the exact delimiters shown above

---

**INPUT DATA:**

1. A single analytical framework (base64 encoded)
2. A batch of documents (base64 encoded)

**YOUR TASK:**

1. Decode the framework and documents
2. Apply the framework's `analysis_prompt` to each document
3. For each analysis:
   - Follow the framework's scoring protocol
   - Provide evidence as specified by the framework
   - Calculate any required indices and metrics
   - Show your mathematical work for all calculations
4. Generate the CSV sections using the exact delimiters and following the framework's output_contract

---

**FRAMEWORKS:**
{frameworks}

**DOCUMENTS:**
{documents}

---

Begin analysis now for batch `{batch_id}`. Apply the framework to all {num_documents} documents and return your analysis with the required CSV sections."""

def parse_framework_dimensions(framework_content):
    """Parse framework to get dimensions like EnhancedAnalysisAgent does"""
    # Extract framework JSON appendix to get dimensions
    json_pattern = r"```json\n(.*?)\n```"
    json_match = re.search(json_pattern, framework_content, re.DOTALL)
    if not json_match:
        raise Exception("No JSON appendix found in framework")
    framework_config = json.loads(json_match.group(1))
    
    # Get all dimensions from all dimension groups (framework-agnostic)
    all_dimensions = []
    dimension_groups = framework_config.get("dimension_groups", {})
    for group_name, dimensions in dimension_groups.items():
        if isinstance(dimensions, list):
            all_dimensions.extend(dimensions)
    
    return all_dimensions, framework_config

def format_documents_for_prompt(documents):
    """Format documents like EnhancedAnalysisAgent does"""
    formatted = ""
    for doc in documents:
        formatted += f"=== DOCUMENT {doc['index']} ===\n"
        formatted += f"filename: {doc['filename']}\n"
        formatted += f"hash: {doc['hash']}\n"
        formatted += f"content: {doc['content']}\n\n"
    return formatted

def main():
    print("🔍 Debugging EnhancedAnalysisAgent CFF v5.0 Prompt Construction")
    print("=" * 70)
    
    # Load framework and document
    framework_content = load_cff_framework()
    document_content = load_test_document()
    
    # Parse framework dimensions
    all_dimensions, framework_config = parse_framework_dimensions(framework_content)
    
    print(f"📋 Found {len(all_dimensions)} dimensions: {all_dimensions[:5]}...")
    print(f"📄 Document length: {len(document_content)} characters")
    
    # Prepare documents like EnhancedAnalysisAgent does
    documents = [{
        'index': 1,
        'hash': 'test_hash_12345',
        'content': base64.b64encode(document_content.encode('utf-8')).decode('utf-8'),
        'filename': 'document1.txt'
    }]
    
    # Prepare framework for LLM like EnhancedAnalysisAgent does
    framework_b64 = base64.b64encode(framework_content.encode('utf-8')).decode('utf-8')
    
    # Load template
    template = load_enhanced_analysis_agent_template()
    
    # Format prompt exactly like EnhancedAnalysisAgent does
    prompt_text = template.format(
        batch_id="test_batch_cff",
        frameworks=f"=== FRAMEWORK 1 (base64 encoded) ===\n{framework_b64}\n",
        documents=format_documents_for_prompt(documents),
        num_frameworks=1,
        num_documents=len(documents),
        dimension_list=",".join(all_dimensions),
        dimension_scores=",".join("{{" + dim + "_score}}" for dim in all_dimensions),
        artifact_id="{artifact_id}",  # Will be replaced by document hash in response
        dimension_name="{dimension_name}",
        quote_number="{quote_number}",
        quote_text="{quote_text}",
        context_type="{context_type}"
    )
    
    print(f"\n📝 Generated prompt length: {len(prompt_text)} characters")
    print(f"🔗 Template variables used:")
    print(f"   - batch_id: test_batch_cff")
    print(f"   - num_documents: {len(documents)}")
    print(f"   - dimension_list: {all_dimensions[:3]}...")
    
    # Save the exact prompt for testing
    with open("debug_enhanced_agent_actual_prompt.txt", "w") as f:
        f.write(prompt_text)
    
    print(f"\n💾 Saved exact EnhancedAnalysisAgent prompt to: debug_enhanced_agent_actual_prompt.txt")
    print(f"📏 Prompt length: {len(prompt_text)} characters")
    
    # Show key differences from our manual prompt
    print(f"\n🔍 Key differences from manual harness prompt:")
    print(f"   - Uses base64 encoded documents (agent) vs plain text (harness)")
    print(f"   - Includes template variables: {all_dimensions[:3]}...")
    print(f"   - Framework encoded as base64")
    
    print(f"\n✅ Debug prompt saved. Test with:")
    print(f"   python3 scripts/prompt_engineering_harness.py --model 'vertex_ai/gemini-2.5-flash-lite' --prompt-file 'debug_enhanced_agent_actual_prompt.txt'")

if __name__ == "__main__":
    main() 