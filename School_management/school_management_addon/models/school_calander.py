from odoo import models, fields, api

class SchoolCalendar(models.Model):
    _name = 'school_management.calendar'
    _description = 'School Calendar'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string='Calendar Name')
    academic_year_id = fields.Many2one('school_management.academic.year', string='Academic Year')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name and not record.start_date:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name} - {record.start_date}"

