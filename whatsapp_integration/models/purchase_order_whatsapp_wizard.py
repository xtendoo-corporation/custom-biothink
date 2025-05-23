# -*- coding: utf-8 -*-
from odoo import models, fields

class PurchaseOrderWhatsappWizard(models.TransientModel):
    _name = 'purchase.order.whatsapp.wizard'
    _description = 'Asistente para enviar WhatsApp de pedido de compra'

    order_id = fields.Many2one('purchase.order', string='Pedido de compra', required=True)
    custom_message = fields.Text('Mensaje personalizado', required=True)

    def action_send(self):
        self.ensure_one()
        partner = self.order_id.partner_id
        pdf_attachment = self.env['ir.attachment'].search([
            ('res_model', '=', 'purchase.order'),
            ('res_id', '=', self.order_id.id),
            ('mimetype', '=', 'application/pdf')
        ], limit=1)
        self.env['whatsapp.message'].create_and_send_from_document(
            partner=partner,
            message=self.custom_message,
            document=pdf_attachment if pdf_attachment else None
        )
        return {'type': 'ir.actions.act_window_close'}
