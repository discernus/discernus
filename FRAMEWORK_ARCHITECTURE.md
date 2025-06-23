# Discernus Framework Architecture Guide

## Overview

Discernus uses a **two-tier framework architecture** that separates framework templates from active research frameworks. This guide explains the purpose and usage of each tier to prevent confusion and ensure proper development practices.

## Two-Tier Architecture

### Tier 1: Framework Templates (Archive)
**Location**: `framework_templates/`
**Purpose**: Archive of "original DNA" framework templates
**Usage**: Reference only, not for active development

```
framework_templates/
└── moral_foundations_theory/
    └── moral_foundations_theory_founding_template.yaml  # Template/archive copy
```

**Characteristics**:
- 📚 **Historical record** of framework designs
- 🔒 **Read-only reference** - not modified during research
- 🏛️ **Template DNA** for creating new research instances
- 📖 **Documentation purposes** and version history

### Tier 2: Research Workspaces (Active)
**Location**: `research_workspaces/[workspace_name]/frameworks/`
**Purpose**: Active research frameworks used in experiments
**Usage**: Active development and experimentation

```
research_workspaces/
└── june_2025_research_dev_workspace/
    └── frameworks/
        └── moral_foundations_theory/
            └── moral_foundations_theory_framework.yaml  # Active research framework
```

**Characteristics**:
- 🔬 **Active research** frameworks that can be modified
- 🎯 **Experiment-specific** versions with project customizations
- ✅ **Production frameworks** that experiments actually reference
- 🔄 **Iterative development** with version control and validation

## Critical Distinctions

| Aspect | Framework Templates | Research Workspaces |
|--------|-------------------|-------------------|
| **Purpose** | Historical archive | Active research |
| **Modification** | Read-only reference | Editable during research |
| **Experiments** | ❌ Don't reference | ✅ Reference these |
| **File Names** | `*_founding_template.yaml` | `*_framework.yaml` |
| **Development** | Frozen snapshots | Living documents |

## When to Use Which

### Use Framework Templates When:
- 📚 Reviewing the original framework design
- 🏗️ Starting a new research workspace
- 📖 Understanding framework evolution history
- 🔍 Comparing against original specifications

### Use Research Workspaces When:
- 🔬 Conducting experiments
- 📝 Developing new frameworks
- 🎯 Creating experiment definitions
- ✅ Running production analyses

## Common Mistakes to Avoid

### ❌ Mistake 1: Referencing Templates in Experiments
```yaml
# WRONG - Don't do this
file_path: "framework_templates/moral_foundations_theory/moral_foundations_theory_founding_template.yaml"
```

```yaml
# CORRECT - Use research workspace
file_path: "research_workspaces/june_2025_research_dev_workspace/frameworks/moral_foundations_theory/moral_foundations_theory_framework.yaml"
```

### ❌ Mistake 2: Editing Template Files Directly
Templates should remain as historical references. Make changes in research workspaces.

### ❌ Mistake 3: Using Templates for System Testing
System tests should use dedicated test frameworks, not templates or research workspaces.

## Development Workflow

### 1. Starting New Research
```bash
# Copy template to research workspace
cp -r framework_templates/moral_foundations_theory research_workspaces/my_workspace/frameworks/

# Rename and customize for research
mv research_workspaces/my_workspace/frameworks/moral_foundations_theory/moral_foundations_theory_founding_template.yaml \
   research_workspaces/my_workspace/frameworks/moral_foundations_theory/moral_foundations_theory_framework.yaml
```

### 2. Creating Experiments
Always reference the research workspace framework:
```yaml
components:
  frameworks:
    - id: "moral_foundations_theory"
      file_path: "research_workspaces/my_workspace/frameworks/moral_foundations_theory/moral_foundations_theory_framework.yaml"
```

### 3. System Testing
Use dedicated test frameworks that don't depend on either tier:
```yaml
# System health tests use their own test frameworks
file_path: "tests/system_health/frameworks/moral_foundations_theory/moral_foundations_theory_framework.yaml"
```

## Directory Structure Summary

```
discernus/
├── framework_templates/                 # Tier 1: Historical archive
│   └── moral_foundations_theory/
│       └── moral_foundations_theory_founding_template.yaml
│
├── research_workspaces/                 # Tier 2: Active research
│   └── june_2025_research_dev_workspace/
│       └── frameworks/
│           └── moral_foundations_theory/
│               └── moral_foundations_theory_framework.yaml
│
└── tests/                              # Independent: System testing
    └── system_health/
        └── frameworks/
            └── moral_foundations_theory/
                └── moral_foundations_theory_framework.yaml
```

## Best Practices

### For Researchers
1. ✅ Always work in research workspaces
2. ✅ Reference workspace frameworks in experiments
3. ✅ Use descriptive workspace names
4. ✅ Document framework modifications

### For Developers
1. ✅ Understand the two-tier architecture
2. ✅ Use appropriate tier for your use case
3. ✅ Create dedicated test assets for system validation
4. ✅ Update this documentation when architecture changes

### For Framework Creation
1. ✅ Start with templates as baseline
2. ✅ Develop in research workspaces
3. ✅ Test with dedicated test frameworks
4. ✅ Archive successful frameworks as new templates

## Migration Notes

When updating existing code that references the old `frameworks/` directory:
- **Template references**: Update to `framework_templates/`
- **Active framework references**: Update to appropriate research workspace
- **System test references**: Update to `tests/system_health/test_framework/`

This architecture ensures clean separation between historical templates, active research, and system validation while preventing the confusion that led to this documentation. 