# 🗄️ MODELO DE DATOS - SISTEMA DE CLAIMS

## 📋 **RESUMEN DEL SISTEMA**

Sistema automático para procesar emails de claims que:
1. **Monitorea** emails entrantes con palabras "claim" o "claims" en el subject
2. **Extrae** toda la información del email (remitente, contenido, adjuntos)
3. **Clasifica** si es un nuevo siniestro o seguimiento
4. **Almacena** documentos en Google Cloud Storage
5. **Registra** todo en base de datos PostgreSQL

---

## 🗂️ **ESTRUCTURA DE TABLAS**

### 📧 **Tabla 1: emails_recibidos**
```sql
CREATE TABLE emails_recibidos (
    id SERIAL PRIMARY KEY,
    gmail_message_id VARCHAR(255) UNIQUE NOT NULL,
    thread_id VARCHAR(255),
    remitente_email VARCHAR(255) NOT NULL,
    remitente_nombre VARCHAR(255),
    destinatario_email VARCHAR(255) NOT NULL,
    subject TEXT NOT NULL,
    contenido_texto TEXT,
    contenido_html TEXT,
    snippet TEXT,
    fecha_recibido TIMESTAMP NOT NULL,
    fecha_procesado TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    metadata JSONB,
    headers JSONB,
    es_nuevo_siniestro BOOLEAN DEFAULT FALSE,
    numero_siniestro VARCHAR(100),
    estado_procesamiento VARCHAR(50) DEFAULT 'pendiente',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 📎 **Tabla 2: documentos_adjuntos**
```sql
CREATE TABLE documentos_adjuntos (
    id SERIAL PRIMARY KEY,
    email_id INTEGER REFERENCES emails_recibidos(id) ON DELETE CASCADE,
    nombre_archivo VARCHAR(255) NOT NULL,
    tipo_mime VARCHAR(100) NOT NULL,
    tamaño_bytes BIGINT NOT NULL,
    gmail_attachment_id VARCHAR(255),
    url_storage VARCHAR(500),
    bucket_name VARCHAR(100) DEFAULT 'claims-documents-zurich-ai',
    ruta_storage VARCHAR(500),
    es_imagen BOOLEAN DEFAULT FALSE,
    es_documento BOOLEAN DEFAULT FALSE,
    contenido_descargado BOOLEAN DEFAULT FALSE,
    fecha_descarga TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 🚨 **Tabla 3: siniestros_reportados**
```sql
CREATE TABLE siniestros_reportados (
    id SERIAL PRIMARY KEY,
    numero_siniestro VARCHAR(100) UNIQUE NOT NULL,
    email_inicial_id INTEGER REFERENCES emails_recibidos(id),
    remitente_email VARCHAR(255) NOT NULL,
    remitente_nombre VARCHAR(255),
    fecha_reporte TIMESTAMP NOT NULL,
    fecha_siniestro DATE,
    tipo_siniestro VARCHAR(100),
    descripcion TEXT,
    estado VARCHAR(50) DEFAULT 'nuevo',
    prioridad VARCHAR(20) DEFAULT 'normal',
    asegurado VARCHAR(255),
    numero_poliza VARCHAR(100),
    monto_estimado DECIMAL(15,2),
    ubicacion_siniestro TEXT,
    notas_internas TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 🔗 **DIAGRAMA DE RELACIONES**

```
┌─────────────────────┐         ┌─────────────────────┐         ┌─────────────────────┐
│   emails_recibidos  │         │ documentos_adjuntos │         │ siniestros_reportados│
├─────────────────────┤         ├─────────────────────┤         ├─────────────────────┤
│ id (PK)             │◄────────│ id (PK)             │         │ id (PK)             │
│ gmail_message_id    │         │ email_id (FK)       │         │ numero_siniestro    │
│ thread_id           │         │ nombre_archivo      │         │ email_inicial_id(FK)│
│ remitente_email     │         │ tipo_mime           │         │ remitente_email     │
│ remitente_nombre    │         │ tamaño_bytes        │         │ remitente_nombre    │
│ destinatario_email  │         │ gmail_attachment_id │         │ fecha_reporte       │
│ subject             │         │ url_storage         │         │ fecha_siniestro     │
│ contenido_texto     │         │ bucket_name         │         │ tipo_siniestro      │
│ contenido_html      │         │ ruta_storage        │         │ descripcion         │
│ snippet             │         │ es_imagen           │         │ estado              │
│ fecha_recibido      │         │ es_documento        │         │ prioridad           │
│ fecha_procesado     │         │ contenido_descargado│         │ asegurado           │
│ metadata (JSONB)    │         │ fecha_descarga      │         │ numero_poliza       │
│ headers (JSONB)     │         │ created_at          │         │ monto_estimado      │
│ es_nuevo_siniestro  │         │ updated_at          │         │ ubicacion_siniestro │
│ numero_siniestro    │         └─────────────────────┘         │ notas_internas      │
│ estado_procesamiento│                                        │ created_at          │
│ created_at          │                                        │ updated_at          │
│ updated_at          │                                        └─────────────────────┘
└─────────────────────┘
```

---

## 🔄 **FLUJO DE PROCESAMIENTO**

### 1. **Detección de Email**
```
Email llega → Filtro por "claim/claims" en subject → Extraer datos completos
```

### 2. **Análisis de Contenido**
```
Contenido → Análisis con AI → Determinar si es nuevo siniestro
```

### 3. **Procesamiento de Adjuntos**
```
Adjuntos → Descarga → Almacenamiento en GCS → URLs en BD
```

### 4. **Clasificación de Siniestro**
```
Nuevo siniestro → Crear registro → Generar número único
Seguimiento → Vincular a siniestro existente
```

---

## 📊 **ÍNDICES RECOMENDADOS**

```sql
-- Índices para emails_recibidos
CREATE INDEX idx_emails_gmail_message_id ON emails_recibidos(gmail_message_id);
CREATE INDEX idx_emails_remitente ON emails_recibidos(remitente_email);
CREATE INDEX idx_emails_fecha_recibido ON emails_recibidos(fecha_recibido);
CREATE INDEX idx_emails_subject_claim ON emails_recibidos USING gin(to_tsvector('english', subject));
CREATE INDEX idx_emails_es_nuevo_siniestro ON emails_recibidos(es_nuevo_siniestro);

-- Índices para documentos_adjuntos
CREATE INDEX idx_docs_email_id ON documentos_adjuntos(email_id);
CREATE INDEX idx_docs_gmail_attachment_id ON documentos_adjuntos(gmail_attachment_id);
CREATE INDEX idx_docs_url_storage ON documentos_adjuntos(url_storage);

-- Índices para siniestros_reportados
CREATE INDEX idx_siniestros_numero ON siniestros_reportados(numero_siniestro);
CREATE INDEX idx_siniestros_remitente ON siniestros_reportados(remitente_email);
CREATE INDEX idx_siniestros_fecha_reporte ON siniestros_reportados(fecha_reporte);
CREATE INDEX idx_siniestros_estado ON siniestros_reportados(estado);
CREATE INDEX idx_siniestros_numero_poliza ON siniestros_reportados(numero_poliza);
```

---

## 🎯 **CASOS DE USO**

### **Caso 1: Nuevo Siniestro**
1. Email con "claim" en subject
2. Análisis determina que es nuevo reporte
3. Se crea registro en `siniestros_reportados`
4. Se genera número único de siniestro
5. Se procesan adjuntos

### **Caso 2: Seguimiento de Siniestro**
1. Email de remitente existente
2. Se vincula a siniestro existente
3. Se actualizan documentos
4. Se registra seguimiento

### **Caso 3: Documentos Adicionales**
1. Email con adjuntos
2. Se descargan a Google Cloud Storage
3. Se generan URLs públicas
4. Se registran en `documentos_adjuntos`

---

## 🔧 **CONFIGURACIÓN DE GOOGLE CLOUD STORAGE**

### **Estructura de Carpetas**
```
claims-documents-zurich-ai/
├── documentos/
│   ├── siniestro-001/
│   │   ├── email-001/
│   │   │   ├── foto_daño.jpg
│   │   │   └── reporte.pdf
│   │   └── email-002/
│   │       └── documento_adicional.pdf
│   └── siniestro-002/
│       └── email-001/
│           └── evidencia.pdf
```

### **URLs Generadas**
```
https://storage.googleapis.com/claims-documents-zurich-ai/documentos/siniestro-001/email-001/foto_daño.jpg
```

---

## 📈 **MÉTRICAS Y MONITOREO**

### **KPIs del Sistema**
- Emails procesados por día
- Nuevos siniestros detectados
- Documentos almacenados
- Tiempo de procesamiento
- Tasa de éxito en clasificación

### **Alertas**
- Emails no procesados
- Errores en descarga de adjuntos
- Siniestros duplicados
- Fallos en almacenamiento

---

**Estado**: 📋 **DISEÑO COMPLETADO**
**Próximo Paso**: Implementación de modelos SQLAlchemy 