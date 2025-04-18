from odoo import models, fields,api

class SchoolJobPosition(models.Model):
    _name = 'school_management.job.position'
    _description = 'Job Position'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string='Position Name')
    code = fields.Char(string='Position Code')
    # department_id = fields.Many2one('school_management.school.department', string='Department')
    description = fields.Text(string='Description')
    is_teacher = fields.Boolean(string='Is Teaching Position', default=False)
    active = fields.Boolean(string='Active', default=True)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name and not record.code:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name} - {record.code}"
