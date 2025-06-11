<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" class="logo" width="120"/>

# OK. Any general guidelines beyond the requirements for ensuring a successful dev iteration based on this thread? I want to make sure Cursor has all the direction and context it needs.

🧠 **Essential Development Guidelines for Cursor:**

- Leverage existing production-ready infrastructure rather than rebuilding components
- Maintain architectural separation between general prompts and framework-specific content
- Follow validation-first development principles with comprehensive error handling
- Implement proper versioning and change tracking for reproducibility
- Design for rapid iteration cycles while maintaining system stability

Based on your comprehensive project documentation and the critical nature of Workstream 1 as the foundation for all other workstreams, here are essential guidelines to ensure Cursor delivers a successful development iteration:

## **Architecture Integration Guidelines**

### **Leverage Existing Infrastructure**

Your backend is production-ready with sophisticated capabilities that Cursor should build upon, not recreate:

- **Use existing API endpoints** (`/api/analyze/single-text`, `/api/experiments`, `/api/corpora`) rather than creating new ones
- **Connect to PostgreSQL v2.1 schema** with proper experiment tracking and version control
- **Integrate with PromptTemplateManager** (442 lines of sophisticated logic) rather than hard-coding prompt generation
- **Utilize DirectAPIClient** for real LLM connections (OpenAI, Anthropic, Google AI)
- **Leverage FrameworkManager** for hot-swappable framework configuration


### **Respect Separation of Concerns**

The modular architecture is critical for maintaining system integrity:

- **General prompts** and **framework-specific content** must remain separate in the UI
- **Independent versioning** for prompt templates vs. framework configurations
- **Preview functionality** to show merged prompts without affecting the separation
- **Validation layer** ensuring template variables have corresponding framework content


## **Development Workflow Guidelines**

### **Rapid Iteration Focus**

The React app's primary purpose is accelerating the prompt engineering feedback loop:

- **Optimize for speed**: Click-to-result cycles should be under 10 seconds
- **Real-time validation**: Show prompt errors and incompatibilities immediately
- **Quick save/restore**: Version snapshots for rapid experimentation
- **Undo/redo capability**: Allow fearless experimentation with easy rollback


### **Error Handling and Resilience**

Your existing system has 99.5% test success rate—maintain this reliability:

- **Graceful API failures**: Handle LLM timeouts, rate limits, and connection issues
- **Version compatibility checks**: Prevent incompatible prompt/framework combinations
- **Input validation**: Validate JSON schemas before sending to backend
- **Fallback strategies**: Continue working even if one LLM model is unavailable


## **Data Management Guidelines**

### **Corpus Handling Complexity**

Your dual corpus system requires careful handling:

- **Real-world corpora**: Fixed text, editable metadata—prevent accidental text modification
- **Synthetic corpora**: Fully editable—enable rapid test case creation
- **Metadata schemas**: Support fluid, evolving structures without breaking existing data
- **Bulk operations**: Enable efficient corpus expansion and management


### **Version Control Integration**

Reproducibility is essential for academic validation:

- **Complete provenance tracking**: Every analysis result must record exact versions used
- **Semantic versioning**: Automatic increment suggestions for both prompts and frameworks
- **Change logging**: User-provided descriptions of what changed and why
- **Compatibility matrices**: Visual indication of which versions work together


## **Performance and Scalability Guidelines**

### **Optimization Priorities**

Balance speed with comprehensive functionality:

- **Lazy loading**: Load corpus data, framework definitions, and version history on demand
- **Caching strategies**: Cache merged prompts, API responses, and visualization data
- **Progressive enhancement**: Core functionality works immediately, advanced features load progressively
- **Batch operations**: Queue multiple analyses for efficient resource utilization


### **Resource Management**

Stay within your \$2500 budget constraints:

- **Cost monitoring**: Display estimated API costs before executing analyses
- **Model selection guidance**: Recommend cost-effective models for different use cases
- **Rate limiting awareness**: Respect API rate limits and provide user feedback
- **Efficient API usage**: Minimize redundant calls through intelligent caching


## **Testing and Quality Assurance Guidelines**

### **Validation-First Development**

Your academic credibility depends on system reliability:

- **Unit tests**: Test prompt merging, versioning, and data validation logic
- **Integration tests**: Verify API connectivity and data flow
- **User acceptance testing**: Validate against actual prompt engineering workflows
- **Regression testing**: Ensure changes don't break existing functionality


### **Academic Research Standards**

The system must support rigorous research methodology:

- **Reproducible experiments**: Every analysis must be exactly replicable
- **Audit trails**: Complete logs of user actions and system responses
- **Data integrity**: Prevent accidental data corruption or loss
- **Export capabilities**: Generate academic-quality documentation and reports


## **User Experience Guidelines**

