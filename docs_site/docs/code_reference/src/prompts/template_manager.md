# Template Manager

**Module:** `src.prompts.template_manager`
**File:** `/app/src/prompts/template_manager.py`
**Package:** `prompts`

Prompt Template Manager - Minimal implementation for analysis service

## Dependencies

- `enum`
- `json`
- `typing`

## Table of Contents

### Classes
- [PromptMode](#promptmode)
- [PromptTemplateManager](#prompttemplatemanager)

## Classes

### PromptMode
*Inherits from: Enum*

Prompt generation modes

---

### PromptTemplateManager

Minimal prompt template manager for analysis service functionality.
This is a basic implementation to fix import errors and get the pipeline working.

#### Methods

##### `__init__`
```python
__init__(self)
```

##### `generate_api_prompt`
```python
generate_api_prompt(self, text: str, framework: str, model_name: str, model: str) -> str
```

Generate API prompt for text analysis

##### `generate_interactive_prompt`
```python
generate_interactive_prompt(self, framework_name: str) -> str
```

Generate interactive prompt for a framework

##### `get_template`
```python
get_template(self, template_id: str) -> Optional[Dict[Any]]
```

Get template by ID

##### `list_templates`
```python
list_templates(self) -> Dict[Any]
```

List available templates

---

*Generated on 2025-06-23 10:38:43*