#!/usr/bin/env python3
"""
Run database sync and then start the server
This script ensures we have local data before starting the API
"""

import os
import sys
import subprocess
import time
from pathlib import Path

def run_sync():
    """Run the database sync script"""
    print("🔄 Starting database sync...")
    
    try:
        # Run the sync script
        result = subprocess.run([
            sys.executable, "sync_render_to_sqlite.py"
        ], capture_output=True, text=True, cwd=Path(__file__).parent)
        
        if result.returncode == 0:
            print("✅ Database sync completed successfully")
            print(result.stdout)
            return True
        else:
            print("⚠️ Database sync failed, but continuing...")
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
            return False
            
    except Exception as e:
        print(f"⚠️ Error running sync: {e}")
        return False

def run_server():
    """Run the FastAPI server"""
    print("🚀 Starting FastAPI server...")
    
    try:
        # Run the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--host", "0.0.0.0", "--port", "8000", "--reload"
        ], cwd=Path(__file__).parent)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

def main():
    """Main function"""
    print("🚀 RENDER SYNC + SERVER")
    print("=" * 50)
    
    # Change to backend directory
    backend_dir = Path(__file__).parent
    os.chdir(backend_dir)
    
    # Run sync first
    sync_success = run_sync()
    
    if not sync_success:
        print("⚠️ Sync failed, but starting server anyway...")
    
    # Wait a moment
    time.sleep(2)
    
    # Run server
    run_server()

if __name__ == "__main__":
    main() 