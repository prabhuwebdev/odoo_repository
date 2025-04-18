from odoo import models, fields,api

class DisciplineIncident(models.Model):
    _name = 'school_management.discipline.incident'
    _description = 'Discipline Incident'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    student_id = fields.Many2one('school_management.student', string='Student')
    class_id = fields.Many2one('school_management.class', string='Class', compute='_compute_class_section', store=True)
    section_id = fields.Many2one('school_management.section', string='Section', compute='_compute_class_section', store=True)
    category_id = fields.Many2one('school_management.discipline.category', string='Incident Category')
    incident_date = fields.Date(string='Incident Date', default=fields.Date.today)
    reported_by = fields.Many2one('res.partner', string='Reported By')  # Assuming the reporter is a partner (e.g., teacher or staff)
    description = fields.Text(string='Description')
    action_taken = fields.Text(string='Action Taken')
    parent_notified = fields.Boolean(string='Parent Notified', default=False)
    notification_date = fields.Date(string='Notification Date')
    follow_up_required = fields.Boolean(string='Follow-up Required', default=False)
    follow_up_date = fields.Date(string='Follow-up Date')
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('reported', 'Reported'),
            ('under_review', 'Under Review'),
            ('action_taken', 'Action Taken'),
            ('closed', 'Closed')
        ],
        string='Status',
        default='draft'
    )
    points_deducted = fields.Integer(string='Points Deducted', compute='_compute_points_deducted', store=True)

    @api.depends('category_id')
    def _compute_points_deducted(self):
        for record in self:
            if record.category_id:
                record.points_deducted = record.category_id.points  # Assuming the category holds the points to be deducted

    @api.depends('student_id')
    def _compute_class_section(self):
        for record in self:
            if record.student_id:
                record.class_id = record.student_id.class_id
                record.section_id = record.student_id.section_id


    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.incident_date:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.incident_date}"
