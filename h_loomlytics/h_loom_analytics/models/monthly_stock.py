from odoo import models, fields, api

class MonthlyStockManagement(models.Model):
    _name = "monthly.stock.management"
    _description = "Monthly Stock Management"

    month = fields.Integer(string="Month")
    year = fields.Integer(string="Year")
    product = fields.Char(string="Product")
    product_group = fields.Char(string="Product Group")
    floor = fields.Char(string="Floor")
    section = fields.Char(string="Section")
    supplier = fields.Char(string="Supplier")
    invoice_number = fields.Char(string="Invoice Number")
    invoice_date = fields.Date(string="Invoice Date")
    closing_quantity = fields.Float(string="Closing Quantity")
    sale_rate = fields.Float(string="Sale Rate")
