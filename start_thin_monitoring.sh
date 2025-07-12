#!/bin/bash
# Quick Start THIN Monitoring
# ===========================

echo "🔧 Starting THIN Monitoring System for Cursor Agents"
echo "=" * 55

# Check if we're in the right directory
if [ ! -d "discernus" ]; then
    echo "❌ Run this from the project root directory"
    exit 1
fi

# Check if setup has been run
if [ ! -f ".cursor/rules" ]; then
    echo "🚀 First time setup - running installation..."
    python3 scripts/setup_thin_monitoring.py
    echo ""
fi

# Start monitoring in background
echo "🔍 Starting real-time THICK pattern detection..."
python3 scripts/cursor_thin_watcher.py &
WATCHER_PID=$!

echo "✅ THIN monitoring active!"
echo ""
echo "🎯 System Status:"
echo "   • Cursor constrained by .cursor/rules"
echo "   • Real-time monitoring: PID $WATCHER_PID"
echo "   • Linting errors will show in VSCode/Cursor"
echo "   • Warning files created for THICK patterns"
echo ""
echo "💡 Success indicators:"
echo "   • Cursor suggests llm_client.call_llm() instead of parsing"
echo "   • Warning files appear when writing THICK code"
echo "   • Less refactoring needed from THICK to THIN"
echo ""
echo "🛑 To stop monitoring: kill $WATCHER_PID"
echo "📚 Documentation: THIN_MONITORING_README.md"
echo ""
echo "Press Ctrl+C to stop monitoring..."

# Wait for interrupt
trap "echo ''; echo '👋 THIN monitoring stopped'; kill $WATCHER_PID 2>/dev/null; exit 0" INT

# Keep script running
while kill -0 $WATCHER_PID 2>/dev/null; do
    sleep 1
done

echo "⚠️  Monitoring process ended unexpectedly" 