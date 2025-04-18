from odoo import models, fields, api

class GradeRange(models.Model):
    _name = 'school_management.grade.range'
    _description = 'Grade Range'

    grading_system_id = fields.Many2one('school_management.grading.system', string='Grading System')
    name = fields.Char(string='Grade Name')
    min_percentage = fields.Float(string='Minimum Percentage', default=0.0)
    max_percentage = fields.Float(string='Maximum Percentage', default=100.0)
    grade_point = fields.Float(string='Grade Point', default=0.0)
    description = fields.Char(string='Description')
    sequence = fields.Integer(string='Sequence', default=10)
