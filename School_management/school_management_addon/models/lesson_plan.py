from odoo import models, fields, api

class LessonPlan(models.Model):
    _name = 'school_management.lesson.plan'
    _description = 'Lesson Plan'

    name = fields.Char(string='Plan Name')
    # teacher_id = fields.Many2one('hr.employee', string='Teacher')
    subject_id = fields.Many2one('school_management.subject', string='Subject')
    class_id = fields.Many2one('school_management.class', string='Class')
    section_id = fields.Many2one('school_management.section', string='Section')
    start_date = fields.Date(string='Start Date')
    end_date = fields.Date(string='End Date')
    topics = fields.Text(string='Topics Covered')
    teaching_methods = fields.Text(string='Teaching Methods')
    resources = fields.Text(string='Resources Required')
    assessment = fields.Text(string='Assessment Method')
    completed = fields.Boolean(string='Completed', default=False)
    completion_date = fields.Date(string='Completion Date')
    notes = fields.Text(string='Notes')
