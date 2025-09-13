# Show Your Work Architecture

## Executive Summary

The "Show Your Work" architecture represents a fundamental shift from deterministic execution to adversarial attestation. By leveraging modern LLM capabilities with structured output via tool calling, we achieve massive scalability improvements while maintaining verifiability through multi-tier verification.

### Key Innovations
1. **LLM Internal Execution**: Primary LLMs perform calculations internally and provide results directly via tool calls
2. **Adversarial Attestation**: Separate verifier LLMs validate the work by examining the code and output
3. **Structured Output via Tool Calling**: Eliminates parsing brittleness by using platform-guaranteed structured responses
4. **Selective File Passing**: Context management through intelligent artifact selection
5. **Fail-Fast Verification**: Immediate error reporting when verification fails

## Core Principle: Structured Output via Multi-Tool Calling

The fundamental principle of this architecture is that **LLMs provide structured data through multiple focused tool calls (function calls), not through text parsing**. This approach works around Gemini 2.5 Pro's limitations with complex nested schemas while maintaining full functionality.

### How Multi-Tool Calling Works

Instead of one complex tool, we use three focused tools that work together:

```python
# Three-Tool Schema (provided to LLM)
tools = [
    {
        "type": "function",
        "function": {
            "name": "record_analysis_scores",
            "description": "Record dimensional scores with confidence and salience",
            "parameters": {
                "type": "object",
                "properties": {
                    "document_id": {"type": "string"},
                    "framework_name": {"type": "string"},
                    "framework_version": {"type": "string"},
                    "scores": {
                        "type": "object",
                        "additionalProperties": {
                            "type": "object",
                            "properties": {
                                "raw_score": {"type": "number"},
                                "salience": {"type": "number"},
                                "confidence": {"type": "number"}
                            }
                        }
                    }
                },
                "required": ["document_id", "framework_name", "framework_version", "scores"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "record_evidence_quotes",
            "description": "Record evidence quotes and reasoning for each dimension",
            "parameters": {
                "type": "object",
                "properties": {
                    "document_id": {"type": "string"},
                    "evidence": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "dimension": {"type": "string"},
                                "quote": {"type": "string"},
                                "reasoning": {"type": "string"}
                            }
                        }
                    }
                },
                "required": ["document_id", "evidence"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "record_computational_work",
            "description": "Record derived metrics calculations and code execution",
            "parameters": {
                "type": "object",
                "properties": {
                    "document_id": {"type": "string"},
                    "executed_code": {"type": "string"},
                    "execution_output": {"type": "string"},
                    "derived_metrics": {
                        "type": "object",
                        "additionalProperties": {"type": "number"}
                    }
                },
                "required": ["document_id", "executed_code", "execution_output", "derived_metrics"]
            }
        }
    }
]

# LLM Response (3 sequential tool calls)
# The API guarantees this structure - no string parsing needed!
tool_calls = [
    {
        "name": "record_analysis_scores",
        "arguments": {
            "document_id": "doc_001",
            "framework_name": "pdaf_v10",
            "scores": {
                "populism": {"raw_score": 0.8, "salience": 0.9, "confidence": 1.0},
                "authoritarianism": {"raw_score": 0.7, "salience": 0.8, "confidence": 0.9}
            }
        }
    },
    {
        "name": "record_evidence_quotes", 
        "arguments": {
            "document_id": "doc_001",
            "evidence": [
                {
                    "dimension": "populism",
                    "quote": "The people are being betrayed by the elite...",
                    "reasoning": "Direct people vs elite framing"
                }
            ]
        }
    },
    {
        "name": "record_computational_work",
        "arguments": {
            "document_id": "doc_001",
            "executed_code": "import numpy as np\noverall_intensity = np.mean([0.8, 0.7])",
            "execution_output": "0.75",
            "derived_metrics": {"overall_intensity": 0.75}
        }
    }
]

# Agent processes each tool call and saves artifacts
for tool_call in tool_calls:
    if tool_call["name"] == "record_analysis_scores":
        with open("analysis_scores.json", "w") as f:
            json.dump(tool_call["arguments"], f)
    elif tool_call["name"] == "record_evidence_quotes":
        with open("evidence_quotes.json", "w") as f:
            json.dump(tool_call["arguments"], f)
    elif tool_call["name"] == "record_computational_work":
        with open("computational_work.json", "w") as f:
            json.dump(tool_call["arguments"], f)
```

