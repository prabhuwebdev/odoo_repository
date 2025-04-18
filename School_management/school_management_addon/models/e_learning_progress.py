from odoo import models, fields, api

class ELearningProgress(models.Model):
    _name = 'school_management.e.learning.progress'
    _description = 'E-Learning Progress'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    student_id = fields.Many2one('res.partner', string="Student")
    course_id = fields.Many2one('school_management.e.learning.course', string="Course")
    enrollment_date = fields.Date(string="Enrollment Date", default=fields.Date.today)

    progress_percentage = fields.Float(string="Progress %", default=0.0)
    completed_modules = fields.Integer(string="Completed Modules", default=0)
    total_modules = fields.Integer(string="Total Modules", compute="_compute_total_modules")
    last_activity = fields.Datetime(string="Last Activity")

    completion_date = fields.Date(string="Completion Date")
    certificate_issued = fields.Boolean(string="Certificate Issued", default=False)
    certificate_date = fields.Date(string="Certificate Date")

    state = fields.Selection([
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('expired', 'Expired'),
    ], string="Status", default="in_progress")

    def _compute_total_modules(self):
        for record in self:
            record.total_modules = self.env['e.learning.module'].search_count([('course_id', '=', record.course_id.id)])


    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.student_id:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.student_id}"