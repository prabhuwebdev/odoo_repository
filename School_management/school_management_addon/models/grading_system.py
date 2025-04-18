from odoo import models, fields, api

class GradingSystem(models.Model):
    _name = 'school_management.grading.system'
    _description = 'Grading System'

    name = fields.Char(string='Grading System Name')
    description = fields.Text(string='Description')
    pass_percentage = fields.Float(string='Pass Percentage', default=35.0)
    active = fields.Boolean(string='Active', default=True)
