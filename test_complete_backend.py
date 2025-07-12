#!/usr/bin/env python3
"""
Script completo de pruebas para el backend de Zurich Claims
Prueba: conexión a BD, creación de siniestros, subida de documentos, y flujo completo
"""

import requests
import json
import time
import os
from pathlib import Path

# Configuración
BASE_URL = "http://localhost:8000"
TEST_CLAIM_DATA = {
    "coverage_type": "Auto",
    "full_name": "Juan Pérez García",
    "email": "juan.perez@email.com",
    "phone": "+52 55 1234 5678",
    "policy_number": "POL-2024-001234",
    "incident_date": "2024-07-06",
    "incident_location": "Av. Insurgentes Sur 1234, CDMX",
    "description": "Accidente automovilístico en intersección. Daños menores en parachoques delantero.",
    "estimated_amount": 15000.00
}

def print_test_header(test_name):
    """Imprimir encabezado de prueba"""
    print(f"\n{'='*60}")
    print(f"🧪 PRUEBA: {test_name}")
    print(f"{'='*60}")

def print_success(message):
    """Imprimir mensaje de éxito"""
    print(f"✅ {message}")

def print_error(message):
    """Imprimir mensaje de error"""
    print(f"❌ {message}")

def print_info(message):
    """Imprimir mensaje informativo"""
    print(f"ℹ️  {message}")

def test_server_health():
    """Probar que el servidor esté funcionando"""
    print_test_header("SERVIDOR Y HEALTH CHECK")
    
    try:
        # Probar endpoint raíz
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Servidor respondiendo: {data['message']}")
        else:
            print_error(f"Servidor no responde correctamente: {response.status_code}")
            return False
            
        # Probar health check
        response = requests.get(f"{BASE_URL}/api/health")
        if response.status_code == 200:
            data = response.json()
            print_success(f"Health check: {data['status']}")
            print_info(f"Servicios: {data['services']}")
        else:
            print_error(f"Health check falló: {response.status_code}")
            return False
            
        return True
        
    except requests.exceptions.ConnectionError:
        print_error("No se puede conectar al servidor. ¿Está corriendo en http://localhost:8000?")
        return False
    except Exception as e:
        print_error(f"Error inesperado: {str(e)}")
        return False

