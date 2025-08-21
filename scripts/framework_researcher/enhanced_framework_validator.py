#!/usr/bin/env python3
"""
Enhanced Framework Validator: Integrated Structural + Academic Validation
Combines framework specification compliance with academic literature grounding
"""
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, Any, Optional, List

# Add project root to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from discernus.gateway.llm_gateway import LLMGateway
from discernus.gateway.model_registry import ModelRegistry

class EnhancedFrameworkValidator:
    """
    Enhanced Framework Validator that combines:
    1. Structural validation (specification compliance)
    2. Academic validation (literature grounding and credibility)
    """
    
    def __init__(self):
        """Initialize the enhanced validator with LLM gateway"""
        self.model_registry = ModelRegistry()
        self.llm_gateway = LLMGateway(self.model_registry)
        
        # Model selection for different validation phases
        self.structural_model = "vertex_ai/gemini-2.5-pro"  # For framework analysis
        self.academic_model = "vertex_ai/gemini-2.5-pro"    # For academic validation
        
        print("🔍 Enhanced Framework Validator initialized")
        print("📚 Combines structural compliance + academic validation")
    
    def validate_framework(self, framework_path: str, enable_academic_validation: bool = True, verbose: bool = False, generate_research_directions: bool = False) -> Dict[str, Any]:
        """
        Comprehensive framework validation with optional academic grounding
        
        Args:
            framework_path: Path to framework file
            enable_academic_validation: Whether to perform academic validation
            verbose: Whether to include detailed LLM responses and analysis
            generate_research_directions: Whether to generate research directions for valid frameworks
        
        Returns:
            Comprehensive validation results
        """
        print(f"\n🔍 Validating framework: {framework_path}")
        
        # Phase 1: Structural Validation
        print("📋 Phase 1: Structural Validation...")
        structural_results = self._validate_structure(framework_path, verbose)
        print(f"📋 Structural validation results: {structural_results}")
        
        # Phase 2: Academic Validation (if enabled)
        academic_results = None
        if enable_academic_validation and structural_results.get('status') == 'PASSED':
            print("📚 Phase 2: Academic Validation...")
            academic_results = self._validate_academic_grounding(framework_path, structural_results, verbose)
        else:
            print(f"📚 Phase 2: Academic validation skipped - structural status: {structural_results.get('status', 'UNKNOWN')}")
        
        # Phase 3: Integrated Assessment
        print("🎯 Phase 3: Integrated Assessment...")
        integrated_results = self._integrate_validation_results(structural_results, academic_results)
        print(f"🎯 Integrated assessment results: {integrated_results}")
        
        # Phase 4: Research Directions Generation (if enabled and framework passed or has warnings)
        research_directions = None
        if generate_research_directions and structural_results.get('status') in ['PASSED', 'WARNING']:
            print("🔬 Phase 4: Research Directions Generation...")
            research_directions = self._generate_research_directions(framework_path, structural_results, academic_results, verbose)
        elif generate_research_directions:
            print(f"🔬 Phase 4: Research directions generation skipped - framework did not pass structural validation")
        
        # Generate comprehensive report
        final_report = self._generate_enhanced_report(framework_path, structural_results, academic_results, integrated_results, verbose, research_directions)
        
        return {
            'framework_path': framework_path,
            'structural_validation': structural_results,
            'academic_validation': academic_results,
            'integrated_assessment': integrated_results,
            'research_directions': research_directions,
            'final_report': final_report,
            'validation_timestamp': self._get_timestamp(),
            'verbose_mode': verbose
        }
    
    def _validate_structure(self, framework_path: str, verbose: bool = False) -> Dict[str, Any]:
        """Phase 1: Structural validation using LLM analysis"""
        
        # Load framework content
        try:
            with open(framework_path, 'r', encoding='utf-8') as f:
                framework_content = f.read()
        except Exception as e:
            return {
                'status': 'ERROR',
                'error': f'Failed to read framework file: {e}',
                'details': None
            }
        
        # Load framework specification
        spec_content = self._load_framework_specification()
        
        # LLM-based structural validation
        prompt = f"""You are a framework validation expert. Analyze this framework against the Discernus v10.0 specification.

FRAMEWORK CONTENT:
{framework_content}

FRAMEWORK SPECIFICATION:
{spec_content}

Analyze the framework for:
1. **Structural Compliance**: Does it follow the specification format?
2. **Content Quality**: Are all required sections present and well-formed?
3. **Coherence**: Is the framework internally consistent?
4. **Completeness**: Are all required elements present?

Provide a JSON response with:
{{
    "status": "PASSED|FAILED|WARNING",
    "structural_score": 0-10,
    "issues": [
        {{
            "type": "BLOCKING|QUALITY|SUGGESTION",
            "description": "Issue description",
            "impact": "Impact on framework execution",
            "fix": "How to resolve this issue"
        }}
    ],
    "summary": "Overall assessment of framework structure"
}}"""

        try:
            response, metadata = self.llm_gateway.execute_call(
                model=self.structural_model,
                prompt=prompt,
                system_prompt="You are a framework validation specialist. Provide clear, actionable feedback in JSON format.",
                temperature=0.1,
                max_tokens=8000
            )
            
            # Store raw response for verbose logging
            if verbose:
                structural_results = {
                    'raw_llm_response': response,
                    'llm_metadata': metadata,
                    'prompt_used': prompt[:1000] + "..." if len(prompt) > 1000 else prompt
                }
            else:
                structural_results = {}
            
            # Parse JSON response
            try:
                validation_data = json.loads(response)
                structural_results.update(validation_data)
                return structural_results
            except json.JSONDecodeError:
                # Try to find JSON in code blocks first
                if "```json" in response:
                    json_start = response.find("```json") + 7
                    json_end = response.rfind("```")
                    json_content = response[json_start:json_end].strip()
                    try:
                        validation_data = json.loads(json_content)
                        structural_results.update(validation_data)
                        return structural_results
                    except json.JSONDecodeError:
                        pass
                
                # Fallback parsing for partial responses
                fallback_data = self._parse_partial_validation_response(response)
                structural_results.update(fallback_data)
                return structural_results
                
        except Exception as e:
            error_result = {
                'status': 'ERROR',
                'error': f'LLM validation failed: {e}',
                'details': None
            }
            if verbose:
                error_result['prompt_used'] = prompt[:1000] + "..." if len(prompt) > 1000 else prompt
            return error_result
    
    def _validate_academic_grounding(self, framework_path: str, structural_results: Dict[str, Any], verbose: bool = False) -> Dict[str, Any]:
        """Phase 2: Academic validation using DiscernusLibrarian methodology"""
        
        # Extract theoretical content from framework
        theoretical_elements = self._extract_theoretical_content(framework_path)
        
        # Create research question for academic validation
        research_question = f"Validate the academic foundations and theoretical grounding of this framework: {theoretical_elements}"
        
        # Use LLM for academic validation (simplified version of DiscernusLibrarian)
        academic_prompt = f"""You are conducting academic validation of a research framework.

FRAMEWORK THEORETICAL CONTENT:
{theoretical_elements}

RESEARCH QUESTION: {research_question}

Conduct academic validation by:

1. **Theoretical Foundation Assessment**: Evaluate the academic credibility of theoretical claims
2. **Literature Support**: Identify what academic literature would support these claims
3. **Research Gap Analysis**: Identify potential gaps in academic support
4. **Methodological Validation**: Assess if the framework methodology aligns with academic standards
5. **Citation Quality**: Evaluate the quality and relevance of any citations provided

Provide a JSON response with:
{{
    "academic_credibility_score": 0-10,
    "theoretical_validation": "Assessment of theoretical foundations",
    "literature_coverage": "Analysis of academic literature support",
    "research_gaps": "Identified gaps in academic support",
    "methodological_validation": "Assessment of methodology alignment",
    "confidence_level": "HIGH|MEDIUM|LOW",
    "recommendations": "Specific recommendations for academic improvement"
}}"""

        try:
            response, metadata = self.llm_gateway.execute_call(
                model=self.academic_model,
                prompt=academic_prompt,
                max_tokens=8000
            )
            
            # Store raw response for verbose logging
            if verbose:
                academic_results = {
                    'raw_llm_response': response,
                    'llm_metadata': metadata,
                    'prompt_used': academic_prompt[:1000] + "..." if len(academic_prompt) > 1000 else academic_prompt,
                    'theoretical_content_extracted': theoretical_elements[:500] + "..." if len(theoretical_elements) > 500 else theoretical_elements
                }
            else:
                academic_results = {}
            
            # Parse JSON response
            try:
                academic_data = json.loads(response)
                academic_results.update(academic_data)
                return academic_results
            except json.JSONDecodeError:
                fallback_data = self._parse_partial_academic_response(response)
                academic_results.update(fallback_data)
                return academic_results
                
        except Exception as e:
            error_result = {
                'academic_credibility_score': 0,
                'error': f'Academic validation failed: {e}',
                'confidence_level': 'LOW'
            }
            if verbose:
                error_result['prompt_used'] = academic_prompt[:1000] + "..." if len(academic_prompt) > 1000 else academic_prompt
                error_result['theoretical_content_extracted'] = theoretical_elements[:500] + "..." if len(theoretical_elements) > 500 else theoretical_elements
            return error_result
    
    def _integrate_validation_results(self, structural_results: Dict[str, Any], academic_results: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """Phase 3: Integrate structural and academic validation results"""
        
        # Calculate integrated score
        structural_score = structural_results.get('structural_score', 0)
        academic_score = academic_results.get('academic_credibility_score', 0) if academic_results else 0
        
        # Weight the scores (structural: 60%, academic: 40%)
        integrated_score = (structural_score * 0.6) + (academic_score * 0.4)
        
        # Determine overall status
        if structural_results.get('status') == 'FAILED':
            overall_status = 'FAILED'
        elif integrated_score >= 8:
            overall_status = 'EXCELLENT'
        elif integrated_score >= 6:
            overall_status = 'GOOD'
        elif integrated_score >= 4:
            overall_status = 'FAIR'
        else:
            overall_status = 'POOR'
        
        return {
            'overall_score': round(integrated_score, 1),
            'overall_status': overall_status,
            'structural_weight': 0.6,
            'academic_weight': 0.4,
            'confidence_level': academic_results.get('confidence_level', 'UNKNOWN') if academic_results else 'UNKNOWN',
            'recommendations': self._generate_integrated_recommendations(structural_results, academic_results)
        }
    
    def _generate_research_directions(self, framework_path: str, structural_results: Dict[str, Any], 
                                     academic_results: Optional[Dict[str, Any]], verbose: bool = False) -> Dict[str, Any]:
        """Phase 4: Generate research directions for frameworks that pass validation"""
        
        framework_name = Path(framework_path).stem
        
        # Extract theoretical content for research direction generation
        theoretical_content = self._extract_theoretical_content(framework_path)
        
        # Generate research directions using LLM
        research_prompt = f"""This analytical framework has passed validation for compliance with the specification it is designed to match. You are an academic researcher who is seeking to identify literature review questions that, if answered, might make the framework more robust by grounding its dimensions, definitions, and derived metrics in the most relevant academic research.

FRAMEWORK:
{theoretical_content}

Please suggest one to three questions, arranged in priority order, that would guide future literature reviews.

Provide your response in markdown format with the following structure:

# Research Directions for {framework_name}

## Research Questions

### Priority 1: [Specific research question]
**Rationale**: [Why this question is important for this framework]
**Expected Outcomes**: [What insights this research would provide]
**Methodology Suggestions**: [Suggested research approaches and literature to examine]

### Priority 2: [Specific research question]
**Rationale**: [Why this question is important for this framework]
**Expected Outcomes**: [What insights this research would provide]
**Methodology Suggestions**: [Suggested research approaches and literature to examine]

### Priority 3: [Specific research question]
**Rationale**: [Why this question is important for this framework]
**Expected Outcomes**: [What insights this research would provide]
**Methodology Suggestions**: [Suggested research approaches and literature to examine]

## Overall Research Strategy
[Brief overview of the research approach for this framework]

## Academic Impact
[How this research would strengthen this specific framework]"""

        try:
            response, metadata = self.llm_gateway.execute_call(
                model=self.academic_model,
                prompt=research_prompt,
                max_tokens=8000
            )
            
            # Store verbose information if requested
            if verbose:
                self._last_research_directions = {
                    'raw_llm_response': response,
                    'llm_metadata': metadata,
                    'prompt_used': research_prompt[:1000] + "..." if len(research_prompt) > 1000 else research_prompt
                }
            
            # Save research directions directly as markdown
            research_file_path = self._save_research_directions_markdown(framework_name, response, verbose)
            
            # Return basic info with file path
            research_data = {
                'framework_name': framework_name,
                'research_file_path': str(research_file_path),
                'format': 'markdown',
                'raw_content': response
            }
            
            return research_data
                
        except Exception as e:
            print(f"⚠️ Research directions generation failed: {e}")
            return {
                'framework_name': framework_name,
                'error': f'Research directions generation failed: {e}',
                'research_questions': []
            }
    
    def _save_research_directions_markdown(self, framework_name: str, markdown_content: str, verbose: bool = False) -> Path:
        """Save research directions directly as markdown"""
        
        # Create research directions directory
        research_dir = Path(__file__).parent / "research_directions"
        research_dir.mkdir(exist_ok=True)
        
        # Generate filename
        timestamp = self._get_timestamp().replace(' ', '_').replace(':', '-')
        filename = f"research_directions_{framework_name}_{timestamp}.md"
        file_path = research_dir / filename
        
        # Add header and metadata
        full_markdown = f"""# Research Directions for {framework_name}

**Generated**: {self._get_timestamp()}
**Framework**: {framework_name}
**Format**: Markdown (Direct LLM Output)

---

{markdown_content}

---

*Generated by Enhanced Framework Validator - Research Directions Module*
"""
        
        # Save file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(full_markdown)
            
            print(f"📄 Research directions saved to: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"⚠️ Failed to save research directions: {e}")
            return Path("research_directions_failed.md")

    def _save_research_directions(self, framework_name: str, research_data: Dict[str, Any], verbose: bool = False) -> Path:
        """Save research directions to a markdown file with JSON structure"""
        
        # Create research directions directory
        research_dir = Path(__file__).parent / "research_directions"
        research_dir.mkdir(exist_ok=True)
        
        # Generate filename
        timestamp = self._get_timestamp().replace(' ', '_').replace(':', '-')
        filename = f"research_directions_{framework_name}_{timestamp}.md"
        file_path = research_dir / filename
        
        # Create markdown content
        markdown_content = f"""# Research Directions for {framework_name}

**Generated**: {self._get_timestamp()}
**Framework**: {framework_name}

## Research Questions

"""
        
        # Add research questions
        for question in research_data.get('research_questions', []):
            markdown_content += f"""### Priority {question.get('priority', 'N/A')}: {question.get('question', 'No question provided')}

**Rationale**: {question.get('rationale', 'No rationale provided')}

**Expected Outcomes**: {question.get('expected_outcomes', 'No outcomes specified')}

**Methodology Suggestions**: {question.get('methodology_suggestions', 'No methodology specified')}

"""
        
        # Add overall strategy and impact
        markdown_content += f"""## Overall Research Strategy

{research_data.get('overall_research_strategy', 'No strategy provided')}

## Academic Impact

{research_data.get('academic_impact', 'No impact assessment provided')}

## JSON Data Structure

```json
{json.dumps(research_data, indent=2)}
```

---

*Generated by Enhanced Framework Validator - Research Directions Module*
"""
        
        # Save file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"📄 Research directions saved to: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"⚠️ Failed to save research directions: {e}")
            return Path("research_directions_failed.md")

    def _parse_research_directions(self, research_file_path: Path) -> Dict[str, Any]:
        """Light parsing of research directions to extract questions and count"""
        try:
            with open(research_file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract research questions using regex
            import re
            question_pattern = r'### Priority (\d+): (.+?)(?=\n\n|\n###|\n##|\n---|$)'
            matches = re.findall(question_pattern, content, re.DOTALL)
            
            questions = []
            for priority, question_text in matches:
                # Clean up the question text
                clean_question = question_text.strip()
                questions.append({
                    'priority': int(priority),
                    'question': clean_question
                })
            
            # Sort by priority
            questions.sort(key=lambda x: x['priority'])
            
            return {
                'total_questions': len(questions),
                'questions': questions,
                'raw_content': content
            }
            
        except Exception as e:
            print(f"⚠️ Failed to parse research directions: {e}")
            return {
                'total_questions': 0,
                'questions': [],
                'raw_content': '',
                'error': str(e)
            }

    def _initiate_librarian_research(self, framework_path: str, research_file_path: Path, 
                                   research_data: Dict[str, Any]) -> Dict[str, Any]:
        """Initiate librarian research for each identified question"""
        
        # Parse the research directions
        parsed_directions = self._parse_research_directions(research_file_path)
        
        if parsed_directions['total_questions'] == 0:
            print("⚠️ No research questions found to research")
            return {
                'status': 'NO_QUESTIONS',
                'message': 'No research questions found in the directions file'
            }
        
        print(f"🔬 Found {parsed_directions['total_questions']} research questions")
        
        # Read the full framework content
        try:
            with open(framework_path, 'r', encoding='utf-8') as f:
                framework_content = f.read()
        except Exception as e:
            print(f"⚠️ Failed to read framework: {e}")
            return {
                'status': 'FRAMEWORK_READ_ERROR',
                'message': f'Failed to read framework: {e}'
            }
        
        # Initialize librarian (we'll need to import it)
        try:
            from discernus.librarian.discernuslibrarian import DiscernusLibrarian
            librarian = DiscernusLibrarian()
        except ImportError:
            print("⚠️ DiscernusLibrarian not available - skipping research initiation")
            return {
                'status': 'LIBRARIAN_UNAVAILABLE',
                'message': 'DiscernusLibrarian not available for import'
            }
        
        research_results = []
        
        # For each question, execute librarian research sequentially
        for question_data in parsed_directions['questions']:
            priority = question_data['priority']
            question = question_data['question']
            
            print(f"🔬 Researching Priority {priority}: {question[:100]}...")
            
            # Create research prompt combining framework and research directions
            research_prompt = f"""You are conducting academic research to strengthen an analytical framework.

FRAMEWORK CONTEXT:
{framework_content[:8000]}  # Limit framework content to avoid token limits

RESEARCH DIRECTIONS CONTEXT:
{parsed_directions['raw_content'][:4000]}  # Limit research directions content

RESEARCH QUESTION:
{question}

Please conduct a focused literature review on this specific question. Consider how it relates to the broader framework context and the academic reasoning provided in the research directions.

Focus your research on:
1. Relevant academic literature and theoretical frameworks
2. Empirical studies that address this question
3. How findings relate to the framework's theoretical foundations
4. Potential implications for framework refinement

Provide a comprehensive research report with proper citations and academic rigor."""
            
            try:
                # Execute the research using the librarian
                print(f"   📚 Executing research for Priority {priority}...")
                
                # Use the librarian's research_question method
                research_result = librarian.research_question(
                    research_prompt,
                    save_results=True
                )
                
                # Extract key information from the research result
                if hasattr(research_result, 'research_summary'):
                    summary = research_result.research_summary
                else:
                    summary = "Research completed but no summary available"
                
                if hasattr(research_result, 'key_findings'):
                    findings = research_result.key_findings
                else:
                    findings = "Key findings not available"
                
                # Get the detailed report path if available
                detailed_report_path = None
                if hasattr(research_result, 'saved_files') and research_result.saved_files:
                    detailed_report_path = research_result.saved_files.get('report_file')
                
                # Store the research result
                research_results.append({
                    'priority': priority,
                    'question': question,
                    'status': 'COMPLETED',
                    'summary': summary,
                    'findings': findings,
                    'research_object': research_result,
                    'detailed_report_path': detailed_report_path,
                    'prompt_used': research_prompt[:500] + "..." if len(research_prompt) > 500 else research_prompt
                })
                
                print(f"   ✅ Research completed for Priority {priority}")
                
            except Exception as e:
                print(f"   ⚠️ Research failed for Priority {priority}: {e}")
                research_results.append({
                    'priority': priority,
                    'question': question,
                    'status': 'FAILED',
                    'error': str(e),
                    'prompt_used': research_prompt[:500] + "..." if len(research_prompt) > 500 else research_prompt
                })
        
        # Generate synthesis of all research results
        if any(r['status'] == 'COMPLETED' for r in research_results):
            print("🔬 Generating research synthesis...")
            synthesis = self._synthesize_research_results(framework_path, research_results, parsed_directions)
        else:
            synthesis = None
        
        return {
            'status': 'RESEARCH_COMPLETED' if any(r['status'] == 'COMPLETED' for r in research_results) else 'RESEARCH_FAILED',
            'total_questions': parsed_directions['total_questions'],
            'research_results': research_results,
            'synthesis': synthesis,
            'framework_path': framework_path,
            'research_file_path': str(research_file_path)
        }

    def _synthesize_research_results(self, framework_path: str, research_results: List[Dict[str, Any]], 
                                   parsed_directions: Dict[str, Any]) -> Dict[str, Any]:
        """Synthesize research results into actionable recommendations"""
        
        # Filter completed research
        completed_research = [r for r in research_results if r['status'] == 'COMPLETED']
        
        if not completed_research:
            return {
                'status': 'NO_RESULTS',
                'message': 'No completed research to synthesize'
            }
        
        print(f"   🔬 Synthesizing {len(completed_research)} research results...")
        
        # Create synthesis prompt
        framework_name = Path(framework_path).stem
        synthesis_prompt = f"""You are an academic research synthesizer. You have completed research on {len(completed_research)} key questions for the {framework_name} analytical framework.

RESEARCH CONTEXT:
{parsed_directions['raw_content'][:3000]}

RESEARCH RESULTS:
"""
        
        # Add each research result
        for i, research in enumerate(completed_research, 1):
            synthesis_prompt += f"""
RESEARCH {i} - Priority {research['priority']}:
Question: {research['question']}
Summary: {research.get('summary', 'No summary available')}
Key Findings: {research.get('findings', 'No findings available')}

"""
        
        synthesis_prompt += f"""
Based on this research, please provide:

1. **Key Insights**: What are the main academic findings that strengthen or challenge the framework?

2. **Framework Recommendations**: What specific improvements should be made to the framework based on this research?

3. **Theoretical Strengthening**: How can the framework's theoretical foundations be improved?

4. **Methodological Improvements**: What methodological enhancements are suggested by the research?

5. **Academic Validation**: How well does the current framework align with established academic literature?

Provide your response in markdown format with clear sections and actionable recommendations.

IMPORTANT: After your synthesis, include a section called "## Detailed Research Appendices" that lists each research question and notes that detailed reports are available for academic review.
"""
        
        try:
            # Use the academic model for synthesis
            response, metadata = self.llm_gateway.execute_call(
                model=self.academic_model,
                prompt=synthesis_prompt,
                max_tokens=6000
            )
            
            # Save synthesis to file
            synthesis_file_path = self._save_research_synthesis(framework_name, response, research_results)
            
            return {
                'status': 'SYNTHESIS_COMPLETED',
                'synthesis_content': response,
                'synthesis_file_path': str(synthesis_file_path),
                'llm_metadata': metadata,
                'prompt_used': synthesis_prompt[:1000] + "..." if len(synthesis_prompt) > 1000 else synthesis_prompt
            }
            
        except Exception as e:
            print(f"   ⚠️ Synthesis failed: {e}")
            return {
                'status': 'SYNTHESIS_FAILED',
                'error': str(e),
                'message': 'Failed to generate research synthesis'
            }

    def _save_research_synthesis(self, framework_name: str, synthesis_content: str, 
                                research_results: List[Dict[str, Any]]) -> Path:
        """Save research synthesis to a markdown file"""
        
        # Create synthesis directory
        synthesis_dir = Path(__file__).parent / "research_synthesis"
        synthesis_dir.mkdir(exist_ok=True)
        
        # Generate filename
        timestamp = self._get_timestamp().replace(' ', '_').replace(':', '-')
        filename = f"research_synthesis_{framework_name}_{timestamp}.md"
        file_path = synthesis_dir / filename
        
        # Create markdown content
        full_markdown = f"""# Research Synthesis for {framework_name}

**Generated**: {self._get_timestamp()}
**Framework**: {framework_name}
**Research Questions**: {len([r for r in research_results if r['status'] == 'COMPLETED'])} completed

## Research Summary

"""
        
        # Add research question summaries
        for research in research_results:
            if research['status'] == 'COMPLETED':
                full_markdown += f"""### Priority {research['priority']}: {research['question'][:100]}...
**Status**: ✅ Completed
**Summary**: {research.get('summary', 'No summary available')[:200]}...

"""
        
        # Add synthesis content
        full_markdown += f"""## Research Synthesis

{synthesis_content}

## Detailed Research Appendices

The following detailed research reports are available for academic review and contain the full multi-stage research validation, counter-evidence analysis, and comprehensive findings:

"""
        
        # Add detailed report references
        for research in research_results:
            if research['status'] == 'COMPLETED' and research.get('detailed_report_path'):
                full_markdown += f"""### Priority {research['priority']}: {research['question'][:100]}...
**Detailed Report**: `{research['detailed_report_path']}`
**Content**: Multi-stage research validation, counter-evidence analysis, literature completeness check, red team critique, and comprehensive findings with academic citations.

"""
        
        # Now append the actual detailed reports
        full_markdown += f"""
---

## Detailed Research Reports

The following sections contain the complete, unedited research reports for each priority question:

"""
        
        # Append each detailed report
        for research in research_results:
            if research['status'] == 'COMPLETED' and research.get('detailed_report_path'):
                try:
                    with open(research['detailed_report_path'], 'r', encoding='utf-8') as f:
                        detailed_content = f.read()
                    
                    full_markdown += f"""
---

### Priority {research['priority']}: {research['question'][:100]}...

**Complete Research Report:**

{detailed_content}

---
"""
                except Exception as e:
                    full_markdown += f"""
---

### Priority {research['priority']}: {research['question'][:100]}...

**Error**: Could not load detailed report: {e}

---
"""
        
        full_markdown += f"""
---

*Generated by Enhanced Framework Validator - Research Synthesis Module*
"""
        
        # Save file
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(full_markdown)
            
            print(f"   📄 Research synthesis saved to: {file_path}")
            return file_path
            
        except Exception as e:
            print(f"   ⚠️ Failed to save synthesis: {e}")
            return Path("research_synthesis_failed.md")
    
    def _generate_enhanced_report(self, framework_path: str, structural_results: Dict[str, Any], 
                                 academic_results: Optional[Dict[str, Any]], 
                                 integrated_results: Dict[str, Any], verbose: bool = False, 
                                 research_directions: Optional[Dict[str, Any]] = None) -> str:
        """Generate comprehensive enhanced validation report"""
        
        framework_name = Path(framework_path).stem
        
        report = f"""# Enhanced Framework Validation Report

**Framework**: {framework_name}
**Validation Date**: {self._get_timestamp()}
**Overall Status**: {integrated_results['overall_status']} ({integrated_results['overall_score']}/10)

---

## 📋 Phase 1: Structural Validation

**Status**: {structural_results.get('status', 'UNKNOWN')}
**Score**: {structural_results.get('structural_score', 'N/A')}/10

**Summary**: {structural_results.get('summary', 'No summary available')}

**Issues Found**:"""

        # Add structural issues
        for issue in structural_results.get('issues', []):
            report += f"""
- **{issue.get('type', 'UNKNOWN')}**: {issue.get('description', 'No description')}
  - Impact: {issue.get('impact', 'Unknown')}
  - Fix: {issue.get('fix', 'No fix suggested')}"""

        # Add academic validation section if available
        if academic_results:
            report += f"""

---

## 📚 Phase 2: Academic Validation

**Academic Credibility Score**: {academic_results.get('academic_credibility_score', 'N/A')}/10
**Confidence Level**: {academic_results.get('confidence_level', 'UNKNOWN')}

**Theoretical Validation**: {academic_results.get('theoretical_validation', 'No assessment available')}

**Literature Coverage**: {academic_results.get('literature_coverage', 'No analysis available')}

**Research Gaps**: {academic_results.get('research_gaps', 'No gaps identified')}

**Methodological Validation**: {academic_results.get('methodological_validation', 'No assessment available')}

**Academic Recommendations**: {academic_results.get('recommendations', 'No recommendations available')}"""
        else:
            report += f"""

---

## 📚 Phase 2: Academic Validation

**Status**: Skipped or not available
**Note**: Academic validation was not performed or failed to complete"""

        # Add integrated assessment
        report += f"""

---

## 🎯 Phase 3: Integrated Assessment

**Overall Score**: {integrated_results['overall_score']}/10
**Overall Status**: {integrated_results['overall_status']}
**Confidence Level**: {integrated_results['confidence_level']}

**Score Breakdown**:
- Structural Validation: {structural_results.get('structural_score', 'N/A')}/10 (Weight: 60%)
- Academic Validation: {academic_results.get('academic_credibility_score', 'N/A') if academic_results else 'N/A'}/10 (Weight: 40%)

**Integrated Recommendations**: {integrated_results['recommendations']}

---

## 📊 Validation Summary

**Framework**: {framework_name}
**Validation Method**: Enhanced validation with structural + academic assessment
**Overall Assessment**: {integrated_results['overall_status']} ({integrated_results['overall_score']}/10)

**Key Strengths**: {self._identify_strengths(structural_results, academic_results)}
**Key Areas for Improvement**: {self._identify_improvements(structural_results, academic_results)}

"""

        # Add research directions section if available
        if research_directions:
            report += self._generate_research_directions_report_section(research_directions)
        
        report += """

---

*Generated by Enhanced Framework Validator with academic grounding validation*
"""

        # Add verbose content if requested
        if verbose:
            report += self._generate_verbose_report_section(structural_results, academic_results)
        
        return report
    
    def _extract_theoretical_content(self, framework_path: str) -> str:
        """Extract theoretical content from framework for academic validation"""
        try:
            with open(framework_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract theoretical sections (more flexible extraction)
            theoretical_sections = []
            
            # Look for theoretical foundations section
            if 'Theoretical & Empirical Foundations' in content:
                start = content.find('Theoretical & Empirical Foundations')
                end = content.find('### Section 3:', start)
                if end == -1:
                    end = content.find('## Part 2:', start)
                if end != -1:
                    theoretical_sections.append(content[start:end])
            
            # Look for methodology section
            if 'Analytical Methodology' in content:
                start = content.find('Analytical Methodology')
                end = content.find('### Section 4:', start)
                if end == -1:
                    end = content.find('## Part 2:', start)
                if end != -1:
                    theoretical_sections.append(content[start:end])
            
            # Look for framework dimensions section (common in political frameworks)
            if 'Framework Dimensions' in content:
                start = content.find('Framework Dimensions')
                end = content.find('## Part 2:', start)
                if end != -1:
                    theoretical_sections.append(content[start:end])
            
            # Look for overview/abstract section
            if 'Abstract & Raison d\'être' in content:
                start = content.find('Abstract & Raison d\'être')
                end = content.find('## Framework Dimensions', start)
                if end == -1:
                    end = content.find('## Part 2:', start)
                if end != -1:
                    theoretical_sections.append(content[start:end])
            
            # Combine theoretical content
            if theoretical_sections:
                return '\n\n'.join(theoretical_sections)
            else:
                # More comprehensive fallback - include more content for better context
                return content[:8000]  # Increased from 2000 to 8000 characters
                
        except Exception as e:
            return f"Error extracting theoretical content: {e}"
    
    def _load_framework_specification(self) -> str:
        """Load the current framework specification"""
        spec_path = Path(__file__).parent.parent.parent / "docs" / "specifications" / "FRAMEWORK_SPECIFICATION.md"
        
        if not spec_path.exists():
            return "Framework specification not found"
        
        try:
            with open(spec_path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading specification: {e}"
    
    def _parse_partial_validation_response(self, response: str) -> Dict[str, Any]:
        """Parse partial LLM response for structural validation"""
        # Try to extract more information from the response
        response_lower = response.lower()
        
        # Determine status from content
        if 'passed' in response_lower or 'success' in response_lower:
            status = 'PASSED'
        elif 'failed' in response_lower or 'error' in response_lower:
            status = 'FAILED'
        elif 'warning' in response_lower or 'issue' in response_lower:
            status = 'WARNING'
        else:
            status = 'WARNING'
        
        # Try to extract a score if present
        import re
        score_match = re.search(r'(\d+(?:\.\d+)?)/10', response)
        structural_score = float(score_match.group(1)) if score_match else 5
        
        # Look for specific issues mentioned
        issues = []
        if 'blocking' in response_lower:
            issues.append({
                'type': 'BLOCKING',
                'description': 'Blocking issues identified in partial response',
                'impact': 'Framework may not execute properly',
                'fix': 'Review framework manually for blocking issues'
            })
        
        if 'quality' in response_lower:
            issues.append({
                'type': 'QUALITY',
                'description': 'Quality issues identified in partial response',
                'impact': 'Framework may have quality problems',
                'fix': 'Review framework manually for quality issues'
            })
        
        if not issues:
            issues.append({
                'type': 'QUALITY',
                'description': 'Partial LLM response - validation may be incomplete',
                'impact': 'Limited validation coverage',
                'fix': 'Review framework manually or retry validation'
            })
        
        return {
            'status': status,
            'structural_score': structural_score,
            'issues': issues,
            'summary': f'Partial validation response analyzed: {response[:300]}...'
        }
    
    def _parse_partial_academic_response(self, response: str) -> Dict[str, Any]:
        """Parse partial LLM response for academic validation"""
        return {
            'academic_credibility_score': 5,  # Default score
            'theoretical_validation': f'Partial academic assessment: {response[:200]}...',
            'literature_coverage': 'Partial analysis due to truncated response',
            'research_gaps': 'Unable to complete gap analysis',
            'methodological_validation': 'Partial methodology assessment',
            'confidence_level': 'LOW',
            'recommendations': 'Retry academic validation for complete assessment'
        }
    
    def _generate_integrated_recommendations(self, structural_results: Dict[str, Any], 
                                          academic_results: Optional[Dict[str, Any]]) -> str:
        """Generate integrated recommendations based on both validation phases"""
        recommendations = []
        
        # Structural recommendations
        if structural_results.get('status') == 'FAILED':
            recommendations.append("Address all blocking structural issues before proceeding")
        
        for issue in structural_results.get('issues', []):
            if issue.get('type') == 'BLOCKING':
                recommendations.append(f"Critical: {issue.get('fix', 'Fix required')}")
            elif issue.get('type') == 'QUALITY':
                recommendations.append(f"Improve: {issue.get('fix', 'Quality improvement needed')}")
        
        # Academic recommendations
        if academic_results:
            if academic_results.get('academic_credibility_score', 0) < 6:
                recommendations.append("Strengthen academic foundations with additional literature review")
            
            if academic_results.get('confidence_level') == 'LOW':
                recommendations.append("Conduct more comprehensive academic validation")
        
        if not recommendations:
            recommendations.append("Framework appears well-validated across all dimensions")
        
        return '; '.join(recommendations)
    
    def _identify_strengths(self, structural_results: Dict[str, Any], 
                           academic_results: Optional[Dict[str, Any]]) -> str:
        """Identify key strengths of the framework"""
        strengths = []
        
        if structural_results.get('status') == 'PASSED':
            strengths.append("Passes structural validation")
        
        if structural_results.get('structural_score', 0) >= 8:
            strengths.append("High structural quality")
        
        if academic_results and academic_results.get('academic_credibility_score', 0) >= 7:
            strengths.append("Strong academic grounding")
        
        if not strengths:
            strengths.append("Basic framework structure present")
        
        return ', '.join(strengths)
    
    def _identify_improvements(self, structural_results: Dict[str, Any], 
                              academic_results: Optional[Dict[str, Any]]) -> str:
        """Identify key areas for improvement"""
        improvements = []
        
        # Structural improvements
        for issue in structural_results.get('issues', []):
            if issue.get('type') in ['BLOCKING', 'QUALITY']:
                improvements.append(issue.get('description', 'Issue identified'))
        
        # Academic improvements
        if academic_results and academic_results.get('academic_credibility_score', 0) < 6:
            improvements.append("Strengthen academic foundations")
        
        if not improvements:
            improvements.append("No major improvements identified")
        
        return ', '.join(improvements)
    
    def _generate_verbose_report_section(self, structural_results: Dict[str, Any], academic_results: Optional[Dict[str, Any]]) -> str:
        """Generate verbose report section with detailed LLM responses and analysis"""
        
        verbose_section = """

---

## 🔍 VERBOSE VALIDATION DETAILS

*This section provides detailed transparency into the validation process, including raw LLM responses and analysis reasoning.*

### 📋 Phase 1: Structural Validation Details

**Prompt Sent to LLM**:"""
        
        if 'prompt_used' in structural_results:
            verbose_section += f"\n```\n{structural_results['prompt_used']}\n```"
        else:
            verbose_section += "\n*No prompt information available*"
        
        verbose_section += "\n\n**Raw LLM Response**:"
        if 'raw_llm_response' in structural_results:
            verbose_section += f"\n```\n{structural_results['raw_llm_response']}\n```"
        else:
            verbose_section += "\n*No raw response available*"
        
        if 'llm_metadata' in structural_results:
            verbose_section += f"\n\n**LLM Metadata**:\n```json\n{json.dumps(structural_results['llm_metadata'], indent=2)}\n```"
        
        # Add academic validation details if available
        if academic_results:
            verbose_section += """

### 📚 Phase 2: Academic Validation Details

**Theoretical Content Extracted**:"""
            
            if 'theoretical_content_extracted' in academic_results:
                verbose_section += f"\n```\n{academic_results['theoretical_content_extracted']}\n```"
            else:
                verbose_section += "\n*No theoretical content extraction available*"
            
            verbose_section += "\n\n**Academic Validation Prompt**:"
            if 'prompt_used' in academic_results:
                verbose_section += f"\n```\n{academic_results['prompt_used']}\n```"
            else:
                verbose_section += "\n*No prompt information available*"
            
            verbose_section += "\n\n**Raw Academic LLM Response**:"
            if 'raw_llm_response' in academic_results:
                verbose_section += f"\n```\n{academic_results['raw_llm_response']}\n```"
            else:
                verbose_section += "\n*No raw response available*"
            
            if 'llm_metadata' in academic_results:
                verbose_section += f"\n\n**Academic LLM Metadata**:\n```json\n{json.dumps(academic_results['llm_metadata'], indent=2)}\n```"
        
        # Add research directions details if available
        if hasattr(self, '_last_research_directions') and self._last_research_directions:
            verbose_section += """

### 🔬 Phase 4: Research Directions Generation Details

**Research Directions Prompt**:"""
            
            if 'prompt_used' in self._last_research_directions:
                verbose_section += f"\n```\n{self._last_research_directions['prompt_used']}\n```"
            else:
                verbose_section += "\n*No prompt information available*"
            
            verbose_section += "\n\n**Raw Research Directions LLM Response**:"
            if 'raw_llm_response' in self._last_research_directions:
                verbose_section += f"\n```\n{self._last_research_directions['raw_llm_response']}\n```"
            else:
                verbose_section += "\n*No raw response available*"
            
            if 'llm_metadata' in self._last_research_directions:
                verbose_section += f"\n\n**Research Directions LLM Metadata**:\n```json\n{json.dumps(self._last_research_directions['llm_metadata'], indent=2)}\n```"
        
        verbose_section += """

---

*Verbose mode provides full transparency into the validation process for debugging and quality assessment.*
"""
        
        return verbose_section
    
    def _generate_research_directions_report_section(self, research_directions: Dict[str, Any]) -> str:
        """Generate research directions section for the enhanced report"""
        
        research_section = f"""

---

## 🔬 Research Directions Generated

**Framework**: {research_directions.get('framework_name', 'Unknown')}
**Research File**: {research_directions.get('research_file_path', 'Not saved')}

**Research Questions Identified**:"""

        # Add research questions
        for question in research_directions.get('research_questions', []):
            research_section += f"""

### Priority {question.get('priority', 'N/A')}: {question.get('question', 'No question provided')}

**Rationale**: {question.get('rationale', 'No rationale provided')}

**Expected Outcomes**: {question.get('expected_outcomes', 'No outcomes specified')}

**Methodology Suggestions**: {question.get('methodology_suggestions', 'No methodology specified')}"""

        # Add overall strategy and impact
        research_section += f"""

**Overall Research Strategy**: {research_directions.get('overall_research_strategy', 'No strategy provided')}

**Academic Impact**: {research_directions.get('academic_impact', 'No impact assessment provided')}

**Next Steps**: Use the DiscernusLibrarian to research these questions and strengthen the framework's academic foundations.
"""
        
        return research_section
    
    def _get_timestamp(self) -> str:
        """Get current timestamp for validation reports"""
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")

def main():
    """Main function for command-line usage"""
    parser = argparse.ArgumentParser(description='Enhanced Framework Validator with Academic Grounding')
    parser.add_argument('framework_path', help='Path to framework file to validate')
    parser.add_argument('--no-academic', action='store_true', 
                       help='Skip academic validation (structural only)')
    parser.add_argument('--verbose', action='store_true',
                       help='Include detailed LLM responses and analysis in report')
    parser.add_argument('--research-directions', action='store_true',
                       help='Generate research directions for frameworks that pass validation')
    parser.add_argument('--initiate-research', action='store_true',
                       help='Initiate librarian research after generating directions')
    parser.add_argument('--output', help='Output file for validation report')
    
    args = parser.parse_args()
    
    # Validate framework
    validator = EnhancedFrameworkValidator()
    results = validator.validate_framework(args.framework_path, not args.no_academic, args.verbose, args.research_directions)
    
    # Initiate librarian research if requested
    if args.initiate_research and results.get('research_directions'):
        print("\n🔬 Initiating Librarian Research...")
        research_results = validator._initiate_librarian_research(
            args.framework_path, 
            Path(results['research_directions']['research_file_path']),
            results['research_directions']
        )
        results['librarian_research'] = research_results
    
    # Print results
    print("\n" + "="*80)
    print("ENHANCED FRAMEWORK VALIDATION RESULTS")
    print("="*80)
    print(f"Framework: {results['framework_path']}")
    print(f"Overall Status: {results['integrated_assessment']['overall_status']}")
    print(f"Overall Score: {results['integrated_assessment']['overall_score']}/10")
    print(f"Structural Status: {results['structural_validation'].get('status', 'UNKNOWN')}")
    
    if results['academic_validation']:
        print(f"Academic Score: {results['academic_validation'].get('academic_credibility_score', 'N/A')}/10")
    
    if results.get('librarian_research'):
        print(f"Librarian Research: {results['librarian_research'].get('status', 'Unknown')} ({results['librarian_research'].get('total_questions', 0)} questions)")
        if results['librarian_research'].get('synthesis'):
            synthesis = results['librarian_research']['synthesis']
            print(f"Research Synthesis: {synthesis.get('status', 'Unknown')}")
            if synthesis.get('synthesis_file_path'):
                print(f"Synthesis Report: {synthesis['synthesis_file_path']}")
    
    # Save report if output file specified
    if args.output:
        try:
            with open(args.output, 'w', encoding='utf-8') as f:
                f.write(results['final_report'])
            print(f"\n📄 Enhanced validation report saved to: {args.output}")
        except Exception as e:
            print(f"⚠️ Failed to save report: {e}")
    
    return results

if __name__ == "__main__":
    main()
