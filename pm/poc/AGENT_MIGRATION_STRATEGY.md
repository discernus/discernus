# Agent Migration Strategy: Production to PoC Integration

**Date**: July 23, 2025  
**Status**: Technical Planning Document  
**Context**: Reconciling production agent capabilities with PoC THIN architecture

---

## Executive Summary

This document outlines the technical strategy for migrating production Discernus agents to the PoC's Redis Streams + MinIO architecture. Analysis shows that production agents are more THIN-compatible than initially apparent, enabling a viable integration path that preserves sophisticated analytical capabilities while eliminating orchestration brittleness.

## Background: The Reconciliation Challenge

### Production System Problems
- **Catastrophic failures**: 4,000-file submission incident demonstrates orchestration layer dangers
- **Brittleness**: Every new framework/experiment breaks due to THICK parsing
- **Performance issues**: No parallelization despite LLM capabilities
- **THICK code drift**: Cursor consistently writes parsing code despite THIN principles
- **Security risks**: Runaway execution due to complex orchestration logic

### PoC Architecture Strengths
- **Security**: Thin router with explicit task types prevents runaway execution
- **Extensibility**: External prompts + agent registry eliminate parsing brittleness
- **Performance**: Redis Streams enable natural parallelization
- **THIN compliance**: Forces minimal orchestration logic, prevents THICK drift

### The Technical Question
Can sophisticated production agents (ForensicQAAgent, CalculationAgent, etc.) be adapted to the PoC's stateless, Redis-based task model without losing their analytical capabilities?

## Agent Compatibility Analysis

### Production Agent Inventory
From `agent_registry.yaml`, the production system includes:

1. **AnalysisAgent** - Primary framework application with provenance
2. **ForensicQAAgent** - Content integrity validation via LLM intelligence
3. **CalculationAgent** - Deterministic mathematical calculations
4. **DataExtractionAgent** - LLM-to-LLM JSON extraction with retry logic
5. **SynthesisAgent** - Academic report generation
6. **ProjectCoherenceAnalyst** - Holistic project validation
7. **MethodologicalOverwatchAgent** - Quality control checkpoints
8. **EnsembleConfigurationAgent** - Model health assessment
9. **StatisticalAnalysisConfigurationAgent** - Statistical plan generation
10. **ExecutionPlannerAgent** - Cost/time estimation
11. **ExperimentConclusionAgent** - Final audit generation

### THIN Compatibility Assessment

**Key Finding**: Production agents are already architected with THIN principles:

- **ForensicQAAgent**: Uses LLM intelligence for validation, not hardcoded rules
- **CalculationAgent**: Declarative formula execution from framework specs
- **Most agents**: External prompt templates with minimal orchestration logic

## Migration Strategy: Three Agent Archetypes

### Type 1: LLM-Driven Agents (Easy Port)
**Agents**: ForensicQAAgent, AnalysisAgent, SynthesisAgent, ProjectCoherenceAnalyst

**Current Architecture**:
```python
# Production pattern
def validate_content_integrity(self, corpus_file_path, corpus_text, llm_response):
    validation_prompt = f"""You are a forensic validation expert...
    ACTUAL CORPUS TEXT: {corpus_text}
    LLM RESPONSE: {llm_response}
    ..."""
    validation_response = self.gateway.execute_call(model, validation_prompt)
```

**PoC Adaptation Pattern**:
```python
# agents/ForensicQAAgent/main.py
class ForensicQAAgent:
    def process_task(self, task_id: str):
        task_data = self._get_redis_task(task_id)
        corpus_text = get_artifact(task_data['corpus_hash']).decode('utf-8')
        llm_response = get_artifact(task_data['analysis_result_hash']).decode('utf-8')
        
        # Use external prompt template
        prompt_text = self.prompt_template.format(
            corpus_text=corpus_text,
            llm_response=llm_response
        )
        
        validation_result = completion(model="gemini-2.5-flash", 
                                     messages=[{"role": "user", "content": prompt_text}])
        result_hash = put_artifact(validation_result.encode('utf-8'))
        self._signal_completion(task_id, result_hash)
```

