from odoo import fields,models

class SupplierMaster(models.Model):
    _name = "supplier.master"
    _description ="Description about supplier master"

    supplier_name=fields.Char(string="Supplier Name")
    supplier_city = fields.Char(string="Supplier City")
    supplier_gst = fields.Char(string="Supplier GST")