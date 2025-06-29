# 📧 Guía de Procesamiento de Emails - Gmail + Gemini

## 🎯 Objetivo

Crear un sistema que:
1. **Lea emails** con asunto "test" desde Gmail
2. **Extraiga texto** del cuerpo del email
3. **Procese imágenes** adjuntas con Gemini 2.0 Flash Lite
4. **Almacene resultados** en variables para uso posterior

## 🚀 Configuración Inicial

### 1. Variables de Entorno

Asegúrate de tener configuradas en tu archivo `.env`:

```bash
# Gemini API Key
GEMINI_API_KEY=your_gemini_api_key_here

# Resend API Key (para envío de emails)
RESEND_API_KEY=your_resend_api_key_here
```

### 2. Configuración de Gmail API

#### Paso 1: Google Cloud Console
1. Ve a [Google Cloud Console](https://console.cloud.google.com/)
2. Crea un nuevo proyecto o selecciona uno existente

#### Paso 2: Habilitar Gmail API
1. Ve a "APIs & Services" > "Library"
2. Busca "Gmail API" y habilítala

#### Paso 3: Crear Credenciales
1. Ve a "APIs & Services" > "Credentials"
2. Haz clic en "Create Credentials" > "OAuth 2.0 Client IDs"
3. Selecciona "Desktop application"
4. Descarga el archivo JSON

#### Paso 4: Configurar Credenciales
1. Renombra el archivo descargado a `credentials.json`
2. Colócalo en el directorio raíz del proyecto

### 3. Ejecutar Configuración

```bash
# Verificar configuración de Gmail API
python setup_gmail_api.py

# Crear archivo de ejemplo de credenciales
python setup_gmail_api.py --example
```

## 📧 Cómo Usar el Sistema

### 1. Enviar Email de Prueba

Desde tu email personal, envía un email a `geramfernandez@gmail.com` con:
- **Asunto:** `test`
- **Cuerpo:** Cualquier texto
- **Adjuntos:** Imágenes (opcional)

### 2. Procesar Emails

```bash
python email_processor.py
```

### 3. Resultados Esperados

El sistema:
- ✅ Busca emails con asunto "test"
- ✅ Extrae texto del cuerpo del email
- ✅ Procesa imágenes adjuntas con Gemini
- ✅ Almacena resultados en variables
- ✅ Muestra análisis completo en consola

## 🔧 Componentes del Sistema

### 1. GmailService (`app/services/gmail_service.py`)
- Autenticación con Gmail API
- Búsqueda de emails por asunto
- Extracción de contenido y adjuntos
- Manejo de archivos de credenciales

### 2. LLMService (`app/services/llm_service.py`)
- Integración con Google GenAI
- Análisis de imágenes con Gemini 2.0 Flash Lite
- Extracción de texto de imágenes
- Análisis completo de contenido de emails

### 3. EmailProcessor (`email_processor.py`)
- Orquestador principal del sistema
- Integración de Gmail + Gemini
- Procesamiento de múltiples emails
- Almacenamiento de resultados en variables

## 📊 Variables de Salida

### email_text
```python
# Texto extraído del cuerpo del email
email_text = "Contenido del email..."
```

### image_analysis
```python
# Análisis de imágenes adjuntas
image_analysis = {
    "imagen1.jpg": {
        "text_content": "Texto extraído de la imagen",
        "description": "Descripción de la imagen",
        "confidence": "high"
    }
}
```

### complete_analysis
```python
# Análisis completo del email
complete_analysis = {
    "email_text": "Texto del email",
    "attachments_analysis": [...],
    "summary": {
        "summary": "Resumen del email",
        "key_points": ["punto1", "punto2"],
        "action_required": True
    }
}
```

## 🛠️ Solución de Problemas

### Error de Autenticación Gmail
```
❌ Error autenticando con Gmail
```
**Solución:**
1. Verifica que `credentials.json` existe
2. Asegúrate de que Gmail API esté habilitada
3. Revisa los permisos de la aplicación

### Error de Gemini API
```
❌ Cliente de Gemini no disponible
```
**Solución:**
1. Verifica `GEMINI_API_KEY` en `.env`
2. Asegúrate de que la API key sea válida

### No se Encuentran Emails
```
📭 No se encontraron emails con asunto 'test'
```
**Solución:**
1. Envía un email con asunto "test"
2. Verifica que el email llegó a la bandeja de entrada
3. Espera unos minutos para que se indexe

## 📋 Ejemplo de Uso Completo

### 1. Enviar Email de Prueba
```
Asunto: test
Cuerpo: Este es un email de prueba con una imagen adjunta.
Adjunto: imagen.jpg
```

### 2. Ejecutar Procesamiento
```bash
python email_processor.py
```

### 3. Resultado Esperado
```
🚀 Procesador de Emails - Gmail + Gemini
============================================================
✅ Servicios configurados correctamente

📧 Buscando emails con asunto 'test'...
📧 Encontrados 1 emails

📧 Procesando Email 1/1
============================================================
📧 Email ID: 18c1234567890abcdef
📋 Asunto: test
👤 Remitente: tu-email@gmail.com
📅 Fecha: Mon, 23 Jun 2025 22:45:00 +0000
📄 Cuerpo: Este es un email de prueba...
📎 Adjuntos: 1

📄 Texto del Email:
========================================
Este es un email de prueba con una imagen adjunta.
========================================

🖼️  Procesando 1 adjuntos...

📎 Adjunto 1: imagen.jpg
   🔍 Analizando imagen con Gemini...
   ✅ Análisis completado
   📝 Texto extraído: Texto encontrado en la imagen
   📋 Descripción: Imagen con texto
   🎯 Confianza: high

🤖 Analizando contenido completo con Gemini...

📊 Resultados del Análisis Completo
============================================================
📋 Resumen: Email de prueba con imagen adjunta
🎯 Puntos clave: prueba, imagen, texto
⚡ Acción requerida: False

💾 Guardando resultados en variables...
✅ Variables guardadas:
   📄 email_text: 45 caracteres
   🖼️  image_analysis: 1 imágenes
   📊 complete_analysis: Análisis completo disponible

🎯 Variables Finales:
============================================================
📄 email_text: Este es un email de prueba...
🖼️  image_analysis: {"imagen.jpg": {...}}
📊 complete_analysis: {...}

🎉 ¡Procesamiento completado!
💡 Las variables están disponibles para uso posterior
```

## 🎯 Próximos Pasos

1. **Integración con MVP**: Conectar con el sistema de seguros
2. **Webhook de Recepción**: Configurar recepción automática
3. **Procesamiento Automático**: Automatizar el flujo completo
4. **Base de Datos**: Almacenar resultados en PostgreSQL

## 📞 Soporte

Si encuentras problemas:
1. Revisa los logs de error
2. Verifica la configuración de APIs
3. Asegúrate de que las credenciales sean válidas
4. Consulta la documentación de Google Cloud y Gemini 