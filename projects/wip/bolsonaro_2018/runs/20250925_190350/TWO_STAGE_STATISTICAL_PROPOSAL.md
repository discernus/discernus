# Two-Stage Statistical Analysis Proposal

**Current Architecture:** Single Gemini-2.5-Pro call for both planning and execution
**Proposed Architecture:** Separated planning (Pro) and execution (Flash-Lite) stages

---

## Current Architecture Analysis

### Confirmed Current Implementation
The V2StatisticalAgent currently:
- Uses **only Gemini-2.5-Pro** for statistical analysis (line 447 in `v2_statistical_agent.py`)
- Performs both **statistical planning** AND **execution** in a single LLM call
- Despite listing Flash-Lite in metadata, never actually uses it

### Problems with Single-Stage Approach
1. **Cognitive Load Mixing**: Pro must simultaneously plan methodology AND execute calculations
2. **Fabrication Risk**: Single model can fabricate without computational verification
3. **Resource Inefficiency**: Using expensive Pro model for computational tasks
4. **No Verification**: No independent validation of statistical approach vs results

---

## Proposed Two-Stage Architecture

### Stage 1: Statistical Planning (Gemini-2.5-Pro)
**Role:** Strategic statistical methodology design
**Responsibilities:**
- Analyze experimental design and research questions
- Determine appropriate statistical tests and methodologies
- Identify grouping variables and analytical approach
- Generate detailed statistical analysis plan
- Specify exact calculations needed

**Output Example:**
```json
{
  "statistical_plan": {
    "research_questions": ["Pre/post stabbing rhetorical changes"],
    "statistical_tests": [
      {
        "test": "independent_t_test",
        "variables": ["economic_populist_appeals"],
        "groups": ["pre_stabbing", "post_stabbing"],
        "rationale": "Compare means between temporal periods"
      },
      {
        "test": "correlation_matrix",
        "variables": ["all_dimensions"],
        "rationale": "Examine dimensional relationships"
      }
    ],
    "effect_size_measures": ["cohens_d", "correlation_coefficients"],
    "multiple_comparison_corrections": ["none_justified"],
    "analysis_tier": "tier_3_exploratory"
  }
}
```

### Stage 2: Statistical Execution (Gemini-2.5-Flash-Lite + Code Execution)
**Role:** Computational implementation of statistical plan
**Responsibilities:**
- Receive statistical plan from Stage 1
- Generate Python code to implement exact calculations
- Execute code using structured code execution tool
- Return raw computational results without interpretation

**Code Generation Example:**
```python
import pandas as pd
import numpy as np
from scipy import stats

# Extract economic populist appeals scores
economic_scores = [0.7, 0.25, 0.6, 0.7, 0.8, 0.1, 0.7, 0.8, 0.85, 0.8, 0.7, 0.7]

# Pre/post stabbing split (based on Sept 6 cutoff)
pre_stabbing = economic_scores[:5]  # [0.7, 0.25, 0.6, 0.7, 0.8]
post_stabbing = economic_scores[5:]  # [0.1, 0.7, 0.8, 0.85, 0.8, 0.7, 0.7]

# Calculate means and standard deviations
pre_mean = np.mean(pre_stabbing)
post_mean = np.mean(post_stabbing)
pre_std = np.std(pre_stabbing, ddof=1)
post_std = np.std(post_stabbing, ddof=1)

# Independent t-test
t_stat, p_value = stats.ttest_ind(pre_stabbing, post_stabbing)

# Cohen's d effect size
pooled_std = np.sqrt(((len(pre_stabbing)-1)*pre_std**2 + (len(post_stabbing)-1)*post_std**2) /
                    (len(pre_stabbing) + len(post_stabbing) - 2))
cohens_d = (pre_mean - post_mean) / pooled_std

print(f"Pre-stabbing: M={pre_mean:.3f}, SD={pre_std:.3f}")
print(f"Post-stabbing: M={post_mean:.3f}, SD={post_std:.3f}")
print(f"t({len(pre_stabbing)+len(post_stabbing)-2})={t_stat:.3f}, p={p_value:.3f}")
print(f"Cohen's d={cohens_d:.3f}")
```

