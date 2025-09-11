# Dependency Cleanup Plan

**Date**: 2025-01-11  
**Current Status**: 50% dependency bloat (15 used / 30 declared)  
**Goal**: Remove unused dependencies to improve security, maintenance, and build times  

## Analysis Results

### ✅ KEEP - Actually Used Dependencies (15)
```
python-dotenv    # Environment variable loading
gitpython        # Git operations (used in CLI/provenance)
litellm          # LLM gateway abstraction
requests         # HTTP client
click            # CLI framework
rich             # Terminal formatting
pandas           # Data processing
numpy            # Numerical computing
scipy            # Scientific computing
PyYAML           # Configuration files
pydantic         # Data validation
pydantic-settings # Configuration management
txtai            # RAG/search engine
typesense        # Search backend
rank_bm25        # Search ranking
loguru           # Logging
ratelimit        # Rate limiting
```

### 🗑️ REMOVE - Unused Dependencies (13)

#### High Confidence Removals:
```
anthropic              # Not used (LiteLLM handles Anthropic)
google-cloud-aiplatform # Not used (LiteLLM handles Vertex AI)
google-auth            # Not used (no direct Google Cloud usage)
youtube-transcript-api # Corpus collection only, not core platform
yt-dlp                 # Corpus collection only, not core platform
jupyter                # Development/analysis only, not runtime
nbformat               # Jupyter notebook support, not used
plotly                 # Visualization, not used in core
nltk                   # NLP toolkit, not used
textblob               # NLP library, not used
scikit-learn           # ML library, not used in core
```

#### Moderate Confidence Removals:
```
statsmodels           # Statistical analysis (may be used in synthesis)
pingouin              # Statistical analysis (may be used in synthesis)
```

### 🔍 INVESTIGATE - Need Deeper Analysis (2)

These might be used indirectly or in specific modes:
- **statsmodels**: Check if used in statistical synthesis
- **pingouin**: Check if used in statistical analysis

## Implementation Plan

### Phase 1: Safe Removals (High Confidence)
Remove dependencies that are clearly unused:
```toml
# REMOVE these from pyproject.toml dependencies:
"anthropic>=0.7.0",
"google-cloud-aiplatform>=1.104.0", 
"google-auth>=2.40.0",
"youtube-transcript-api>=0.6.2",
"yt-dlp>=2025.6.9",
"jupyter>=1.0.0",
"nbformat>=5.7.0", 
"plotly>=5.14.0",
"nltk>=3.8",
"textblob>=0.15.3",
"scikit-learn>=1.2.0",
```

### Phase 2: Statistical Package Analysis
Investigate statistical packages:
1. Search for `statsmodels` and `pingouin` usage
2. Test statistical synthesis without these packages
3. Move to optional dependencies if needed

### Phase 3: Optional Dependencies Reorganization
Move corpus collection tools to optional dependencies:
```toml
[project.optional-dependencies]
corpus = [
    "youtube-transcript-api>=0.6.2",
    "yt-dlp>=2025.6.9",
]

analysis = [
    "jupyter>=1.0.0",
    "nbformat>=5.7.0",
    "plotly>=5.14.0",
]

nlp = [
    "nltk>=3.8", 
    "textblob>=0.15.3",
]

ml = [
    "scikit-learn>=1.2.0",
    "statsmodels>=0.14.0",
    "pingouin>=0.5",
]
```

## Benefits

### 🚀 Performance Improvements
- **Faster installs**: ~40% fewer packages to download/compile
- **Smaller Docker images**: Reduced attack surface
- **Faster CI/CD**: Quicker dependency resolution

### 🔒 Security Benefits  
- **Reduced attack surface**: Fewer dependencies = fewer vulnerabilities
- **Easier auditing**: Smaller dependency tree to monitor
- **Clear separation**: Core vs optional functionality

### 🛠️ Maintenance Benefits
- **Clearer dependencies**: Only what's actually needed
- **Easier updates**: Fewer packages to track for security updates
- **Better documentation**: Clear separation of required vs optional

## Risk Assessment

### ✅ Low Risk Removals
All high-confidence removals are safe because:
- LiteLLM abstracts away direct provider SDKs
- Corpus tools are development-time only
- Analysis tools are optional for core functionality

### ⚠️ Medium Risk (Statistical Packages)
Need to verify statistical synthesis doesn't break:
- Test synthesis agent without statsmodels/pingouin
- Check if calculations are done in pandas/numpy instead

## Validation Plan

1. **Remove high-confidence dependencies**
2. **Run full test suite** 
3. **Test core workflows** (analysis + synthesis)
4. **Test statistical preparation mode**
5. **Verify no import errors**

## Expected Outcome

- **Dependencies**: 30 → 17 (43% reduction)
- **Install time**: Significantly faster
- **Security posture**: Improved
- **Maintenance burden**: Reduced
- **Functionality**: Unchanged (core features)

This cleanup aligns with THIN architecture principles - only include what's actually needed for core functionality.
