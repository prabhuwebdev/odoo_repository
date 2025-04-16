from odoo import models, fields,api

class HostelRoom(models.Model):
    _name = 'school_management.hostel.room'
    _description = 'Hostel Room'

    display_name = fields.Char(string="Hostel Room",compute="_compute_name_display", store=False)
    name = fields.Char(string='Room Number')
    building_id = fields.Many2one('hostel.building', string='Building')
    floor = fields.Integer(string='Floor', default=0)
    room_type = fields.Selection([
        ('standard', 'Standard'),
        ('deluxe', 'Deluxe'),
        ('dormitory', 'Dormitory')
    ], string='Room Type', default='standard')
    capacity = fields.Integer(string='Capacity', default=2)
    occupied = fields.Integer(string='Occupied Beds', compute='_compute_beds')
    available = fields.Integer(string='Available Beds', compute='_compute_beds')
    monthly_fee = fields.Float(string='Monthly Fee', default=0.0)
    amenities = fields.Text(string='Amenities')
    active = fields.Boolean(string='Active', default=True)

    def _compute_beds(self):
        for room in self:
            room.occupied = 0
            room.available = room.capacity

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.display_name = "NEW"
            else:
                record.display_name = f"{record.name}"