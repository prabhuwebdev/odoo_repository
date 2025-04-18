from odoo import models, fields,api

class InventoryItem(models.Model):
    _name = 'school_management.inventory.item'
    _description = 'Inventory Item'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string='Item Name')
    code = fields.Char(string='Item Code')
    category_id = fields.Many2one('school_management.inventory.category', string='Category')
    unit = fields.Selection([
        ('pcs/set', 'Pcs/Set'),
        ('pack', 'Pack'),
        ('box', 'Box'),
        ('kg', 'Kg'),
        ('liter', 'Liter')
    ], string='Unit of Measure')
    reorder_level = fields.Float(string='Reorder Level', default=0.0)
    current_stock = fields.Float(string='Current Stock', default=0.0)
    value_per_unit = fields.Float(string='Value Per Unit', default=0.0)
    total_value = fields.Float(string='Total Value', compute='_compute_total_value')
    location = fields.Char(string='Storage Location')
    is_asset = fields.Boolean(string='Is Asset', default=False)
    description = fields.Text(string='Description')
    active = fields.Boolean(string='Active', default=True)

    def _compute_total_value(self):
        for rec in self:
            rec.total_value = rec.current_stock * rec.value_per_unit

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name and not record.code:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name} - {record.code}"
