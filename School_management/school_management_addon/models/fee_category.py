from odoo import models,fields

class FeeCategory(models.Model):
    _name = 'school_management.fee.category'
    _description = 'Fee Category'

    name = fields.Char(string='Category Name')
    code = fields.Char(string='Category Code')
    refundable = fields.Boolean(string='Refundable', default=False)
    optional = fields.Boolean(string='Optional', default=False)
    default_amount = fields.Float(string='Default Amount', default=0.0)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
