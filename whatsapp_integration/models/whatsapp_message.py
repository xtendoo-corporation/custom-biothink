# -*- coding: utf-8 -*-

from odoo import models, fields, api

class WhatsAppMessage(models.Model):
    _name = 'whatsapp.message'
    _description = 'Mensaje WhatsApp'
    _order = 'create_date desc'

    partner_id = fields.Many2one('res.partner', string='Contacto')
    message = fields.Text('Mensaje')
    message_type = fields.Selection([
        ('out', 'Enviado'),
        ('in', 'Recibido')
    ], string='Tipo', default='out')
    status = fields.Selection([
        ('pending', 'Pendiente'),
        ('sent', 'Enviado'),
        ('delivered', 'Entregado'),
        ('read', 'Leído'),
        ('failed', 'Fallido')
    ], string='Estado', default='pending')
    document_id = fields.Many2one('ir.attachment', string='Documento adjunto')
    whatsapp_message_id = fields.Char('ID Mensaje WhatsApp')
    error_message = fields.Text('Error')
    create_date = fields.Datetime('Fecha', readonly=True)

    def send_message(self):
        """
        Envía el mensaje a través de la API de WhatsApp Business Platform (Meta).
        Soporta mensajes de texto y documentos PDF adjuntos.
        """
        self.ensure_one()
        config = self.env['whatsapp.config'].search([('active', '=', True)], limit=1)
        if not config:
            self.status = 'failed'
            self.error_message = 'No hay configuración activa de WhatsApp.'
            return False
        if not self.partner_id or not self.partner_id.mobile:
            self.status = 'failed'
            self.error_message = 'El contacto no tiene número de móvil.'
            return False
        import requests
        headers = config.get_headers()
        base_url = config.whatsapp_api_url.rstrip('/')
        phone_number_id = config.phone_number_id
        to_number = self.partner_id.mobile
        # Si hay documento adjunto, primero subir el archivo
        if self.document_id:
            # Descargar el archivo desde Odoo
            file_content = self.document_id.datas
            import base64
            file_bytes = base64.b64decode(file_content)
            file_name = self.document_id.name or 'documento.pdf'
            # Subir el archivo a WhatsApp (endpoint /media)
            media_url = f"{base_url}/v19.0/{phone_number_id}/media"
            files = {
                'file': (file_name, file_bytes, self.document_id.mimetype or 'application/pdf')
            }
            data = {
                'messaging_product': 'whatsapp'
            }
            try:
                media_resp = requests.post(media_url, headers={k: v for k, v in headers.items() if k != 'Content-Type'}, files=files, data=data, timeout=15)
                if media_resp.status_code == 200:
                    media_id = media_resp.json().get('id')
                else:
                    self.status = 'failed'
                    self.error_message = f"Error subiendo documento: {media_resp.text}"
                    return False
            except Exception as e:
                self.status = 'failed'
                self.error_message = f"Error subiendo documento: {str(e)}"
                return False
            # Enviar el mensaje de documento
            payload = {
                "messaging_product": "whatsapp",
                "to": to_number,
                "type": "document",
                "document": {
                    "id": media_id,
                    "caption": self.message or file_name,
                    "filename": file_name
                }
            }
        else:
            # Mensaje de texto simple
            payload = {
                "messaging_product": "whatsapp",
                "to": to_number,
                "type": "text",
                "text": {"body": self.message}
            }
        # Enviar el mensaje
        url = f"{base_url}/v19.0/{phone_number_id}/messages"
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=15)
            if response.status_code == 200:
                resp_json = response.json()
                self.status = 'sent'
                self.whatsapp_message_id = resp_json.get('messages', [{}])[0].get('id')
                self.error_message = False
                return True
            else:
                self.status = 'failed'
                self.error_message = f"Error {response.status_code}: {response.text}"
                return False
        except Exception as e:
            self.status = 'failed'
            self.error_message = str(e)
            return False

    def action_send_whatsapp(self):
        """
        Acción manual para enviar el mensaje de WhatsApp desde la vista de formulario.
        """
        for record in self:
            record.send_message()

    @api.model
    def create_and_send_from_document(cls, partner, message, document=None):
        """
        Crea y envía automáticamente un mensaje de WhatsApp asociado a un documento (presupuesto, factura, etc.).
        """
        vals = {
            'partner_id': partner.id,
            'message': message,
            'message_type': 'out',
            'status': 'pending',
        }
        if document:
            vals['document_id'] = document.id
        whatsapp_msg = cls.create(vals)
        whatsapp_msg.send_message()
        return whatsapp_msg
