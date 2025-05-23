# WhatsApp Business Integration para Odoo 18.0

Este módulo integra Odoo con la API oficial de WhatsApp Business Platform (Meta), permitiendo enviar y recibir mensajes, adjuntar documentos y automatizar notificaciones.

## Índice
- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso del módulo](#uso-del-módulo)
- [Solución de problemas](#solución-de-problemas)
- [Preguntas frecuentes](#preguntas-frecuentes)
- [Documentación adicional](#documentación-adicional)Business Platform para Odoo 18.0

Este módulo integra Odoo con la API oficial de WhatsApp Business Platform (Meta), permitiendo enviar y recibir mensajes, adjuntar documentos y automatizar notificaciones.

## Índice
- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Uso del módulo](#uso-del-módulo)
- [Solución de problemas](#solución-de-problemas)
- [Preguntas frecuentes](#preguntas-frecuentes)

## Requisitos previos

Antes de utilizar este módulo, necesitarás:

1. **Cuenta de WhatsApp Business API**: Debes tener una cuenta en [Meta for Developers](https://developers.facebook.com/) y haber completado el proceso de solicitud para la API de WhatsApp Business.

2. **Número de teléfono registrado**: Un número de teléfono verificado por WhatsApp para tu empresa.

3. **Credenciales API**: 
   - Token de acceso permanente
   - ID de número de teléfono
   - ID de la aplicación Meta

## Instalación

1. Copia este directorio en tu carpeta de addons de Odoo (`/path/to/odoo/addons/` o una ruta personalizada incluida en tu configuración).

2. Actualiza la lista de módulos desde Odoo:
   - Navegación: Configuración > Aplicaciones
   - Haz clic en "Actualizar lista de aplicaciones"

3. Busca "WhatsApp Business Integration" e instala el módulo.

4. Reinicia el servidor Odoo para aplicar todos los cambios.

## Configuración

### 1. Configuración de la API de WhatsApp

1. Navega a **WhatsApp > Configuración** en el menú principal.

2. Crea un nuevo registro con la siguiente información:
   - **Nombre**: Un nombre descriptivo para esta configuración (ej. "WhatsApp Producción").
   - **URL de API de WhatsApp**: Generalmente `https://graph.facebook.com/v17.0/`.
   - **Token de WhatsApp**: Tu token de acceso permanente generado en Meta for Developers.
   - **ID de número de teléfono**: El ID de tu número de teléfono de WhatsApp Business.
   - **Token de verificación del webhook**: Un token personalizado para verificar las llamadas webhook (puedes crear uno aleatorio).
   - **Activo**: Marcar como activo.

### 2. Configuración del Webhook (Para recibir mensajes)

1. En tu cuenta de Meta for Developers, configura un Webhook con la siguiente URL:
   ```
   https://tu-dominio-odoo.com/whatsapp/webhook
   ```

2. Utiliza el mismo "Token de verificación del webhook" que configuraste en Odoo.

3. Selecciona los siguientes campos para suscribirte:
   - `messages`
   - `message_status`

### 3. Creación de plantillas de mensajes

1. Navega a **WhatsApp > Plantillas**.

2. Crea plantillas para los tipos de mensajes más comunes:
   - Confirmación de pedido
   - Estado de envío
   - Recordatorio de pago
   - Recordatorio de evento/cita

## Uso del módulo

### Enviar mensaje manual desde un registro

1. **Desde un presupuesto/pedido de venta**:
   - Abre el pedido de venta
   - Haz clic en "Acción > Enviar presupuesto por WhatsApp"
   - Personaliza el mensaje si lo deseas
   - Haz clic en "Enviar por WhatsApp"

2. **Desde una factura**:
   - Abre la factura
   - Haz clic en "Acción > Enviar WhatsApp personalizado"
   - Personaliza el mensaje
   - Haz clic en "Enviar por WhatsApp"

3. **Desde un evento del calendario**:
   - Abre el evento
   - Haz clic en "Acción > Enviar recordatorio por WhatsApp"
   - Personaliza el mensaje
   - Haz clic en "Enviar por WhatsApp"

### Ver historial de mensajes

Navega a **WhatsApp > Mensajes** para ver todo el historial de mensajes enviados y recibidos, incluyendo su estado de entrega.

## Solución de problemas

### Problema: Mensaje no enviado
- Verifica que el token de API sea válido y no haya expirado
- Confirma que el número de teléfono del contacto incluya el código de país (ej. +34612345678)
- Revisa los registros de errores en el mensaje (WhatsApp > Mensajes)

### Problema: No se reciben mensajes entrantes
- Verifica que el webhook esté correctamente configurado en Meta for Developers
- Comprueba que tu servidor Odoo sea accesible públicamente
- Confirma que el token de verificación coincida exactamente

## Preguntas frecuentes

**¿Puedo enviar documentos adjuntos?**
Sí, el módulo permite enviar PDFs de presupuestos, facturas y otros documentos directamente a través de WhatsApp.

**¿Es posible automatizar el envío de mensajes?**
Sí, puedes configurar acciones automatizadas en Odoo para enviar mensajes en eventos específicos (confirmación de pedido, recordatorio de pago, etc.).

**¿Los mensajes enviados quedan registrados en el historial del cliente?**
Sí, todos los mensajes se registran y pueden verse en la sección de WhatsApp > Mensajes, filtrados por cliente.

**¿Necesito un número de WhatsApp Business verificado?**
Sí, debes completar el proceso de verificación de WhatsApp Business para poder utilizar la API oficial.

## Documentación oficial
- [WhatsApp Business Platform](https://business.whatsapp.com/products/business-platform)
- [API Reference](https://developers.facebook.com/docs/whatsapp)

## Documentación adicional
- [Guía de configuración paso a paso](docs/guia_configuracion.md) - Instrucciones detalladas con capturas de pantalla para la configuración inicial

## Notas
- Este módulo cumple con la normativa de privacidad y los términos de uso de WhatsApp Business.
- Requiere cuenta y configuración previa en Meta for Developers.
- La plantilla de mensajes debe estar aprobada por WhatsApp antes de poder utilizarla.
