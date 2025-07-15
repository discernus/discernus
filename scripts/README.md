# Automated Model Registry Updater

This directory contains scripts to automatically maintain the model registry (`discernus/gateway/models.yaml`) with up-to-date information from various LLM providers.

## Problem Solved

The `models.yaml` file is the single source of truth for model availability, pricing, and rate limits. Manual maintenance leads to:
- ❌ Outdated model information (like the Claude 3.5 Sonnet issue)
- ❌ Missing newly released models
- ❌ Incorrect pricing information
- ❌ Stale rate limit data

## Solution

The automated updater:
- ✅ **Queries providers directly** for available models
- ✅ **Updates pricing** from LiteLLM's cost map
- ✅ **Discovers new models** automatically
- ✅ **Removes deprecated models** that are no longer available
- ✅ **Runs on schedule** (weekly) via GitHub Actions
- ✅ **Creates backups** before making changes

## Files

- `update_model_registry.py` - Main updater script
- `../github/workflows/update-model-registry.yml` - GitHub Action workflow
- `README.md` - This documentation

## Usage

### Manual Updates

```bash
# Full update (live changes)
python3 scripts/update_model_registry.py

# Dry run (show what would change)
python3 scripts/update_model_registry.py --dry-run

# Check if updates are needed
python3 scripts/update_model_registry.py --check
```

### GitHub Actions

**Automatic Schedule:**
- Runs every Monday at 2 AM UTC
- Creates a pull request with changes for review

**Manual Trigger:**
1. Go to Actions tab in GitHub
2. Select "Update Model Registry"
3. Click "Run workflow"
4. Choose dry-run or live update

## Provider Support

### Current Providers

| Provider | Method | Models Discovered |
|----------|--------|------------------|
| **Vertex AI** | Known model list + regions | Claude 3.5/3.7/4, Gemini 2.5 |
| **OpenRouter** | API query | All available models |
| **Anthropic** | Known model list | Claude 3.5 Sonnet, Claude 3 Haiku |
| **OpenAI** | Known model list | GPT-4o, GPT-4o Mini |

### Adding New Providers

To add a new provider, extend the `ModelRegistryUpdater` class:

```python
def get_newprovider_models(self) -> List[Dict[str, Any]]:
    """Query NewProvider for available models"""
    try:
        # Query provider API
        response = requests.get("https://api.newprovider.com/models")
        # Parse and return model information
        return models
    except Exception as e:
        print(f"⚠️  Failed to query NewProvider: {e}")
        return []

# Add to run_update() method:
discovered_models = {
    'vertex_ai': self.get_vertex_ai_models(),
    'openrouter': self.get_openrouter_models(),
    'anthropic': self.get_anthropic_models(),
    'openai': self.get_openai_models(),
    'newprovider': self.get_newprovider_models(),  # Add this
}
```

## Configuration

### Model Registry Format

Each model entry in `models.yaml` follows this format:

```yaml
provider/model-id:
  provider: "provider_name"
  performance_tier: "top-tier" | "cost-effective" | "general-purpose"
  context_window: 200000
  costs:
    input_per_million_tokens: 3.00
    output_per_million_tokens: 15.00
  utility_tier: 1  # 1 = highest priority
  task_suitability: [synthesis, coordination, planning]
  optimal_batch_size: 8
  last_updated: "2025-01-15"
  review_by: "2025-07-15"
  notes: "Human-readable notes about the model"
  
  # Vertex AI specific
  regions:
    us-east5:
      tpm: 350000
      rpm: 80
```

### Auto-Discovery Fields

Models discovered automatically get these additional fields:

```yaml
auto_discovered: true
notes: "Auto-discovered model from provider"
```

## Integration with Experiment System

The updated `models.yaml` ensures that:

1. **Model Selection** works correctly (fixes Claude 3.5 Sonnet issue)
2. **Rate Limits** are accurate for planning
3. **Cost Estimation** uses current pricing
4. **New Models** are available for experiments

## Monitoring

### GitHub Actions Dashboard

Monitor the automated updates:
- Actions tab → "Update Model Registry" workflow
- Check for failed runs or PRs requiring review

### Manual Checks

```bash
# Check if registry needs updates
python3 scripts/update_model_registry.py --check
echo $?  # 0 = up to date, 1 = needs updates

# Validate current registry
python3 -c "import yaml; yaml.safe_load(open('discernus/gateway/models.yaml'))"
```

## Troubleshooting

### Common Issues

**Script fails with import errors:**
```bash
pip install -r requirements.txt
pip install PyYAML requests
```

**No models discovered:**
- Check network connectivity
- Verify API credentials (if required)
- Check provider API status

**GitHub Action fails:**
- Check workflow permissions
- Verify Python dependencies
- Check for YAML syntax errors

### Recovery

If the automated update breaks something:

1. **Restore from backup:**
   ```bash
   cp discernus/gateway/models.yaml.backup discernus/gateway/models.yaml
   ```

2. **Reset to known good state:**
   ```bash
   git checkout HEAD~1 -- discernus/gateway/models.yaml
   ```

3. **Fix manually then run update:**
   ```bash
   # Fix the issue
   python3 scripts/update_model_registry.py --dry-run  # Test
   python3 scripts/update_model_registry.py  # Apply
   ```

## Development

### Testing Changes

Always test changes to the updater script:

```bash
# Test without making changes
python3 scripts/update_model_registry.py --dry-run

# Test with a copy of the config
cp discernus/gateway/models.yaml /tmp/models.yaml.test
python3 scripts/update_model_registry.py --config /tmp/models.yaml.test
```

### Extending Functionality

Common extensions:

1. **Add health checks** for model availability
2. **Implement caching** for provider API calls
3. **Add Slack notifications** for changes
4. **Create model usage analytics**
5. **Add cost optimization recommendations**

## Related Files

- `discernus/gateway/models.yaml` - The model registry itself
- `discernus/gateway/llm_gateway.py` - Uses the model registry
- `discernus/core/agent_registry.yaml` - Agent definitions
- `experiments/*/experiment.md` - Request specific models

## Support

For issues with the automated updater:
1. Check this documentation
2. Review GitHub Action logs
3. Test with `--dry-run` flag
4. Create an issue with error details 