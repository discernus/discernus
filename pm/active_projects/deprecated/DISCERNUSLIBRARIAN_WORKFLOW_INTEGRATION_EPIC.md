# EPIC: DiscernusLibrarian → WorkflowOrchestrator Integration

**Priority**: Medium (Future Enhancement)  
**Status**: Backlog - Current DiscernusLibrarian working well for framework weight research  
**Goal**: Enable meta-research intelligence and complex research workflows while maintaining current research capabilities

---

## 🎯 **Strategic Context**

Current DiscernusLibrarian successfully executing framework weight validation research:
- ✅ **A1 Relational Dynamics**: Completed with western democracy scope fix  
- ✅ **SE1 Campaign Effectiveness**: Completed with strategic effectiveness validation
- ✅ **Iterative Adversarial Research**: Manual Blue Team analysis improving research quality

**Integration Goal**: Enable automated **meta-research intelligence** where Research Director agent redesigns research strategies based on Red/Blue Team conflicts until convergence.

---

## 🔄 **Meta-Research Vision**

Enable this automated research intelligence cycle:
```
Research Director: "Given question X, approach A failed due to conflicts Y+Z. 
                   Let me design approach B with different methodology."
                   ↓
Execute New Research Plan → Red/Blue Analysis → Convergence Assessment → 
                   ↓
Director: "Approach B better but still conflicts. Try approach C..."
                   ↓  
Continue until: Research conflicts resolved OR maximum learning extracted
```

---

## 📋 **Epic Breakdown**

### **Phase 1: Infrastructure Preparation** (Foundation)
- [ ] **Issue #1**: Create Research Agent Base Classes
  - Extract LiteratureDiscoveryAgent from DiscernusLibrarian Phases 0-2
  - Extract RedTeamCritiqueAgent from DiscernusLibrarian Phase 4  
  - Extract SynthesisAgent from DiscernusLibrarian Phase 3
  - All agents implement WorkflowOrchestrator interface

- [ ] **Issue #2**: Add Research Agents to Agent Registry
  - Define agent registry entries for literature research agents
  - Test dynamic agent loading via WorkflowOrchestrator
  - Ensure compatibility with existing LLM Gateway + Model Registry

### **Phase 2: Core Meta-Research Agents** (Intelligence Layer)
- [ ] **Issue #3**: Implement ResearchDirectorAgent (Key Innovation)
  - Strategic memory across research iterations
  - Research strategy redesign based on failure patterns  
  - Convergence assessment with continuation/termination logic
  - Integration with existing research history storage

- [ ] **Issue #4**: Implement BlueTeamCounterAgent
  - Systematic counterpoint analysis against Red Team critiques
  - Evidence-based defense of research findings
  - Integration with adversarial research workflow

- [ ] **Issue #5**: Implement ConvergenceAssessmentAgent
  - Research quality assessment across Red/Blue analysis
  - Convergence criteria evaluation
  - Strategic learning extraction from research conflicts

### **Phase 3: Workflow Integration** (Orchestration)
- [ ] **Issue #6**: Design Meta-Research Workflow Definitions
  - YAML workflow definitions for iterative adversarial research
  - Looping logic with Research Director coordination
  - State management for multi-iteration research cycles

- [ ] **Issue #7**: Enhanced Session Management  
  - Research provenance across multiple iterations
  - Strategic decision audit trails
  - Academic-quality research documentation

### **Phase 4: Advanced Capabilities** (Enhancement)
- [ ] **Issue #8**: Redis Integration for Long-Running Research
  - Async coordination for complex research cycles
  - Resource management across multi-hour research sessions
  - Real-time monitoring and intervention capabilities

- [ ] **Issue #9**: Research Portfolio Management
  - Parallel execution of multiple research questions (A1, SE1, A2...)
  - Cross-question synthesis opportunities
  - Resource optimization across research portfolio

### **Phase 5: Migration & Compatibility** (Transition)
- [ ] **Issue #10**: Maintain Simple Research Interface
  - DiscernusLibrarian wrapper for basic literature reviews
  - Backward compatibility for current research patterns
  - Clear upgrade path for users wanting meta-research

- [ ] **Issue #11**: Research Workflow Templates
  - Pre-built workflows for common research patterns
  - Framework weight validation template
  - Academic literature review template
  - Meta-analysis research template

---

## 🎯 **Success Criteria**

### **Functional Requirements**
- ✅ **Meta-Research Intelligence**: Research Director automatically redesigns failed research strategies
- ✅ **Iterative Adversarial Research**: Automated Red/Blue cycles until convergence  
- ✅ **Research Portfolio Management**: Execute multiple research questions simultaneously
- ✅ **Academic Provenance**: Complete audit trails for complex research workflows
- ✅ **Simple Interface Maintained**: Current DiscernusLibrarian usage patterns preserved

### **Technical Requirements**  
- ✅ **Agent Registry Integration**: All research agents discoverable via standard registry
- ✅ **State Management**: Research history preserved across iterations and sessions
- ✅ **Resource Management**: Intelligent API rate limit handling across complex workflows
- ✅ **THIN Architecture**: Zero intelligence in orchestration, all intelligence in agents

### **Quality Gates**
- ✅ **Research Quality**: Meta-research produces equal/better results than current approach
- ✅ **Usability**: Simple research remains as easy as current DiscernusLibrarian
- ✅ **Performance**: Complex research workflows complete within reasonable time/cost
- ✅ **Reliability**: Fault tolerance and recovery for long-running research sessions

---

## 🚀 **Implementation Strategy**

### **Incremental Approach**
1. **Phase 1-2**: Can be implemented without disrupting current DiscernusLibrarian
2. **Phase 3**: WorkflowOrchestrator gains research capabilities alongside current features  
3. **Phase 4-5**: Advanced features and migration support

### **Risk Mitigation**
- Maintain current DiscernusLibrarian throughout implementation
- Each phase adds capability without breaking existing functionality
- Clear rollback strategy if integration introduces complexity

### **Timeline Estimate**
- **Phase 1-2**: 2-3 weeks (foundation + core agents)
- **Phase 3-4**: 2-3 weeks (workflow integration + advanced features)  
- **Phase 5**: 1 week (compatibility + templates)
- **Total**: ~6-8 weeks when ready to tackle

---

## 📊 **Current vs Future Comparison**

### **Current DiscernusLibrarian (Working Well)**
- ✅ Simple 5-phase sequential research
- ✅ Single research question focus  
- ✅ Manual iterative adversarial research (Blue Team counterpoint)
- ✅ Direct execution with immediate results

### **Future Integrated System (Epic Goal)**  
- ✅ **All current capabilities preserved**
- 🚀 Automated meta-research intelligence with strategy redesign
- 🚀 Research Director coordination across multiple research iterations
- 🚀 Parallel research portfolio execution (A1 + SE1 + A2 simultaneously)
- 🚀 Long-running research sessions with Redis coordination
- 🚀 Academic-quality research provenance and collaboration

---

**Ready When You Are**: This epic provides complete roadmap for integration while maintaining current research momentum. Framework weight validation research can continue uninterrupted with current DiscernusLibrarian approach.

---

## 📝 **Next Steps**

1. **Continue Current Research**: Framework weight validation with existing DiscernusLibrarian
2. **Monitor Research Needs**: Assess when meta-research intelligence becomes necessary
3. **Scope Phase 1**: When ready, start with Research Agent extraction (non-disruptive)
4. **Evaluate Integration**: Test WorkflowOrchestrator research capabilities before full migration 