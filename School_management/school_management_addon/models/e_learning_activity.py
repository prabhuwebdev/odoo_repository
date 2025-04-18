from odoo import models, fields, api

class ELearningActivity(models.Model):
    _name = 'school_management.e.learning.activity'
    _description = 'E-Learning Activity'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    student_id = fields.Many2one('res.partner', string="Student")
    course_id = fields.Many2one('school_management.e.learning.course', string="Course")
    content_id = fields.Many2one('school_management.e.learning.content', string="Content")

    activity_date = fields.Datetime(string="Activity Date", default=fields.Datetime.now)
    activity_type = fields.Selection([
        ('view', 'View'),
        ('download', 'Download'),
        ('quiz_attempt', 'Quiz Attempt'),
        ('assignment_submit', 'Assignment Submit'),
    ], string="Activity Type")

    time_spent = fields.Float(string="Time Spent (minutes)", default=0.0)
    progress = fields.Float(string="Progress", default=0.0)
    is_completed = fields.Boolean(string="Completed", default=False)
    completion_date = fields.Datetime(string="Completion Date")

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.student_id:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.student_id}"
