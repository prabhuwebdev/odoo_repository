from odoo import models,fields,api


class FeeStructure(models.Model):
    _name = 'school_management.fee.structure'
    _description = 'Fee Structure'

    name = fields.Char(string='Fee Structure Name')
    code = fields.Char(string='Structure Code')
    academic_year_id = fields.Many2one('academic.year', string='Academic Year')
    class_id = fields.Many2one('school.class', string='Class')  # Assuming manyZone was a typo for many2one
    Frequency = fields.Selection([
        ('annual', 'Annual'),
        ('half-yearly', 'Half-yearly'),
        ('quarterly', 'Quarterly'),
        ('monthly', 'Monthly'),
    ], string='Frequency', default='monthly')
    total_amount = fields.Float(string='Total Amount', default=0.0)
    payment_terms = fields.Text(string='Payment Terms')
    applicable_date = fields.Date(string='Applicable From')
    active = fields.Boolean(string='Active', default=True)

    fee_structure_ids = fields.One2many('school_management.fee.assignment', 'fee_structure_id',
                                        string="Fee Assignments")

