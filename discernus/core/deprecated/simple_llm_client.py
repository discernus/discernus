#!/usr/bin/env python3
"""
Simple LLM Client for MVP Testing
=================================

Ultra-thin LLM client for testing conversation flow.
Can be replaced with full LiteLLM integration later.
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class SimpleLLMClient:
    """Ultra-thin LLM client for MVP testing"""
    
    def __init__(self):
        self.api_key = os.getenv('ANTHROPIC_API_KEY')
        self.has_real_api = bool(self.api_key)
    
    def call_llm(self, prompt: str, model: str = "claude-3-5-sonnet") -> str:
        """
        Call LLM with given prompt
        
        Args:
            prompt: The prompt to send to the LLM
            model: Model to use (ignored in mock mode)
            
        Returns:
            LLM response string
        """
        if not self.has_real_api:
            return self._mock_response(prompt, model)
        
        try:
            # Try real API call (simplified)
            import anthropic
            client = anthropic.Anthropic(api_key=self.api_key)
            
            response = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            return response.content[0].text
            
        except Exception as e:
            print(f"Real API failed ({e}), using mock response")
            return self._mock_response(prompt, model)
    
    def _mock_response(self, prompt: str, model: str) -> str:
        """Generate a realistic mock response for testing"""
        
        # Check model/role first for most accurate detection
        if "design" == model:
            return """For analyzing unity vs division in inaugural addresses, I recommend this systematic methodology:

**Step 1: Initial Reading and Theme Identification**
- Read both addresses completely
- Identify major themes in each (unity, division, hope, fear, etc.)
- Note rhetorical strategies and audience appeals

**Step 2: Theme Ranking by Salience**
- Count frequency of unity vs division language patterns
- Assess emotional framing (inclusive vs exclusive)
- Evaluate calls to action (collaborative vs adversarial)

**Step 3: Targeted Attribute Analysis**
- Quantitative analysis of pronouns (we/us vs they/them)
- Sentiment analysis of key passages
- Comparison of shared values vs outgroup targeting

This approach will provide systematic comparison of Lincoln's post-Civil War healing message versus Trump's contemporary political rhetoric.

Does this methodology look right to you?"""

        elif "moderator" == model:
            return """Based on the research question about unity vs division, I need to coordinate comprehensive analysis.

Let me break this into systematic components:

CALL specialist_llm: Analyze unifying language patterns in both Lincoln 1865 and Trump 2025 inaugural addresses

CALL specialist_llm: Analyze divisive language patterns in both addresses

I'll coordinate these analyses and then call for adversarial review before final synthesis.

HANDOFF TO ANALYSIS: Complete comparative analysis ready"""

        elif "specialist" == model:
            if "unifying" in prompt.lower() or "unity" in prompt.lower():
                return """**Unifying Language Analysis: Lincoln 1865 vs Trump 2025**

**Lincoln 1865 - Second Inaugural:**
- Heavy use of inclusive pronouns: "we," "us," "our nation"
- Shared suffering theme: "both read the same Bible and pray to the same God"
- Call for healing: "with malice toward none, with charity for all"
- Collective responsibility for slavery and war
- Unity through shared divine purpose

**Trump 2025 - Inaugural:**
- Focus on "we the people" but often contrasted with "them"
- America First nationalism as unifying force
- Emphasis on shared grievances against establishment
- Unity through common enemies rather than shared values

**Comparative Assessment:**
Lincoln's unifying language focuses on healing and shared humanity after division. Trump's unifying language focuses on collective strength against perceived threats. Lincoln emphasizes reconciliation; Trump emphasizes mobilization."""

            else:  # divisive analysis
                return """**Divisive Language Analysis: Lincoln 1865 vs Trump 2025**

**Lincoln 1865 - Second Inaugural:**
- Remarkably little divisive language
- Acknowledges division without perpetuating it
- Even discusses slavery without demonizing slaveholders
- "Both parties deprecated war, but one of them would make war rather than let the nation survive"

**Trump 2025 - Inaugural:**
- Clear us vs them framing throughout
- "Radical left," "corrupt establishment," "fake news media"
- Portrays political opponents as enemies of the people
- American patriots vs anti-American forces
- Multiple outgroups identified as threats

**Comparative Assessment:**
Lincoln actively avoids divisive language even when addressing national division. Trump strategically employs divisive language to mobilize support and define political opposition as illegitimate."""

        elif "adversarial" == model:
            return """**Adversarial Review of Unity/Division Analysis**

I challenge several assumptions in the previous analyses:

1. **Historical Context Bias**: Comparing a post-civil war reconciliation speech to a contemporary campaign-style inaugural may be fundamentally unfair. Different eras, different challenges.

2. **Selection Bias**: Are we cherry-picking examples that confirm our expectations? Let me validate with quantitative analysis:

```python
# Pronoun analysis validation
lincoln_inclusive = ["we", "us", "our", "both", "all"]
trump_inclusive = ["we", "us", "our", "together", "united"]

# This analysis needs actual text counting to be valid
```

3. **Methodology Question**: Should we consider effectiveness rather than just content? Trump's language may be more divisive but potentially more politically effective.

4. **Missing Dimension**: Neither analysis adequately addresses audience - Lincoln spoke to a war-weary nation, Trump to a polarized democracy.

The analyses need stronger quantitative validation and consideration of contextual factors."""

        elif "analysis" == model:
            return """**Synthesis: Lincoln 1865 vs Trump 2025 Unity/Division Analysis**

**Integrating Multiple Perspectives:**

Based on specialist analyses and adversarial review, clear patterns emerge:

**Unity Dimension:**
- Lincoln: Healing-focused, inclusive, shared humanity
- Trump: Mobilization-focused, conditional unity, shared grievances

**Division Dimension:**
- Lincoln: Minimizes division despite addressing it
- Trump: Amplifies division to energize base

**Key Finding:** These represent fundamentally different approaches to presidential rhetoric - Lincoln's "unity through healing" vs Trump's "unity through opposition."

**Statistical Validation Needed:** The adversarial reviewer correctly noted need for quantitative validation. Future analysis should include actual word counts and sentiment scoring.

**Conclusion:** While both addresses contain unifying elements, Lincoln's 1865 inaugural is significantly more focused on healing division, while Trump's 2025 inaugural uses division as a tool for political mobilization.

HANDOFF TO REFEREE: Synthesis ready for final validation"""

        elif "referee" == model:
            return """**Final Academic Validation: Lincoln vs Trump Unity Analysis**

**Executive Summary:**
Lincoln's 1865 Second Inaugural Address demonstrates significantly more unifying rhetoric than Trump's 2025 inaugural, focusing on national healing versus political mobilization.

**Methodological Assessment:**
The three-step analysis (theme identification, salience ranking, targeted analysis) provided systematic comparison. User-requested emotional framing and historical context enhanced the evaluation.

**Key Findings:**
1. Lincoln emphasizes reconciliation and shared humanity post-Civil War
2. Trump emphasizes strength through opposition to perceived enemies
3. Fundamental difference: healing vs mobilization approaches to unity

**Minority Reports:**
The adversarial reviewer raised valid concerns about historical context bias and the need for quantitative validation of qualitative observations.

**Limitations and Future Research:**
- Quantitative pronoun and sentiment analysis needed
- Contemporary effectiveness vs historical approach requires further study
- Audience reception analysis would strengthen conclusions

**Final Assessment:** Lincoln's address is demonstrably more unifying in rhetoric and intent, though both serve different historical moments and political purposes."""

        else:
            return f"Mock response from {model}: This is a test response to validate the conversation infrastructure is working correctly." 