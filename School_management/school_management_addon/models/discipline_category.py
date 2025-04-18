from odoo import models, fields, api

class DisciplineCategory(models.Model):
    _name = 'school_management.discipline.category'
    _description = 'Discipline Category'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string='Category Name')
    code = fields.Char(string='Category Code')
    
    severity = fields.Selection(
        selection=[
            ('low', 'Low'),
            ('medium', 'Medium'),
            ('high', 'High'),
            ('critical', 'Critical'),
        ],
        string='Severity Level',
        default='medium'
    )

    points = fields.Integer(string='Demerit Points')
    description = fields.Text(string='Description')
    consequences = fields.Text(string='Consequences')
    active = fields.Boolean(string='Active', default=True)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name and not record.code:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name} - {record.code}"

