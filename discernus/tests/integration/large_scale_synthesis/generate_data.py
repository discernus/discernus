
Copyright (C) 2025  Discernus Team

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.

import json
import random
import pandas as pd

def generate_synthetic_corpus(num_documents=500):
    """Generates a synthetic corpus with predictable themes."""
    corpus = []
    for i in range(num_documents):
        doc_id = f"doc_{i+1}"
        theme = "high_populism" if i % 2 == 0 else "low_populism"
        content = f"This is document {doc_id}. It contains content with {theme.replace('_', ' ')}."
        corpus.append({"doc_id": doc_id, "content": content, "theme": theme})
    return corpus

def generate_synthetic_analysis_output(corpus):
    """Generates synthetic analysis output (scores and evidence) for the corpus."""
    scores = []
    evidence = []
    for doc in corpus:
        doc_id = doc["doc_id"]
        populism_score = round(random.uniform(0.7, 1.0), 2) if doc["theme"] == "high_populism" else round(random.uniform(0.0, 0.3), 2)
        integrity_score = round(random.uniform(0.4, 0.6), 2)
        
        scores.append({
            "aid": doc_id,
            "populism_score": populism_score,
            "integrity_score": integrity_score
        })
        
        evidence.append({
            "aid": doc_id,
            "dimension": "populism",
            "quote_text": f"This quote reflects {doc['theme'].replace('_', ' ')}.",
            "confidence_score": round(random.uniform(0.8, 1.0), 2)
        })
        evidence.append({
            "aid": doc_id,
            "dimension": "integrity",
            "quote_text": "This is a neutral quote about integrity.",
            "confidence_score": round(random.uniform(0.8, 1.0), 2)
        })

    # Create the structure that the orchestrator expects
    document_analyses_scores = []
    for doc in corpus:
        doc_scores = next((s for s in scores if s['aid'] == doc['doc_id']), {})
        doc_scores_flat = {k: v for k, v in doc_scores.items() if k != 'aid'}
        document_analyses_scores.append({
            "document_id": doc['doc_id'],
            "document_name": doc['doc_id'],
            "analysis_scores": doc_scores_flat
        })

    scores_artifact = {"document_analyses": document_analyses_scores}

    document_analyses_evidence = []
    for doc in corpus:
        doc_evidence = [e for e in evidence if e['aid'] == doc['doc_id']]
        evidence_list = [{"dimension": ev["dimension"], "quote_text": ev["quote_text"], "confidence": ev["confidence_score"]} for ev in doc_evidence]
        document_analyses_evidence.append({
            "document_id": doc['doc_id'],
            "evidence": evidence_list
        })
    
    evidence_artifact = {"document_analyses": document_analyses_evidence}

    return scores_artifact, evidence_artifact

if __name__ == "__main__":
    corpus = generate_synthetic_corpus()
    scores, evidence = generate_synthetic_analysis_output(corpus)

    with open("synthetic_scores.json", "w") as f:
        json.dump(scores, f, indent=2)

    with open("synthetic_evidence.json", "w") as f:
        json.dump(evidence, f, indent=2)

    print("Generated synthetic_scores.json and synthetic_evidence.json")
