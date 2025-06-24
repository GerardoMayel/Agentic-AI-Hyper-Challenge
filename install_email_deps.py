#!/usr/bin/env python3
"""
Script de Instalación de Dependencias para Pruebas de Email
"""

import subprocess
import sys

def install_package(package):
    """Instala un paquete usando pip."""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ {package} instalado correctamente")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ Error instalando {package}")
        return False

def main():
    """Instala las dependencias necesarias para las pruebas de email."""
    print("🔧 Instalando Dependencias para Pruebas de Email")
    print("=" * 50)
    
    # Lista de dependencias requeridas
    packages = [
        "sendgrid",
        "python-dotenv"
    ]
    
    print("📦 Paquetes a instalar:")
    for package in packages:
        print(f"   - {package}")
    
    print("\n🚀 Iniciando instalación...")
    
    success_count = 0
    for package in packages:
        if install_package(package):
            success_count += 1
    
    print(f"\n📊 Resumen:")
    print(f"   Paquetes instalados: {success_count}/{len(packages)}")
    
    if success_count == len(packages):
        print("\n🎉 ¡Todas las dependencias instaladas correctamente!")
        print("\n📋 Próximos pasos:")
        print("   1. Configura las variables de entorno en .env")
        print("   2. Ejecuta: python quick_email_test.py")
        print("   3. O ejecuta: python email_validation_script.py")
    else:
        print("\n❌ Algunas dependencias no se pudieron instalar.")
        print("   Revisa los errores e intenta nuevamente.")

if __name__ == "__main__":
    main() 