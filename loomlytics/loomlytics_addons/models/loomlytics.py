from odoo import fields,models



class Loomlytics(models.Model):
    _name="loomlytics.loomlytics"
    _description = "Info About The Loomlytics"

    type=fields.Char(string="Type")
    floor=fields.Char(string="Floor")
    section=fields.Char(string="Section")
    supplier=fields.Char(string="Supplier")
    invno=fields.Char(string="Inv No")
    invdate=fields.Date(string="Inv Date")
    designno=fields.Char(string="Design No")
    openingqty=fields.Float(string="Opening Qty",digits=(10,2))
    closingqty=fields.Float(string="Closing Qty",digits=(10,2))
    salrate=fields.Float(string="Salrate",digits=(10,2))
    avgsales=fields.Float(string="AvgSales",digits=(10,2))
    totalsales=fields.Float(string="TotalSales",digits=(10,2))
    aging=fields.Char(string="Aging")
