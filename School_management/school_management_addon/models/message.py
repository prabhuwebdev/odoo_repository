
from odoo import fields,models,api
class CustomMessage(models.Model):
    _name = 'school_management.message'
    _description = 'Custom Message'

    display_name = fields.Char(string="Message", compute="_compute_name_display", store=False)
    name = fields.Char(string='Subject')
    body = fields.Html(string='Message Body')
    # sender_id = fields.Many2one('res.users', string='Sender')
    message_type = fields.Selection([
        ('general', 'General'),
        ('academic', 'Academic'),
        ('administrative', 'Administrative'),
        ('urgent', 'Urgent')
    ], string='Message Type', default='general')
    recipient_type = fields.Selection([
        ('individual', 'Individual'),
        ('group', 'Group'),
        ('all', 'All')
    ], string='Recipient Type')
    date_sent = fields.Datetime(string='Date Sent', default=fields.Datetime.now)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('read', 'Read')
    ], string='Status', default='draft')
    attachment_ids = fields.Many2many('ir.attachment', string='Attachments')

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"
