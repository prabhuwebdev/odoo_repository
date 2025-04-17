from odoo import models, fields,api

class NotificationTemplate(models.Model):
    _name = 'school_management.notification.template'
    _description = 'Notification Template'

    display_name = fields.Char(string="Notification", compute="_compute_name_display", store=False)
    name = fields.Char(string="Template Name")
    notification_type = fields.Selection([
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('push', 'Push'),
        ('in_app', 'In App'),
    ], string="Notification Type")
    subject = fields.Char(string="Subject")
    body = fields.Html(string="Body")
    recipient_type = fields.Selection([
        ('all', 'All'),
        ('student', 'Student'),
        ('employee', 'Employee'),
        ('parent', 'Parent'),
    ], string="Default Recipients", default='all')
    active = fields.Boolean(string="Active", default=True)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"
