#!/bin/bash
# Discernus Infrastructure Startup Script
# Prevents the $0.50 MinIO debugging dance that wastes Cursor agent cycles

set -e  # Exit on any error

echo "🚀 Starting Discernus Infrastructure..."

# Check if MinIO is already running
if lsof -i :9000 > /dev/null 2>&1; then
    echo "✅ MinIO already running on port 9000"
else
    echo "🗄️ Starting MinIO server..."
    
    # Create data directory
    mkdir -p ~/minio-data
    
    # Start MinIO in background with correct credentials
    # These match what discernus/storage/minio_client.py expects
    MINIO_ROOT_USER=minio MINIO_ROOT_PASSWORD=minio123 \
    nohup minio server ~/minio-data --console-address ":9001" > ~/minio.log 2>&1 &
    
    echo "⏳ Waiting for MinIO to start..."
    sleep 3
    
    # Test connection
    if curl -s http://localhost:9000/minio/health/live > /dev/null; then
        echo "✅ MinIO started successfully on http://localhost:9000"
        echo "🌐 MinIO Console: http://localhost:9001 (user: minio, pass: minio123)"
    else
        echo "❌ MinIO failed to start. Check ~/minio.log for errors."
        exit 1
    fi
fi

# Check if Redis is needed (for old CLI - will be deprecated)
if command -v redis-server > /dev/null 2>&1; then
    if ! pgrep redis-server > /dev/null; then
        echo "🔄 Starting Redis server..."
        redis-server --daemonize yes
        echo "✅ Redis started"
    else
        echo "✅ Redis already running"
    fi
else
    echo "⚠️  Redis not installed (optional - only needed for legacy CLI)"
fi

echo ""
echo "🎯 Infrastructure Status:"
echo "   ✅ MinIO: http://localhost:9000 (storage)"
echo "   ✅ MinIO Console: http://localhost:9001"
if pgrep redis-server > /dev/null; then
    echo "   ✅ Redis: localhost:6379 (legacy CLI only)"
else
    echo "   ⚠️  Redis: not running (legacy CLI won't work)"
fi
echo ""
echo "🚀 Ready for Discernus development!"
echo "💡 Use 'python3 -c \"from discernus.core.thin_orchestrator import ThinOrchestrator\"' for direct execution"
echo "💡 Use 'discernus/cli.py run' for legacy Redis-based execution (requires Redis)" 