# Testing Documentation

## Overview

This directory contains testing documentation and methodologies for the Discernus project.

## Key Testing Methods

### 🚀 Fast Iteration Testing Methods
**[FAST_ITERATION_TESTING_METHODS.md](FAST_ITERATION_TESTING_METHODS.md)** - The canonical guide for rapid development iteration

**Core Principle**: Use the right testing method for the job to minimize cost and maximize speed.

1. **Mock Testing for Infrastructure** - Test code logic with simulated data (0 cost, instant feedback)
2. **Prompt Engineering Testing Harness** - Iterate on LLM prompts directly (minimal cost, fast iteration)
3. **Full Experiment Runs** - Reserve for integration testing and final validation (higher cost, comprehensive testing)

### 📋 Testing Checklist

- [ ] **Always start with mock testing** for infrastructure and logic issues
- [ ] **Use prompt engineering harness** for LLM response iteration
- [ ] **Reserve full experiments** for end-to-end validation
- [ ] **Test fast, iterate fast, fix fast**
- [ ] **Minimize API costs during development**

## Testing Philosophy

**"Test the infrastructure with mocks, test the prompts with harness, test the system with experiments."**

This approach prevents the costly "run and see" debugging cycle that wastes time and money.

## Related Documentation

- [CLI Best Practices](../../CLI_BEST_PRACTICES.md)
- [Troubleshooting Guide](../../troubleshooting/TROUBLESHOOTING_GUIDE.md)
- [Development Workflows](../../workflows/DEVELOPMENT_WORKFLOW.md)
