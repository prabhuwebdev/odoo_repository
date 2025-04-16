from odoo import models, fields,api

class FeeReminder(models.Model):
    _name = 'school_management.fee.reminder'
    _description = 'Fee Reminder'

    display_name = fields.Char(string="Fee Remainder",compute="_compute_name_display", store=False)
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

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"