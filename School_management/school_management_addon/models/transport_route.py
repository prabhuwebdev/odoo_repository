from odoo import models, fields, api

class TransportRoute(models.Model):
    _name = 'school_management.transport.route'
    _description = 'Transport Route'

    name_display = fields.Char(string="Display",compute="_compute_name_display", store=False)
    name = fields.Char(string="Route Name")
    code = fields.Char(string="Route Code")
    start_point = fields.Char(string="Start Point")
    end_point = fields.Char(string="End Point")
    distance = fields.Float(string="Distance (km)", default=0.0)
    estimated_time = fields.Integer(string="Estimated Time (minutes)", default=0)
    notes = fields.Text(string="Notes")
    active = fields.Boolean(default=True)

    @api.depends()
    def _compute_name_display(self):
        for record in self:
            if not record.name and not record.code:
                record.name_display = "NEW"
            else:
                record.name_display = f"{record.name} - {record.code}"
