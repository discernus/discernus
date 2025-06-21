# Api Retry Handler

**Module:** `src.utils.api_retry_handler`
**File:** `/Volumes/dev/discernus/src/utils/api_retry_handler.py`
**Package:** `utils`

API Retry Handler for LLM Providers
===================================

Robust retry handling for API calls with exponential backoff, rate limiting,
and provider failover to improve reliability in production research environments.

## Dependencies

- `dataclasses`
- `enum`
- `functools`
- `logging`
- `random`
- `requests`
- `time`
- `typing`

## Table of Contents

### Classes
- [RetryReason](#retryreason)
- [RetryConfig](#retryconfig)
- [APIRetryHandler](#apiretryhandler)
- [ProviderFailoverHandler](#providerfailoverhandler)

### Functions
- [with_openai_retry](#with-openai-retry)
- [with_anthropic_retry](#with-anthropic-retry)
- [with_mistral_retry](#with-mistral-retry)
- [with_google_ai_retry](#with-google-ai-retry)

## Classes

### RetryReason
*Inherits from: Enum*

Reasons for retrying API calls.

---

### RetryConfig

Configuration for retry behavior.

---

### APIRetryHandler

Comprehensive retry handler for LLM API calls.

Features:
- Exponential backoff with jitter
- Rate limit detection and handling
- Provider-specific error classification
- Automatic provider failover
- Comprehensive logging and monitoring

#### Methods

##### `__init__`
```python
__init__(self, config: Optional[[RetryConfig](src/utils/api_retry_handler.md#retryconfig)])
```

##### `with_retry`
```python
with_retry(self, provider: str, model: str)
```

Decorator for adding retry logic to API calls.

Args:
    provider: API provider name (openai, anthropic, mistral, google_ai)
    model: Model name being used

##### `_execute_with_retry`
```python
_execute_with_retry(self, func: Callable, provider: str, model: str, *args, **kwargs)
```

Execute function with comprehensive retry logic.

##### `_classify_error`
```python
_classify_error(self, error: Exception, provider: str) -> [RetryReason](src/utils/api_retry_handler.md#retryreason)
```

Classify error type for appropriate retry strategy.

##### `_should_retry`
```python
_should_retry(self, retry_reason: [RetryReason](src/utils/api_retry_handler.md#retryreason)) -> bool
```

Determine if error type should be retried.

##### `_calculate_delay`
```python
_calculate_delay(self, attempt: int, retry_reason: [RetryReason](src/utils/api_retry_handler.md#retryreason)) -> float
```

Calculate delay before retry with exponential backoff.

##### `_update_retry_stats`
```python
_update_retry_stats(self, provider: str, retry_reason: [RetryReason](src/utils/api_retry_handler.md#retryreason))
```

Update retry statistics for monitoring.

##### `get_retry_stats`
```python
get_retry_stats(self) -> Dict[Any]
```

Get comprehensive retry statistics.

##### `log_stats`
```python
log_stats(self)
```

Log current retry statistics.

---

### ProviderFailoverHandler

Handles automatic failover between LLM providers when one fails.

#### Methods

##### `__init__`
```python
__init__(self, provider_priority: Optional[List[str]])
```

Initialize with provider priority order.

Args:
    provider_priority: List of providers in order of preference
                     Default: ["openai", "anthropic", "google_ai", "mistral"]

##### `get_next_provider`
```python
get_next_provider(self, failed_provider: Optional[str]) -> Optional[str]
```

Get the next available provider for failover.

Args:
    failed_provider: Provider that just failed (will be marked unhealthy)
    
Returns:
    Next provider to try, or None if all providers are unhealthy

##### `mark_provider_healthy`
```python
mark_provider_healthy(self, provider: str)
```

Mark provider as healthy (e.g., after successful call).

##### `get_health_status`
```python
get_health_status(self) -> Dict[Any]
```

Get current provider health status.

---

## Functions

### `with_openai_retry`
```python
with_openai_retry(model: str)
```

Decorator for OpenAI API calls.

---

### `with_anthropic_retry`
```python
with_anthropic_retry(model: str)
```

Decorator for Anthropic API calls.

---

### `with_mistral_retry`
```python
with_mistral_retry(model: str)
```

Decorator for Mistral API calls.

---

### `with_google_ai_retry`
```python
with_google_ai_retry(model: str)
```

Decorator for Google AI API calls.

---

*Generated on 2025-06-21 18:56:11*