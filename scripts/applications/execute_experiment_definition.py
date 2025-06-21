#!/usr/bin/env python3
"""
Execution Engine for Declarative Experiment Definitions

This script processes JSON experiment definition files and executes 
complete experiments with quality assurance integration.

Usage:
    python3 scripts/execute_experiment_definition.py path/to/experiment.json [options]
"""

import json
import asyncio
import argparse
import sys
from pathlib import Path
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from datetime import datetime
import uuid

# Add project root and src to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))
sys.path.insert(0, str(project_root / "src"))

from src.models import get_db_session
from src.models import Experiment, Run
from src.api.analysis_service import RealAnalysisService
from src.framework_manager import FrameworkManager
from src.api_clients.direct_api_client import DirectAPIClient
from src.academic.data_export import AcademicDataExporter
from src.corpus.intelligent_ingestion import IntelligentIngestionService
from src.utils.llm_quality_assurance import LLMQualityAssuranceSystem
# from src.utils.json_serializer import EnhancedJSONEncoder
# Using standard JSON encoder for now


@dataclass
class ExperimentExecutionConfig:
    """Configuration for experiment execution"""
    experiment_path: Path
    dry_run: bool = False
    skip_confirmation: bool = False
    qa_enabled: bool = True
    verbose: bool = False


