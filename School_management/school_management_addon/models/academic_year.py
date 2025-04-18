from odoo import models, fields, api

class SchoolAcademicYear(models.Model):
    _name = 'school_management.academic.year'
    _description = 'Academic Year'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string='Academic Year')
    code = fields.Char(string='Code')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    description = fields.Text(string='Description')
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('active', 'Active'),
            ('closed', 'Closed')
        ],
        string='Status',
        default='draft'
    )
    sequence = fields.Integer(string='Sequence', default=10)


    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name and not record.code:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name} - {record.code}"
