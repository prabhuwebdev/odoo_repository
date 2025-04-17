from odoo import models, fields,api

class PortalUser(models.Model):
    _name = 'school_management.portal.user'
    _description = 'School Portal User'

    display_name = fields.Char(string="Portal User", compute="_compute_name_display", store=False)
    name = fields.Char(string='User Name')
    login = fields.Char(string='Login')
    password = fields.Char(string='Password')
    user_type = fields.Selection([
        ('admin', 'Admin'),
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('parent', 'Parent')
    ], string='User Type')
    # student_id = fields.Many2one('school_management.student', string='Student')
    # parent_id = fields.Many2one('school_management.parent', string='Parent')
    employee_id = fields.Many2one('school_management.employee', string='Employee')
    active = fields.Boolean(string='Active', default=True)
    last_login = fields.Datetime(string='Last Login')

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"
