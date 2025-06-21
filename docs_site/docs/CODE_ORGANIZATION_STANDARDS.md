# Code Organization Standards
*Preventing Production Code Pollution*

## 🎯 **The Problem**

**Issue**: Codebase cluttered with experimental code, temporary files, and obsolete systems that:
- Confuse AI assistants during searches
- Lead to using deprecated patterns  
- Make it hard to find actual production code
- Result in building on unstable foundations

**Solution**: Clear separation with promotion process.

---

## 📁 **Directory Structure Standards**

### **✅ PRODUCTION TIER** (Searchable, Maintained, Stable)

```
src/narrative_gravity/          # Core production code
├── api/                       # Production API components
├── models/                    # Production data models  
├── utils/                     # Production utilities
├── visualization/             # Production visualization
└── academic/                  # Production academic tools

scripts/production/            # Production-ready scripts
├── check_existing_systems.py  # System prevention tools
├── execute_experiment.py      # Core experiment execution
└── architectural_compliance.py # Production validation

docs/specifications/           # Production documentation
docs/user-guides/             # Production user guides
frameworks/                   # Production framework definitions
```

**Criteria for Production Tier**:
- ✅ **Fully tested** and working
- ✅ **Documented** with clear usage
- ✅ **Maintained** and up-to-date
- ✅ **Used in actual research** workflows
- ✅ **No "TODO" or "experimental" markers**

### **✍️ In-Code Documentation Standards**

To ensure code is clear, maintainable, and readable, all Python functions and classes in the **Production Tier** (`src/` and `scripts/applications/`) **must** include Google-style docstrings.

### Docstring Format (Google Style)

Docstrings should provide a clear summary of the object's purpose, its arguments, any expected return values, and any exceptions it might raise.

**Example of a well-documented function:**

```python
def example_function(arg1, arg2):
    """Summarizes the function's behavior in one line.

    A more detailed description of the function's purpose, behavior,
    and any side effects. Can be multiple lines.

    Args:
        arg1 (str): Description of the first argument.
        arg2 (int): Description of the second argument, including its
            default value if applicable.

    Returns:
        bool: Description of the return value, explaining what True or
              False represents.

    Raises:
        ValueError: If `arg2` is a negative number.
        TypeError: If `arg1` is not a string.
    """
    if not isinstance(arg1, str):
        raise TypeError("arg1 must be a string.")
    if arg2 < 0:
        raise ValueError("arg2 cannot be negative.")
    return True
```

This standard enables automated tools to generate documentation and helps developers understand code without having to read its implementation.

### **🧪 EXPERIMENTAL TIER** (Limited Searchability)

```
experimental/                 # All experimental code
├── prototypes/              # Early-stage development
├── testing/                 # Ad hoc testing scripts
├── iterations/              # Development iterations
├── tmp/                     # Temporary files
└── deprecated/              # Code marked for deletion

sandbox/                     # Individual development areas
├── researcher1/             # Personal experimental space
├── researcher2/             # Personal experimental space
└── shared/                  # Shared experimental work
```

**Criteria for Experimental Tier**:
- 🧪 **Unfinished** or exploratory code
- 🧪 **Ad hoc testing** and validation scripts
- 🧪 **Prototype implementations**
- 🧪 **Temporary files** and one-off analyses
- 🧪 **Personal research** iterations

### **🗑️ DEPRECATED TIER** (No Searchability)

```
deprecated/                  # Clearly obsolete code
├── by-date/                # Organized by deprecation date
│   ├── 2025-06-18/        # What was deprecated when
│   └── 2025-06-17/
└── by-system/             # Organized by system replaced
    ├── old-qa-system/     # What system this replaced
    └── legacy-api/
```

---

## 🔄 **Promotion Process**

### **Experimental → Production Promotion**

**Requirements for Promotion**:
1. ✅ **Code Quality**: Passes all quality checks
2. ✅ **Testing**: Comprehensive test coverage
3. ✅ **Documentation**: Clear usage documentation
4. ✅ **Integration**: Works with existing production systems
5. ✅ **Review**: Peer review completed
6. ✅ **Performance**: Meets production performance standards

