from odoo import models, fields, api

class TransportVehicle(models.Model):
    _name = 'school_management.transport.vehicle'
    _description = 'Transport Vehicle'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string="Vehicle Name")
    registration_number = fields.Char(string="Registration Number")
    make = fields.Char(string="Make")
    model = fields.Char(string="Model")
    year = fields.Integer(string="Year")
    capacity = fields.Integer(string="Capacity")
    fuel_type = fields.Selection([
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('cng', 'CNG'),
        ('electric', 'Electric')],
        string="Fuel Type"
    )
    driver_id = fields.Many2one('res.partner', string="Driver")
    route_id = fields.Many2one('school_management.transport.route', string="Assigned Route")
    gps_device_id = fields.Char(string="GPS Device ID")
    insurance_expiry = fields.Date(string="Insurance Expiry")
    fitness_expiry = fields.Date(string="Fitness Expiry")
    permit_expiry = fields.Date(string="Permit Expiry")
    active = fields.Boolean(default=True)


    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name}"
