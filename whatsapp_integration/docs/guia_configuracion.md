# Guía de Configuración Paso a Paso: WhatsApp Business Integration

Esta guía te ayudará a configurar correctamente el módulo de integración de WhatsApp Business Platform con Odoo 18.0, con instrucciones detalladas e imágenes para cada paso del proceso.

## Índice
1. [Requisitos previos](#1-requisitos-previos)
2. [Instalación del módulo](#2-instalación-del-módulo)
3. [Configuración de Meta for Developers](#3-configuración-de-meta-for-developers)
4. [Configuración del módulo en Odoo](#4-configuración-del-módulo-en-odoo)
5. [Configuración del Webhook](#5-configuración-del-webhook)
6. [Prueba de la integración](#6-prueba-de-la-integración)

## 1. Requisitos previos

Antes de comenzar, asegúrate de tener:

- Un sistema Odoo 18.0 funcionando correctamente
- Acceso administrativo a Odoo
- Una cuenta de [Meta for Developers](https://developers.facebook.com/)
- Un número de teléfono empresarial que puedas verificar

**Nota importante**: La API de WhatsApp Business Platform es un producto de pago de Meta. Deberás completar el proceso de solicitud y verificación en Meta for Developers.

![Requisitos previos](img/requisitos_previos.png)
*[CAPTURA RECOMENDADA: Página principal de Meta for Developers]*

## 2. Instalación del módulo

### 2.1. Copiar los archivos del módulo

Copia la carpeta `whatsapp_integration` a tu directorio de addons de Odoo:

```bash
cp -r /ruta/origen/whatsapp_integration /ruta/a/addons/odoo
```

### 2.2. Actualizar la lista de aplicaciones

1. Inicia sesión en Odoo con un usuario administrador
2. Ve a **Configuración → Aplicaciones**
3. Haz clic en el botón **Actualizar lista de aplicaciones**

![Actualizar aplicaciones](img/actualizar_apps.png)
*[CAPTURA RECOMENDADA: Pantalla de actualización de lista de aplicaciones]*

### 2.3. Instalar el módulo

1. En la misma pantalla de Aplicaciones, busca "WhatsApp Business Integration"
2. Haz clic en el botón **Instalar**
3. Espera a que se complete la instalación

![Instalar módulo](img/instalar_modulo.png)
*[CAPTURA RECOMENDADA: Resultado de búsqueda y botón de instalación]*

Una vez instalado, verás un nuevo menú "WhatsApp" en la barra de navegación principal.

![Menú WhatsApp](img/menu_whatsapp.png)
*[CAPTURA RECOMENDADA: Menú principal con la opción WhatsApp visible]*

## 3. Configuración de Meta for Developers

### 3.1. Crear una aplicación en Meta for Developers

1. Inicia sesión en [Meta for Developers](https://developers.facebook.com/)
2. Ve a **Mis Aplicaciones**
3. Haz clic en **Crear Aplicación**
4. Selecciona **Empresa** como tipo de aplicación
5. Completa la información requerida y haz clic en **Crear Aplicación**

![Crear aplicación](img/crear_app_meta.png)
*[CAPTURA RECOMENDADA: Formulario de creación de aplicación]*

### 3.2. Configurar WhatsApp Business Platform

1. En el panel de la aplicación, busca **WhatsApp** en la lista de productos
2. Haz clic en **Configurar**
3. Sigue las instrucciones para agregar un número de teléfono de empresa
4. Completa el proceso de verificación del número

![Configurar WhatsApp](img/config_whatsapp_meta.png)
*[CAPTURA RECOMENDADA: Sección de configuración de WhatsApp en Meta for Developers]*

### 3.3. Obtener las credenciales necesarias

1. En la sección de WhatsApp, ve a **Configuración de API**
2. Anota la siguiente información:
   - **ID del número de teléfono**: identificador único para tu número de WhatsApp
   - **Token de acceso permanente**: crea un nuevo token y guárdalo de forma segura

![Credenciales API](img/credenciales_api.png)
*[CAPTURA RECOMENDADA: Página de configuración de API mostrando el ID y opción de generar token]*

## 4. Configuración del módulo en Odoo

### 4.1. Configurar la conexión con WhatsApp

1. En Odoo, ve a **WhatsApp → Configuración**
2. Haz clic en **Crear**
3. Completa el formulario con la siguiente información:
   - **Nombre**: Un nombre descriptivo (ej. "WhatsApp Production")
   - **URL de API de WhatsApp**: `https://graph.facebook.com/v17.0/`
   - **Token de WhatsApp**: Pega el token de acceso permanente que generaste en Meta
   - **ID de número de teléfono**: Ingresa el ID del número de teléfono de WhatsApp
   - **Token de verificación del webhook**: Crea un token personalizado (cadena alfanumérica única)
   - **Activo**: Marca esta casilla

![Configuración Odoo](img/config_odoo.png)
*[CAPTURA RECOMENDADA: Formulario de configuración de WhatsApp en Odoo]*

4. Haz clic en **Guardar**

### 4.2. Crear plantillas de mensajes

1. Ve a **WhatsApp → Plantillas**
2. Haz clic en **Crear**
3. Completa el formulario:
   - **Nombre**: Nombre descriptivo para la plantilla (ej. "Confirmación de Pedido")
   - **Cuerpo de la plantilla**: El texto del mensaje, puedes usar variables como `{{nombre}}` o `{{numero_pedido}}`
   - **Activo**: Marca esta casilla

![Plantilla de mensaje](img/plantilla_mensaje.png)
*[CAPTURA RECOMENDADA: Formulario de creación de plantilla]*

4. Haz clic en **Guardar**
5. Repite este proceso para crear diferentes plantillas según tus necesidades

## 5. Configuración del Webhook

### 5.1. Preparar tu servidor Odoo

Asegúrate de que tu servidor Odoo sea accesible públicamente mediante HTTPS. El webhook de WhatsApp requiere una conexión segura.

### 5.2. Configurar el webhook en Meta for Developers

1. En tu aplicación de Meta for Developers, ve a la sección de **WhatsApp → Configuración**
2. Desplázate hasta **Webhooks** y haz clic en **Configurar webhooks**
3. Ingresa la siguiente información:
   - **URL de devolución de llamada**: `https://tu-dominio-odoo.com/whatsapp/webhook`
   - **Token de verificación**: El mismo token que configuraste en Odoo
   - **Campos para suscribirse**: Selecciona `messages` y `message_status`

![Configuración webhook](img/config_webhook.png)
*[CAPTURA RECOMENDADA: Formulario de configuración del webhook en Meta]*

4. Haz clic en **Verificar y guardar**

Si la configuración es correcta, Meta verificará la conexión con tu servidor Odoo.

## 6. Prueba de la integración

### 6.1. Enviar un mensaje de prueba desde Odoo

1. Ve a **Ventas → Presupuestos**
2. Abre un presupuesto existente (o crea uno nuevo)
3. Asegúrate de que el cliente tenga un número de teléfono móvil con formato internacional (ej. +34612345678)
4. Haz clic en **Acción → Enviar presupuesto por WhatsApp**
5. Se abrirá un asistente donde puedes personalizar el mensaje
6. Haz clic en **Enviar por WhatsApp**

![Enviar mensaje](img/enviar_mensaje.png)
*[CAPTURA RECOMENDADA: Asistente de envío de mensaje desde un presupuesto]*

### 6.2. Verificar el estado del mensaje

1. Ve a **WhatsApp → Mensajes**
2. Busca el mensaje que acabas de enviar
3. Verifica su estado (pendiente, enviado, entregado, leído)

![Estado mensaje](img/estado_mensaje.png)
*[CAPTURA RECOMENDADA: Lista de mensajes mostrando estados]*

### 6.3. Probar la recepción de mensajes

1. Envía un mensaje desde WhatsApp al número de teléfono configurado
2. Ve a **WhatsApp → Mensajes**
3. Verifica que el mensaje entrante aparezca en la lista

![Mensaje recibido](img/mensaje_recibido.png)
*[CAPTURA RECOMENDADA: Lista de mensajes mostrando un mensaje recibido]*

## Solución de problemas comunes

### El webhook no verifica correctamente
- Verifica que tu servidor Odoo sea accesible públicamente mediante HTTPS
- Asegúrate de que el token de verificación sea exactamente el mismo en Odoo y en Meta
- Revisa los registros de Odoo para ver errores específicos

### Los mensajes no se envían
- Verifica que el token de acceso permanente sea válido
- Asegúrate de que el número de teléfono del destinatario incluya el código de país
- Revisa los registros de error en la vista de mensajes

### No se reciben mensajes
- Verifica que el webhook esté correctamente configurado y verificado
- Asegúrate de estar suscrito a los eventos `messages` y `message_status`
- Revisa los registros de Odoo para detectar errores en la recepción

## Soporte adicional

Si necesitas más ayuda con la configuración o tienes problemas específicos, puedes:

1. Revisar la [documentación oficial de WhatsApp Business Platform](https://developers.facebook.com/docs/whatsapp)
2. Contactar con el soporte técnico de tu proveedor
3. Consultar los foros de la comunidad Odoo

---

*Recuerda reemplazar las referencias a imágenes (img/nombre_imagen.png) con capturas de pantalla reales de tu entorno cuando implementes esta guía.*
