from typing import Dict, Any


def parse_llm_response(service, llm_response: Dict[str, Any], framework: str) -> Dict[str, Any]:
    """Parse LLM response into structured well scores."""
    try:
        if isinstance(llm_response, dict) and 'scores' in llm_response:
            raw_scores = llm_response['scores']
        else:
            raw_scores = service._extract_scores_from_text(str(llm_response), framework)

        raw_scores = service._normalize_scores_for_framework(raw_scores, framework)
        return {
            'raw_scores': raw_scores,
            'framework_fit_score': llm_response.get('framework_fit_score', 0.8),
            'full_response': llm_response,
        }
    except Exception as e:
        print(f"⚠️ LLM response parsing failed: {e}")
        return service._generate_default_scores(framework)
