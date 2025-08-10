#!/bin/bash

# Python Cache Cleanup Script
# Removes Python cache files to keep the codebase clean

echo "🧹 Cleaning Python cache files..."

# Count files before cleanup
BEFORE=$(find . -name "*.pyc" -o -name "__pycache__" -o -name "*.pyo" | wc -l | tr -d ' ')

if [ "$BEFORE" -eq 0 ]; then
    echo "✅ No Python cache files found - already clean!"
    exit 0
fi

echo "📊 Found $BEFORE Python cache files to remove..."

# Remove Python cache files
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null
find . -name "*.pyo" -delete

# Count files after cleanup
AFTER=$(find . -name "*.pyc" -o -name "__pycache__" -o -name "*.pyo" | wc -l | tr -d ' ')

if [ "$AFTER" -eq 0 ]; then
    echo "✅ Successfully removed $BEFORE Python cache files"
    echo "💾 Project is now clean of Python cache artifacts"
else
    echo "⚠️  Warning: $AFTER cache files remain (may be in use)"
fi

echo "🧹 Python cache cleanup complete!"
