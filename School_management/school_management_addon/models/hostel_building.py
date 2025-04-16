from odoo import models, fields,api

class HostelBuilding(models.Model):
    _name = 'school_management.hostel.building'
    _description = 'Hostel Building'

    display_name = fields.Char(string="Hostel Building",compute="_compute_name_display", store=False)
    name = fields.Char(string='Building Name')
    code = fields.Char(string='Building Code')
    type = fields.Selection([
        ('boys', 'Boys'),
        ('girls', 'Girls'),
        ('staff', 'Staff')
    ], string='Type')
    floors = fields.Integer(string='Number of Floors', default=1)
    warden_id = fields.Many2one('hr.employee', string='Warden')
    address = fields.Text(string='Address')
    capacity = fields.Integer(string='Total Capacity', compute='_compute_capacity')
    available_capacity = fields.Integer(string='Available Capacity', compute='_compute_capacity')
    active = fields.Boolean(string='Active', default=True)

    def _compute_capacity(self):
        # Placeholder logic
        for rec in self:
            rec.capacity = 0
            rec.available_capacity = 0

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"