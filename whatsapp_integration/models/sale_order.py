# -*- coding: utf-8 -*-
from odoo import api, models

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def action_send_whatsapp(self):
        """
        Acción para enviar automáticamente el presupuesto por WhatsApp al cliente.
        """
        for order in self:
            partner = order.partner_id
            # Buscar el PDF generado del presupuesto
            pdf_attachment = self.env['ir.attachment'].search([
                ('res_model', '=', 'sale.order'),
                ('res_id', '=', order.id),
                ('mimetype', '=', 'application/pdf')
            ], limit=1)
            message = f"Estimado {partner.name}, le enviamos su presupuesto {order.name}."
            self.env['whatsapp.message'].create_and_send_from_document(
                partner=partner,
                message=message,
                document=pdf_attachment if pdf_attachment else None
            )