### Benefits of Multi-Tool Calling

1. **Zero Parsing**: The agent receives structured data from the API, not strings to parse
2. **Guaranteed Schema**: The platform ensures the response matches the tool definition
3. **Gemini Compatibility**: Works around Gemini 2.5 Pro's limitations with complex nested schemas
4. **Clean Artifacts**: Each tool call produces discrete, well-formed files
5. **Single LLM Call**: Uses full context window efficiently without artificial chunking
6. **Internal Processing**: LLM does three-phase analysis internally, returns aggregated results
7. **Robust Error Handling**: Individual tool failures don't break entire analysis

## Data Flow

```
Document → EnhancedAnalysisAgentMultiTool (with multi-tool calling)
    ├── Creates: analysis_scores.json (dimensional scores with confidence/salience)
    ├── Creates: evidence_quotes.json (evidence quotes and reasoning)
    └── Creates: computational_work.json (derived metrics and code execution)
           ↓
    VerificationAgent (adversarial LLM with tool calling)
    ├── Reads: analysis_scores.json, evidence_quotes.json, computational_work.json
    └── Creates: attestation.json (verification results)
           ↓
    [Repeat for all documents]
           ↓
    Statistical Planning + Execution Agent (with tool calling)
    ├── Reads: All analysis_scores.json files (numerical data only)
    ├── Creates: statistics.json (results)
    ├── Creates: statistical_work.json (code, output)
    └── Creates: statistical_data.csv (aggregated data)
           ↓
    Statistical Verification Agent (with tool calling)
    ├── Reads: statistics.json, statistical_work.json, statistical_data.csv
    └── Creates: statistical_attestation.json
           ↓
    Evidence CSV Export Module (deterministic Python)
    ├── Reads: All evidence_quotes.json files
    └── Creates: evidence.csv
           ↓
    Synthesis Agent
    ├── Reads: Curated evidence from Evidence Retriever
    └── Creates: Final synthesis report
```

## Adversarial Attestation Flow

This 5-step process is the core of the "Show Your Work" architecture:

1. **Primary Work**: The primary LLM (e.g., Gemini 2.5 Pro) performs analysis, executes code internally, and calls three tools with:
   - `record_analysis_scores`: Dimensional scores with confidence/salience
   - `record_evidence_quotes`: Evidence quotes and reasoning
   - `record_computational_work`: Derived metrics and code execution

2. **Work Storage**: The agent saves these as separate artifact files:
   - `analysis_scores.json`: The dimensional scores
   - `evidence_quotes.json`: The evidence and reasoning
   - `computational_work.json`: The code and output for verification

3. **Adversarial Verification**: A `VerificationAgent` with a different LLM (initially Gemini, later DeepSeek-Prover-V2):
   - Reads all three artifacts (analysis_scores.json, evidence_quotes.json, computational_work.json)
   - Re-executes the code internally
   - Compares its output with the claimed output
   - Calls a tool to record its attestation

4. **Attestation Storage**: The verification results are saved as `attestation.json`

5. **Fail-Fast**: If verification fails, the experiment stops immediately with detailed error reporting

## CSV Generation Strategy

### Principle: Structured Data to CSV

CSVs are generated from structured data received via tool calls, not by parsing LLM text responses.

### Implementation

1. **Analysis CSVs**: The `EnhancedAnalysisAgentMultiTool` provides numerical data via three tool calls. The agent's Python code formats this into CSVs.

2. **Statistical CSVs**: The `Statistical Planning + Execution Agent` provides aggregated results via tool calls. The agent's Python code creates:
   - `statistical_results.csv`: Summary statistics
   - `statistical_data.csv`: Aggregated numerical data

