# LiteLLM Integration Plan for Discernus

**Document Version**: v1.0.0  
**Created**: 2025-06-25  
**Author**: Claude & Jeff  
**Status**: Planning Phase  
**Priority**: High (Critical for scaling multi-LLM experiments)

## 🎯 Executive Summary

LiteLLM integration will replace Discernus's custom `DirectAPIClient` with a production-grade LLM gateway that provides unified API management, intelligent rate limiting, automatic load balancing, and robust fallback handling across 100+ LLM providers.

**Core Benefits**: Eliminates rate limiting bottlenecks, reduces maintenance burden, enables massive scale experiments, and provides production-grade reliability.

## 🚨 Problems LiteLLM Solves

### **Current Architecture Limitations**

1. **Rate Limiting Catastrophe**: Multi-LLM experiments hit provider limits simultaneously
2. **Manual Provider Management**: 4 custom provider classes with duplicated logic
3. **No Load Balancing**: Cannot distribute load across multiple deployments
4. **Complex Failover Logic**: Custom retry handlers are maintenance-heavy
5. **Model Mapping Hell**: Manual model name mappings across providers
6. **Cost Tracking Inconsistency**: Different cost calculation per provider

### **Real-World Impact**
- ❌ $252 comprehensive experiment **failed due to rate limits**
- ❌ Manual provider management **increases development friction**
- ❌ No horizontal scaling across **multiple API keys/deployments**
- ❌ Custom retry logic **requires constant maintenance**

## 💡 LiteLLM Solution Architecture

### **Unified Gateway Approach**
```
┌─────────────────────────────────────────────────────────────┐
│                    Discernus System                         │
├─────────────────────────────────────────────────────────────┤
│  Analysis Service                                           │
│    ↓                                                        │
│  LiteLLM Router/Gateway                                     │
│    ├── Rate Limiting & Queue Management                     │
│    ├── Load Balancing (Multiple Deployments)               │
│    ├── Automatic Fallback & Retry Logic                    │
│    ├── Cost Tracking & Budget Controls                     │
│    └── Model Name Resolution                               │
│         ↓                                                   │
│  Provider APIs (OpenAI, Anthropic, Mistral, Google AI)     │
└─────────────────────────────────────────────────────────────┘
```

### **Key Features**
- **Unified Interface**: Single API for all providers
- **Smart Rate Limiting**: Per-provider TPM/RPM limits with queuing
- **Load Balancing**: Multiple routing strategies (latency, cost, usage-based)
- **Automatic Fallbacks**: Provider failover with circuit breakers
- **Cost Controls**: Budget limits and spend tracking
- **Model Resolution**: Automatic model name mapping

## 🔧 Technical Implementation

### **Phase 1: LiteLLM SDK Integration**

**1. Install LiteLLM**
```bash
pip install litellm
```

**2. Create LiteLLM Configuration**
```yaml
# litellm_config.yaml
model_list:
  # OpenAI Deployments
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY
      rpm: 3500  # Requests per minute
      tpm: 150000  # Tokens per minute
  
  - model_name: gpt-4o-mini
    litellm_params:
      model: openai/gpt-4o-mini
      api_key: os.environ/OPENAI_API_KEY
      rpm: 5000
      tpm: 200000
  
  # Anthropic Deployments
  - model_name: claude-3.5-sonnet
    litellm_params:
      model: anthropic/claude-3-5-sonnet-20241022
      api_key: os.environ/ANTHROPIC_API_KEY
      rpm: 4000
      tpm: 400000
  
  - model_name: claude-3.5-haiku
    litellm_params:
      model: anthropic/claude-3-5-haiku-20241022
      api_key: os.environ/ANTHROPIC_API_KEY
      rpm: 4000
      tpm: 400000
  
  # Mistral Deployments
  - model_name: mistral-large
    litellm_params:
      model: mistral/mistral-large-latest
      api_key: os.environ/MISTRAL_API_KEY
      rpm: 1000
      tpm: 30000
  
  # Google AI Deployments
  - model_name: gemini-2.5-flash
    litellm_params:
      model: vertex_ai/gemini-2.5-flash
      vertex_project: os.environ/GOOGLE_CLOUD_PROJECT
      vertex_location: us-central1
      rpm: 2000
      tpm: 32000

router_settings:
  routing_strategy: usage-based-routing-v2  # Smart load balancing
  redis_host: localhost  # For usage tracking
  redis_port: 6379
  enable_pre_call_check: true  # Rate limit checking
  
cost_controls:
  max_budget: 500.0  # Monthly budget limit
  budget_duration: 30d
```

