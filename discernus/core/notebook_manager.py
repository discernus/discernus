#!/usr/bin/env python3
"""
Research Notebook Manager
========================

THIN Principle: Automatically create Jupyter notebooks for important research calculations
while letting agents determine what constitutes "important" vs "transient" calculations.

Maintains experiment provenance by capturing significant computational analyses.
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional
import nbformat as nbf

class NotebookManager:
    """
    Manages creation of research notebooks for experiment results
    
    THIN Principle: Infrastructure creates notebooks, agents indicate importance
    """
    
    def __init__(self, session_id: str, project_root: str = "."):
        self.session_id = session_id
        self.project_root = Path(project_root)
        self.session_path = self.project_root / "research_sessions" / session_id
        self.notebook_path = self.session_path / "results_notebook.ipynb"
        
        # Initialize or load existing notebook
        self.notebook = self._load_or_create_notebook()
        
    def _load_or_create_notebook(self) -> nbf.NotebookNode:
        """Load existing notebook or create new one"""
        
        if self.notebook_path.exists():
            with open(self.notebook_path, 'r') as f:
                return nbf.read(f, as_version=4)
        else:
            # Create new notebook with header
            nb = nbf.v4.new_notebook()
            
            # Add title cell
            title_cell = nbf.v4.new_markdown_cell(f"""
# Research Session Results

**Session ID**: {self.session_id}  
**Created**: {time.strftime('%Y-%m-%d %H:%M:%S UTC')}

This notebook contains the important computational analyses and results from this research session.

---
""")
            nb.cells.append(title_cell)
            
            return nb
    
    def add_calculation(self, 
                       calculation_data: Dict[str, Any],
                       importance_level: str = "medium") -> bool:
        """
        Add a calculation to the research notebook if it meets importance criteria
        
        Args:
            calculation_data: {
                'code': str,
                'output': str, 
                'result_data': Any,
                'speaker': str,
                'context': str,
                'timestamp': float
            }
            importance_level: "low", "medium", "high"
            
        Returns:
            bool: True if added to notebook, False if deemed transient
        """
        
        # Determine if calculation should be saved to notebook
        should_save = self._assess_calculation_importance(calculation_data, importance_level)
        
        if not should_save:
            return False
        
        # Create markdown cell with context
        context_cell = nbf.v4.new_markdown_cell(f"""
## {calculation_data.get('speaker', 'Agent')} Analysis

**Time**: {time.strftime('%Y-%m-%d %H:%M:%S UTC', time.localtime(calculation_data.get('timestamp', time.time())))}  
**Context**: {calculation_data.get('context', 'Statistical analysis')}  
**Importance**: {importance_level.upper()}

---
""")
        
        # Create code cell
        code_cell = nbf.v4.new_code_cell(calculation_data['code'])
        
        # Create output cell if there's meaningful output
        if calculation_data.get('output') or calculation_data.get('result_data'):
            output_content = ""
            
            if calculation_data.get('output'):
                output_content += f"**Console Output:**\n```\n{calculation_data['output']}\n```\n\n"
            
            if calculation_data.get('result_data'):
                output_content += f"**Structured Results:**\n```json\n{json.dumps(calculation_data['result_data'], indent=2, default=str)}\n```"
            
            output_cell = nbf.v4.new_markdown_cell(output_content)
            
            # Add all cells
            self.notebook.cells.extend([context_cell, code_cell, output_cell])
        else:
            # Add context and code only
            self.notebook.cells.extend([context_cell, code_cell])
        
        # Save notebook
        self._save_notebook()
        return True
    
    def _assess_calculation_importance(self, 
                                     calculation_data: Dict[str, Any], 
                                     importance_level: str) -> bool:
        """
        Assess whether a calculation should be saved to the research notebook
        
        THIN Principle: Simple heuristics + agent guidance
        """
        
        code = calculation_data.get('code', '')
        output = calculation_data.get('output', '')
        result_data = calculation_data.get('result_data')
        
        # High importance: Always save
        if importance_level == "high":
            return True
        
        # Low importance: Save only if agent explicitly indicates
        if importance_level == "low":
            # Look for explicit importance indicators in code comments
            return any(indicator in code.lower() for indicator in [
                '# important', '# save', '# research result', '# notebook'
            ])
        
        # Medium importance: Apply heuristics
        importance_indicators = {
            # Statistical analysis
            'statistical_keywords': ['correlation', 'regression', 'significance', 'p-value', 'chi-square', 't-test'],
            'data_science_ops': ['groupby', 'merge', 'pivot', 'aggregate', 'transform'],
            'visualization': ['plot', 'chart', 'graph', 'figure', 'visualization'],
            'machine_learning': ['model', 'predict', 'classify', 'cluster', 'accuracy', 'score'],
            'research_outputs': ['result_data =', 'findings =', 'conclusion =', 'summary ='],
        }
        
        # Count importance indicators
        importance_score = 0
        code_lower = code.lower()
        
        for category, keywords in importance_indicators.items():
            if any(keyword in code_lower for keyword in keywords):
                importance_score += 1
        
        # Additional factors
        if result_data:  # Has structured output
            importance_score += 2
        
        if len(code) > 200:  # Substantial calculation
            importance_score += 1
        
        if any(word in output.lower() for word in ['error', 'warning']) and importance_score > 0:
            importance_score -= 1  # Reduce score for errors unless other indicators present
        
        # Save if importance score >= 2
        return importance_score >= 2
    
    def add_research_summary(self, summary: str, final_results: Dict[str, Any] = None):
        """Add final research summary to notebook"""
        
        summary_cell = nbf.v4.new_markdown_cell(f"""
