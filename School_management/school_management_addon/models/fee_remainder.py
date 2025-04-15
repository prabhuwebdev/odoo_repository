from odoo import models, fields

class FeeReminder(models.Model):
    _name = 'school_management.fee.reminder'
    _description = 'Fee Reminder'

    name = fields.Char(string='Reminder Name')
    days_before_due = fields.Integer(string='Days Before Due', default=0)
    days_after_due = fields.Integer(string='Days After Due', default=0)
    reminder_type = fields.Selection([
        ('email', 'Email'),
        ('sms', 'SMS'),
        ('both', 'Both')
    ], string='Reminder Type')
    subject = fields.Char(string='Subject')
    active = fields.Boolean(string='Active', default=True)
    message_template = fields.Html(string='Message Template')