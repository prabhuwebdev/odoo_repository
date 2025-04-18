from odoo import models, fields, api

class SchoolAcademicTerm(models.Model):
    _name = 'school_management.academic.term'
    _description = 'Academic Term'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string='Term Name')
    academic_year_id = fields.Many2one('school_management.academic.year', string='Academic Year', required=True)
    sequence = fields.Integer(string='Sequence', default=1)
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


    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name and not record.start_date:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name} - {record.start_date}"
