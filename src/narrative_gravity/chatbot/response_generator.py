"""
Response Generator for Narrative Gravity Analysis Chatbot

Handles response formatting, template management, and output styling
for consistent user experience.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
import json

class ResponseGenerator:
    """
    Generates formatted responses for the narrative gravity analysis chatbot.
    
    Handles templating, formatting, and styling of various response types
    while maintaining consistent voice and academic precision.
    """
    
    def __init__(self):
        self.response_templates = self._load_response_templates()
        self.formatting_rules = self._load_formatting_rules()
    
    def _load_response_templates(self) -> Dict[str, str]:
        """Load response templates for different interaction types."""
        return {
            'welcome': """👋 **Welcome to Narrative Gravity Analysis**

I'm your research assistant for analyzing political discourse using established frameworks.

**Current framework**: {framework_name}

**What I can help with**:
• Analyze political texts and speeches
• Explain theoretical frameworks and concepts  
• Compare different analyses
• Interpret scoring and results

**Try asking**:
• "What is the Fukuyama Identity framework?"
• "Analyze this speech: [paste text]"
• "Explain Megalothymic Thymos"

What would you like to explore?""",
            
            'analysis_complete': """✅ **Analysis Complete**

{analysis_content}

**Next steps**:
• Ask me to explain any concepts or scores
• Analyze another text to compare
• Switch frameworks to see different perspectives

What would you like to do next?""",
            
            'framework_switched': """🎯 **Framework Changed**

Now using: **{framework_name}**

{framework_description}

Ready to analyze with this new perspective! What text would you like to examine?""",
            
            'comparison_ready': """📊 **Comparison Analysis**

{comparison_content}

**Insights**:
{insights}

Would you like to:
• Analyze additional texts?
• Explore specific differences?
• Try a different framework?""",
            
            'concept_explained': """💡 **Concept Explanation**

{concept_content}

**Application**: {application_notes}

**Related concepts**: {related_concepts}

Want to see how this applies to a specific text analysis?""",
            
            'error_graceful': """⚠️ **Something went wrong**

{error_message}

**You can try**:
• Rephrasing your question
• Starting with a simpler query
• Asking "What can you help me with?"

