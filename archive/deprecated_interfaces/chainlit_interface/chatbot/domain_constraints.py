"""
Domain Constraint Engine for Narrative Gravity Analysis Chatbot

Ensures conversational interface stays focused on political discourse analysis
while providing helpful redirects for off-topic queries.
"""

import re
from typing import List, Dict, Optional
from enum import Enum

class QueryType(Enum):
    """Classification of query types"""
    FRAMEWORK_QUESTION = "framework_question"
    ANALYSIS_REQUEST = "analysis_request" 
    METHODOLOGY_QUESTION = "methodology_question"
    COMPARISON_REQUEST = "comparison_request"
    EXPLANATION_REQUEST = "explanation_request"
    OFF_TOPIC = "off_topic"
    UNCLEAR = "unclear"

class DomainConstraintEngine:
    """
    Domain constraint engine that validates queries and classifies intent
    while maintaining focus on narrative gravity analysis.
    """
    
    def __init__(self):
        # Core domain keywords - must be present for relevance
        self.domain_keywords = {
            # Meta-analysis terms
            'framework', 'analysis', 'dipole', 'narrative', 'gravity',
            'political', 'discourse', 'civic', 'identity', 'recognition',
            'thymos', 'creedal', 'ethnic', 'democratic', 'megalothymic',
            'integrative', 'fragmentary', 'wells', 'score', 'analyze',
            'fukuyama', 'trump', 'biden', 'speech', 'rhetoric',
            
            # Political content indicators
            'government', 'nation', 'country', 'america', 'american', 'americans',
            'president', 'congress', 'senate', 'election', 'vote', 'voting',
            'policy', 'law', 'constitution', 'constitutional', 'freedom', 'liberty',
            'democracy', 'republic', 'citizen', 'citizenship', 'rights',
            'immigration', 'border', 'security', 'military', 'defense',
            'economy', 'economic', 'tax', 'taxes', 'welfare', 'healthcare',
            'education', 'justice', 'court', 'legal', 'illegal', 'criminal',
            'party', 'republican', 'democrat', 'conservative', 'liberal',
            'campaign', 'candidate', 'politics', 'politician', 'administration',
            'federal', 'state', 'local', 'congress', 'senate', 'house',
            'people', 'public', 'community', 'society', 'social'
        }
        
        # Framework-specific terms
        self.framework_terms = {
            'fukuyama', 'civic_virtue', 'political_spectrum', 
            'moral_rhetorical_posture', 'creedal', 'ethnic',
            'integrative', 'fragmentary', 'thymos', 'megalothymic'
        }
        
        # Analysis action words
        self.analysis_terms = {
            'analyze', 'score', 'measure', 'evaluate', 'assess',
            'compare', 'contrast', 'examine', 'study'
        }
        
        # Obvious off-topic indicators
        self.off_topic_indicators = {
            'weather', 'recipe', 'sports', 'movie', 'music', 
            'math', 'programming', 'medical', 'shopping',
            'games', 'entertainment', 'fashion', 'food', 'dating'
        }
        
        # More specific off-topic patterns to avoid false positives
        self.off_topic_patterns = [
            r'\b(weather|forecast|temperature|rain|snow)\b',
            r'\b(recipe|cooking|baking|ingredients)\b', 
            r'\b(sports|football|basketball|baseball|soccer)\b',
            r'\b(movie|film|cinema|netflix|hollywood)\b',
            r'\b(music|song|album|artist|concert)\b',
            r'\b(math|mathematics|algebra|calculus|geometry)\b',
            r'\b(programming|coding|software|developer|bug)\b',
            r'\b(medical|doctor|hospital|medicine|disease)\b',
            r'\b(shopping|store|buy|purchase|sale)\b',
            r'\b(game|gaming|video game|xbox|playstation)\b',
            r'\b(fashion|clothes|style|outfit)\b',
            r'\b(dating|relationship|romance|love)\b'
        ]
        
        # Intent classification patterns
        self.intent_patterns = {
            QueryType.FRAMEWORK_QUESTION: [
                r'\b(what is|explain|describe|tell me about)\b.*\b(frameworks?|dipoles?)\b',
                r'\b(fukuyama|civic virtue|political spectrum)\b.*\b(frameworks?|theory)\b',
                r'\b(how does|what does)\b.*\b(frameworks?|dipoles?|wells?)\b.*\bwork\b',
                r'\b(switch|change|use)\b.*\b(frameworks?)\b',
                r'\b(list|show)\b.*\b(frameworks?)\b',
                r'\b(available)\b.*\b(frameworks?)\b',
                r'\b(frameworks?)\b.*\b(available|list)\b'
            ],
            QueryType.ANALYSIS_REQUEST: [
                r'\b(analyze|score|measure|evaluate)\b',
                r'\b(analyze this|score this|evaluate this)\b',
                r'\banalysis\b.*\b(speech|text|transcript|document)\b'
            ],
            QueryType.COMPARISON_REQUEST: [
                r'\b(compare|contrast)\b',
                r'\b(versus|vs|against)\b',
                r'\b(difference|similar|same)\b.*\b(analysis|score|framework)\b'
            ],
            QueryType.EXPLANATION_REQUEST: [
                r'\b(what does|what is|explain|meaning of)\b.*\b(thymos|megalothymic|democratic|creedal|ethnic|identity|recognition)\b',
                r'\b(interpret|understand|mean)\b.*\b(results|scores)\b',
                r'\b(explain)\b.*\b(thymos|identity|recognition|dipole|well)\b'
            ]
        }
    
    def is_domain_relevant(self, query: str) -> bool:
        """
        Check if query is relevant to narrative analysis domain.
        
        Args:
            query: User input query
            
        Returns:
            True if query is within domain scope
        """
        query_lower = query.lower()
        
        # Check for obvious off-topic content first
        has_off_topic = any(
            indicator in query_lower for indicator in self.off_topic_indicators
        )
        
        if has_off_topic:
            return False
        
        # Check for explicit analysis requests (these should always be accepted)
        analysis_patterns = [
            r'\b(analyze|score|evaluate|examine)\b.*\b(this|text|speech|transcript)\b',
            r'\b(analyze this|score this|evaluate this)\b',
            r'\banalysis\b.*\b(of|for)\b'
        ]
        
        for pattern in analysis_patterns:
            if re.search(pattern, query_lower):
                return True
        
        # Check for domain keywords
        has_domain_keywords = any(
            keyword in query_lower for keyword in self.domain_keywords
        )
        
        # Check for political discourse content (common political terms)
        political_content_indicators = {
            'government', 'immigration', 'border', 'illegal', 'citizens', 'citizenship',
            'welfare', 'banned', 'order', 'biden', 'trump', 'americans', 'nation',
            'defend', 'planes', 'migrants', 'illegals', 'media', 'justice'
        }
        
        has_political_content = any(
            indicator in query_lower for indicator in political_content_indicators
        )
        
        # Accept if has domain keywords OR political content
        return has_domain_keywords or has_political_content
    
    def classify_intent(self, query: str) -> QueryType:
        """
        Classify the intent of a domain-relevant query.
        
        Args:
            query: User input query
            
        Returns:
            QueryType classification
        """
        if not self.is_domain_relevant(query):
            return QueryType.OFF_TOPIC
        
        query_lower = query.lower()
        
        # Check each intent pattern
        for intent_type, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, query_lower, re.IGNORECASE):
                    return intent_type
        
        # Default to unclear if no pattern matches
        return QueryType.UNCLEAR
    
    def get_redirect_message(self, query_type: QueryType = QueryType.OFF_TOPIC) -> str:
        """
        Generate appropriate redirect message for off-topic or unclear queries.
        
        Args:
            query_type: Type of query that needs redirection
            
        Returns:
            Helpful redirect message
        """
        if query_type == QueryType.OFF_TOPIC:
            return """I'm the Narrative Gravity Analysis Assistant, specialized in political discourse analysis.

I can help you with:
• Analyzing political texts using established frameworks (Fukuyama Identity, Civic Virtue, Political Spectrum)
• Explaining framework dipoles and theoretical foundations
• Comparing different texts or frameworks
• Interpreting analysis results and scores

What political text or discourse would you like to analyze?"""
        
        elif query_type == QueryType.UNCLEAR:
            return """I'm not sure exactly what you're looking for. I specialize in narrative gravity analysis of political discourse.

Try asking me:
• "Analyze this speech transcript" (with text)
• "What is the Fukuyama Identity framework?"
• "Explain Megalothymic Thymos scores"
• "Compare Trump and Biden rhetoric"
• "Switch to Civic Virtue framework"

How can I help you analyze political narratives?"""
        
        else:
            return self.get_redirect_message(QueryType.OFF_TOPIC)
    
    def extract_framework_mentions(self, query: str) -> List[str]:
        """
        Extract mentioned frameworks from query.
        
        Args:
            query: User input query
            
        Returns:
            List of framework names mentioned
        """
        query_lower = query.lower()
        mentioned_frameworks = []
        
        framework_mappings = {
            'fukuyama': 'fukuyama_identity',
            'civic virtue': 'civic_virtue', 
            'political spectrum': 'political_spectrum',
            'moral rhetorical': 'moral_rhetorical_posture',
            'rhetorical posture': 'moral_rhetorical_posture'
        }
        
        for keyword, framework_id in framework_mappings.items():
            if keyword in query_lower:
                mentioned_frameworks.append(framework_id)
        
        return mentioned_frameworks
    
    def validate_and_classify(self, query: str) -> Dict:
        """
        Complete validation and classification of user query.
        
        Args:
            query: User input query
            
        Returns:
            Dictionary with validation results and classification
        """
        is_relevant = self.is_domain_relevant(query)
        intent = self.classify_intent(query)
        frameworks = self.extract_framework_mentions(query)
        
        return {
            'is_domain_relevant': is_relevant,
            'intent': intent,
            'mentioned_frameworks': frameworks,
            'requires_redirect': not is_relevant or intent == QueryType.UNCLEAR,
            'redirect_message': self.get_redirect_message(intent) if not is_relevant or intent == QueryType.UNCLEAR else None
        } 