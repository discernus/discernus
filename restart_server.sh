#!/bin/bash
# Smart Flask Server Restart Script
# Kills existing processes and starts fresh on port 5001

echo "🔄 Restarting Discernus Web Server..."

# Kill existing Flask processes
echo "🛑 Stopping existing servers..."
lsof -ti:5001 | xargs kill -9 2>/dev/null || true
lsof -ti:5002 | xargs kill -9 2>/dev/null || true
pkill -f "python3 discernus/web/app.py" 2>/dev/null || true

# Wait a moment for cleanup
sleep 1

# Start fresh server
echo "🚀 Starting server on port 5001..."
cd "$(dirname "$0")"
python3 discernus/web/app.py

echo "✅ Server should be running at http://localhost:5001" 