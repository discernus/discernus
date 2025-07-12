# SOAR v2.0 Phase 1 Implementation Context
## Fixing Framework-Guided Analysis with Hybrid Architecture

**Date**: January 11, 2025  
**Status**: Implementation Ready  
**Priority**: Critical - Core functionality missing  
**Approach**: Hybrid FrameworkAnalyzer + Enhanced ThinOrchestrator

---

## Executive Summary

SOAR 1.0 infrastructure is complete but **framework specifications never reach analysis agents**, causing complete analysis failure. We need to implement a **hybrid architecture** that provides both direct framework application and complex orchestration capabilities.

### The Problem
- ✅ CLI, validation, and orchestration work perfectly
- ❌ **Framework context completely isolated** from analysis execution
- ❌ System produces generic conversation instead of framework-guided analysis
- ❌ Test case `soar execute examples/soar_cff_sample_project` fails completely

### The Solution: Hybrid Architecture (Option 3)
1. **FrameworkAnalyzer**: Simple, direct framework application for systematic analysis
2. **Enhanced ThinOrchestrator**: Complex multi-agent synthesis and debate orchestration  
3. **CLI Intelligence**: Chooses approach based on project complexity
4. **Framework Context Injection**: Bridge the gap between validation and execution

---

## Current Infrastructure Analysis

### ✅ Working Components (Leverage, Don't Rebuild)

**SOAR Infrastructure**:
- `FrameworkLoader` (455 lines): Loads and validates frameworks successfully
- `ValidationAgent` (500 lines): Comprehensive project validation with rubrics
- `ThinOrchestrator` (996 lines): Multi-agent conversation orchestration
- `soar_cli.py`: Complete CLI with validate/execute commands

**Sample Project**:
- `examples/soar_cff_sample_project/`: Complete CFF v3.1 test case
- 8 political speeches across 4 ideological categories
- Detailed experiment design with statistical analysis plan
- Expected outputs: CFF dimension scores with evidence citations

### ❌ Critical Gap (Fix Required)

**Framework Context Isolation**:
```python
# CURRENT BROKEN FLOW:
1. CLI loads project → FrameworkLoader validates framework ✅
2. CLI creates ResearchConfig(research_question, source_texts) ❌ NO FRAMEWORK
3. ThinOrchestrator runs generic analysis ❌ FRAMEWORK IGNORED
4. Results: Generic conversation about "CFF" → Citation File Format ❌

# NEEDED WORKING FLOW:
1. CLI loads project → FrameworkLoader validates framework ✅
2. CLI creates ResearchConfig(research_question, source_texts, FRAMEWORK_SPEC) ✅
3. FrameworkAnalyzer OR Enhanced ThinOrchestrator applies framework ✅
4. Results: CFF dimension scores with textual evidence ✅
```

---

## Technical Implementation Details

### 1. Research Question Extraction Fix (15 minutes)

**Current Broken Code** (`soar_cli.py:314-322`):
```python
# Simple extraction - look for research question
lines = experiment_content.split('\n')
for line in lines:
    if 'research question' in line.lower() and ':' in line:
        research_question = line.split(':', 1)[1].strip()
        break
```

**Problem**: experiment.md uses section headers `## Research Question` not inline format

**Fix**: Parse markdown sections properly
```python
def _extract_research_question(experiment_content: str) -> str:
    """Extract research question from experiment.md markdown"""
    lines = experiment_content.split('\n')
    in_research_section = False
    
    for line in lines:
        line = line.strip()
        
        # Check for research question section header
        if line.lower().startswith('## research question'):
            in_research_section = True
            continue
            
        # If we're in the research section and find a non-empty line
        if in_research_section and line and not line.startswith('#'):
            # Look for primary question
            if line.startswith('**Primary Question**:'):
                return line.split(':', 1)[1].strip()
            # Or just return first substantial line
            return line
            
        # Stop if we hit another section
        if in_research_section and line.startswith('##'):
            break
    
    return "Research question not found"
```

### 2. ResearchConfig Enhancement (10 minutes)

