from odoo import models, fields,api

from odoo import models, fields


class MailServerConfiguration(models.Model):
    _name = 'school_management.mail.configuration'
    _description = 'Mail Server Configuration'

    display_name = fields.Char(string="Email Configuration",compute="_compute_name_display", store=False)
    name = fields.Char(string='Configuration Name')
    smtp_server = fields.Char(string='SMTP Server')
    smtp_port = fields.Integer(string='SMTP Port', default=587)

    smtp_encryption = fields.Selection(
        selection=[
            ('none', 'None'),
            ('ssl', 'SSL'),
            ('tls', 'TLS'),
        ],
        string='Encryption',
        default='tls'
    )

    smtp_user = fields.Char(string='SMTP Username')
    smtp_password = fields.Char(string='SMTP Password')
    default_from = fields.Char(string='Default From')

    is_default = fields.Boolean(string='Is Default', default=False)
    active = fields.Boolean(string='Active', default=True)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"
