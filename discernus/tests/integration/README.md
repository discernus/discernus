# Integration Tests

This directory contains comprehensive integration tests for the Discernus pipeline using real LLMs.

## Nano and Micro Integration Tests

### Overview

The nano and micro integration tests provide comprehensive validation of the complete Discernus pipeline using real LLMs. These tests are designed to catch real-world issues that mock-based tests miss.

### Test Strategy

**Clean Slate Approach**: Each test starts with a completely clean experiment directory by removing all run artifacts (runs/, session/, shared_cache/, logs/, temp_derived_metrics/).

**Real LLM Testing**: Uses Gemini 2.5 Flash Lite for all stages (analysis, calculation, synthesis) to provide real-world validation while keeping costs minimal.

**Complete Pipeline Validation**: Tests the entire pipeline from corpus ingestion to final report generation.

### Test Experiments

#### Nano Test Experiment
- **Purpose**: Basic pipeline validation
- **Documents**: 2 (1 positive, 1 negative sentiment)
- **Dimensions**: 2 (positive_sentiment, negative_sentiment)
- **Derived Metrics**: None
- **Statistical Analysis**: Basic descriptive statistics only
- **Expected Duration**: 2-3 minutes
- **Expected Cost**: ~$0.001

#### Micro Test Experiment
- **Purpose**: Complete pipeline validation with statistical analysis
- **Documents**: 4 (2 positive, 2 negative sentiment)
- **Dimensions**: 2 (positive_sentiment, negative_sentiment)
- **Derived Metrics**: 2 (net_sentiment, sentiment_magnitude)
- **Statistical Analysis**: Descriptive statistics + ANOVA
- **Expected Duration**: 3-5 minutes
- **Expected Cost**: ~$0.002

### Running the Tests

#### Prerequisites

1. **Environment Setup**:
   ```bash
   # Activate virtual environment
   source venv/bin/activate
   
   # Set required environment variables
   export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/service-account.json"
   ```

2. **Verify Setup**:
   ```bash
   # Check if environment is ready
   python3 -c "from discernus.tests import print_test_environment; print_test_environment()"
   ```

#### Running Tests

**Option 1: Using the test runner (recommended)**:
```bash
cd discernus/tests/integration
python3 run_nano_micro_tests.py
```

**Option 2: Using unittest directly**:
```bash
cd discernus/tests/integration
python3 -m unittest test_nano_micro_integration -v
```

**Option 3: From project root**:
```bash
python3 -m unittest discernus.tests.integration.test_nano_micro_integration -v
```

### Test Validation

The tests validate:

#### Analysis Phase
- ✅ Correct number of documents processed
- ✅ Valid dimensional score structure
- ✅ Score ranges (0.0-1.0)
- ✅ Evidence extraction
- ✅ Sentiment classification accuracy

#### Derived Metrics Phase
- ✅ Correct calculation of derived metrics (micro only)
- ✅ Valid metric values
- ✅ Proper data structure

#### Statistical Analysis Phase
- ✅ Descriptive statistics for all dimensions
- ✅ ANOVA results (micro only)
- ✅ Group statistics
- ✅ Valid statistical values

#### Synthesis Phase
- ✅ Complete report generation
- ✅ Evidence integration
- ✅ Statistical findings inclusion
- ✅ Report quality and coherence

### Cost and Performance

| Test | Duration | Cost | Purpose |
|------|----------|------|---------|
| Nano | 2-3 min | ~$0.001 | Basic pipeline validation |
| Micro | 3-5 min | ~$0.002 | Complete pipeline validation |
| Full Suite | 5-8 min | ~$0.003 | Comprehensive validation |

**Cost is negligible** - less than half a penny for the complete test suite.

### Troubleshooting

#### Common Issues

**Environment Variables Missing**:
```
❌ Missing required environment variables:
   - GOOGLE_APPLICATION_CREDENTIALS
```
**Solution**: Set the required environment variables before running tests.

**Import Errors**:
```
❌ Import error: No module named 'discernus'
```
**Solution**: Make sure you're running from the project root with the virtual environment activated.

**API Errors**:
```
❌ Experiment failed with CleanAnalysisError: API quota exceeded
```
**Solution**: Check your Google Cloud API quotas and billing.

#### Debug Mode

For detailed debugging, you can run individual test methods:

```bash
# Run only nano test
python3 -m unittest discernus.tests.integration.test_nano_micro_integration.TestNanoMicroIntegration.test_nano_experiment_integration -v

# Run only micro test
python3 -m unittest discernus.tests.integration.test_nano_micro_integration.TestNanoMicroIntegration.test_micro_experiment_integration -v
```

### Test Architecture

The integration tests follow these principles:

1. **Real LLM Testing**: Uses actual LLMs to catch prompt and response issues
2. **Clean Slate**: Each test starts fresh to avoid interference
3. **Comprehensive Validation**: Tests all pipeline phases with detailed assertions
4. **Cost Effective**: Uses the most cost-effective model for validation
5. **Clear Failure Modes**: Provides detailed error messages when tests fail

### Integration with CI/CD

These tests can be integrated into CI/CD pipelines:

```yaml
# Example GitHub Actions workflow
- name: Run Integration Tests
  run: |
    source venv/bin/activate
    cd discernus/tests/integration
    python3 run_nano_micro_tests.py
  env:
    GOOGLE_APPLICATION_CREDENTIALS: ${{ secrets.GOOGLE_APPLICATION_CREDENTIALS }}
```

### Maintenance

When updating the pipeline:

1. **Run tests after changes** to ensure no regressions
2. **Update test assertions** if pipeline output format changes
3. **Add new test cases** for new features
4. **Monitor test costs** to ensure they remain negligible

The tests are designed to be stable and reliable, providing confidence that the pipeline works correctly with real LLMs.
