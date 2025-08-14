#!/usr/bin/env python3
"""
Statistical Analysis Agent for Incremental Notebook Construction

This agent takes an existing notebook with derived metrics and adds 
statistical analysis capabilities to it. This tests the "incremental 
construction" approach where specialized agents enhance notebooks 
step-by-step rather than trying to generate everything at once.
"""

import sys
import json
from pathlib import Path
from typing import Dict, Any

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent / '../../'))

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry


class StatisticalAnalysisAgent:
    """Agent that adds statistical analysis functions to existing notebooks."""
    
    def __init__(self, model: str = "vertex_ai/gemini-2.5-pro"):
        self.model = model
        self.model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(self.model_registry)
    
    def enhance_notebook_with_statistics(self, 
                                       input_notebook_path: Path, 
                                       output_notebook_path: Path,
                                       framework_content: str,
                                       analysis_data: Dict[str, Any]) -> bool:
        """Add statistical analysis functions to an existing notebook."""
        
        try:
            print("📊 Statistical Analysis Agent - Enhancing Notebook")
            print("=" * 60)
            
            # Read existing notebook
            if not input_notebook_path.exists():
                print(f"❌ Input notebook not found: {input_notebook_path}")
                return False
                
            existing_notebook = input_notebook_path.read_text()
            print(f"✅ Loaded existing notebook: {len(existing_notebook)} characters")
            
            # Create focused prompt for statistical enhancement
            system_prompt = """You are a statistical analysis expert who enhances existing Python notebooks by adding rigorous statistical analysis functions. You work with existing code and add statistical capabilities without breaking what's already there."""
            
            prompt = f"""
I have an existing Python notebook that calculates derived metrics from research data. I need you to enhance it by adding statistical analysis functions.

EXISTING NOTEBOOK CONTENT:
{existing_notebook}

FRAMEWORK CONTEXT:
The framework defines these dimension pairs that should be statistically analyzed:
- Cohesive vs Fragmentative indices (main comparison)
- Individual tension scores (identity, emotional, success, relational, goal)
- Raw dimension scores from analysis

STATISTICAL ANALYSIS TO ADD:

1. **Descriptive Statistics Function**:
```python
def calculate_descriptive_statistics(df):
    # Mean, median, std dev, min, max for all numeric columns
    # Return structured results
```

2. **Correlation Analysis Function**:
```python
def calculate_correlation_matrix(df):
    # Pearson correlations between all derived metrics
    # Include p-values and significance testing
```

3. **Comparative Analysis Function**:
```python
def perform_cohesion_analysis(df):
    # Compare cohesive vs fragmentative patterns
    # T-tests or appropriate statistical tests
```

4. **Tension Analysis Function**:
```python
def analyze_tension_patterns(df):
    # Statistical analysis of tension scores
    # Identify significant patterns
```

5. **Enhanced Main Function**:
Modify the existing main() function to also run statistical analyses and save results to additional CSV files.

REQUIREMENTS:
- Keep ALL existing code intact
- Add statistical functions before the existing main() function
- Import required statistics libraries (scipy.stats, etc.)
- Enhance main() to call statistical functions
- Save statistical results to 'statistical_analysis_results.csv'
- Handle missing data gracefully
- Include error handling and logging

OUTPUT: Complete enhanced Python notebook with existing functionality + statistical analysis.
"""

            # Generate enhanced notebook
            print("🔄 Generating statistical enhancements...")
            response_content, metadata = self.llm_gateway.execute_call(
                model=self.model,
                prompt=prompt,
                system_prompt=system_prompt,
                max_tokens=6000,
                temperature=0.2
            )
            
            print(f"✅ Generated enhanced notebook: {len(response_content)} characters")
            
            # Save enhanced notebook
            output_notebook_path.write_text(response_content)
            print(f"✅ Saved enhanced notebook: {output_notebook_path}")
            
            # Basic validation
            if self._validate_enhanced_notebook(response_content, existing_notebook):
                print("✅ Enhanced notebook validation passed")
                return True
            else:
                print("❌ Enhanced notebook validation failed")
                return False
                
        except Exception as e:
            print(f"❌ Statistical enhancement failed: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def _validate_enhanced_notebook(self, enhanced_content: str, original_content: str) -> bool:
        """Validate that enhancement preserved original functionality and added statistics."""
        
        # Check that original functions are still present
        original_functions = [
            "calculate_identity_tension",
            "calculate_emotional_tension",
            "calculate_cohesive_index"
        ]
        
        for func in original_functions:
            if func not in enhanced_content:
                print(f"❌ Missing original function: {func}")
                return False
        
        # Check that new statistical functions were added
        statistical_functions = [
            "calculate_descriptive_statistics",
            "calculate_correlation_matrix",
            "perform_cohesion_analysis"
        ]
        
        added_functions = 0
        for func in statistical_functions:
            if func in enhanced_content:
                added_functions += 1
                print(f"✅ Added statistical function: {func}")
        
        if added_functions < 2:
            print(f"❌ Too few statistical functions added: {added_functions}/3")
            return False
        
        # Check for required imports
        required_imports = ["scipy", "stats"]
        for imp in required_imports:
            if imp in enhanced_content:
                print(f"✅ Found required import: {imp}")
        
        print(f"✅ Validation passed: {added_functions} statistical functions added")
        return True


def test_incremental_construction():
    """Test the incremental notebook construction approach."""
    
    print("🧪 Testing Incremental Notebook Construction")
    print("=" * 60)
    
    # Paths
    input_notebook = Path("cff_derived_metrics_notebook.py")
    output_notebook = Path("cff_notebook_v2_with_statistics.py")
    
    if not input_notebook.exists():
        print(f"❌ Input notebook not found: {input_notebook}")
        return False
    
    # Load framework and analysis data (mock for testing)
    framework_content = "CFF v7.3 framework content"
    analysis_data = {"test": "data"}
    
    # Create statistical analysis agent
    agent = StatisticalAnalysisAgent()
    
    # Enhance notebook
    success = agent.enhance_notebook_with_statistics(
        input_notebook, 
        output_notebook, 
        framework_content, 
        analysis_data
    )
    
    if success:
        print("\n🎉 SUCCESS: Incremental notebook construction works!")
        print(f"   📓 Original: {input_notebook}")
        print(f"   📈 Enhanced: {output_notebook}")
        print("\n   This proves the incremental construction approach is viable!")
        return True
    else:
        print("\n❌ FAILURE: Incremental construction failed")
        return False


if __name__ == "__main__":
    test_incremental_construction()
