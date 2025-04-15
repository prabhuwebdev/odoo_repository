from odoo import models, fields

class SalesData(models.Model):
    _name = "sales.data"
    _description = "Sales Data"

    month = fields.Selection([
        ('01', '01'), ('02', '02'), ('03', '03'),
        ('04', '04'), ('05', '05'), ('06', '06'),
        ('07', '07'), ('08', '08'), ('09', '09'),
        ('10', '10'), ('11', '11'), ('12', '12')
    ], string="Month")

    year = fields.Integer(string="Year", default=lambda self: fields.Date.today().year)

    item7 = fields.Char(string="Item 7")
    item8 = fields.Char(string="Item 8")
    salqtd = fields.Float(string="Sales Quantity")
    salamount = fields.Float(string="Sales Amount")
    netqtd = fields.Float(string="Net Quantity")
    netamount = fields.Float(string="Net Amount")

