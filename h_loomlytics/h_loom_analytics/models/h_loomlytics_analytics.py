from odoo import fields,models

class h_loomlytics(models.Model):
    _name = "loomlytics.analytics"
    _description = "Information about Loomlytics analytics"

    month=fields.Integer(string="Month")
    year=fields.Integer(string="Year")
    product_group=fields.Char(string="Product Group")
    product=fields.Char(string="Product")
    floor=fields.Char(string="Floor")
    section=fields.Char(string="Section")
    supplier=fields.Char(string="Supplier")
    salqty = fields.Integer(string="Qty")
    salrate = fields.Float(string="Sale Rate")
    salamount=fields.Integer(string="Sales Val")
    # netamount=fields.Integer(string="Net Amount")
