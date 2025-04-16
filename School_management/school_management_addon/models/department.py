from odoo import models, fields, api


class SchoolDepartment(models.Model):
    _name = 'school_management.department'
    _description = 'Department'

    display_name = fields.Char(string="Department",compute="_compute_name_display", store=False)
    name = fields.Char(string='Department Name')
    code = fields.Char(string='Department Code')
    parent_id = fields.Many2one('school.department', string='Parent Department')
    manager_id = fields.Many2one('school_management.employee', string='Department Head')
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"