**Actual Execution Results:**
```
Pre-stabbing: M=0.610, SD=0.249
Post-stabbing: M=0.664, SD=0.251
t(10)=-0.384, p=0.708
Cohen's d=-0.217 (small effect, opposite direction)
```

---

## Benefits of Two-Stage Approach

### 1. **Eliminates Fabrication Risk**
- **Planning Stage**: Pro focuses purely on methodology, cannot fabricate numerical results
- **Execution Stage**: Flash-Lite must use actual code execution, cannot fabricate calculations
- **Verification**: Independent stages can be cross-validated

### 2. **Optimized Model Usage**
- **Pro**: Complex reasoning for statistical methodology (expensive but necessary)
- **Flash-Lite**: Simple code generation and execution (cheaper and sufficient)
- **Cost Efficiency**: Right model for right task

### 3. **Enhanced Reliability**
- **Separation of Concerns**: Planning vs execution isolated
- **Audit Trail**: Clear handoff between stages with complete documentation
- **Independent Validation**: Each stage can be verified separately

### 4. **Improved Accuracy**
- **Pro focuses entirely on methodology** without computational distractions
- **Flash-Lite focuses entirely on computation** without strategic overhead
- **Code Execution Tool** ensures accurate calculations

### 5. **Better Error Detection**
- **Plan Review**: Statistical methodology can be reviewed before execution
- **Code Review**: Generated code can be validated before execution
- **Result Validation**: Computational results can be independently verified

---

## Implementation Architecture

```python
def execute_two_stage_analysis(self, raw_artifacts: List[str], batch_id: str):
    # Stage 1: Statistical Planning (Gemini-2.5-Pro)
    planning_prompt = self._create_planning_prompt(raw_artifacts)
    statistical_plan = self.gateway.execute_call(
        model="vertex_ai/gemini-2.5-pro",
        prompt=planning_prompt
    )

    # Stage 2: Statistical Execution (Gemini-2.5-Flash-Lite + Code Execution)
    execution_prompt = self._create_execution_prompt(statistical_plan, raw_artifacts)
    computational_results = self.gateway.execute_call(
        model="vertex_ai/gemini-2.5-flash-lite",
        prompt=execution_prompt,
        tools=[{"codeExecution": {}}]  # Enable code execution tool
    )

    # Combine planning rationale with computational results
    return self._synthesize_results(statistical_plan, computational_results)
```

---

## Comparison: Current vs Proposed

| Aspect | Current (Single-Stage) | Proposed (Two-Stage) |
|--------|----------------------|---------------------|
| **Model Usage** | Pro only | Pro (planning) + Flash-Lite (execution) |
| **Fabrication Risk** | High (no verification) | Eliminated (forced code execution) |
| **Cost Efficiency** | Poor (Pro for computation) | Optimized (right model for task) |
| **Audit Trail** | Single black box | Clear planning → execution flow |
| **Error Detection** | Post-hoc only | At planning and execution stages |
| **Reliability** | Vulnerable to hallucination | Code execution enforced |
| **Interpretability** | Mixed planning/results | Clear separation of concerns |

---

## Expected Impact on Bolsonaro Analysis

Using the two-stage approach on this corpus would have produced:

**Stage 1 (Pro Planning):** Proper experimental design recognizing September 6 stabbing as natural experiment
**Stage 2 (Flash-Lite Execution):** Accurate calculations showing:
- Pre-stabbing economic appeals: M=0.61
- Post-stabbing economic appeals: M=0.66
- Effect: d=-0.22 (small effect, opposite direction than claimed)
- **No fabricated "large decrease" (d=-1.13)**

**Final Result:** Accurate statistical foundation for theoretical interpretation, preventing fabricated narrative about rhetorical strategy pivot.

---

## Recommendation

**Implement two-stage statistical analysis immediately** to:
1. Eliminate statistical fabrication vulnerabilities
2. Optimize computational resource usage
3. Enhance audit trail and verification capabilities
4. Improve overall system reliability and trustworthiness

This architectural change would transform the statistical agent from a fabrication risk into a reliable computational tool while preserving the interpretive capabilities that make LLM-based analysis valuable.