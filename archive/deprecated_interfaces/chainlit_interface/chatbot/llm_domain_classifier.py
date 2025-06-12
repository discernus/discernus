"""
LLM-Based Domain Classifier for Narrative Gravity Analysis Chatbot

Uses actual language models to intelligently determine if content is relevant
to political discourse analysis, replacing brittle keyword-based approaches.
"""

import os
import json
import hashlib
from typing import Dict, Optional, Tuple
from enum import Enum
from dataclasses import dataclass
from datetime import datetime, timedelta

# Try to import OpenAI, fallback gracefully if not available
try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

class ClassificationResult(Enum):
    """Domain classification results"""
    POLITICAL_DISCOURSE = "political_discourse"
    FRAMEWORK_QUESTION = "framework_question" 
    ANALYSIS_REQUEST = "analysis_request"
    FRAMEWORK_CREATION = "framework_creation"
    OFF_TOPIC = "off_topic"
    UNCLEAR = "unclear"

@dataclass
class ClassificationResponse:
    """Structured response from LLM classifier"""
    result: ClassificationResult
    confidence: float
    reasoning: str
    intent_type: str
    cached: bool = False

class LLMDomainClassifier:
    """
    LLM-powered domain classifier for narrative gravity analysis.
    
    Uses GPT models to intelligently classify user queries and content
    rather than relying on brittle keyword matching.
    """
    
    def __init__(self, model: str = "gpt-3.5-turbo", cache_ttl_hours: int = 24):
        self.model = model
        self.cache_ttl = timedelta(hours=cache_ttl_hours)
        self.cache = {}
        self.fallback_keywords = self._load_fallback_keywords()
        
        # Initialize OpenAI if available
        if OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY'):
            openai.api_key = os.getenv('OPENAI_API_KEY')
            self.llm_available = True
        else:
            self.llm_available = False
            print("⚠️  OpenAI not available, falling back to keyword matching")
    
    def classify_query(self, query: str) -> ClassificationResponse:
        """
        Classify a user query using LLM intelligence.
        
        Args:
            query: User input to classify
            
        Returns:
            Classification result with confidence and reasoning
        """
        # Check cache first
        cache_key = self._get_cache_key(query)
        if cache_key in self.cache:
            cached_result = self.cache[cache_key]
            if datetime.now() - cached_result['timestamp'] < self.cache_ttl:
                cached_result['response'].cached = True
                return cached_result['response']
        
        # Use LLM if available, otherwise fallback
        if self.llm_available:
            result = self._classify_with_llm(query)
        else:
            result = self._classify_with_fallback(query)
        
        # Cache the result
        self.cache[cache_key] = {
            'response': result,
            'timestamp': datetime.now()
        }
        
        return result
    
    def _classify_with_llm(self, query: str) -> ClassificationResponse:
        """Classify using LLM intelligence."""
        
        prompt = f"""You are a domain classifier for a political discourse analysis research tool.

Your task: Determine if the following user input is relevant to political discourse analysis.

CLASSIFICATION OPTIONS:
1. POLITICAL_DISCOURSE - Text contains political speech, rhetoric, or discourse that can be analyzed
2. FRAMEWORK_QUESTION - Questions about analytical frameworks (Fukuyama, Civic Virtue, etc.)
3. ANALYSIS_REQUEST - Requests to analyze text, even if no text provided yet
4. FRAMEWORK_CREATION - Requests to create, design, or develop new analytical frameworks
5. OFF_TOPIC - Clearly unrelated to politics or discourse analysis (weather, recipes, etc.)
6. UNCLEAR - Cannot determine relevance from the input

GUIDELINES:
- Political content includes: speeches, policy statements, campaign rhetoric, governance language
- Accept analysis requests even if incomplete: "analyze this speech"
- Accept framework questions: "what is the Fukuyama framework?"
- Framework creation includes: "create a framework based on X", "develop dipoles for Y", "build framework"
- Reject obvious off-topic: weather, recipes, entertainment, personal advice
- When in doubt, lean toward acceptance for research purposes

USER INPUT: "{query}"

Respond with JSON:
{{
    "classification": "POLITICAL_DISCOURSE|FRAMEWORK_QUESTION|ANALYSIS_REQUEST|FRAMEWORK_CREATION|OFF_TOPIC|UNCLEAR",
    "confidence": 0.0-1.0,
    "reasoning": "Brief explanation of your classification decision"
}}"""

        try:
            # Try new OpenAI client first (v1.0+)
            try:
                from openai import OpenAI
                client = OpenAI()
                response = client.chat.completions.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200,
                    temperature=0.1
                )
                content = response.choices[0].message.content.strip()
            except ImportError:
                # Fallback to old API if available
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=200,
                    temperature=0.1
                )
                content = response.choices[0].message.content.strip()
            
            # Parse JSON response
            try:
                result_data = json.loads(content)
                classification = ClassificationResult(result_data['classification'].lower())
                confidence = float(result_data['confidence'])
                reasoning = result_data['reasoning']
                
                return ClassificationResponse(
                    result=classification,
                    confidence=confidence,
                    reasoning=reasoning,
                    intent_type=classification.value
                )
                
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"⚠️  LLM response parsing failed: {e}")
                return self._classify_with_fallback(query)
                
        except Exception as e:
            print(f"⚠️  LLM classification failed: {e}")
            return self._classify_with_fallback(query)
    
    def _classify_with_fallback(self, query: str) -> ClassificationResponse:
        """Fallback classification using improved keyword matching."""
        
        query_lower = query.lower()
        
        # Check for obvious off-topic content
        off_topic_patterns = [
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
        
        import re
        for pattern in off_topic_patterns:
            if re.search(pattern, query_lower):
                return ClassificationResponse(
                    result=ClassificationResult.OFF_TOPIC,
                    confidence=0.8,
                    reasoning="Matched off-topic pattern (fallback classification)",
                    intent_type="off_topic"
                )
        
        # Check for framework questions
        framework_patterns = [
            r'\b(what is|explain|describe)\b.*\b(framework|fukuyama|civic virtue)\b',
            r'\b(switch|change|use)\b.*\b(framework)\b',
            r'\b(list|show|available)\b.*\b(frameworks?)\b'
        ]
        
        for pattern in framework_patterns:
            if re.search(pattern, query_lower):
                return ClassificationResponse(
                    result=ClassificationResult.FRAMEWORK_QUESTION,
                    confidence=0.7,
                    reasoning="Matched framework question pattern (fallback)",
                    intent_type="framework_question"
                )
        
        # Check for framework creation requests
        creation_patterns = [
            r'\b(create|build|develop|design)\b.*\b(framework|dipole)\b',
            r'\b(new framework|custom framework)\b',
            r'\b(framework.*based on)\b',
            r'\b(dipoles?.*for)\b',
            r'\b(build.*out.*framework)\b'
        ]
        
        for pattern in creation_patterns:
            if re.search(pattern, query_lower):
                return ClassificationResponse(
                    result=ClassificationResult.FRAMEWORK_CREATION,
                    confidence=0.7,
                    reasoning="Matched framework creation pattern (fallback)",
                    intent_type="framework_creation"
                )
        
        # Check for analysis requests
        analysis_patterns = [
            r'\b(analyze|score|evaluate|examine)\b',
            r'\banalysis\b.*\b(of|for)\b'
        ]
        
        for pattern in analysis_patterns:
            if re.search(pattern, query_lower):
                return ClassificationResponse(
                    result=ClassificationResult.ANALYSIS_REQUEST,
                    confidence=0.7,
                    reasoning="Matched analysis request pattern (fallback)",
                    intent_type="analysis_request"
                )
        
        # Check for political content
        political_keywords = self.fallback_keywords['political']
        found_political = any(keyword in query_lower for keyword in political_keywords)
        
        if found_political:
            return ClassificationResponse(
                result=ClassificationResult.POLITICAL_DISCOURSE,
                confidence=0.6,
                reasoning="Contains political keywords (fallback classification)",
                intent_type="political_discourse"
            )
        
        # Default to unclear
        return ClassificationResponse(
            result=ClassificationResult.UNCLEAR,
            confidence=0.3,
            reasoning="Could not classify with available patterns (fallback)",
            intent_type="unclear"
        )
    
    def _load_fallback_keywords(self) -> Dict[str, set]:
        """Load keyword sets for fallback classification."""
        return {
            'political': {
                'government', 'politics', 'political', 'policy', 'election',
                'president', 'congress', 'senate', 'democracy', 'republican',
                'democrat', 'conservative', 'liberal', 'campaign', 'vote',
                'immigration', 'border', 'citizenship', 'constitution',
                'freedom', 'liberty', 'rights', 'justice', 'welfare',
                'economy', 'economic', 'tax', 'healthcare', 'education',
                'biden', 'trump', 'obama', 'clinton', 'america', 'american',
                'nation', 'national', 'federal', 'state', 'public'
            }
        }
    
    def _get_cache_key(self, query: str) -> str:
        """Generate cache key for query."""
        return hashlib.md5(query.encode()).hexdigest()
    
    def is_relevant_to_domain(self, query: str) -> Tuple[bool, str]:
        """
        Simple boolean check for domain relevance.
        
        Args:
            query: User input query
            
        Returns:
            Tuple of (is_relevant, reasoning)
        """
        result = self.classify_query(query)
        
        relevant_types = {
            ClassificationResult.POLITICAL_DISCOURSE,
            ClassificationResult.FRAMEWORK_QUESTION,
            ClassificationResult.ANALYSIS_REQUEST,
            ClassificationResult.FRAMEWORK_CREATION
        }
        
        is_relevant = result.result in relevant_types
        return is_relevant, result.reasoning
    
    def clear_cache(self):
        """Clear the classification cache."""
        self.cache.clear()
    
    def get_cache_stats(self) -> Dict:
        """Get cache statistics."""
        now = datetime.now()
        valid_entries = sum(
            1 for entry in self.cache.values()
            if now - entry['timestamp'] < self.cache_ttl
        )
        
        return {
            'total_entries': len(self.cache),
            'valid_entries': valid_entries,
            'cache_hit_ratio': valid_entries / max(len(self.cache), 1)
        } 