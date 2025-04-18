from odoo import models, fields, api

class SchoolClass(models.Model):
    _name = 'school_management.class'
    _description = 'Class'

    name = fields.Char(string="Class Name")
    code = fields.Char(string="Class Code")
    sequence = fields.Integer(string="Sequence", default=10)
    # academic_year_id = fields.Many2one('school.academic.year', string="Academic Year")
    grade_level = fields.Integer(string="Grade Level")
    description = fields.Text(string="Description")
    active = fields.Boolean(string="Active", default=True)
