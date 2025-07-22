#!/usr/bin/env python3
"""
Discernus Agents - A collection of specialized agents for computational text analysis.
"""

from .project_coherence_analyst import ProjectCoherenceAnalyst
from .ensemble_configuration_agent import EnsembleConfigurationAgent
from .execution_planner_agent import ExecutionPlannerAgent
from .methodological_overwatch_agent import MethodologicalOverwatchAgent
from .experiment_conclusion_agent import ExperimentConclusionAgent
from .data_extraction_agent import DataExtractionAgent

__all__ = [
    "AnalysisAgent",
    "DataExtractionAgent",
    "DetectiveAgent",
    "GenericExpertAgent",
    "InitializationAgent",
    "DiscernusLibrarianAgent",
    "QualitativeAnalysisAgent",
    "QuantitativeAnalysisAgent",
    "ResearcherAgent",
    "SynthesisAgent",
    "ValidationAgent",
] 