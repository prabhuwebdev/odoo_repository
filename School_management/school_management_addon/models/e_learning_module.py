from odoo import models, fields, api

class ELearningModule(models.Model):
    _name = 'school_management.e.learning.module'
    _description = 'E-Learning Module'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string="Module Name", required=True)
    course_id = fields.Many2one('school_management.e.learning.course', string="Course")
    sequence = fields.Integer(string="Sequence", default=10)

    description = fields.Html(string="Description")
    duration = fields.Float(string="Duration (minutes)", default=0.0)

    is_published = fields.Boolean(string="Published", default=False)
    active = fields.Boolean(string="Active", default=True)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name}"