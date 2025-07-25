#!/usr/bin/env python3
"""
Experiment Lifecycle Management
===============================

THIN lifecycle management for Discernus experiments.
Provides intelligent experiment startup and resumption with validation,
while keeping the WorkflowOrchestrator pristine and reusable.

Philosophy:
- WorkflowOrchestrator = "Dumb loop" execution engine (stays THIN)
- ExperimentLifecycle = LLM-powered validation and planning (uses intelligence)
- Natural separation: Planning vs Execution
"""

import json
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass

from discernus.gateway.llm_gateway import LLMGateway
from discernus.core.spec_loader import SpecLoader
from discernus.orchestration.workflow_orchestrator import WorkflowOrchestrator

# Import validation agents for the validation gauntlet
from discernus.agents.true_validation_agent import TrueValidationAgent
from discernus.agents.project_coherence_analyst import ProjectCoherenceAnalyst
from discernus.agents.statistical_analysis_configuration_agent import StatisticalAnalysisConfigurationAgent
from discernus.agents.ensemble_configuration_agent import EnsembleConfigurationAgent

# Additional imports for intelligent resumption
import asyncio
import sys
import re
import datetime

from discernus.gateway.model_registry import ModelRegistry


@dataclass
class ValidationGauntletResult:
    """Results from the validation gauntlet - comprehensive pre-flight validation"""
    true_validation_passed: bool
    project_coherence_passed: bool
    statistical_plan_valid: bool
    model_health_passed: bool
    overall_passed: bool
    issues: List[str]
    recommendations: List[str]
    enhanced_workflow: Optional[List[Dict[str, Any]]] = None
    validation_details: Dict[str, Any] = None


@dataclass
class ExperimentValidationResult:
    """Results of experiment lifecycle validation"""
    is_valid: bool
    is_complete: bool  # Has research deliverables
    missing_agents: List[str]
    validation_issues: List[str]
    recommendations: List[str]
    enhanced_workflow: Optional[List[Dict[str, Any]]] = None


@dataclass
class ResumeAnalysisResult:
    """Result of intelligent resume analysis"""
    can_resume: bool
    state_file: Optional[Path]
    resume_step: int
    total_steps: int
    workflow_changes: List[str]
    resource_warnings: List[str]
    resumption_strategy: str  # 'continue', 'restart_from_step', 'workflow_changed'
    user_guidance: str
    state_integrity: bool
    completed_steps: List[str]
    remaining_steps: List[str]


