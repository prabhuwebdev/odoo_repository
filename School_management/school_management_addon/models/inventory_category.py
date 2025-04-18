from odoo import models, fields, api

class InventoryCategory(models.Model):
    _name = 'school_management.inventory.category'
    _description = 'Inventory Category'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string='Category Name')
    code = fields.Char(string='Category Code')
    # parent_id = fields.Many2one('school_management.inventory.category', string='Parent Category')
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name and not record.code:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name} - {record.code}"
