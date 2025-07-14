#!/usr/bin/env python3
"""
Build script with automatic Render to SQLite sync
This script is designed to run during deployment to ensure SQLite has latest data
"""

import os
import sys
import time
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

def run_sync():
    """Run the sync process"""
    print("🔄 Starting Render to SQLite sync...")
    
    try:
        from sync_render_to_sqlite import main as sync_main
        sync_main()
        print("✅ Sync completed successfully")
        return True
    except Exception as e:
        print(f"❌ Sync failed: {e}")
        print("⚠️  Continuing without sync - will use existing SQLite data")
        return False

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting FastAPI server...")
    
    try:
        import uvicorn
        from main import app
        
        uvicorn.run(
            app,
            host="0.0.0.0",
            port=int(os.environ.get("PORT", 8000)),
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        sys.exit(1)

def main():
    """Main build process"""
    print("🏗️ BUILD WITH SYNC PROCESS")
    print("=" * 50)
    
    # Check if we're in production
    is_production = os.environ.get("ENVIRONMENT") == "production"
    print(f"Environment: {'Production' if is_production else 'Development'}")
    
    # Always try to sync in production, optionally in development
    if is_production or os.environ.get("FORCE_SYNC") == "true":
        print("\n📊 Production sync required...")
        sync_success = run_sync()
        
        if not sync_success:
            print("⚠️  Sync failed but continuing with server startup")
    else:
        print("\n📊 Development mode - skipping sync")
        print("Set FORCE_SYNC=true to enable sync in development")
    
    # Start the server
    print("\n🚀 Starting server...")
    start_server()

if __name__ == "__main__":
    main() 