```yaml
# agents/ForensicQAAgent/prompt.yaml
template: |
  You are a forensic validation expert. Your job is to detect if an LLM hallucinated text content.

  ACTUAL CORPUS TEXT:
  {corpus_text}

  LLM RESPONSE CLAIMING TO ANALYZE THIS TEXT:
  {llm_response}

  VALIDATION TASK:
  Does the LLM response contain quoted text that matches the actual corpus text? 

  Respond with:
  VALID: [YES/NO]
  CONFIDENCE: [HIGH/MEDIUM/LOW]
  EXPLANATION: [Brief explanation of your finding]
  EVIDENCE: [Key phrases that match or don't match]
```

**Migration Complexity**: Low (1-2 days per agent)
- Extract hardcoded prompts to external YAML
- Add Redis task processing wrapper
- Preserve core LLM intelligence

### Type 2: Deterministic Agents (Simple Port)
**Agents**: CalculationAgent, DataExtractionAgent

**Current Architecture**:
```python
# Production CalculationAgent - already THIN
def execute(self, workflow_state, step_config):
    calculation_spec = framework_spec.get('calculation_spec')  # Declarative formulas
    for name, formula in calculation_spec.items():
        code = f"result_data = {formula}"
        execution_result = self.executor.execute_code(code, context)
```

**PoC Adaptation**: Nearly direct port - change trigger mechanism from workflow orchestrator to Redis task

**Migration Complexity**: Low (2-3 days per agent)
- Preserve existing deterministic logic
- Change invocation pattern to Redis task processing
- No architectural changes required

### Type 3: Multi-Step Coordination Agents (Moderate Port)
**Agents**: MethodologicalOverwatchAgent, EnsembleConfigurationAgent, ExecutionPlannerAgent

**Strategy**: Decompose complex multi-step processes into discrete Redis tasks, using OrchestratorAgent intelligence for sequencing

**Example - MethodologicalOverwatchAgent**:
```python
# Current: Single method with multiple steps
def review_analysis_results(self, analysis_results):
    # Step 1: Quality check
    # Step 2: Statistical validation  
    # Step 3: Methodological assessment
    # Return combined decision

# PoC Adaptation: Decompose into tasks
# OrchestratorAgent creates sequence:
# 1. quality_check_task -> QualityCheckAgent
# 2. statistical_validation_task -> StatisticalValidationAgent  
# 3. methodological_assessment_task -> MethodologicalAssessmentAgent
# 4. decision_synthesis_task -> DecisionSynthesisAgent
```

**Migration Complexity**: Moderate (1 week per agent)
- Identify natural task boundaries
- Create sub-agents for each discrete step
- Use OrchestratorAgent for intelligent sequencing

## Detailed Migration Plan

### Phase 1: Proof of Concept (1 week)
**Objective**: Validate the migration approach with one agent from each archetype

1. **ForensicQAAgent Port** (Type 1)
   - Extract validation prompts to external YAML
   - Implement Redis task processing wrapper
   - Test with real corpus/analysis data
   - Verify functional equivalence to production version

2. **CalculationAgent Port** (Type 2)
   - Adapt trigger mechanism to Redis tasks
   - Preserve formula execution logic
   - Test with existing framework calculation specs
   - Validate mathematical output accuracy

3. **Multi-Step Agent Analysis** (Type 3)
   - Select MethodologicalOverwatchAgent for decomposition study
   - Identify discrete task boundaries
   - Design task sequence coordination pattern

### Phase 2: Core Agent Migration (3-4 weeks)
**Priority Order** (based on academic research criticality):

1. **Week 1**: AnalysisAgent (Type 1) - Primary analytical workhorse
2. **Week 2**: SynthesisAgent (Type 1) - Academic report generation
3. **Week 3**: DataExtractionAgent (Type 2) - JSON extraction with retry logic
4. **Week 4**: ProjectCoherenceAnalyst (Type 1/3 hybrid) - Holistic validation

### Phase 3: Advanced Capabilities (2-3 weeks)
1. **Statistical Agents**: StatisticalAnalysisConfigurationAgent
2. **Planning Agents**: ExecutionPlannerAgent  
3. **Quality Assurance**: MethodologicalOverwatchAgent (decomposed)
4. **Model Management**: EnsembleConfigurationAgent

