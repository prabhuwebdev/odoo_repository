from odoo import models, fields, api

class SchoolSection(models.Model):
    _name = 'school_management.section'
    _description = 'Section'

    name = fields.Char(string="Section Name")
    code = fields.Char(string="Section Code")
    class_id = fields.Many2one('school_management.class', string="Class")
    capacity = fields.Integer(string="Capacity", default=40)
    teacher_id = fields.Many2one('res.partner', string="Class Teacher")  # Assuming teachers are stored in res.partner
    room_number = fields.Char(string="Room Number")
    active = fields.Boolean(string="Active", default=True)
