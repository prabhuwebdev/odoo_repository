from odoo import models,fields,api

class FeeCategory(models.Model):
    _name = 'school_management.fee.category'
    _description = 'Fee Category'

    display_name = fields.Char(string="Fee Category",compute="_compute_name_display", store=False)
    name = fields.Char(string='Category Name')
    code = fields.Char(string='Category Code')
    refundable = fields.Boolean(string='Refundable', default=False)
    optional = fields.Boolean(string='Optional', default=False)
    default_amount = fields.Float(string='Default Amount', default=0.0)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)
    fee_assignment_ids = fields.One2many('school_management.fee.assignment', 'fee_category_id',
                                         string="Fee Assignments")

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"