from odoo import models,fields

class FeeAssignment(models.Model):
    _name = 'school_management.fee.assignment'
    _description = 'Fee Assignment'

    fee_structure_id = fields.Many2one('school_management.fee.structure', string='Fee Structure')
    fee_category_id = fields.Many2one('school_management.fee.category', string='Fee Category')
    amount = fields.Float(string='Amount', default=0.0)