**3. Replace DirectAPIClient**
```python
# src/api_clients/litellm_client.py
import litellm
from litellm import Router
from typing import Dict, Tuple, Any, Optional
import os
import yaml
from pathlib import Path

class LiteLLMClient:
    """LiteLLM-powered client for Discernus analysis"""
    
    def __init__(self, config_path: Optional[str] = None):
        """Initialize LiteLLM router with Discernus configuration"""
        
        # Load configuration
        if not config_path:
            config_path = Path(__file__).parent.parent.parent / "litellm_config.yaml"
        
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        
        # Initialize router with configuration
        self.router = Router(
            model_list=config['model_list'],
            **config.get('router_settings', {})
        )
        
        # Set up cost tracking
        litellm.success_callback = ["langfuse"]  # Optional: observability
        
    def analyze_text(self, text: str, framework: str, model_name: str) -> Tuple[Dict[str, Any], float]:
        """
        Analyze text using LiteLLM router
        
        Args:
            text: Text to analyze
            framework: Framework specification (YAML)
            model_name: Model to use (will route automatically)
            
        Returns:
            Tuple of (analysis_result, cost)
        """
        # Build prompt (reuse existing template logic)
        prompt = self._build_analysis_prompt(text, framework)
        
        # Make API call through LiteLLM
        response = self.router.completion(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=2000
        )
        
        # Extract content and cost
        content = response.choices[0].message.content
        cost = response._hidden_params.get('response_cost', 0.0)
        
        # Parse response (reuse existing parsing logic)
        analysis_result = self._parse_response(content, text, framework)
        
        return analysis_result, cost
    
    def test_connections(self) -> Dict[str, bool]:
        """Test all configured providers"""
        results = {}
        
        # Test each model group
        test_models = ['gpt-4o-mini', 'claude-3.5-haiku', 'mistral-large', 'gemini-2.5-flash']
        
        for model in test_models:
            try:
                response = self.router.completion(
                    model=model,
                    messages=[{"role": "user", "content": "Hello"}],
                    max_tokens=5
                )
                provider = self._get_provider_from_model(model)
                results[provider] = True
                print(f"✅ {provider} connection successful")
            except Exception as e:
                provider = self._get_provider_from_model(model)
                results[provider] = False
                print(f"❌ {provider} connection failed: {e}")
        
        return results
    
    def get_available_models(self) -> Dict[str, list]:
        """Get available models by provider"""
        # Extract from router configuration
        models_by_provider = {}
        
        for model_config in self.router.model_list:
            provider = self._get_provider_from_model(model_config['model_name'])
            if provider not in models_by_provider:
                models_by_provider[provider] = []
            models_by_provider[provider].append(model_config['model_name'])
        
        return models_by_provider
    
    def _build_analysis_prompt(self, text: str, framework: str) -> str:
        """Build analysis prompt (reuse existing logic)"""
        # Import and use existing template manager
        from src.prompts.template_manager import TemplateManager
        template_manager = TemplateManager()
        return template_manager.build_analysis_prompt(text, framework)
    
    def _parse_response(self, content: str, text: str, framework: str) -> Dict[str, Any]:
        """Parse LLM response (reuse existing logic)"""
        # Import and use existing parsing logic from DirectAPIClient
        from src.api_clients.direct_api_client import DirectAPIClient
        dummy_client = DirectAPIClient()
        return dummy_client._parse_response(content, text, framework)
    
    def _get_provider_from_model(self, model_name: str) -> str:
        """Get provider name from model name"""
        if any(x in model_name.lower() for x in ["gpt", "openai"]):
            return "openai"
        elif any(x in model_name.lower() for x in ["claude", "anthropic"]):
            return "anthropic"
        elif any(x in model_name.lower() for x in ["mistral"]):
            return "mistral"
        elif any(x in model_name.lower() for x in ["gemini", "google"]):
            return "google_ai"
        else:
            return "unknown"
```

