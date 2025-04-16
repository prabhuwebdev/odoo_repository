from odoo import models, fields, api

class FeePayment(models.Model):
    _name = 'school_management.fee.payment'
    _description = 'Fee Payment'

    display_name = fields.Char(string="Fee Payment",compute="_compute_name_display", store=False)
    name = fields.Char(string='Payment Reference', default='New')
    invoice_id = fields.Many2one('school_management.fee.invoice', string='Invoice')
    student_id = fields.Many2one('school.student', string='Student')
    payment_date = fields.Date(string='Payment Date', default=fields.Date.today)
    amount = fields.Float(string='Amount', default=0.0)
    payment_method = fields.Selection([
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('bank_transfer', 'Bank Transfer'),
        ('online', 'Online')
    ], string='Payment Method')
    reference = fields.Char(string='Reference Number')
    collected_by = fields.Many2one('res.users', string='Collected By')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')
    notes = fields.Text(string='Notes')

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('school.fee.payment') or 'New'
        return super(FeePayment, self).create(vals)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"