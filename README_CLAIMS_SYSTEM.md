# 🚨 SISTEMA DE PROCESAMIENTO AUTOMÁTICO DE CLAIMS

## 📋 **DESCRIPCIÓN**

Sistema automatizado para procesar emails de claims que:
- **Monitorea** emails entrantes con palabras "claim" o "claims" en el subject
- **Extrae** toda la información del email (remitente, contenido, adjuntos)
- **Clasifica** si es un nuevo siniestro o seguimiento
- **Almacena** documentos en Google Cloud Storage
- **Registra** todo en base de datos PostgreSQL

---

## 🏗️ **ARQUITECTURA**

### **Servicios Integrados**
- **Gmail API**: Lectura y procesamiento de emails
- **Google Cloud Storage**: Almacenamiento de documentos
- **PostgreSQL**: Base de datos para registros
- **Python/Reflex**: Backend y frontend

### **Flujo de Procesamiento**
```
Email llega → Filtro por keywords → Extracción de datos → Clasificación → Almacenamiento → Base de datos
```

---

## 📦 **INSTALACIÓN Y CONFIGURACIÓN**

### **1. Configurar Variables de Entorno**

Crear archivo `.env` con las siguientes variables:

```bash
# Base de Datos
DATABASE_URL=postgresql://usuario:password@localhost:5432/nombre_db

# Gmail API
GMAIL_USER_EMAIL=tu_email@gmail.com
GMAIL_CREDENTIALS_FILE=credentials.json

# Google Cloud Storage
GOOGLE_CLOUD_PROJECT_ID=velvety-glyph-464401-v6
GOOGLE_CLOUD_STORAGE_BUCKET=claims-documents-zurich-ai
GOOGLE_CLOUD_STORAGE_FOLDER=documentos
```

### **2. Instalar Dependencias**

```bash
pip install -r requirements.txt
```

### **3. Configurar Google Cloud**

```bash
# Autenticación con Google Cloud
gcloud auth application-default login

# Verificar proyecto
gcloud config set project velvety-glyph-464401-v6
```

### **4. Crear Tablas de Base de Datos**

```bash
python create_tables.py
```

---

## 🚀 **USO DEL SISTEMA**

### **Procesamiento Automático de Emails**

```bash
python process_claims_emails.py
```

**Opciones disponibles:**
1. **Procesar emails nuevos**: Busca y procesa emails con palabras clave de claims
2. **Mostrar estadísticas**: Muestra estadísticas del sistema
3. **Salir**: Termina el programa

### **Scripts de Prueba**

```bash
# Probar Gmail API
python gmail_email_test.py

# Probar Google Cloud Storage
python test_storage.py
```

---

## 📊 **MODELO DE DATOS**

### **Tabla: emails_recibidos**
- `id`: Identificador único
- `gmail_message_id`: ID del mensaje de Gmail
- `remitente_email`: Email del remitente
- `subject`: Asunto del email
- `contenido_texto`: Contenido en texto plano
- `contenido_html`: Contenido HTML
- `es_nuevo_siniestro`: Si es un nuevo siniestro
- `numero_siniestro`: Número del siniestro asociado
- `estado_procesamiento`: Estado del procesamiento

### **Tabla: documentos_adjuntos**
- `id`: Identificador único
- `email_id`: Referencia al email
- `nombre_archivo`: Nombre del archivo
- `url_storage`: URL en Google Cloud Storage
- `tipo_mime`: Tipo MIME del archivo
- `contenido_descargado`: Si se descargó correctamente

### **Tabla: siniestros_reportados**
- `id`: Identificador único
- `numero_siniestro`: Número único del siniestro
- `remitente_email`: Email del reportante
- `fecha_reporte`: Fecha del reporte
- `tipo_siniestro`: Tipo de siniestro
- `descripcion`: Descripción del siniestro
- `estado`: Estado del siniestro

---

## 🔧 **CONFIGURACIÓN AVANZADA**

