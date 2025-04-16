from odoo import models,fields,api

class FeeAssignment(models.Model):
    _name = 'school_management.fee.assignment'
    _description = 'Fee Assignment'

    display_name=fields.Char(string="Fee Assignment", compute="_compute_name_display",store=False)

    fee_structure_id = fields.Many2one('school_management.fee.structure', string='Fee Structure')
    fee_category_id = fields.Many2one('school_management.fee.category', string='Fee Category')
    amount = fields.Float(string='Amount', default=0.0)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.amount:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.amount}"