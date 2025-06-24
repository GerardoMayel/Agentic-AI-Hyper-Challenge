# Email Testing Guide - chiefdataaiofficer.com

Esta guía te ayudará a validar que el sistema de email está funcionando correctamente con tu dominio `chiefdataaiofficer.com`.

## 📧 Configuración Requerida

### 1. Variables de Entorno

Asegúrate de tener configuradas las siguientes variables en tu archivo `.env`:

```bash
# SendGrid API Key (requerida)
SENDGRID_API_KEY=your_sendgrid_api_key_here

# Gmail App Password (opcional - para pruebas de recepción)
GMAIL_APP_PASSWORD=your_gmail_app_password_here
```

### 2. Configuración de SendGrid

1. **Verificar Dominio**: Asegúrate de que `chiefdataaiofficer.com` esté verificado en SendGrid
2. **Configurar Remitente**: El email `gerardo_mayel_fernandez_alamilla@chiefdataaiofficer.com` debe estar autorizado
3. **API Key**: Genera una API key con permisos de envío

### 3. Configuración de Gmail (Opcional)

Para las pruebas de recepción, necesitas una contraseña de aplicación de Gmail:

1. Ve a [Google Account Settings](https://myaccount.google.com/)
2. Activa la verificación en dos pasos si no está activada
3. Ve a "Contraseñas de aplicación"
4. Genera una contraseña para "Correo"
5. Usa esa contraseña como `GMAIL_APP_PASSWORD`

## 🚀 Scripts de Prueba

### Script Rápido

Para una prueba básica de envío:

```bash
python quick_email_test.py
```

Este script:
- ✅ Verifica la configuración de SendGrid
- ✅ Envía un email de prueba
- ✅ Confirma el envío exitoso

### Script Completo

Para una validación exhaustiva:

```bash
python email_validation_script.py
```

Este script incluye:
- ✅ Prueba de conexión con SendGrid
- ✅ Envío de emails de prueba
- ✅ Prueba de auto-respuesta
- ✅ Verificación de recepción (si Gmail está configurado)
- ✅ Pruebas de escenarios del MVP de seguros
- ✅ Generación de reporte

## 📋 Escenarios de Prueba

### 1. Prueba Básica de Envío
- **Objetivo**: Verificar que SendGrid puede enviar emails desde tu dominio
- **Resultado Esperado**: Email recibido en `geramfernandez@gmail.com`

### 2. Prueba de Auto-Respuesta
- **Objetivo**: Verificar que puedes recibir respuestas
- **Proceso**: 
  1. Se envía un email solicitando respuesta
  2. Responde manualmente al email recibido
  3. El script verifica la recepción

### 3. Escenarios del MVP de Seguros
- **Acuse de Recibo de Siniestro**
- **Solicitud de Documentos**
- **Actualización de Estado**

## 🔍 Interpretación de Resultados

### ✅ Éxito
```
🎉 ¡Validación completada exitosamente!
✅ SendGrid configurado y funcionando
✅ Emails de prueba enviados correctamente
✅ Dominio chiefdataaiofficer.com validado
✅ Escenarios del MVP probados
```

### ❌ Errores Comunes

#### Error de API Key
```
❌ Error: SENDGRID_API_KEY no está configurada
```
**Solución**: Configura la variable de entorno `SENDGRID_API_KEY`

#### Error de Dominio
```
❌ Error enviando email: 403 Forbidden
```
**Solución**: Verifica que el dominio esté autorizado en SendGrid

#### Error de Rate Limiting
```
❌ Error enviando email: 429 Too Many Requests
```
**Solución**: Espera unos minutos antes de volver a intentar

## 📊 Reportes

El script completo genera un reporte en `email_validation_report.json`:

```json
{
  "timestamp": "2024-01-15T10:30:00",
  "domain": "chiefdataaiofficer.com",
  "from_email": "gerardo_mayel_fernandez_alamilla@chiefdataaiofficer.com",
  "test_email": "geramfernandez@gmail.com",
  "sendgrid_configured": true,
  "gmail_configured": true,
  "test_status": "completed"
}
```

## 🛠️ Solución de Problemas

### SendGrid no funciona
1. Verifica que la API key sea válida
2. Confirma que el dominio esté verificado
3. Revisa los logs de SendGrid

### Gmail no recibe emails
1. Verifica la carpeta de spam
2. Confirma que el dominio no esté en lista negra
3. Revisa la configuración de DNS

### No se pueden verificar respuestas
1. Configura `GMAIL_APP_PASSWORD`
2. Activa la verificación en dos pasos en Gmail
3. Usa una contraseña de aplicación, no tu contraseña normal

## 📞 Soporte

Si encuentras problemas:

1. Revisa los logs del script
2. Verifica la configuración de SendGrid
3. Confirma las variables de entorno
4. Consulta la documentación de SendGrid

## 🎯 Próximos Pasos

Una vez que las pruebas de email funcionen:

1. ✅ Integra el servicio de email en el MVP
2. ✅ Configura el webhook de recepción
3. ✅ Implementa las notificaciones automáticas
4. ✅ Prueba el flujo completo de siniestros 