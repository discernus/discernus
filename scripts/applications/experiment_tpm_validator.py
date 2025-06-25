#!/usr/bin/env python3
"""
Experiment TPM Validation System
================================

Pre-flight TPM validation to prevent expensive experiment failures.
Analyzes corpus size, model TPM limits, and estimated runtime before experiments start.

Provides actionable suggestions when TPM limits will be exceeded.
"""

import os
import sys
import json
import yaml
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass
from datetime import timedelta
import tiktoken

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

@dataclass
class TPMValidationResult:
    """Results of TPM validation for an experiment"""
    
    # Overall validation status
    is_feasible: bool
    total_estimated_tokens: int
    estimated_duration_minutes: float
    estimated_cost: float
    
    # Per-model analysis
    model_analysis: Dict[str, Dict[str, Any]]
    
    # Recommendations
    recommendations: List[str]
    warnings: List[str]
    blocking_issues: List[str]
    
    # Alternative suggestions
    suggested_models: List[str]
    suggested_corpus_modifications: List[str]
    suggested_batching_strategy: Optional[Dict[str, Any]]

class ExperimentTPMValidator:
    """
    Comprehensive TPM validation for experiments before execution.
    
    Prevents expensive failures by analyzing:
    - Total token requirements vs TPM limits
    - Estimated experiment duration
    - Alternative model/corpus suggestions
    """
    
    def __init__(self):
        # Model TPM limits (conservative estimates for Tier 1/2)
        self.model_tpm_limits = {
            # OpenAI Models
            'gpt-4o': 30000,
            'gpt-4o-mini': 200000,
            'gpt-4': 10000,
            'gpt-4-turbo': 450000,
            'gpt-3.5-turbo': 200000,
            'o1-preview': 30000,
            'o1-mini': 100000,
            
            # Anthropic Models  
            'claude-3-5-sonnet-20241022': 40000,
            'claude-3-5-sonnet': 40000,
            'claude-3-5-haiku-20241022': 50000,
            'claude-3-5-haiku': 50000,
            'claude-3-opus-20240229': 20000,
            'claude-3-sonnet-20240229': 40000,
            
            # Mistral Models
            'mistral-large-latest': 30000,
            'mistral-medium-latest': 30000,
            'mistral-small-latest': 60000,
            'codestral-latest': 30000,
            
            # Google Models
            'gemini-1.5-pro': 32000,
            'gemini-1.5-flash': 100000,
            'gemini-2.0-flash': 100000,
            
            # Local Models (no TPM limits, but processing speed limits)
            'ollama/llama3.2': 999999,  # Local, no TPM limit
            'ollama/mistral': 999999,   # Local, no TPM limit
        }
        
        # Model cost estimates (per 1K tokens input/output average)
        self.model_costs = {
            'gpt-4o': 0.005,
            'gpt-4o-mini': 0.0002,
            'gpt-4': 0.03,
            'gpt-4-turbo': 0.01,
            'gpt-3.5-turbo': 0.001,
            'claude-3-5-sonnet-20241022': 0.003,
            'claude-3-5-haiku-20241022': 0.0008,
            'mistral-large-latest': 0.002,
            'mistral-small-latest': 0.0006,
            'gemini-1.5-pro': 0.00125,
            'gemini-1.5-flash': 0.0002,
            'ollama/llama3.2': 0.0,  # Local models are free
            'ollama/mistral': 0.0,
        }
        
        # Safety margins for TPM calculations
        self.safety_margin = 0.8  # Use 80% of limit to be conservative
        
        # Try to initialize tiktoken for accurate token counting
        try:
            self.encoding = tiktoken.encoding_for_model("gpt-4")
            self.tiktoken_available = True
        except Exception:
            self.tiktoken_available = False
            print("⚠️ tiktoken not available, using word-based estimation")
    
    def estimate_tokens(self, text: str) -> int:
        """Estimate token count for text"""
        if self.tiktoken_available:
            try:
                return len(self.encoding.encode(text))
            except Exception:
                pass
        
        # Fallback: word-based estimation (1.3 tokens per word)
        return int(len(text.split()) * 1.3)
    
    def load_corpus_content(self, corpus_spec: Dict[str, Any]) -> Tuple[str, int]:
        """
        Load corpus content and estimate total tokens
        Returns (combined_content, total_tokens)
        """
        file_path = corpus_spec.get('file_path') or corpus_spec.get('path')
        pattern = corpus_spec.get('pattern', '*.txt')
        
        if not file_path:
            raise ValueError("Corpus specification missing file_path or path")
        
        corpus_path = Path(file_path)
        if not corpus_path.exists():
            raise FileNotFoundError(f"Corpus path not found: {file_path}")
        
        all_content = []
        
        if corpus_path.is_file():
            # Single file
            with open(corpus_path, 'r', encoding='utf-8') as f:
                content = f.read()
                all_content.append(content)
        
        elif corpus_path.is_dir():
            # Directory with pattern
            txt_files = list(corpus_path.glob(pattern))
            if not txt_files:
                raise FileNotFoundError(f"No files found matching pattern '{pattern}' in {corpus_path}")
            
            for txt_file in sorted(txt_files):
                with open(txt_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    all_content.append(content)
        
        else:
            raise ValueError(f"Corpus path is neither file nor directory: {file_path}")
        
        # Combine all content
        combined_content = "\n\n".join(all_content)
        total_tokens = self.estimate_tokens(combined_content)
        
        return combined_content, total_tokens
    
    def load_framework_content(self, framework_spec: Dict[str, Any]) -> Tuple[str, int]:
        """
        Load framework content and estimate tokens for prompts
        Returns (framework_content, estimated_prompt_tokens)
        """
        framework_id = framework_spec.get('id') or framework_spec.get('name')
        file_path = framework_spec.get('file_path')
        
        if file_path:
            framework_path = Path(file_path)
        else:
            # Try standard framework location
            framework_path = project_root / 'asset_storage' / 'framework' / framework_id / f'{framework_id}.yaml'
            if not framework_path.exists():
                framework_path = project_root / 'asset_storage' / 'framework' / framework_id / f'{framework_id}.json'
        
        if not framework_path.exists():
            raise FileNotFoundError(f"Framework file not found: {framework_path}")
        
        # Load framework content
        with open(framework_path, 'r', encoding='utf-8') as f:
            if framework_path.suffix.lower() == '.yaml':
                framework_data = yaml.safe_load(f)
            else:
                framework_data = json.load(f)
        
        # Estimate prompt tokens (framework instructions + structure)
        framework_str = json.dumps(framework_data, indent=2)
        
        # Add typical prompt template overhead
        prompt_overhead = """
        You are analyzing text using the following framework. Please provide scores for each dimension.
        
        Framework:
        {framework_content}
        
        Text to analyze:
        {text_content}
        
        Please respond with JSON containing scores for each dimension.
        """
        
        estimated_prompt_content = prompt_overhead.format(
            framework_content=framework_str,
            text_content="[TEXT_PLACEHOLDER]"
        )
        
        estimated_prompt_tokens = self.estimate_tokens(estimated_prompt_content)
        
        return framework_str, estimated_prompt_tokens
    
    def get_model_tpm_limit(self, model_name: str) -> int:
        """Get TPM limit for model with pattern matching"""
        # Direct lookup
        if model_name in self.model_tpm_limits:
            return self.model_tpm_limits[model_name]
        
        # Pattern matching
        model_lower = model_name.lower()
        
        if 'gpt-4o-mini' in model_lower:
            return 200000
        elif 'gpt-4o' in model_lower:
            return 30000
        elif 'gpt-4' in model_lower and 'turbo' in model_lower:
            return 450000
        elif 'gpt-4' in model_lower:
            return 10000
        elif 'gpt-3.5' in model_lower:
            return 200000
        elif 'claude-3-5-sonnet' in model_lower or 'claude-3.5-sonnet' in model_lower:
            return 40000
        elif 'claude-3-5-haiku' in model_lower or 'claude-3.5-haiku' in model_lower:
            return 50000
        elif 'claude-3-opus' in model_lower:
            return 20000
        elif 'mistral-large' in model_lower:
            return 30000
        elif 'mistral-small' in model_lower:
            return 60000
        elif 'gemini-1.5-pro' in model_lower:
            return 32000
        elif 'gemini-1.5-flash' in model_lower or 'gemini-2.0-flash' in model_lower:
            return 100000
        elif 'ollama/' in model_lower:
            return 999999  # Local models have no TPM limits
        else:
            # Conservative default for unknown models
            return 10000
    
    def get_model_cost(self, model_name: str) -> float:
        """Get cost estimate per 1K tokens for model"""
        if model_name in self.model_costs:
            return self.model_costs[model_name]
        
        # Pattern matching for cost estimation
        model_lower = model_name.lower()
        
        if 'gpt-4' in model_lower:
            return 0.02  # Conservative estimate for GPT-4 variants
        elif 'gpt-3.5' in model_lower:
            return 0.001
        elif 'claude' in model_lower:
            return 0.002  # Conservative estimate
        elif 'mistral' in model_lower:
            return 0.001
        elif 'gemini' in model_lower:
            return 0.0005
        elif 'ollama/' in model_lower:
            return 0.0  # Local models are free
        else:
            return 0.01  # Conservative default
    
    def validate_experiment(self, experiment_file: Path) -> TPMValidationResult:
        """
        Comprehensive TPM validation for an experiment definition
        """
        print(f"🔍 TPM VALIDATION: {experiment_file.name}")
        print("=" * 60)
        
        # Load experiment definition
        with open(experiment_file, 'r', encoding='utf-8') as f:
            experiment = yaml.safe_load(f)
        
        components = experiment.get('components', {})
        
        # Extract experiment configuration
        frameworks = components.get('frameworks', components.get('framework', []))
        if not isinstance(frameworks, list):
            frameworks = [frameworks]
        
        models_config = components.get('models', [])
        if not models_config:
            raise ValueError("No models specified in experiment")
        
        corpus_config = components.get('corpus', {})
        if not corpus_config:
            raise ValueError("No corpus specified in experiment")
        
        # Handle corpus as list (take first one for validation)
        if isinstance(corpus_config, list):
            corpus_config = corpus_config[0] if corpus_config else {}
            if not corpus_config:
                raise ValueError("No corpus specified in experiment")
        
        # Analysis variables
        total_estimated_tokens = 0
        model_analysis = {}
        recommendations = []
        warnings = []
        blocking_issues = []
        estimated_cost = 0.0
        max_duration_minutes = 0.0
        
        try:
            # Load corpus and estimate tokens
            print("📊 Analyzing corpus...")
            corpus_content, corpus_tokens = self.load_corpus_content(corpus_config)
            print(f"   • Corpus tokens: {corpus_tokens:,}")
            
            # Load framework and estimate prompt tokens
            print("🗂️  Analyzing framework...")
            if frameworks:
                framework_content, prompt_tokens = self.load_framework_content(frameworks[0])
                print(f"   • Framework prompt tokens: {prompt_tokens:,}")
            else:
                prompt_tokens = 3000  # Default estimate
                warnings.append("No framework specified, using default prompt token estimate")
            
            # Calculate total tokens per analysis
            tokens_per_analysis = corpus_tokens + prompt_tokens
            print(f"   • Total tokens per analysis: {tokens_per_analysis:,}")
            
            # Analyze each model
            print("🤖 Analyzing models...")
            for model_config in models_config:
                model_name = model_config.get('name') or model_config.get('id', 'unknown')
                print(f"\n   🔍 Model: {model_name}")
                
                # Get model specifications
                tpm_limit = self.get_model_tpm_limit(model_name)
                safe_tpm_limit = int(tpm_limit * self.safety_margin)
                cost_per_1k = self.get_model_cost(model_name)
                
                print(f"      • TPM limit: {tpm_limit:,} (safe limit: {safe_tpm_limit:,})")
                
                # Calculate if this analysis fits within TPM limits
                can_handle_analysis = tokens_per_analysis <= safe_tpm_limit
                
                if can_handle_analysis:
                    # Calculate estimated duration for full corpus analysis
                    estimated_minutes = tokens_per_analysis / safe_tpm_limit * 60
                    model_cost = (tokens_per_analysis / 1000) * cost_per_1k
                    
                    print(f"      ✅ Can handle analysis: ~{estimated_minutes:.1f} minutes")
                    print(f"      💰 Estimated cost: ${model_cost:.4f}")
                    
                    model_analysis[model_name] = {
                        'feasible': True,
                        'tokens_required': tokens_per_analysis,
                        'tpm_limit': tpm_limit,
                        'safe_tpm_limit': safe_tpm_limit,
                        'estimated_duration_minutes': estimated_minutes,
                        'estimated_cost': model_cost,
                        'utilization_percent': (tokens_per_analysis / safe_tpm_limit) * 100
                    }
                    
                    max_duration_minutes = max(max_duration_minutes, estimated_minutes)
                    estimated_cost += model_cost
                    
                else:
                    # Analysis exceeds TPM limits
                    tokens_over_limit = tokens_per_analysis - safe_tpm_limit
                    
                    print(f"      ❌ EXCEEDS TPM LIMIT")
                    print(f"         Required: {tokens_per_analysis:,} tokens")
                    print(f"         Available: {safe_tpm_limit:,} tokens")
                    print(f"         Overflow: {tokens_over_limit:,} tokens")
                    
                    model_analysis[model_name] = {
                        'feasible': False,
                        'tokens_required': tokens_per_analysis,
                        'tpm_limit': tpm_limit,
                        'safe_tpm_limit': safe_tpm_limit,
                        'tokens_over_limit': tokens_over_limit,
                        'utilization_percent': (tokens_per_analysis / safe_tpm_limit) * 100
                    }
                    
                    blocking_issues.append(
                        f"Model {model_name} cannot handle analysis: "
                        f"{tokens_per_analysis:,} tokens required but only "
                        f"{safe_tpm_limit:,} available per minute"
                    )
            
            total_estimated_tokens = tokens_per_analysis * len(models_config)
            
        except Exception as e:
            blocking_issues.append(f"Failed to load experiment components: {e}")
            
            return TPMValidationResult(
                is_feasible=False,
                total_estimated_tokens=0,
                estimated_duration_minutes=0,
                estimated_cost=0,
                model_analysis={},
                recommendations=[],
                warnings=[],
                blocking_issues=blocking_issues,
                suggested_models=[],
                suggested_corpus_modifications=[],
                suggested_batching_strategy=None
            )
        
        # Generate recommendations and alternatives
        is_feasible = len(blocking_issues) == 0
        
        if not is_feasible:
            # Generate suggestions for blocked experiments
            suggestions = self._generate_alternatives(
                tokens_per_analysis, 
                corpus_tokens, 
                prompt_tokens,
                model_analysis
            )
            
            recommendations.extend(suggestions['recommendations'])
            suggested_models = suggestions['suggested_models']
            suggested_corpus_modifications = suggestions['corpus_modifications']
            suggested_batching_strategy = suggestions['batching_strategy']
        else:
            # Generate optimization suggestions for feasible experiments
            if max_duration_minutes > 60:
                recommendations.append(
                    f"Experiment will take ~{max_duration_minutes:.1f} minutes. "
                    "Consider using higher-TPM models for faster execution."
                )
            
            if estimated_cost > 5.0:
                recommendations.append(
                    f"Estimated cost is ${estimated_cost:.2f}. "
                    "Consider using more cost-effective models like gpt-3.5-turbo or claude-haiku."
                )
            
            suggested_models = []
            suggested_corpus_modifications = []
            suggested_batching_strategy = None
        
        return TPMValidationResult(
            is_feasible=is_feasible,
            total_estimated_tokens=total_estimated_tokens,
            estimated_duration_minutes=max_duration_minutes,
            estimated_cost=estimated_cost,
            model_analysis=model_analysis,
            recommendations=recommendations,
            warnings=warnings,
            blocking_issues=blocking_issues,
            suggested_models=suggested_models,
            suggested_corpus_modifications=suggested_corpus_modifications,
            suggested_batching_strategy=suggested_batching_strategy
        )
    
    def _generate_alternatives(self, tokens_per_analysis: int, corpus_tokens: int, 
                             prompt_tokens: int, model_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Generate alternative suggestions for blocked experiments"""
        
        recommendations = []
        suggested_models = []
        corpus_modifications = []
        batching_strategy = None
        
        # Find models that can handle the analysis
        viable_models = []
        for model_name, limit in self.model_tpm_limits.items():
            safe_limit = int(limit * self.safety_margin)
            if tokens_per_analysis <= safe_limit:
                cost_per_1k = self.get_model_cost(model_name)
                viable_models.append({
                    'name': model_name,
                    'tpm_limit': limit,
                    'cost_per_1k': cost_per_1k,
                    'estimated_cost': (tokens_per_analysis / 1000) * cost_per_1k
                })
        
        # Sort by cost (ascending)
        viable_models.sort(key=lambda x: x['estimated_cost'])
        
        if viable_models:
            recommendations.append("✅ SOLUTION 1: Switch to higher-TPM models")
            suggested_models = [model['name'] for model in viable_models[:5]]  # Top 5 options
        
        # Suggest corpus modifications
        if corpus_tokens > 15000:  # Large corpus
            # Calculate target size for most restrictive model
            blocked_models = [name for name, analysis in model_analysis.items() 
                            if not analysis.get('feasible', True)]
            
            if blocked_models:
                min_tpm = min(self.get_model_tpm_limit(model) for model in blocked_models)
                safe_min_tpm = int(min_tpm * self.safety_margin)
                max_corpus_tokens = safe_min_tpm - prompt_tokens
                
                if max_corpus_tokens > 1000:  # Reasonable minimum
                    recommendations.append("✅ SOLUTION 2: Reduce corpus size")
                    
                    # Calculate reduction percentage
                    reduction_percent = (1 - max_corpus_tokens / corpus_tokens) * 100
                    
                    corpus_modifications.extend([
                        f"Reduce corpus to ~{max_corpus_tokens:,} tokens ({reduction_percent:.0f}% reduction)",
                        "Use stratified sampling to maintain representativeness",
                        "Focus on key sections or representative excerpts",
                        "Consider splitting into multiple smaller experiments"
                    ])
        
        # Suggest batching strategy for very large corpora
        if corpus_tokens > 50000:
            recommendations.append("✅ SOLUTION 3: Implement text chunking")
            
            chunk_size = 10000  # Conservative chunk size
            num_chunks = (corpus_tokens + chunk_size - 1) // chunk_size
            
            batching_strategy = {
                'chunk_size_tokens': chunk_size,
                'estimated_chunks': num_chunks,
                'strategy': 'sliding_window',
                'overlap_tokens': 1000,
                'aggregation_method': 'weighted_average'
            }
        
        if not recommendations:
            recommendations.append(
                "❌ No simple solutions available. "
                "Consider using local models (ollama) or splitting into multiple experiments."
            )
        
        return {
            'recommendations': recommendations,
            'suggested_models': suggested_models,
            'corpus_modifications': corpus_modifications,
            'batching_strategy': batching_strategy
        }
    
    def print_validation_report(self, result: TPMValidationResult, experiment_file: Path):
        """Print a comprehensive validation report"""
        
        print(f"\n📋 TPM VALIDATION REPORT")
        print("=" * 60)
        print(f"Experiment: {experiment_file.name}")
        print(f"Status: {'✅ FEASIBLE' if result.is_feasible else '❌ BLOCKED'}")
        print(f"Total Estimated Tokens: {result.total_estimated_tokens:,}")
        print(f"Estimated Duration: {result.estimated_duration_minutes:.1f} minutes")
        print(f"Estimated Cost: ${result.estimated_cost:.4f}")
        
        # Model analysis
        print(f"\n🤖 MODEL ANALYSIS:")
        for model_name, analysis in result.model_analysis.items():
            status = "✅" if analysis['feasible'] else "❌"
            print(f"   {status} {model_name}")
            print(f"      Required: {analysis['tokens_required']:,} tokens")
            print(f"      TPM Limit: {analysis['tpm_limit']:,}")
            print(f"      Utilization: {analysis['utilization_percent']:.1f}%")
            
            if analysis['feasible']:
                print(f"      Duration: ~{analysis['estimated_duration_minutes']:.1f} minutes")
                print(f"      Cost: ${analysis['estimated_cost']:.4f}")
            else:
                print(f"      ❌ OVERFLOW: {analysis['tokens_over_limit']:,} tokens")
        
        # Blocking issues
        if result.blocking_issues:
            print(f"\n🚫 BLOCKING ISSUES:")
            for issue in result.blocking_issues:
                print(f"   • {issue}")
        
        # Warnings
        if result.warnings:
            print(f"\n⚠️  WARNINGS:")
            for warning in result.warnings:
                print(f"   • {warning}")
        
        # Recommendations
        if result.recommendations:
            print(f"\n💡 RECOMMENDATIONS:")
            for rec in result.recommendations:
                print(f"   • {rec}")
        
        # Suggested alternatives
        if result.suggested_models:
            print(f"\n🔄 SUGGESTED MODELS (by cost):")
            for model in result.suggested_models:
                cost = self.get_model_cost(model)
                tpm = self.get_model_tpm_limit(model)
                print(f"   • {model} (TPM: {tpm:,}, Cost: ${cost:.4f}/1K tokens)")
        
        if result.suggested_corpus_modifications:
            print(f"\n📝 CORPUS MODIFICATION OPTIONS:")
            for mod in result.suggested_corpus_modifications:
                print(f"   • {mod}")
        
        if result.suggested_batching_strategy:
            strategy = result.suggested_batching_strategy
            print(f"\n🔄 SUGGESTED BATCHING STRATEGY:")
            print(f"   • Chunk size: {strategy['chunk_size_tokens']:,} tokens")
            print(f"   • Estimated chunks: {strategy['estimated_chunks']}")
            print(f"   • Strategy: {strategy['strategy']}")
            print(f"   • Aggregation: {strategy['aggregation_method']}")

def main():
    """CLI interface for TPM validation"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Validate experiment TPM requirements")
    parser.add_argument("experiment_file", type=Path, help="Path to experiment YAML file")
    parser.add_argument("--json", action="store_true", help="Output results as JSON")
    
    args = parser.parse_args()
    
    if not args.experiment_file.exists():
        print(f"❌ Experiment file not found: {args.experiment_file}")
        sys.exit(1)
    
    # Run validation
    validator = ExperimentTPMValidator()
    result = validator.validate_experiment(args.experiment_file)
    
    if args.json:
        # JSON output for programmatic use
        output = {
            'is_feasible': result.is_feasible,
            'total_estimated_tokens': result.total_estimated_tokens,
            'estimated_duration_minutes': result.estimated_duration_minutes,
            'estimated_cost': result.estimated_cost,
            'model_analysis': result.model_analysis,
            'recommendations': result.recommendations,
            'warnings': result.warnings,
            'blocking_issues': result.blocking_issues,
            'suggested_models': result.suggested_models,
            'suggested_corpus_modifications': result.suggested_corpus_modifications,
            'suggested_batching_strategy': result.suggested_batching_strategy
        }
        print(json.dumps(output, indent=2))
    else:
        # Human-readable report
        validator.print_validation_report(result, args.experiment_file)
    
    # Exit with appropriate code
    sys.exit(0 if result.is_feasible else 1)

if __name__ == "__main__":
    main() 