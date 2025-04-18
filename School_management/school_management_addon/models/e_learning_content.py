from odoo import models, fields, api

class ELearningContent(models.Model):
    _name = 'school_management.e.learning.content'
    _description = 'E-Learning Content'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string="Content Title", required=True)
    module_id = fields.Many2one('school_management.e.learning.module', string="Module")
    sequence = fields.Integer(string="Sequence", default=10)

    content_type = fields.Selection(
        selection=[
            ('video', 'Video'),
            ('document', 'Document'),
            ('quiz', 'Quiz'),
            ('assignment', 'Assignment'),
            ('scorm', 'SCORM')
        ],
        string="Content Type"
    )

    content = fields.Html(string="HTML Content")
    video_url = fields.Char(string="Video URL")
    file = fields.Binary(string="File")
    file_name = fields.Char(string="File Name")
    duration = fields.Float(string="Duration (minutes)", default=0.0)
    is_mandatory = fields.Boolean(string="Mandatory", default=True)
    is_published = fields.Boolean(string="Published", default=False)
    active = fields.Boolean(string="Active", default=True)


    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name}"