**Current Code** (`discernus/orchestration/orchestrator.py:85-90`):
```python
@dataclass
class ResearchConfig:
    """Minimal research session configuration"""
    research_question: str
    source_texts: str
    enable_code_execution: bool = True
    dev_mode: bool = False
    simulated_researcher_profile: str = "experienced_computational_social_scientist"
```

**Enhancement**: Add framework specification field
```python
@dataclass
class ResearchConfig:
    """Research session configuration with framework support"""
    research_question: str
    source_texts: str
    framework_specification: Optional[str] = None  # NEW FIELD
    framework_name: Optional[str] = None  # NEW FIELD
    enable_code_execution: bool = True
    dev_mode: bool = False
    simulated_researcher_profile: str = "experienced_computational_social_scientist"
```

### 3. CLI Framework Integration (20 minutes)

**Current Code** (`soar_cli.py:125-140`):
```python
# Load project components
framework_loader = FrameworkLoader()
project_components = _load_project_components(project_path, framework_loader)

# Create research configuration
config = ResearchConfig(
    research_question=project_components['research_question'],
    source_texts=project_components['corpus_description'],  # WRONG - NOT ACTUAL CORPUS
    enable_code_execution=True,
    dev_mode=dev_mode,
    simulated_researcher_profile=researcher_profile if dev_mode else None
)
```

**Enhancement**: Load framework and actual corpus
```python
# Load project components INCLUDING framework
framework_loader = FrameworkLoader()
project_components = _load_project_components(project_path, framework_loader)

# Load framework specification
framework_path = Path(project_path) / "framework.md"
framework_spec = None
framework_name = None
if framework_path.exists():
    framework_spec = framework_loader.load_framework_specification(str(framework_path))
    framework_name = framework_spec.get('name', 'Unknown Framework')

# Load actual corpus content
corpus_path = Path(project_path) / "corpus"
corpus_content = _load_corpus_content(corpus_path)

# Create enhanced research configuration
config = ResearchConfig(
    research_question=project_components['research_question'],
    source_texts=corpus_content,  # ACTUAL CORPUS CONTENT
    framework_specification=framework_spec,  # FRAMEWORK SPECIFICATION
    framework_name=framework_name,  # FRAMEWORK NAME
    enable_code_execution=True,
    dev_mode=dev_mode,
    simulated_researcher_profile=researcher_profile if dev_mode else None
)
```

### 4. FrameworkAnalyzer Implementation (2-3 hours)

**Create New File**: `discernus/core/framework_analyzer.py`