### Phase 4: Integration Testing (1 week)
1. **End-to-end workflow validation**
2. **Performance benchmarking against production**
3. **Academic provenance verification**
4. **Cost/safety guard validation**

## Technical Implementation Patterns

### Agent Registry Expansion
```yaml
# Expanded agent registry supporting production agents
agents:
  # Type 1: LLM-Driven Agents
  - name: ForensicQAAgent
    type: llm_validation
    prompt_file: "agents/ForensicQAAgent/prompt.yaml"
    model: "gemini-2.5-flash"
    inputs: ["corpus_hash", "analysis_result_hash"]
    outputs: ["validation_result_hash"]

  # Type 2: Deterministic Agents  
  - name: CalculationAgent
    type: deterministic
    requires_framework_spec: true
    calculation_spec_key: "calculation_spec"
    inputs: ["analysis_results_hash", "framework_hash"]
    outputs: ["calculation_results_hash"]

  # Type 3: Multi-Step Agents (decomposed)
  - name: MethodologicalOverwatchAgent
    type: orchestrated_sequence
    sub_tasks: ["quality_check", "statistical_validation", "methodological_assessment"]
    coordination_agent: "OrchestratorAgent"
```

### External Prompt Management
```
agents/
├── ForensicQAAgent/
│   ├── main.py
│   ├── prompt.yaml
│   └── config.yaml
├── CalculationAgent/
│   ├── main.py
│   └── config.yaml
├── AnalysisAgent/
│   ├── main.py
│   ├── prompt.yaml
│   └── config.yaml
```

### Redis Task Coordination Patterns
```python
# Standard task processing pattern for all agents
class BasePoCAAgent:
    def process_task(self, task_id: str) -> bool:
        # 1. Get task from Redis stream
        task_data = self._get_redis_task(task_id)
        
        # 2. Retrieve required artifacts
        artifacts = self._get_artifacts(task_data)
        
        # 3. Execute agent logic (LLM call or deterministic processing)
        result = self._execute_agent_logic(artifacts)
        
        # 4. Store result as artifact
        result_hash = put_artifact(result)
        
        # 5. Signal completion
        self._signal_completion(task_id, result_hash)
        
        return True
```

## Risk Assessment and Mitigation

### Technical Risks

**Risk**: Agent functionality degradation during migration
**Mitigation**: Parallel validation - run both production and PoC versions, compare outputs

**Risk**: Complex state management doesn't translate to stateless model  
**Mitigation**: Phase 1 proof-of-concept validates approach before full commitment

**Risk**: Performance regression due to Redis overhead
**Mitigation**: Benchmark early, optimize Redis configurations, leverage parallelization gains

### Timeline Risks

**Risk**: Underestimating integration complexity
**Mitigation**: Phase 1 provides realistic complexity assessment, adjust timeline based on findings

**Risk**: THICK code drift during implementation
**Mitigation**: Strict external prompt requirements, code review focus on THIN principles

## Success Criteria

### Functional Parity
- [ ] All production agents successfully ported to PoC architecture
- [ ] Identical analytical outputs between production and PoC versions
- [ ] Academic provenance and validation capabilities preserved

### Architectural Benefits
- [ ] Elimination of parsing code and orchestration brittleness
- [ ] Parallelization performance improvements demonstrated
- [ ] Security improvements - no runaway execution risks
- [ ] THIN architecture compliance maintained

### Operational Readiness
- [ ] Comprehensive testing infrastructure implemented
- [ ] Cost and safety guards functional
- [ ] Academic workflow integration verified
- [ ] Documentation and deployment procedures complete

## Conclusion

The analysis demonstrates that sophisticated production agents can be successfully migrated to the PoC's THIN architecture. The key insight is that most production agents already follow THIN principles internally - they use LLM intelligence for complex decisions and declarative specifications for deterministic processing.

The migration strategy preserves analytical sophistication while eliminating the orchestration brittleness that has plagued the production system. The estimated timeline of 6-8 weeks represents a substantial improvement over rebuilding agent capabilities from scratch.

**Recommendation**: Proceed with Phase 1 proof-of-concept to validate the approach with ForensicQAAgent and CalculationAgent before committing to full migration.

---

*This document integrates findings from the technical co-founder assessment and provides a concrete roadmap for preserving production agent capabilities within the PoC's superior architectural foundation.*