---

# Research Summary

{summary}

**Final Analysis Timestamp**: {time.strftime('%Y-%m-%d %H:%M:%S UTC')}
""")
        
        self.notebook.cells.append(summary_cell)
        
        if final_results:
            results_cell = nbf.v4.new_markdown_cell(f"""
## Key Results

```json
{json.dumps(final_results, indent=2, default=str)}
```
""")
            self.notebook.cells.append(results_cell)
        
        self._save_notebook()
    
    def _save_notebook(self):
        """Save notebook to file"""
        self.session_path.mkdir(parents=True, exist_ok=True)
        
        with open(self.notebook_path, 'w') as f:
            nbf.write(self.notebook, f)
    
    def get_notebook_path(self) -> Path:
        """Get path to the research notebook"""
        return self.notebook_path

def enhance_code_execution_with_notebook(conversation_id: str, 
                                       speaker: str, 
                                       calculation_data: Dict[str, Any]) -> bool:
    """
    Enhanced code execution that automatically manages research notebooks
    
    THIN Principle: Infrastructure makes notebook decisions, agents provide hints
    """
    
    # Determine importance level from agent context
    importance_level = _detect_importance_level(calculation_data, speaker)
    
    # Create/update research notebook
    notebook_manager = NotebookManager(conversation_id)
    
    # Add context about the speaker and purpose
    calculation_data['context'] = _infer_calculation_context(calculation_data, speaker)
    
    # Try to add to notebook
    added_to_notebook = notebook_manager.add_calculation(calculation_data, importance_level)
    
    if added_to_notebook:
        print(f"📓 Important calculation saved to research notebook: {notebook_manager.get_notebook_path()}")
    
    return added_to_notebook

def _detect_importance_level(calculation_data: Dict[str, Any], speaker: str) -> str:
    """
    Detect importance level from calculation context
    
    THIN Principle: Simple heuristics based on agent behavior
    """
    
    code = calculation_data.get('code', '').lower()
    
    # High importance indicators
    high_importance_signals = [
        'final', 'result', 'conclusion', 'summary', 'report',
        'significant', 'important', 'key finding', 'main result'
    ]
    
    if any(signal in code for signal in high_importance_signals):
        return "high"
    
    # Speaker-based importance
    if speaker in ['data_science_expert', 'discernuslibrarian_agent']:
        return "medium"  # These experts typically do important work
    
    if speaker in ['moderator_llm']:
        return "high"  # Moderator calculations are usually synthesis
    
    # Default
    return "medium"

def _infer_calculation_context(calculation_data: Dict[str, Any], speaker: str) -> str:
    """Infer what type of calculation this is for context"""
    
    code = calculation_data.get('code', '').lower()
    
    # Context patterns
    if any(word in code for word in ['correlation', 'regression', 'model']):
        return "Statistical Analysis"
    elif any(word in code for word in ['plot', 'chart', 'visualization']):
        return "Data Visualization"
    elif any(word in code for word in ['count', 'frequency', 'distribution']):
        return "Descriptive Statistics"
    elif any(word in code for word in ['test', 'hypothesis', 'significance']):
        return "Hypothesis Testing"
    elif speaker == 'discernuslibrarian_agent':
        return "Literature Analysis"
    elif speaker == 'corpus_detective_agent':
        return "Corpus Analysis"
    else:
        return "Computational Analysis"

if __name__ == "__main__":
    # Test notebook functionality
    test_calculation = {
        'code': '''
import pandas as pd
import numpy as np

# Important statistical analysis
data = pd.DataFrame({'A': [1,2,3,4,5], 'B': [2,4,6,8,10]})
correlation = data.corr()
print("Correlation analysis:")
print(correlation)

# Store important result
result_data = {
    'correlation_coefficient': correlation.iloc[0,1],
    'interpretation': 'Strong positive correlation'
}
''',
        'output': 'Correlation analysis:\n     A    B\nA  1.0  1.0\nB  1.0  1.0',
        'result_data': {'correlation_coefficient': 1.0, 'interpretation': 'Strong positive correlation'},
        'speaker': 'data_science_expert',
        'timestamp': time.time()
    }
    
    # Test the system
    added = enhance_code_execution_with_notebook("test_session", "data_science_expert", test_calculation)
    print(f"Test calculation added to notebook: {added}") 