3. **Evidence CSV**: A deterministic Python module (not an LLM) reads all `evidence_quotes.json` files after completion and generates `evidence.csv` by extracting and formatting the evidence arrays.

### Benefits
- No output token limits (CSVs are generated from structured data)
- Consistent formatting (Python code controls CSV structure)
- Efficient processing (no string parsing needed)

## Error Handling and Recovery

### Tool Call Failures

1. **Retry Logic**: If a tool call fails (network, API error), retry up to 3 times with exponential backoff
2. **Partial Progress**: Save progress after each successful document analysis
3. **Resume Capability**: Can resume from last successful document

### Verification Failures

1. **Immediate Stop**: Fail fast when verification fails
2. **Detailed Reporting**: Generate comprehensive error report with:
   - Original code and output
   - Verifier's re-execution results
   - Discrepancy analysis
3. **Manual Review**: Flag for human inspection

### Schema Violations

1. **Validation**: Validate tool call responses against expected schema
2. **Graceful Degradation**: If non-critical fields are missing, log warning and continue
3. **Critical Failures**: If required fields are missing, stop and report

## Caching Strategy

### Content-Addressable Storage

All artifacts use SHA-256 hashing for identification, enabling:
- Deduplication of identical analyses
- Efficient caching of results
- Complete provenance tracking

### Cache Levels

1. **Document Analysis Cache**: Cache `analysis.json` and `work.json` by document hash
2. **Verification Cache**: Cache `attestation.json` by work hash
3. **Statistical Cache**: Cache statistical results by input data hash

### Cache Invalidation

- Analysis changes invalidate downstream caches
- Framework changes invalidate all caches
- Manual cache clearing available via CLI

## Agent Responsibilities

### EnhancedAnalysisAgentMultiTool (Modified)
- **Input**: Single document + framework
- **Processing**: Score dimensions, calculate derived metrics (per-document) with internal three-phase analysis
- **Tool Calls**: `record_analysis_scores`, `record_evidence_quotes`, `record_computational_work`
- **Output**: `analysis_scores.json` + `evidence_quotes.json` + `computational_work.json`

### VerificationAgent (New)
- **Input**: `analysis_scores.json` + `evidence_quotes.json` + `computational_work.json`
- **Processing**: Re-execute code, verify results
- **Tool Calls**: `record_attestation`
- **Output**: `attestation.json`

### Statistical Planning + Execution Agent (New)
- **Input**: All `analysis_scores.json` files (numerical data only, no evidence)
- **Processing**: Generate plan, execute statistical analysis
- **Tool Calls**: `record_statistical_results`
- **Output**: `statistics.json` + `statistical_work.json` + CSVs

### Statistical Verification Agent (New)
- **Input**: `statistics.json` + `statistical_work.json`
- **Processing**: Re-execute statistical code, verify results
- **Tool Calls**: `record_statistical_attestation`
- **Output**: `statistical_attestation.json`

### Evidence CSV Export Module (Deterministic)
- **Input**: All `evidence_quotes.json` files (including evidence)
- **Processing**: Extract and format evidence arrays
- **Output**: `evidence.csv`
- **Note**: This is Python code, not an LLM agent

## Example Flow

### Per-Document Processing (Map Phase)

```python
# Orchestrator's per-document loop
for document in corpus:
    # 1. Analysis with derived metrics
    analysis_result = enhanced_analysis_agent_multi_tool.analyze(document, framework)
    # Agent internally calls LLM which uses three tools to save:
    # - analysis_scores.json (dimensional scores with confidence/salience)
    # - evidence_quotes.json (evidence quotes and reasoning)
    # - computational_work.json (derived metrics and code execution)
    
    # 2. Verification
    verification = verification_agent.verify(
        analysis_result['analysis_scores_path'],
        analysis_result['evidence_quotes_path'],
        analysis_result['computational_work_path']
    )
    # Agent internally calls LLM which uses tool to save:
    # - attestation.json
    
    if not verification['success']:
        raise VerificationError(verification['details'])
```