**Promotion Checklist**:
```bash
# 1. Run quality checks
python3 scripts/production/validate_for_promotion.py experimental/prototypes/new_system.py

# 2. Ensure no experimental dependencies
python3 scripts/production/check_production_dependencies.py new_system

# 3. Add to production inventory
echo "new_system: Description and usage" >> docs/EXISTING_SYSTEMS_INVENTORY.md

# 4. Move to production location
mv experimental/prototypes/new_system.py src/narrative_gravity/production_module/

# 5. Update production documentation
# 6. Add to production test suite
```

### **Production → Deprecated Process**

**When Replacing Production Code**:
1. 📝 **Document replacement reason** in deprecation log
2. 🏷️ **Tag with deprecation date** and replacement system
3. 📦 **Move to `deprecated/by-system/old-system-name/`**
4. 🔗 **Update all references** to point to new system
5. 📚 **Update documentation** and inventory

---

## 🔍 **Search Strategy Updates**

### **AI Assistant Search Rules**

**ALWAYS Search These** (Production Tier):
- `src/narrative_gravity/` - Core production code
- `scripts/production/` - Production scripts
- `docs/specifications/` - Production documentation  
- `docs/user-guides/` - Production guides
- `frameworks/` - Production frameworks

**CONDITIONAL Search** (Experimental Tier):
- `experimental/` - Only when explicitly looking for experimental work
- `sandbox/` - Only when asked about specific research

**NEVER Search** (Deprecated Tier):
- `deprecated/` - Should not appear in normal searches
- `tmp/` - Temporary files
- Files marked with `# DEPRECATED` comments

### **Updated Search Scripts**

Update `scripts/check_existing_systems.py` to focus on production:

```bash
# Search production code first
grep -r "$query" src/narrative_gravity/
grep -r "$query" scripts/production/
grep -r "$query" docs/specifications/

# Only search experimental if no production matches
if [[ $production_matches == 0 ]]; then
    echo "⚠️  No production systems found. Checking experimental..."
    grep -r "$query" experimental/
fi
```

---

## 🛡️ **Implementation Plan**

### **Phase 1: Reorganize Existing Code**

1. **Audit Current Code**:
   ```bash
   # Create inventory of what we have
   find . -name "*.py" -type f | grep -E "(test|tmp|old|backup|archive)" > experimental_candidates.txt
   find . -name "*.py" -type f | grep -vE "(test|tmp|old|backup|archive)" > production_candidates.txt
   ```

2. **Create New Directory Structure**:
   ```bash
   mkdir -p experimental/{prototypes,testing,iterations,tmp,deprecated}
   mkdir -p sandbox/{shared}
   mkdir -p scripts/production
   mkdir -p deprecated/{by-date,by-system}
   ```

3. **Move Code to Appropriate Tiers**:
   - Identify truly production-ready code → `src/` and `scripts/production/`
   - Move experimental/testing code → `experimental/`
   - Archive obsolete code → `deprecated/`

### **Phase 2: Update Tooling**

1. **Update Search Tools**:
   - Modify `check_existing_systems.py` to focus on production
   - Add production-only search mode
   - Add experimental search mode (explicit opt-in)

2. **Create Promotion Tools**:
   - `scripts/production/validate_for_promotion.py`
   - `scripts/production/promote_to_production.py`
   - `scripts/production/deprecate_system.py`

3. **Update Documentation Tools**:
   - Auto-generate production inventory
   - Flag experimental dependencies in production code

### **Phase 3: Establish Process**

1. **Development Workflow**:
   - All new development starts in `experimental/`
   - Use promotion checklist for moving to production
   - Regular cleanup of experimental code

2. **Maintenance Workflow**:
   - Monthly review of experimental code (promote or delete)
   - Quarterly audit of production code (ensure still maintained)
   - Document all deprecations

---

## 📋 **Benefits**

1. **🔍 Clean Searches**: AI assistants find only production-ready code
2. **🏗️ Stable Foundation**: Building on maintained, tested systems
3. **🧪 Freedom to Experiment**: Clear space for iteration without pollution
4. **📚 Clear Documentation**: Production inventory stays accurate
5. **🚀 Faster Development**: Less time sorting through obsolete code

---

## 🎯 **Success Metrics**

- **Search Accuracy**: 90%+ of searches return production-ready results
- **Build Quality**: No new systems built on deprecated foundations  
- **Code Reuse**: Measurable increase in reusing existing production systems
- **Maintenance**: Clear ownership and update responsibility for production code

**This organization standard should prevent both "rebuilding worse systems" AND "building on rotten foundations" problems!** 