**4. Update Analysis Service**
```python
# src/api/analysis_service.py (modifications)

# Replace DirectAPIClient import
# from src.api_clients.direct_api_client import DirectAPIClient
from src.api_clients.litellm_client import LiteLLMClient

class AnalysisService:
    def __init__(self):
        # Replace DirectAPIClient with LiteLLMClient
        # self.api_client = DirectAPIClient()
        self.api_client = LiteLLMClient()
        
        # Rest of initialization remains the same
        # ...
    
    # analyze_text method remains the same - interface is compatible!
```

### **Phase 2: Advanced Features**

**1. Multiple API Key Load Balancing**
```yaml
# Multiple deployments for high-throughput
model_list:
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY_1
      rpm: 3500
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY_2
      rpm: 3500
  - model_name: gpt-4o
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY_3
      rpm: 3500
```

**2. Cost-Based Routing**
```yaml
router_settings:
  routing_strategy: cost-based-routing  # Route to cheapest model
```

**3. Redis-Based Usage Tracking**
```bash
# Start Redis for production usage tracking
docker run -d --name redis -p 6379:6379 redis:latest
```

**4. Budget Controls**
```python
# Automatic budget enforcement
router = Router(
    model_list=model_list,
    max_budget=500.0,  # $500 monthly limit
    budget_duration="30d"
)
```

### **Phase 3: LiteLLM Proxy Server (Optional)**

For even more advanced features, deploy LiteLLM as a standalone proxy:

```bash
# Start LiteLLM proxy server
litellm --config litellm_config.yaml --port 4000

# Use proxy in Discernus
export LITELLM_PROXY_URL="http://localhost:4000"
```

## 📊 Implementation Timeline

### **Week 1: Core Integration**
- [ ] Install LiteLLM and dependencies
- [ ] Create `litellm_config.yaml` configuration
- [ ] Implement `LiteLLMClient` class
- [ ] Update `AnalysisService` to use LiteLLM
- [ ] Test with single-model experiments

### **Week 2: Multi-Provider Setup**
- [ ] Configure all 4 providers (OpenAI, Anthropic, Mistral, Google AI)
- [ ] Set up rate limits and cost controls
- [ ] Test provider failover and load balancing
- [ ] Run comprehensive multi-LLM experiment successfully

### **Week 3: Production Hardening**
- [ ] Set up Redis for usage tracking
- [ ] Configure multiple API keys per provider
- [ ] Implement budget controls and alerting
- [ ] Performance testing and optimization

### **Week 4: Advanced Features**
- [ ] Evaluate LiteLLM Proxy Server
- [ ] Set up observability (Langfuse integration)
- [ ] Implement custom routing strategies if needed
- [ ] Documentation and team training

## 🎯 Success Metrics

### **Immediate (Week 1-2)**
- ✅ Zero rate limiting errors in multi-LLM experiments
- ✅ Unified API interface across all 4 providers
- ✅ Successful $252 comprehensive experiment execution

### **Medium-term (Week 3-4)**
- ✅ 50%+ reduction in API management code
- ✅ Automatic load balancing across multiple API keys
- ✅ Cost tracking accuracy within 5%

### **Long-term (Month 2+)**
- ✅ Ability to run 10x larger experiments without infrastructure issues
- ✅ Seamless addition of new LLM providers
- ✅ Production-grade reliability (99.9% uptime)

## 🔍 Migration Strategy

### **Backward Compatibility**
```python
# Maintain existing interface for seamless migration
class LiteLLMClient:
    def analyze_text(self, text: str, framework: str, model_name: str) -> Tuple[Dict[str, Any], float]:
        # Same signature as DirectAPIClient - no breaking changes!
        pass
```

### **Gradual Rollout**
1. **Phase A**: LiteLLM for new experiments only
2. **Phase B**: Migrate existing experiment orchestrator
3. **Phase C**: Deprecate DirectAPIClient completely

### **Rollback Plan**
- Keep `DirectAPIClient` as fallback during transition
- Feature flag to switch between implementations
- Comprehensive testing before full migration

## 💰 Cost Impact Analysis

### **Infrastructure Costs**
- **Redis**: ~$10-20/month for usage tracking
- **Additional API Keys**: ~$0 (just for load balancing)
- **LiteLLM License**: $0 (open source)

