from odoo import models, fields,api

class PortalAccessRight(models.Model):
    _name = 'school_management.portal.access.right'
    _description = 'Portal Access Right'

    # group_id = fields.Many2one('school_management.portal.access.group', string='Access Group')
    # model_id = fields.Many2one('ir.model', string='Model')
    perm_read = fields.Boolean(string='Read Access', default=False)
    perm_write = fields.Boolean(string='Write Access', default=False)
    perm_create = fields.Boolean(string='Create Access', default=False)
    perm_unlink = fields.Boolean(string='Delete Access', default=False)
