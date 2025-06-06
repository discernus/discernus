#!/usr/bin/env python3
"""
API Cost Management Utility - Updated for 2025 Models
Provides cost tracking, limits, and monitoring for OpenAI, Anthropic, Mistral, and Google AI APIs
"""

import json
import time
import os
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Optional, List, Tuple
from dataclasses import dataclass, asdict

@dataclass
class CostEntry:
    """Single cost entry"""
    timestamp: str
    provider: str
    model: str
    cost: float
    tokens_input: int
    tokens_output: int
    request_type: str
    
@dataclass
class CostLimits:
    """Cost limits configuration"""
    daily_limit: float = 10.0     # Increased default due to better pricing
    weekly_limit: float = 50.0    # Increased default due to better pricing
    monthly_limit: float = 200.0  # Increased default due to better pricing
    single_request_limit: float = 2.0  # Increased for advanced models

class CostManager:
    """Manages API costs across all providers - Updated for 2025"""
    
    def __init__(self, cost_file: str = "api_costs.json", limits_file: str = "cost_limits.json"):
        self.cost_file = Path(cost_file)
        self.limits_file = Path(limits_file)
        self.costs: List[CostEntry] = []
        self.limits = CostLimits()
        
        # Load existing data
        self._load_costs()
        self._load_limits()
        
        # Updated model costs for 2025 (per 1K tokens unless specified)
        self.model_costs = {
            "openai": {
                # 2025 GPT-4.1 series (April 2025) - 26-83% cost reduction
                "gpt-4.1": {"input": 0.005, "output": 0.015},
                "gpt-4.1-mini": {"input": 0.00015, "output": 0.0006},
                "gpt-4.1-nano": {"input": 0.0001, "output": 0.0004},
                
                # o-series reasoning models (2025) - Premium pricing for reasoning
                "o1": {"input": 0.015, "output": 0.06},
                "o3": {"input": 0.015, "output": 0.06},
                "o4-mini": {"input": 0.003, "output": 0.012},
                
                # GPT-4o series (current production)
                "gpt-4o": {"input": 0.005, "output": 0.015},
                "gpt-4o-mini": {"input": 0.00015, "output": 0.0006},
                
                # Legacy support
                "gpt-4": {"input": 0.03, "output": 0.06},
                "gpt-4-turbo": {"input": 0.01, "output": 0.03},
                "gpt-4-turbo-2024-04-09": {"input": 0.01, "output": 0.03},
                "gpt-3.5-turbo": {"input": 0.0005, "output": 0.0015}
            },
            "anthropic": {
                # Claude 4 series (May 2025)
                "claude-4-opus": {"input": 0.025, "output": 0.125},  # Premium model
                "claude-4-sonnet": {"input": 0.006, "output": 0.024},
                
                # Claude 3.7 with extended thinking (February 2025)
                "claude-3-7-sonnet": {"input": 0.004, "output": 0.018},
                "claude-3.7-sonnet": {"input": 0.004, "output": 0.018},
                
                # Latest Claude 3.5 series
                "claude-3.5-sonnet": {"input": 0.003, "output": 0.015},
                "claude-3.5-haiku": {"input": 0.00025, "output": 0.00125},
                "claude-3-5-sonnet-20241022": {"input": 0.003, "output": 0.015},
                "claude-3-5-haiku-20241022": {"input": 0.00025, "output": 0.00125},
                
                # Legacy support
                "claude-3-sonnet": {"input": 0.003, "output": 0.015},
                "claude-3-haiku": {"input": 0.00025, "output": 0.00125},
                "claude-3-opus": {"input": 0.015, "output": 0.075},
                "claude-3-sonnet-20240229": {"input": 0.003, "output": 0.015},
                "claude-3-haiku-20240307": {"input": 0.00025, "output": 0.00125}
            },
            "mistral": {
                # 2025 Models
                "mistral-medium-3": {"input": 0.02, "output": 0.06},      # May 2025 - frontier multimodal
                "codestral-2501": {"input": 0.012, "output": 0.036},      # January 2025 - coding
                "devstral-small-2505": {"input": 0.012, "output": 0.036}, # May 2025 - software engineering
                "mistral-saba-2502": {"input": 0.008, "output": 0.024},   # February 2025 - multilingual
                "mistral-ocr-2505": {"input": 0.02, "output": 0.0, "per_operation": 0.02},  # May 2025 - OCR service
                
                # Production models
                "mistral-large-2411": {"input": 0.008, "output": 0.024},
                "mistral-small-2409": {"input": 0.002, "output": 0.006},
                
                # Legacy support
                "mistral-large": {"input": 0.008, "output": 0.024},
                "mistral-large-latest": {"input": 0.008, "output": 0.024},
                "mistral-medium": {"input": 0.0025, "output": 0.0075},
                "mistral-medium-latest": {"input": 0.0025, "output": 0.0075},
                "mistral-small": {"input": 0.002, "output": 0.006},
                "mistral-small-latest": {"input": 0.002, "output": 0.006},
                "mistral-tiny": {"input": 0.0002, "output": 0.0006}
            },
            "google_ai": {
                # Gemini 2.5 series (2025) - Per 1K characters
                "gemini-2.5-pro": {"input": 0.002, "output": 0.008},      # June 2025 - most intelligent with Deep Think
                "gemini-2.5-flash": {"input": 0.001, "output": 0.004},    # May 2025 - adaptive thinking
                "gemini-2-5-pro-preview": {"input": 0.002, "output": 0.008},
                "gemini-2-5-flash-preview": {"input": 0.001, "output": 0.004},
                
                # Gemini 2.0 series (current production) - Per 1K characters
                "gemini-2.0-flash": {"input": 0.0008, "output": 0.003},
                "gemini-2.0-pro": {"input": 0.0008, "output": 0.003},
                "gemini-2-0-flash-exp": {"input": 0.0008, "output": 0.003},
                
                # Legacy support - Per 1K characters
                "gemini-1.5-flash": {"input": 0.0005, "output": 0.0015},
                "gemini-1.5-pro": {"input": 0.0005, "output": 0.0015},
                "gemini-pro": {"input": 0.0005, "output": 0.0015},
                "gemini-pro-vision": {"input": 0.0005, "output": 0.0015}
            }
        }
    
    def _load_costs(self):
        """Load cost history from file"""
        if self.cost_file.exists():
            try:
                with open(self.cost_file, 'r') as f:
                    data = json.load(f)
                    self.costs = [CostEntry(**entry) for entry in data]
            except Exception as e:
                print(f"⚠️ Could not load cost history: {e}")
                self.costs = []
        else:
            self.costs = []
    
    def _load_limits(self):
        """Load cost limits from file"""
        if self.limits_file.exists():
            try:
                with open(self.limits_file, 'r') as f:
                    data = json.load(f)
                    self.limits = CostLimits(**data)
            except Exception as e:
                print(f"⚠️ Could not load cost limits: {e}")
                self.limits = CostLimits()
    
    def _save_costs(self):
        """Save cost history to file"""
        try:
            with open(self.cost_file, 'w') as f:
                json.dump([asdict(cost) for cost in self.costs], f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save cost history: {e}")
    
    def _save_limits(self):
        """Save cost limits to file"""
        try:
            with open(self.limits_file, 'w') as f:
                json.dump(asdict(self.limits), f, indent=2)
        except Exception as e:
            print(f"⚠️ Could not save cost limits: {e}")
    
    def estimate_cost(self, text: str, provider: str, model: str) -> Tuple[float, int, int]:
        """Estimate cost for analyzing text - Updated for 2025 models"""
        # Rough token estimation (words * 1.3)
        words = len(text.split())
        input_tokens = int(words * 1.3)
        
        # Estimate output tokens based on model capabilities
        if any(x in model.lower() for x in ["4.1", "claude-4", "medium-3", "2.5"]):
            # Advanced models can provide more detailed analysis
            output_tokens = 500
        elif any(x in model.lower() for x in ["o1", "o3", "o4", "3.7", "reasoning"]):
            # Reasoning models provide deeper analysis
            output_tokens = 800
        elif any(x in model.lower() for x in ["codestral", "devstral"]):
            # Coding models may provide code examples
            output_tokens = 600
        else:
            # Standard analysis output
            output_tokens = 300
        
        # Get model costs
        if provider in self.model_costs and model in self.model_costs[provider]:
            costs = self.model_costs[provider][model]
            
            # Handle special pricing models
            if "per_operation" in costs:
                # OCR and other per-operation models
                cost = costs["per_operation"]
            elif provider == "google_ai":
                # Google AI uses character-based pricing
                input_chars = len(text)
                output_chars = output_tokens * 4  # Rough conversion
                cost = (input_chars * costs["input"] / 1000) + (output_chars * costs["output"] / 1000)
            else:
                # Standard token-based pricing
                cost = (input_tokens * costs["input"] / 1000) + (output_tokens * costs["output"] / 1000)
        else:
            # Default estimation if model not found - use reasonable fallback
            cost = (input_tokens * 0.005 / 1000) + (output_tokens * 0.015 / 1000)
        
        return round(cost, 7), input_tokens, output_tokens
    
    def check_limits_before_request(self, estimated_cost: float) -> Tuple[bool, str]:
        """Check if request would exceed limits"""
        
        # Check single request limit
        if estimated_cost > self.limits.single_request_limit:
            return False, f"Request cost ${estimated_cost:.4f} exceeds single request limit ${self.limits.single_request_limit:.2f}"
        
        # Calculate current spending
        now = datetime.now()
        daily_spent = self._get_spending_since(now - timedelta(days=1))
        weekly_spent = self._get_spending_since(now - timedelta(weeks=1))
        monthly_spent = self._get_spending_since(now - timedelta(days=30))
        
        # Check daily limit
        if daily_spent + estimated_cost > self.limits.daily_limit:
            return False, f"Would exceed daily limit: ${daily_spent + estimated_cost:.4f} > ${self.limits.daily_limit:.2f}"
        
        # Check weekly limit
        if weekly_spent + estimated_cost > self.limits.weekly_limit:
            return False, f"Would exceed weekly limit: ${weekly_spent + estimated_cost:.4f} > ${self.limits.weekly_limit:.2f}"
        
        # Check monthly limit
        if monthly_spent + estimated_cost > self.limits.monthly_limit:
            return False, f"Would exceed monthly limit: ${monthly_spent + estimated_cost:.4f} > ${self.limits.monthly_limit:.2f}"
        
        return True, "Within limits"
    
    def _get_spending_since(self, since_date: datetime) -> float:
        """Get total spending since a specific date"""
        total = 0.0
        for cost_entry in self.costs:
            entry_date = datetime.fromisoformat(cost_entry.timestamp)
            if entry_date >= since_date:
                total += cost_entry.cost
        return total
    
    def record_cost(self, provider: str, model: str, actual_cost: float, 
                   tokens_input: int, tokens_output: int, request_type: str = "analysis"):
        """Record actual cost after API call"""
        entry = CostEntry(
            timestamp=datetime.now().isoformat(),
            provider=provider,
            model=model,
            cost=actual_cost,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            request_type=request_type
        )
        
        self.costs.append(entry)
        self._save_costs()
        
        # Check if we're approaching limits
        self._check_and_warn_limits()
    
    def _check_and_warn_limits(self):
        """Check current spending against limits and warn if approaching"""
        now = datetime.now()
        daily_spent = self._get_spending_since(now - timedelta(days=1))
        weekly_spent = self._get_spending_since(now - timedelta(weeks=1))
        monthly_spent = self._get_spending_since(now - timedelta(days=30))
        
        # Warn if approaching limits (80% threshold)
        if daily_spent > self.limits.daily_limit * 0.8:
            print(f"⚠️ WARNING: Daily spending ${daily_spent:.2f} approaching limit ${self.limits.daily_limit:.2f}")
        
        if weekly_spent > self.limits.weekly_limit * 0.8:
            print(f"⚠️ WARNING: Weekly spending ${weekly_spent:.2f} approaching limit ${self.limits.weekly_limit:.2f}")
        
        if monthly_spent > self.limits.monthly_limit * 0.8:
            print(f"⚠️ WARNING: Monthly spending ${monthly_spent:.2f} approaching limit ${self.limits.monthly_limit:.2f}")
    
    def get_spending_summary(self) -> Dict:
        """Get summary of spending over different periods"""
        now = datetime.now()
        daily = self._get_spending_since(now - timedelta(days=1))
        weekly = self._get_spending_since(now - timedelta(weeks=1))
        monthly = self._get_spending_since(now - timedelta(days=30))
        
        return {
            "daily": daily,
            "weekly": weekly,
            "monthly": monthly,
            "usage_by_provider": self._get_usage_by_provider(),
            "usage_by_model": self._get_usage_by_model()
        }
    
    def _get_usage_by_provider(self) -> Dict:
        """Get total usage grouped by provider"""
        usage = {}
        for entry in self.costs:
            if entry.provider not in usage:
                usage[entry.provider] = {"cost": 0.0, "requests": 0}
            usage[entry.provider]["cost"] += entry.cost
            usage[entry.provider]["requests"] += 1
        return usage
    
    def _get_usage_by_model(self) -> Dict:
        """Get usage breakdown by model"""
        usage = {}
        for entry in self.costs:
            model_key = f"{entry.provider}_{entry.model}"
            if model_key not in usage:
                usage[model_key] = {"cost": 0.0, "requests": 0}
            usage[model_key]["cost"] += entry.cost
            usage[model_key]["requests"] += 1
        return usage
    
    def set_limits(self, daily: Optional[float] = None, weekly: Optional[float] = None, 
                  monthly: Optional[float] = None, single_request: Optional[float] = None):
        """Update cost limits"""
        if daily is not None:
            self.limits.daily_limit = daily
        if weekly is not None:
            self.limits.weekly_limit = weekly
        if monthly is not None:
            self.limits.monthly_limit = monthly
        if single_request is not None:
            self.limits.single_request_limit = single_request
        
        self._save_limits()
        print(f"✅ Cost limits updated:")
        print(f"  Daily: ${self.limits.daily_limit:.2f}")
        print(f"  Weekly: ${self.limits.weekly_limit:.2f}")
        print(f"  Monthly: ${self.limits.monthly_limit:.2f}")
        print(f"  Single Request: ${self.limits.single_request_limit:.2f}")
    
    def export_costs(self, filename: str = None):
        """Export cost data to CSV for analysis"""
        if filename is None:
            filename = f"cost_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        
        import csv
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['timestamp', 'provider', 'model', 'cost', 'tokens_input', 'tokens_output', 'request_type']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for entry in self.costs:
                writer.writerow(asdict(entry))
        
        print(f"📊 Cost data exported to: {filename}")
        return filename
    
    def get_model_info(self, provider: str, model: str) -> Dict[str, any]:
        """Get detailed information about a specific model"""
        if provider not in self.model_costs or model not in self.model_costs[provider]:
            return {"error": f"Model {model} not found for provider {provider}"}
        
        costs = self.model_costs[provider][model]
        
        # Categorize models by generation/capability
        model_info = {
            "provider": provider,
            "model": model,
            "pricing": costs,
            "generation": "unknown",
            "capabilities": [],
            "context_window": "unknown",
            "recommended_use": "general"
        }
        
        # OpenAI model categorization
        if provider == "openai":
            if "4.1" in model:
                model_info["generation"] = "2025"
                model_info["capabilities"] = ["1M+ context window", "improved coding", "cost reduction"]
                model_info["context_window"] = "1M+ tokens"
                model_info["recommended_use"] = "advanced analysis, long documents"
            elif model.startswith("o"):
                model_info["generation"] = "2025"
                model_info["capabilities"] = ["advanced reasoning", "step-by-step thinking"]
                model_info["recommended_use"] = "complex reasoning, problem solving"
            elif "4o" in model:
                model_info["generation"] = "2024"
                model_info["capabilities"] = ["multimodal", "fast", "cost-effective"]
                model_info["recommended_use"] = "general purpose, multimodal"
        
        # Anthropic model categorization
        elif provider == "anthropic":
            if "claude-4" in model:
                model_info["generation"] = "2025"
                model_info["capabilities"] = ["200K context", "enhanced reasoning", "multimodal"]
                model_info["context_window"] = "200K tokens"
                model_info["recommended_use"] = "advanced analysis, long documents"
            elif "3.7" in model:
                model_info["generation"] = "2025"
                model_info["capabilities"] = ["extended thinking", "reasoning transparency"]
                model_info["recommended_use"] = "complex reasoning with explanation"
            elif "3.5" in model or "3-5" in model:
                model_info["generation"] = "2024"
                model_info["capabilities"] = ["improved performance", "cost-effective"]
                model_info["recommended_use"] = "general purpose analysis"
        
        # Mistral model categorization
        elif provider == "mistral":
            if "medium-3" in model:
                model_info["generation"] = "2025"
                model_info["capabilities"] = ["frontier multimodal", "advanced reasoning"]
                model_info["recommended_use"] = "advanced multimodal analysis"
            elif "codestral" in model or "devstral" in model:
                model_info["generation"] = "2025"
                model_info["capabilities"] = ["code generation", "software engineering"]
                model_info["recommended_use"] = "coding, technical analysis"
            elif "saba" in model:
                model_info["generation"] = "2025"
                model_info["capabilities"] = ["multilingual", "Middle East/South Asia languages"]
                model_info["recommended_use"] = "multilingual analysis"
            elif "ocr" in model:
                model_info["generation"] = "2025"
                model_info["capabilities"] = ["OCR service", "document processing"]
                model_info["recommended_use"] = "document analysis, OCR"
        
        # Google AI model categorization
        elif provider == "google_ai":
            if "2.5" in model:
                model_info["generation"] = "2025"
                model_info["capabilities"] = ["Deep Think reasoning", "adaptive thinking budgets"]
                model_info["recommended_use"] = "complex reasoning with adaptive depth"
            elif "2.0" in model or "2-0" in model:
                model_info["generation"] = "2024"
                model_info["capabilities"] = ["next-generation features", "native audio"]
                model_info["recommended_use"] = "multimodal analysis"
        
        return model_info
    
    def get_cost_comparison(self, text: str, providers: List[str] = None) -> Dict[str, Dict]:
        """Compare costs across different models for the same text"""
        if providers is None:
            providers = list(self.model_costs.keys())
        
        comparison = {}
        
        for provider in providers:
            if provider not in self.model_costs:
                continue
                
            comparison[provider] = {}
            
            for model in self.model_costs[provider]:
                cost, input_tokens, output_tokens = self.estimate_cost(text, provider, model)
                model_info = self.get_model_info(provider, model)
                
                comparison[provider][model] = {
                    "estimated_cost": cost,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "generation": model_info.get("generation", "unknown"),
                    "capabilities": model_info.get("capabilities", []),
                    "recommended_use": model_info.get("recommended_use", "general")
                }
        
        return comparison
    
    def get_best_value_models(self, text: str, max_cost: float = None) -> List[Dict]:
        """Get recommendations for best value models based on cost and capabilities"""
        comparison = self.get_cost_comparison(text)
        recommendations = []
        
        for provider in comparison:
            for model, info in comparison[provider].items():
                if max_cost and info["estimated_cost"] > max_cost:
                    continue
                    
                # Calculate value score (capability vs cost)
                capability_score = 1
                if info["generation"] == "2025":
                    capability_score += 2
                elif info["generation"] == "2024":
                    capability_score += 1
                
                capability_score += len(info["capabilities"]) * 0.5
                
                # Value is capability divided by cost (higher is better)
                value_score = capability_score / max(info["estimated_cost"], 0.0001)
                
                recommendations.append({
                    "provider": provider,
                    "model": model,
                    "estimated_cost": info["estimated_cost"],
                    "generation": info["generation"],
                    "capabilities": info["capabilities"],
                    "value_score": value_score,
                    "recommended_use": info["recommended_use"]
                })
        
        # Sort by value score (descending)
        recommendations.sort(key=lambda x: x["value_score"], reverse=True)
        
        return recommendations[:10]  # Return top 10 recommendations
    
    def add_cost(self, provider: str, model: str, cost: float, 
                   tokens_input: int, tokens_output: int, request_type: str = "analysis"):
        """Add a new cost entry and save to file."""
        entry = CostEntry(
            timestamp=datetime.now().isoformat(),
            provider=provider,
            model=model,
            cost=cost,
            tokens_input=tokens_input,
            tokens_output=tokens_output,
            request_type=request_type
        )
        self.costs.append(entry)
        self._save_costs()
        self._check_and_warn_limits() 