### **Development Savings**
- **Reduced Maintenance**: -40 hours/month (no custom provider management)
- **Faster Iterations**: -20 hours/month (unified interface)
- **Better Reliability**: -10 hours/month (fewer debugging sessions)

**Total Monthly Savings**: ~$4,500 in developer time

## 🚨 Risk Assessment

### **High Risk**
- **Provider API Changes**: LiteLLM handles model updates automatically ✅
- **Rate Limiting Edge Cases**: LiteLLM has battle-tested rate limiting ✅

### **Medium Risk**
- **Learning Curve**: 2-3 days to understand LiteLLM configuration ⚠️
- **Redis Dependency**: Adds infrastructure dependency ⚠️

### **Low Risk**
- **Performance Overhead**: Minimal (lightweight router) ✅
- **Migration Complexity**: Same interface, gradual rollout ✅

## 🎓 Next Steps

1. **Install LiteLLM**: `pip install litellm`
2. **Create Configuration**: Set up `litellm_config.yaml`
3. **Build `LiteLLMClient`**: Replace `DirectAPIClient`
4. **Test with Small Experiment**: Validate rate limiting
5. **Run Full Comprehensive Study**: Execute $252 experiment successfully

**Priority**: This should be implemented **before** running any more large-scale multi-LLM experiments. The rate limiting issues will only get worse as we scale up.

---

**Conclusion**: LiteLLM integration is a **strategic upgrade** that transforms Discernus from a custom-built API management system to a production-grade, scalable LLM platform. The investment pays for itself within the first month through reduced maintenance and successful large-scale experiments.

## 🚨 TPM-Aware Rate Limiting Solution

### **The Real Bottleneck: Token Throughput**

LiteLLM solves **Request Per Minute (RPM)** limits but **Token Per Minute (TPM)** limits are the actual constraint for large-scale narrative analysis experiments.

**Problem**: Each MFT analysis consumes ~5,000-15,000+ tokens:
- Framework specification: ~2,000-3,000 tokens
- Political speech text: ~2,000-8,000+ tokens  
- Analysis instructions: ~1,000-2,000 tokens

**Reality**: Your comprehensive experiment needs 350K-1.8M+ tokens across 14 runs.

### **TPM-Aware LiteLLM Configuration**

```yaml
# Enhanced model configuration with TPM optimization
model_list:
  # High-TPM models for bulk processing
  - model_name: gpt-3.5-turbo-bulk
    litellm_params:
      model: openai/gpt-3.5-turbo
      api_key: os.environ/OPENAI_API_KEY
      rpm: 500
      tpm: 200000  # 🎯 20x higher than GPT-4
      max_tokens: 4000
      
  - model_name: claude-haiku-bulk
    litellm_params:
      model: anthropic/claude-3-5-haiku-20241022
      api_key: os.environ/ANTHROPIC_API_KEY
      rpm: 50
      itpm: 50000   # 🎯 Higher throughput than Sonnet
      otpm: 10000
      
  # Flagship models for quality validation
  - model_name: gpt-4o-quality
    litellm_params:
      model: openai/gpt-4o
      api_key: os.environ/OPENAI_API_KEY
      rpm: 500
      tpm: 30000
      max_tokens: 4000
      
  - model_name: claude-sonnet-quality
    litellm_params:
      model: anthropic/claude-3-5-sonnet-20241022
      api_key: os.environ/ANTHROPIC_API_KEY
      rpm: 50
      itpm: 40000
      otpm: 8000

router_settings:
  routing_strategy: tpm-aware-routing  # New strategy
  enable_pre_call_check: true
  tpm_budget_management: true
  
  # TPM-specific controls
  max_tokens_per_minute: 50000  # Global TPM limit
  token_usage_window: 60        # Seconds
  queue_on_tpm_limit: true      # Queue requests when TPM exceeded
```

### **Enhanced LiteLLMClient with TPM Logic**