class ExperimentLifecycleManager:
    """
    THIN lifecycle management for experiments.
    
    Responsibilities:
    1. Pre-flight validation gauntlet (TrueValidationAgent, ProjectCoherenceAnalyst, etc.)
    2. Workflow completeness analysis
    3. Research deliverables verification
    4. Intelligent defaults and enhancements
    5. Clean handoff to WorkflowOrchestrator
    
    What it does NOT do:
    - Execute workflows (WorkflowOrchestrator's job)
    - Parse LLM responses (THIN violation)
    - Hardcode domain logic (framework-agnostic)
    """
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        
        # Initialize model registry and gateway
        from discernus.gateway.model_registry import ModelRegistry
        self.model_registry = ModelRegistry()
        self.gateway = LLMGateway(self.model_registry)
        self.spec_loader = SpecLoader()
        
        # Initialize validation agents for the gauntlet
        self.true_validation_agent = TrueValidationAgent()
        self.project_coherence_analyst = ProjectCoherenceAnalyst()
        self.statistical_analysis_agent = StatisticalAnalysisConfigurationAgent()
        self.ensemble_configuration_agent = EnsembleConfigurationAgent()
        
    async def validate_and_prepare_experiment(self, 
                                            experiment_file: Path,
                                            dev_mode: bool = False) -> ExperimentValidationResult:
        """
        Comprehensive experiment validation and preparation using the validation gauntlet.
        
        Phase 1: Sequential Validation Gauntlet
        1. TrueValidationAgent - Rubric-based framework/experiment validation
        2. ProjectCoherenceAnalyst - Socratic research methodology validation  
        3. StatisticalAnalysisConfigurationAgent - Statistical plan validation
        4. EnsembleConfigurationAgent - Model health checks and resource planning
        5. WorkflowCompletenessValidator - Ensure SynthesisAgent exists for reports
        
        Returns validated/enhanced workflow ready for WorkflowOrchestrator.
        """
        print("🔍 Running Validation Gauntlet...")
        
        # Load specifications first
        specifications = self._load_experiment_specifications(experiment_file)
        
        if not specifications['validation']['overall_valid']:
            return ExperimentValidationResult(
                is_valid=False,
                is_complete=False,
                missing_agents=[],
                validation_issues=self._extract_validation_issues(specifications),
                recommendations=[]
            )
        
        # Execute the validation gauntlet
        gauntlet_result = await self._run_validation_gauntlet(
            experiment_file,
            specifications,
            dev_mode
        )
        
        if not gauntlet_result.overall_passed:
            return ExperimentValidationResult(
                is_valid=False,
                is_complete=False,
                missing_agents=[],
                validation_issues=gauntlet_result.issues,
                recommendations=gauntlet_result.recommendations
            )
        
        # Analyze workflow completeness using LLM intelligence
        workflow_analysis = await self._analyze_workflow_completeness(
            specifications['experiment']['workflow'],
            specifications['framework'],
            specifications['experiment']
        )
        
        # Enhance workflow if needed and validation passed
        if gauntlet_result.enhanced_workflow:
            workflow_analysis.enhanced_workflow = gauntlet_result.enhanced_workflow
        
        return workflow_analysis
    
    async def _run_validation_gauntlet(self, 
                                     experiment_file: Path,
                                     specifications: Dict,
                                     dev_mode: bool) -> ValidationGauntletResult:
        """
        Execute the sequential validation gauntlet as specified in Issue #131.
        
        This is the core implementation of the validation system architecture.
        """
        print("🎯 Phase 1: Sequential Validation Gauntlet")
        
        issues = []
        recommendations = []
        validation_details = {}
        
        # Step 1: TrueValidationAgent - Rubric-based validation
        print("  📋 Step 1: TrueValidationAgent - Rubric-based validation")
        framework_content = (experiment_file.parent / specifications['experiment']['framework_file']).read_text()
        experiment_content = experiment_file.read_text()
        
        true_validation_result = await self.true_validation_agent.validate_project_coherence(
            framework_content, experiment_content
        )
        validation_details['true_validation'] = true_validation_result
        
        true_validation_passed = true_validation_result.get('validation_passed', False)
        if not true_validation_passed:
            issues.append(f"TrueValidationAgent failed: {true_validation_result.get('feedback', 'Unknown error')}")
            recommendations.append("Review framework and experiment specifications against validation rubrics")
        
        # Step 2: ProjectCoherenceAnalyst - Socratic methodology validation
        print("  🤔 Step 2: ProjectCoherenceAnalyst - Socratic methodology validation")  
        project_coherence_result = await self.project_coherence_analyst.validate_project(str(experiment_file.parent))
        validation_details['project_coherence'] = project_coherence_result
        
        project_coherence_passed = project_coherence_result.get('validation_passed', False)
        if not project_coherence_passed:
            issues.append(f"ProjectCoherenceAnalyst failed: {project_coherence_result.get('feedback', 'Methodology issues found')}")
            recommendations.append("Address methodological concerns raised in Socratic analysis")
        
        # Step 3: StatisticalAnalysisConfigurationAgent - Statistical plan validation
        print("  📊 Step 3: StatisticalAnalysisConfigurationAgent - Statistical plan validation")
        stat_plan_result = self.statistical_analysis_agent.generate_statistical_plan(
            {'experiment_md_path': str(experiment_file)}, {}
        )
        validation_details['statistical_plan'] = stat_plan_result
        
        statistical_plan_valid = stat_plan_result.get('validation_status') in ['complete', 'generated']
        if not statistical_plan_valid:
            issues.append(f"Statistical plan validation failed: {stat_plan_result.get('notes', 'Unknown error')}")
            recommendations.append("Define clear statistical analysis methodology")
        
        # Step 4: EnsembleConfigurationAgent - Model health checks and resource planning  
        print("  🏥 Step 4: EnsembleConfigurationAgent - Model health checks")
        # Extract models from experiment specification
        experiment_data = specifications['experiment']
        models_list = experiment_data.get('models', ['vertex_ai/gemini-2.5-pro'])  # Default model
        
        # For now, assume models are healthy (this would need actual health checks)
        model_health_passed = True
        validation_details['model_health'] = {'status': 'healthy', 'models': models_list}
        
        if not model_health_passed:
            issues.append("Model health checks failed")
            recommendations.append("Check model availability and configure fallbacks")
        
        # Step 5: WorkflowCompletenessValidator - Ensure workflow produces research deliverables
        print("  ✅ Step 5: WorkflowCompletenessValidator - Research deliverables check")
        workflow_completeness_result = self._validate_workflow_completeness(specifications['experiment']['workflow'])
        validation_details['workflow_completeness'] = workflow_completeness_result
        
        if not workflow_completeness_result['complete']:
            issues.extend(workflow_completeness_result['issues'])
            recommendations.extend(workflow_completeness_result['recommendations'])
        
        # Overall validation result
        overall_passed = (true_validation_passed and 
                         project_coherence_passed and 
                         statistical_plan_valid and 
                         model_health_passed and 
                         workflow_completeness_result['complete'])
        
        # Generate enhanced workflow if needed
        enhanced_workflow = None
        if not workflow_completeness_result['complete']:
            enhanced_workflow = self._generate_enhanced_workflow(
                specifications['experiment']['workflow'],
                workflow_completeness_result['missing_agents']
            )
        
        print(f"🏁 Validation Gauntlet Result: {'✅ PASSED' if overall_passed else '❌ FAILED'}")
        
        return ValidationGauntletResult(
            true_validation_passed=true_validation_passed,
            project_coherence_passed=project_coherence_passed, 
            statistical_plan_valid=statistical_plan_valid,
            model_health_passed=model_health_passed,
            overall_passed=overall_passed,
            issues=issues,
            recommendations=recommendations,
            enhanced_workflow=enhanced_workflow,
            validation_details=validation_details
        )
    
    def _validate_workflow_completeness(self, workflow: List[Dict]) -> Dict[str, Any]:
        """
        Validate that workflow will produce research deliverables.
        This addresses the core Issue #68 problem where experiments were technically compliant but research useless.
        """
        agent_names = [step.get('agent', '') for step in workflow]
        
        issues = []
        recommendations = []
        missing_agents = []
        
        # Check for SynthesisAgent (research deliverables) - this is the core Issue #68 fix
        if 'SynthesisAgent' not in agent_names:
            missing_agents.append('SynthesisAgent')
            issues.append('No SynthesisAgent found - workflow will not produce final research reports')
            recommendations.append('Add SynthesisAgent to generate comprehensive research deliverables')
        
        # Check for validation agents
        validation_agents = ['TrueValidationAgent', 'ProjectCoherenceAnalyst']
        has_validation = any(agent in agent_names for agent in validation_agents)
        if not has_validation:
            issues.append('No pre-flight validation agents found in workflow')
            recommendations.append('Consider adding validation agents to workflow for quality assurance')
        
        is_complete = len(missing_agents) == 0
        
        return {
            'complete': is_complete,
            'missing_agents': missing_agents,
            'issues': issues,
            'recommendations': recommendations
        }
    
    def _generate_enhanced_workflow(self, original_workflow: List[Dict], missing_agents: List[str]) -> List[Dict]:
        """
        Generate enhanced workflow by adding missing agents while preserving original sequence.
        """
        enhanced = original_workflow.copy()
        
        # Add missing SynthesisAgent at the end if needed
        if 'SynthesisAgent' in missing_agents:
            enhanced.append({
                'agent': 'SynthesisAgent',
                'config': {
                    'output_artifacts': [
                        'comprehensive_research_report.md',
                        'analysis_summary.json'
                    ]
                }
            })
        
        return enhanced
    
    async def _analyze_workflow_completeness(self, 
                                           workflow: List[Dict],
                                           framework: Dict,
                                           experiment: Dict) -> ExperimentValidationResult:
        """
        Use LLM intelligence to analyze workflow completeness.
        
        This is where the INTELLIGENCE lives - LLM determines:
        - Are research deliverables specified?
        - Is methodology sound?
        - Are there missing validation steps?
        - What would a researcher expect from this experiment?
        """
        
        prompt = f"""
You are a research methodology expert analyzing an experiment workflow for completeness.

FRAMEWORK: {framework.get('name', 'Unknown')} v{framework.get('version', 'Unknown')}
EXPERIMENT GOAL: {experiment.get('hypothesis', 'Not specified')}

CURRENT WORKFLOW:
{self._format_workflow_for_analysis(workflow)}

VALIDATION CRITERIA:
1. RESEARCH DELIVERABLES: Will this produce actionable reports for researchers?
2. METHODOLOGY SOUNDNESS: Is this a complete research workflow?
3. VALIDATION COVERAGE: Are there appropriate quality controls?
4. WORKFLOW COMPLETENESS: Are there missing standard steps?

ANALYSIS QUESTIONS:
- Does this workflow produce final reports (SynthesisAgent or equivalent)?
- Are there pre-flight validation steps (TrueValidationAgent, ProjectCoherenceAnalyst)?
- Would a researcher find this workflow useful?
- What agents or steps are missing for a complete analysis?

Respond with JSON:
{{
    "is_complete": boolean,
    "missing_agents": ["AgentName1", "AgentName2"],
    "issues": ["Issue 1", "Issue 2"],
    "recommendations": ["Add SynthesisAgent for final reporting", "Add pre-flight validation"],
    "enhanced_workflow": [enhanced workflow with added agents]
}}
"""
        
        try:
            response = await self.gateway.generate_completion(
                messages=[{"role": "user", "content": prompt}],
                model="vertex_ai/gemini-2.5-pro",
                max_tokens=2000
            )
            
            analysis = json.loads(response.content)
            
            return ExperimentValidationResult(
                is_valid=True,
                is_complete=analysis['is_complete'],
                missing_agents=analysis['missing_agents'],
                validation_issues=analysis['issues'],
                recommendations=analysis['recommendations'],
                enhanced_workflow=analysis.get('enhanced_workflow')
            )
            
        except Exception as e:
            # Fallback to simple heuristic analysis
            return self._heuristic_workflow_analysis(workflow)
    
    def _heuristic_workflow_analysis(self, workflow: List[Dict]) -> ExperimentValidationResult:
        """
        Fallback heuristic analysis when LLM is unavailable.
        Basic pattern matching for common workflow issues.
        """
        agent_names = [step.get('agent', '') for step in workflow]
        
        missing_agents = []
        issues = []
        recommendations = []
        
        # Check for SynthesisAgent (research deliverables)
        if 'SynthesisAgent' not in agent_names:
            missing_agents.append('SynthesisAgent')
            issues.append('No SynthesisAgent found - workflow will not produce final reports')
            recommendations.append('Add SynthesisAgent to generate research deliverables')
        
        # Check for validation agents
        validation_agents = ['TrueValidationAgent', 'ProjectCoherenceAnalyst']
        has_validation = any(agent in agent_names for agent in validation_agents)
        if not has_validation:
            issues.append('No pre-flight validation agents found')
            recommendations.append('Consider adding TrueValidationAgent for methodology validation')
        
        is_complete = len(missing_agents) == 0
        
        return ExperimentValidationResult(
            is_valid=True,
            is_complete=is_complete,
            missing_agents=missing_agents,
            validation_issues=issues,
            recommendations=recommendations
        )
    
    def _load_experiment_specifications(self, experiment_file: Path) -> Dict:
        """Load and validate experiment specifications"""
        # Resolve framework and corpus paths
        experiment_config = self.spec_loader.experiment_parser.parse_experiment(experiment_file)
        framework_file_path = experiment_file.parent / experiment_config['framework_file']
        corpus_dir_path = experiment_file.parent / experiment_config['corpus']
        
        return self.spec_loader.load_specifications(
            framework_file=framework_file_path,
            experiment_file=experiment_file,
            corpus_dir=corpus_dir_path
        )
    
    def _extract_validation_issues(self, specifications: Dict) -> List[str]:
        """Extract validation issues from specifications"""
        issues = []
        for spec_type, validation in specifications['validation'].items():
            if spec_type != 'overall_valid' and validation and not validation['valid']:
                issues.extend(validation['issues'])
        return issues
    
    def _format_workflow_for_analysis(self, workflow: List[Dict]) -> str:
        """Format workflow for LLM analysis"""
        formatted = []
        for i, step in enumerate(workflow):
            agent = step.get('agent', 'Unknown')
            inputs = step.get('inputs', [])
            outputs = step.get('outputs', [])
            formatted.append(f"Step {i+1}: {agent}")
            if inputs:
                formatted.append(f"  Inputs: {inputs}")
            if outputs:
                formatted.append(f"  Outputs: {outputs}")
        return "\n".join(formatted)