```python
#!/usr/bin/env python3
"""
SOAR Framework Analyzer
======================

Simple, direct framework application for systematic text analysis.
Part of SOAR v2.0 hybrid architecture.

THIN Principle: Use LLM intelligence to apply framework specifications 
directly to texts without complex orchestration overhead.
"""

from typing import Dict, List, Any, Optional
from pathlib import Path
import json

class FrameworkAnalyzer:
    """
    Direct framework application engine
    
    Provides systematic framework-guided analysis without orchestration complexity.
    Designed for single-framework, multi-text analysis scenarios.
    """
    
    def __init__(self, llm_client):
        self.llm_client = llm_client
    
    async def analyze_corpus_with_framework(self, 
                                          corpus_texts: Dict[str, str],
                                          framework_spec: Dict[str, Any],
                                          research_question: str) -> Dict[str, Any]:
        """
        Apply framework systematically to corpus texts
        
        Args:
            corpus_texts: {"filename": "content", ...}
            framework_spec: Complete framework specification
            research_question: Research question for context
            
        Returns:
            Complete framework-guided analysis results
        """
        
        results = {
            'framework_name': framework_spec.get('name', 'Unknown'),
            'research_question': research_question,
            'text_analyses': {},
            'synthesis': None,
            'metadata': {
                'texts_analyzed': len(corpus_texts),
                'framework_dimensions': len(framework_spec.get('dimensions', [])),
                'analysis_type': 'systematic_framework_application'
            }
        }
        
        # Analyze each text individually with framework
        for filename, content in corpus_texts.items():
            text_analysis = await self._analyze_single_text(
                filename, content, framework_spec, research_question
            )
            results['text_analyses'][filename] = text_analysis
        
        # Generate synthesis across all texts
        results['synthesis'] = await self._synthesize_framework_results(
            results['text_analyses'], framework_spec, research_question
        )
        
        return results
    
    async def _analyze_single_text(self, 
                                 filename: str,
                                 content: str, 
                                 framework_spec: Dict[str, Any],
                                 research_question: str) -> Dict[str, Any]:
        """Apply framework to single text"""
        
        # Build framework-specific analysis prompt
        analysis_prompt = self._build_framework_prompt(
            filename, content, framework_spec, research_question
        )
        
        # Get LLM analysis
        analysis_response = await self.llm_client.call_llm(
            analysis_prompt, "framework_analyzer"
        )
        
        # Parse structured response (LLM should return JSON)
        try:
            structured_analysis = json.loads(analysis_response)
        except json.JSONDecodeError:
            # Fallback: Use LLM to structure the response
            structure_prompt = f"""
            Convert this analysis into structured JSON format:
            
            Framework: {framework_spec.get('name')}
            Analysis: {analysis_response}
            
            Return JSON with framework dimensions and scores.
            """
            structured_response = await self.llm_client.call_llm(
                structure_prompt, "framework_analyzer"
            )
            try:
                structured_analysis = json.loads(structured_response)
            except:
                structured_analysis = {
                    'error': 'Could not structure analysis',
                    'raw_analysis': analysis_response
                }
        
        return structured_analysis
    
    def _build_framework_prompt(self, 
                              filename: str,
                              content: str,
                              framework_spec: Dict[str, Any],
                              research_question: str) -> str:
        """Build framework-specific analysis prompt"""
        
        framework_name = framework_spec.get('name', 'Unknown Framework')
        dimensions = framework_spec.get('dimensions', [])
        
        prompt = f"""# {framework_name} Framework Analysis

## Research Context
**Research Question**: {research_question}
**Text**: {filename}

## Framework Specification
**Framework**: {framework_name}
**Description**: {framework_spec.get('description', 'No description')}

## Analysis Dimensions
"""
        
        # Add each dimension with detailed instructions
        for dim in dimensions:
            prompt += f"""
### {dim.get('name', 'Unknown Dimension')}
**Description**: {dim.get('description', 'No description')}
**Scale**: {dim.get('scale', 'No scale specified')}
**Markers**: {dim.get('markers', 'No markers specified')}
"""
        
        prompt += f"""

## Text to Analyze
```
{content[:10000]}  # Limit to first 10k chars to avoid token limits
```

## Analysis Instructions

Apply the {framework_name} framework systematically to this text. For each dimension:

1. **Score**: Provide numerical score according to dimension scale
2. **Evidence**: Quote specific text passages that justify the score
3. **Reasoning**: Explain how the evidence connects to the score

## Required Output Format

Return your analysis as valid JSON:

```json
{{
    "text_filename": "{filename}",
    "framework_name": "{framework_name}",
    "dimensions": [
        {{
            "name": "dimension_name",
            "score": numeric_score,
            "evidence": ["quote 1", "quote 2"],
            "reasoning": "explanation of score"
        }}
    ],
    "overall_assessment": "summary of text according to framework",
    "confidence": "high/medium/low",
    "notes": "any additional observations"
}}
```

Begin analysis:
"""
        
        return prompt
    
    async def _synthesize_framework_results(self,
                                          text_analyses: Dict[str, Dict],
                                          framework_spec: Dict[str, Any],
                                          research_question: str) -> Dict[str, Any]:
        """Generate synthesis across all framework analyses"""
        
        synthesis_prompt = f"""# Framework Synthesis Analysis

## Research Question
{research_question}

## Framework
{framework_spec.get('name', 'Unknown Framework')}

## Individual Text Analyses
"""
        
        for filename, analysis in text_analyses.items():
            synthesis_prompt += f"\n### {filename}\n{json.dumps(analysis, indent=2)}\n"
        
        synthesis_prompt += """

## Synthesis Task

Analyze the results across all texts according to the research question:

1. **Patterns**: What patterns emerge across texts?
2. **Comparisons**: How do texts compare on framework dimensions?
3. **Insights**: What insights does framework analysis reveal?
4. **Conclusions**: What conclusions answer the research question?

Return synthesis as JSON:

```json
{
    "research_question": "the research question",
    "framework_patterns": "patterns across texts",
    "comparative_analysis": "how texts compare",
    "key_insights": "main insights from framework application",
    "conclusions": "conclusions that answer research question",
    "statistical_summary": "quantitative patterns if applicable"
}
```
"""
        
        synthesis_response = await self.llm_client.call_llm(
            synthesis_prompt, "framework_synthesis"
        )
        
        try:
            return json.loads(synthesis_response)
        except:
            return {
                'error': 'Could not structure synthesis',
                'raw_synthesis': synthesis_response
            }
```

