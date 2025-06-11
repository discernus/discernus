"""
Conversation Context Manager for Narrative Gravity Analysis Chatbot

Maintains conversation state, analysis history, and user preferences
across chat interactions.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

@dataclass
class AnalysisRecord:
    """Record of a completed analysis"""
    analysis_id: str
    text_content: str
    framework_used: str
    timestamp: datetime
    results: Dict[str, Any]
    summary: str
    
    def __post_init__(self):
        if isinstance(self.timestamp, str):
            self.timestamp = datetime.fromisoformat(self.timestamp)

@dataclass
class UserPreferences:
    """User preferences for analysis"""
    preferred_framework: str = "fukuyama_identity"
    show_detailed_explanations: bool = True
    include_visualizations: bool = True
    export_format: str = "json"

@dataclass
class DipoleDefinition:
    """Definition of a dipole in framework creation"""
    name: str = ""
    description: str = ""
    positive_well: Dict[str, Any] = field(default_factory=dict)
    negative_well: Dict[str, Any] = field(default_factory=dict)
    angles: Dict[str, int] = field(default_factory=dict)
    weights: Dict[str, float] = field(default_factory=dict)

@dataclass
class FrameworkCreationSession:
    """Tracks progress of framework creation conversation"""
    framework_name: str = ""
    display_name: str = ""
    description: str = ""
    source_material: str = ""
    theoretical_foundation: str = ""
    dipoles: List[DipoleDefinition] = field(default_factory=list)
    current_dipole_index: int = 0
    creation_step: str = "conceptualization"  # conceptualization, validation, refinement, implementation, testing
    test_texts: List[str] = field(default_factory=list)
    test_results: List[Dict] = field(default_factory=list)

class ConversationState(Enum):
    """Current state of conversation"""
    GREETING = "greeting"
    WAITING_FOR_INPUT = "waiting_for_input"
    PROCESSING_ANALYSIS = "processing_analysis"
    SHOWING_RESULTS = "showing_results"
    COMPARING_ANALYSES = "comparing_analyses"
    EXPLAINING_CONCEPTS = "explaining_concepts"
    # Framework creation states
    CREATING_FRAMEWORK = "creating_framework"
    DEFINING_DIPOLES = "defining_dipoles"
    CONFIGURING_WELLS = "configuring_wells"
    TESTING_FRAMEWORK = "testing_framework"
    FINALIZING_FRAMEWORK = "finalizing_framework"

class ConversationContext:
    """
    Manages conversation state and history for narrative gravity analysis chatbot.
    
    Tracks:
    - Current framework and preferences
    - Analysis history
    - Conversation state
    - User preferences
    """
    
    def __init__(self, user_id: Optional[str] = None):
        self.user_id = user_id or f"user_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        self.session_start = datetime.now()
        
        # Current state
        self.current_framework = "fukuyama_identity"
        self.conversation_state = ConversationState.GREETING
        self.user_preferences = UserPreferences()
        
        # Analysis history
        self.analysis_history: List[AnalysisRecord] = []
        self.last_analysis: Optional[AnalysisRecord] = None
        
        # Framework creation session
        self.framework_creation: Optional[FrameworkCreationSession] = None
        
        # Conversation memory
        self.message_history: List[Dict[str, Any]] = []
        self.context_variables: Dict[str, Any] = {}
        
        # Statistics
        self.total_analyses = 0
        self.frameworks_used = set()
        
    def add_message(self, role: str, content: str, metadata: Optional[Dict] = None) -> None:
        """
        Add a message to conversation history.
        
        Args:
            role: 'user' or 'assistant'
            content: Message content
            metadata: Optional metadata about the message
        """
        message = {
            'role': role,
            'content': content,
            'timestamp': datetime.now(),
            'metadata': metadata or {}
        }
        self.message_history.append(message)
    
    def set_framework(self, framework_name: str) -> bool:
        """
        Set the current framework for analysis.
        
        Args:
            framework_name: Name of framework to use
            
        Returns:
            True if framework was set successfully
        """
        # Validate framework exists (this could be enhanced with actual validation)
        valid_frameworks = {
            'fukuyama_identity', 'civic_virtue', 
            'political_spectrum', 'moral_rhetorical_posture'
        }
        
        if framework_name in valid_frameworks:
            self.current_framework = framework_name
            self.frameworks_used.add(framework_name)
            self.context_variables['framework_changed'] = True
            return True
        return False
    
    def add_analysis(self, analysis_record: AnalysisRecord) -> None:
        """
        Add completed analysis to history.
        
        Args:
            analysis_record: Complete analysis record
        """
        self.analysis_history.append(analysis_record)
        self.last_analysis = analysis_record
        self.total_analyses += 1
        self.frameworks_used.add(analysis_record.framework_used)
        
        # Update conversation state
        self.conversation_state = ConversationState.SHOWING_RESULTS
    
    def get_recent_analyses(self, limit: int = 5) -> List[AnalysisRecord]:
        """
        Get most recent analyses.
        
        Args:
            limit: Maximum number of analyses to return
            
        Returns:
            List of recent analysis records
        """
        return self.analysis_history[-limit:] if self.analysis_history else []
    
    def find_analysis_by_content(self, search_term: str) -> Optional[AnalysisRecord]:
        """
        Find analysis by searching content.
        
        Args:
            search_term: Term to search for in analysis text
            
        Returns:
            First matching analysis record, if any
        """
        search_lower = search_term.lower()
        for analysis in reversed(self.analysis_history):  # Search most recent first
            if search_lower in analysis.text_content.lower() or search_lower in analysis.summary.lower():
                return analysis
        return None
    
    def get_framework_usage_stats(self) -> Dict[str, int]:
        """
        Get statistics on framework usage.
        
        Returns:
            Dictionary mapping framework names to usage counts
        """
        stats = {}
        for analysis in self.analysis_history:
            framework = analysis.framework_used
            stats[framework] = stats.get(framework, 0) + 1
        return stats
    
    def can_compare_analyses(self) -> bool:
        """
        Check if there are enough analyses for comparison.
        
        Returns:
            True if comparison is possible
        """
        return len(self.analysis_history) >= 2
    
    def get_comparison_candidates(self) -> List[AnalysisRecord]:
        """
        Get analyses suitable for comparison.
        
        Returns:
            List of analysis records that can be compared
        """
        if not self.can_compare_analyses():
            return []
        
        # Return last few analyses for comparison
        return self.analysis_history[-3:] if len(self.analysis_history) >= 3 else self.analysis_history
    
    def set_context_variable(self, key: str, value: Any) -> None:
        """
        Set a context variable for conversation tracking.
        
        Args:
            key: Variable name
            value: Variable value
        """
        self.context_variables[key] = value
    
    def get_context_variable(self, key: str, default: Any = None) -> Any:
        """
        Get a context variable value.
        
        Args:
            key: Variable name
            default: Default value if key not found
            
        Returns:
            Variable value or default
        """
        return self.context_variables.get(key, default)
    
    def update_state(self, new_state: ConversationState) -> None:
        """
        Update the conversation state.
        
        Args:
            new_state: New conversation state
        """
        self.conversation_state = new_state
        self.context_variables['state_changed'] = True
    
    def get_session_summary(self) -> Dict[str, Any]:
        """
        Get summary of current conversation session.
        
        Returns:
            Dictionary with session statistics and context
        """
        duration = datetime.now() - self.session_start
        
        return {
            'user_id': self.user_id,
            'session_duration_minutes': duration.total_seconds() / 60,
            'total_messages': len(self.message_history),
            'total_analyses': self.total_analyses,
            'frameworks_used': list(self.frameworks_used),
            'current_framework': self.current_framework,
            'current_state': self.conversation_state.value,
            'has_analysis_history': bool(self.analysis_history),
            'can_compare': self.can_compare_analyses()
        }
    
    def clear_history(self, keep_preferences: bool = True) -> None:
        """
        Clear conversation history.
        
        Args:
            keep_preferences: Whether to preserve user preferences
        """
        self.analysis_history = []
        self.last_analysis = None
        self.message_history = []
        self.context_variables = {}
        self.total_analyses = 0
        self.frameworks_used = set()
        self.framework_creation = None
        
        if not keep_preferences:
            self.user_preferences = UserPreferences()
        
        self.conversation_state = ConversationState.GREETING

    # Framework creation methods
    
    def start_framework_creation(self, source_material: str = "") -> None:
        """Start a new framework creation session."""
        self.framework_creation = FrameworkCreationSession(source_material=source_material)
        self.conversation_state = ConversationState.CREATING_FRAMEWORK
    
    def is_creating_framework(self) -> bool:
        """Check if currently in framework creation mode."""
        return self.framework_creation is not None
    
    def get_framework_creation(self) -> Optional[FrameworkCreationSession]:
        """Get current framework creation session."""
        return self.framework_creation
    
    def add_dipole_to_framework(self, dipole: DipoleDefinition) -> None:
        """Add a dipole definition to the current framework."""
        if self.framework_creation:
            self.framework_creation.dipoles.append(dipole)
    
    def update_framework_step(self, step: str) -> None:
        """Update the current step in framework creation."""
        if self.framework_creation:
            self.framework_creation.creation_step = step
    
    def finalize_framework_creation(self) -> Optional[FrameworkCreationSession]:
        """Complete framework creation and return the session."""
        session = self.framework_creation
        self.framework_creation = None
        self.conversation_state = ConversationState.WAITING_FOR_INPUT
        return session 