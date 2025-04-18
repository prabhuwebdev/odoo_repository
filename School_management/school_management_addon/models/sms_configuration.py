from odoo import models, fields,api


class SmsConfiguration(models.Model):
    _name = 'school_management.sms.configuration'
    _description = 'SMS Configuration'


    display_name = fields.Char(string="Email Configuration",compute="_compute_name_display", store=False)
    name = fields.Char(string='Configuration Name')
    provider = fields.Selection(
        selection=[
            ('generic', 'Generic'),
            ('twilio', 'Twilio'),
            ('msg91', 'MSG91'),
            ('custom', 'Custom'),
        ],
        string='SMS Provider'
    )

    api_key = fields.Char(string='API Key')
    api_secret = fields.Char(string='API Secret')
    sender_id = fields.Char(string='Sender ID')
    api_endpoint = fields.Char(string='API Endpoint')

    is_default = fields.Boolean(string='Is Default', default=False)
    active = fields.Boolean(string='Active', default=True)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"