# ⚠️ DEPRECATED: Templates Directory

**This directory has been migrated to proper Python package structure.**

## New Location

**Production pipeline code is now located at:**
```
discernus/pipeline/
├── __init__.py
└── notebook_generation/
    ├── __init__.py
    ├── notebook_generator.py        # (was templates/generator/notebook_generator.py)
    ├── template_selector.py         # (was templates/generator/template_selector.py)
    └── templates/
        ├── universal_stage6_template.ipynb  # (was templates/universal_stage6_template.ipynb)
        └── patterns/                # (was templates/patterns/)
```

## Migration Rationale

The `templates/` directory was confusing because it contained:
- ❌ **Production pipeline code** (notebook_generator.py, template_selector.py)
- ❌ **Runtime templates** (universal_stage6_template.ipynb)
- ❌ **Framework patterns** (patterns/)

This has been reorganized into proper Python package structure:
- ✅ **Clear ownership** of production code
- ✅ **Proper imports** (`from discernus.pipeline import ...`)
- ✅ **Better testing** and documentation
- ✅ **Standard packaging** for production infrastructure

## What Remains Here (Temporarily)

Some legacy files remain for compatibility:
- `base/` - Template base patterns (review needed)
- `test/` - Test templates (review needed)  
- `exports/` - Generated exports (can be removed)
- `generator/` - Legacy production code (will be removed)
- `patterns/` - Legacy patterns (will be removed)

## Action Required

**For developers:**
1. Update imports: `from discernus.pipeline.notebook_generation import ...`
2. Update paths to new template location
3. Use new pipeline structure for any new development

**For documentation:**
1. Update any references to `templates/generator/`
2. Point to new `discernus/pipeline/` structure

---

**Migration completed:** June 30, 2025  
**Next cleanup:** Remove legacy files after validation period 