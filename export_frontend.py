#!/usr/bin/env python3
"""
Script para exportar solo el frontend de la aplicación Reflex.
Este script se usa para generar archivos estáticos sin requerir conexión a base de datos.
"""

import os
import subprocess
import sys

def export_frontend():
    """Exporta solo el frontend de la aplicación."""
    
    print("🚀 Exportando frontend estático de la aplicación Reflex...")
    
    # Configurar variables de entorno para modo estático
    os.environ["STATIC_MODE"] = "true"
    
    try:
        # Ejecutar reflex export
        result = subprocess.run([
            "reflex", "export"
        ], capture_output=True, text=True, check=True)
        
        print("✅ Frontend estático exportado exitosamente")
        print(f"📁 Archivos generados en: .web/public")
        
        # Mostrar contenido del directorio
        if os.path.exists(".web/public"):
            files = os.listdir(".web/public")
            print(f"📄 Archivos generados: {len(files)}")
            for file in files[:10]:  # Mostrar primeros 10 archivos
                print(f"   - {file}")
            if len(files) > 10:
                print(f"   ... y {len(files) - 10} archivos más")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Error exportando frontend: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

if __name__ == "__main__":
    success = export_frontend()
    sys.exit(0 if success else 1) 