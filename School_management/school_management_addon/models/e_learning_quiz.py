from odoo import models, fields, api

class ELearningQuiz(models.Model):
    _name = 'school_management.e.learning.quiz'
    _description = 'E-Learning Quiz'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string="Quiz Title", required=True)
    content_id = fields.Many2one('school_management.e.learning.content', string="E-Learning Content")
    description = fields.Html(string="Description")
    time_limit = fields.Integer(string="Time Limit (minutes)")
    passing_score = fields.Float(string="Passing Score (%)", default=60.0)
    allow_multiple_attempts = fields.Boolean(string="Allow Multiple Attempts", default=True)
    max_attempts = fields.Integer(string="Maximum Attempts", default=3)
    show_correct_answers = fields.Boolean(string="Show Correct Answers", default=True)
    randomize_questions = fields.Boolean(string="Randomize Questions", default=False)
    active = fields.Boolean(string="Active", default=True)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name}"