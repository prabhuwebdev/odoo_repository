from odoo import models, fields

class PortalUserGroup(models.Model):
    _name = 'school_management.portal.user.group'
    _description = 'Portal User Group'

    # user_id = fields.Many2one('res.users', string='User')
    group_id = fields.Many2one('school_management.portal.access.group', string='Access Group')
