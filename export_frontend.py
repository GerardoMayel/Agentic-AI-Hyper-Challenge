#!/usr/bin/env python3
"""
Script para exportar solo el frontend de la aplicación Reflex.
Este script se usa para generar archivos estáticos sin requerir conexión a base de datos.
"""

import os
import subprocess
import sys
import shutil

def export_frontend():
    """Exporta solo el frontend de la aplicación."""
    
    print("🚀 Exportando frontend estático de la aplicación Reflex...")
    
    # Configurar variables de entorno para modo estático
    os.environ["STATIC_MODE"] = "true"
    
    try:
        # Ejecutar reflex export con --frontend-only
        result = subprocess.run([
            "reflex", "export", "--frontend-only"
        ], capture_output=True, text=True, check=True)
        
        print("✅ Frontend estático exportado exitosamente")
        print(f"📁 Archivos generados en: .web/public")
        
        # Verificar si existe el directorio pages y copiar archivos
        pages_dir = ".web/pages"
        public_dir = ".web/public"
        
        if os.path.exists(pages_dir):
            print(f"📄 Copiando archivos de {pages_dir} a {public_dir}...")
            
            # Crear directorio public si no existe
            os.makedirs(public_dir, exist_ok=True)
            
            # Copiar todos los archivos de pages a public
            for item in os.listdir(pages_dir):
                src = os.path.join(pages_dir, item)
                dst = os.path.join(public_dir, item)
                
                if os.path.isfile(src):
                    shutil.copy2(src, dst)
                    print(f"   ✅ Copiado: {item}")
                elif os.path.isdir(src):
                    if os.path.exists(dst):
                        shutil.rmtree(dst)
                    shutil.copytree(src, dst)
                    print(f"   ✅ Copiado directorio: {item}")
        else:
            print(f"⚠️  Directorio {pages_dir} no encontrado")
            print("🔍 Buscando archivos HTML en otros directorios...")
            
            # Buscar archivos HTML en .web
            web_dir = ".web"
            if os.path.exists(web_dir):
                for root, dirs, files in os.walk(web_dir):
                    for file in files:
                        if file.endswith('.html'):
                            print(f"   📄 Encontrado HTML: {os.path.join(root, file)}")
                        elif file.endswith('.js') and 'index' in file:
                            print(f"   📄 Encontrado JS principal: {os.path.join(root, file)}")
        
        # Mostrar contenido final del directorio public
        if os.path.exists(public_dir):
            files = os.listdir(public_dir)
            print(f"📄 Archivos finales en {public_dir}: {len(files)}")
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