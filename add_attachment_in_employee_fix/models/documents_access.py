from odoo import models


class DocumentAccess(models.Model):
    _inherit = 'documents.access'

    def _prepare_create_values(self, vals_list):
        vals_list = super()._prepare_create_values(vals_list)
        if vals_list[0].get('partner_id') is False:
            vals_list[0]['partner_id'] = self.env.user.partner_id.id
        documents = self.env['documents.document'].browse(
            [vals['document_id'] for vals in vals_list])
        documents.check_access('write')
        return vals_list
