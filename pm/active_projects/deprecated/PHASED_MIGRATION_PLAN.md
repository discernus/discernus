# Phased Migration Plan: Legacy Intelligence Integration

**Date**: July 24, 2025  
**Status**: Implementation Ready  
**Context**: Addressing Phase 3 orchestration reliability issues

---

## Executive Summary

This plan extracts critical orchestration intelligence from legacy agents to solve current reliability issues while preserving the Redis/MinIO/Gemini architecture. Focus is on **reliability engineering** rather than feature migration.

**Timeline**: 3 weeks to production-ready orchestration  
**Approach**: Selective intelligence extraction + infrastructure hardening  
**Risk**: Low - preserves existing architecture while adding reliability layers

---

## Phase A: Emergency Reliability (Week 1)

**Goal**: Stop the "blew up in flames" failures immediately

### A1: Model Health Pre-Flight Checks

**Extract from**: `ProjectCoherenceAnalyst._check_model_health()`

**Implementation**: Enhance `OrchestratorAgent/main.py`
```python
def validate_model_health(self, models):
    """Pre-flight model availability check"""
    for model in models:
        try:
            test_response = self.gateway.execute_call(
                model=model, 
                prompt="Health check - respond with 'OK'"
            )
            if not test_response or 'OK' not in test_response:
                return {'valid': False, 'failed_model': model}
        except Exception as e:
            return {'valid': False, 'failed_model': model, 'error': str(e)}
    return {'valid': True}
```

**Integration Point**: Add to `main()` before task creation
```python
# Before creating analysis tasks
health_check = self.validate_model_health(['gemini-2.5-flash'])
if not health_check['valid']:
    return {'status': 'terminated', 'reason': f"Model {health_check['failed_model']} unavailable"}
```

### A2: Resource Availability Validation  

**Extract from**: `ProjectCoherenceAnalyst._validate_project_structure()`

**Implementation**: Add corpus and artifact validation
```python
def validate_execution_resources(self, corpus_hashes, framework_hashes):
    """Validate all required resources are available"""
    missing_artifacts = []
    
    for hash_id in corpus_hashes + framework_hashes:
        if not self.artifact_storage.exists(hash_id):
            missing_artifacts.append(hash_id)
    
    if missing_artifacts:
        return {'valid': False, 'missing': missing_artifacts}
    return {'valid': True}
```

### A3: Graceful Error Handling

**Extract from**: `ProjectCoherenceAnalyst` exception patterns

**Implementation**: Wrap main orchestration logic
```python
def main(self):
    try:
        # Current orchestration logic
        result = self.execute_orchestration()
        return result
    except Exception as e:
        error_context = {
            'error': str(e),
            'phase': 'orchestration',
            'timestamp': datetime.now().isoformat()
        }
        print(f"Orchestration failed: {error_context}")
        return {'status': 'error', 'context': error_context}
```

**Validation Criteria for Phase A**:
- [ ] OrchestratorAgent successfully detects model unavailability
- [ ] Resource validation prevents execution with missing artifacts  
- [ ] Error handling provides clear failure context instead of crashes
- [ ] Phase 3 test completes without "blowing up in flames"

---

## Phase B: Quality Gates (Week 2)

**Goal**: Add mid-flight failure detection to prevent cascade failures

### B1: New QualityGateAgent (Minimal MethodologicalOverwatchAgent)

**File**: `agents/QualityGateAgent/main.py`
```python
class QualityGateAgent:
    def main(self):
        task = self.get_task_data()
        batch_results = self.load_batch_analysis_results(task['batch_result_hashes'])
        
        # Simple quality assessment
        assessment = self.assess_batch_quality(batch_results)
        
        if assessment['decision'] == 'TERMINATE':
            self.signal_pipeline_termination(assessment['reason'])
        
        return {'status': assessment['decision'], 'reason': assessment['reason']}
    
    def assess_batch_quality(self, results):
        """Simplified quality check"""
        if not results:
            return {'decision': 'TERMINATE', 'reason': 'No analysis results found'}
        
        # Check for systematic failures
        error_count = sum(1 for r in results if 'error' in str(r).lower())
        if error_count > len(results) * 0.5:  # >50% errors
            return {'decision': 'TERMINATE', 'reason': f'{error_count}/{len(results)} results contain errors'}
        
        return {'decision': 'PROCEED', 'reason': 'Results appear valid'}
```

### B2: Integration with OrchestratorAgent

**Enhancement**: Add quality gate task creation
```python
# After analysis tasks are created
quality_gate_task = {
    'task_type': 'quality_gate',
    'batch_result_hashes': analysis_task_hashes,
    'depends_on': analysis_task_ids
}
self.redis_client.xadd('task_stream', quality_gate_task)
```

### B3: Router Integration  

**Enhancement**: `scripts/router.py`
```python
# Add quality gate routing
elif task_type == 'quality_gate':
    return self.spawn_agent('QualityGateAgent', task_data)
```

**Validation Criteria for Phase B**:
- [ ] Quality gate detects systematic analysis failures
- [ ] Pipeline terminates early on quality failure instead of proceeding to synthesis
- [ ] Router correctly spawns QualityGateAgent containers
- [ ] Quality assessment provides actionable failure reasons

