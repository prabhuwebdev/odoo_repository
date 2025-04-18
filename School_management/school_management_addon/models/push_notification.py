from odoo import models, fields,api
from datetime import datetime


class PushNotification(models.Model):
    _name = 'school_management.push.notification'
    _description = 'Push Notification'


    display_name = fields.Char(string="Push Notification",compute="_compute_name_display", store=False)
    name = fields.Char(string='Notification Title')
    message = fields.Text(string='Message')

    recipient_type = fields.Selection(
        selection=[
            ('all', 'All'),
            ('student', 'Student'),
            ('employee', 'Employee'),
            ('parent', 'Parent'),
        ],
        string='Recipient Type',
        default='all'
    )

    sent_date = fields.Datetime(string='Sent Date', default=fields.Datetime.now)
    clicked_count = fields.Integer(string='Clicked Count', default=0)
    delivered_count = fields.Integer(string='Delivered Count', default=0)

    # created_by = fields.Many2one('res.users', string='Created By', default=lambda self: self.env.user)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"
