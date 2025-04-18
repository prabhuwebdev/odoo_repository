from odoo import models, fields, api

class CertificateTemplate(models.Model):
    _name = 'school_management.certificate.template'
    _description = 'Certificate Template'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string='Template Name')
    certificate_type = fields.Selection(
        selection=[
            ('transfer', 'Transfer'),
            ('bonafide', 'Bonafide'),
            ('character', 'Character'),
            ('completion', 'Completion'),
            ('appreciation', 'Appreciation'),
            ('participation', 'Participation')
        ],
        string='Certificate Type'
    )
    header = fields.Html(string='Header Content')
    body = fields.Html(string='Body Content')
    footer = fields.Html(string='Footer Content')
    background = fields.Binary(string='Background Image')
    
    paper_format = fields.Selection(
        selection=[
            ('a4', 'A4'),
            ('letter', 'Letter'),
            ('legal', 'Legal')
        ],
        string='Paper Format',
        default='a4'
    )
    orientation = fields.Selection(
        selection=[
            ('portrait', 'Portrait'),
            ('landscape', 'Landscape')
        ],
        string='Orientation',
        default='portrait'
    )
    
    margin_top = fields.Float(string='Top Margin (mm)', default=25.0)
    margin_bottom = fields.Float(string='Bottom Margin (mm)', default=25.0)
    margin_left = fields.Float(string='Left Margin (mm)', default=25.0)
    margin_right = fields.Float(string='Right Margin (mm)', default=25.0)
    
    school_logo = fields.Boolean(string='Show School Logo', default=True)
    school_seal = fields.Boolean(string='Show School Seal', default=True)
    principal_signature = fields.Boolean(string='Show Principal Signature', default=True)
    qr_code = fields.Boolean(string='Include QR Code', default=False)
    
    is_default = fields.Boolean(string='Is Default', default=False)
    active = fields.Boolean(string='Active', default=True)


    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name}"
