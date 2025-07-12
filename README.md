# Claims Management System

Automated claims management system that processes incoming emails and generates claims automatically.

## 🗄️ Database Configuration

**Base de datos activa:** `claims_ropj_z7d1`
- **Host:** dpg-d1k9hmer433s73c9g7mg-a.oregon-postgres.render.com
- **Usuario:** agent
- **Estado:** ✅ Conectada y funcionando
- **Versión PostgreSQL:** 16.9
- **Tablas:** 2 (CLAIM_FORM, DOCUMENTS)

### 📋 Estructura de Tablas

#### 🏷️ Tabla CLAIM_FORM (15 columnas)
| Campo | Tipo | Nullable | Descripción |
|-------|------|----------|-------------|
| `id` | INTEGER | NOT NULL | Primary Key |
| `claim_id` | VARCHAR(50) | NULL | ID único auto-generado (CLM-XXXXXXXX) |
| `coverage_type` | VARCHAR(100) | NOT NULL | Tipo de cobertura |
| `full_name` | VARCHAR(200) | NOT NULL | Nombre completo |
| `email` | VARCHAR(200) | NOT NULL | Email del cliente |
| `phone` | VARCHAR(50) | NULL | Teléfono |
| `policy_number` | VARCHAR(100) | NULL | Número de póliza |
| `incident_date` | TIMESTAMP | NULL | Fecha del incidente |
| `incident_location` | VARCHAR(500) | NULL | Ubicación del incidente |
| `description` | TEXT | NULL | Descripción del siniestro |
| `estimated_amount` | DOUBLE PRECISION | NULL | Monto estimado |
| `status` | VARCHAR(50) | NULL | Estado del reclamo (PENDING, APPROVED, etc.) |
| `is_active` | BOOLEAN | NULL | Si el registro está activo |
| `created_at` | TIMESTAMP | NULL | Fecha de creación |
| `updated_at` | TIMESTAMP | NULL | Fecha de última actualización |

#### 📄 Tabla DOCUMENTS (15 columnas)
| Campo | Tipo | Nullable | Descripción |
|-------|------|----------|-------------|
| `id` | INTEGER | NOT NULL | Primary Key |
| `claim_form_id` | INTEGER | NOT NULL | Foreign Key → CLAIM_FORM.id |
| `filename` | VARCHAR(255) | NOT NULL | Nombre del archivo en storage |
| `original_filename` | VARCHAR(255) | NOT NULL | Nombre original del archivo |
| `file_type` | VARCHAR(100) | NOT NULL | Tipo MIME del archivo |
| `file_size` | INTEGER | NOT NULL | Tamaño en bytes |
| `document_type` | VARCHAR(100) | NOT NULL | Tipo de documento (POLICE_REPORT, RECEIPT, etc.) |
| `storage_url` | VARCHAR(500) | NOT NULL | URL pública del archivo |
| `storage_path` | VARCHAR(500) | NOT NULL | Ruta en Google Cloud Storage |
| `uploaded_by` | VARCHAR(200) | NULL | Usuario que subió el archivo |
| `upload_notes` | TEXT | NULL | Notas de la subida |
| `is_verified` | BOOLEAN | NULL | Si el documento está verificado |
| `is_active` | BOOLEAN | NULL | Si el registro está activo |
| `uploaded_at` | TIMESTAMP | NULL | Fecha de subida |
| `updated_at` | TIMESTAMP | NULL | Fecha de última actualización |

### 🔗 Relaciones
- **DOCUMENTS** → **CLAIM_FORM** (Many-to-One)
- Un reclamo puede tener múltiples documentos
- Al eliminar un reclamo, se eliminan todos sus documentos (CASCADE)

### 🔑 Índices
- `CLAIM_FORM.claim_id` (UNIQUE)
- `CLAIM_FORM.id` (Primary Key)
- `DOCUMENTS.id` (Primary Key)
- `DOCUMENTS.claim_form_id` (Foreign Key)

### 🌐 URLs de Conexión
**Desarrollo Local (.env):**
```
postgresql://agent:QRp3aBO6eGFT2mXY6p1nTmAxd41QRFJc@dpg-d1k9hmer433s73c9g7mg-a.oregon-postgres.render.com/claims_ropj_z7d1
```

**Producción (render.yaml):**
```
postgresql://agent:DoyP8c9r4AV7Y2x12OyEJub8si46wavT@dpg-d1gb61bipnbc73agtmm0-a.oregon-postgres.render.com/claims_ropj
```

## ☁️ Google Cloud Storage Configuration

**Bucket activo:** `claims-documents-zurich-ai`
- **Project ID:** `velvety-glyph-464401-v6`
- **Folder:** `documentos`
- **Estado:** ✅ Conectado y funcionando
- **Autenticación:** Application Default Credentials (ADC)

### 📁 Estructura de Almacenamiento
```
claims-documents-zurich-ai/
└── documentos/
    └── {claim_id}/
        ├── {document_type}_{timestamp}_{unique_id}.{extension}
        └── ...
```

