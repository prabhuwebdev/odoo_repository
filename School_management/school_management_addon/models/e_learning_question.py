from odoo import models, fields, api

class ELearningQuestion(models.Model):
    _name = 'school_management.e.learning.question'
    _description = 'E-Learning Question'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    quiz_id = fields.Many2one('school_management.e.learning.quiz', string="Quiz")
    question_text = fields.Html(string="Question")
    question_type = fields.Selection(
        selection=[
            ('single_choice', 'Single Choice'),
            ('multiple_choice', 'Multiple Choice'),
            ('true_false', 'True/False'),
            ('short_answer', 'Short Answer'),
            ('essay', 'Essay')
        ],
        string="Question Type"
    )
    points = fields.Float(string="Points", default=1.0)
    difficulty = fields.Selection(
        selection=[
            ('easy', 'Easy'),
            ('medium', 'Medium'),
            ('hard', 'Hard')
        ],
        string="Difficulty",
        default='medium'
    )
    sequence = fields.Integer(string="Sequence", default=10)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.question_type:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.question_type}"
