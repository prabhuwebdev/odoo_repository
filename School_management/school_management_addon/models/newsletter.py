from odoo import models, fields,api

class Newsletter(models.Model):
    _name = 'school_management.newsletter'
    _description = 'Newsletter'

    display_name = fields.Char(string="NewsLetter", compute="_compute_name_display", store=False)

    name = fields.Char(string='Newsletter Title')
    issue_number = fields.Char(string='Issue Number')
    publish_date = fields.Date(string='Publish Date', default=fields.Date.today)
    content = fields.Html(string='Content')
    recipient_type = fields.Selection([
        ('all', 'All'),
        ('student', 'Student'),
        ('employee', 'Employee'),
        ('parent', 'Parent'),
        ('alumni', 'Alumni')
    ], string='Recipient Type', default='all')
    sent = fields.Boolean(string='Sent', default=False)
    sent_date = fields.Datetime(string='Sent Date')
    # attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    # created_by = fields.Many2one('res.users', string='Created By')

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"
