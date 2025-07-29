# THIN Multi-Document Analysis Workflow Plan

**Date**: January 26, 2025  
**Status**: Implementation Ready  
**Architecture**: Pure THIN - LLM Intelligence with Software Coordination Only  

---

## Executive Summary

**THE CORRECT THIN SOLUTION**: Ask LLMs to perform framework calculations directly and show their mathematical work, then use batch synthesis LLM calls to extract calculated results into research-ready CSV format.

**Key Insight**: The LLM is already capable of performing all framework calculations (Character Tension, MC-SCI, cluster scores, etc.). Instead of building complex parsing pipelines, simply ask the LLM to do the math and show the work, then extract the calculated numbers via subsequent LLM calls.

**Result**: Pure THIN architecture with no parsing, no transformation pipelines, and complete framework agnosticism.

---

## Architecture Overview

### **4-Stage THIN Workflow**

```
Stage 1: Enhanced Analysis     → Individual documents with LLM calculations
Stage 2: Batch Synthesis       → Extract calculated numbers → CSV batches  
Stage 3: Rollup Synthesis      → Combine CSV batches → Master CSV (if needed)
Stage 4: Final Synthesis       → Statistical analysis + interpretive report
```

### **Core THIN Principles**

✅ **LLM Intelligence**: All calculations, reasoning, and format handling  
✅ **Software Coordination**: File management, batch orchestration, verification only  
✅ **Framework Agnostic**: LLM understands any framework's calculation requirements  
✅ **No Parsing**: LLM outputs desired formats directly  
✅ **Mathematical Rigor**: "Show your math" with programmatic verification  

---

## Stage 1: Enhanced Analysis Agent

### **Current State**: Already Working ✅
- Individual document analysis with structured JSON output
- LLM performs framework calculations and shows mathematical work
- ~15KB JSON artifacts with complete analysis + verification

### **Enhancement Required**: Calculation Emphasis
```yaml
analysis_prompt_addition: |
  CRITICAL: After completing your analysis, PERFORM ALL FRAMEWORK CALCULATIONS 
  and SHOW YOUR MATHEMATICAL WORK step-by-step.
  
  For CAF v4.3, calculate and verify:
  1. All 5 Character Tension scores using the formula
  2. Moral Character Strategic Contradiction Index (MC-SCI)  
  3. Virtue and Vice cluster scores (salience-weighted)
  4. Character Balance, Intensity, and Moral Clarity
  5. Character Salience Concentration (standard deviation)
  
  Include a "mathematical_verification" section with:
  - Step-by-step calculations showing your work
  - Formula applications with actual numbers
  - Confidence assessment for each calculated result
```

---

## Stage 2: Batch Synthesis Agent

### **Purpose**: Extract Calculated Numbers → Research CSV

**Input**: Batch of analysis JSON artifacts (with calculations completed)  
**Output**: CSV with extracted calculated results  
**Batch Size**: Dynamic based on context window and base64 overhead  

### **Context Window Calculation**
```python
# Account for base64 encoding overhead (33% increase)
base64_doc_size = avg_doc_size_kb * 1.33
base64_framework_size = framework_size_kb * 1.33
per_doc_context = base64_doc_size + base64_framework_size + analysis_context

# Gemini 2.5 Flash: ~8MB context budget
available_context = 8000 - 100  # 100KB response buffer
safe_context = available_context * 0.7  # 30% safety margin
batch_size = safe_context / per_doc_context

# For large_batch_test (46 docs, 35KB avg):
# Per doc context: ~82KB (including base64 overhead)
# Recommended batch size: ~40 documents
# 46 documents → 2 batches of 23 documents each
```

### **Batch Synthesis Prompt Pattern**
```python
batch_synthesis_prompt = f"""
Extract the calculated results from these {batch_size} analysis JSONs into research CSV.

INPUT: Analysis JSONs with completed mathematical_verification sections
TASK: Extract ONLY the calculated values (do not recalculate)

CSV Structure for CAF v4.3:
document_id, dignity_score, dignity_salience, tribalism_score, tribalism_salience, 
dignity_tribalism_tension, truth_score, truth_salience, manipulation_score, 
manipulation_salience, truth_manipulation_tension, [all dimensions], 
mc_sci, virtue_cluster, vice_cluster, character_balance, character_intensity, 
moral_clarity, character_salience_concentration

CRITICAL RULES:
1. Extract calculated values from mathematical_verification sections
2. Do NOT perform new calculations
3. Verify extracted numbers match the analysis show-work
4. Flag any discrepancies found
5. Output clean CSV format (no markdown code fences)
"""
```

---

