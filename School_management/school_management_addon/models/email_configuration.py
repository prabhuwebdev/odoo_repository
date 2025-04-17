from odoo import models, fields,api

class MailConfiguration(models.Model):
    _name = 'school_management.mail.configuration'
    _description = 'Mail Configuration'

    display_name = fields.Char(string="Email Configuration", compute="_compute_name_display", store=False)
    name = fields.Char(string="Configuration Name", required=True)
    smtp_server = fields.Char(string="SMTP Server")
    smtp_port = fields.Integer(string="SMTP Port")

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"
