from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class SyllabusTracker(models.Model):
    _name = 'school_management.syllabus.tracker'
    _description = 'Syllabus Tracker'

    subject_id = fields.Many2one('school_management.subject', string='Subject')
    class_id = fields.Many2one('school_management.class', string='Class')
    # teacher_id = fields.Many2one('hr.employee', string='Teacher')
    academic_year = fields.Selection(
        selection=[(str(year), str(year)) for year in range(date.today().year, date.today().year - 30, -1)],
        string='Academic Year',
        default=str(date.today().year)
    )

    total_units = fields.Integer(string='Total Units', )
    completed_units = fields.Integer(string='Completed Units', )
    progress = fields.Float(string='Progress', compute='_compute_progress', store=True)
    last_updated = fields.Datetime(string='Last Updated', default=fields.Datetime.now)

    @api.depends('total_units', 'completed_units')
    def _compute_progress(self):
        for record in self:
            if record.total_units:
                record.progress = (record.completed_units / record.total_units) * 100

    @api.constrains('academic_year')
    def _check_year_validity(self):
        for record in self:
            if record.academic_year and (record.academic_year < 2000 or record.academic_year > 2100):
                raise ValidationError("Academic year must be between 2000 and 2100.")
            
    