from odoo import fields,models

class ProductMaster(models.Model):
    _name = "product.master"
    _description ="Description about product master"

    product_name=fields.Char(string="Product Name")