def test_create_claim():
    """Probar creación de siniestro"""
    print_test_header("CREACIÓN DE SINIESTRO")
    
    try:
        response = requests.post(
            f"{BASE_URL}/api/claims",
            json=TEST_CLAIM_DATA,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            data = response.json()
            print_success(f"Siniestro creado exitosamente")
            print_info(f"ID: {data['data']['id']}")
            print_info(f"Claim ID: {data['data']['claim_id']}")
            print_info(f"Status: {data['data']['status']}")
            return data['data']['claim_id']
        else:
            print_error(f"Error creando siniestro: {response.status_code}")
            print_error(f"Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Error inesperado: {str(e)}")
        return None

def test_upload_document(claim_id):
    """Probar subida de documento"""
    print_test_header("SUBIDA DE DOCUMENTO")
    
    if not claim_id:
        print_error("No se puede subir documento sin claim_id")
        return None
        
    try:
        # Crear archivo de prueba
        test_file_path = "test_document.pdf"
        with open(test_file_path, "w") as f:
            f.write("Este es un documento de prueba para el siniestro.")
        
        # Subir archivo
        with open(test_file_path, "rb") as f:
            files = {"file": ("test_document.pdf", f, "application/pdf")}
            data = {
                "document_type": "police_report",
                "upload_notes": "Reporte policial del accidente"
            }
            
            response = requests.post(
                f"{BASE_URL}/api/claims/{claim_id}/documents",
                files=files,
                data=data
            )
        
        # Limpiar archivo de prueba
        os.remove(test_file_path)
        
        if response.status_code == 200:
            data = response.json()
            print_success("Documento subido exitosamente")
            print_info(f"ID: {data['data']['id']}")
            print_info(f"Filename: {data['data']['filename']}")
            print_info(f"Storage URL: {data['data']['storage_url']}")
            return data['data']['id']
        else:
            print_error(f"Error subiendo documento: {response.status_code}")
            print_error(f"Respuesta: {response.text}")
            return None
            
    except Exception as e:
        print_error(f"Error inesperado: {str(e)}")
        return None

def test_get_claim(claim_id):
    """Probar obtención de siniestro"""
    print_test_header("OBTENCIÓN DE SINIESTRO")
    
    if not claim_id:
        print_error("No se puede obtener siniestro sin claim_id")
        return False
        
    try:
        response = requests.get(f"{BASE_URL}/api/claims/{claim_id}")
        
        if response.status_code == 200:
            data = response.json()
            print_success("Siniestro obtenido exitosamente")
            claim = data['data']['claim']
            print_info(f"Nombre: {claim['full_name']}")
            print_info(f"Email: {claim['email']}")
            print_info(f"Policy: {claim['policy_number']}")
            print_info(f"Status: {claim['status']}")
            
            documents = data['data']['documents']
            print_info(f"Documentos: {len(documents)}")
            for doc in documents:
                print_info(f"  - {doc['original_filename']} ({doc['document_type']})")
            
            return True
        else:
            print_error(f"Error obteniendo siniestro: {response.status_code}")
            print_error(f"Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Error inesperado: {str(e)}")
        return False

def test_list_claims():
    """Probar listado de siniestros"""
    print_test_header("LISTADO DE SINIESTROS")
    
    try:
        response = requests.get(f"{BASE_URL}/api/claims")
        
        if response.status_code == 200:
            data = response.json()
            claims = data['data']['claims']
            print_success(f"Listado exitoso: {len(claims)} siniestros encontrados")
            
            for claim in claims:
                print_info(f"  - {claim['claim_id']}: {claim['full_name']} ({claim['status']})")
            
            return True
        else:
            print_error(f"Error listando siniestros: {response.status_code}")
            print_error(f"Respuesta: {response.text}")
            return False
            
    except Exception as e:
        print_error(f"Error inesperado: {str(e)}")
        return False

def main():
    """Ejecutar todas las pruebas"""
    print("🚀 INICIANDO PRUEBAS COMPLETAS DEL BACKEND ZURICH CLAIMS")
    print(f"📍 URL Base: {BASE_URL}")
    print(f"⏰ Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Contador de pruebas
    tests_passed = 0
    total_tests = 5
    
    # 1. Probar servidor y health check
    if test_server_health():
        tests_passed += 1
    
    # 2. Probar creación de siniestro
    claim_id = test_create_claim()
    if claim_id:
        tests_passed += 1
    
    # 3. Probar subida de documento
    if test_upload_document(claim_id):
        tests_passed += 1
    
    # 4. Probar obtención de siniestro
    if test_get_claim(claim_id):
        tests_passed += 1
    
    # 5. Probar listado de siniestros
    if test_list_claims():
        tests_passed += 1
    
    # Resumen final
    print(f"\n{'='*60}")
    print(f"📊 RESUMEN DE PRUEBAS")
    print(f"{'='*60}")
    print(f"✅ Pruebas exitosas: {tests_passed}/{total_tests}")
    print(f"❌ Pruebas fallidas: {total_tests - tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print_success("🎉 ¡TODAS LAS PRUEBAS PASARON EXITOSAMENTE!")
        print_info("El backend está funcionando correctamente con la base de datos externa")
    else:
        print_error("⚠️  Algunas pruebas fallaron")
        print_info("Revisa los errores anteriores para identificar problemas")
    
    print(f"\n🔗 Documentación API: {BASE_URL}/docs")
    print(f"📋 OpenAPI Spec: {BASE_URL}/openapi.json")

if __name__ == "__main__":
    main() 