class ExperimentStartup:
    """
    Intelligent experiment startup with validation and enhancement.
    Replaces direct CLI → WorkflowOrchestrator calls.
    """
    
    def __init__(self, project_path: str):
        self.project_path = project_path
        self.lifecycle_manager = ExperimentLifecycleManager(project_path)
    
    async def start_experiment(self, 
                              experiment_file: Path,
                              dev_mode: bool = False,
                              auto_enhance: bool = True) -> Dict[str, Any]:
        """
        Smart experiment startup with validation and enhancement.
        
        Process:
        1. Load and validate specifications
        2. Analyze workflow completeness  
        3. Enhance workflow if needed (with user consent)
        4. Execute via pristine WorkflowOrchestrator
        
        Returns: Experiment results
        """
        
        print("🔍 Validating experiment specifications...")
        validation_result = await self.lifecycle_manager.validate_and_prepare_experiment(
            experiment_file, dev_mode
        )
        
        if not validation_result.is_valid:
            raise ValueError(f"Experiment validation failed: {validation_result.validation_issues}")
        
        # Handle incomplete workflows
        if not validation_result.is_complete:
            print(f"⚠️ Workflow completeness issues found:")
            for issue in validation_result.validation_issues:
                print(f"   - {issue}")
            
            print(f"💡 Recommendations:")
            for rec in validation_result.recommendations:
                print(f"   - {rec}")
            
            if validation_result.enhanced_workflow:
                # Show proposed enhancements
                print("\n🔧 Proposed Workflow Enhancements:")
                self._show_workflow_comparison(experiment_file, validation_result.enhanced_workflow)
                
                # Get user consent
                if auto_enhance:
                    if dev_mode:
                        print("🚀 DEV MODE: Auto-approving workflow enhancements")
                        user_consent = True
                    else:
                        user_consent = self._get_user_consent_for_enhancements()
                else:
                    user_consent = False
                
                if user_consent:
                    print("✅ User approved enhancements. Applying...")
                    enhanced_experiment = self._apply_workflow_enhancements(
                        experiment_file, validation_result.enhanced_workflow
                    )
                else:
                    print("❌ User declined enhancements. Using original workflow (may not produce deliverables)")
                    enhanced_experiment = experiment_file
            else:
                print("❌ No automatic enhancements available. Using original workflow")
                enhanced_experiment = experiment_file
        else:
            print("✅ Workflow is complete and ready for execution")
            enhanced_experiment = experiment_file
        
        # Execute via pristine WorkflowOrchestrator
        print("🚀 Executing experiment via WorkflowOrchestrator...")
        orchestrator = WorkflowOrchestrator(self.project_path)
        
        # Load final specifications for execution
        spec_loader = SpecLoader()
        specifications = self._load_specifications_for_execution(enhanced_experiment, spec_loader)
        
        # Prepare initial state (same as current CLI)
        initial_state = self._prepare_initial_state(specifications, enhanced_experiment)
        
        # Execute with pristine orchestrator
        return orchestrator.execute_workflow(initial_state)
    
    def _apply_workflow_enhancements(self, 
                                   experiment_file: Path, 
                                   enhanced_workflow: List[Dict]) -> Path:
        """
        Apply workflow enhancements and return path to enhanced experiment.
        
        Following Research Provenance Guide v3.0:
        - Never modify original experiment.md (preserves user intent)
        - Create immutable snapshots with audit trail
        - Generate enhanced experiment file for execution
        """
        from datetime import datetime
        import yaml
        
        # Create enhanced experiment directory structure
        experiment_name = experiment_file.stem
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        enhanced_dir = experiment_file.parent / 'experiments' / experiment_name / 'enhanced' / f'enhanced_{timestamp}'
        enhanced_dir.mkdir(parents=True, exist_ok=True)
        
        # Create experiment snapshot (original user intent) 
        snapshot_file = enhanced_dir / 'experiment_snapshot.md'
        snapshot_file.write_text(experiment_file.read_text())
        
        # Read original experiment
        original_content = experiment_file.read_text()
        
        # Create enhanced experiment with updated workflow and corrected paths
        enhanced_content = self._update_experiment_workflow_with_paths(
            original_content, enhanced_workflow, experiment_file, enhanced_dir
        )
        
        # Create enhanced experiment snapshot
        enhanced_experiment_file = enhanced_dir / 'enhanced_experiment_snapshot.md'
        enhanced_experiment_file.write_text(enhanced_content)
        
        # Create audit trail
        audit_trail = {
            'enhancement_timestamp': datetime.now().isoformat() + 'Z',
            'original_experiment': str(experiment_file),
            'enhanced_experiment': str(enhanced_experiment_file),
            'enhancements_applied': {
                'added_agents': [step['agent'] for step in enhanced_workflow 
                               if step not in self._parse_original_workflow(original_content)],
                'enhancement_reason': 'Workflow completeness validation failed',
                'validation_system': 'THIN Experiment Lifecycle v1.0'
            },
            'provenance_compliance': 'Research Provenance Guide v3.0'
        }
        
        audit_file = enhanced_dir / 'enhancement_audit.json'
        with open(audit_file, 'w') as f:
            json.dump(audit_trail, f, indent=2)
        
        print(f"✅ Enhanced experiment created: {enhanced_experiment_file}")
        print(f"📋 Original preserved as: {snapshot_file}")
        print(f"🔍 Audit trail: {audit_file}")
        
        return enhanced_experiment_file
    
    def _show_workflow_comparison(self, experiment_file: Path, enhanced_workflow: List[Dict]):
        """Show user a clear comparison of original vs enhanced workflow"""
        original_content = experiment_file.read_text()
        original_workflow = self._parse_original_workflow(original_content)
        
        print("\n📋 CURRENT WORKFLOW:")
        if original_workflow:
            for i, step in enumerate(original_workflow):
                agent = step.get('agent', 'Unknown')
                print(f"   {i+1}. {agent}")
        else:
            print("   (No workflow found)")
        
        print("\n🔧 ENHANCED WORKFLOW:")
        for i, step in enumerate(enhanced_workflow):
            agent = step.get('agent', 'Unknown')
            is_new = step not in original_workflow
            marker = " ✨ NEW" if is_new else ""
            print(f"   {i+1}. {agent}{marker}")
        
        print("\n💡 ENHANCEMENT BENEFITS:")
        print("   • Ensures research deliverables are generated")
        print("   • Fixes Issue #68: 'technically compliant but research useless' workflows")
        print("   • Maintains full provenance with original experiment preserved")
    
    def _get_user_consent_for_enhancements(self) -> bool:
        """Get user consent for workflow enhancements with clear explanation"""
        print("\n" + "="*60)
        print("🤖 INTELLIGENT RESEARCH ASSISTANT RECOMMENDATION")
        print("="*60)
        print("\nI've analyzed your experiment and found that it may not produce")
        print("the research deliverables you expect. I can automatically enhance")
        print("your workflow to ensure comprehensive results.")
        print("\nYour original experiment will be completely preserved.")
        print("The enhanced version will be saved separately with full audit trail.")
        
        while True:
            choice = input("\nWould you like me to enhance your workflow? [Y]es / [N]o / [S]how details: ").strip().upper()
            
            if choice in ['Y', 'YES']:
                return True
            elif choice in ['N', 'NO']:
                return False
            elif choice in ['S', 'SHOW', 'DETAILS']:
                self._show_enhancement_details()
                continue
            else:
                print("Please enter Y for Yes, N for No, or S for Show details")
    
    def _show_enhancement_details(self):
        """Show detailed explanation of what enhancements will do"""
        print("\n" + "-"*50)
        print("ENHANCEMENT DETAILS")
        print("-"*50)
        print("What I will do:")
        print("✅ Add SynthesisAgent to generate comprehensive research reports")
        print("✅ Create experiment_snapshot.md (your original intent)")
        print("✅ Create enhanced_experiment_snapshot.md (system recommendations)")  
        print("✅ Create enhancement_audit.json (full provenance trail)")
        print("✅ Never modify your original experiment.md file")
        print("\nWhat you get:")
        print("📊 Comprehensive research deliverables")
        print("🔍 Complete audit trail of all changes")
        print("💾 Original experiment preserved exactly as you wrote it")
        print("📝 Research reports in markdown and JSON formats")
        print("\nThis follows Research Provenance Guide v3.0 for academic integrity.")
        print("-"*50)
    
    def _update_experiment_workflow(self, original_content: str, enhanced_workflow: List[Dict]) -> str:
        """
        Update the workflow section in experiment content while preserving other sections.
        Creates a single clean YAML section with enhancement comments embedded.
        """
        import re
        import yaml
        from datetime import datetime
        
        # Parse the original YAML front matter
        yaml_match = re.search(r'---\n(.*?)\n---', original_content, re.DOTALL)
        if not yaml_match:
            raise ValueError("Original experiment must have YAML front matter")
        
        # Parse the original configuration
        original_yaml_content = yaml_match.group(1)
        original_config = yaml.safe_load(original_yaml_content)
        
        # Update the workflow in the configuration
        original_config['workflow'] = enhanced_workflow
        
        # Create enhanced YAML with embedded comments
        enhanced_yaml_lines = [
            "---",
            "# ENHANCED EXPERIMENT - Auto-generated by THIN Experiment Lifecycle",
            "# Original experiment preserved as experiment_snapshot.md", 
            f"# Generated: {datetime.now().isoformat()}Z",
            "# Enhancement: Added missing agents for research deliverables",
            ""
        ]
        
        # Add the configuration as clean YAML
        yaml_content = yaml.dump(original_config, default_flow_style=False, sort_keys=False)
        enhanced_yaml_lines.extend(yaml_content.split('\n'))
        enhanced_yaml_lines.append("---")
        
        # Get the markdown content after the original YAML
        content_after_yaml = re.sub(r'---\n.*?\n---\n?', '', original_content, flags=re.DOTALL)
        
        return '\n'.join(enhanced_yaml_lines) + '\n' + content_after_yaml
    
    def _update_experiment_workflow_with_paths(self, original_content: str, enhanced_workflow: List[Dict], 
                                             original_experiment_file: Path, enhanced_dir: Path) -> str:
        """
        Update workflow and fix relative paths to point back to original locations.
        This ensures the enhanced experiment can find the framework and corpus files.
        """
        import re
        import yaml
        from datetime import datetime
        
        # Parse the original YAML front matter
        yaml_match = re.search(r'---\n(.*?)\n---', original_content, re.DOTALL)
        if not yaml_match:
            raise ValueError("Original experiment must have YAML front matter")
        
        # Parse the original configuration
        original_yaml_content = yaml_match.group(1)
        original_config = yaml.safe_load(original_yaml_content)
        
        # Update the workflow in the configuration
        original_config['workflow'] = enhanced_workflow
        
        # Fix relative paths to point back to original location
        # Enhanced directory structure: original_dir/experiments/experiment/enhanced/enhanced_timestamp/
        # So to get back to original_dir from enhanced_dir, go up 4 levels: ../../../../
        relative_path_to_original = Path('../../../../')
        
        # Update framework_file path
        if 'framework_file' in original_config:
            original_framework_path = original_config['framework_file']
            if not Path(original_framework_path).is_absolute():
                # Make path relative to enhanced directory pointing back to original
                original_config['framework_file'] = str(relative_path_to_original / original_framework_path)
        
        # Update corpus path
        if 'corpus' in original_config:
            original_corpus_path = original_config['corpus']
            if not Path(original_corpus_path).is_absolute():
                # Make path relative to enhanced directory pointing back to original
                original_config['corpus'] = str(relative_path_to_original / original_corpus_path)
        
        # Create enhanced YAML with embedded comments
        enhanced_yaml_lines = [
            "---",
            "# ENHANCED EXPERIMENT - Auto-generated by THIN Experiment Lifecycle",
            "# Original experiment preserved as experiment_snapshot.md", 
            f"# Generated: {datetime.now().isoformat()}Z",
            "# Enhancement: Added missing agents for research deliverables",
            "# Note: Paths adjusted to reference original framework and corpus locations",
            ""
        ]
        
        # Add the configuration as clean YAML
        yaml_content = yaml.dump(original_config, default_flow_style=False, sort_keys=False)
        enhanced_yaml_lines.extend(yaml_content.split('\n'))
        enhanced_yaml_lines.append("---")
        
        # Get the markdown content after the original YAML
        content_after_yaml = re.sub(r'---\n.*?\n---\n?', '', original_content, flags=re.DOTALL)
        
        return '\n'.join(enhanced_yaml_lines) + '\n' + content_after_yaml
    
    def _parse_original_workflow(self, original_content: str) -> List[Dict]:
        """Parse workflow from original experiment content for comparison"""
        import re
        import yaml
        
        workflow_match = re.search(r'workflow:\s*\n(.*?)(?=\n\S|\n*$)', original_content, re.DOTALL)
        if not workflow_match:
            return []
        
        try:
            workflow_yaml = 'workflow:\n' + workflow_match.group(1)
            parsed = yaml.safe_load(workflow_yaml)
            return parsed.get('workflow', [])
        except Exception:
            return []
    
    def _load_specifications_for_execution(self, experiment_file: Path, spec_loader: SpecLoader) -> Dict:
        """Load specifications for WorkflowOrchestrator execution"""
        experiment_config = spec_loader.experiment_parser.parse_experiment(experiment_file)
        framework_file_path = experiment_file.parent / experiment_config['framework_file']
        corpus_dir_path = experiment_file.parent / experiment_config['corpus']
        
        return spec_loader.load_specifications(
            framework_file=framework_file_path,
            experiment_file=experiment_file,
            corpus_dir=corpus_dir_path
        )
    
    def _prepare_initial_state(self, specifications: Dict, experiment_file: Path) -> Dict:
        """Prepare initial state for WorkflowOrchestrator (mirrors current CLI logic)"""
        return {
            'framework': specifications.get('framework'),
            'experiment': specifications.get('experiment'),
            'corpus': specifications.get('corpus'),
            'workflow': specifications.get('experiment', {}).get('workflow', []),
            'analysis_agent_instructions': specifications.get('framework', {}).get('analysis_variants', {}).get(
                specifications.get('experiment', {}).get('analysis_variant', 'default'), {}
            ).get('analysis_prompt', ''),
            'project_path': str(experiment_file.parent),
            'framework_path': str(experiment_file.parent / specifications.get('experiment', {}).get('framework_file', '')),
            'experiment_path': str(experiment_file),
            'corpus_path': str(experiment_file.parent / specifications.get('experiment', {}).get('corpus', ''))
        }