```python
# src/api_clients/litellm_client.py (enhanced)
import litellm
from litellm import Router
import tiktoken
from typing import Dict, Tuple, Any, Optional, List
import time
import asyncio

class TPMAwareLiteLLMClient:
    """LiteLLM client with Token-Per-Minute awareness"""
    
    def __init__(self, config_path: Optional[str] = None):
        # Initialize base LiteLLM router
        self.router = Router(model_list=config['model_list'], **config.get('router_settings', {}))
        
        # TPM tracking
        self.tpm_tracker = {}
        self.token_window = 60  # seconds
        
    def estimate_tokens(self, text: str, model: str = "gpt-4") -> int:
        """Estimate token count for text"""
        try:
            encoding = tiktoken.encoding_for_model(model.replace("openai/", ""))
            return len(encoding.encode(text))
        except:
            # Fallback estimation
            return len(text.split()) * 1.3
    
    def check_tpm_availability(self, model: str, estimated_tokens: int) -> bool:
        """Check if model can handle estimated tokens within TPM limit"""
        current_time = time.time()
        
        # Clean old entries (outside window)
        if model in self.tpm_tracker:
            self.tpm_tracker[model] = [
                (timestamp, tokens) for timestamp, tokens in self.tpm_tracker[model]
                if current_time - timestamp < self.token_window
            ]
        else:
            self.tpm_tracker[model] = []
        
        # Calculate current TPM usage
        current_tpm = sum(tokens for _, tokens in self.tpm_tracker[model])
        model_tpm_limit = self._get_model_tpm_limit(model)
        
        return current_tpm + estimated_tokens <= model_tpm_limit
    
    def analyze_text_with_tpm_control(self, text: str, framework: str, model_name: str) -> Tuple[Dict[str, Any], float]:
        """Analyze text with TPM-aware scheduling"""
        
        # Build prompt and estimate tokens
        prompt = self._build_analysis_prompt(text, framework)
        estimated_tokens = self.estimate_tokens(prompt, model_name)
        
        # Check TPM availability
        if not self.check_tpm_availability(model_name, estimated_tokens):
            print(f"⏳ TPM limit reached for {model_name}, waiting...")
            time.sleep(10)  # Wait and retry
            return self.analyze_text_with_tpm_control(text, framework, model_name)
        
        # Make API call
        response = self.router.completion(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.1,
            max_tokens=2000
        )
        
        # Track token usage
        self._track_tpm_usage(model_name, estimated_tokens)
        
        # Extract results
        content = response.choices[0].message.content
        cost = response._hidden_params.get('response_cost', 0.0)
        analysis_result = self._parse_response(content, text, framework)
        
        return analysis_result, cost
    
    def batch_analyze_texts(self, texts: List[str], framework: str, model_name: str, max_batch_tokens: int = 15000) -> List[Tuple[Dict[str, Any], float]]:
        """Batch multiple texts into single API calls to maximize TPM efficiency"""
        
        # Group texts into TPM-efficient batches
        batches = self._create_token_aware_batches(texts, framework, max_batch_tokens)
        
        results = []
        for batch in batches:
            batch_prompt = self._build_batch_analysis_prompt(batch, framework)
            
            # Single API call for entire batch
            response = self.router.completion(
                model=model_name,
                messages=[{"role": "user", "content": batch_prompt}],
                temperature=0.1,
                max_tokens=4000
            )
            
            # Parse batch results
            batch_results = self._parse_batch_response(response.choices[0].message.content, batch, framework)
            results.extend(batch_results)
            
            # Track TPM usage for entire batch
            batch_tokens = self.estimate_tokens(batch_prompt, model_name)
            self._track_tpm_usage(model_name, batch_tokens)
        
        return results
    
    def _create_token_aware_batches(self, texts: List[str], framework: str, max_tokens: int) -> List[List[str]]:
        """Group texts into batches that fit within token limits"""
        batches = []
        current_batch = []
        current_tokens = 0
        
        # Estimate framework overhead
        framework_tokens = self.estimate_tokens(framework)
        batch_overhead = 500  # Prompt instructions, formatting
        
        for text in texts:
            text_tokens = self.estimate_tokens(text)
            batch_tokens = framework_tokens + batch_overhead + sum(self.estimate_tokens(t) for t in current_batch) + text_tokens
            
            if batch_tokens > max_tokens and current_batch:
                # Start new batch
                batches.append(current_batch)
                current_batch = [text]
            else:
                current_batch.append(text)
        
        if current_batch:
            batches.append(current_batch)
        
        return batches
    
    def _build_batch_analysis_prompt(self, texts: List[str], framework: str) -> str:
        """Build prompt for analyzing multiple texts in one call"""
        texts_section = "\n\n".join([f"TEXT {i+1}:\n{text}" for i, text in enumerate(texts)])
        
        return f"""
        Analyze the following {len(texts)} texts using the Moral Foundations Theory framework.
        Return results as a JSON array with one analysis object per text, in the same order.

        FRAMEWORK:
        {framework}

        TEXTS TO ANALYZE:
        {texts_section}

        Return format: [analysis1, analysis2, analysis3, ...]
        Each analysis should follow the standard MFT scoring format.
        """
    
    def _get_model_tpm_limit(self, model: str) -> int:
        """Get TPM limit for model"""
        tpm_limits = {
            "gpt-3.5-turbo": 200000,
            "gpt-4o": 30000,
            "gpt-4": 10000,
            "claude-3-5-sonnet-20241022": 40000,
            "claude-3-5-haiku-20241022": 50000,
            "mistral-large-latest": 30000
        }
        return tpm_limits.get(model, 10000)  # Conservative default
```