### 🔧 Funcionalidades Implementadas
- ✅ **Conexión al bucket**
- ✅ **Subida de archivos** con nombres únicos
- ✅ **Generación de rutas** estructuradas por claim_id
- ✅ **Metadatos de archivos** (tamaño, tipo, URL)
- ✅ **Listado de archivos** por claim
- ✅ **Eliminación de archivos**

### 📋 Operaciones Disponibles
- `upload_file()` - Subir archivo con metadatos
- `list_files_by_claim()` - Listar archivos de un reclamo
- `delete_file()` - Eliminar archivo específico
- `get_file_url()` - Obtener URL pública o firmada
- `generate_file_path()` - Generar ruta única para archivo

## 🚀 Features

- **Automatic email processing**: Monitors email `gerardo_mayel_fernandez_alamilla@chiefdataaiofficer.com` for emails containing the keyword "claim"
- **Web dashboard**: Web interface to view and manage claims
- **Cloud storage**: Documents stored in Google Cloud Storage
- **PostgreSQL database**: Persistent storage for claims and documents
- **REST API**: Endpoints for integration with other systems
- **Web forms**: Responsive forms to complete claim information

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Gmail API     │    │   Reflex App    │    │   PostgreSQL    │
│   (Email Input) │───▶│   (Web Server)  │───▶│   (Database)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                              │
                              ▼
                       ┌─────────────────┐
                       │ Google Cloud    │
                       │ Storage         │
                       │ (Documents)     │
                       └─────────────────┘
```

## 📋 Requirements

- Python 3.11+
- PostgreSQL database
- Google Cloud Storage bucket
- Gmail API credentials
- Gemini API key

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone <repository-url>
cd Agentic-AI-Hyper-Challenge
```

### 2. Install dependencies
```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure environment variables
Create `.env` file with the following variables:

```env
# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Google Cloud
GOOGLE_CLOUD_PROJECT_ID=your-project-id
GOOGLE_CLOUD_BUCKET_NAME=your-bucket-name
GOOGLE_APPLICATION_CREDENTIALS_JSON={"type": "service_account", ...}

# Gmail API
GMAIL_CREDENTIALS_JSON={"installed": {"client_id": "...", ...}}
GMAIL_TOKEN_JSON={"token": "...", "refresh_token": "...", ...}

# AI Services
GEMINI_API_KEY=your-gemini-api-key

# Email Services
SENDGRID_API_KEY=your-sendgrid-api-key

# App Configuration
SECRET_KEY=your-secret-key
```

### 4. Configure database
```bash
# Create tables
python create_tables.py

# Or use Alembic for migrations
alembic upgrade head
```

## 🚀 Execution

### Option 1: Using the automated script (Recommended)
```bash
# Make sure the script is executable
chmod +x run_app.sh

# Run the application
./run_app.sh
```

### Option 2: Manual execution
```bash
# Activate virtual environment
source venv/bin/activate

# Run Reflex directly
reflex run

# Or using the Python script
python start_app.py
```

The application will be available at:
- **Dashboard**: http://localhost:3000/dashboard
- **Home**: http://localhost:3000
- **Forms**: http://localhost:3000/claim-form

### Render deployment

1. Connect the repository to Render
2. Configure environment variables in Render
3. The application will deploy automatically

**Production URL**: https://claims-management-system-j7jz.onrender.com

## 📧 Email Processing Flow

1. **Monitoring**: Application checks for new emails every 5 minutes
2. **Detection**: Searches for emails with keyword "claim"
3. **Processing**: Extracts information and attached documents
4. **Storage**: Saves to database and uploads documents to storage
5. **Response**: Sends confirmation email with claim number
6. **Forms**: Provides links to web forms and PDF

## 🔧 API Endpoints

### Email Webhook
```
POST /api/email-webhook
```
Receives incoming emails and processes claims.

### Claims API
```
GET /api/claims
```
Gets list of claims.

```
GET /api/claims/{claim_number}
```
Gets details of a specific claim.

## 🧪 Testing

### Test the application
```bash
python test_complete_flow.py
```

### Test email processing
```bash
python test_claims_email_processing.py
```

## 📊 Dashboard

The web dashboard provides:
- Claims and documents statistics
- Recent claims list
- System status
- Button to manually process emails
- Links to forms and details

## 🔒 Security

- Credentials stored in environment variables
- OAuth2 authentication for Gmail API
- Secure access tokens
- Input data validation

## 📝 Logs

The application logs:
- Email processing
- Errors and exceptions
- System status
- Database activity

## 🚨 Monitoring

- Health check endpoint for monitoring
- Detailed operation logs
- Processing metrics
- External service status

## 📞 Support

For issues or questions:
1. Check application logs
2. Verify environment variable configuration
3. Test individual endpoints
4. Verify connectivity with external services

## 🔄 Updates

To update the application:
1. Pull changes from repository
2. Update dependencies: `pip install -r requirements.txt`
3. Run database migrations if necessary
4. Restart the application

---

**Note**: The application is designed to run continuously and process emails automatically. In production, it's recommended to use a process manager like PM2 or systemd.
