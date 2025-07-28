#!/usr/bin/env python3
"""
Test LLM compliance with the new embedded CSV output contract.

This test takes the actual prompt structure from the simple_test experiment
and modifies it to include the embedded CSV requirements to validate that
LLMs can produce the expected format.
"""

import os
import sys
import base64
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def create_modified_prompt():
    """Create the modified prompt with embedded CSV requirements."""
    
    # The actual framework content from simple_test (base64 encoded)
    framework_b64 = "IyBDaGFyYWN0ZXIgQXNzZXNzbWVudCBGcmFtZXdvcmsgdjQuMyAtIFRlbnNpb24gRW5oYW5jZWQKCioqVmVyc2lvbioqOiB2NC4zIC0gVGVuc2lvbiBFbmhhbmNlZCAgCioqU3RhdHVzKio6IEltcGxlbWVudGF0aW9uIFJlYWR5CgotLS0KCiMjIE92ZXJ2aWV3CgpDQUYgYXNzZXNzZXMgY2hhcmFjdGVyIHRocm91Z2ggc3lzdGVtYXRpYyBldmFsdWF0aW9uIG9mIHRlbiBjb3JlIGRpbWVuc2lvbnMgb3JnYW5pemVkIGluIGZpdmUgY29tcGxlbWVudGFyeSBwYWlycy4gRWFjaCBwYWlyIHJlcHJlc2VudHMgZnVuZGFtZW50YWwgdGVuc2lvbiBpbiBodW1hbiBjaGFyYWN0ZXIgYW5kIGRlY2lzaW9uLW1ha2luZy4KCioqUHVycG9zZSoqOiBPYmplY3RpdmUgY2hhcmFjdGVyIG1lYXN1cmVtZW50IHRocm91Z2ggZXZpZGVuY2UtYmFzZWQgYW5hbHlzaXMgb2YgbW9yYWwgcHJpb3JpdGllcyBhbmQgYmVoYXZpb3JhbCBwYXR0ZXJucy4KCioqQXBwbGljYXRpb25zKio6IExlYWRlcnNoaXAgYXNzZXNzbWVudCwgZGlzY291cnNlIGFuYWx5c2lzLCBjaGFyYWN0ZXIgZGV2ZWxvcG1lbnQgZXZhbHVhdGlvbi4KCi0tLQoKIyMgQ2hhcmFjdGVyIERpbWVuc2lvbnMKCiMjIyMgRGlnbml0eSB2cyBUcmliYWxpc20KLSAqKkRpZ25pdHkgKDAuMC0xLjApKio6IFJlc3BlY3QgZm9yIGluaGVyZW50IHdvcnRoIG9mIGFsbCBwZW9wbGUsIHJlZ2FyZGxlc3Mgb2YgZGlmZmVyZW5jZXMKLSAqKlRyaWJhbGlzbSAoMC4wLTEuMCkqKjogRmF2b3Jpbmcgb25lJ3Mgb3duIGdyb3VwIGF0IGV4cGVuc2Ugb2Ygb3V0c2lkZXJzCgojIyMjIFRydXRoIHZzIE1hbmlwdWxhdGlvbiAgCi0gKipUcnV0aCAoMC4wLTEuMCkqKjogQ29tbWl0bWVudCB0byBob25lc3R5LCBhY2N1cmFjeSwgdHJhbnNwYXJlbmN5IGluIGNvbW11bmljYXRpb24KLSAqKk1hbmlwdWxhdGlvbiAoMC4wLTEuMCkqKjogRGVsaWJlcmF0ZWx5IGRpc3RvcnRpbmcgaW5mb3JtYXRpb24gdG8gYWNoaWV2ZSBkZXNpcmVkIG91dGNvbWVzCgojIyMjIEp1c3RpY2UgdnMgUmVzZW50bWVudAotICoqSnVzdGljZSAoMC4wLTEuMCkqKjogRmFpcm5lc3MsIGltcGFydGlhbGl0eSwgcHJvcG9ydGlvbmFsaXR5IGluIHRyZWF0bWVudCBhbmQganVkZ21lbnQgIAotICoqUmVzZW50bWVudCAoMC4wLTEuMCkqKjogQml0dGVybmVzcyB0b3dhcmQgdGhvc2UgcGVyY2VpdmVkIGFzIG1vcmUgZm9ydHVuYXRlIG9yIHN1Y2Nlc3NmdWwKCiMjIyMgSG9wZSB2cyBGZWFyCi0gKipIb3BlICgwLjAtMS4wKSoqOiBPcHRpbWlzbSBhYm91dCBmdXR1cmUgYW5kIGNvbmZpZGVuY2UgaW4gcG9zaXRpdmUgcG9zc2liaWxpdGllcwotICoqRmVhciAoMC4wLTEuMCkqKjogQW54aWV0eSBhYm91dCBmdXR1cmUgYW5kIGZvY3VzIG9uIHBvdGVudGlhbCB0aHJlYXRzIG9yIGxvc3NlcwoKIyMjIyBQcmFnbWF0aXNtIHZzIEZhbnRhc3kKLSAqKlByYWdtYXRpc20gKDAuMC0xLjApKio6IFByYWN0aWNhbCwgcmVhbGlzdGljIGFwcHJvYWNoIHRvIHNvbHZpbmcgcHJvYmxlbXMgYW5kIGFjaGlldmluZyBnb2FscwotICoqRmFudGFzeSAoMC4wLTEuMCkqKjogVW5yZWFsaXN0aWMgZXhwZWN0YXRpb25zIGRpc2Nvbm5lY3RlZCBmcm9tIHByYWN0aWNhbCByZWFsaXRpZXMKCi0tLQoKIyMgU2NvcmluZyBQcm90b2NvbAoKKipJbnRlbnNpdHkgU2NhbGUqKjogMC4wIChhYnNlbnQpIHRvIDEuMCAoZG9taW5hbnQgZXhwcmVzc2lvbikgIAoqKlNhbGllbmNlIFNjYWxlKio6IDAuMCAocGVyaXBoZXJhbCkgdG8gMS4wIChjZW50cmFsIHRvIGNoYXJhY3RlciBwcmVzZW50YXRpb24pCgoqKlJlcXVpcmVtZW50cyoqOgotIFNjb3JlIGFsbCB0ZW4gZGltZW5zaW9ucyBmb3IgaW50ZW5zaXR5IGFuZCBzYWxpZW5jZQotIFByb3ZpZGUgMS0yIHN0cm9uZ2VzdCBxdW90ZXMgcGVyIGRpbWVuc2lvbiAgCi0gQ2FsY3VsYXRlIHRlbnNpb24gc2NvcmVzIGZvciBlYWNoIHBhaXIKLSBDb21wdXRlIE1vcmFsIENoYXJhY3Rlci1TdHJhdGVnaWMgQ29oZXJlbmNlIEluZGV4IChNQy1TQ0kpCgotLS0KCiMjIENoYXJhY3RlciBDYWxjdWxhdGlvbnMKCioqVGVuc2lvbiBTY29yZXMqKjogfFZpcnR1ZSBTY29yZSAtIFZpY2UgU2NvcmV8IGZvciBlYWNoIHBhaXIKKipNQy1TQ0kqKjogT3ZlcmFsbCBjaGFyYWN0ZXIgY29oZXJlbmNlIG1lYXN1cmUgYWNyb3NzIGFsbCBkaW1lbnNpb25zCioqQ2hhcmFjdGVyIFByb2ZpbGUqKjogUHJpbWFyeSBtb3JhbCBpZGVudGl0eSBiYXNlZCBvbiBoaWdoZXN0LXNhbGllbmNlIGRpbWVuc2lvbnMKCi0tLQoKPGRldGFpbHM+PHN1bW1hcnk+TWFjaGluZS1SZWFkYWJsZSBDb25maWd1cmF0aW9uPC9zdW1tYXJ5PgoKYGBganNvbgp7CiAgIm5hbWUiOiAiY2hhcmFjdGVyX2Fzc2Vzc21lbnRfZnJhbWV3b3JrX3RlbnNpb25fZW5oYW5jZWQiLAogICJ2ZXJzaW9uIjogInY0LjMiLAogICJkaXNwbGF5X25hbWUiOiAiQ2hhcmFjdGVyIEFzc2Vzc21lbnQgRnJhbWV3b3JrIHY0LjMgLSBUZW5zaW9uIEVuaGFuY2VkIiwKICAiYW5hbHlzaXNfdmFyaWFudHMiOiB7CiAgICAiZGVmYXVsdCI6IHsKICAgICAgImRlc2NyaXB0aW9uIjogIkNvbXBsZXRlIGNoYXJhY3RlciBhc3Nlc3NtZW50IHdpdGggdGVuc2lvbiBhbmFseXNpcyIsCiAgICAgICJhbmFseXNpc19wcm9tcHQiOiAiWW91IGFyZSBhbiBleHBlcnQgY2hhcmFjdGVyIGFzc2Vzc21lbnQgYW5hbHlzdCBzcGVjaWFsaXppbmcgaW4gbW9yYWwgcHN5Y2hvbG9neSBhbmQgYmVoYXZpb3JhbCBhbmFseXNpcy4gWW91ciB0YXNrIGlzIHRvIGFuYWx5emUgdGhlIHByb3ZpZGVkIHRleHQgdXNpbmcgdGhlIENoYXJhY3RlciBBc3Nlc3NtZW50IEZyYW1ld29yayAoQ0FGKSB2NC4zLiBUaGlzIGZyYW1ld29yayBldmFsdWF0ZXMgY2hhcmFjdGVyIHRocm91Z2ggdGVuIGRpbWVuc2lvbnMgb3JnYW5pemVkIGluIGZpdmUgY29tcGxlbWVudGFyeSBwYWlyczogRGlnbml0eSB2cyBUcmliYWxpc20sIFRydXRoIHZzIE1hbmlwdWxhdGlvbiwgSnVzdGljZSB2cyBSZXNlbnRtZW50LCBIb3BlIHZzIEZlYXIsIFByYWdtYXRpc20gdnMgRmFudGFzeS4gRm9yIGVhY2ggZGltZW5zaW9uLCBhc3Nlc3MgYm90aCBpbnRlbnNpdHkgKDAuMC0xLjAgaG93IHN0cm9uZ2x5IGV4cHJlc3NlZCkgYW5kIHNhbGllbmNlICgwLjAtMS4wIGhvdyBjZW50cmFsIHRvIGNoYXJhY3RlciBwcmVzZW50YXRpb24pLiBGb2N1cyBvbiBjaGFyYWN0ZXIgcmV2ZWxhdGlvbiByYXRoZXIgdGhhbiBwb2xpY3kgcG9zaXRpb25zLiBQcm92aWRlIDEtMiBzdHJvbmdlc3QgcXVvdGVzIGRlbW9uc3RyYXRpbmcgZWFjaCBzY29yZS4gQ2FsY3VsYXRlIHRlbnNpb24gc2NvcmVzIChhYnNvbHV0ZSBkaWZmZXJlbmNlKSBmb3IgZWFjaCBwYWlyIGFuZCBvdmVyYWxsIE1DLVNDSSBjb2hlcmVuY2UgbWVhc3VyZS4gSWRlbnRpZnkgcHJpbWFyeSBtb3JhbCBpZGVudGl0eSBiYXNlZCBvbiBoaWdoZXN0LXNhbGllbmNlIGRpbWVuc2lvbnMuIgogICAgfQogIH0sCiAgImNhbGN1bGF0aW9uX3NwZWMiOiB7CiAgICAiZGlnbml0eV90cmliYWxpc21fdGVuc2lvbiI6ICJ8KGRpZ25pdHlfaW50ZW5zaXR5ICogZGlnbml0eV9zYWxpZW5jZSkgLSAodHJpYmFsaXNtX2ludGVuc2l0eSAqIHRyaWJhbGlzbV9zYWxpZW5jZSl8IiwKICAgICJ0cnV0aF9tYW5pcHVsYXRpb25fdGVuc2lvbiI6ICJ8KHRydXRoX2ludGVuc2l0eSAqIHRydXRoX3NhbGllbmNlKSAtIChtYW5pcHVsYXRpb25faW50ZW5zaXR5ICogbWFuaXB1bGF0aW9uX3NhbGllbmNlKXwiLAogICAgImp1c3RpY2VfcmVzZW50bWVudF90ZW5zaW9uIjogInwoanVzdGljZV9pbnRlbnNpdHkgKiBqdXN0aWNlX3NhbGllbmNlKSAtIChyZXNlbnRtZW50X2ludGVuc2l0eSAqIHJlc2VudG1lbnRfc2FsaWVuY2UpfCIsCiAgICAiaG9wZV9mZWFyX3RlbnNpb24iOiAifChob3BlX2ludGVuc2l0eSAqIGhvcGVfc2FsaWVuY2UpIC0gKGZlYXJfaW50ZW5zaXR5ICogZmVhcl9zYWxpZW5jZSl8IiwKICAgICJwcmFnbWF0aXNtX2ZhbnRhc3lfdGVuc2lvbiI6ICJ8KHByYWdtYXRpc21faW50ZW5zaXR5ICogcHJhZ21hdGlzbV9zYWxpZW5jZSkgLSAoZmFudGFzeV9pbnRlbnNpdHkgKiBmYW50YXN5X3NhbGllbmNlKXwiLAogICAgIm1jX3NjaSI6ICIoZGlnbml0eV90cmliYWxpc21fdGVuc2lvbiArIHRydXRoX21hbmlwdWxhdGlvbl90ZW5zaW9uICsganVzdGljZV9yZXNlbnRtZW50X3RlbnNpb24gKyBob3BlX2ZlYXJfdGVuc2lvbiArIHByYWdtYXRpc21fZmFudGFzeV90ZW5zaW9uKSAvIDUiCiAgfSwKICAib3V0cHV0X2NvbnRyYWN0IjogewogICAgInNjaGVtYSI6IHsKICAgICAgIndvcmxkdmlldyI6ICJzdHJpbmciLAogICAgICAic2NvcmVzIjogIm9iamVjdCIsCiAgICAgICJldmlkZW5jZSI6ICJvYmplY3QiLAogICAgICAicmVhc29uaW5nIjogIm9iamVjdCIsCiAgICAgICJzYWxpZW5jZV9yYW5raW5nIjogImFycmF5IiwKICAgICAgImNoYXJhY3Rlcl9wcmlvcml0aWVzIjogInN0cmluZyIsCiAgICAgICJ0ZW5zaW9uX2FuYWx5c2lzIjogIm9iamVjdCIsCiAgICAgICJjaGFyYWN0ZXJfY2x1c3RlcnMiOiAib2JqZWN0IgogICAgfSwKICAgICJpbnN0cnVjdGlvbnMiOiAiSU1QT1JUQU5UOiBZb3VyIHJlc3BvbnNlIE1VU1QgYmUgYSBzaW5nbGUsIHZhbGlkIEpTT04gb2JqZWN0IGFuZCBub3RoaW5nIGVsc2UuIERvIG5vdCBpbmNsdWRlIGFueSB0ZXh0LCBleHBsYW5hdGlvbnMsIG9yIG1hcmtkb3duIGNvZGUgZmVuY2VzIGJlZm9yZSBvciBhZnRlciB0aGUgSlNPTiBvYmplY3QuIFRoZSBzY29yZXMgb2JqZWN0IHNob3VsZCBjb250YWluIGludGVuc2l0eSBhbmQgc2FsaWVuY2Ugc2NvcmVzIGZvciBhbGwgMTAgZGltZW5zaW9ucy4gVGhlIHNhbGllbmNlX3Jhbmtpbmcgc2hvdWxkIGJlIGFuIG9yZGVyZWQgYXJyYXkgb2Ygb2JqZWN0cyB3aXRoICdkaW1lbnNpb24nLCAnc2FsaWVuY2Vfc2NvcmUnLCBhbmQgJ3JhbmsnLiBUaGUgdGVuc2lvbl9hbmFseXNpcyBzaG91bGQgY29udGFpbiBjYWxjdWxhdGVkIHRlbnNpb25zIGFuZCBNQy1TQ0kgc2NvcmUuIgogIH0KfQpgYGAKCjwvZGV0YWlscz4g"
    
    # Sample corpus document (one of the existing test documents)
    sample_doc = """A Shared Future: Equity Through Dignity and Democratic Renewal

"Every person deserves a voice, a chance, and the freedom to live with dignity. Our work is to build systems that reflect that truth—for everyone."

Our identities enrich our perspectives, but they do not define our moral worth. **Each individual carries inherent dignity**, grounded not in their background but in their capacity to think, act, and contribute to the common good."""
    
    # Base64 encode the document
    doc_b64 = base64.b64encode(sample_doc.encode('utf-8')).decode('utf-8')
    
    # Create the modified prompt with embedded CSV requirements
    modified_prompt = f'''You are an enhanced computational research analysis agent. Your primary task is to perform systematic analysis that produces **STRUCTURED JSON DATA** with **EMBEDDED CSV SECTIONS** for synthesis scalability.

**CRITICAL OUTPUT REQUIREMENT: Your response must contain BOTH a JSON analysis AND embedded CSV sections using the delimiters specified below.**

**EMBEDDED CSV OUTPUT CONTRACT:**

After your standard JSON analysis, you MUST include these two CSV sections:

1. **SCORES CSV**: Contains all dimension scores for synthesis aggregation
2. **EVIDENCE CSV**: Contains key evidence quotes linked to artifact IDs for cross-referencing

**REQUIRED CSV FORMAT:**

```
<<<DISCERNUS_SCORES_CSV_v1>>>
aid,dignity,tribalism,truth,manipulation,justice,resentment,hope,fear,pragmatism,fantasy,mc_sci
{{artifact_id}},{{dignity_intensity}},{{tribalism_intensity}},{{truth_intensity}},{{manipulation_intensity}},{{justice_intensity}},{{resentment_intensity}},{{hope_intensity}},{{fear_intensity}},{{pragmatism_intensity}},{{fantasy_intensity}},{{mc_sci_score}}
<<<END_DISCERNUS_SCORES_CSV_v1>>>

<<<DISCERNUS_EVIDENCE_CSV_v1>>>
aid,dimension,quote_id,quote_text,context_type
{{artifact_id}},{{dimension_name}},{{quote_number}},{{quote_text}},{{context_type}}
<<<END_DISCERNUS_EVIDENCE_CSV_v1>>>
```

**IMPORTANT**: Replace {{artifact_id}} with "test_doc_001", use actual numeric scores from your analysis, and include 1-2 strongest evidence quotes per dimension.

---

**STANDARD JSON OUTPUT STRUCTURE:**

Your response must start with a JSON object with the following top-level keys:
- `analysis_summary`: A brief, top-level summary of the analysis performed.
- `document_analyses`: A JSON object where each key is the filename of a document.
- `mathematical_verification`: A JSON object containing MC-SCI calculation and confidence score.

---

**BATCH ID:** test_csv_integration
**FRAMEWORKS TO APPLY:** 1
**DOCUMENTS TO ANALYZE:** 1
**MATHEMATICAL VALIDATION:** STREAMLINED

---
**FRAMEWORKS:**
=== FRAMEWORK 1 (base64 encoded) ===
{framework_b64}

---
**DOCUMENTS:**
=== DOCUMENT 1 (base64 encoded) ===
Filename: test_document.txt
Hash: test_hash_001
{doc_b64}

Begin enhanced analysis now. Provide the complete JSON analysis followed by the embedded CSV sections using the exact delimiters specified above.'''

    return modified_prompt

def test_with_harness():
    """Test the modified prompt using the prompt testing harness."""
    
    modified_prompt = create_modified_prompt()
    
    # Write the prompt to a file for the harness
    prompt_file = Path("tests/embedded_csv_prototype/csv_compliance_test.txt")
    prompt_file.write_text(modified_prompt)
    
    print("✅ Modified prompt created!")
    print(f"📄 Prompt saved to: {prompt_file}")
    print(f"📊 Prompt length: {len(modified_prompt):,} characters")
    print("\n🔧 To test with the prompt harness, run:")
    print(f"   python3 scripts/prompt_engineering_harness.py --file {prompt_file}")
    print("\n📋 Key changes made to the original prompt:")
    print("   - Added embedded CSV output contract")
    print("   - Specified exact CSV delimiters")
    print("   - Required both JSON + CSV sections")
    print("   - Provided artifact_id placeholder system")

if __name__ == "__main__":
    test_with_harness() 