### **Experiment Validation with TPM Pre-Flight Checks**

```python
# Enhanced experiment orchestrator with TPM validation
class TPMAwareExperimentOrchestrator:
    """Experiment orchestrator with Token-Per-Minute awareness"""
    
    def validate_experiment_feasibility(self, experiment_config: dict) -> Dict[str, Any]:
        """Validate experiment against TPM constraints before execution"""
        
        validation_results = {
            "feasible": True,
            "total_estimated_tokens": 0,
            "estimated_duration_minutes": 0,
            "model_utilization": {},
            "recommendations": []
        }
        
        for run in experiment_config["execution"]["matrix"]:
            model = run["model"]
            corpus = run["corpus_subset"]
            
            # Estimate tokens for this run
            corpus_tokens = self._estimate_corpus_tokens(corpus)
            framework_tokens = self._estimate_framework_tokens(run["framework"])
            total_tokens = corpus_tokens + framework_tokens
            
            validation_results["total_estimated_tokens"] += total_tokens
            
            # Calculate duration for this model
            model_tpm = self._get_model_tpm_limit(model)
            run_duration = total_tokens / model_tpm  # minutes
            
            validation_results["model_utilization"][model] = validation_results["model_utilization"].get(model, 0) + run_duration
            validation_results["estimated_duration_minutes"] = max(validation_results["estimated_duration_minutes"], run_duration)
        
        # Generate recommendations
        if validation_results["estimated_duration_minutes"] > 120:  # 2+ hours
            validation_results["recommendations"].append("Consider using higher-TPM models like gpt-3.5-turbo")
            
        if validation_results["total_estimated_tokens"] > 500000:  # 500k+ tokens
            validation_results["recommendations"].append("Consider implementing text batching to improve TPM efficiency")
            
        for model, duration in validation_results["model_utilization"].items():
            if duration > 180:  # 3+ hours for single model
                validation_results["recommendations"].append(f"Model {model} will take {duration:.1f} minutes - consider load balancing")
        
        return validation_results
    
    def run_tpm_optimized_experiment(self, experiment_config: dict):
        """Run experiment with TPM optimization strategies"""
        
        # Pre-flight validation
        validation = self.validate_experiment_feasibility(experiment_config)
        print(f"🔍 Experiment validation:")
        print(f"  Total estimated tokens: {validation['total_estimated_tokens']:,}")
        print(f"  Estimated duration: {validation['estimated_duration_minutes']:.1f} minutes")
        
        if validation["recommendations"]:
            print("  Recommendations:")
            for rec in validation["recommendations"]:
                print(f"    - {rec}")
        
        # Execute with TPM awareness
        for run in experiment_config["execution"]["matrix"]:
            print(f"\n🚀 Starting run: {run['run_id']}")
            
            # Check if we should use batching
            if self._should_use_batching(run):
                print("  📦 Using text batching for TPM efficiency")
                self._execute_batched_run(run)
            else:
                print("  📄 Using individual text analysis")
                self._execute_standard_run(run)
```

**Summary**: This enhanced approach combines LiteLLM's request management with intelligent TPM awareness, text batching, and pre-flight validation to handle the token throughput constraints that are the real bottleneck in large-scale experiments. 