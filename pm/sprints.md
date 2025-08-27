# Discernus v10 Sprints

**Purpose**: Organized backlog with sprint planning, dependencies, and detailed item specifications.

**Usage**: 
- "groom our sprints" → organize inbox items into proper sprint structure
- Items moved here from inbox.md during grooming sessions

---

## Current Status

**Date**: 2025-01-27
**Status**: Testing Infrastructure Fix Required - CLI v10 Compliance Complete
**Next Priority**: Fix integration test infrastructure to unblock validation

**CLI v10 Compliance**: ✅ **COMPLETE**
**Statistical Analysis Pipeline**: ✅ **COMPLETE**
**Framework Validation**: ✅ **COMPLETE**
**Current Blocker**: Integration tests failing due to incorrect mocking

---

## Current Sprint Planning

### Sprint 1: Critical Infrastructure & Quality Assurance (IMMEDIATE)

**Timeline**: 1-2 days
**Goal**: Fix critical system issues and establish testing foundation

#### [CRITICAL-001] Fix Graceful Degradation in Derived Metrics Phase ✅ **COMPLETED**

- **Description**: **CRITICAL BUG**: Derived metrics phase failures are being silently caught and the experiment continues with degraded results instead of failing fast
- **Dependencies**: None (blocking everything)
- **Root Cause**: Lines 197-201 in CleanAnalysisOrchestrator catch derived metrics failures and continue with `{"error": str(e), "status": "failed"}` instead of propagating the error
- **Evidence**: Terminal shows "Derived metrics phase failed, attempting to continue: Derived metrics functions file not found" but experiment completes successfully
- **Impact**: 
  - Masks critical LLM generation failures
  - Produces unreliable experiment results
  - Violates THIN architecture fail-fast principles
  - Makes debugging extremely difficult
- **Acceptance Criteria**:
  - [x] Derived metrics phase failures cause immediate experiment termination
  - [x] Clear error messages indicate the specific failure point
  - [x] No graceful degradation for critical pipeline components
  - [x] Statistical analysis phase depends on derived metrics and should also fail if derived metrics fail
- **Effort**: 1-2 hours ✅ **COMPLETED**
- **Priority**: **CRITICAL** (data integrity issue)
- **Status**: ✅ **VERIFIED COMPLETE** - All acceptance criteria met, fail-fast behavior properly implemented

#### [CRITICAL-002] Fix Derived Metrics Cache Stale File References

- **Description**: **CRITICAL BUG**: Cached derived metrics functions reference temporary file paths that get cleaned up, causing "functions file not found" errors on cache hits
- **Dependencies**: [CRITICAL-001]
- **Root Cause**: Cache stores function metadata pointing to temporary workspace files, but temporary directories are cleaned up after each run (lines 769-772)
- **Evidence**: Cache hit shows "💾 Using cached derived metrics functions" but then fails with "Derived metrics functions file not found"
- **Solution**: Store actual function code content in cache, recreate function files from cached content when cache hit occurs
- **Impact**:
  - Cache hits cause experiment failures instead of performance improvements
  - Violates caching reliability principles
  - Makes development velocity worse instead of better
- **Acceptance Criteria**:
  - [ ] Cache stores actual function code content, not just metadata
  - [ ] Cache hits recreate function files from stored content
  - [ ] Both derived metrics and statistical analysis caches fixed
  - [ ] Workspace cleanup doesn't break cached functions
- **Effort**: 1 hour
- **Priority**: **CRITICAL** - Blocking caching benefits
- **Status**: **NEEDS VERIFICATION** - Implementation exists but cache content storage needs testing

#### [PERF-001] Implement Validation Caching

- **Description**: Implement caching for experiment coherence validation to eliminate redundant validation when input assets haven't changed
- **Dependencies**: [CRITICAL-002]
- **Root Cause**: Validation runs every time even when framework, experiment, and corpus haven't changed, causing unnecessary LLM calls and delays
- **Solution**: Cache validation results based on content hashes of framework, experiment, corpus, and model
- **Impact**:
  - Eliminates 20-30 second validation delays on repeated runs
  - Reduces LLM API costs for development iterations
  - Maintains same validation quality and error detection
- **Acceptance Criteria**:
  - [ ] ValidationCacheManager created with deterministic cache keys
  - [ ] Cache key based on framework + experiment + corpus + model content
  - [ ] Validation results cached with success/failure status and issues
  - [ ] Cache hits skip validation and use stored results
  - [ ] Failed validations properly cached and re-raise errors
  - [ ] Unit tests cover all caching scenarios
  - [ ] Integration with CleanAnalysisOrchestrator performance metrics
- **Effort**: 2 hours
- **Priority**: **HIGH** - Significant development velocity improvement
- **Status**: **NEEDS VERIFICATION** - Implementation exists but caching behavior needs testing

#### [TEST-INFRA] Fix Integration Test Infrastructure

- **Description**: Integration tests incorrectly mock critical setup, causing false failures
- **Impact**: False test failures prevent validation of all features
- **Root Cause**: Tests mock `_initialize_infrastructure` which bypasses `artifact_storage` setup
- **Acceptance Criteria**:
  - [ ] Integration tests run without infrastructure errors
  - [ ] Tests accurately reflect actual system status
  - [ ] False failures are eliminated
  - [ ] Real issues (if any) are identified
- **Effort**: 1-2 hours
- **Priority**: **HIGHEST** - Blocking everything

#### [QUALITY-001] Fix Fact-Checker False Positive on Evidence Citations

- **Description**: Fact-checker incorrectly flags legitimate evidence attribution `(Source: filename.txt)` as "Citation Violation"
- **Impact**: 
  - False positives on correct evidence citations
  - Revision agent asked to "fix" legitimate provenance tracking
  - Undermines evidence attribution which is required for academic integrity
- **Root Cause**: Citation Violation rubric is too broad, catching internal evidence references
- **Solution**: Refine rubric to distinguish between external academic citations and internal evidence attribution
- **Acceptance Criteria**:
  - [ ] `(Source: filename.txt)` format is NOT flagged as citation violation
  - [ ] External academic citations like `(Author, Year)` are still flagged
  - [ ] Rubric clearly distinguishes evidence attribution from academic citations
  - [ ] False positive rate on evidence citations is zero
- **Effort**: 30 minutes
- **Priority**: **HIGH** - Affects report quality and revision agent effectiveness
- **Status**: **NEEDS VERIFICATION** - Implementation exists but behavior needs testing
