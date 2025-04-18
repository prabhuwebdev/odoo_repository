from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _name = 'school_management.purchase.order'
    _description = 'Purchase Order'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    # name = fields.Char(string='Order Reference', default='New')
    vendor_id = fields.Many2one('res.partner', string='Vendor')
    order_date = fields.Date(string='Order Date', default=fields.Date.today)
    expected_date = fields.Date(string='Expected Delivery Date')
    order_line_ids = fields.One2many('school_management.purchase.order.line','order_id',string='Order Lines')

    total_amount = fields.Float(string='Total Amount', compute='_compute_total_amount')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirmed', 'Confirmed'),
        ('received', 'Received'),
        ('cancelled', 'Cancelled')
    ], string='Status', default='draft')
    notes = fields.Text(string='Notes')

    def _compute_total_amount(self):
        for rec in self:
            rec.total_amount = sum(line.subtotal for line in rec.order_line_ids)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.order_date:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.order_date}"
