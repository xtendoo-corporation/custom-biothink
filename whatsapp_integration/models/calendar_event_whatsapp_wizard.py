# -*- coding: utf-8 -*-
from odoo import models, fields

class CalendarEventWhatsappWizard(models.TransientModel):
    _name = 'calendar.event.whatsapp.wizard'
    _description = 'Asistente para enviar WhatsApp de evento de calendario'

    event_id = fields.Many2one('calendar.event', string='Evento', required=True)
    custom_message = fields.Text('Mensaje personalizado', required=True)

    def action_send(self):
        self.ensure_one()
        self.event_id.action_send_whatsapp_reminder(custom_message=self.custom_message)
        return {'type': 'ir.actions.act_window_close'}
