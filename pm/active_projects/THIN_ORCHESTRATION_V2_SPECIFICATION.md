# THIN Orchestration v2.0 Specification
**Date**: July 25, 2025  
**Status**: Draft Specification - Based on Distributed Prototype Learnings  
**Branch**: feature/thin-orchestration-v2

---

## Executive Summary

Based on the distributed coordination prototype, we learned that **LLM agents produce quality academic output** but **distributed coordination creates reliability problems**. This specification preserves the proven agent intelligence while simplifying coordination through direct function calls.

---

## Key Learnings from Distributed Prototype

### ✅ **What Worked Well**
1. **Multi-stage processing**: BatchAnalysis → Synthesis → Report produces better results than single-shot
2. **LLM agent quality**: Generated 120-line academic research reports with proper analysis
3. **Framework-agnostic processing**: Successfully processed CAF v4.3 without hardcoded logic
4. **BaseAgent infrastructure**: Standardized logging, YAML prompts, MinIO integration solid
5. **Artifact storage**: Content-addressable storage provides good provenance

### ❌ **What Created Problems**
1. **Redis coordination**: Required manual intervention, tasks got stuck
2. **Process spawning**: Router complexity, silent failures, debugging difficulty
3. **Distributed state**: Result hash passing fragile, orchestrator died mid-process
4. **Observability**: CLI disconnected from actual system state
5. **Error recovery**: No graceful handling, required manual Redis manipulation

---

## THIN Orchestration v2.0 Architecture

### Core Principle: **Direct Function Calls, Not Distributed Coordination**

```python
class ThinOrchestrator:
    def __init__(self):
        self.batch_agent = AnalyseBatchAgent()
        self.synthesis_agent = SynthesisAgent()
        self.report_agent = ReportAgent()
        self.storage = MinIOStorage()  # Keep for provenance
        
    def run_experiment(self, experiment_path: Path) -> ExperimentResult:
        # Standard Python exception handling
        try:
            # 1. Validation (keep existing pattern)
            experiment = self.validate_experiment(experiment_path)
            run_id = self.create_run_folder(experiment)
            
            # 2. Direct agent calls with clear data flow
            batch_result = self.batch_agent.analyze(
                documents=experiment.corpus,
                framework=experiment.framework,
                run_id=run_id
            )
            
            synthesis_result = self.synthesis_agent.synthesize(
                batch_results=[batch_result],
                framework=experiment.framework,
                run_id=run_id
            )
            
            final_report = self.report_agent.generate(
                synthesis_result=synthesis_result,
                experiment_metadata=experiment.metadata,
                run_id=run_id
            )
            
            # 3. Save all results to filesystem AND MinIO
            self.save_results(run_id, batch_result, synthesis_result, final_report)
            
            return ExperimentResult(run_id, final_report)
            
        except Exception as e:
            # Standard Python stack traces, no distributed debugging
            self.log_error(f"Experiment failed: {e}")
            raise
```

---

## Component Architecture

### **1. Preserve Proven Agent Intelligence**

Keep the existing agent implementations that work:
- **AnalyseBatchAgent**: Multi-document, multi-framework batch processing
- **SynthesisAgent**: Statistical aggregation and pattern analysis  
- **ReportAgent**: Human-readable academic report generation
- **BaseAgent**: Standardized logging, YAML prompts, MinIO integration

**Change**: Call as functions, not through Redis coordination.

### **2. Simplified Data Flow**

```
Input: experiment.yaml + framework.md + corpus/
  ↓ (direct function call)
BatchAnalysis: documents → structured analysis results
  ↓ (direct function call)  
Synthesis: analysis results → statistical aggregation
  ↓ (direct function call)
Report: synthesis results → academic report
  ↓ (direct file write)
Output: results written to both filesystem and MinIO
```

### **3. Preserved Capabilities**

**Keep everything that works:**
- Framework-agnostic processing
- External YAML prompts for agent customization
- MinIO artifact storage for provenance
- Complete audit trails and result hashing
- CLI interface and validation patterns
- Multi-run statistical capabilities

**Remove complexity that causes problems:**
- Redis coordination and task queues
- Process spawning and router complexity
- Distributed state management
- Complex completion signaling

---

## Scaling Strategy

