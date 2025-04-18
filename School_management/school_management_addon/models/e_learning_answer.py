from odoo import models, fields, api

class ELearningAnswer(models.Model):
    _name = 'school_management.e.learning.answer'
    _description = 'E-Learning Answer'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    question_id = fields.Many2one('school_management.e.learning.question', string="Question")
    answer_text = fields.Html(string="Answer")
    is_correct = fields.Boolean(string="Is Correct", default=False)
    sequence = fields.Integer(string="Sequence", default=10)


    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.question_id:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.question_id}"
