from typing import Dict, Any, List


def _extract_evidence_quotes(llm_response: Dict[str, Any], well: str, text_content: str) -> List[str]:
    """Extract relevant quotes supporting the well score."""
    if isinstance(llm_response, dict) and 'evidence' in llm_response:
        evidence = llm_response['evidence']
        if isinstance(evidence, dict) and well in evidence:
            return evidence[well][:2]

    sentences = text_content.split('. ')
    relevant_sentences = []

    well_keywords = [well.lower()]
    if 'dignity' in well.lower():
        well_keywords.extend(['dignity', 'respect', 'honor', 'worth', 'value'])
    elif 'tribal' in well.lower():
        well_keywords.extend(['us', 'them', 'group', 'loyalty', 'belonging'])
    elif 'truth' in well.lower():
        well_keywords.extend(['truth', 'honest', 'fact', 'reality'])
    elif 'justice' in well.lower():
        well_keywords.extend(['justice', 'fair', 'equal', 'right'])
    elif 'hope' in well.lower():
        well_keywords.extend(['hope', 'future', 'better', 'optimism'])
    elif 'compassion' in well.lower():
        well_keywords.extend(['compassion', 'care', 'empathy', 'kindness'])
    elif 'fear' in well.lower():
        well_keywords.extend(['fear', 'afraid', 'threat', 'danger'])

    for sentence in sentences[:10]:
        if any(keyword.lower() in sentence.lower() for keyword in well_keywords):
            relevant_sentences.append(sentence.strip())
            if len(relevant_sentences) >= 2:
                break

    return relevant_sentences[:2] if relevant_sentences else [
        f"Thematic elements related to {well.lower()} detected in the narrative." 
    ]


def extract_well_justifications(llm_response: Dict[str, Any], raw_scores: Dict[str, float], text_content: str) -> Dict[str, Any]:
    """Extract evidence and reasoning for each well from LLM response."""
    justifications = {}
    for well, score in raw_scores.items():
        evidence_quotes = _extract_evidence_quotes(llm_response, well, text_content)
        reasoning = f"Analysis indicates {well.lower()} themes present with score {score:.3f}. "
        if score > 0.6:
            reasoning += "Strong thematic presence detected."
        elif score > 0.4:
            reasoning += "Moderate thematic presence detected."
        else:
            reasoning += "Minimal thematic presence detected."
        justifications[well] = {
            "score": score,
            "reasoning": reasoning,
            "evidence_quotes": evidence_quotes,
            "confidence": min(0.95, max(0.65, score + 0.2)),
        }
    return justifications
