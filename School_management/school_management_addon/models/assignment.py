from odoo import models, fields, api

class Assignment(models.Model):
    _name = 'school_management.assignment'
    _description = 'Assignment'

    name = fields.Char(string='Assignment Title')
    description = fields.Html(string='Description')
    class_id = fields.Many2one('school_management.class', string='Class')
    section_id = fields.Many2one('school_management.section', string='Section')
    subject_id = fields.Many2one('school_management.subject', string='Subject')
    # teacher_id = fields.Many2one('hr.employee', string='Assigned By')
    assigned_date = fields.Date(string='Assigned Date', default=fields.Date.today)
    due_date = fields.Date(string='Due Date')
    submission_type = fields.Selection([
        ('online', 'Online'),
        ('offline', 'Offline'),
        ('both', 'Both')
    ], string='Submission Type', default='online')
    max_mark = fields.Float(string='Maximum Mark', default=10.0)
    attachment = fields.Binary(string='Attachment')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('assigned', 'Assigned'),
        ('evaluating', 'Evaluating'),
        ('completed', 'Completed')
    ], string='Status', default='draft')
