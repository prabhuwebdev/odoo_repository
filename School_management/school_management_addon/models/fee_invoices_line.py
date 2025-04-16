from odoo import models, fields, api

class FeeInvoiceLine(models.Model):
    _name = 'school_management.fee.invoice.line'
    _description = 'Fee Invoice Line'

    invoice_id = fields.Many2one('school_management.fee.invoice', string='Invoice')
    fee_category_id = fields.Many2one('school_management.fee.category', string='Fee Category')
    amount = fields.Float(string='Amount', default=0.0)
    discount = fields.Float(string='Discount %', default=0.0)
    discount_amount = fields.Float(string='Discount Amount', compute='_compute_discount_amount', store=True)
    final_amount = fields.Float(string='Final Amount', compute='_compute_final_amount', store=True)

    @api.depends('amount', 'discount')
    def _compute_discount_amount(self):
        for line in self:
            line.discount_amount = line.amount * line.discount / 100.0

    @api.depends('amount', 'discount_amount')
    def _compute_final_amount(self):
        for line in self:
            line.final_amount = line.amount - line.discount_amount