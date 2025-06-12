#!/bin/bash

echo "🐛 Launching Narrative Gravity Research Workbench with Debug Mode"
echo "=================================================================="
echo ""
echo "Debug Console Features:"
echo "• 🌐 API call monitoring with timing"
echo "• 🚨 Error tracking and stack traces"
echo "• ⚡ Performance monitoring"
echo "• 🔧 Component lifecycle tracking"
echo "• 👆 User action tracking"
echo "• 📊 Real-time health status"
echo ""
echo "Debug Console Controls:"
echo "• Click the 🐛 Debug button (bottom left) to open console"
echo "• Filter by event type, level, or component"
echo "• Export debug data as JSON for analysis"
echo "• Clear events or toggle debug mode on/off"
echo ""
echo "Alternative Access Methods:"
echo "• Add ?debug=true to URL in browser"
echo "• Open browser console for additional logging"
echo "• Check Application tab in DevTools for localStorage"
echo ""
echo "=================================================================="
echo ""
echo "🔍 Debug events will appear in BOTH locations:"
echo "  1. Browser: Debug console (🐛 button) + browser DevTools"
echo "  2. Terminal: This console output (visible to AI assistant)"
echo ""
echo "Terminal Debug Output Format:"
echo "  🚨 [FRONTEND DEBUG] [Component] Error messages"
echo "  ⚠️  [FRONTEND DEBUG] [API] Warning messages"
echo "  ℹ️  [FRONTEND DEBUG] [User] Info messages"
echo "  🔧 [FRONTEND DEBUG] [Component] Debug messages"
echo ""
echo "Starting development server with terminal debug output..."
echo "=================================================================="

# Set debug mode environment variable
export REACT_APP_DEBUG_MODE=true

# Launch the development server
npm run dev

echo ""
echo "🛑 Debug session ended"
echo "Debug data is preserved in browser localStorage" 