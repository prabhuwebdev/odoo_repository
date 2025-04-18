from odoo import models, fields, api

class ReportCardTemplate(models.Model):
    _name = 'school_management.report.card.template'
    _description = 'Report Card Template'

    name = fields.Char(string='Template Name')
    # academic_year_id = fields.Many2one('academic.year', string='Academic Year')
    # class_ids = fields.Many2many('school_management.class', string='Applicable Classes')
    class_ids = fields.Many2many('school_management.class',relation='report_card_template_class_rel',string='Applicable Classes')

    header = fields.Html(string='Header Content')
    footer = fields.Html(string='Footer Content')
    include_attendance = fields.Boolean(string='Include Attendance', default=True)
    include_behavior = fields.Boolean(string='Include Behavior', default=False)
    include_remarks = fields.Boolean(string='Include Remarks', default=True)
    include_signatures = fields.Boolean(string='Include Signatures', default=True)
    principal_signature = fields.Binary(string='Principal Signature')
    active = fields.Boolean(string='Active', default=True)
