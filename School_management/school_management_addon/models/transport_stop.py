from odoo import models, fields, api

class TransportStop(models.Model):
    _name = 'school_management.transport.stop'
    _description = 'Transport Stop'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string="Stop Name")
    route_id = fields.Many2one('school_management.transport.route', string="Route")
    sequence = fields.Integer(string="Sequence", default=10)
    pickup_time = fields.Float(string="Pickup Time")
    drop_time = fields.Float(string="Drop Time")
    coordinates = fields.Char(string="GPS Coordinates")
    active = fields.Boolean(default=True)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name :
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name}"