---

## Phase C: Advanced Resource Planning (Week 3)

**Goal**: Add sophisticated planning to prevent resource exhaustion

### C1: Enhanced PreTestAgent Resource Planning

**Extract from**: `ExecutionPlannerAgent.create_execution_plan()`

**Enhancement**: `agents/PreTestAgent/main.py`
```python
def estimate_execution_resources(self, corpus_size, framework_count):
    """Token and cost estimation"""
    # Rough token estimation (from ExecutionPlannerAgent patterns)
    estimated_tokens_per_doc = 1000  # Conservative estimate
    estimated_output_per_doc = 500   # From legacy patterns
    
    total_input_tokens = corpus_size * estimated_tokens_per_doc * framework_count
    total_output_tokens = corpus_size * estimated_output_per_doc * framework_count
    
    # Gemini 2.5 Flash pricing (from current patterns)
    input_cost = (total_input_tokens / 1_000_000) * 0.075  # Current rate
    output_cost = (total_output_tokens / 1_000_000) * 0.30  # Current rate
    
    return {
        'estimated_cost': input_cost + output_cost,
        'estimated_tokens': total_input_tokens + total_output_tokens,
        'recommended_batch_size': min(50, corpus_size)  # Conservative batching
    }
```

### C2: Cost-Aware Orchestration

**Enhancement**: `OrchestratorAgent/main.py`
```python
# Add cost validation before execution
def validate_execution_cost(self, resource_estimate):
    """Cost-aware execution gating"""
    max_cost_threshold = 10.0  # $10 maximum per experiment
    
    if resource_estimate['estimated_cost'] > max_cost_threshold:
        return {
            'approved': False, 
            'reason': f"Estimated cost ${resource_estimate['estimated_cost']:.2f} exceeds ${max_cost_threshold} limit"
        }
    
    return {'approved': True}
```

### C3: Supervisor Integration (Production Infrastructure)

**Implementation**: Replace `subprocess.Popen` in `scripts/router.py`
```python
# Instead of subprocess.Popen
import supervisor

class ProductionRouter:
    def spawn_agent(self, agent_name, task_data):
        """Production-grade agent spawning"""
        try:
            process_name = f"{agent_name}_{uuid.uuid4().hex[:8]}"
            supervisor_client = supervisor.xmlrpc.ServerProxy('http://localhost:9001/RPC2')
            
            # Start agent process via Supervisor
            result = supervisor_client.supervisor.startProcess(process_name)
            return {'status': 'spawned', 'process': process_name}
        except Exception as e:
            return {'status': 'failed', 'error': str(e)}
```

**Validation Criteria for Phase C**:
- [ ] Resource estimation prevents runaway costs
- [ ] Batch sizing recommendations optimize for model limits
- [ ] Supervisor manages agent processes reliably
- [ ] Cost validation gates prevent expensive failed experiments

---

## Integration Testing Plan

### Test Scenario 1: Model Failure Recovery
```bash
# Simulate model unavailability
# Expected: Orchestration detects and terminates gracefully
python3 -m pytest tests/test_model_health_validation.py
```

### Test Scenario 2: Quality Gate Termination  
```bash
# Feed corrupted analysis results
# Expected: Quality gate terminates before synthesis
python3 -m pytest tests/test_quality_gate_termination.py
```

### Test Scenario 3: Resource Validation
```bash
# Test with missing artifacts
# Expected: Pre-flight validation catches missing resources
python3 -m pytest tests/test_resource_validation.py
```

### Test Scenario 4: End-to-End Reliability
```bash
# Full Phase 3 test with reliability enhancements
python3 -m pytest tests/test_phase3_reliability.py
```

---

## Success Metrics

### Reliability Metrics
- **Graceful Failure Rate**: 100% of failures provide actionable error messages
- **Early Detection Rate**: >90% of systematic failures caught before synthesis
- **Resource Validation**: 100% of missing resource conditions detected pre-flight
- **Model Health**: 100% of model unavailability detected before task creation

### Performance Metrics  
- **Orchestration Overhead**: <5% additional latency from validation layers
- **Cost Accuracy**: Resource estimates within 20% of actual costs
- **Process Stability**: Supervisor eliminates agent process failures

### Process Metrics
- **Implementation Time**: 3 weeks from plan to production deployment
- **Architecture Compliance**: No violations of THIN principles
- **Integration Risk**: Zero breaking changes to existing Phase 1/2 functionality

---

## Rollback Plan

If migration introduces instability:

1. **Phase A Rollback**: Comment out validation calls in OrchestratorAgent
2. **Phase B Rollback**: Remove quality gate routing from router.py  
3. **Phase C Rollback**: Disable cost validation and revert to subprocess

Each phase is designed to be independently reversible without affecting core functionality.

---

## Next Actions

1. **User Approval**: Review and approve phased approach
2. **Phase A Start**: Begin model health and resource validation implementation
3. **Daily Standups**: Track progress and address integration issues
4. **Phase Gate Reviews**: Validate each phase before proceeding

**Expected Outcome**: Phase 3 orchestration reliability transforms from "blew up in flames" to production-ready stability within 3 weeks.