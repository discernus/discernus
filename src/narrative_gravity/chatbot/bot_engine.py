"""
Narrative Gravity Analysis Chatbot Engine

Main orchestrator for conversational narrative analysis interface.
Integrates domain constraints, framework management, and analysis capabilities.
"""

import re
import json
from typing import Dict, List, Optional, Any, Tuple
from datetime import datetime
from dataclasses import dataclass

from .domain_constraints import DomainConstraintEngine, QueryType
from .conversation_context import ConversationContext, ConversationState, AnalysisRecord, FrameworkCreationSession, DipoleDefinition
from .framework_interface import FrameworkInterface
from .response_generator import ResponseGenerator
from .llm_domain_classifier import LLMDomainClassifier, ClassificationResult
from ..framework_manager import FrameworkManager

class ChatResponse:
    """Structured response from chatbot"""
    
    def __init__(self, content: str, response_type: str = "text", 
                 metadata: Optional[Dict] = None, requires_input: bool = False):
        self.content = content
        self.response_type = response_type  # text, analysis, visualization, error
        self.metadata = metadata or {}
        self.requires_input = requires_input
        self.timestamp = datetime.now()

class NarrativeGravityBot:
    """
    Main chatbot engine for narrative gravity analysis.
    
    Provides conversational interface for political discourse analysis
    while maintaining academic rigor and domain focus.
    """
    
    def __init__(self, user_id: Optional[str] = None, base_dir: str = "."):
        """
        Initialize the chatbot engine.
        
        Args:
            user_id: Optional user identifier for session tracking
            base_dir: Base directory for framework files
        """
        # Core components
        self.llm_classifier = LLMDomainClassifier()  # New LLM-based classifier
        self.domain_engine = DomainConstraintEngine()  # Keep as fallback
        self.context = ConversationContext(user_id)
        self.framework_interface = FrameworkInterface(base_dir)
        self.response_generator = ResponseGenerator()
        
        # Set initial framework from system
        current_framework = self.framework_interface.get_current_framework()
        if current_framework:
            self.context.set_framework(current_framework)
        
        # Welcome state
        self.context.update_state(ConversationState.GREETING)
    
    def process_query(self, user_input: str) -> ChatResponse:
        """
        Process user query and generate appropriate response.
        
        Args:
            user_input: User's input message
            
        Returns:
            Structured chat response
        """
        # Add user message to context
        self.context.add_message("user", user_input)
        
        # Use LLM-based classification
        classification = self.llm_classifier.classify_query(user_input)
        
        # Handle off-topic queries
        if classification.result == ClassificationResult.OFF_TOPIC:
            response = ChatResponse(
                content=self._get_redirect_message(),
                response_type="redirect",
                metadata={
                    'classification': classification.result.value,
                    'confidence': classification.confidence,
                    'reasoning': classification.reasoning,
                    'llm_classified': not classification.cached
                }
            )
            self._add_bot_response(response)
            return response
        
        # Process domain-relevant query based on LLM classification
        response = self._handle_llm_classification(classification, user_input)
        
        # Add bot response to context
        self._add_bot_response(response)
        
        return response
    
    def _handle_llm_classification(self, classification: "ClassificationResponse", 
                                 user_input: str) -> ChatResponse:
        """Handle LLM classification results."""
        
        if classification.result == ClassificationResult.FRAMEWORK_QUESTION:
            return self._handle_framework_question(user_input, {})
        
        elif classification.result == ClassificationResult.ANALYSIS_REQUEST:
            return self._handle_analysis_request(user_input)
        
        elif classification.result == ClassificationResult.FRAMEWORK_CREATION:
            return self._handle_framework_creation(user_input, classification)
        
        elif classification.result == ClassificationResult.POLITICAL_DISCOURSE:
            # Direct political content - offer to analyze it
            return self._handle_political_content(user_input, classification)
        
        else:  # UNCLEAR
            return self._handle_unclear_query(user_input, classification)
    
    def _handle_political_content(self, user_input: str, 
                                classification: "ClassificationResponse") -> ChatResponse:
        """Handle direct political discourse content."""
        
        # Extract the political text for analysis
        text_to_analyze = self._extract_political_text(user_input)
        
        if text_to_analyze and len(text_to_analyze) > 50:
            # Process the analysis directly
            self.context.update_state(ConversationState.PROCESSING_ANALYSIS)
            analysis_result = self._perform_analysis(text_to_analyze)
            
            return ChatResponse(
                content=analysis_result,
                response_type="analysis_result",
                metadata={
                    'classification': classification.result.value,
                    'confidence': classification.confidence,
                    'auto_analyzed': True,
                    'text_length': len(text_to_analyze)
                }
            )
        else:
            # Offer to analyze the content
            return ChatResponse(
                content=f"""I can see this is political discourse! 

**LLM Classification**: {classification.reasoning} (confidence: {classification.confidence:.2f})

Would you like me to analyze this content using the current framework? Or would you prefer to:
• Switch to a different framework first
• Ask questions about the analytical approach
• Provide additional context

What would you like to do?""",
                response_type="political_content_detected",
                metadata={
                    'classification': classification.result.value,
                    'confidence': classification.confidence
                },
                requires_input=True
            )
    
    def _handle_unclear_query(self, user_input: str, 
                            classification: "ClassificationResponse") -> ChatResponse:
        """Handle unclear queries with helpful guidance."""
        
        return ChatResponse(
            content=f"""I'm not entirely sure how to help with that query.

**Analysis**: {classification.reasoning} (confidence: {classification.confidence:.2f})

I specialize in political discourse analysis. Here are some things I can help with:

**Framework Questions**:
• "What is the Fukuyama Identity framework?"
• "Explain Megalothymic Thymos"
• "Switch to Civic Virtue framework"

**Analysis Requests**:
• "Analyze this speech: [paste political text]"
• "Score this transcript using current framework"

**Political Content**:
• Paste any political speech, policy statement, or campaign rhetoric

What would you like to explore?""",
            response_type="unclear_guidance",
            metadata={
                'classification': classification.result.value,
                'confidence': classification.confidence
            },
            requires_input=True
        )
    
    def _extract_political_text(self, user_input: str) -> Optional[str]:
        """Extract political text from user input for direct analysis."""
        
        # Look for explicit analysis markers first
        extracted = self._extract_analysis_text(user_input)
        if extracted:
            return extracted
        
        # If the whole input is political content, use it directly
        # (but exclude very short inputs that are likely questions)
        if len(user_input) > 100:  # Reasonable threshold for political text
            return user_input.strip()
        
        return None
    
    def _get_redirect_message(self) -> str:
        """Generate redirect message for off-topic queries."""
        return """I'm the Narrative Gravity Analysis Assistant, specialized in political discourse analysis.

I can help you with:
• **Analyzing political texts** using established frameworks (Fukuyama Identity, Civic Virtue, Political Spectrum)
• **Explaining theoretical frameworks** and their analytical dimensions
• **Comparing different analyses** and interpreting results
• **Framework switching** and methodology questions

**Try asking**:
• "What is the Fukuyama Identity framework?"
• "Analyze this speech: [paste political text]"
• "Explain Megalothymic Thymos"
• "Compare Trump and Biden rhetoric"

What political discourse would you like to analyze?"""
    
    def _handle_framework_question(self, user_input: str, 
                                  validation_result: Dict) -> ChatResponse:
        """Handle framework-related questions."""
        user_lower = user_input.lower()
        mentioned_frameworks = validation_result.get('mentioned_frameworks', [])
        
        # Framework switching request
        if any(word in user_lower for word in ['switch', 'change', 'use']):
            if mentioned_frameworks:
                framework_name = mentioned_frameworks[0]
                success, message = self.framework_interface.switch_framework(framework_name)
                if success:
                    self.context.set_framework(framework_name)
                    self.context.update_state(ConversationState.WAITING_FOR_INPUT)
                
                return ChatResponse(
                    content=message + "\n\nWhat would you like to analyze with this framework?",
                    response_type="framework_switch",
                    metadata={'framework_changed': success, 'new_framework': framework_name}
                )
            else:
                # Show available frameworks
                summary = self.framework_interface.get_framework_summary()
                return ChatResponse(
                    content=summary + "\n\nWhich framework would you like to switch to?",
                    response_type="framework_list",
                    requires_input=True
                )
        
        # Framework explanation request
        elif any(word in user_lower for word in ['what is', 'explain', 'describe']):
            if mentioned_frameworks:
                explanation = self.framework_interface.explain_framework(mentioned_frameworks[0])
            else:
                explanation = self.framework_interface.explain_framework()
            
            self.context.update_state(ConversationState.EXPLAINING_CONCEPTS)
            return ChatResponse(
                content=explanation + "\n\nWould you like to analyze some text using this framework?",
                response_type="framework_explanation",
                requires_input=True
            )
        
        # List all frameworks
        elif any(word in user_lower for word in ['list', 'available', 'all', 'show']):
            summary = self.framework_interface.get_framework_summary()
            return ChatResponse(
                content=summary + "\n\nWhich framework interests you?",
                response_type="framework_list",
                requires_input=True
            )
        
        else:
            # General framework help
            current = self.framework_interface.get_current_framework()
            display_name = self.framework_interface._get_display_name(current) if current else "None"
            
            return ChatResponse(
                content=f"""Currently using: **{display_name}**

I can help you with:
• **Switch frameworks**: "Switch to Civic Virtue framework"
• **Explain frameworks**: "What is the Fukuyama Identity framework?"
• **List frameworks**: "Show me all available frameworks"
• **Compare frameworks**: "How do frameworks differ?"

What would you like to know about frameworks?""",
                response_type="framework_help",
                requires_input=True
            )
    
    def _handle_analysis_request(self, user_input: str) -> ChatResponse:
        """Handle analysis requests."""
        # Extract text for analysis
        text_to_analyze = self._extract_analysis_text(user_input)
        
        if not text_to_analyze:
            self.context.update_state(ConversationState.WAITING_FOR_INPUT)
            return ChatResponse(
                content="""Ready to analyze! Please provide the text in one of these ways:

**Option 1**: Paste the text directly
"Analyze this: [paste your text here]"

**Option 2**: Describe the text you want to analyze
"Analyze Trump's 2016 acceptance speech"

**Option 3**: Provide a URL
"Analyze this YouTube transcript: [URL]"

What text would you like me to analyze?""",
                response_type="analysis_prompt",
                requires_input=True
            )
        
        # Process the analysis (placeholder for now)
        self.context.update_state(ConversationState.PROCESSING_ANALYSIS)
        
        # This would integrate with your existing analysis engine
        analysis_result = self._perform_analysis(text_to_analyze)
        
        return ChatResponse(
            content=analysis_result,
            response_type="analysis_result",
            metadata={'text_analyzed': text_to_analyze[:100] + "..."}
        )
    
    def _handle_comparison_request(self, user_input: str) -> ChatResponse:
        """Handle comparison requests."""
        if not self.context.can_compare_analyses():
            return ChatResponse(
                content="""I need at least 2 previous analyses to make comparisons.

Please analyze some texts first:
• "Analyze this Trump speech: [text]"
• "Analyze this Biden speech: [text]"

Then I can compare them for you!""",
                response_type="comparison_unavailable"
            )
        
        candidates = self.context.get_comparison_candidates()
        comparison_text = self._generate_comparison(candidates)
        
        self.context.update_state(ConversationState.COMPARING_ANALYSES)
        return ChatResponse(
            content=comparison_text,
            response_type="comparison_result",
            metadata={'compared_analyses': len(candidates)}
        )
    
    def _handle_explanation_request(self, user_input: str) -> ChatResponse:
        """Handle requests for explanations of concepts or results."""
        user_lower = user_input.lower()
        
        # Check for specific concept requests
        concept_patterns = {
            'thymos': ['thymos', 'megalothymic', 'democratic thymos'],
            'identity': ['creedal identity', 'ethnic identity', 'identity foundation'],
            'recognition': ['integrative recognition', 'fragmentary recognition', 'recognition dynamics'],
            'score': ['score', 'scoring', 'interpret score', 'meaning of score'],
            'dipole': ['dipole', 'dipoles', 'gravity well', 'wells']
        }
        
        for concept, patterns in concept_patterns.items():
            if any(pattern in user_lower for pattern in patterns):
                explanation = self._explain_concept(concept, user_input)
                self.context.update_state(ConversationState.EXPLAINING_CONCEPTS)
                return ChatResponse(
                    content=explanation,
                    response_type="concept_explanation",
                    metadata={'concept': concept}
                )
        
        # General explanation
        return ChatResponse(
            content="""I can explain various aspects of narrative gravity analysis:

**Concepts**:
• "What does Megalothymic Thymos mean?"
• "Explain Creedal Identity"
• "How do dipoles work?"

**Scoring**:
• "How do you score narratives?"
• "What does a high score mean?"
• "Interpret these results"

**Frameworks**:
• "What is the Fukuyama framework?"
• "How do frameworks differ?"

What would you like me to explain?""",
            response_type="explanation_help",
            requires_input=True
        )
    
    def _handle_general_query(self, user_input: str) -> ChatResponse:
        """Handle general domain-relevant queries."""
        current_framework = self.framework_interface.get_current_framework()
        display_name = self.framework_interface._get_display_name(current_framework) if current_framework else "None"
        
        return ChatResponse(
            content=f"""I'm your Narrative Gravity Analysis Assistant using the **{display_name}** framework.

**What I can do:**
• **Analyze political texts**: "Analyze this speech transcript"
• **Explain frameworks**: "What is the Fukuyama Identity framework?"
• **Compare analyses**: "Compare this to the previous speech"
• **Interpret results**: "What does a high Megalothymic Thymos score mean?"

**Sample queries:**
• "Analyze this Trump 2015 campaign announcement"
• "Switch to Civic Virtue framework"
• "Explain Creedal Identity vs Ethnic Identity"
• "Compare my last two analyses"

What would you like to explore?""",
            response_type="general_help",
            requires_input=True
        )
    
    def _handle_framework_creation(self, user_input: str, 
                                  classification: "ClassificationResponse") -> ChatResponse:
        """Handle framework creation requests using conversational flow."""
        
        # Check if already in framework creation mode
        if self.context.is_creating_framework():
            return self._continue_framework_creation(user_input)
        
        # Start new framework creation session
        return self._start_framework_creation(user_input, classification)
    
    def _start_framework_creation(self, user_input: str, 
                                 classification: "ClassificationResponse") -> ChatResponse:
        """Start a new framework creation conversation."""
        
        # Extract source material if provided
        source_material = self._extract_source_material(user_input)
        
        # Initialize framework creation session
        self.context.start_framework_creation(source_material)
        
        return ChatResponse(
            content=f"""🛠️ **Framework Creation Assistant**

I'll guide you through creating a custom analytical framework! This is exactly how the Fukuyama Identity Framework was developed through conversation.

**Classification**: {classification.reasoning} (confidence: {classification.confidence:.2f})

Let's start with the foundation:

**Step 1: Framework Concept**
What is the core theoretical insight or thinker you want to base this framework on? For example:
• "Based on John Stuart Mill's concept of liberty"
• "Inspired by Hannah Arendt's theory of political action" 
• "Focused on Marx's class consciousness"

**Or describe the political phenomenon you want to analyze:**
• "Framework for analyzing populist rhetoric"
• "Tool for measuring democratic backsliding"
• "System for evaluating policy discourse"

What's your starting point for this framework?""",
            response_type="framework_creation_start",
            metadata={
                'classification': classification.result.value,
                'confidence': classification.confidence,
                'source_material': source_material
            },
            requires_input=True
        )
    
    def _continue_framework_creation(self, user_input: str) -> ChatResponse:
        """Continue an ongoing framework creation conversation."""
        
        session = self.context.get_framework_creation()
        if not session:
            return self._start_framework_creation(user_input, None)
        
        current_step = session.creation_step
        
        if current_step == "conceptualization":
            return self._handle_conceptualization_step(user_input, session)
        elif current_step == "dipole_definition":
            return self._handle_dipole_definition_step(user_input, session)
        elif current_step == "validation":
            return self._handle_validation_step(user_input, session)
        elif current_step == "refinement":
            return self._handle_refinement_step(user_input, session)
        elif current_step == "implementation":
            return self._handle_implementation_step(user_input, session)
        elif current_step == "testing":
            return self._handle_testing_step(user_input, session)
        else:
            # Default back to conceptualization
            session.creation_step = "conceptualization"
            return self._handle_conceptualization_step(user_input, session)
    
    def _handle_conceptualization_step(self, user_input: str, session) -> ChatResponse:
        """Handle the initial framework conceptualization."""
        
        # Store the theoretical foundation
        session.theoretical_foundation = user_input.strip()
        session.creation_step = "dipole_definition"
        
        return ChatResponse(
            content=f"""✅ **Theoretical Foundation Captured**

**Your Framework Concept**: {session.theoretical_foundation}

**Step 2: Dipole Discovery**
Now we need to identify the core tensions or opposing forces. In the Fukuyama example, we discovered:
• Creedal vs. Ethnic Identity
• Integrative vs. Fragmentary Recognition  
• Democratic vs. Megalothymic Thymos

**For your framework, what are the fundamental opposing forces or tensions?**

Think about:
• What are the key contradictions in your theoretical area?
• What opposing tendencies drive political narratives?
• What binaries or spectrums exist in this domain?

**Please suggest 3-5 potential dipoles** (opposing pairs). For example:
"I think the key tensions are individual liberty vs collective security, and procedural fairness vs substantive outcomes"

What opposing forces do you see in your theoretical domain?""",
            response_type="framework_dipole_discovery",
            requires_input=True
        )
    
    def _extract_analysis_text(self, user_input: str) -> Optional[str]:
        """Extract text to be analyzed from user input."""
        # Look for quoted text or text after "analyze this:"
        patterns = [
            r'analyze this:?\s*(.+)',
            r'analyze\s*["\'](.+?)["\']',
            r'score this:?\s*(.+)',
            r'["\'](.{50,})["\']'  # Quoted text over 50 chars
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE | re.DOTALL)
            if match:
                text = match.group(1).strip()
                if len(text) > 20:  # Minimum length for meaningful analysis
                    return text
        
        return None
    
    def _extract_source_material(self, user_input: str) -> str:
        """Extract source material or theoretical basis from framework creation request."""
        patterns = [
            r'based on (.+)',
            r'framework.*for (.+)',
            r'inspired by (.+)',
            r'focused on (.+)',
            r'using (.+)',
            r'from (.+?)(?:\s|$)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input, re.IGNORECASE)
            if match:
                return match.group(1).strip()
        
        return user_input.strip()
    
    def _handle_dipole_definition_step(self, user_input: str, session) -> ChatResponse:
        """Handle dipole definition and validation."""
        
        # Parse dipoles from user input 
        suggested_dipoles = self._parse_dipoles_from_text(user_input)
        
        if not suggested_dipoles:
            return ChatResponse(
                content="""I need clearer dipole suggestions. Please provide opposing pairs like:

**Example format:**
"The key tensions are:
• Individual Liberty vs Collective Security
• Procedural Fairness vs Substantive Outcomes  
• Elite Expertise vs Popular Wisdom"

Or simply list them:
"Liberty vs Security, Process vs Outcomes, Elite vs Popular"

What are the fundamental opposing forces in your theoretical domain?""",
                response_type="dipole_clarification",
                requires_input=True
            )
        
        # Store suggested dipoles
        for dipole_text in suggested_dipoles:
            dipole = DipoleDefinition()
            dipole.name = dipole_text
            session.dipoles.append(dipole)
        
        session.creation_step = "validation"
        
        dipole_list = "\n".join([f"• {d.name}" for d in session.dipoles])
        
        return ChatResponse(
            content=f"""✅ **Dipoles Identified**

**Your Suggested Dipoles:**
{dipole_list}

**Step 3: Framework Validation**
Now let's evaluate these dipoles. Like in the Fukuyama analysis, we need to consider:

• **Theoretical Coherence**: Do these capture the core tensions in your domain?
• **Analytical Power**: Will these help distinguish different types of political discourse?
• **Practical Utility**: Can these be reliably scored by analysts?

**Questions for you:**
1. Are these the most fundamental tensions, or should we refine them?
2. Which dipole is most central to your theoretical framework?
3. Should we reduce to 3 core dipoles (like Fukuyama) or keep more?

**Your assessment**: Do these dipoles capture the essence of your framework, or should we refine them?""",
            response_type="framework_validation",
            requires_input=True
        )
    
    def _parse_dipoles_from_text(self, text: str) -> List[str]:
        """Extract dipole pairs from user text."""
        dipoles = []
        
        # Look for "vs" or "versus" patterns
        vs_pattern = r'([^•\n]+?)\s+(?:vs\.?|versus|against)\s+([^•\n]+)'
        matches = re.findall(vs_pattern, text, re.IGNORECASE)
        
        for positive, negative in matches:
            dipole_name = f"{positive.strip()} vs {negative.strip()}"
            dipoles.append(dipole_name)
        
        # Also look for bullet-pointed lists
        bullet_pattern = r'[•\-\*]\s*([^•\-\*\n]+)'
        bullet_matches = re.findall(bullet_pattern, text)
        
        # Group bullets into pairs if no "vs" found but multiple bullets exist
        if not dipoles and len(bullet_matches) >= 2:
            for i in range(0, len(bullet_matches), 2):
                if i + 1 < len(bullet_matches):
                    dipole_name = f"{bullet_matches[i].strip()} vs {bullet_matches[i+1].strip()}"
                    dipoles.append(dipole_name)
        
        return dipoles
    
    def _perform_analysis(self, text: str) -> str:
        """
        Perform narrative gravity analysis on text.
        
        This is a placeholder that would integrate with your existing analysis engine.
        """
        current_framework = self.context.current_framework
        
        # Placeholder analysis result
        # This would call your existing analysis engine
        analysis_summary = f"""**Analysis Results** using {self.framework_interface._get_display_name(current_framework)}

Text analyzed: "{text[:100]}{'...' if len(text) > 100 else ''}"

**Gravity Well Scores** (0.0 - 1.0):
• Creedal Identity: 0.75
• Integrative Recognition: 0.68
• Democratic Thymos: 0.82
• Ethnic Identity: 0.15
• Fragmentary Recognition: 0.23
• Megalothymic Thymos: 0.18

**Key Metrics**:
• Identity Elevation Score (IES): 0.67
• Identity Coherence Score (ICS): 0.74
• Thymos Alignment Score (TAS): 0.76

**Summary**: This narrative demonstrates strong integrative characteristics with high democratic thymos and creedal identity orientation. Low disintegrative scores suggest constructive civic discourse.

Would you like me to explain any of these scores or compare with another text?"""
        
        # Create analysis record
        analysis_record = AnalysisRecord(
            analysis_id=f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            text_content=text,
            framework_used=current_framework,
            timestamp=datetime.now(),
            results={
                "ies": 0.67, "ics": 0.74, "tas": 0.76,
                "wells": {"creedal_identity": 0.75, "democratic_thymos": 0.82}
            },
            summary="Strong integrative characteristics with democratic orientation"
        )
        
        # Add to context
        self.context.add_analysis(analysis_record)
        
        return analysis_summary
    
    def _generate_comparison(self, analyses: List[AnalysisRecord]) -> str:
        """Generate comparison between analyses."""
        if len(analyses) < 2:
            return "Need at least 2 analyses for comparison."
        
        # Placeholder comparison
        return f"""**Comparison of {len(analyses)} Analyses**

**Analysis 1**: {analyses[0].summary}
**Analysis 2**: {analyses[1].summary}

**Key Differences**:
• Democratic Thymos: +0.15 higher in Analysis 2
• Ethnic Identity: -0.08 lower in Analysis 2
• Overall trend: More integrative orientation in recent analysis

Would you like detailed metrics or to analyze another text?"""
    
    def _explain_concept(self, concept: str, user_input: str) -> str:
        """Explain a specific concept."""
        explanations = {
            'thymos': """**Thymos** in Fukuyama's framework represents the human drive for recognition and dignity.

**Democratic Thymos** (Healthy):
• Seeks equal recognition through civic participation
• Channels dignity needs through democratic processes
• Values procedural fairness and mutual respect

**Megalothymic Thymos** (Destructive):
• Desires superior recognition through dominance
• Creates zero-sum competition for status
• Threatens democratic norms and institutions

This psychological distinction is central to understanding how political narratives either strengthen or undermine democratic culture.""",
            
            'identity': """**Identity Foundation** determines how citizenship and belonging are defined.

**Creedal Identity** (Integrative):
• Citizenship based on shared democratic principles
• Voluntary commitment to constitutional ideals
• Accessible to all regardless of background

**Ethnic Identity** (Disintegrative):
• Belonging through blood, soil, or cultural inheritance
• Treats citizenship as inherited rather than chosen
• Creates insider/outsider distinctions

This distinction is crucial for democratic sustainability and social cohesion."""
        }
        
        return explanations.get(concept, f"I need more specific information to explain {concept}. What aspect interests you?")
    
    def _add_bot_response(self, response: ChatResponse) -> None:
        """Add bot response to conversation context."""
        self.context.add_message(
            "assistant", 
            response.content,
            metadata={
                'response_type': response.response_type,
                'metadata': response.metadata
            }
        )
    
    def get_session_summary(self) -> Dict[str, Any]:
        """Get summary of current session."""
        return self.context.get_session_summary()
    
    def reset_session(self, keep_preferences: bool = True) -> None:
        """Reset conversation session."""
        self.context.clear_history(keep_preferences)
        self.context.update_state(ConversationState.GREETING)
    
    def _handle_validation_step(self, user_input: str, session) -> ChatResponse:
        """Handle framework validation and refinement decisions."""
        
        user_lower = user_input.lower()
        
        if any(word in user_lower for word in ['yes', 'good', 'correct', 'right', 'keep']):
            session.creation_step = "implementation"
            return self._handle_implementation_step("", session)
        
        elif any(word in user_lower for word in ['refine', 'change', 'modify', 'adjust']):
            session.creation_step = "refinement"
            return ChatResponse(
                content="""**Step 3b: Framework Refinement**

Let's refine your dipoles. You can:

**Modify existing dipoles:**
"Change 'Liberty vs Security' to 'Individual Freedom vs Collective Safety'"

**Remove dipoles:**
"Remove the third dipole, it's not core to the framework"

**Add new dipoles:**
"Add 'Procedural Justice vs Distributive Justice'"

**Or provide completely new dipoles:**
"Let's restart with: X vs Y, A vs B, C vs D"

What changes would you like to make?""",
                response_type="framework_refinement",
                requires_input=True
            )
        
        else:
            # Ask for clarification
            return ChatResponse(
                content="""Please let me know:

• **"These look good"** - if you're happy with the dipoles as they are
• **"Let's refine them"** - if you want to modify, add, or remove dipoles
• **"Start over"** - if you want to completely rethink the approach

Which direction would you like to go?""",
                response_type="validation_clarification",
                requires_input=True
            )
    
    def _handle_refinement_step(self, user_input: str, session) -> ChatResponse:
        """Handle dipole refinement."""
        
        # Process refinement requests
        if "remove" in user_input.lower():
            # Handle dipole removal
            return self._process_dipole_removal(user_input, session)
        elif "add" in user_input.lower():
            # Handle dipole addition
            return self._process_dipole_addition(user_input, session)
        elif "change" in user_input.lower() or "modify" in user_input.lower():
            # Handle dipole modification
            return self._process_dipole_modification(user_input, session)
        else:
            # Replace all dipoles with new ones
            new_dipoles = self._parse_dipoles_from_text(user_input)
            if new_dipoles:
                session.dipoles = []
                for dipole_text in new_dipoles:
                    dipole = DipoleDefinition()
                    dipole.name = dipole_text
                    session.dipoles.append(dipole)
                
                session.creation_step = "validation"
                return self._show_refined_dipoles(session)
        
        return ChatResponse(
            content="I didn't understand the refinement. Please be more specific about what you'd like to change.",
            response_type="refinement_clarification",
            requires_input=True
        )
    
    def _handle_implementation_step(self, user_input: str, session) -> ChatResponse:
        """Handle framework implementation and configuration generation."""
        
        # Generate framework name if not set
        if not session.framework_name:
            session.framework_name = self._generate_framework_name(session)
        
        session.creation_step = "testing"
        
        dipole_list = "\n".join([f"• {d.name}" for d in session.dipoles])
        
        return ChatResponse(
            content=f"""🎯 **Framework Implementation Ready**

**Framework Name**: {session.framework_name}
**Theoretical Basis**: {session.theoretical_foundation}

**Dipoles**:
{dipole_list}

**Step 4: Testing & Validation**
Now let's test your framework! I can:

1. **Generate full technical implementation** (JSON configs, prompts)
2. **Test with sample texts** to see how it performs
3. **Compare results** with existing frameworks

**For testing, please provide a political text** (speech, statement, etc.) or say:
• "Test with Trump 2016 speech"
• "Use Biden inauguration address"  
• "Test with sample presidential text"

What text would you like to use for initial testing?""",
            response_type="framework_implementation",
            requires_input=True
        )
    
    def _handle_testing_step(self, user_input: str, session) -> ChatResponse:
        """Handle framework testing with sample texts."""
        
        # Extract test text
        test_text = self._extract_test_text(user_input)
        
        if not test_text:
            return ChatResponse(
                content="""Please provide a text to test the framework:

**Options:**
• Paste a political speech or statement directly
• "Test with Trump 2016 acceptance speech"
• "Use a Biden campaign text"
• "Test with sample presidential rhetoric"

What text should we use for testing?""",
                response_type="testing_text_needed",
                requires_input=True
            )
        
        # Simulate framework testing (placeholder)
        session.test_texts.append(test_text)
        test_results = self._simulate_framework_test(session, test_text)
        session.test_results.append(test_results)
        
        return ChatResponse(
            content=f"""🧪 **Framework Test Results**

**Text Tested**: "{test_text[:100]}{'...' if len(test_text) > 100 else ''}"

**{session.framework_name} Scores**:
{self._format_test_results(test_results)}

**Next Steps:**
• **"Test another text"** - to validate with more examples
• **"Generate implementation"** - to create full technical specs
• **"Refine framework"** - to adjust based on results
• **"Compare with Fukuyama"** - to see how it differs

What would you like to do next?""",
            response_type="framework_test_results",
            requires_input=True,
            metadata={'test_results': test_results}
        )
    
    def _generate_framework_name(self, session) -> str:
        """Generate a framework name based on theoretical foundation."""
        foundation = session.theoretical_foundation.lower()
        
        # Extract key terms
        key_terms = []
        if "mill" in foundation:
            key_terms.append("Mill")
        elif "arendt" in foundation:
            key_terms.append("Arendt")
        elif "marx" in foundation:
            key_terms.append("Marx")
        elif "liberty" in foundation:
            key_terms.append("Liberty")
        elif "populist" in foundation:
            key_terms.append("Populist")
        elif "democratic" in foundation:
            key_terms.append("Democratic")
        
        if key_terms:
            return f"{key_terms[0]} Framework"
        else:
            return "Custom Framework"
    
    def _extract_test_text(self, user_input: str) -> Optional[str]:
        """Extract test text from user input."""
        # Check for quoted text first
        quoted_match = re.search(r'"([^"]+)"', user_input)
        if quoted_match:
            return quoted_match.group(1)
        
        # Check for common test requests
        test_patterns = {
            r'trump.*2016': "My fellow Americans, tonight, we mark a historic moment as we begin our journey to make America great again...",
            r'biden.*inauguration': "Today, we celebrate the triumph not of a candidate, but of a cause, the cause of democracy...",
            r'sample.*presidential': "My fellow citizens, we gather today at a crossroads in our nation's history..."
        }
        
        for pattern, sample_text in test_patterns.items():
            if re.search(pattern, user_input.lower()):
                return sample_text
        
        # If input is long enough, use it as test text
        if len(user_input) > 50:
            return user_input
        
        return None
    
    def _simulate_framework_test(self, session, test_text: str) -> Dict[str, float]:
        """Simulate framework testing (placeholder implementation)."""
        import random
        
        results = {}
        for dipole in session.dipoles:
            # Extract dipole components
            parts = dipole.name.split(' vs ')
            if len(parts) == 2:
                positive_well = parts[0].strip().lower().replace(' ', '_')
                negative_well = parts[1].strip().lower().replace(' ', '_')
                
                # Simulate scoring
                pos_score = random.uniform(0.1, 0.9)
                neg_score = 1.0 - pos_score
                
                results[positive_well] = pos_score
                results[negative_well] = neg_score
        
        return results
    
    def _format_test_results(self, results: Dict[str, float]) -> str:
        """Format test results for display."""
        formatted = []
        for well, score in results.items():
            well_display = well.replace('_', ' ').title()
            formatted.append(f"• {well_display}: {score:.2f}")
        
        return "\n".join(formatted) 