### 5. CLI Intelligence Implementation (30 minutes)

**Enhance** `soar_cli.py` execute command:

```python
async def _execute_orchestration(config: ResearchConfig, project_path: str) -> Dict[str, Any]:
    """Execute using hybrid architecture - choose approach based on project needs"""
    
    # Decide on execution approach
    if config.framework_specification and _is_simple_framework_analysis(config):
        # Use direct FrameworkAnalyzer for systematic framework application
        return await _execute_with_framework_analyzer(config, project_path)
    else:
        # Use enhanced ThinOrchestrator for complex orchestration
        return await _execute_with_orchestrator(config, project_path)

def _is_simple_framework_analysis(config: ResearchConfig) -> bool:
    """Determine if this is a simple framework analysis case"""
    # Simple heuristics - can be enhanced later
    has_framework = config.framework_specification is not None
    reasonable_corpus_size = len(config.source_texts) < 100000  # Under 100k chars
    
    return has_framework and reasonable_corpus_size

async def _execute_with_framework_analyzer(config: ResearchConfig, project_path: str) -> Dict[str, Any]:
    """Execute using direct FrameworkAnalyzer"""
    
    from discernus.core.framework_analyzer import FrameworkAnalyzer
    from discernus.core.thin_litellm_client import ThinLiteLLMClient
    
    # Initialize analyzer
    llm_client = ThinLiteLLMClient()
    analyzer = FrameworkAnalyzer(llm_client)
    
    # Parse corpus into individual texts
    corpus_texts = _parse_corpus_content(config.source_texts)
    
    # Run framework analysis
    results = await analyzer.analyze_corpus_with_framework(
        corpus_texts=corpus_texts,
        framework_spec=config.framework_specification,
        research_question=config.research_question
    )
    
    # Save results to project directory
    results_path = Path(project_path) / "results"
    results_path.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    result_file = results_path / f"framework_analysis_{timestamp}.json"
    
    with open(result_file, 'w') as f:
        json.dump(results, f, indent=2)
    
    return {
        'status': 'completed',
        'approach': 'framework_analyzer',
        'results_file': str(result_file),
        'texts_analyzed': results['metadata']['texts_analyzed'],
        'framework_name': results['framework_name']
    }

async def _execute_with_orchestrator(config: ResearchConfig, project_path: str) -> Dict[str, Any]:
    """Execute using enhanced ThinOrchestrator"""
    
    # Enhance orchestrator prompts with framework context if available
    if config.framework_specification:
        # Inject framework context into design prompts
        enhanced_orchestrator = _create_framework_enhanced_orchestrator(config)
    else:
        # Use standard orchestrator
        enhanced_orchestrator = ThinOrchestrator(str(project_root), str(results_path))
    
    # Continue with existing orchestration logic...
    # (This maintains compatibility with existing complex orchestration)
```

---

## Validation Criteria

### Phase 1 Success Criteria

**✅ Research Question Extraction**:
```bash
soar execute examples/soar_cff_sample_project --dev-mode
# Should show: "🔬 Research Question: How do political speeches from different ideological orientations..."
# NOT: "🔬 Research Question: Research question not found"
```

