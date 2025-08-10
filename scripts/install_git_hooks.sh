#!/bin/bash
#
# Install Git Hooks for THIN Architecture Compliance
# ==================================================
# Sets up pre-commit hook to prevent THIN violations from being committed.

set -e

PROJECT_ROOT=$(git rev-parse --show-toplevel)
HOOKS_DIR="$PROJECT_ROOT/.git/hooks"

echo "🔧 Installing THIN Architecture Git Hooks..."

# Create pre-commit hook
cat > "$HOOKS_DIR/pre-commit" << 'EOF'
#!/bin/bash
#
# THIN Architecture Pre-Commit Hook
# =================================
# Lightweight compliance check to prevent THIN violations from being committed.
# Runs only on staged files for speed.

set -e

echo "🔍 THIN Architecture Pre-Commit Check..."

# Get the project root
PROJECT_ROOT=$(git rev-parse --show-toplevel)
cd "$PROJECT_ROOT"

# Get list of staged Python files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM | grep '\.py$' | head -10 || true)

if [ -z "$STAGED_FILES" ]; then
    echo "✅ No Python files staged - skipping THIN check"
    exit 0
fi

echo "📁 Checking $(echo "$STAGED_FILES" | wc -l) staged Python files..."

# Run lightweight compliance check on staged files only
VIOLATION_COUNT=0
for file in $STAGED_FILES; do
    if [ -f "$file" ]; then
        # Run compliance check on individual file
        RESULT=$(python3 scripts/thin_compliance_check.py "$file" 2>&1 || true)
        
        # Count violations in this file
        FILE_VIOLATIONS=$(echo "$RESULT" | grep -c "VIOLATION:" || true)
        
        if [ "$FILE_VIOLATIONS" -gt 0 ]; then
            echo "⚠️  $file: $FILE_VIOLATIONS violations"
            VIOLATION_COUNT=$((VIOLATION_COUNT + FILE_VIOLATIONS))
        fi
    fi
done

# Report results
if [ "$VIOLATION_COUNT" -eq 0 ]; then
    echo "✅ THIN compliance check passed - no violations in staged files"
    exit 0
else
    echo ""
    echo "❌ THIN VIOLATIONS DETECTED: $VIOLATION_COUNT issues in staged files"
    echo ""
    echo "🚨 COMMIT BLOCKED - Fix violations before committing:"
    echo "   1. Run: python3 scripts/thin_precheck.py"
    echo "   2. Review: docs/developer/CURSOR_AGENT_DISCIPLINE_GUIDE.md"  
    echo "   3. Fix violations using THIN patterns"
    echo "   4. Re-run: python3 scripts/thin_compliance_check.py"
    echo ""
    echo "💡 Remember: Use LLM intelligence, not complex software logic"
    exit 1
fi
EOF

# Make hook executable
chmod +x "$HOOKS_DIR/pre-commit"

echo "✅ Pre-commit hook installed successfully!"
echo ""
echo "🎯 What this does:"
echo "   • Runs THIN compliance check on staged Python files before commit"
echo "   • Blocks commits that introduce THIN violations"  
echo "   • Lightweight - only checks files you're actually committing"
echo ""
echo "🔧 To disable temporarily: git commit --no-verify"
echo "🗑️  To uninstall: rm .git/hooks/pre-commit"
echo ""
echo "📋 Current THIN violations in repo: $(python3 scripts/thin_compliance_check.py 2>&1 | grep -c "VIOLATION:" || echo "0")"