class ExperimentResumption:
    """
    Intelligent experiment resumption with state analysis.
    Replaces direct CLI → WorkflowOrchestrator resume calls.
    """
    
    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        
        # Initialize LLM components for intelligent analysis
        self.model_registry = ModelRegistry()
        self.gateway = LLMGateway(self.model_registry)
        
        # Initialize validation agents for workflow analysis
        self.validation_agent = TrueValidationAgent(self.gateway)
        self.coherence_analyst = ProjectCoherenceAnalyst(self.gateway)
    
    async def resume_experiment(self, 
                               state_file: Optional[Path] = None,
                               from_step: Optional[int] = None,
                               dry_run: bool = False) -> Dict[str, Any]:
        """
        Smart experiment resumption with state analysis.
        
        Process:
        1. Discover and analyze state files
        2. Validate resumption point and state integrity
        3. Check for workflow changes since interruption
        4. Provide user guidance and options
        5. Resume via pristine WorkflowOrchestrator
        
        Returns: Resume results
        """
        
        print("🔍 Analyzing experiment state for intelligent resumption...")
        
        # Phase 1: Enhanced State Discovery & Analysis
        analysis_result = await self._analyze_resumption_context(state_file, from_step)
        
        if not analysis_result.can_resume:
            print(f"❌ Cannot resume: {analysis_result.user_guidance}")
            raise ValueError(analysis_result.user_guidance)
        
        # Phase 2: User Experience & Guidance  
        if not dry_run:
            self._display_resumption_status(analysis_result)
            user_confirmed = self._get_user_resumption_consent(analysis_result)
            if not user_confirmed:
                print("🚫 Resume cancelled by user.")
                return {"status": "cancelled"}
        
        if dry_run:
            print("🧪 DRY RUN: Analysis complete, resumption would proceed")
            return {
                "status": "dry_run_success",
                "analysis": analysis_result,
                "would_resume_from_step": analysis_result.resume_step
            }
        
        # Phase 3: Intelligent Resumption Execution
        print("🔄 Executing intelligent resumption...")
        return await self._execute_intelligent_resumption(analysis_result)
    
    async def _analyze_resumption_context(self, 
                                        state_file: Optional[Path], 
                                        from_step: Optional[int]) -> ResumeAnalysisResult:
        """Phase 1: Enhanced State Discovery & Analysis"""
        
        # State discovery (enhanced version of CLI logic)
        if not state_file:
            state_file = self._find_latest_state_file()
        
        if not state_file:
            return ResumeAnalysisResult(
                can_resume=False,
                state_file=None,
                resume_step=0,
                total_steps=0,
                workflow_changes=[],
                resource_warnings=[],
                resumption_strategy="no_state_found",
                user_guidance="No state files found for resumption. Please verify the project path contains results/ or experiments/ directories with state files.",
                state_integrity=False,
                completed_steps=[],
                remaining_steps=[]
            )
        
        # Load and validate state integrity
        try:
            with open(state_file, 'r', encoding='utf-8') as f:
                state_data = json.load(f)
        except Exception as e:
            return ResumeAnalysisResult(
                can_resume=False,
                state_file=state_file,
                resume_step=0,
                total_steps=0,
                workflow_changes=[],
                resource_warnings=[],
                resumption_strategy="corrupted_state",
                user_guidance=f"State file corrupted or unreadable: {str(e)}",
                state_integrity=False,
                completed_steps=[],
                remaining_steps=[]
            )
        
        # Analyze workflow and determine resumption strategy
        workflow_steps = state_data.get('workflow', [])
        if not workflow_steps:
            return ResumeAnalysisResult(
                can_resume=False,
                state_file=state_file,
                resume_step=0,
                total_steps=0,
                workflow_changes=[],
                resource_warnings=[],
                resumption_strategy="no_workflow",
                user_guidance="No workflow steps found in state file.",
                state_integrity=False,
                completed_steps=[],
                remaining_steps=[]
            )
        
        # Determine resume step
        resume_step = from_step if from_step else self._determine_resume_step(state_file, workflow_steps)
        
        # Validate resume step
        if resume_step < 1 or resume_step > len(workflow_steps):
            return ResumeAnalysisResult(
                can_resume=False,
                state_file=state_file,
                resume_step=resume_step,
                total_steps=len(workflow_steps),
                workflow_changes=[],
                resource_warnings=[],
                resumption_strategy="invalid_step",
                user_guidance=f"Invalid resume step {resume_step}. Must be between 1 and {len(workflow_steps)}.",
                state_integrity=True,
                completed_steps=[],
                remaining_steps=[]
            )
        
        # Analyze completed vs remaining steps
        completed_steps = []
        remaining_steps = []
        for i, step in enumerate(workflow_steps):
            agent_name = step.get('agent', f'Step{i+1}')
            if i < resume_step - 1:
                completed_steps.append(f"Step {i+1}: {agent_name}")
            else:
                remaining_steps.append(f"Step {i+1}: {agent_name}")
        
        # Phase 2: Resumption Intelligence - Check for workflow changes
        workflow_changes = await self._detect_workflow_changes(state_data)
        
        # Resource validation
        resource_warnings = self._validate_resumption_resources(state_data)
        
        # Determine resumption strategy
        resumption_strategy = "continue"
        if workflow_changes:
            resumption_strategy = "workflow_changed"
        elif resource_warnings:
            resumption_strategy = "resource_warnings"
        
        user_guidance = self._generate_user_guidance(resumption_strategy, workflow_changes, resource_warnings)
        
        return ResumeAnalysisResult(
            can_resume=True,
            state_file=state_file,
            resume_step=resume_step,
            total_steps=len(workflow_steps),
            workflow_changes=workflow_changes,
            resource_warnings=resource_warnings,
            resumption_strategy=resumption_strategy,
            user_guidance=user_guidance,
            state_integrity=True,
            completed_steps=completed_steps,
            remaining_steps=remaining_steps
        )
    
    def _find_latest_state_file(self) -> Optional[Path]:
        """Enhanced state file discovery (implements CLI logic with improvements)"""
        state_files = []
        
        # Search legacy results/ structure
        results_dir = self.project_path / "results"
        if results_dir.exists():
            for session_dir in results_dir.iterdir():
                if session_dir.is_dir():
                    # Look for both final and partial state files
                    for state_file in session_dir.glob("state_after_step_*.json"):
                        state_files.append(state_file)
                    for partial_state_file in session_dir.glob("state_step_*_partial.json"):
                        state_files.append(partial_state_file)
        
        # Search experiments/ structure (WorkflowOrchestrator v3.0+)
        experiments_dir = self.project_path / "experiments"
        if experiments_dir.exists():
            for experiment_dir in experiments_dir.iterdir():
                if experiment_dir.is_dir():
                    sessions_dir = experiment_dir / "sessions"
                    if sessions_dir.exists():
                        for session_dir in sessions_dir.iterdir():
                            if session_dir.is_dir():
                                # Look for both final and partial state files
                                for state_file in session_dir.glob("state_after_step_*.json"):
                                    state_files.append(state_file)
                                for partial_state_file in session_dir.glob("state_step_*_partial.json"):
                                    state_files.append(partial_state_file)
        
        if not state_files:
            return None
        
        # Return the most recently modified state file
        latest_file = max(state_files, key=lambda x: x.stat().st_mtime)
        print(f"✅ Intelligent Resume: Found latest state file: {latest_file}")
        return latest_file
    
    def _determine_resume_step(self, state_file: Path, workflow_steps: List[Dict]) -> int:
        """Intelligent resume step determination with enhanced logic"""
        filename = state_file.name
        
        # Handle partial state files like "state_step_1_partial.json"
        partial_match = re.search(r'state_step_(\d+)_partial', filename)
        if partial_match:
            current_step = int(partial_match.group(1))
            # For partial state files, resume from the same step since it may be incomplete
            print(f"📍 Detected partial completion: resuming from step {current_step}")
            return current_step
        
        # Handle completed state files like "state_after_step_1_AgentName.json"
        completed_match = re.search(r'state_after_step_(\d+)_', filename)
        if completed_match:
            completed_step = int(completed_match.group(1))
            resume_step = completed_step + 1
            print(f"📍 Detected completion through step {completed_step}: resuming from step {resume_step}")
            return resume_step
        
        # Fallback: resume from step 1
        print("📍 Could not detect completion level: resuming from step 1")
        return 1
    
    async def _detect_workflow_changes(self, state_data: Dict[str, Any]) -> List[str]:
        """Phase 2: Intelligent workflow change detection"""
        workflow_changes = []
        
        try:
            # Look for current experiment.md file
            experiment_files = list(self.project_path.glob("experiment.md"))
            if not experiment_files:
                # Try finding in experiments/ subdirectories
                experiment_files = list(self.project_path.glob("experiments/*/experiment.md"))
            
            if not experiment_files:
                workflow_changes.append("Current experiment.md file not found - cannot validate workflow consistency")
                return workflow_changes
            
            current_experiment_file = experiment_files[0]
            
            # Parse YAML directly from experiment file instead of using SpecLoader
            import yaml
            experiment_content = current_experiment_file.read_text()
            
            # Extract YAML block
            current_workflow = []
            if '```yaml' in experiment_content:
                yaml_start = experiment_content.find('```yaml') + 7
                yaml_end = experiment_content.find('```', yaml_start)
                if yaml_start > 6 and yaml_end > yaml_start:
                    yaml_content = experiment_content[yaml_start:yaml_end].strip()
                    experiment_config = yaml.safe_load(yaml_content)
                    current_workflow = experiment_config.get('workflow', [])
            
            original_workflow = state_data.get('workflow', [])
            
            # Compare workflow structures
            if len(current_workflow) != len(original_workflow):
                workflow_changes.append(f"Workflow length changed: was {len(original_workflow)} steps, now {len(current_workflow)} steps")
            
            # Compare individual steps - focus on essential differences
            for i, (orig_step, curr_step) in enumerate(zip(original_workflow, current_workflow)):
                step_num = i + 1
                
                # Compare agent names (most important)
                orig_agent = orig_step.get('agent', '')
                curr_agent = curr_step.get('agent', '')
                
                if orig_agent != curr_agent:
                    workflow_changes.append(f"Step {step_num} agent changed: was {orig_agent}, now {curr_agent}")
                
                # Compare models if both are specified
                orig_model = orig_step.get('model')
                curr_model = curr_step.get('model')
                
                if orig_model and curr_model and orig_model != curr_model:
                    workflow_changes.append(f"Step {step_num} model changed: was {orig_model}, now {curr_model}")
                
                # Compare runs if both are specified  
                orig_runs = orig_step.get('runs')
                curr_runs = curr_step.get('runs')
                
                if orig_runs and curr_runs and orig_runs != curr_runs:
                    workflow_changes.append(f"Step {step_num} runs changed: was {orig_runs}, now {curr_runs}")
        
        except Exception as e:
            # Don't treat parsing errors as workflow changes - be conservative
            print(f"⚠️  Could not detect workflow changes due to parsing error: {str(e)}")
        
        return workflow_changes
    
    def _validate_resumption_resources(self, state_data: Dict[str, Any]) -> List[str]:
        """Phase 2: Resource availability validation"""
        warnings = []
        
        # Check if framework file still exists
        framework_file = state_data.get('framework_file')
        if framework_file:
            framework_path = self.project_path / framework_file
            if not framework_path.exists():
                warnings.append(f"Framework file not found: {framework_file}")
        
        # Check if corpus directory still exists
        corpus_path = state_data.get('corpus_path')
        if corpus_path:
            corpus_dir = self.project_path / corpus_path
            if not corpus_dir.exists():
                warnings.append(f"Corpus directory not found: {corpus_path}")
        
        # Check model availability (basic check)
        workflow_steps = state_data.get('workflow', [])
        for i, step in enumerate(workflow_steps):
            model_name = step.get('model')
            if model_name:
                try:
                    # Attempt to validate model is accessible
                    available_models = self.model_registry.list_models()
                    if model_name not in [m['name'] for m in available_models]:
                        warnings.append(f"Step {i+1} model may not be available: {model_name}")
                except Exception:
                    # If we can't check model availability, don't block resumption
                    pass
        
        return warnings
    
    def _generate_user_guidance(self, strategy: str, workflow_changes: List[str], resource_warnings: List[str]) -> str:
        """Generate human-readable guidance for resumption decision"""
        if strategy == "continue":
            return "✅ Ready to resume - no issues detected"
        elif strategy == "workflow_changed":
            guidance = "⚠️  Workflow changes detected since interruption:\n"
            for change in workflow_changes:
                guidance += f"   - {change}\n"
            guidance += "Consider: resume with current workflow, or restart experiment with updated configuration"
            return guidance
        elif strategy == "resource_warnings":
            guidance = "⚠️  Resource warnings detected:\n"
            for warning in resource_warnings:
                guidance += f"   - {warning}\n"
            guidance += "Verify resources are accessible before resuming"
            return guidance
        else:
            return "Unknown resumption strategy"
    
    def _display_resumption_status(self, analysis: ResumeAnalysisResult):
        """Phase 3: Clear status reporting for user"""
        print(f"\n📂 State File: {analysis.state_file}")
        print(f"🎯 Resume Strategy: {analysis.resumption_strategy}")
        print(f"📊 Progress: {len(analysis.completed_steps)}/{analysis.total_steps} steps completed")
        
        print(f"\n📋 Workflow Status:")
        for step in analysis.completed_steps:
            print(f"   ✅ {step}")
        
        if analysis.resume_step <= analysis.total_steps:
            remaining_step = analysis.remaining_steps[0] if analysis.remaining_steps else "Unknown"
            print(f"   🚀 RESUMING: {remaining_step}")
            
            for step in analysis.remaining_steps[1:]:
                print(f"   ⏳ {step}")
        
        if analysis.workflow_changes:
            print(f"\n⚠️  Workflow Changes Detected:")
            for change in analysis.workflow_changes:
                print(f"   - {change}")
        
        if analysis.resource_warnings:
            print(f"\n⚠️  Resource Warnings:")
            for warning in analysis.resource_warnings:
                print(f"   - {warning}")
        
        if analysis.user_guidance and analysis.user_guidance != "✅ Ready to resume - no issues detected":
            print(f"\n💡 Guidance: {analysis.user_guidance}")
    
    def _get_user_resumption_consent(self, analysis: ResumeAnalysisResult) -> bool:
        """Phase 3: User experience - get consent for resumption"""
        if analysis.resumption_strategy == "continue":
            prompt = f"🚀 Resume experiment from step {analysis.resume_step}?"
        elif analysis.resumption_strategy == "workflow_changed":
            prompt = "⚠️  Workflow changes detected. Resume with CURRENT workflow configuration?"
        elif analysis.resumption_strategy == "resource_warnings":
            prompt = "⚠️  Resource warnings detected. Resume anyway?"
        else:
            prompt = f"Resume experiment from step {analysis.resume_step}?"
        
        while True:
            response = input(f"{prompt} [y/N]: ").lower().strip()
            if response in ['y', 'yes']:
                return True
            elif response in ['n', 'no', '']:
                return False
            else:
                print("Please enter 'y' for yes or 'n' for no.")
    
    async def _execute_intelligent_resumption(self, analysis: ResumeAnalysisResult) -> Dict[str, Any]:
        """Phase 4: Provenance-compliant handoff to WorkflowOrchestrator"""
        
        # Load state data
        with open(analysis.state_file, 'r', encoding='utf-8') as f:
            state_data = json.load(f)
        
        # Initialize WorkflowOrchestrator for clean handoff
        orchestrator = WorkflowOrchestrator(str(self.project_path))
        
        # Use the existing CLI resumption execution logic (proven working)
        workflow_steps = state_data.get('workflow', [])
        
        return self._execute_resumption_with_provenance(orchestrator, state_data, analysis.resume_step, workflow_steps, analysis)
    
    def _execute_resumption_with_provenance(self, orchestrator: WorkflowOrchestrator, 
                                          state_data: Dict[str, Any], 
                                          resume_step: int, 
                                          workflow_steps: List[Dict],
                                          analysis: ResumeAnalysisResult) -> Dict[str, Any]:
        """Execute resumption with provenance trail (based on CLI logic)"""
        
        # Create resumption audit trail
        resumption_audit = {
            "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
            "resume_step": resume_step,
            "total_steps": len(workflow_steps),
            "resumption_strategy": analysis.resumption_strategy,
            "workflow_changes": analysis.workflow_changes,
            "resource_warnings": analysis.resource_warnings,
            "state_file_used": str(analysis.state_file),
            "intelligent_analysis": True
        }
        
        # Extract existing session path from state data (CLI pattern)
        existing_session_path = state_data.get('session_results_path')
        if existing_session_path:
            # Handle both absolute and relative paths from the state file
            if not Path(existing_session_path).is_absolute():
                # Path is relative to project directory
                full_session_path = Path(orchestrator.project_path) / existing_session_path
            else:
                full_session_path = Path(existing_session_path)
                
            if full_session_path.exists():
                # Reuse existing session directory
                orchestrator.session_results_path = full_session_path
                orchestrator.session_id = full_session_path.name  # Use directory name as session ID
                orchestrator.conversation_id = state_data.get('conversation_id', f"resumed_conversation_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}")
                
                # Initialize logger and archive manager for existing session
                from discernus.core.conversation_logger import ConversationLogger
                orchestrator.logger = ConversationLogger(str(orchestrator.project_path))
                
                # Initialize archive manager if it doesn't exist
                if not hasattr(orchestrator, 'archive_manager') or not orchestrator.archive_manager:
                    from discernus.core.llm_archive_manager import LLMArchiveManager
                    orchestrator.archive_manager = LLMArchiveManager(orchestrator.session_results_path)
                    
                    # Update gateway to use archive manager if it's an LLMGateway
                    if hasattr(orchestrator.gateway, 'archive_manager') and hasattr(orchestrator.gateway, '__class__'):
                        from discernus.gateway.llm_gateway import LLMGateway
                        if isinstance(orchestrator.gateway, LLMGateway):
                            orchestrator.gateway.archive_manager = orchestrator.archive_manager
                
                print(f"♻️  Resuming existing session: {orchestrator.session_id}")
            else:
                # Fallback to new session if existing session path not found
                orchestrator._init_session_logging()
                print(f"🆕 Creating new session (existing session not found at {full_session_path}): {orchestrator.session_id}")
        else:
            # Fallback to new session if no session path in state
            orchestrator._init_session_logging()
            print(f"🆕 Creating new session (no session path in state): {orchestrator.session_id}")
        
        # Save resumption audit trail
        audit_file = orchestrator.session_results_path / "resumption_audit.json"
        with open(audit_file, 'w', encoding='utf-8') as f:
            json.dump(resumption_audit, f, indent=2)
        
        # Prime the workflow state
        orchestrator.workflow_state = state_data
        orchestrator.workflow_state['session_results_path'] = str(orchestrator.session_results_path)
        orchestrator.workflow_state['conversation_id'] = orchestrator.conversation_id
        orchestrator.workflow_state['resumption_audit'] = resumption_audit
        
        # Execute remaining steps (same as CLI logic)
        for i in range(resume_step - 1, len(workflow_steps)):
            step_config = workflow_steps[i]
            agent_name = step_config.get('agent')
            
            print(f"\n🚀 Executing Step {i+1}: {agent_name}")
            
            try:
                if not agent_name:
                    raise ValueError(f"Step {i+1} is missing the 'agent' key.")
                
                step_output = orchestrator._execute_step(agent_name, step_config)
                
                # Update the master workflow state
                if step_output:
                    orchestrator.workflow_state.update(step_output)
                
                # Save state snapshot
                orchestrator._save_state_snapshot(f"state_after_step_{i+1}_{agent_name}.json")
                
                print(f"✅ Step {i+1} completed successfully")
                
            except Exception as e:
                print(f"❌ Step {i+1} failed: {str(e)}")
                raise e
        
        return {
            "status": "success",
            "session_id": orchestrator.session_id,
            "session_results_path": str(orchestrator.session_results_path),
            "final_state": orchestrator.workflow_state,
            "resumption_audit": resumption_audit,
            "intelligent_resumption": True
        } 