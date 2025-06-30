# Discernus Design System Organization Plan

## Current State Analysis
```
discernus/
├── 2_pm/viz/discernus_visual_design_guide.md     # ❌ Should be user-facing
├── discernus/visualization/                       # ✅ Core library code (correct)
├── examples/                                      # ⚠️ Needs organization
└── [various PDFs in root]                        # ❌ Should be organized
```

## Recommended Organization

### 1. Documentation Structure
```
1_docs/
├── visualization/                                 # NEW: Design system docs
│   ├── design_guide.md                          # MOVE: Main design guide
│   ├── typography_guide.md                      # NEW: Typography details
│   ├── grayscale_guide.md                       # NEW: B&W compatibility
│   ├── accessibility_guide.md                   # NEW: WCAG compliance
│   └── journal_compliance.md                    # NEW: Academic standards
├── specs/                                        # EXISTING: Keep current specs
└── frameworks/                                   # EXISTING: Keep current
```

### 2. Examples Organization
```
examples/
├── visualization/                                # NEW: Design system examples
│   ├── basic/                                   # Simple demonstrations
│   │   ├── typography_demo.py
│   │   ├── color_palette_demo.py
│   │   └── grayscale_demo.py
│   ├── advanced/                                # Complex real-world examples
│   │   ├── complete_workflow_demo.py
│   │   ├── academic_publication_demo.py
│   │   └── multi_framework_comparison.py
│   └── gallery/                                 # Visual showcase
│       ├── good_vs_bad_examples.py
│       ├── journal_compliance_showcase.py
│       └── accessibility_showcase.py
├── notebooks/                                   # EXISTING: Keep Jupyter examples
└── [other existing examples]                    # EXISTING: Keep current
```

### 3. Core Library Structure
```
discernus/
├── visualization/                               # EXISTING: Core functionality
│   ├── __init__.py                             # ✅ Updated with new functions
│   ├── discernus_typography.py                 # ✅ Typography system
│   ├── grayscale_strategy.py                   # ✅ B&W compatibility
│   ├── design_tokens.py                        # NEW: Design system constants
│   └── [existing viz modules]                  # EXISTING: Keep current
```

### 4. Output Organization
```
outputs/                                         # NEW: Generated files
├── examples/                                    # Example outputs
│   ├── typography_profiles.pdf
│   ├── grayscale_strategies.pdf
│   └── complete_workflow/
│       ├── research_color.pdf
│       ├── research_grayscale.pdf
│       └── nature_submission.pdf
└── gallery/                                    # Showcase outputs
    ├── good_examples/
    ├── bad_examples/
    └── journal_compliance/
```

## Migration Plan

### Phase 1: Core Documentation (Immediate)
- [ ] Move `2_pm/viz/discernus_visual_design_guide.md` → `1_docs/visualization/design_guide.md`
- [ ] Create `1_docs/visualization/` directory structure
- [ ] Update all internal documentation links

### Phase 2: Examples Organization (Next)
- [ ] Create `examples/visualization/` structure
- [ ] Reorganize existing examples into logical categories
- [ ] Create `outputs/` directory for generated files
- [ ] Add `.gitignore` patterns for output files

### Phase 3: Enhanced Documentation (Later)
- [ ] Split design guide into focused documents
- [ ] Create visual gallery documentation
- [ ] Add interactive documentation examples

## Rationale

### Why This Organization?

**User Discovery Path:**
1. `1_docs/visualization/design_guide.md` - Main entry point
2. `examples/visualization/basic/` - Learn fundamentals  
3. `examples/visualization/advanced/` - Real-world usage
4. `discernus/visualization/` - Library implementation

**Maintainability:**
- Documentation in `1_docs/` (user-facing)
- Examples in `examples/` (learning/testing)
- Core code in `discernus/` (library)
- Outputs in `outputs/` (generated, gitignored)

**Discoverability:**
- Clear path from docs → examples → implementation
- Logical grouping by complexity and use case
- Separate generated files from source code

## Immediate Actions Needed

1. **Move design guide:** `2_pm/viz/` → `1_docs/visualization/`
2. **Organize examples:** Create visualization subdirectory
3. **Create outputs directory:** Clean up root-level PDFs
4. **Update imports:** Ensure all examples work after reorganization
5. **Update README:** Add design system documentation links 