### **Single-Process Scaling (Sufficient for Academic Use)**
```python
def run_large_experiment(self, experiment):
    # For corpora that fit in memory: direct processing
    if experiment.corpus_size < 1000:
        return self.run_sequential(experiment)
    
    # For large corpora: batch processing with progress tracking
    batches = self.partition_corpus(experiment.corpus, batch_size=50)
    batch_results = []
    
    for i, batch in enumerate(batches):
        self.log_progress(f"Processing batch {i+1}/{len(batches)}")
        result = self.batch_agent.analyze(batch, experiment.framework)
        batch_results.append(result)
    
    # Continue with synthesis and reporting
    return self.complete_processing(batch_results, experiment)
```

### **Future: Add Multiprocessing When Needed**
```python
# Only if single-process proves insufficient
def run_parallel_experiment(self, experiment):
    with multiprocessing.Pool() as pool:
        batch_results = pool.map(
            partial(self.process_batch, framework=experiment.framework),
            self.partition_corpus(experiment.corpus)
        )
    return self.aggregate_results(batch_results)
```

---

## Error Handling and Observability

### **Standard Python Patterns**
```python
def run_experiment(self, experiment_path):
    try:
        # Clear logging at each stage
        self.logger.info(f"Starting experiment: {experiment_path}")
        
        experiment = self.validate_experiment(experiment_path)
        self.logger.info(f"Validation complete: {experiment.name}")
        
        batch_result = self.batch_agent.analyze(experiment)
        self.logger.info(f"Batch analysis complete: {len(batch_result.documents)} docs")
        
        # etc. - clear progress at each stage
        
    except ValidationError as e:
        self.logger.error(f"Experiment validation failed: {e}")
        raise
    except LLMError as e:
        self.logger.error(f"LLM processing failed: {e}")
        raise
    except Exception as e:
        self.logger.error(f"Unexpected error: {e}")
        # Standard Python stack trace shows exactly where failure occurred
        raise
```

### **CLI Status Integration**
```python
def get_run_status(self, run_id):
    """CLI status that reflects actual file system state"""
    run_path = Path(f"projects/experiment/runs/{run_id}")
    
    return RunStatus(
        validation=self.check_stage_complete(run_path / "validation.log"),
        batch_analysis=self.check_stage_complete(run_path / "results/batch_analysis"),
        synthesis=self.check_stage_complete(run_path / "results/synthesis"),
        report=self.check_stage_complete(run_path / "results/reports")
    )
```

---

## Implementation Plan

### **Phase 1: Core Simplification (3-4 days)**
1. Create `ThinOrchestrator` class with direct function calls
2. Preserve existing agent implementations, change invocation pattern
3. Remove Redis dependencies, router complexity
4. Ensure CLI status reflects actual file system state

### **Phase 2: Enhanced Error Handling (1-2 days)**  
1. Add comprehensive logging at each stage
2. Implement graceful error recovery
3. Add progress tracking for large experiments
4. Test with the three existing test experiments

### **Phase 3: Performance Optimization (2-3 days)**
1. Add batch processing for large corpora
2. Implement caching to avoid redundant LLM calls
3. Add multiprocessing if single-process proves insufficient
4. Benchmark performance vs. distributed approach

---

## Success Criteria

### **Reliability Requirements**
- ✅ **Zero manual interventions**: Experiments run from start to finish without debugging
- ✅ **Clear error messages**: Standard Python exceptions with actionable stack traces  
- ✅ **Accurate status reporting**: CLI reflects actual processing state
- ✅ **Graceful failure handling**: Partial results preserved, clear error reporting

### **Quality Requirements** 
- ✅ **Same output quality**: Academic reports as good as distributed prototype
- ✅ **Framework agnostic**: Works with any specification-compliant framework
- ✅ **Complete provenance**: Full audit trails in MinIO and file system
- ✅ **Performance competitive**: Faster than distributed approach due to no coordination overhead

### **Maintainability Requirements**
- ✅ **Single-developer comprehensible**: New developer can understand system in one day
- ✅ **Standard debugging**: Python debugger works, no distributed system expertise needed
- ✅ **Local development**: Full system runs on laptop without infrastructure dependencies

---

## Conclusion

The distributed coordination prototype proved that **LLM agents can produce quality academic research**. This specification preserves that proven capability while eliminating the coordination complexity that caused reliability problems.

**The goal**: Same quality outputs with boring reliability - experiments that run without manual intervention and produce the same quality research reports we achieved in the prototype.

**The test**: Can a researcher run `discernus run experiment.yaml` and get a complete research report without any manual debugging or system intervention?

With this architecture: **Yes**. 