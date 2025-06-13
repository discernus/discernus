"""
Seed Prompt Library for Structured Component Development

Provides standardized prompt templates for systematic development of:
- Prompt templates (hierarchical analysis instructions)
- Framework architectures (dipole-based moral frameworks)  
- Weighting methodologies (mathematical scoring approaches)

Each seed prompt is designed to accelerate development while maintaining
conversational flexibility and academic rigor.
"""

from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum


class ComponentType(Enum):
    """Component types for structured development."""
    PROMPT_TEMPLATE = "prompt_template"
    FRAMEWORK = "framework"
    WEIGHTING_METHODOLOGY = "weighting_methodology"


@dataclass
class SeedPrompt:
    """Container for a structured development seed prompt."""
    component_type: ComponentType
    purpose: str
    prompt_template: str
    success_criteria: List[str]
    development_steps: List[str]
    quality_metrics: List[str]


class SeedPromptLibrary:
    """
    Library of standardized seed prompts for component development.
    
    Provides structured conversation starters for LLM-assisted development
    sessions, ensuring consistency and quality across development workflows.
    """
    
    def __init__(self):
        self._prompts = self._initialize_seed_prompts()
    
    def get_prompt(self, component_type: ComponentType, context: Optional[Dict] = None) -> str:
        """
        Get a customized seed prompt for component development.
        
        Args:
            component_type: Type of component being developed
            context: Optional context for prompt customization
                   
        Returns:
            Formatted seed prompt string ready for LLM conversation
        """
        if component_type not in self._prompts:
            raise ValueError(f"No seed prompt available for {component_type}")
        
        seed_prompt = self._prompts[component_type]
        return self._format_prompt(seed_prompt, context or {})
    
    def get_success_criteria(self, component_type: ComponentType) -> List[str]:
        """Get success criteria for component type."""
        return self._prompts[component_type].success_criteria
    
    def get_development_steps(self, component_type: ComponentType) -> List[str]:
        """Get structured development steps for component type."""
        return self._prompts[component_type].development_steps
    
    def get_quality_metrics(self, component_type: ComponentType) -> List[str]:
        """Get quality assessment metrics for component type."""
        return self._prompts[component_type].quality_metrics
    
    def list_available_types(self) -> List[ComponentType]:
        """List all available component types."""
        return list(self._prompts.keys())
    
    def _initialize_seed_prompts(self) -> Dict[ComponentType, SeedPrompt]:
        """Initialize the library with all seed prompts."""
        return {
            ComponentType.PROMPT_TEMPLATE: self._create_prompt_template_seed(),
            ComponentType.FRAMEWORK: self._create_framework_seed(), 
            ComponentType.WEIGHTING_METHODOLOGY: self._create_weighting_seed()
        }
    
    def _create_prompt_template_seed(self) -> SeedPrompt:
        """Create seed prompt for prompt template development."""
        return SeedPrompt(
            component_type=ComponentType.PROMPT_TEMPLATE,
            purpose="Develop LLM prompt templates for hierarchical narrative analysis",
            prompt_template="""I'm developing prompt templates for LLM-based narrative analysis that must produce consistent, hierarchical thematic scoring.

Current Challenge: {current_challenge}

Framework Context: {framework_name} - {framework_description}

Target Framework Wells: {framework_wells}

Success Criteria:
- Reliable identification of 2-3 dominant themes with relative weighting (must sum to 100%)
- Specific textual evidence extraction supporting scoring decisions
- Clear explanation of WHY each well dominates over others
- Framework fit assessment (0.0-1.0) with missing dimension identification
- Coefficient of variation < 0.20 across multiple runs on same text
- Distinguish between strong presence (0.7-1.0) and weak presence (0.0-0.3)

Current Prompt Template Version: {current_version}

Help me iteratively refine this prompt template focusing on:
1. **Instruction Clarity**: Unambiguous directives for LLM reasoning
2. **Reasoning Chain Requirements**: Step-by-step analytical process
3. **Output Formatting**: Structured JSON with required fields
4. **Scoring Methodology Alignment**: Consistency with framework mathematics
5. **Evidence Integration**: Connecting textual quotes to scoring decisions

Development Hypothesis: {development_hypothesis}

Let's work through systematic improvements that will enhance consistency and hierarchical detection.""",
            success_criteria=[
                "Instructions are unambiguous and actionable",
                "Output format is precisely specified with required fields",
                "Reasoning requirements guide LLM through analytical steps", 
                "Scoring methodology aligns with framework mathematics",
                "Evidence extraction requirements are explicit",
                "Edge cases and ambiguous scenarios are addressed",
                "Hierarchical ranking produces meaningful distinctions",
                "Cross-run consistency (CV < 0.20) is achieved"
            ],
            development_steps=[
                "Hypothesis Formation: Define specific improvement goal",
                "Baseline Testing: Evaluate current prompt against 3-5 texts",
                "Systematic Refinement: Modify instructions based on performance gaps",
                "Validation Testing: Test modifications against representative corpus",
                "Performance Analysis: Calculate CV, scoring distribution, hierarchy detection",
                "Evidence Documentation: Capture reasoning and performance impact",
                "Version Creation: Document changes and create new template version"
            ],
            quality_metrics=[
                "Coefficient of Variation (target: < 0.20)",
                "Hierarchical Clarity Score (dominant themes clearly identified)",
                "Evidence Quality (specific quotes supporting each score)",
                "Framework Fit Accuracy (missing dimensions correctly identified)",
                "Output Format Compliance (structured JSON adherence)",
                "Instruction Following Rate (LLM compliance with directives)",
                "Cross-Text Consistency (stable performance across narrative types)"
            ]
        )
    
    def _create_framework_seed(self) -> SeedPrompt:
        """Create seed prompt for framework development."""
        return SeedPrompt(
            component_type=ComponentType.FRAMEWORK,
            purpose="Develop dipole-based moral frameworks for narrative analysis",
            prompt_template="""I'm developing analytical frameworks for political narrative analysis using dipole-based moral architecture.

Framework Focus: {framework_domain}

Theoretical Foundation: {theoretical_source}

Current Framework State: {existing_dipoles}

Development Goals:
- Create 4-5 conceptually distinct dipoles capturing core moral tensions
- Ensure dipoles are measurable through textual analysis of political narratives
- Achieve framework coherence and theoretical grounding
- Design for cross-narrative applicability while maintaining analytical precision
- Balance comprehensive coverage with practical usability

Target Analysis Domain: {target_domain}

Help me systematically develop this framework through:

1. **Conceptual Architecture Design**
   - Identify fundamental moral tensions in the domain
   - Map relationships between competing values/principles
   - Ensure conceptual distinctness between dipole pairs

2. **Dipole Definition and Refinement**
   - Craft precise language for positive and negative wells
   - Define clear operational boundaries for each well
   - Create examples of strong/weak manifestations in text

3. **Theoretical Justification**
   - Ground each dipole in established moral/political theory
   - Explain why these tensions matter for understanding narratives
   - Connect to broader scholarly frameworks and debates

4. **Application Testing Scenarios**
   - Design test cases across different narrative types
   - Identify edge cases where framework boundaries are tested
   - Plan validation approaches for framework effectiveness

Current Development Hypothesis: {development_hypothesis}

Let's work through this step by step, focusing on conceptual clarity, analytical precision, and theoretical rigor.""",
            success_criteria=[
                "Dipoles are conceptually distinct and non-overlapping",
                "Wells have clear operational definitions for textual analysis",
                "Framework covers intended analytical domain comprehensively",
                "Theoretical foundation is solid and well-documented",
                "Cross-narrative applicability is demonstrated",
                "Dipole relationships create coherent analytical system",
                "Framework enables meaningful distinctions between narratives",
                "Academic grounding supports scholarly credibility"
            ],
            development_steps=[
                "Theoretical Grounding: Establish conceptual foundation from source material",
                "Domain Analysis: Map core tensions and competing values in target domain",
                "Dipole Architecture: Design complementary tension pairs systematically",
                "Definition Refinement: Craft precise language with clear boundaries",
                "Coherence Validation: Ensure dipoles work together as unified system",
                "Application Testing: Test framework against diverse narrative samples",
                "Theoretical Integration: Connect to broader scholarly frameworks",
                "Documentation: Create comprehensive framework specification"
            ],
            quality_metrics=[
                "Conceptual Distinctness (dipoles measure different dimensions)",
                "Operational Clarity (definitions enable consistent application)", 
                "Theoretical Grounding (connection to established scholarship)",
                "Domain Coverage (framework captures key tensions comprehensively)",
                "Cross-Narrative Validity (works across different narrative types)",
                "Analytical Precision (enables meaningful distinctions)",
                "Academic Credibility (suitable for scholarly publication)",
                "Practical Usability (researchers can apply framework effectively)"
            ]
        )
    
    def _create_weighting_seed(self) -> SeedPrompt:
        """Create seed prompt for weighting methodology development."""
        return SeedPrompt(
            component_type=ComponentType.WEIGHTING_METHODOLOGY,
            purpose="Develop mathematical weighting schemes for hierarchical narrative analysis",
            prompt_template="""I'm developing mathematical weighting schemes for narrative analysis that must capture thematic hierarchy and dominance patterns effectively.

Current Problem: {current_problem}

Data Structure: 
- Input: {num_wells} wells scored 0.0-1.0 per framework
- Current Approach: {current_approach}
- Observed Issues: {observed_issues}

Analytical Goals:
- Amplify dominant themes (0.7+ scores) while preserving analytical subtlety
- Reduce impact of background themes (0.0-0.3 scores) without eliminating them
- Create meaningful distinctions in narrative positioning on 2D coordinate system
- Maintain mathematical interpretability and theoretical justification
- Handle edge cases gracefully (single-well dominance, balanced narratives)

Mathematical Constraints:
- Preserve relative ordering of well strengths
- Avoid artificial compression of meaningful differences  
- Enable clear visualization on circular coordinate system
- Support statistical analysis and comparison across narratives

Development Focus: {development_focus}

Help me develop alternative weighting schemes focusing on:

1. **Mathematical Approaches**
   - Exponential transforms for dominance amplification
   - Winner-take-most algorithms for hierarchy emphasis
   - Hierarchical weighting based on LLM-provided rankings
   - Threshold-based approaches for categorical distinctions

2. **Dominance Detection and Amplification**
   - Single-well dominance detection (>80% weight scenarios)
   - Multi-well hierarchy preservation and enhancement
   - Background noise reduction while maintaining analytical precision

3. **Edge Case Handling and Normalization**
   - Balanced narrative scenarios (no clear dominant theme)
   - Extreme dominance scenarios (single theme overwhelming)
   - Ambiguous cases where multiple themes compete

4. **Validation Against Expected Hierarchies**
   - Test scenarios with known thematic structures
   - Comparison with human expert rankings
   - Cross-methodology consistency checks

Current Development Hypothesis: {development_hypothesis}

Let's explore systematic approaches to mathematical transformation of theme scores that enhance analytical clarity while maintaining theoretical rigor.""",
            success_criteria=[
                "Mathematical approach is well-defined and theoretically justified",
                "Dominance patterns are amplified appropriately without distortion",
                "Edge cases behave predictably and meaningfully",
                "Results align with expected narrative hierarchies", 
                "Integration with existing analysis pipeline is seamless",
                "Statistical properties support comparative analysis",
                "Algorithm parameters are interpretable and tunable",
                "Performance improvements are measurable and significant"
            ],
            development_steps=[
                "Mathematical Framework: Define transformation constraints and objectives",
                "Algorithm Development: Design specific weighting functions and parameters",
                "Edge Case Analysis: Test behavior with extreme and ambiguous scenarios",
                "Validation Design: Create test scenarios with known expected outcomes",
                "Performance Testing: Compare against baseline approaches quantitatively",
                "Parameter Tuning: Optimize algorithm parameters for best performance",
                "Integration Planning: Ensure compatibility with existing scoring pipeline",
                "Documentation: Specify mathematical formulation and implementation"
            ],
            quality_metrics=[
                "Hierarchy Enhancement Score (improved thematic distinction)",
                "Edge Case Robustness (predictable behavior in extreme scenarios)",
                "Statistical Stability (consistent results across similar narratives)",
                "Theoretical Alignment (results match expected hierarchical patterns)",
                "Mathematical Validity (transforms preserve meaningful relationships)",
                "Implementation Efficiency (computational performance and scalability)",
                "Parameter Interpretability (algorithm settings have clear meaning)",
                "Cross-Methodology Consistency (results align with alternative approaches)"
            ]
        )
    
    def _format_prompt(self, seed_prompt: SeedPrompt, context: Dict) -> str:
        """Format seed prompt with context variables."""
        try:
            return seed_prompt.prompt_template.format(**context)
        except KeyError as e:
            # Return prompt with placeholders for missing context
            missing_keys = [key for key in self._extract_template_keys(seed_prompt.prompt_template) 
                          if key not in context]
            formatted_context = context.copy()
            for key in missing_keys:
                formatted_context[key] = f"[{key.upper()}_TO_BE_SPECIFIED]"
            return seed_prompt.prompt_template.format(**formatted_context)
    
    def _extract_template_keys(self, template: str) -> List[str]:
        """Extract format keys from template string."""
        import re
        return re.findall(r'\{(\w+)\}', template)


# Convenience functions for direct access
def get_prompt_template_seed(context: Optional[Dict] = None) -> str:
    """Quick access to prompt template development seed."""
    library = SeedPromptLibrary()
    return library.get_prompt(ComponentType.PROMPT_TEMPLATE, context)


def get_framework_seed(context: Optional[Dict] = None) -> str:
    """Quick access to framework development seed.""" 
    library = SeedPromptLibrary()
    return library.get_prompt(ComponentType.FRAMEWORK, context)


def get_weighting_seed(context: Optional[Dict] = None) -> str:
    """Quick access to weighting methodology development seed."""
    library = SeedPromptLibrary()
    return library.get_prompt(ComponentType.WEIGHTING_METHODOLOGY, context) 