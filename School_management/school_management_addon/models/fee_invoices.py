from odoo import models,fields,api

class FeeInvoice(models.Model):
    _name = 'school_management.fee.invoice'
    _description = 'Fee Invoice'

    name = fields.Char(string='Invoice Number', default='New')
    student_id = fields.Many2one('student', string='Student')
    fee_structure_id = fields.Many2one('fee.structure', string='Fee Structure')
    invoice_date = fields.Date(string='Invoice Date', default=fields.Date.today)
    due_date = fields.Date(string='Due Date')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('paid', 'Paid'),
        ('partially_paid', 'Partially Paid'),
        ('cancelled', 'Cancelled'),
    ], string='Status', default='draft')
    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount', store=True)
    paid_amount = fields.Float(string='Paid Amount', compute='_compute_paid_amount', store=True)
    balance_amount = fields.Float(string='Balance Amount', compute='_compute_balance_amount', store=True)
    notes = fields.Text(string='Notes')

    @api.depends('fee_structure_id', 'student_id')
    def _compute_total_amount(self):
        for record in self:
            # Logic to calculate total_amount based on fee structure and student
            record.total_amount = 0.0  # Example, add actual calculation logic

    @api.depends('total_amount', 'paid_amount')
    def _compute_balance_amount(self):
        for record in self:
            record.balance_amount = record.total_amount - record.paid_amount

    @api.depends('paid_amount')
    def _compute_paid_amount(self):
        for record in self:
            # Logic to calculate paid amount
            record.paid_amount = 0.0  # Example, add actual calculation logic

