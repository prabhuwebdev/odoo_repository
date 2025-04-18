from odoo import models, fields, api

class CertificateIssue(models.Model):
    _name = 'school_management.certificate.issue'
    _description = 'Certificate Issue'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    student_id = fields.Many2one('school_management.student', string='Student')
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
    template_id = fields.Many2one('school_management.certificate.template', string='Certificate Template')
    issue_date = fields.Date(string='Issue Date', default=fields.Date.today)
    purpose = fields.Char(string='Purpose')
    custom_text = fields.Text(string='Custom Text')
    valid_from = fields.Date(string='Valid From', default=fields.Date.today)
    valid_until = fields.Date(string='Valid Until')
    issued_by = fields.Many2one('res.partner', string='Issued By')  # Assuming issued by a partner (e.g., admin or staff)
    print_count = fields.Integer(string='Print Count', default=0)
    last_printed = fields.Datetime(string='Last Printed')

    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('issued', 'Issued'),
            ('cancelled', 'Cancelled')
        ],
        string='Status',
        default='draft'
    )


    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.issue_date:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.issue_date}"