I'm here to help with narrative gravity analysis!"""
        }
    
    def _load_formatting_rules(self) -> Dict[str, Any]:
        """Load formatting rules for consistent output."""
        return {
            'max_text_preview': 150,
            'score_precision': 2,
            'concept_explanation_length': 500,
            'use_emojis': True,
            'markdown_formatting': True,
            'include_next_steps': True
        }
    
    def format_welcome_message(self, framework_name: str) -> str:
        """Generate welcome message with current framework."""
        return self.response_templates['welcome'].format(
            framework_name=framework_name
        )
    
    def format_analysis_result(self, analysis_data: Dict[str, Any], 
                             framework_name: str) -> str:
        """
        Format analysis results with proper structure and styling.
        
        Args:
            analysis_data: Analysis results and metadata
            framework_name: Name of framework used
            
        Returns:
            Formatted analysis response
        """
        # Extract key components
        text_preview = self._truncate_text(
            analysis_data.get('text', ''), 
            self.formatting_rules['max_text_preview']
        )
        
        scores = analysis_data.get('scores', {})
        metrics = analysis_data.get('metrics', {})
        summary = analysis_data.get('summary', '')
        
        # Build formatted response
        response = f"✅ **Analysis Complete** using {framework_name}\n\n"
        
        # Text preview
        response += f"**Text analyzed**: \"{text_preview}{'...' if len(analysis_data.get('text', '')) > self.formatting_rules['max_text_preview'] else ''}\"\n\n"
        
        # Gravity well scores
        if scores:
            response += "**Gravity Well Scores** (0.0-1.0):\n"
            integrative_scores = []
            disintegrative_scores = []
            
            for well_name, score in scores.items():
                formatted_score = round(score, self.formatting_rules['score_precision'])
                score_line = f"• **{self._humanize_well_name(well_name)}**: {formatted_score}"
                
                # Categorize by type (this would be determined by framework config)
                if self._is_integrative_well(well_name):
                    integrative_scores.append(score_line)
                else:
                    disintegrative_scores.append(score_line)
            
            if integrative_scores:
                response += "\n*Integrative Wells:*\n" + "\n".join(integrative_scores) + "\n"
            if disintegrative_scores:
                response += "\n*Disintegrative Wells:*\n" + "\n".join(disintegrative_scores) + "\n"
        
        # Key metrics
        if metrics:
            response += "\n**Key Metrics**:\n"
            for metric_name, value in metrics.items():
                formatted_value = round(value, self.formatting_rules['score_precision'])
                response += f"• **{self._humanize_metric_name(metric_name)}**: {formatted_value}\n"
        
        # Summary
        if summary:
            response += f"\n**Summary**: {summary}\n"
        
        # Next steps
        if self.formatting_rules['include_next_steps']:
            response += "\n**What's next?**\n"
            response += "• Ask me to explain any scores or concepts\n"
            response += "• Analyze another text for comparison\n"
            response += "• Try a different framework perspective\n"
        
        return response
    
    def format_framework_explanation(self, framework_data: Dict[str, Any]) -> str:
        """
        Format framework explanation with structure and examples.
        
        Args:
            framework_data: Framework configuration and metadata
            
        Returns:
            Formatted framework explanation
        """
        name = framework_data.get('display_name', framework_data.get('name', 'Unknown'))
        description = framework_data.get('description', '')
        version = framework_data.get('version', '')
        
        response = f"📚 **{name}**"
        if version:
            response += f" (v{version})"
        response += "\n\n"
        
        if description:
            response += f"{description}\n\n"
        
        # Core dipoles
        dipoles = framework_data.get('dipoles', [])
        if dipoles:
            response += "**Core Analytical Dimensions**:\n"
            for i, dipole in enumerate(dipoles, 1):
                pos_name = dipole.get('positive', {}).get('name', 'Unknown')
                neg_name = dipole.get('negative', {}).get('name', 'Unknown')
                dipole_desc = dipole.get('description', '')
                
                response += f"{i}. **{dipole['name']}**: {pos_name} ↔ {neg_name}\n"
                if dipole_desc:
                    response += f"   _{dipole_desc}_\n"
        
        # Gravity wells summary
        wells = framework_data.get('wells', {})
        if wells:
            response += f"\n**Measurement Points**: {len(wells)} gravity wells for precise scoring\n"
        
        return response
    
    def format_comparison_result(self, comparison_data: Dict[str, Any]) -> str:
        """
        Format comparison between multiple analyses.
        
        Args:
            comparison_data: Comparison results and insights
            
        Returns:
            Formatted comparison response
        """
        analyses = comparison_data.get('analyses', [])
        insights = comparison_data.get('insights', [])
        
        response = f"📊 **Comparison Analysis** ({len(analyses)} texts)\n\n"
        
        # Individual analysis summaries
        for i, analysis in enumerate(analyses, 1):
            text_preview = self._truncate_text(analysis.get('text', ''), 80)
            summary = analysis.get('summary', 'No summary available')
            
            response += f"**Text {i}**: \"{text_preview}...\"\n"
            response += f"*Analysis*: {summary}\n\n"
        
        # Key differences and insights
        if insights:
            response += "**Key Insights**:\n"
            for insight in insights:
                response += f"• {insight}\n"
        
        return response
    
    def format_concept_explanation(self, concept_name: str, 
                                 explanation_data: Dict[str, Any]) -> str:
        """
        Format concept explanation with examples and context.
        
        Args:
            concept_name: Name of concept being explained
            explanation_data: Explanation content and examples
            
        Returns:
            Formatted concept explanation
        """
        response = f"💡 **{concept_name}**\n\n"
        
        # Main explanation
        explanation = explanation_data.get('explanation', '')
        if explanation:
            response += f"{explanation}\n\n"
        
        # Examples
        examples = explanation_data.get('examples', [])
        if examples:
            response += "**Examples**:\n"
            for example in examples:
                response += f"• {example}\n"
            response += "\n"
        
        # Related concepts
        related = explanation_data.get('related_concepts', [])
        if related:
            response += f"**Related concepts**: {', '.join(related)}\n"
        
        return response
    
    def format_error_message(self, error_type: str, error_details: str = '') -> str:
        """
        Format error messages in a helpful, non-technical way.
        
        Args:
            error_type: Type of error encountered
            error_details: Additional error context
            
        Returns:
            User-friendly error message
        """
        error_messages = {
            'framework_not_found': "❌ Framework not available. Try 'list frameworks' to see options.",
            'analysis_failed': "⚠️ Analysis couldn't complete. Please check your text and try again.",
            'text_too_short': "📝 Text is too short for analysis. Please provide at least 50 characters.",
            'no_text_provided': "📄 No text found to analyze. Please include text after 'analyze this:'",
            'comparison_impossible': "📊 Need at least 2 analyses for comparison. Try analyzing more texts first.",
            'unknown_concept': "❓ Concept not recognized. Try asking about specific framework terms.",
            'general': f"⚠️ Something went wrong: {error_details}"
        }
        
        base_message = error_messages.get(error_type, error_messages['general'])
        
        # Add helpful suggestions
        suggestions = [
            "• Try rephrasing your question",
            "• Ask 'What can you help me with?' for guidance",
            "• Start with 'What is the Fukuyama framework?'"
        ]
        
        return base_message + "\n\n**Suggestions**:\n" + "\n".join(suggestions)
    
    def _truncate_text(self, text: str, max_length: int) -> str:
        """Truncate text to specified length."""
        if len(text) <= max_length:
            return text
        return text[:max_length].strip()
    
    def _humanize_well_name(self, well_name: str) -> str:
        """Convert technical well names to human-readable format."""
        name_mappings = {
            'creedal_identity': 'Creedal Identity',
            'ethnic_identity': 'Ethnic Identity',  
            'integrative_recognition': 'Integrative Recognition',
            'fragmentary_recognition': 'Fragmentary Recognition',
            'democratic_thymos': 'Democratic Thymos',
            'megalothymic_thymos': 'Megalothymic Thymos'
        }
        return name_mappings.get(well_name, well_name.replace('_', ' ').title())
    
    def _humanize_metric_name(self, metric_name: str) -> str:
        """Convert technical metric names to human-readable format."""
        name_mappings = {
            'ies': 'Identity Elevation Score',
            'ics': 'Identity Coherence Score', 
            'tas': 'Thymos Alignment Score',
            'overall_score': 'Overall Narrative Score',
            'integrative_score': 'Integrative Tendency',
            'disintegrative_score': 'Disintegrative Tendency'
        }
        return name_mappings.get(metric_name, metric_name.replace('_', ' ').title())
    
    def _is_integrative_well(self, well_name: str) -> bool:
        """Determine if a gravity well is integrative or disintegrative."""
        integrative_wells = {
            'creedal_identity', 'integrative_recognition', 'democratic_thymos'
        }
        return well_name in integrative_wells
    
    def add_response_metadata(self, response: str, metadata: Dict[str, Any]) -> str:
        """
        Add metadata to response if needed (for debugging or analytics).
        
        Args:
            response: Base response text
            metadata: Additional metadata to include
            
        Returns:
            Response with metadata if debugging enabled
        """
        # In production, metadata would be logged separately
        # For development, could append debug info
        return response 