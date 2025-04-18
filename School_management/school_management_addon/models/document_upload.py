from odoo import models, fields, api
from datetime import datetime

class DocumentUpload(models.Model):
    _name = 'school_management.document.upload'
    _description = 'Document Upload'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string="Document Name", required=True)
    document_type_id = fields.Many2one('school_management.document.type', string="Document Type")
    model = fields.Char(string="Related Model")
    res_id = fields.Integer(string="Resource ID")
    file = fields.Binary(string="File")
    file_name = fields.Char(string="File Name")
    mime_type = fields.Char(string="MIME Type")
    upload_date = fields.Datetime(string="Upload Date", default=fields.Datetime.now)
    uploaded_by = fields.Many2one('res.users', string="Uploaded By", default=lambda self: self.env.user)
    description = fields.Text(string="Description")
    is_verified = fields.Boolean(string="Verified", default=False)
    verified_by = fields.Many2one('res.users', string="Verified By")
    verification_date = fields.Datetime(string="Verification Date")


    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name}"
