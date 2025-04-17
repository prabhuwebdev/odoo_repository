from odoo import models, fields, api
from num2words import num2words

class DealerPurchase(models.Model):
    _name = 'dealer.purchase'
    _description = 'Dealer Purchase Record'

    customer_name = fields.Char(string="Customer Name", required=True)
    phone_number = fields.Char(string="Phone Number", required=True)
    is_dealer = fields.Boolean(string="Is Dealer?", default=True)
    purchase_line_ids = fields.One2many('dealer.purchase.line', 'purchase_id', string="Product Lines")



    total_amount = fields.Float(string="Total Amount", compute="_compute_totals",store=True)
    total_amount_words = fields.Char(string="Total Amount (in Words)", compute="_compute_totals",store=True)


    @api.depends('purchase_line_ids.amount')
    def _compute_totals(self):
        for record in self:
            total = sum(line.amount for line in record.purchase_line_ids)
            record.total_amount = total
            record.total_amount_words = num2words(total, to='currency', lang='en_IN')
            
            
    def action_generate_report(self):
        report_action = self.env.ref('dealer_purchase.action_report_dealer_purchase')
        pdf_content, content_type = report_action._render_qweb_pdf(self.ids)

        # Optionally return a download action
        return {
            'type': 'ir.actions.report',
            'report_type': 'qweb-pdf',
            'report_name': 'dealer_purchase.report_dealer_purchase_document',
            'report_file': 'dealer_purchase.report_dealer_purchase_document',
            'res_model': 'dealer.purchase',
            'res_id': self.id,
        }


class DealerPurchaseLine(models.Model):
    _name = 'dealer.purchase.line'
    _description = 'Dealer Purchase Line'

    purchase_id = fields.Many2one('dealer.purchase', string="Purchase")
    product_name = fields.Char(string="Product")
    # product_name=fields.Many2one("product.product",string="Product")
    unit_price = fields.Float(string="Unit Price")
    hsn_code = fields.Char(string="HSN Code")
    quantity = fields.Integer(string="Quantity")
    discount = fields.Float(string="Discount (%)")
    tax_rate = fields.Float(string="Tax Rate (%)")
    amount = fields.Float(string="Amount", compute="_compute_amount", store=True)
    amount_words = fields.Char(string="Amount in Words", compute="_compute_amount", store=True)

    @api.depends('unit_price', 'quantity', 'discount', 'tax_rate', 'purchase_id.is_dealer')
    def _compute_amount(self):
        for line in self:
            price = line.unit_price * line.quantity
            discount = (line.discount / 100.0) * price if line.purchase_id.is_dealer else 0
            tax = (line.tax_rate / 100.0) * (price - discount)
            total = price - discount + tax
            line.amount = total
            line.amount_words = num2words(total, to='currency', lang='en_IN')
