from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import timedelta
import random
import string


class AssignmentSubmission(models.Model):
    _name = 'school_management.assignment.submission'
    _description = 'Assignment Submission'

    # name = fields.Char(string="Student ID", readonly=True, default=lambda self: self._generate_student_id())
    student_id = fields.Many2one('school_management.student', string="Student")
    assignment_id = fields.Many2one('school_management.assignment', string="Assignment")
    submission_date = fields.Datetime(string='Submission Date', default=fields.Datetime.now)
    content = fields.Html(string='Submission Content')
    attachment = fields.Binary(string='Attachment')
    marks_obtained = fields.Float(string='Marks Obtained', default=0.0)
    feedback = fields.Text(string='Teacher Feedback')
    state = fields.Selection([
        ('submitted', 'Submitted'),
        ('draft', 'Draft'),
        ('evaluated', 'Evaluated'),
        ('late', 'Late'),
        ('resubmit', 'Resubmit')
    ], string='Status', default='submitted')
    # evaluated_by = fields.Many2one('hr.employee', string='Evaluated By')
    evaluation_date = fields.Datetime(string='Evaluation Date')

# def _generate_student_id(self):
#         """ Generate a unique Student ID """
#         return 'AP-' + ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    