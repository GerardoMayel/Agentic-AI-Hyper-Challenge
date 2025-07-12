#!/usr/bin/env python3
"""
Script para probar el flujo completo: crear siniestro y subir documento
"""

import requests
import os
import time

API_URL = "http://localhost:8000/api"
PDF_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "Redacted Customer ClaimForm.pdf")

# Datos de ejemplo para el siniestro
claim_data = {
    "coverage_type": "AUTO",
    "full_name": "Gerardo Mayel",
    "email": "gerardo_mayel_fernandez_alamilla@chiefdataaiofficer.com",
    "phone": "555-123-4567",
    "policy_number": "POL123456789",
    "incident_date": "2024-07-06T12:00:00",
    "incident_location": "CDMX, México",
    "description": "Colisión menor en cruce principal.",
    "estimated_amount": 15000.0
}

def crear_siniestro():
    print("\n🚗 Creando siniestro...")
    resp = requests.post(f"{API_URL}/claims", json=claim_data)
    print(f"Status: {resp.status_code}")
    print(f"Respuesta: {resp.json()}")
    if resp.status_code == 200 and resp.json().get("success"):
        return resp.json()["data"]["claim_id"]
    else:
        raise Exception("No se pudo crear el siniestro")

def subir_documento(claim_id):
    print("\n📄 Subiendo documento PDF...")
    with open(PDF_PATH, "rb") as f:
        files = {"file": ("Redacted Customer ClaimForm.pdf", f, "application/pdf")}
        data = {
            "document_type": "CLAIM_FORM",
            "upload_notes": "Documento de prueba automatizada"
        }
        resp = requests.post(f"{API_URL}/claims/{claim_id}/documents", files=files, data=data)
        print(f"Status: {resp.status_code}")
        print(f"Respuesta: {resp.json()}")
        if resp.status_code == 200 and resp.json().get("success"):
            return resp.json()["data"]
        else:
            raise Exception("No se pudo subir el documento")

def main():
    print("=== PRUEBA FLUJO COMPLETO SINIESTRO + DOCUMENTO ===")
    claim_id = crear_siniestro()
    print(f"\n✅ Siniestro creado con claim_id: {claim_id}")
    # Esperar un poco para asegurar que el claim esté en la base
    time.sleep(1)
    doc_info = subir_documento(claim_id)
    print(f"\n✅ Documento subido y registrado:")
    print(f"   - ID: {doc_info['id']}")
    print(f"   - Nombre: {doc_info['filename']}")
    print(f"   - URL: {doc_info['storage_url']}")
    print("\n🎉 Prueba completa exitosa!")

if __name__ == "__main__":
    main() 