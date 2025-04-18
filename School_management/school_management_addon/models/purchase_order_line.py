from odoo import models, fields, api

class PurchaseOrderLine(models.Model):
    _name = 'school_management.purchase.order.line'
    _description = 'Purchase Order Line'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    order_id = fields.Many2one('school_management.purchase.order', string='Purchase Order', required=True, ondelete='cascade')
    item_id = fields.Many2one('school_management.inventory.item', string='Item')
    description = fields.Text(string='Description')
    quantity = fields.Float(string='Quantity', default=1.0)
    received_quantity = fields.Float(string='Received Quantity', default=0.0)
    unit_price = fields.Float(string='Unit Price', default=0.0)
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal')

    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.unit_price

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.quantity:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.quantity}"
