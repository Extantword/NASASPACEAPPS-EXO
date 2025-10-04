#!/usr/bin/env python3
"""
Simple startup script for the Exoplanet Explorer API
"""
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    import uvicorn
    from app.main import app
    
    print("🚀 Starting Exoplanet Explorer API...")
    print("📡 Server will start at: http://localhost:8000")
    print("📚 API Documentation: http://localhost:8000/docs")
    print("⚡ Real-time status: http://localhost:8000/api/v1/data/status")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
    
except ImportError as e:
    print(f"❌ Import error: {e}")
    print("💡 Try installing dependencies: pip install -r requirements.txt")
    sys.exit(1)
except Exception as e:
    print(f"❌ Error starting server: {e}")
    sys.exit(1)