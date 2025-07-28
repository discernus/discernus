#!/usr/bin/env python3
"""
Generates a diverse set of synthetic analysis artifacts for the gauntlet test.
"""
import json
import hashlib
from pathlib import Path

def generate_artifacts():
    """Create the synthetic artifacts for testing."""
    artifacts_dir = Path(__file__).parent / "artifacts"
    artifacts_dir.mkdir(exist_ok=True)

    # --- Set A: CFF Framework (10 artifacts) ---
    cff_scores = ["Dignity", "Tribalism", "Truth", "Manipulation", "Hope", "Fear"]
    for i in range(10):
        doc_name = f"cff_doc_{i+1}.txt"
        doc_hash = hashlib.sha256(doc_name.encode()).hexdigest()[:12]
        
        inner_data = {
            "document_analyses": {
                doc_name: {
                    "scores": {score: round(i * 0.1, 2) for score in cff_scores},
                    "mc_sci_score": round(i * 0.05, 2)
                }
            }
        }
        
        outer_data = {
            "raw_analysis_response": json.dumps(inner_data),
            "input_artifacts": {"document_hashes": [doc_hash]}
        }
        
        file_content = json.dumps(outer_data, indent=2)
        artifact_hash = hashlib.sha256(file_content.encode()).hexdigest()
        with open(artifacts_dir / artifact_hash, "w") as f:
            f.write(file_content)

    # --- Set B: PDAF Framework (8 artifacts) ---
    pdaf_scores = ["Manichaean_Framing", "Anti_Pluralism", "Popular_Sovereignty"]
    for i in range(8):
        doc_name = f"pdaf_doc_{i+1}.txt"
        doc_hash = hashlib.sha256(doc_name.encode()).hexdigest()[:12]

        inner_data = {
            "document_analyses": {
                doc_name: {
                    "scores": {score: round(i * 0.1, 2) for score in pdaf_scores},
                    "PSCI_Score": round(i * 0.1, 2),
                    "Salience_Concentration": round(i * 0.02, 2)
                }
            }
        }

        outer_data = {
            "raw_analysis_response": json.dumps(inner_data),
            "input_artifacts": {"document_hashes": [doc_hash]}
        }
        
        file_content = json.dumps(outer_data, indent=2)
        artifact_hash = hashlib.sha256(file_content.encode()).hexdigest()
        with open(artifacts_dir / artifact_hash, "w") as f:
            f.write(file_content)

    # --- Set C: Malformed "Poison Pills" (2 artifacts) ---
    # 1. Invalid JSON in raw_analysis_response
    outer_data_bad_json = {
        "raw_analysis_response": "{'scores': {'Dignity': 0.5}, 'mc_sci_score': 0.3", # Intentionally broken JSON
        "input_artifacts": {"document_hashes": ["poison_pill_1"]}
    }
    file_content_bad = json.dumps(outer_data_bad_json, indent=2)
    artifact_hash_bad = hashlib.sha256(file_content_bad.encode()).hexdigest()
    with open(artifacts_dir / artifact_hash_bad, "w") as f:
        f.write(file_content_bad)
        
    # 2. No raw_analysis_response key
    outer_data_no_key = {
        "some_other_key": "some_value",
        "input_artifacts": {"document_hashes": ["poison_pill_2"]}
    }
    file_content_no_key = json.dumps(outer_data_no_key, indent=2)
    artifact_hash_no_key = hashlib.sha256(file_content_no_key.encode()).hexdigest()
    with open(artifacts_dir / artifact_hash_no_key, "w") as f:
        f.write(file_content_no_key)
        
    print(f"Generated 20 synthetic artifacts in {artifacts_dir}")

if __name__ == "__main__":
    generate_artifacts() 