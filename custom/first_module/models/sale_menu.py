from odoo import fields,models


class PriceRangeMaster(models.Model):
    _name = "price.range.master"
    _description = "Price Range Master"

    price_range=fields.Char()

class SectionMaster(models.Model):
    _name="section.master"
    _description = "Section Master"

    section=fields.Char()