## Stage 3: Rollup Synthesis Agent

### **Trigger Condition**: Multiple batch CSVs from Stage 2
**Input**: Array of batch CSV files  
**Output**: Single master CSV with all documents  

### **Rollup Synthesis Prompt**
```python
rollup_prompt = """
Combine these batch CSV files into a single master CSV.

INPUT: {num_batches} CSV files with calculated results
TASK: Simple concatenation preserving all data

CRITICAL RULES:
1. Concatenate all rows (no mathematical operations)
2. Verify no documents missing or duplicated
3. Maintain all calculated values exactly as provided
4. Add batch_source column for provenance tracking
5. Output clean CSV format

This is pure data consolidation - NO recalculation permitted.
"""
```

### **Verification Logic**
```python
def verify_rollup_integrity(master_csv, batch_csvs, original_documents):
    """Ensure rollup preserves all data correctly"""
    master_rows = count_csv_rows(master_csv)
    batch_total_rows = sum(count_csv_rows(csv) for csv in batch_csvs)
    expected_rows = len(original_documents)
    
    assert master_rows == batch_total_rows == expected_rows
    assert no_duplicate_document_ids(master_csv)
    assert all_calculated_values_preserved(master_csv, batch_csvs)
```

---

## Stage 4: Final Synthesis Agent

### **Input**: Master CSV with all per-document calculations completed
**Output**: Complete research report with statistical analysis and interpretation

### **Final Synthesis Prompt**
```python
final_synthesis_prompt = """
Analyze this master CSV data using the framework's interpretive guidance.

PROVIDED: CSV with ALL per-document calculations already completed and verified
TASK: Statistical analysis + framework-guided interpretation

PERFORM:
1. Descriptive statistics (means, standard deviations, distributions)
2. Framework-specific pattern analysis using calculated metrics
3. Cross-document comparisons and clustering analysis  
4. Interpretive synthesis as specified by the framework
5. Statistical significance testing where appropriate

SHOW YOUR MATH for any additional statistical calculations beyond the provided data.
The individual document calculations are already verified - build upon them.

Focus on interpretation and synthesis, not recalculation of provided metrics.
"""
```

---

## Dynamic Batch Management System

### **Orchestrator Batch Decision Logic**

```python
class ThinBatchOrchestrator:
    def __init__(self, experiment_path):
        self.context_limit_mb = 8.0  # Gemini 2.5 Flash
        self.base64_overhead = 1.33  # 33% encoding increase
        self.safety_margin = 0.3     # 30% context safety buffer
        
    def create_execution_plan(self, documents, framework):
        """Determine optimal batching strategy"""
        batch_size = self._calculate_optimal_batch_size(documents, framework)
        
        if len(documents) <= batch_size:
            return {
                'strategy': 'single_batch',
                'analysis_batches': 1,
                'synthesis_batches': 1, 
                'needs_rollup': False,
                'estimated_time_minutes': len(documents) * 1.2 + 5
            }
        else:
            num_batches = math.ceil(len(documents) / batch_size)
            return {
                'strategy': 'multi_batch',
                'analysis_batches': len(documents),  # Always parallel
                'synthesis_batches': num_batches,
                'needs_rollup': True,
                'estimated_time_minutes': len(documents) * 1.2 + num_batches * 3 + 10
            }
    
    def _calculate_optimal_batch_size(self, documents, framework):
        avg_doc_size = sum(doc.size_kb for doc in documents) / len(documents)
        
        # Account for base64 encoding overhead
        context_per_doc = (avg_doc_size + framework.size_kb) * self.base64_overhead + 15
        
        # Calculate available context with safety margin
        available_context = (self.context_limit_mb * 1024) * (1 - self.safety_margin) - 100
        
        return max(1, min(int(available_context / context_per_doc), 40))
```

### **Progress Tracking & State Management**

```python
class ExperimentState:
    def __init__(self):
        self.stages = {
            'analysis': {'total': 0, 'complete': 0, 'failed': 0},
            'batch_synthesis': {'total': 0, 'complete': 0, 'failed': 0}, 
            'rollup_synthesis': {'required': False, 'complete': False},
            'final_synthesis': {'complete': False}
        }
        
    def get_progress_summary(self):
        """Real-time experiment progress"""
        analysis_pct = (self.stages['analysis']['complete'] / 
                       max(1, self.stages['analysis']['total'])) * 100
        
        synthesis_pct = (self.stages['batch_synthesis']['complete'] / 
                        max(1, self.stages['batch_synthesis']['total'])) * 100
        
        return {
            'analysis_progress': f"{analysis_pct:.1f}%",
            'synthesis_progress': f"{synthesis_pct:.1f}%", 
            'rollup_needed': self.stages['rollup_synthesis']['required'],
            'overall_stage': self._determine_current_stage()
        }
```

