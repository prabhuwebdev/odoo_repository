from odoo import models, fields, api

class Examination(models.Model):
    _name = 'school_management.examination'
    _description = 'Examination'

    name = fields.Char(string='Examination Name')
    exam_type = fields.Selection([
        ('regular', 'Regular'),
        ('midterm', 'Midterm'),
        ('final', 'Final'),
        ('supplementary', 'Supplementary')
    ], string='Examination Type')
    academic_year = fields.Char(string='Academic Year')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    class_ids = fields.Many2many('school_management.class', string='Applicable Classes')
    grade_system_id = fields.Many2one('school_management.grading.system', string='Grading System')
    publish_date = fields.Date(string='Result Publish Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('ongoing', 'Ongoing'),
        ('completed', 'Completed'),
        ('published', 'Published')
    ], string='Status', default='draft')
    description = fields.Text(string='Description')
    
    
    @api.constrains('academic_year')
    def _check_year_validity(self):
        for record in self:
            if record.academic_year and (record.academic_year < 2000 or record.academic_year > 2100):
                raise ValidationError("Academic year must be between 2000 and 2100.")