### Batch Processing (Reduce Phase)

```python
# After all documents are processed
# 3. Statistical Analysis (single batch call)
analysis_scores_paths = [r['analysis_scores_path'] for r in all_results]
statistical_result = statistical_agent.analyze_batch(analysis_scores_paths, hypotheses)
# Agent internally calls LLM which uses tool to save:
# - statistics.json
# - statistical_work.json
# - statistical_data.csv

# 4. Statistical Verification
stat_verification = statistical_verification_agent.verify(
    statistical_result['statistics_path'],
    statistical_result['work_path']
)

if not stat_verification['success']:
    raise StatisticalVerificationError(stat_verification['details'])

# 5. Evidence CSV (deterministic)
evidence_quotes_paths = [r['evidence_quotes_path'] for r in all_results]
evidence_csv_path = evidence_export_module.generate(evidence_quotes_paths)
```

## Phased Implementation Plan

### Phase 0: Foundation ✅
**Status**: COMPLETE
- Validated LLM internal code execution
- Confirmed multi-tool calling approach
- Established architecture principles
- Successfully tested with PDAF v10.0.2 and long documents (10,930 words)

**Test Results**:
- **Framework**: PDAF v10.0.2 (9 dimensions + derived metrics)
- **Document**: Trump speech (10,930 words)
- **Model**: Gemini 2.5 Pro
- **Token Usage**: 35,074 tokens ($0.13)
- **Tool Calls**: 3 successful calls
- **Artifacts**: 3 properly stored artifacts
- **Generated Data**: 9 dimensional scores, 9 evidence quotes, 8 derived metrics, Python code execution

### Phase 1: Enhanced Analysis with Verification
**Goal**: Implement per-document analysis with derived metrics and verification

**Implementation**:
1. Enhance `EnhancedAnalysisAgentMultiTool` to:
   - Calculate derived metrics per-document
   - Use multi-tool calling for structured output
   - Generate `analysis_scores.json`, `evidence_quotes.json`, and `computational_work.json`

2. Create `VerificationAgent`:
   - Use Gemini 2.5 Pro initially (same as primary)
   - Verify derived metrics calculations
   - Generate `attestation.json`

3. Update orchestrator for per-document loop

**Validation Gate**: 
- Run on 10-document test corpus
- All verifications must pass
- Performance metrics: <30s per document

### Phase 2: Statistical Analysis with Verification
**Goal**: Implement batch statistical processing

**Implementation**:
1. Create `Statistical Planning + Execution Agent`:
   - Process all numerical data in one batch
   - Generate statistical plan
   - Execute internally and output via tool calls

2. Create `Statistical Verification Agent`:
   - Verify statistical calculations
   - Use same model initially

3. Implement `Evidence CSV Export Module`:
   - Deterministic Python code
   - Extract evidence from all evidence_quotes.json files

**Validation Gate**:
- Run on 50-document corpus
- Statistical verification must pass
- CSV generation must complete

### Phase 3: Specialized Verifiers
**Goal**: Integrate math-specialized verification models

**Implementation**:
1. Integrate DeepSeek-Prover-V2 via OpenRouter:
   - Primary verifier for mathematical calculations
   - Enhanced proof checking

2. Integrate Llama-3.1-405B as secondary verifier:
   - Tie-breaking for disagreements
   - General verification backup

3. Implement disagreement resolution logic

**Validation Gate**:
- Run parallel verification comparison
- Document disagreement patterns
- Establish confidence thresholds

### Phase 4: Production Deployment
**Goal**: Full system with monitoring

**Implementation**:
1. Create `ShowYourWorkOrchestrator`:
   - Clean, simple implementation (~1200 lines)
   - Efficient artifact management
   - Progress tracking and resumability

2. Add comprehensive monitoring:
   - Verification success rates
   - Performance metrics
   - Cost tracking

3. Documentation and training

**Validation Gate**:
- Run on full 800+ document corpus
- All verifications pass
- Performance within budget

