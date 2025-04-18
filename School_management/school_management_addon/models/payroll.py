from odoo import models, fields, api

class Payroll(models.Model):
    _name = 'school_management.payroll'
    _description = 'Payroll'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string="Payroll Name")
    date_from = fields.Date(string="Period From")
    date_to = fields.Date(string="Period To")
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('done', 'Done'),
        ('cancelled', 'Cancelled')],
        default='draft', string="Status"
    )

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name :
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name}"
