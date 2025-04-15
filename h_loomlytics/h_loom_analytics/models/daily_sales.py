from odoo import models, fields, api


class DailySalesManagement(models.Model):
    _name = "daily.sales.management"
    _description = "Daily Sales Management"

    product = fields.Char(string="Product")
    product_group = fields.Char(string="Product Group")
    floor = fields.Char(string="Floor")
    section = fields.Char(string="Section")
    supplier = fields.Char(string="Supplier")
    sales_date = fields.Date(string="Sales Date")
    sale_quantity = fields.Integer(string="Sale Quantity")
    sale_amount = fields.Float(string="Sale Amount")