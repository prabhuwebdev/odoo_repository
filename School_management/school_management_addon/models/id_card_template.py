from odoo import models, fields, api

class IDCardTemplate(models.Model):
    _name = 'school_management.id.card.template'
    _description = 'ID Card Template'

    name = fields.Char(string='Template Name')
    id_type = fields.Selection([('student', 'Student'), ('employee', 'Employee')], string='Type')
    background = fields.Binary(string='Background Image')
    school_logo = fields.Binary(string='School Logo')
    show_barcode = fields.Boolean(string='Show Barcode', default=True)
    show_photo = fields.Boolean(string='Show Photo', default=True)
    show_blood_group = fields.Boolean(string='Show Blood Group', default=True)
    show_emergency_contact = fields.Boolean(string='Show Emergency Contact', default=True)
    header = fields.Html(string='Header Content')
    footer = fields.Html(string='Footer Content')
    is_default = fields.Boolean(string='Is Default', default=False)
    active = fields.Boolean(string='Active', default=True)