### **Palabras Clave de Claims**

El sistema busca las siguientes palabras en el subject y contenido:
- `claim`, `claims`
- `siniestro`, `siniestros`
- `accidente`, `daño`, `pérdida`
- `robo`, `incendio`, `reclamo`
- `breakdown`, `damage`, `loss`
- `theft`, `fire`, `accident`

### **Estructura de Almacenamiento**

Los documentos se almacenan en Google Cloud Storage con la estructura:
```
claims-documents-zurich-ai/
├── documentos/
│   ├── CLAIM-20241201-1234/
│   │   ├── email-001/
│   │   │   ├── foto_daño.jpg
│   │   │   └── reporte.pdf
│   │   └── email-002/
│   │       └── documento_adicional.pdf
```

### **Generación de Números de Siniestro**

Formato: `CLAIM-YYYYMMDD-XXXX`
- `YYYYMMDD`: Fecha del reporte
- `XXXX`: Número aleatorio de 4 dígitos

---

## 📈 **MONITOREO Y ESTADÍSTICAS**

### **Métricas del Sistema**
- Emails procesados por día
- Nuevos siniestros detectados
- Documentos almacenados
- Tiempo de procesamiento
- Tasa de éxito en clasificación

### **Estados de Procesamiento**
- `pendiente`: Email en cola de procesamiento
- `procesando`: Email siendo procesado
- `completado`: Email procesado exitosamente
- `error`: Error en el procesamiento

---

## 🛠️ **MANTENIMIENTO**

### **Limpieza de Datos**
```sql
-- Emails con errores de procesamiento
SELECT * FROM emails_recibidos WHERE estado_procesamiento = 'error';

-- Documentos no descargados
SELECT * FROM documentos_adjuntos WHERE contenido_descargado = FALSE;
```

### **Backup de Base de Datos**
```bash
pg_dump -h localhost -U usuario -d nombre_db > backup_claims_$(date +%Y%m%d).sql
```

### **Monitoreo de Storage**
```bash
# Listar archivos en bucket
gsutil ls gs://claims-documents-zurich-ai/documentos/
```

---

## 🚨 **SOLUCIÓN DE PROBLEMAS**

### **Error de Conexión a Gmail**
```bash
# Verificar credenciales
python gmail_email_test.py

# Reautenticar si es necesario
gcloud auth application-default login
```

### **Error de Conexión a Base de Datos**
```bash
# Verificar DATABASE_URL en .env
echo $DATABASE_URL

# Probar conexión
python create_tables.py
```

### **Error de Google Cloud Storage**
```bash
# Verificar permisos
gcloud auth list

# Verificar bucket
gsutil ls gs://claims-documents-zurich-ai/
```

---

## 📞 **SOPORTE**

### **Logs del Sistema**
Los logs se muestran en consola con emojis para facilitar la identificación:
- ✅ Éxito
- ❌ Error
- ⚠️ Advertencia
- 🔍 Búsqueda
- 📧 Email
- 📁 Documento

### **Archivos de Configuración**
- `.env`: Variables de entorno
- `credentials.json`: Credenciales de Gmail API
- `requirements.txt`: Dependencias de Python

---

## 🔄 **ACTUALIZACIONES FUTURAS**

### **Próximas Funcionalidades**
- [ ] Integración con AI para análisis de contenido
- [ ] Dashboard web para visualización
- [ ] Notificaciones automáticas
- [ ] API REST para integración externa
- [ ] Reportes automáticos
- [ ] Clasificación automática de documentos

### **Mejoras Planificadas**
- [ ] Procesamiento en tiempo real
- [ ] Análisis de sentimiento
- [ ] Extracción automática de datos
- [ ] Integración con sistemas de seguros
- [ ] Workflow automatizado de aprobación

---

**Estado del Proyecto**: 🟢 **FUNCIONAL**
**Última Actualización**: Diciembre 2024
**Versión**: 1.0.0 