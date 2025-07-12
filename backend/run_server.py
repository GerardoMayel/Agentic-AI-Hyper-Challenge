#!/usr/bin/env python3
"""
Script para levantar el servidor FastAPI del backend
"""

import sys
import os
from pathlib import Path

# Agregar el directorio backend al path de Python
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Agregar el directorio raíz al path para encontrar el .env
root_dir = backend_dir.parent
sys.path.insert(0, str(root_dir))

if __name__ == "__main__":
    import uvicorn
    from main import app
    
    print("🚀 Starting Zurich Claims Backend Server...")
    print(f"📁 Backend directory: {backend_dir}")
    print(f"📁 Root directory: {root_dir}")
    
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        reload_dirs=[str(backend_dir)]
    ) 