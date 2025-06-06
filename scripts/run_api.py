#!/usr/bin/env python3
"""
Startup script for Narrative Gravity Analysis API.
Runs the FastAPI server for development and testing.
"""

import sys
import os
from pathlib import Path
import uvicorn

# Add project root to Python path for src imports
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

def main():
    """Start the FastAPI server."""
    print("🚀 Starting Narrative Gravity Analysis API")
    print("=" * 50)
    print("API Documentation: http://localhost:8000/api/docs")
    print("Health Check: http://localhost:8000/api/health")
    print("Press Ctrl+C to stop")
    print("=" * 50)
    
    try:
        # Import the app
        from src.api.main import app
        
        # Run the server
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            reload=True,  # Auto-reload on code changes
            log_level="info"
        )
        
    except KeyboardInterrupt:
        print("\n👋 API server stopped")
    except Exception as e:
        print(f"❌ Failed to start API server: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 