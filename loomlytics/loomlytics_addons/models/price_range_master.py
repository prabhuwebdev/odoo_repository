from odoo import fields,models

class PriceRangeMaster(models.Model):
    _name = "price.range.master"
    _description ="Description about price range master"

    price_range=fields.Char(string="Price Range Master")