---

## Implementation Roadmap

### **Phase 1: Enhanced Analysis Calculations (2-3 days)**
- ✅ Analysis agent already works - enhance prompts to emphasize calculations
- ✅ Verify mathematical_verification sections are comprehensive
- ✅ Test with simple_test project (2 documents)

### **Phase 2: Batch Synthesis Implementation (3-4 days)**  
- 🔄 Create BatchSynthesisAgent with CSV extraction logic
- 🔄 Implement dynamic batch size calculation with base64 overhead
- 🔄 Add batch CSV verification and quality checks
- 🔄 Test with large_batch_test project (46 documents)

### **Phase 3: Rollup & Final Synthesis (2-3 days)**
- 📋 Implement RollupSynthesisAgent for multi-batch consolidation  
- 📋 Enhanced FinalSynthesisAgent for statistical analysis
- 📋 End-to-end integration with ThinBatchOrchestrator

### **Phase 4: Production Validation (1-2 days)**
- 📋 Test with multiple frameworks (CAF, PDAF, etc.)
- 📋 Performance optimization and error handling
- 📋 Documentation and developer guidance

---

## Verification & Quality Assurance

### **Mathematical Verification Pipeline**
```python
class CalculationVerifier:
    def verify_analysis_math(self, analysis_json):
        """Spot-check LLM mathematical work"""
        calcs = analysis_json['mathematical_verification']
        
        # Verify key calculations programmatically
        tensions = self._verify_tension_calculations(calcs['character_tension_calculations'])
        clusters = self._verify_cluster_calculations(calcs['character_cluster_calculations'])  
        
        return {
            'tensions_verified': tensions,
            'clusters_verified': clusters,
            'discrepancies': self._identify_discrepancies(tensions, clusters)
        }
```

### **CSV Extraction Verification**
```python
def verify_csv_extraction(csv_output, source_analyses):
    """Ensure CSV accurately reflects analysis calculations"""
    for row in csv_output:
        source_analysis = find_analysis_by_document_id(row['document_id'], source_analyses)
        
        # Verify key calculated values match
        assert row['mc_sci'] == source_analysis['mathematical_verification']['mc_sci_calculation']['result_rounded']
        assert row['virtue_cluster'] == source_analysis['mathematical_verification']['character_cluster_calculations']['virtue_cluster_score']['result_rounded']
        # ... verify all calculated fields
```

---

## Success Criteria

### **Functional Requirements**
- ✅ **Simple Test**: 2 documents → single batch → direct final synthesis
- ✅ **Large Batch Test**: 46 documents → 2 batches → rollup → final synthesis  
- ✅ **Framework Agnostic**: Works with CAF, PDAF, and future frameworks
- ✅ **Mathematical Accuracy**: All calculations verified and reproducible

### **THIN Architecture Compliance**
- ✅ **No Parsing Logic**: LLM handles all format generation and interpretation
- ✅ **No Framework Hardcoding**: Software agnostic to framework specifics  
- ✅ **No Intelligence in Software**: Coordination and verification only
- ✅ **Complete Auditability**: Every calculation traceable and verifiable

### **Performance Benchmarks**  
- ✅ **Simple Test (2 docs)**: Complete in under 5 minutes
- ✅ **Large Batch (46 docs)**: Complete in under 30 minutes
- ✅ **Context Efficiency**: No context window failures due to poor batching
- ✅ **Cost Optimization**: Minimal redundant LLM calls

---

## Conclusion

This THIN multi-document analysis workflow solves the original large corpus synthesis challenge while maintaining pure THIN architectural principles. By leveraging the LLM's existing calculation capabilities and using intelligent batch synthesis, we achieve:

1. **Framework Agnosticism**: LLM understands any framework's calculations
2. **Mathematical Rigor**: "Show your math" with programmatic verification  
3. **Scalability**: Handles corpora from 2 to thousands of documents
4. **Research Ready**: Direct CSV output for R/pandas analysis
5. **Complete Transparency**: End-to-end audit trail and reproducibility

**The key insight**: Stop trying to make software intelligent. Let the LLM do what it does best - understand natural language requirements and perform complex reasoning - while software provides only coordination and verification.

This approach eliminates the entire parsing pipeline that caused the previous architectural confusion and delivers the large-scale synthesis capability the project requires.

---

**Next Actions**: Begin Phase 1 implementation with enhanced analysis calculation prompts, then proceed through systematic implementation and testing of each stage. 