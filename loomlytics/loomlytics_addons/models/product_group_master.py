from odoo import fields,models

class ProductGroupMaster(models.Model):
    _name = "product.group.master"
    _description ="Description about product group master"

    product_group_name=fields.Char(string="Product Group Name")