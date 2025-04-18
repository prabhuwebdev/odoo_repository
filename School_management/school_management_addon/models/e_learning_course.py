from odoo import models, fields, api

class ELearningCourse(models.Model):
    _name = 'school_management.e.learning.course'
    _description = 'E-Learning Course'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string="Course Name", required=True)
    code = fields.Char(string="Course Code")
    subject_id = fields.Many2one('school_management.subject', string="Related Subject")
    class_ids = fields.Many2many('school_management.class', string="Applicable Classes")
    teacher_id = fields.Many2one('res.users', string="Instructor")

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    description = fields.Html(string="Description")
    objectives = fields.Html(string="Learning Objectives")
    prerequisites = fields.Text(string="Prerequisites")

    featured_image = fields.Binary(string="Featured Image")
    duration = fields.Float(string="Duration (hours)", default=0.0)

    is_published = fields.Boolean(string="Published", default=False)
    publish_date = fields.Date(string="Publish Date")
    active = fields.Boolean(string="Active", default=True)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name and not record.code:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name} - {record.code}"