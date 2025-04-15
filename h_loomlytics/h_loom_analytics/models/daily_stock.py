from odoo import models, fields, api


class DailyStockManagement(models.Model):
    _name = "daily.stock.management"
    _description = "Daily Stock Management"

    product = fields.Char(string="Product")
    product_group = fields.Char(string="Product Group")
    floor = fields.Char(string="Floor")
    section = fields.Char(string="Section")
    supplier = fields.Char(string="Supplier")
    invoice_number = fields.Char(string="Invoice Number")
    stock_date = fields.Date(string="Stock Date")
    invoice_date = fields.Date(string="Invoice Date")
    closing_quantity = fields.Float(string="Closing Quantity")
    sale_rate = fields.Float(string="Sale Rate")