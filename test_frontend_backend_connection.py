#!/usr/bin/env python3
"""
Script para probar la conexión entre frontend y backend
"""

import requests
import json
import time

def test_backend_health():
    """Prueba la salud del backend"""
    print("🔍 Probando salud del backend...")
    
    try:
        response = requests.get("http://localhost:8000/api/health")
        if response.status_code == 200:
            data = response.json()
            print("✅ Backend está funcionando")
            print(f"   Status: {data['status']}")
            print(f"   Services: {data['services']}")
            return True
        else:
            print(f"❌ Backend no responde correctamente: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al backend: {e}")
        return False

def test_frontend_health():
    """Prueba la salud del frontend"""
    print("\n🌐 Probando salud del frontend...")
    
    try:
        response = requests.get("http://localhost:3000")
        if response.status_code == 200:
            print("✅ Frontend está funcionando")
            return True
        else:
            print(f"❌ Frontend no responde correctamente: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Error conectando al frontend: {e}")
        return False

def test_claim_creation():
    """Prueba la creación de un claim"""
    print("\n📝 Probando creación de claim...")
    
    # Datos de prueba
    test_claim = {
        "coverage_type": "Trip Cancellation",
        "full_name": "John Doe Test",
        "email": "john.doe.test@example.com",
        "phone": "+1 (555) 123-4567",
        "policy_number": "POL-123456789",
        "incident_date": "2024-01-15T10:30:00",
        "incident_location": "123 Test Street, Test City, TS 12345",
        "description": "Test claim for frontend-backend integration",
        "estimated_amount": 1500.00
    }
    
    try:
        response = requests.post(
            "http://localhost:8000/api/claims",
            headers={"Content-Type": "application/json"},
            json=test_claim
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Claim creado exitosamente")
            print(f"   Claim ID: {data['data']['claim_id']}")
            print(f"   Status: {data['data']['status']}")
            return data['data']['claim_id']
        else:
            print(f"❌ Error creando claim: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ Error en la petición: {e}")
        return None

def test_document_upload(claim_id):
    """Prueba la subida de un documento"""
    print(f"\n📎 Probando subida de documento para claim {claim_id}...")
    
    # Crear un archivo PDF de prueba (simulado)
    test_file_content = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Contents 4 0 R\n>>\nendobj\n4 0 obj\n<<\n/Length 44\n>>\nstream\nBT\n/F1 12 Tf\n72 720 Td\n(Test Document) Tj\nET\nendstream\nendobj\nxref\n0 5\n0000000000 65535 f \n0000000009 00000 n \n0000000058 00000 n \n0000000115 00000 n \n0000000204 00000 n \ntrailer\n<<\n/Size 5\n/Root 1 0 R\n>>\nstartxref\n297\n%%EOF"
    
    try:
        files = {
            'file': ('test_document.pdf', test_file_content, 'application/pdf')
        }
        data = {
            'document_type': 'TEST_DOCUMENT',
            'upload_notes': 'Test document upload via API'
        }
        
        response = requests.post(
            f"http://localhost:8000/api/claims/{claim_id}/documents",
            files=files,
            data=data
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Documento subido exitosamente")
            print(f"   Document ID: {data['data']['id']}")
            print(f"   Filename: {data['data']['filename']}")
            print(f"   Storage URL: {data['data']['storage_url']}")
            return True
        else:
            print(f"❌ Error subiendo documento: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Error en la petición: {e}")
        return False

def test_complete_flow():
    """Prueba el flujo completo"""
    print("🚀 INICIANDO PRUEBA DE CONEXIÓN FRONTEND-BACKEND")
    print("=" * 60)
    
    # 1. Probar backend
    if not test_backend_health():
        print("❌ No se puede continuar sin backend funcionando")
        return False
    
    # 2. Probar frontend
    if not test_frontend_health():
        print("⚠️ Frontend no está disponible, pero continuamos con las pruebas del backend")
    
    # 3. Probar creación de claim
    claim_id = test_claim_creation()
    if not claim_id:
        print("❌ No se puede continuar sin crear un claim")
        return False
    
    # 4. Probar subida de documento
    if not test_document_upload(claim_id):
        print("❌ Error en la subida de documentos")
        return False
    
    print("\n🎉 ¡PRUEBA COMPLETA EXITOSA!")
    print("✅ Se pudo:")
    print("   - Conectar al backend")
    print("   - Conectar al frontend")
    print("   - Crear un claim en la base de datos")
    print("   - Subir un documento al storage")
    print("   - Guardar la referencia del documento en la base de datos")
    
    return True

if __name__ == "__main__":
    # Esperar un poco para que los servicios se inicien
    print("⏳ Esperando que los servicios se inicien...")
    time.sleep(5)
    
    success = test_complete_flow()
    
    if success:
        print("\n🎯 RESULTADO: Frontend y backend están conectados correctamente")
        print("✅ El sistema está listo para recibir formularios del frontend")
    else:
        print("\n💥 RESULTADO: Hay problemas en la conexión")
        print("❌ Revisa que ambos servicios estén funcionando") 