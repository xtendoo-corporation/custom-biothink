# -*- coding: utf-8 -*-
from odoo import api, models

class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    def action_send_whatsapp_reminder(self, custom_message=None):
        """
        Envía un recordatorio de evento por WhatsApp al invitado principal (partner_id), permitiendo mensaje personalizado.
        """
        for event in self:
            partner = event.partner_id or (event.partner_ids and event.partner_ids[0])
            if not partner:
                continue
            if custom_message:
                message = custom_message
            else:
                message = f"Recordatorio: tiene el evento '{event.name}' el día {event.start.strftime('%d/%m/%Y a las %H:%M')}."
            self.env['whatsapp.message'].create_and_send_from_document(
                partner=partner,
                message=message,
                document=None
            )
