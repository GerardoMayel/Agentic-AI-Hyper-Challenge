#!/usr/bin/env python3
"""
Script para listar todos los archivos en Google Cloud Storage
"""

import sys
import os
from pathlib import Path

# Agregar el directorio backend al path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

from dotenv import load_dotenv
load_dotenv()

from app.services.storage_service import StorageService

def list_all_files():
    """Lista todos los archivos en el storage"""
    print("🔍 Listando TODOS los archivos en Google Cloud Storage...")
    
    try:
        storage_service = StorageService()
        
        if not storage_service.bucket:
            print("❌ No se pudo conectar a Google Cloud Storage")
            return
        
        # Listar archivos sin prefijo para ver todo
        all_files = storage_service.list_files()
        
        if not all_files:
            print("⚠️ No se encontraron archivos en el storage")
            return
        
        print(f"✅ Encontrados {len(all_files)} archivos en total:")
        print("\n📋 Lista completa de archivos:")
        
        for i, file_path in enumerate(all_files, 1):
            # Determinar tipo de archivo
            file_type = "📄"
            if any(ext in file_path.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']):
                file_type = "🖼️"
            elif any(ext in file_path.lower() for ext in ['.pdf']):
                file_type = "📕"
            elif any(ext in file_path.lower() for ext in ['.doc', '.docx']):
                file_type = "📘"
            elif any(ext in file_path.lower() for ext in ['.xls', '.xlsx']):
                file_type = "📗"
            
            print(f"   {i:2d}. {file_type} {file_path}")
        
        # Análisis por carpetas
        print("\n📊 Análisis por carpetas:")
        folders = {}
        for file_path in all_files:
            parts = file_path.split('/')
            if len(parts) > 1:
                folder = parts[0]
                if folder not in folders:
                    folders[folder] = 0
                folders[folder] += 1
        
        for folder, count in sorted(folders.items()):
            print(f"   📁 {folder}/: {count} archivos")
        
        # Buscar archivos de imagen específicamente
        print("\n🖼️ Archivos de imagen encontrados:")
        image_files = []
        for file_path in all_files:
            if any(ext in file_path.lower() for ext in ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']):
                image_files.append(file_path)
        
        if image_files:
            for i, file_path in enumerate(image_files, 1):
                print(f"   {i}. {file_path}")
        else:
            print("   ⚠️ No se encontraron archivos de imagen")
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    list_all_files() 