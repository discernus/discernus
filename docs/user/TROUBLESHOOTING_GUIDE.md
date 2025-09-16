# Troubleshooting Guide
*Strategic Debugging for THIN Architecture*

This guide provides strategic troubleshooting approaches for Discernus that **prevent agent drift** toward THICK solutions and maintain compliance with the three foundational commitments.

## Troubleshooting Philosophy

### Core Principle: "Debug the Orchestration, Not the Intelligence"

**THIN Troubleshooting** focuses on:
- **Infrastructure coordination** (routing, storage, execution)
- **Natural language flow** between components  
- **Academic reproducibility** and audit trails
- **Cost transparency** and resource monitoring

**THICK Anti-Pattern**: Debugging complex parsing logic, hardcoded intelligence, or mathematical operations in software.

### Success Metric
**"If debugging requires understanding LLM responses, you're debugging the wrong layer."** Focus on infrastructure reliability, not content analysis.

### Debugging Methodology: Examine Before Adding

**Core Principle**: Before adding debug output or print statements, examine existing code and logs first.

**Proper Debugging Sequence**:
1. **Check existing audit logs** for relevant agent events in `logs/agents.jsonl`
2. **Examine component implementation** to understand interface and return values
3. **Look for existing logging statements** and event types in the code
4. **Check orchestrator integration points** to see how components are called
5. **Only add debug output as last resort** if existing logging is insufficient

**Why This Matters**:
- **Eliminates redundant work** - Logging often already exists
- **Maintains code quality** - No temporary debug prints to clean up
- **Faster debugging** - Direct examination vs. adding new code
- **Better understanding** - Shows actual system flow, not just "is it called?"

**Anti-Pattern**: Immediately adding `print(f"DEBUG: ...")` statements without first checking existing logging infrastructure.

## Strategic Diagnostic Approaches

### 1. Agent Drift Detection

**Problem**: Agents write complex parsing logic instead of using LLM intelligence

**Diagnostic Patterns**:
- **Line Count Explosion**: Components exceed THIN budgets (>50 lines)
- **Import Proliferation**: regex, bs4, xml.etree, complex parsing libraries
- **Function Complexity**: Multiple if/elif statements, string manipulation
- **Hardcoded Intelligence**: Decision-making logic in infrastructure code

**Resolution Strategy**:
1. **Identify Intelligence**: What decisions is the code making?
2. **Extract to LLM**: Move intelligence to `agent_roles.py` prompts
3. **Simplify Infrastructure**: Reduce to basic routing and storage
4. **Test Natural Language**: Verify LLM-to-LLM communication

### 2. Mathematical Reliability Issues

**Problem**: LLMs performing calculations directly instead of hybrid intelligence pattern

**Diagnostic Patterns**:
- **Inconsistent Results**: Same inputs produce different numerical outputs
- **Opaque Calculations**: Mathematical operations without audit trails
- **Direct LLM Math**: Calculations in LLM responses instead of secure execution
- **Missing Reproducibility**: Cannot independently verify analytical results

**Resolution Strategy**:
1. **Implement Hybrid Pattern**: LLM designs → Code executes → LLM interprets
2. **Use Secure Execution**: Route calculations through `secure_code_executor.py`
3. **Complete Audit Trails**: Log all mathematical operations in chronolog
4. **Verify Independence**: Test reproducibility with independent researchers

### 3. Cost Transparency Problems

**Problem**: Unpredictable pricing or budget overruns

**Diagnostic Patterns**:
- **Budget Surprises**: Actual costs exceed upfront estimates
- **Model Selection Issues**: Suboptimal provider routing
- **Rate Limiting Failures**: API throttling without graceful degradation
- **Missing Cost Tracking**: No real-time budget monitoring

**Resolution Strategy**:
1. **Validate Model Registry**: Check provider selection algorithms
2. **Test Budget Controls**: Verify cost monitoring and alerts
3. **Optimize Routing**: Improve cost/capability trade-offs
4. **Enhance Estimation**: Calibrate upfront predictions with actual usage

### 4. Reproducibility Failures

**Problem**: Independent researchers cannot replicate results

**Diagnostic Patterns**:
- **Incomplete Provenance**: Missing audit trails or decision documentation
- **Non-Deterministic Outputs**: Different results from identical inputs
- **Opaque Methodology**: Unclear analytical processes
- **Missing Context**: Framework or corpus information not preserved

**Resolution Strategy**:
1. **Complete Chronolog**: Ensure all decisions logged with timestamps
2. **Cryptographic Integrity**: Implement tamper-evident record keeping
3. **Methodology Documentation**: Provide complete replication packages
4. **Independent Validation**: Test with external researchers

## Common Problem Patterns

### Infrastructure Coordination Issues

**Symptom**: Components don't communicate properly

**Diagnostic Questions**:
- Are messages routed through correct agent registry entries?
- Is the model registry selecting appropriate providers?
- Are session management and logging working correctly?
- Is the chronolog system capturing all events?

**Resolution Approach**:
1. **Test Infrastructure**: Run `simple_test.py` to validate core components
2. **Check Routing**: Verify agent discovery and message passing
3. **Validate Logging**: Ensure complete conversation capture
4. **Test Persistence**: Confirm Git integration and session management

### Natural Language Flow Breakdown

**Symptom**: LLMs produce unexpected or inconsistent outputs

**Diagnostic Questions**:
- Are prompts centralized in `agent_roles.py`?
- Is framework context properly injected?
- Are conversation histories preserved?
- Are handoff patterns working correctly?

**Resolution Approach**:
1. **Centralize Prompts**: Move hardcoded prompts to `agent_roles.py`
2. **Test Context**: Verify framework and conversation history injection
3. **Validate Handoffs**: Check natural language coordination patterns
4. **Monitor Quality**: Detect and prevent philosophical drift

