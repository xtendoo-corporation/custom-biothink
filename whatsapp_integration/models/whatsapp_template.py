# -*- coding: utf-8 -*-

from odoo import models, fields

class WhatsAppTemplate(models.Model):
    _name = 'whatsapp.template'
    _description = 'Plantilla de Mensaje WhatsApp'

    name = fields.Char('Nombre', required=True)
    template_body = fields.Text('Cuerpo de la plantilla', required=True)
    active = fields.Boolean('Activo', default=True)