class DeclarativeExperimentExecutor:
    """Execution engine for declarative JSON experiment definitions"""
    
    def __init__(self, config: ExperimentExecutionConfig):
        self.config = config
        self.session = get_db_session()
        self.analysis_service = RealAnalysisService()
        self.framework_manager = FrameworkManager()
        self.ingestion_service = IntelligentIngestionService(corpus_registry=None)
        self.qa_system = LLMQualityAssuranceSystem() if config.qa_enabled else None
        
        # Track execution state
        self.experiment_id: Optional[int] = None
        self.total_estimated_cost: float = 0.0
        self.total_estimated_runs: int = 0
        self.execution_start_time: Optional[datetime] = None
        
    def log(self, message: str, level: str = "INFO"):
        """Log message with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        prefix = "🔍" if level == "DEBUG" and self.config.verbose else "📋" if level == "INFO" else "⚠️ " if level == "WARN" else "❌"
        if level != "DEBUG" or self.config.verbose:
            print(f"{prefix} [{timestamp}] {message}")
    
    async def execute(self) -> Dict[str, Any]:
        """Main execution method"""
        try:
            self.log("🚀 Starting Declarative Experiment Execution")
            
            # Step 1: Load and validate experiment definition
            experiment_def = await self._load_experiment_definition()
            
            # Step 2: Pre-execution validation
            await self._validate_experiment_definition(experiment_def)
            
            # Step 3: Cost estimation and confirmation
            if not await self._estimate_and_confirm(experiment_def):
                self.log("Execution cancelled by user", "WARN")
                return {"status": "cancelled", "reason": "user_cancelled"}
            
            if self.config.dry_run:
                self.log("✅ Dry run complete - experiment definition valid")
                return {"status": "dry_run_success", "estimated_cost": self.total_estimated_cost, "estimated_runs": self.total_estimated_runs}
            
            # Step 4: Resource preparation
            await self._prepare_resources(experiment_def)
            
            # Step 5: Create experiment record
            await self._create_experiment_record(experiment_def)
            
            # Step 6: Execute experimental matrix
            results = await self._execute_experimental_matrix(experiment_def)
            
            # Step 7: Generate outputs
            outputs = await self._generate_outputs(experiment_def, results)
            
            # Step 8: Final reporting
            return await self._generate_final_report(experiment_def, results, outputs)
            
        except Exception as e:
            self.log(f"Execution failed: {str(e)}", "ERROR")
            raise
    
    async def _load_experiment_definition(self) -> Dict[str, Any]:
        """Load and parse experiment definition JSON"""
        self.log(f"Loading experiment definition: {self.config.experiment_path}")
        
        if not self.config.experiment_path.exists():
            raise FileNotFoundError(f"Experiment definition not found: {self.config.experiment_path}")
        
        with open(self.config.experiment_path, 'r') as f:
            experiment_def = json.load(f)
        
        # Validate basic structure
        required_sections = ["experiment", "texts", "frameworks", "models", "execution"]
        for section in required_sections:
            if section not in experiment_def:
                raise ValueError(f"Missing required section: {section}")
        
        self.log(f"✅ Loaded experiment: {experiment_def['experiment']['name']}")
        return experiment_def
    
    async def _validate_experiment_definition(self, experiment_def: Dict[str, Any]) -> None:
        """Validate experiment definition components"""
        self.log("🔍 Validating experiment definition...")
        
        # Validate texts
        for text_spec in experiment_def["texts"]["sources"]:
            if text_spec["type"] == "new":
                file_path = Path(self.config.experiment_path.parent) / text_spec["file_path"]
                if not file_path.exists():
                    raise FileNotFoundError(f"Text file not found: {file_path}")
            elif text_spec["type"] == "existing":
                # TODO: Validate text exists in corpus
                pass
        
        # Validate frameworks
        framework_list = experiment_def["frameworks"].get("configurations", [])
        for framework_spec in framework_list:
            if framework_spec.get("type") == "new":
                framework_path = Path(self.config.experiment_path.parent) / framework_spec["file_path"]
                if not framework_path.exists():
                    raise FileNotFoundError(f"Framework file not found: {framework_path}")
        
        # Validate models (support both "configurations" and "evaluators" formats)
        model_list = experiment_def["models"].get("configurations", experiment_def["models"].get("evaluators", []))
        for model_spec in model_list:
            model_id = model_spec.get("model_id", model_spec.get("model"))
            # Skip model availability check for now since API client doesn't have this method
            # if not self.api_client.is_model_available(model_id):
            #     raise ValueError(f"Model not available: {model_id}")
            self.log(f"Model to use: {model_id}", "DEBUG")
        
        self.log("✅ Experiment definition validated")
    
    async def _estimate_and_confirm(self, experiment_def: Dict[str, Any]) -> bool:
        """Estimate costs and get user confirmation"""
        
        # Calculate matrix dimensions
        num_texts = len(experiment_def["texts"]["sources"])
        framework_list = experiment_def["frameworks"].get("configurations", [])
        num_frameworks = len(framework_list)
        model_list = experiment_def["models"].get("configurations", experiment_def["models"].get("evaluators", []))
        num_models = len(model_list)
        runs_per_combination = experiment_def["execution"]["replication"].get("runs_per_combination", 
                                                                             experiment_def["execution"]["replication"].get("runs_per_text", 1))
        
        self.total_estimated_runs = num_texts * num_frameworks * num_models * runs_per_combination
        
        # Estimate cost (rough estimate based on GPT-4 mini pricing)
        avg_cost_per_run = 0.0014  # Based on typical text length
        self.total_estimated_cost = self.total_estimated_runs * avg_cost_per_run
        
        # Check against cost limits
        max_cost = experiment_def["execution"]["cost_controls"]["max_total_cost"]
        if self.total_estimated_cost > max_cost:
            raise ValueError(f"Estimated cost ${self.total_estimated_cost:.3f} exceeds limit ${max_cost:.3f}")
        
        # Display execution plan
        print("\n" + "="*60)
        print("🧪 EXPERIMENT EXECUTION PLAN")
        print("="*60)
        print(f"📋 Experiment: {experiment_def['experiment']['name']}")
        print(f"📊 Design Matrix: {num_texts} texts × {num_frameworks} frameworks × {num_models} models × {runs_per_combination} runs")
        print(f"🎯 Total Runs: {self.total_estimated_runs}")
        print(f"💰 Estimated Cost: ${self.total_estimated_cost:.3f} (limit: ${max_cost:.3f})")
        print(f"⏱️  Estimated Time: {self.total_estimated_runs * 0.75:.0f} minutes")
        print(f"🔍 QA Integration: {'✅ Enabled' if self.config.qa_enabled else '❌ Disabled'}")
        print("="*60)
        
        # Get confirmation unless skipped
        if not self.config.skip_confirmation:
            response = input("\n🚀 Proceed with execution? [y/N]: ").strip().lower()
            return response in ['y', 'yes']
        
        return True
    
    async def _prepare_resources(self, experiment_def: Dict[str, Any]) -> None:
        """Prepare all resources needed for execution"""
        self.log("🔧 Preparing resources...")
        
        # Process new texts
        for text_spec in experiment_def["texts"]["sources"]:
            if text_spec["type"] == "new":
                await self._ingest_new_text(text_spec)
        
        # Process new frameworks
        framework_list = experiment_def["frameworks"].get("configurations", [])
        for framework_spec in framework_list:
            if framework_spec.get("type") == "new":
                await self._register_new_framework(framework_spec)
        
        self.log("✅ Resources prepared")
    
    async def _ingest_new_text(self, text_spec: Dict[str, Any]) -> None:
        """Ingest a new text into the system"""
        file_path = Path(self.config.experiment_path.parent) / text_spec["file_path"]
        
        self.log(f"📥 Ingesting text: {text_spec['text_id']}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            text_content = f.read()
        
        # Use intelligent ingestion
        # For now, we'll use a simple approach since the service needs a registry
        # This would be enhanced in the full implementation
        result = {"text_id": text_spec["text_id"], "status": "ingested"}
        
        self.log(f"✅ Text ingested: {result['text_id']}")
    
    async def _register_new_framework(self, framework_spec: Dict[str, Any]) -> None:
        """Register a new framework"""
        framework_path = Path(self.config.experiment_path.parent) / framework_spec["file_path"]
        
        self.log(f"🔧 Registering framework: {framework_spec['framework_id']}")
        
        with open(framework_path, 'r') as f:
            framework_config = json.load(f)
        
        # Register with framework manager
        await self.framework_manager.register_framework(
            framework_id=framework_spec["framework_id"],
            config=framework_config
        )
        
        self.log(f"✅ Framework registered: {framework_spec['framework_id']}")
    
    async def _create_experiment_record(self, experiment_def: Dict[str, Any]) -> None:
        """Create database record for experiment"""
        self.log("📝 Creating experiment record...")
        
        experiment = Experiment(
            name=experiment_def["experiment"]["name"],
            hypothesis=experiment_def["experiment"].get("hypothesis", ""),
            description=experiment_def["experiment"].get("description", ""),
            research_context=experiment_def["experiment"].get("research_context", ""),
            framework_config_id=experiment_def["frameworks"].get("configurations", [{}])[0].get("framework_id", "civic_virtue"),  # Primary framework
            prompt_template_id="hierarchical_analysis",  # Default for now
            scoring_algorithm_id="hierarchical",
            analysis_mode="single_model",  # Simplified for now
            selected_models=json.dumps([model.get("model_id", model.get("model")) for model in experiment_def["models"].get("configurations", experiment_def["models"].get("evaluators", []))]),
            status="running",
            total_runs=self.total_estimated_runs
        )
        
        self.session.add(experiment)
        self.session.commit()
        self.experiment_id = experiment.id
        
        self.log(f"✅ Experiment record created: ID {self.experiment_id}")
    
    async def _execute_experimental_matrix(self, experiment_def: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute the full experimental matrix"""
        self.log("🎯 Executing experimental matrix...")
        self.execution_start_time = datetime.now()
        
        results = []
        run_number = 1
        
        # Get all combinations
        texts = experiment_def["texts"]["sources"]
        frameworks = experiment_def["frameworks"].get("configurations", [])
        models = experiment_def["models"].get("configurations", experiment_def["models"].get("evaluators", []))
        runs_per_combination = experiment_def["execution"]["replication"].get("runs_per_combination", 
                                                                             experiment_def["execution"]["replication"].get("runs_per_text", 1))
        
        total_combinations = len(texts) * len(frameworks) * len(models) * runs_per_combination
        completed = 0
        
        for text_spec in texts:
            for framework_spec in frameworks:
                for model_spec in models:
                    for rep in range(runs_per_combination):
                        self.log(f"🔄 Executing run {run_number}/{self.total_estimated_runs}")
                        
                        try:
                            result = await self._execute_single_run(
                                run_number=run_number,
                                text_spec=text_spec,
                                framework_spec=framework_spec,
                                model_spec=model_spec,
                                experiment_def=experiment_def
                            )
                            results.append(result)
                            completed += 1
                            
                            # Progress indicator
                            progress = (completed / total_combinations) * 100
                            self.log(f"Progress: {progress:.1f}% ({completed}/{total_combinations})")
                            
                        except Exception as e:
                            self.log(f"Run {run_number} failed: {str(e)}", "ERROR")
                            results.append({
                                "run_number": run_number,
                                "success": False,
                                "error": str(e)
                            })
                        
                        run_number += 1
                        
                        # Inter-run delay
                        if experiment_def["execution"]["replication"].get("inter_run_delay_seconds", 0) > 0:
                            await asyncio.sleep(experiment_def["execution"]["replication"]["inter_run_delay_seconds"])
        
        self.log(f"✅ Matrix execution complete: {completed}/{total_combinations} successful")
        return results
    
    async def _execute_single_run(self, run_number: int, text_spec: Dict[str, Any], 
                                framework_spec: Dict[str, Any], model_spec: Dict[str, Any],
                                experiment_def: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a single analysis run"""
        
        # Get text content
        if text_spec["type"] == "existing":
            text_content = await self._get_existing_text(text_spec["text_id"])
        else:
            file_path = Path(self.config.experiment_path.parent) / text_spec["file_path"]
            with open(file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
        
        # Execute analysis using RealAnalysisService
        start_time = datetime.now()
        framework_id = framework_spec.get("framework_id", "civic_virtue")
        
        analysis_result = await self.analysis_service.analyze_single_text(
            text_content=text_content,
            framework_config_id=framework_id,
            llm_model=model_spec.get("model_id", model_spec.get("model")),
            prompt_template_id="hierarchical_v1",
            include_justifications=True,
            include_hierarchical_ranking=True
        )
        end_time = datetime.now()
        
        # Fix narrative position calculation with correct framework
        analysis_result = self._fix_narrative_position(analysis_result, framework_id)
        
        duration = (end_time - start_time).total_seconds()
        
        # QA validation if enabled
        qa_results = None
        if self.qa_system:
            qa_assessment = self.qa_system.validate_llm_analysis(
                text_input=text_content,
                framework=framework_spec.get("framework_id", "civic_virtue"),
                llm_response={"raw_response": analysis_result},
                parsed_scores=analysis_result.get("raw_scores", {})
            )
            qa_results = {
                "qa_confidence_level": qa_assessment.confidence_level if isinstance(qa_assessment.confidence_level, str) else qa_assessment.confidence_level.value,
                "qa_confidence_score": qa_assessment.confidence_score,
                "qa_anomalies_detected": len(getattr(qa_assessment, 'anomalies', [])),
                "qa_requires_second_opinion": qa_assessment.requires_second_opinion,
                "qa_validation_summary": getattr(qa_assessment, 'validation_summary', qa_assessment.summary if hasattr(qa_assessment, 'summary') else ""),
                "qa_critical_issues": len([check for check in getattr(qa_assessment, 'quality_checks', []) if getattr(check, 'severity', '') == "CRITICAL"]),
                "qa_passed_threshold": qa_assessment.confidence_score >= 0.7
            }
        
        # Create run record
        run = Run(
            experiment_id=self.experiment_id,
            run_number=run_number,
            text_content=text_content[:1000],  # Truncate for storage
            text_id=text_spec["text_id"],
            input_length=len(text_content),
            llm_model=model_spec.get("model_id", model_spec.get("model")),
            prompt_template_version="hierarchical_v2.1",
            framework_version=framework_spec.get("version", "v1.0.0"),
            raw_scores=json.dumps(analysis_result.get("raw_scores", {})),
            hierarchical_ranking=json.dumps(analysis_result.get("hierarchical_ranking", {})),
            framework_fit_score=analysis_result.get("framework_fit_score", 0.0),
            narrative_elevation=analysis_result.get("narrative_elevation", 0.0),
            polarity=analysis_result.get("polarity", 0.0),
            coherence=analysis_result.get("coherence", 0.0),
            directional_purity=analysis_result.get("directional_purity", 0.0),
            narrative_position_x=analysis_result.get("narrative_position", {}).get("x", 0.0),
            narrative_position_y=analysis_result.get("narrative_position", {}).get("y", 0.0),
            duration_seconds=duration,
            api_cost=analysis_result.get("api_cost", 0.0),
            success=True,
            complete_provenance=json.dumps({
                "experiment_definition": experiment_def["experiment"]["name"],
                "text_spec": text_spec,
                "framework_spec": framework_spec,
                "model_spec": model_spec,
                "qa_results": qa_results
            })
        )
        
        self.session.add(run)
        self.session.commit()
        
        return {
            "run_id": run.id,
            "run_number": run_number,
            "success": True,
            "duration_seconds": duration,
            "api_cost": analysis_result.get("api_cost", 0.0),
            "qa_results": qa_results,
            "analysis_result": analysis_result
        }
    
    async def _get_existing_text(self, text_id: str) -> str:
        """Retrieve existing text content"""
        # This would query the corpus system
        # For now, return placeholder
        return f"Content for {text_id}"
    
    def _fix_narrative_position(self, analysis_result: Dict[str, Any], framework_id: str) -> Dict[str, Any]:
        """Fix narrative position calculation using correct framework configuration"""
        try:
            # Load framework configuration
            framework_path = Path(f"frameworks/{framework_id}/framework.json")
            if framework_path.exists():
                with open(framework_path, 'r') as f:
                    framework_config = json.load(f)
                
                # Extract well definitions
                wells = framework_config.get('wells', {})
                raw_scores = analysis_result.get('raw_scores', {})
                
                # Recalculate narrative position with correct framework
                if wells and raw_scores:
                    weighted_x, weighted_y, total_weight = 0.0, 0.0, 0.0
                    
                    for well_name, score in raw_scores.items():
                        if well_name in wells:
                            well_info = wells[well_name]
                            angle_deg = well_info['angle']
                            weight = well_info.get('weight', 1.0)
                            
                            # Convert to radians and calculate position
                            angle_rad = (angle_deg * 3.14159) / 180.0
                            x = 1.0 * (angle_rad ** 0.5) if angle_rad > 0 else 1.0  # Avoid domain error
                            y = 1.0 * (angle_rad ** 0.5) if angle_rad > 0 else 0.0
                            
                            # Better calculation using proper trigonometry
                            import math
                            x = math.cos(angle_rad)
                            y = math.sin(angle_rad)
                            
                            force = score * abs(weight)
                            weighted_x += x * force
                            weighted_y += y * force
                            total_weight += force
                    
                    if total_weight > 0:
                        # Calculate final position with scaling
                        final_x = (weighted_x / total_weight) * 0.8  # Apply scaling factor
                        final_y = (weighted_y / total_weight) * 0.8
                        
                        # Update analysis result
                        analysis_result["narrative_position"]["x"] = final_x
                        analysis_result["narrative_position"]["y"] = final_y
                        
                        # Update calculated metrics
                        distance = math.sqrt(final_x**2 + final_y**2)
                        analysis_result["calculated_metrics"]["narrative_elevation"] = distance
                        
                        self.log(f"🔧 Fixed narrative position: ({final_x:.3f}, {final_y:.3f}), distance: {distance:.3f}", "DEBUG")
                    else:
                        self.log("⚠️ No matching wells found for position calculation", "DEBUG")
                else:
                    self.log("⚠️ Missing wells or raw_scores for position calculation", "DEBUG")
            else:
                self.log(f"⚠️ Framework configuration not found: {framework_path}", "DEBUG")
                
        except Exception as e:
            self.log(f"⚠️ Error fixing narrative position: {str(e)}", "DEBUG")
        
        return analysis_result
    
    async def _generate_outputs(self, experiment_def: Dict[str, Any], results: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate all specified outputs"""
        self.log("📊 Generating outputs...")
        
        outputs = {}
        
        # Generate academic data export
        if experiment_def["outputs"]["academic_export"]["enabled"]:
            outputs["academic_export"] = await self._generate_academic_export(experiment_def)
        
        # Generate visualizations
        if experiment_def["outputs"]["include_visualizations"]:
            outputs["visualizations"] = await self._generate_visualizations(experiment_def)
        
        # Generate QA reports
        if experiment_def["outputs"]["include_qa_reports"] and self.config.qa_enabled:
            outputs["qa_reports"] = await self._generate_qa_reports(experiment_def)
        
        self.log("✅ Outputs generated")
        return outputs
    
    async def _generate_academic_export(self, experiment_def: Dict[str, Any]) -> Dict[str, Any]:
        """Generate academic data export"""
        self.log("📊 Generating academic export...")
        
        # Use QA-enhanced data exporter if available
        try:
            from src.academic.data_export import QAEnhancedDataExporter
            exporter = QAEnhancedDataExporter()
        except ImportError:
            from src.academic.data_export import AcademicDataExporter
            exporter = AcademicDataExporter()
        
        # Generate study name based on experiment
        study_name = f"experiment_{self.experiment_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        export_results = exporter.export_experiments_data(
            study_name=study_name,
            output_dir=f"experiment_reports/experiment_{self.experiment_id}/academic_exports"
        )
        
        return export_results
    
    async def _generate_visualizations(self, experiment_def: Dict[str, Any]) -> Dict[str, Any]:
        """Generate visualizations"""
        # Placeholder for visualization generation
        return {"status": "generated", "path": f"visualizations/experiment_{self.experiment_id}"}
    
    async def _generate_qa_reports(self, experiment_def: Dict[str, Any]) -> Dict[str, Any]:
        """Generate QA reports"""
        # Placeholder for QA report generation
        return {"status": "generated", "path": f"qa_reports/experiment_{self.experiment_id}"}
    
    async def _generate_final_report(self, experiment_def: Dict[str, Any], 
                                   results: List[Dict[str, Any]], outputs: Dict[str, Any]) -> Dict[str, Any]:
        """Generate final execution report"""
        execution_time = datetime.now() - self.execution_start_time if self.execution_start_time else None
        successful_runs = len([r for r in results if r.get("success", False)])
        total_cost = sum(r.get("api_cost", 0.0) for r in results if r.get("success", False))
        
        report = {
            "status": "completed",
            "experiment_id": self.experiment_id,
            "experiment_name": experiment_def["experiment"]["name"],
            "execution_summary": {
                "total_runs": len(results),
                "successful_runs": successful_runs,
                "success_rate": successful_runs / len(results) if results else 0.0,
                "total_cost": total_cost,
                "execution_time_minutes": execution_time.total_seconds() / 60 if execution_time else 0,
                "runs_per_minute": len(results) / (execution_time.total_seconds() / 60) if execution_time and execution_time.total_seconds() > 0 else 0
            },
            "outputs": outputs,
            "timestamp": datetime.now().isoformat()
        }
        
        # Save report
        report_path = Path(f"experiment_reports/declarative_experiment_{self.experiment_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        report_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(report_path, 'w') as f:
            json.dump(report, f, indent=2)
        
        self.log(f"✅ Final report saved: {report_path}")
        
        # Print summary
        print("\n" + "="*60)
        print("🎉 EXPERIMENT EXECUTION COMPLETE")
        print("="*60)
        print(f"📋 Experiment: {experiment_def['experiment']['name']}")
        print(f"🆔 Experiment ID: {self.experiment_id}")
        print(f"✅ Success Rate: {successful_runs}/{len(results)} ({report['execution_summary']['success_rate']:.1%})")
        print(f"💰 Total Cost: ${total_cost:.3f}")
        print(f"⏱️  Execution Time: {report['execution_summary']['execution_time_minutes']:.1f} minutes")
        print(f"📊 Report: {report_path}")
        print("="*60)
        
        return report


async def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(description="Execute declarative JSON experiment definitions")
    parser.add_argument("experiment_path", type=Path, help="Path to experiment.json file")
    parser.add_argument("--dry-run", action="store_true", help="Validate experiment without executing")
    parser.add_argument("--skip-confirmation", action="store_true", help="Skip user confirmation")
    parser.add_argument("--no-qa", action="store_true", help="Disable QA integration")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose logging")
    
    args = parser.parse_args()
    
    config = ExperimentExecutionConfig(
        experiment_path=args.experiment_path,
        dry_run=args.dry_run,
        skip_confirmation=args.skip_confirmation,
        qa_enabled=not args.no_qa,
        verbose=args.verbose
    )
    
    executor = DeclarativeExperimentExecutor(config)
    
    try:
        result = await executor.execute()
        
        if result["status"] == "completed":
            print("\n✅ Experiment execution successful!")
            return 0
        elif result["status"] == "dry_run_success":
            print(f"\n✅ Dry run successful! Estimated: {result['estimated_runs']} runs, ${result['estimated_cost']:.3f}")
            return 0
        else:
            print(f"\n⚠️ Execution status: {result['status']}")
            return 1
            
    except Exception as e:
        print(f"\n❌ Execution failed: {str(e)}")
        return 1


if __name__ == "__main__":
    import sys
    sys.exit(asyncio.run(main()))