### Academic Standards Violations

**Symptom**: Outputs not suitable for publication or peer review

**Diagnostic Questions**:
- Are analytical processes transparent and explainable?
- Can results be independently verified?
- Are cost estimates accurate for institutional budgets?
- Are provenance trails complete and tamper-evident?

**Resolution Approach**:
1. **Enhance Transparency**: Improve analytical process documentation
2. **Validate Reproducibility**: Test with independent researchers
3. **Calibrate Costs**: Align estimates with actual usage patterns
4. **Strengthen Provenance**: Ensure complete audit trails

## Domain-Specific Troubleshooting

### Framework Integration Issues

**Problem**: New analytical frameworks don't integrate properly

**Diagnostic Patterns**:
- Framework validation fails on valid specifications
- Agents don't apply framework criteria correctly
- Extension modules conflict with core platform
- Domain-specific assumptions hardcoded in software

**Resolution Strategy**:
1. **Test Framework Agnosticism**: Validate with multiple frameworks
2. **Check Extension Boundaries**: Ensure core/module separation
3. **Verify Domain Neutrality**: Test across different use cases
4. **Validate Integration**: Check framework loader and validation systems

### Multi-Model Orchestration Problems

**Problem**: Multiple LLM agents don't coordinate effectively

**Diagnostic Patterns**:
- Agents produce inconsistent or contradictory outputs
- Context loss across agent handoffs
- Adversarial review fails to identify issues
- Synthesis doesn't integrate perspectives properly

**Resolution Strategy**:
1. **Validate Agent Registry**: Check discovery and coordination patterns
2. **Test Context Preservation**: Ensure conversation history maintenance
3. **Improve Handoff Protocols**: Enhance natural language coordination
4. **Strengthen Synthesis**: Validate multi-perspective integration

### Performance and Scalability Issues

**Problem**: System doesn't handle large corpora or complex analyses

**Diagnostic Patterns**:
- Timeout errors during analysis
- Memory exhaustion with large texts
- Rate limiting from LLM providers
- Slow response times for complex frameworks

**Resolution Strategy**:
1. **Optimize Batch Processing**: Improve corpus handling efficiency
2. **Enhance Rate Limiting**: Implement intelligent throttling
3. **Improve Resource Management**: Optimize memory and processing
4. **Scale Architecture**: Design for institutional-level usage

## Escalation Protocols

### Architecture Violations

**When to Escalate**:
- Components exceed THIN line count budgets
- Complex parsing logic introduced
- Mathematical operations in software
- Domain-specific assumptions hardcoded

**Escalation Process**:
1. **Immediate Review**: Architecture compliance assessment
2. **Mandatory Refactoring**: Extract intelligence to LLMs
3. **Documentation Update**: Record lessons learned
4. **Prevention Measures**: Enhance agent drift detection

### Academic Standards Issues

**When to Escalate**:
- Reproducibility failures with independent researchers
- Cost estimates significantly exceed actual usage
- Provenance trails incomplete or compromised
- Peer review simulation fails

**Escalation Process**:
1. **Academic Review**: Independent researcher validation
2. **Methodology Audit**: Complete process documentation
3. **Standards Alignment**: Ensure publication readiness
4. **Quality Assurance**: Implement enhanced validation

### Critical System Failures

**When to Escalate**:
- Complete infrastructure breakdown
- Data integrity compromised
- Security vulnerabilities discovered
- Institutional adoption blockers

**Escalation Process**:
1. **Emergency Response**: Immediate system stabilization
2. **Root Cause Analysis**: Comprehensive failure investigation
3. **System Hardening**: Prevent similar failures
4. **Stakeholder Communication**: Transparent status reporting

## Prevention Strategies

### Agent Drift Prevention

**Proactive Measures**:
- **Complexity Budgets**: Enforce line count limits automatically
- **Code Review Standards**: Require THIN compliance validation
- **Testing Integration**: Fail builds on THICK patterns
- **Documentation Emphasis**: Make THIN patterns easier than THICK

**Early Warning Systems**:
- Monitor import patterns for parsing libraries
- Track function complexity metrics
- Alert on hardcoded prompt proliferation
- Validate domain-neutral language usage

### Quality Assurance

**Continuous Monitoring**:
- **Performance Metrics**: Track response times and resource usage
- **Cost Tracking**: Monitor budget adherence and estimation accuracy
- **Reproducibility Testing**: Regular validation with independent researchers
- **Academic Standards**: Ongoing peer review simulation

**Feedback Loops**:
- User experience feedback integration
- Academic community validation
- Institutional adoption metrics
- Extension ecosystem health monitoring

## Success Metrics and Validation

### Diagnostic Success Indicators

**Quantitative Measures**:
- Mean time to resolution: <2 hours for common issues
- Architecture compliance: 100% of components under line count budgets
- Reproducibility rate: >95% across independent runs
- Cost prediction accuracy: Within 10% of actual usage

**Qualitative Measures**:
- Troubleshooting feels like natural research workflow
- Error messages guide researchers toward solutions
- Architecture prevents issues automatically
- Academic standards maintained throughout

### Strategic Impact Assessment

**Platform Reliability**:
- Reduced debugging time for complex issues
- Increased confidence in analytical outputs
- Enhanced academic credibility and adoption
- Improved institutional integration success

**Ecosystem Health**:
- Faster onboarding for new contributors
- Reduced support burden for common issues
- Enhanced extension module compatibility
- Stronger community contribution patterns

---

*This guide emphasizes **strategic diagnosis** over technical implementation, maintaining THIN principles while ensuring robust, scalable, and academically rigorous troubleshooting approaches.* 