## Migration Strategy

### Existing Experiments
1. Provide migration script to convert existing artifacts
2. Re-run verification on historical results
3. Flag any that fail verification for review

### Feature Flags
```python
class FeatureFlags:
    ENABLE_SHOW_YOUR_WORK = os.getenv("ENABLE_SHOW_YOUR_WORK", "false").lower() == "true"
    ENABLE_VERIFICATION = os.getenv("ENABLE_VERIFICATION", "false").lower() == "true"
    VERIFICATION_FAIL_FAST = os.getenv("VERIFICATION_FAIL_FAST", "true").lower() == "true"
```

### Rollback Plan
1. Feature flags allow instant disable
2. Old orchestrator remains available
3. Can run experiments in parallel for comparison

## Performance Expectations

### Token Usage
- **Before**: 2M tokens for 50 documents
- **After**: 1.1M tokens (45% reduction via selective file passing)
- **Verification overhead**: +20% tokens for attestation

### Execution Time
- **Analysis**: 20-30s per document (with verification)
- **Statistical**: 60-90s for full batch
- **Total for 800 docs**: ~7 hours

### Cost Estimates
- **Phase 1 (Gemini only)**: $0.003 per document
- **Phase 2 (with DeepSeek)**: $0.005 per document
- **Full experiment (800 docs)**: ~$4.00

## Security Considerations

1. **Code Execution**: All code runs in LLM sandboxes, not locally
2. **Artifact Isolation**: Each experiment has isolated storage
3. **Verification Independence**: Verifiers cannot see each other's results
4. **Audit Trail**: Complete provenance for all calculations

## Success Metrics

1. **Verification Pass Rate**: >95% agreement between primary and verifier
2. **Performance**: <30s per document including verification
3. **Scalability**: Successfully process 800+ documents
4. **Reliability**: <1% failure rate due to parsing issues (should be 0% with tool calling)

## Conclusion

The Show Your Work architecture with tool calling provides:
- **Reliability**: No parsing brittleness
- **Verifiability**: Complete calculation provenance
- **Scalability**: Efficient context management
- **Simplicity**: Clean, maintainable code

This approach fundamentally solves the orchestration complexity problem while maintaining academic rigor through adversarial attestation.

## Tool API Contracts

Define explicit function-call contracts to eliminate ambiguity. All tools return no content; the agent persists inputs to artifacts.

### record_analysis_scores
- **Purpose**: Save per-document dimensional scores with confidence and salience
- **Arguments schema**:
```json
{
  "type": "object",
  "properties": {
    "document_id": {"type": "string"},
    "framework_name": {"type": "string"},
    "framework_version": {"type": "string"},
    "scores": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "raw_score": {"type": "number"},
          "salience": {"type": "number"},
          "confidence": {"type": "number"}
        },
        "required": ["raw_score", "salience", "confidence"]
      }
    }
  },
  "required": ["document_id", "framework_name", "framework_version", "scores"]
}
```

### record_evidence_quotes
- **Purpose**: Save per-document evidence quotes and reasoning
- **Arguments schema**:
```json
{
  "type": "object",
  "properties": {
    "document_id": {"type": "string"},
    "evidence": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "dimension": {"type": "string"},
          "quote": {"type": "string"},
          "reasoning": {"type": "string"}
        },
        "required": ["dimension", "quote", "reasoning"]
      }
    }
  },
  "required": ["document_id", "evidence"]
}
```

### record_computational_work
- **Purpose**: Save per-document derived metrics calculations and code execution
- **Arguments schema**:
```json
{
  "type": "object",
  "properties": {
    "document_id": {"type": "string"},
    "executed_code": {"type": "string"},
    "execution_output": {"type": "string"},
    "derived_metrics": {
      "type": "object",
      "additionalProperties": {"type": "number"}
    }
  },
  "required": ["document_id", "executed_code", "execution_output", "derived_metrics"]
}
```

