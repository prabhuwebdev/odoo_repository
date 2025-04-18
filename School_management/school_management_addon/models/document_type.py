from odoo import models, fields, api

class DocumentType(models.Model):
    _name = 'school_management.document.type'
    _description = 'Document Type'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string="Document Type", required=True)
    code = fields.Char(string="Code")
    required_for_admission = fields.Boolean(string="Required for Admission", default=False)
    required_for_employee = fields.Boolean(string="Required for Employee", default=False)
    allowed_mime_types = fields.Char(string="Allowed File Types", default="application/pdf")
    max_file_size = fields.Float(string="Max File Size (MB)", default=2.0)
    description = fields.Text(string="Description")
    active = fields.Boolean(string="Active", default=True)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name}"
