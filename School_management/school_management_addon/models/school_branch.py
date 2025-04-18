from odoo import models, fields, api

class SchoolBranch(models.Model):
    _name = 'school_management.branch'
    _description = 'School Branch'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string='Branch Name')
    code = fields.Char(string='Branch Code')
    address = fields.Text(string='Address')
    phone = fields.Char(string='Phone')
    email = fields.Char(string='Email')
    principal_id = fields.Many2one('res.partner', string='Principal')  # Assuming the principal is a partner (staff)
    establishment_date = fields.Date(string='Establishment Date')
    accreditation = fields.Char(string='Accreditation')
    board = fields.Char(string='Board')
    total_students = fields.Integer(string='Total Students')
    total_staff = fields.Integer(string='Total Staff', default=0)
    is_main_branch = fields.Boolean(string='Is Main Branch', default=False)
    active = fields.Boolean(string='Active', default=True)


    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name and not record.code:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name} - {record.code}"

