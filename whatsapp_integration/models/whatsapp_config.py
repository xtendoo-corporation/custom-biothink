# -*- coding: utf-8 -*-

from odoo import models, fields, api

class WhatsAppConfig(models.Model):
    _name = 'whatsapp.config'
    _description = 'Configuración WhatsApp Business'

    name = fields.Char('Nombre', default='Configuración WhatsApp')
    whatsapp_api_url = fields.Char('API URL', required=True, help='Endpoint base de la API de WhatsApp Business')
    whatsapp_token = fields.Char('Token de acceso', required=True)
    phone_number_id = fields.Char('ID de número de teléfono', required=True)
    webhook_verify_token = fields.Char('Token de verificación Webhook', required=True)
    active = fields.Boolean('Activo', default=True)

    def get_headers(self):
        self.ensure_one()
        return {
            'Authorization': f'Bearer {self.whatsapp_token}',
            'Content-Type': 'application/json',
        }
