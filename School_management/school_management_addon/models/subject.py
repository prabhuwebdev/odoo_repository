from odoo import models, fields, api

class SchoolSubject(models.Model):
    _name = 'school_management.subject'
    _description = 'Subject'

    name = fields.Char(string="Subject Name")
    code = fields.Char(string="Subject Code")
    type = fields.Selection([
        ('theory', 'Theory'),
        ('practical', 'Practical'),
        ('both', 'Both')
    ], string="Subject Type")
    class_ids = fields.Many2many('school_management.class', string="Applicable Classes")
    teacher_ids = fields.Many2many('res.partner', string="Assigned Teachers")  # Assuming teachers are stored in res.partner
    credit_hours = fields.Float(string="Credit Hours", default=0.0)
    pass_mark = fields.Float(string="Pass Mark", default=35.0)
    max_mark = fields.Float(string="Maximum Mark", default=100.0)
    is_optional = fields.Boolean(string="Optional Subject", default=False)
    description = fields.Text(string="Description")
    active = fields.Boolean(string="Active", default=True)
