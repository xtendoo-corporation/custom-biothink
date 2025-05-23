# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json

class WhatsAppWebhookController(http.Controller):
    @http.route('/whatsapp/webhook', type='json', auth='public', csrf=False, methods=['POST'])
    def whatsapp_webhook(self, **post):
        # Aquí se procesarán los eventos entrantes de WhatsApp Business Platform
        # Ejemplo: recepción de mensajes, estados, etc.
        # Guardar mensajes recibidos en whatsapp.message
        # Validar el token de verificación si es necesario
        return {'status': 'ok'}

    @http.route('/whatsapp/webhook', type='http', auth='public', csrf=False, methods=['GET'])
    def whatsapp_webhook_verify(self, **kwargs):
        # Verificación inicial del webhook (Meta requiere challenge)
        verify_token = request.env['ir.config_parameter'].sudo().get_param('whatsapp.webhook_verify_token')
        mode = kwargs.get('hub.mode')
        token = kwargs.get('hub.verify_token')
        challenge = kwargs.get('hub.challenge')
        if mode == 'subscribe' and token == verify_token:
            return request.make_response(challenge, headers=[('Content-Type', 'text/plain')])
        return request.make_response('Error: token inválido', headers=[('Content-Type', 'text/plain')])
