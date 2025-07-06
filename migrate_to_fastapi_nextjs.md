# 🚀 Migración a FastAPI + Next.js

## Resumen
Migración completa del sistema de gestión de siniestros de Reflex a una arquitectura moderna y escalable:
- **Backend**: FastAPI (Python)
- **Frontend**: Next.js (React/TypeScript)

## ¿Por qué esta migración?

### Problemas con Reflex
- ❌ `reflex export` no genera archivos HTML estáticos
- ❌ Problemas de despliegue en Render
- ❌ Limitaciones en el control del build process
- ❌ Dependencias complejas y conflictivas

### Ventajas de FastAPI + Next.js
- ✅ **FastAPI**: Alto rendimiento, validación automática, documentación automática
- ✅ **Next.js**: Build process robusto, export estático confiable
- ✅ **Separación clara**: Backend y frontend independientes
- ✅ **Despliegue estándar**: Proceso probado y documentado
- ✅ **Escalabilidad**: Arquitectura de microservicios

## Estructura del Proyecto

```
Agentic-AI-Hyper-Challenge/
├── backend/                 # API FastAPI
│   ├── main.py             # Aplicación principal
│   ├── requirements.txt    # Dependencias Python
│   └── app/                # Servicios existentes (reutilizados)
├── frontend/               # Aplicación Next.js
│   ├── package.json        # Dependencias Node.js
│   ├── next.config.js      # Configuración Next.js
│   ├── tailwind.config.js  # Configuración Tailwind
│   └── pages/              # Páginas de la aplicación
└── render.yaml             # Configuración de despliegue
```

## Pasos de Migración

### 1. Preparar el Backend FastAPI

```bash
# Instalar dependencias del backend
cd backend
pip install -r requirements.txt

# Probar el backend localmente
uvicorn main:app --reload --port 8000
```

### 2. Preparar el Frontend Next.js

```bash
# Instalar dependencias del frontend
cd frontend
npm install

# Probar el frontend localmente
npm run dev
```

### 3. Configurar Variables de Entorno

#### Backend (.env)
```env
DATABASE_URL=postgresql://...
GMAIL_CREDENTIALS_FILE=path/to/credentials.json
GOOGLE_CLOUD_STORAGE_BUCKET=your-bucket-name
GEMINI_API_KEY=your-api-key
```

#### Frontend (.env.local)
```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

### 4. Desplegar en Render

#### Backend (Web Service)
- **Build Command**: `pip install --upgrade pip && pip install -r backend/requirements.txt`
- **Start Command**: `cd backend && uvicorn main:app --host 0.0.0.0 --port $PORT`
- **Environment**: Python

#### Frontend (Static Site)
- **Build Command**: `cd frontend && npm install && npm run build`
- **Publish Directory**: `frontend/out`
- **Environment**: Static

## API Endpoints

### Backend FastAPI

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/api/health` | GET | Estado de servicios |
| `/api/claims` | POST | Crear siniestro |
| `/api/claims` | GET | Listar siniestros |
| `/api/claims/{id}` | GET | Obtener siniestro |
| `/api/claims/upload` | POST | Subir documento |

### Documentación Automática
- **Swagger UI**: `https://your-api.onrender.com/docs`
- **ReDoc**: `https://your-api.onrender.com/redoc`

## Ventajas de la Nueva Arquitectura

### 🔧 Desarrollo
- **Separación clara**: Backend y frontend independientes
- **Herramientas estándar**: FastAPI, Next.js, TypeScript
- **Hot reload**: Desarrollo más rápido
- **Type safety**: Menos errores en tiempo de ejecución

### 🚀 Despliegue
- **Build process confiable**: Next.js genera archivos estáticos
- **Escalabilidad**: Backend y frontend escalan independientemente
- **CDN**: Frontend servido desde CDN global
- **API Gateway**: Backend con rate limiting y caching

### 🔒 Seguridad
- **CORS configurado**: Control de acceso entre dominios
- **Validación automática**: Pydantic en FastAPI
- **Autenticación**: JWT tokens
- **HTTPS**: Certificados automáticos en Render

## Migración de Datos

### Base de Datos
- ✅ **Compatible**: Los modelos SQLAlchemy se reutilizan
- ✅ **Migraciones**: Alembic funciona sin cambios
- ✅ **Conexiones**: Configuración PostgreSQL igual

### Servicios
- ✅ **Reutilización**: Todos los servicios existentes funcionan
- ✅ **Gmail API**: Configuración idéntica
- ✅ **Google Cloud Storage**: Sin cambios
- ✅ **Gemini AI**: Integración preservada

## Próximos Pasos

1. **Probar localmente**: Verificar que todo funciona
2. **Desplegar backend**: Configurar en Render
3. **Desplegar frontend**: Configurar en Render
4. **Configurar dominio**: Apuntar a los servicios
5. **Migrar datos**: Si es necesario
6. **Testing**: Pruebas de integración

## Rollback Plan

Si algo sale mal:
1. **Mantener Reflex**: El código original sigue funcionando
2. **Despliegue paralelo**: Probar nueva arquitectura sin afectar producción
3. **Migración gradual**: Mover funcionalidades una por una
4. **DNS fallback**: Redirigir tráfico si es necesario

## Conclusión

Esta migración resuelve todos los problemas de despliegue y proporciona una base sólida para el crecimiento futuro. La arquitectura FastAPI + Next.js es el estándar de la industria y ofrece:

- ✅ **Confiabilidad**: Procesos de build probados
- ✅ **Escalabilidad**: Arquitectura de microservicios
- ✅ **Mantenibilidad**: Código estándar y documentado
- ✅ **Rendimiento**: Optimizaciones automáticas
- ✅ **Seguridad**: Mejores prácticas implementadas 