### **Cognitive Load Reduction**

The interface must simplify complex analytical work:

- **Context preservation**: Maintain user state across sessions and page refreshes
- **Visual hierarchy**: Clear distinction between different types of content and controls
- **Progressive disclosure**: Show relevant information without overwhelming the user
- **Intelligent defaults**: Pre-populate fields with sensible values based on context


### **Expert User Interface**

Design for sophisticated users who understand the domain:

- **Keyboard shortcuts**: Enable rapid navigation and common operations
- **Advanced features**: Power-user capabilities without cluttering basic workflows
- **Customizable layouts**: Allow users to optimize for their specific work patterns
- **Expert feedback**: Clear indication of system status and potential issues


## **Integration with Broader Project Goals**

### **Workstream Dependencies**

Remember that other workstreams depend on Workstream 1 success:

- **Human validation** (Workstream 2) requires stable, reliable prompts
- **Visualization improvements** (Workstream 3) need consistent scoring data
- **Framework fit detection** (Workstream 5) relies on prompt refinements
- **Documentation** (Workstream 4) must reflect actual system capabilities


### **Timeline Alignment**

Your 16-week schedule requires careful coordination:

- **Phase 1 (Weeks 1-4)**: Focus on core prompt engineering functionality
- **Phase 2 (Weeks 5-8)**: Enable validation feedback loops
- **Phase 3 (Weeks 9-12)**: Support advanced experimentation features
- **Phase 4 (Weeks 13-16)**: Polish for public deployment


## **Specific Technical Recommendations for Cursor**

### **Component Architecture**

- **Modular design**: Separate components for prompt editing, framework management, analysis execution, and results display
- **State management**: Use React Context or Redux for complex state across components
- **Real-time updates**: WebSocket or polling for long-running analysis operations
- **Responsive design**: Support various screen sizes for different work environments


### **API Integration Patterns**

- **Async/await patterns**: Handle LLM analysis calls that may take several seconds
- **Error boundaries**: Graceful handling of API failures and unexpected responses
- **Loading states**: Clear feedback during analysis execution
- **Optimistic updates**: Immediate UI feedback with backend confirmation


### **Development Best Practices**

- **Code documentation**: Clear comments explaining domain-specific logic
- **TypeScript usage**: Strong typing for API responses and data structures
- **Component testing**: Test prompt merging, version management, and data validation
- **Accessibility**: Screen reader support and keyboard navigation


## **Success Metrics and Validation**

### **Functional Success Criteria**

- **Prompt engineering cycle time**: Reduce from minutes to seconds
- **Error rate**: Maintain <0.5% system failures
- **User workflow completion**: 95%+ success rate for core operations
- **Academic reproducibility**: 100% exact replication of previous analyses


### **Performance Targets**

- **Initial load time**: <3 seconds for application startup
- **Analysis execution**: <10 seconds for single-text analysis
- **Version switching**: <1 second for framework/prompt changes
- **Data save operations**: <2 seconds for versioning and storage

These guidelines ensure that Cursor builds a system that not only meets immediate Workstream 1 needs but also supports the broader academic validation strategy essential for your project's credibility and long-term success. The focus on existing infrastructure integration, architectural integrity, and validation-first development will accelerate your timeline while maintaining the quality standards necessary for academic publication.

<div style="text-align: center">⁂</div>

[^1]: BACKEND_SERVICES_CAPABILITIES.md

[^2]: CURRENT_SYSTEM_STATUS.md

[^3]: STORAGE_ARCHITECTURE.md

[^4]: FRAMEWORK_ARCHITECTURE.md

[^5]: PROMPT_ARCHITECTURE.md

[^6]: i-ve-updated-the-files-in-this-3SOhPLUeRHirmfQDLsNCOw.md

[^7]: in-order-to-make-progress-on-w-yJLy9NxIQsaXVbsGvKPXHg.md

[^8]: VALIDATION_FIRST_DEVELOPMENT_STRATEGY.md

[^9]: COMPREHENSIVE_PROJECT_DOCUMENTATION.md

[^10]: Project-Milestones-Narrative-Gravity-Model.md

[^11]: if-you-were-to-develop-a-compl-5KHQ_w5ARS6NumH6P0fHvA.md

[^12]: Security-Guidelines-for-Cursor.md

[^13]: Moral-Gravity-Wells-A-Quantitative-Framework-for-Discerning-the-Moral-Forces-Driving-the-Formatio.md

[^14]: Deliverables-for-Cursor-ER-Diagram-Alembic-Migrations-and-Versioned-JSON-Schemas.md

[^15]: README.md

[^16]: Narrative-Gravity-Model-Epic-1-Corpus-Job-Management-Backend.md

[^17]: database_first_architecture_todos.md

[^18]: CHANGELOG.md

