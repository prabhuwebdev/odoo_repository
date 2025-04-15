from odoo import fields,models

class ProductOrder(models.Model):
    _name = "purchase.order"
    _description ="Description about purchase order"

    supplier_info=fields.Char(string="Supplier Info")
    order_date=fields.Date(string="Order Date")