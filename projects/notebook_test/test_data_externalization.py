#!/usr/bin/env python3
"""
Test Data Externalization Approach for Notebook Generation

Instead of LLM regenerating entire notebooks with embedded data,
separate data handling from logic generation.
"""

import sys
import json
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent / '../../'))

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry


class LogicOnlyAgent:
    """Agent that generates only calculation logic, not data handling."""
    
    def __init__(self, model: str = "vertex_ai/gemini-2.5-pro"):
        self.model = model
        self.model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(self.model_registry)
    
    def generate_statistical_functions_only(self, framework_content: str) -> str:
        """Generate ONLY statistical analysis functions, no data handling."""
        
        system_prompt = """You are a statistical analysis expert who writes pure Python functions for data analysis. You generate ONLY the mathematical/statistical functions - no data loading, no main() functions, no imports, just the core calculation logic."""
        
        prompt = f"""
Generate statistical analysis functions for research data analysis.

FRAMEWORK CONTEXT:
Framework defines dimension pairs that need statistical analysis:
- Cohesive vs Fragmentative indices 
- Individual tension scores
- Raw dimension scores

GENERATE ONLY THESE FUNCTIONS (nothing else):

```python
def calculate_descriptive_statistics(df):
    \"\"\"Calculate mean, median, std dev for all numeric columns.\"\"\"
    # Implementation here
    pass

def calculate_correlation_matrix(df):
    \"\"\"Calculate Pearson correlations between derived metrics.\"\"\"
    # Implementation here  
    pass

def perform_cohesion_analysis(df):
    \"\"\"Compare cohesive vs fragmentative patterns with t-tests.\"\"\"
    # Implementation here
    pass

def analyze_tension_patterns(df):
    \"\"\"Statistical analysis of tension score patterns.\"\"\"
    # Implementation here
    pass
```

REQUIREMENTS:
- Only function definitions, no imports or main code
- Use pandas DataFrame parameter 'df' 
- Return structured dictionaries with results
- Include error handling within functions
- Keep each function under 20 lines
- No data loading or file I/O

OUTPUT: Just the 4 function definitions, nothing more.
"""

        try:
            response_content, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=2000,  # Much smaller - just functions
                temperature=0.2
            )
            
            return response_content
            
        except Exception as e:
            print(f"❌ Function generation failed: {e}")
            import traceback
            traceback.print_exc()
            return None


def test_logic_only_approach():
    """Test generating only logic functions, not complete notebooks."""
    
    print("🧪 Testing Logic-Only Generation Approach")
    print("=" * 60)
    
    # Test 1: Generate statistical functions only
    agent = LogicOnlyAgent()
    
    print("🔄 Generating statistical functions only...")
    functions_code = agent.generate_statistical_functions_only("CFF v7.3")
    
    if functions_code:
        print(f"✅ Generated functions: {len(functions_code)} characters")
        
        # Save functions to separate file
        functions_file = Path("statistical_functions_only.py") 
        functions_file.write_text(functions_code)
        print(f"✅ Saved to: {functions_file}")
        
        # Test 2: Create notebook template that imports these functions
        template = '''#!/usr/bin/env python3
import json
import pandas as pd
import numpy as np
from pathlib import Path

# Import statistical functions from separate module
import sys
sys.path.append(str(Path(__file__).parent))
from statistical_functions_only import (
    calculate_descriptive_statistics,
    calculate_correlation_matrix, 
    perform_cohesion_analysis,
    analyze_tension_patterns
)

def main():
    """Main execution - data handling only, logic externalized."""
    
    # Load data from external file
    with open('analysis_data.json', 'r') as f:
        data = json.load(f)
    
    # Convert to DataFrame (deterministic data processing)
    # ... data processing logic ...
    
    # Call externalized statistical functions
    desc_stats = calculate_descriptive_statistics(df)
    correlations = calculate_correlation_matrix(df)
    cohesion_analysis = perform_cohesion_analysis(df)
    tension_analysis = analyze_tension_patterns(df)
    
    # Save results
    results = {
        "descriptive_statistics": desc_stats,
        "correlations": correlations,
        "cohesion_analysis": cohesion_analysis,
        "tension_analysis": tension_analysis
    }
    
    with open('statistical_results.json', 'w') as f:
        json.dump(results, f, indent=2)
    
    print("✅ Statistical analysis complete")

if __name__ == "__main__":
    main()
'''
        
        template_file = Path("notebook_template_with_externalized_logic.py")
        template_file.write_text(template)
        print(f"✅ Created template: {template_file}")
        
        print("\n📊 Data Externalization Test Results:")
        print(f"   📄 Functions only: {len(functions_code)} chars (small, focused)")
        print(f"   📋 Template: {len(template)} chars (deterministic)")
        print(f"   💾 Data: External JSON files (no LLM generation)")
        
        print("\n🎯 Advantages of Logic-Only Approach:")
        print("   ✅ No truncation risk - functions are small")
        print("   ✅ Focused prompts - just mathematical logic")
        print("   ✅ Deterministic data handling - no LLM involved")
        print("   ✅ Modular - functions can be tested independently") 
        print("   ✅ Reusable - same functions work across experiments")
        
        return True
        
    else:
        print("❌ Function generation failed")
        return False


if __name__ == "__main__":
    test_logic_only_approach()
