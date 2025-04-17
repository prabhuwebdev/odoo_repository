from odoo import models, fields,api

class PortalAccessGroup(models.Model):
    _name = 'school_management.portal.access.group'
    _description = 'Portal Access Group'

    display_name = fields.Char(string="Portal Access Group", compute="_compute_name_display", store=False)
    name = fields.Char(string='Group Name')
    access_level = fields.Selection([
        ('limited', 'Limited'),
        ('standard', 'Standard'),
        ('extended', 'Extended'),
        ('admin', 'Admin')
    ], string='Access Level', default='limited')
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"
