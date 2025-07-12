# Zurich Claims API - Documentación

API REST para la gestión de siniestros y documentos en Zurich Insurance.

## 🌐 Base URL

- Local: `http://localhost:8000/api`
- Producción: (definir según despliegue)

---

## Endpoints principales

### 1. Crear siniestro
`POST /api/claims`

**Descripción:** Crea un nuevo siniestro en la base de datos.

**Request (JSON):**
```json
{
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
```

**Response (200):**
```json
{
  "success": true,
  "message": "Siniestro guardado correctamente.",
  "data": {
    "id": 1,
    "claim_id": "CLM-XXXXXXX",
    "status": "PENDING"
  }
}
```

---

### 2. Subir documento a un siniestro
`POST /api/claims/{claim_id}/documents`

**Descripción:** Sube un documento (PDF o imagen) asociado a un siniestro.

**Request (multipart/form-data):**
- `file`: archivo PDF o imagen
- `document_type`: tipo de documento (ej: `CLAIM_FORM`)
- `upload_notes`: notas opcionales

**Response (200):**
```json
{
  "success": true,
  "message": "Documento subido correctamente.",
  "data": {
    "id": 1,
    "filename": "CLAIM_FORM_20240706_123456_abcd1234.pdf",
    "storage_url": "https://..."
  }
}
```

---

### 3. Consultar siniestro
`GET /api/claims/{claim_id}`

**Descripción:** Obtiene los detalles de un siniestro y sus documentos asociados.

**Response (200):**
```json
{
  "success": true,
  "message": "Siniestro consultado correctamente.",
  "data": {
    "claim": {
      "id": 1,
      "claim_id": "CLM-XXXXXXX",
      "coverage_type": "AUTO",
      "full_name": "Gerardo Mayel",
      "email": "gerardo_mayel_fernandez_alamilla@chiefdataaiofficer.com",
      "phone": "555-123-4567",
      "policy_number": "POL123456789",
      "incident_date": "2024-07-06T12:00:00",
      "incident_location": "CDMX, México",
      "description": "Colisión menor en cruce principal.",
      "estimated_amount": 15000.0,
      "status": "PENDING",
      "created_at": "2024-07-06T12:01:00"
    },
    "documents": [
      {
        "id": 1,
        "filename": "CLAIM_FORM_20240706_123456_abcd1234.pdf",
        "document_type": "CLAIM_FORM",
        "storage_url": "https://...",
        "uploaded_at": "2024-07-06T12:01:10"
      }
    ]
  }
}
```

---

### 4. Listar siniestros
`GET /api/claims?limit=10&offset=0`

**Descripción:** Lista los siniestros registrados (paginado).

**Response (200):**
```json
{
  "success": true,
  "message": "Lista de siniestros obtenida correctamente.",
  "data": [
    {
      "id": 1,
      "claim_id": "CLM-XXXXXXX",
      "full_name": "Gerardo Mayel",
      "status": "PENDING",
      "created_at": "2024-07-06T12:01:00"
    },
    ...
  ]
}
```

---

## Notas
- Todos los endpoints devuelven un objeto con `success`, `message` y `data`.
- Los mensajes de éxito están pensados para el usuario final.
- El backend valida tipos de archivo y existencia de siniestro antes de subir documentos.
- El campo `storage_url` es la URL del documento en Google Cloud Storage.

---

## Autenticación
Actualmente la API no requiere autenticación (solo para pruebas). En producción se recomienda agregar autenticación y control de acceso.

---

## Última actualización
- Fecha: 2024-07-06
- Autor: Gerardo Mayel / Zurich Claims Team 