**✅ Framework Loading**:
- CLI successfully loads CFF v3.1 framework specification
- Framework context available in ResearchConfig
- FrameworkAnalyzer receives complete framework specification

**✅ Systematic Framework Application**:
- Analysis produces CFF dimension scores (-1.0 to +1.0)
- Each text gets systematic framework analysis with evidence citations
- Results show framework-specific analysis, not generic conversation

**✅ Correct Corpus Processing**:
- System analyzes political speeches from corpus/ directory
- NOT software metadata or unrelated content
- All 8 speeches processed with framework application

### Testing Protocol

**1. Quick Validation** (5 minutes):
```bash
# Test research question extraction
python3 -c "
from soar_cli import _load_project_components
from discernus.core.framework_loader import FrameworkLoader
components = _load_project_components('examples/soar_cff_sample_project', FrameworkLoader())
print('Research Question:', components['research_question'])
"
```

**2. Framework Loading Test** (5 minutes):
```bash
# Test framework loading
python3 -c "
from discernus.core.framework_loader import FrameworkLoader
loader = FrameworkLoader()
spec = loader.load_framework_specification('examples/soar_cff_sample_project/framework.md')
print('Framework Name:', spec.get('name'))
print('Dimensions:', len(spec.get('dimensions', [])))
"
```

**3. End-to-End Test** (10 minutes):
```bash
# Full execution test
soar execute examples/soar_cff_sample_project --dev-mode

# Expected output:
# ✅ Framework analysis completed
# ✅ 8 texts analyzed with CFF v3.1
# ✅ Results contain dimension scores with evidence
# ✅ Generated analysis focuses on political rhetoric, not software
```

---

## Implementation Priority

### Immediate (Fix Today):
1. ✅ **Research Question Extraction Fix** - 15 minutes
2. ✅ **ResearchConfig Enhancement** - 10 minutes  
3. ✅ **CLI Framework Integration** - 20 minutes

### Short Term (This Week):
4. ✅ **FrameworkAnalyzer Implementation** - 2-3 hours
5. ✅ **CLI Intelligence** - 30 minutes
6. ✅ **End-to-End Testing** - 1 hour

### Medium Term (Next Week):
7. ⏳ **Enhanced ThinOrchestrator** - Framework context injection
8. ⏳ **Cost Estimation Integration** - LiteLLM cost tracking
9. ⏳ **Configuration Management** - YAML config system

---

## Success Indicators

### Technical Success
- ✅ `soar execute examples/soar_cff_sample_project` completes successfully
- ✅ Framework specification reaches analysis components
- ✅ Systematic CFF v3.1 application visible in results
- ✅ Political speeches analyzed (not software metadata)

### Architectural Success  
- ✅ Hybrid approach provides both direct analysis and complex orchestration
- ✅ CLI intelligently chooses execution approach
- ✅ Framework-agnostic design supports any analytical framework
- ✅ Maintains compatibility with existing infrastructure

### User Experience Success
- ✅ No changes to CLI interface - existing commands work better
- ✅ Clear framework-guided results instead of generic conversation
- ✅ Publication-ready analysis outputs
- ✅ Complete audit trail and provenance

---

## Context for Fresh Agent

**You are implementing the critical fix that makes SOAR v2.0 work**. The infrastructure exists, but framework specifications are completely isolated from analysis execution. Your job is to build the bridge using a hybrid architecture that provides both simple direct analysis and complex orchestration capabilities.

**Start with the immediate fixes** (research question extraction, ResearchConfig enhancement, CLI integration) to get the basic flow working, then implement FrameworkAnalyzer for systematic framework application.

**The test case is ready**: `examples/soar_cff_sample_project` is a complete, real-world test that will validate your implementation. When this test produces CFF dimension scores with evidence citations instead of generic conversation about software, you've succeeded.

**This is THIN architecture**: Use LLM intelligence to apply frameworks, don't build complex parsing or rule-based systems. The framework specifications tell LLMs what to do - your job is to make sure LLMs receive those specifications. 