### record_attestation
- **Purpose**: Save per-document verification attestation
- **Arguments schema**:
```json
{
  "type": "object",
  "properties": {
    "document_id": {"type": "string"},
    "success": {"type": "boolean"},
    "verifier_model": {"type": "string"},
    "verifier_model_version": {"type": "string"},
    "reasoning": {"type": "string"},
    "executed_code_digest_sha256": {"type": "string"},
    "analysis_digest_sha256": {"type": "string"},
    "re_execution_output": {"type": "string"}
  },
  "required": ["document_id", "success", "verifier_model", "reasoning"]
}
```

### record_statistical_results
- **Purpose**: Save batch statistical results and work
- **Arguments schema**:
```json
{
  "type": "object",
  "properties": {
    "statistics_payload": {
      "type": "object",
      "properties": {
        "tests": {
          "type": "array",
          "items": {
            "type": "object",
            "properties": {
              "name": {"type": "string"},
              "parameters": {"type": "object"},
              "metrics": {"type": "object"}  
            },
            "required": ["name", "metrics"]
          }
        },
        "aggregated_rows": {
          "type": "array",
          "items": {"type": "object"}
        }
      },
      "required": ["tests", "aggregated_rows"]
    },
    "executed_code": {"type": "string"},
    "execution_output": {"type": "string"}
  },
  "required": ["statistics_payload", "executed_code", "execution_output"]
}
```

### record_statistical_attestation
- **Purpose**: Save verification attestation for batch statistics
- **Arguments schema**:
```json
{
  "type": "object",
  "properties": {
    "success": {"type": "boolean"},
    "verifier_model": {"type": "string"},
    "verifier_model_version": {"type": "string"},
    "reasoning": {"type": "string"},
    "executed_code_digest_sha256": {"type": "string"},
    "statistics_digest_sha256": {"type": "string"}
  },
  "required": ["success", "verifier_model", "reasoning"]
}
```

## Artifact Naming and Layout

- **Run root**: `projects/<project>/runs/<timestamp>/`
- **Artifacts dir**: `artifacts/`
- **Per-document**:
  - `analysis_scores_<document_hash>.json`
  - `evidence_quotes_<document_hash>.json`
  - `computational_work_<document_hash>.json`
  - `attestation_<document_hash>.json`
- **Batch**:
  - `statistics.json`
  - `statistical_work.json`
  - `statistical_attestation.json`
  - `statistical_data.csv`
  - `evidence.csv`
- **Manifest**:
  - `manifests/input_manifest.json` (document list with file paths and SHA-256)

All files are also stored through `LocalArtifactStorage` with content-addressable SHA-256 IDs for deduplication and provenance.

## Safety and Determinism

- Instruct LLMs to use only Python with: numpy, pandas, scipy.stats, pingouin
- Require deterministic behavior: set seeds where relevant and avoid stochastic algorithms
- No external network or filesystem access; all data is provided via artifact paths
- The code provided in `work.json` is for attestation; no local execution by our system

## Concurrency and Backpressure

- Per-document analysis: process concurrently with a default max concurrency of 4 (configurable)
- Verification is performed per document immediately after analysis; same worker processes both sequentially to minimize I/O
- Statistical batch steps run single-shot (no concurrency)
- Budget guards: max tokens/min and cost thresholds abort with a clear error

## Audit Logging Fields

Each agent logs a structured audit entry per operation including:
- agent_name, model_name, model_version
- input_token_count, output_token_count, tool_call_count
- artifact_input_paths, artifact_output_paths
- input_artifact_hashes, output_artifact_hashes
- start_time_utc, end_time_utc, duration_ms
- cost_estimate_usd

## Configuration and Secrets

- Phase 2 requires `OPENROUTER_API_KEY` (OpenRouter integration); Phase 1 does not
- All LLM calls use explicit safety settings with BLOCK_NONE thresholds to prevent content refusals for political text
- Feature flags (env):
  - `ENABLE_SHOW_YOUR_WORK=true`
  - `ENABLE_VERIFICATION=true`
  - `VERIFICATION_FAIL_FAST=true`
